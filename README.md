<p align="center"> #💠 Lattice Unified | v1.0.0</p>

<br>
High-Performance Data Compression & Archival Suite
Lattice Unified is a professional-grade utility engineered for massive-scale data management. It specializes in bridging the gap between high-capacity storage (1TB+) and rapid deployment through a specialized dual-engine compression architecture.
<br>
## 📥 Core Capabilities
Bimodal Compression Logic: Seamlessly toggle between Nitro Mode (utilizing the Zstandard algorithm for maximum throughput) and Squeeze Mode (utilizing LZMA for deep archival ratios).

Buffered Data Streaming: Optimized for low-memory environments, the engine processes datasets in controlled chunks to ensure system stability even when handling terabyte-scale files.

Intelligent Namespace Protection: Integrated logic automatically detects file naming conflicts and applies non-destructive versioning to prevent accidental data loss.

Structural Fidelity: Unlike standard tools, Lattice preserves the exact directory hierarchy of compressed folders, ensuring seamless restoration.

Active Telemetry Dashboard: A specialized UI layer provides live feedback on hardware strain, memory overhead, and effective space savings.
<br>
| **Layer** | **Implementation** |
| :--- | :--- |
| **Logic Core** | Python 3.12+ (Optimized for 64-bit systems) |
| **Nitro Engine** | Facebook's Zstandard (Zstd) |
| **Archival Engine** | LZMA / Tar-Stream |
| **Interface** | CustomTkinter (Modern GUI Framework) |
| **Monitoring** | PSUtil Hardware Integration |
<br>
#⚙️ Prerequisites & Setup
### 1. Environment Preparation
Before deployment, ensure your system is equipped with the following:

Python 3.12+: Required for modern memory management and core stability.

Git SCM: Essential for secure version control and repository management.

### 2. Local Deployment
Execute the following sequence in your terminal to initialize the suite:

```
# Obtain source code 
git clone https://github.com/kiarash110/Lattice-Unified.git

# Enter project root
cd Lattice-Unified

# Provision environment dependencies
pip install -r requirements.txt
```
<br>
## 🛠️ Operational Maintenance
Interface Unresponsiveness: Large-scale operations (100GB+) may cause the UI to appear static while the processor is under heavy load. Refer to the real-time telemetry stats; if the RAM or Elapsed Time is ticking, the engine is healthy.

Disk Permissions: The compression engine requires direct write access. If "Access Denied" errors occur, verify that your terminal or IDE has administrative privileges over the target drive.

Hardware Bottlenecks: Throughput speed is dictated by your physical drive (HDD vs. NVMe). If the progress indicator stalls, the engine is likely waiting for disk I/O. Do not interrupt the process to avoid archive corruption.
<br>
## 📋 Project Configuration Files
Dependency Manifest (requirements.txt)
Ensure these specific libraries are provisioned in your environment:
```
zstandard

psutil

customtkinter

tkinterdnd2
```
Exclusion Logic (.gitignore)
To maintain a clean repository, ensure the following are excluded from your commits:
```
__pycache__
.zst .gem .tar
.DS_Store Thumbs.db

```
<br>
## ⚖️ Legal & Compliance
Trademark Information: Lattice Unified is an independent open-source project. It is not affiliated with, sponsored by, or endorsed by any corporate entity holding trademarks for "Lattice." The name is used strictly as a descriptor for data structure organization.

Liability Disclaimer: This software is provided "as is." The developer assumes no responsibility for data corruption, hardware failure, or accidental file deletion. Users are strongly advised to verify archives before removing original source data.

