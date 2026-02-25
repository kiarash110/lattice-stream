import os, threading, time, lzma, sys, psutil, tarfile, shutil
import multiprocessing
from multiprocessing import Process, Queue
import customtkinter as ctk
from tkinterdnd2 import DND_FILES, TkinterDnD

def get_safe_path(base_dir, name):
    full_path = os.path.join(base_dir, name)
    if not os.path.exists(full_path): return full_path
    fn, ext = os.path.splitext(name)
    counter = 1
    while os.path.exists(os.path.join(base_dir, f"{fn} ({counter}){ext}")):
        counter += 1
    return os.path.join(base_dir, f"{fn} ({counter}){ext}")

def core_compression_task(path, mode, out_path, queue):
    try:
        import zstandard as zstd
        orig_size = os.path.getsize(path) if os.path.isfile(path) else sum(os.path.getsize(os.path.join(r, f)) for r, d, fs in os.walk(path) for f in fs)
        with open(out_path, 'wb') as ofh:
            writer_obj = zstd.ZstdCompressor(level=3).stream_writer(ofh) if mode == "2" else lzma.open(ofh, "wb")
            with tarfile.open(fileobj=writer_obj, mode="w|") as tar:
                # Add the folder and everything inside it
                tar.add(path, arcname=os.path.basename(path))
            writer_obj.close()
        savings = max(0, (1 - (os.path.getsize(out_path) / orig_size)) * 100) if orig_size > 0 else 0
        queue.put(("SUCCESS", out_path, f"{savings:.1f}%"))
    except Exception as e: queue.put(("ERROR", str(e), "0%"))

def core_decompression_task(path, queue):
    try:
        import zstandard as zstd
        work_dir = os.path.abspath(os.path.dirname(path))
        is_zst = path.lower().endswith('.zst')
        final_out = ""
        
        with open(path, 'rb') as ifh:
            reader = zstd.ZstdDecompressor().stream_reader(ifh) if is_zst else lzma.open(ifh)
            with tarfile.open(fileobj=reader, mode="r|") as tar:
                # Extract all members to ensure folders aren't empty
                for member in tar:
                    # Rename the root folder/file if it already exists
                    if "/" not in member.name and "\\" not in member.name:
                        safe_path = get_safe_path(work_dir, member.name)
                        root_name = os.path.basename(safe_path)
                        # Store the original name to update children paths
                        old_root = member.name
                        member.name = root_name
                        final_out = safe_path
                    elif 'old_root' in locals() and member.name.startswith(old_root):
                        # Update sub-files/folders to move into the renamed (n) folder
                        member.name = member.name.replace(old_root, root_name, 1)
                    
                    tar.extract(member, path=work_dir)
            if not is_zst: reader.close()
        queue.put(("SUCCESS", final_out if final_out else work_dir, "EXTRACTED"))
    except Exception as e: queue.put(("ERROR", str(e), "FAIL"))

