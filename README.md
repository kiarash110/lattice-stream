<p align="center">
  <h1 align="center">💠 **Lattice Unified** | `v1.0.0`</h1>
  <p align="center">
    <b>High-Performance Data Compression & Archival Suite</b><br>
    Lattice Unified is a professional-grade utility engineered for massive-scale data management. It specializes in bridging the gap between high-capacity storage (1TB+) and rapid deployment through a specialized dual-engine compression architecture.
  </p>
</p>

<br>

## 📥 **Core Capabilities**

* 🚀 **Bimodal Compression Logic:** Seamlessly toggle between **Nitro Mode** (utilizing the Zstandard algorithm for maximum throughput) and **Squeeze Mode** (utilizing LZMA for deep archival ratios).
* 🌊 **Buffered Data Streaming:** Optimized for low-memory environments, the engine processes datasets in controlled chunks to ensure **system stability** even when handling terabyte-scale files.
* 🛡️ **Intelligent Namespace Protection:** Integrated logic automatically detects file naming conflicts and applies **non-destructive versioning** to prevent accidental data loss.
* 📂 **Structural Fidelity:** Unlike standard tools, Lattice preserves the **exact directory hierarchy** of compressed folders, ensuring seamless restoration.
* 📊 **Active Telemetry Dashboard:** A specialized UI layer provides **live feedback** on hardware strain, memory overhead, and effective space savings.

<br>

<div align="center">

### 💻 **Technical Architecture**

| **Layer** | **Implementation** |
| :--- | :--- |
| **Logic Core** | **Python 3.12+** (Optimized for 64-bit systems) |
| **Nitro Engine** | **Facebook's Zstandard** (Zstd) |
| **Archival Engine** | **LZMA / Tar-Stream** |
| **Interface** | **CustomTkinter** (Modern GUI Framework) |
| **Monitoring** | **PSUtil** Hardware Integration |

</div>

<br>

## ⚙️ **Prerequisites & Setup**

### 1️⃣ **Environment Preparation**
Before deployment, ensure your system is equipped with the following:
* 🐍 **Python 3.12+**: Required for modern memory management and core stability.
* 🐙 **Git SCM**: Essential for secure version control and repository management.

### 2️⃣ **Local Deployment**
Execute the following sequence in your terminal to initialize the suite:

# Obtain source code 
git clone https://github.com/kiarash110/Lattice-Unified.git

# Enter project root
cd Lattice-Unified

# Provision environment dependencies
pip install -r requirements.txt

<br>

## 🛠️ **Operational Maintenance**

> [!IMPORTANT]
> **Interface Unresponsiveness:** Large-scale operations (**100GB+**) may cause the UI to appear static while the processor is under heavy load. Refer to the real-time telemetry stats; if the RAM or Elapsed Time is ticking, the engine is healthy.

* 🔑 **Disk Permissions:** The compression engine requires **direct write access**. If "Access Denied" errors occur, verify that your terminal or IDE has **administrative privileges** over the target drive.
* 📉 **Hardware Bottlenecks:** Throughput speed is dictated by your physical drive (**HDD vs. NVMe**). If the progress indicator stalls, the engine is likely waiting for disk I/O. **DO NOT** interrupt the process to avoid archive corruption.

<br>

## 📋 **Project Configuration Files**

#### **Dependency Manifest (requirements.txt)**
Ensure these specific libraries are provisioned in your environment:
```text
zstandard
psutil
customtkinter
tkinterdnd2
