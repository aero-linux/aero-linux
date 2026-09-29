# 🚀 DistroWatch Official Distribution Submission Package

### 📧 Submission Channel:
* **To:** `distro@distrowatch.com`
* **Subject:** `New Distribution Submission: Aero Linux`
* **From:** Ronit Gupta <ronitgupta138@gmail.com>

---

### 📋 EXACT EMAIL BODY TO SEND (Copy & Paste):

```text
To: distro@distrowatch.com
Subject: New Distribution Submission: Aero Linux

Dear DistroWatch Maintainers,

I would like to submit a new Linux distribution for consideration and listing on DistroWatch. Below are the required project details and technical specifications:

1. Project Name:
Aero Linux

2. Official Website & Documentation:
• Home Page: https://ronitgupta138.github.io/aero-linux/
• Source Repository: https://github.com/ronitgupta138/aero-linux
• Issue Tracker: https://github.com/ronitgupta138/aero-linux/issues
• Release Portal: https://ronitgupta138.github.io/aero-linux/#download

3. Origin & Technical Profile:
• Origin: India
• Architecture: x86_64
• Base: Debian / Ubuntu (Minimal Base with custom zero-telemetry user space)
• Desktop Environment: Wayland / Sway with Dual Desktop Switcher (Windows-Friendly Floating Mode & Cyber Dark Tiling Mode)
• Category: Desktop, Software Development, Systems Engineering, Local AI
• Status: Active (Production Release v1.4.0-Supernova)
• License: MIT License (Open Source)

4. Brief Description & Core Differentiators:
Aero Linux is an ultra-lean developer operating system engineered specifically for systems programmers, backend engineers, and local AI workloads. 

Key architectural pillars include:
• Sub-350MB Idle RAM Baseline: Stripped of background tracking daemons, telemetry, and snapd overhead (idle footprint measured at 312MB).
• Dynamic In-Memory zRAM ZSTD Compression: Eliminates traditional SSD swap latency stalls with multi-threaded ZSTD in-RAM compression (~2.8:1 ratio), providing 25GB+ effective workspace from 15GB RAM.
• 45 Zero-Dependency Native GTK3 Developer Applications: Instant-start native desktop tools (sub-20ms cold start, 15MB RAM per app) including Database Studio, Container Dashboard, Git Commit Graph, Encrypted Secret Vault, Realtime Regex Studio, Port Auditor, and Markdown Editor.
• 1-Click Local AI Workstation: Built-in CLI (`aero ai`) to initialize and serve local reasoning models (DeepSeek-R1, Llama-3) with automated NVIDIA CUDA and AMD ROCm kernel modesetting (`aero gpu setup`).
• Dual Desktop Engine: 1-command layout toggle (`aero layout windows` vs `aero layout tiling`) with familiar muscle-memory shortcuts (Win+E, Ctrl+Shift+Esc, Alt+Tab, Win+L).
• Hardware Battery Preservation: Direct ACPI charge threshold controls (`aero power --threshold 80`) to protect lithium health during long desk sessions.
• 100% Verified Quality Gate: 130/130 automated unit tests passing across all CLI subcommands and system modules.

5. Download Links & Installation Media:
• Latest Release: https://github.com/ronitgupta138/aero-linux/releases/tag/v1.4.0-supernova
• Standalone Debian Package (.deb):
  https://github.com/ronitgupta138/aero-linux/releases/download/v1.4.0-supernova/aero-linux_1.4.0_amd64.deb
  SHA256: 2a8c775aa2a73209f536c93bbde5e5b47d49b1f27097ce6f136948c507208ee2
• Source Code Archive (.tar.gz):
  https://github.com/ronitgupta138/aero-linux/releases/download/v1.4.0-supernova/aero-linux-1.4-supernova-src.tar.gz
  SHA256: ad8a236db540f8e5a4c3ba78b1694d51b838a2523d4707080b5a2f305b9fa7a4
• 1-Command Universal Installer:
  curl -fsSL https://raw.githubusercontent.com/ronitgupta138/aero-linux/main/install.sh | bash

6. Maintainer Contact:
Ronit Gupta
Email: ronitgupta138@gmail.com
GitHub: https://github.com/ronitgupta138

Please let me know if you require any additional technical details or review builds.

Best regards,
Ronit Gupta
Lead Developer, Aero Linux
```