class LatticeApp(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        self.TkdndVersion = TkinterDnD._require(self)
        self.title("Lattice Unified")
        self.geometry("750x850")
        self.brand_color = "#6200EA"
        self.is_running = False
        self.start_time = 0
        self.current_progress = 0

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(anchor="ne", padx=20, pady=20)
        ctk.CTkButton(self.top_frame, text="THEME", width=80, command=self.toggle_theme, fg_color=self.brand_color).pack()
        
        ctk.CTkLabel(self, text="Lattice", font=("Impact", 60)).pack(pady=5)
        self.mode_var = ctk.StringVar(value="2")
        self.radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.radio_frame.pack(pady=10)
        ctk.CTkRadioButton(self.radio_frame, text="Nitro (Zstd)", variable=self.mode_var, value="2").pack(side="left", padx=30)
        ctk.CTkRadioButton(self.radio_frame, text="Squeeze (Lzma)", variable=self.mode_var, value="1").pack(side="left", padx=30)

        self.path_entry = ctk.CTkEntry(self, placeholder_text="Drop file/folder here", width=550, height=50, border_color=self.brand_color)
        self.path_entry.pack(pady=10)
        self.path_entry.drop_target_register(DND_FILES); self.path_entry.dnd_bind('<<Drop>>', self.handle_drop)

        self.stats_f = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_f.pack(fill="x", padx=60)
        self.stat_time = ctk.CTkLabel(self.stats_f, text="Elapsed: 0.0s", font=("Courier", 13))
        self.stat_time.pack(side="left", expand=True)
        self.stat_ram = ctk.CTkLabel(self.stats_f, text="RAM: 0 MB", font=("Courier", 13))
        self.stat_ram.pack(side="left", expand=True)
        self.stat_savings = ctk.CTkLabel(self.stats_f, text="Saved: 0.0%", font=("Courier", 13))
        self.stat_savings.pack(side="left", expand=True)

        self.progress = ctk.CTkProgressBar(self, width=550)
        self.progress.set(0); self.progress.pack(pady=(20, 0))
        self.perc_label = ctk.CTkLabel(self, text="0%", font=("Arial", 12, "bold"))
        self.perc_label.pack(pady=(5, 10))
        
        self.history_box = ctk.CTkTextbox(self, width=550, height=150, font=("Courier", 12), border_width=1)
        self.history_box.pack(pady=10)
        self.status_text = ctk.CTkLabel(self, text="Ready", font=("Arial", 14), text_color="gray")
        self.status_text.pack(pady=5)

        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        ctk.CTkButton(self.btn_frame, text="Compress", command=lambda: self.trigger("C"), width=200, height=45, fg_color=self.brand_color).pack(side="left", padx=15)
        ctk.CTkButton(self.btn_frame, text="Decompress", command=lambda: self.trigger("D"), width=200, height=45, fg_color=self.brand_color).pack(side="left", padx=15)
        
        threading.Thread(target=self.update_stats_loop, daemon=True).start()

    def toggle_theme(self): ctk.set_appearance_mode("Light" if ctk.get_appearance_mode() == "Dark" else "Dark")
    def handle_drop(self, e): self.path_entry.delete(0, 'end'); self.path_entry.insert(0, e.data.strip('{}'))

    def update_stats_loop(self):
        while True:
            if self.is_running:
                self.stat_time.configure(text=f"Elapsed: {time.time() - self.start_time:.1f}s")
                try:
                    p = psutil.Process(os.getpid())
                    mem = sum(c.memory_info().rss for c in p.children(recursive=True)) + p.memory_info().rss
                    self.stat_ram.configure(text=f"RAM: {mem / (1024*1024):.0f} MB")
                except: pass
                if self.current_progress < 0.95:
                    self.current_progress += 0.01
                    self.progress.set(self.current_progress)
                    self.perc_label.configure(text=f"{int(self.current_progress*100)}%")
            time.sleep(0.1)

    def trigger(self, act):
        path = self.path_entry.get().strip().strip('"')
        if not os.path.exists(path): return
        if act == "C" and path.lower().endswith(('.gem', '.zst')):
            self.status_text.configure(text="Double Compression Blocked", text_color="#F44336"); return
        self.current_progress = 0; self.is_running = True; self.start_time = time.time()
        self.status_text.configure(text="Processing...", text_color=self.brand_color)
        threading.Thread(target=self.run_logic, args=(act, path), daemon=True).start()

    def run_logic(self, act, path):
        try:
            q = Queue()
            p = Process(target=core_compression_task if act == "C" else core_decompression_task, 
                        args=(path, self.mode_var.get(), path + (".gem" if self.mode_var.get() == "1" else ".zst"), q) if act == "C" else (path, q))
            p.start()
            while p.is_alive(): time.sleep(0.1)
            res, msg, savings = q.get()
            if res == "ERROR": raise Exception(msg)
            self.is_running = False
            self.progress.set(1.0); self.perc_label.configure(text="100%", text_color="#4CAF50")
            self.stat_savings.configure(text=f"Saved: {savings}")
            self.on_success(msg, savings if act == "C" else "EXTRACTED")
        except Exception as e: self.is_running = False; self.on_fail(str(e))

    def on_success(self, out, info):
        self.status_text.configure(text="Success", text_color="#4CAF50")
        self.history_box.insert("end", f"DONE: {os.path.basename(out)} | {info}\n")
        time.sleep(1.5); self.reset_ui()

    def on_fail(self, err):
        self.status_text.configure(text="Error", text_color="#F44336")
        self.history_box.insert("end", f"ERR: {err[:50]}...\n")
        time.sleep(1.5); self.reset_ui()

    def reset_ui(self):
        self.status_text.configure(text="Ready", text_color="gray")
        self.path_entry.delete(0, 'end'); self.progress.set(0); self.perc_label.configure(text="0%", text_color="white")

if __name__ == "__main__":
    multiprocessing.freeze_support(); app = LatticeApp(); app.mainloop()