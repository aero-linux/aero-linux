# ⚡ Aero Linux

> **The Ultra-Lean AI & High-Performance Developer Operating System**

[![CI / Test Suite](https://github.com/ronitgupta138/aero-linux/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/ronitgupta138/aero-linux/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-cyan.svg)](LICENSE)
[![Idle Memory](https://img.shields.io/badge/Idle_RAM-~310MB-brightgreen.svg)]()
[![zRAM](https://img.shields.io/badge/zRAM_ZSTD-Default_Enabled-blue.svg)]()

---

## 🚀 Why Aero Linux?

Most modern Linux desktop distributions consume 1.2GB–2GB of RAM at idle and require hours of manual setup to configure CUDA, ROCm, local LLM runtimes, low-latency schedulers, and battery threshold governors.

**Aero Linux** is engineered specifically for developers, AI engineers, and performance purists:
- **Sub-350MB Idle RAM:** Hyper-optimized Wayland/Sway and clean X11 stack with zero telemetry or background bloat.
- **Native Local AI Engine (`aero ai`):** 1-click Ollama, vLLM, and containerized GPU serving out of the box.
- **Dynamic zRAM ZSTD Swapping:** Doubles effective RAM for heavy LLM inference and local builds without system freeze.
- **Adaptive Power & P-State Engine:** Silent, cool fan profiles on battery; automatic high-performance boost on AC/gaming.
- **Zero-Latency Kernel Tweaks:** High inotify limits, BBR TCP congestion control, and tuned sysctl responsiveness.

---

## 🛠️ The Aero Control Suite (`aero-cli`)

Aero includes a native management CLI out of the box:

```bash
# Full system, kernel, battery, and AI readiness audit
aero doctor

# Switch adaptive power and thermal profiles
aero power [battery|balanced|boost|gaming]
aero power --threshold 80   # Cap battery charge at 80% to preserve lifespan

# 1-click local LLM inference
aero ai init                # Setup Ollama & container runtimes
aero ai pull deepseek-r1:8b # Pull model
aero ai run deepseek-r1:8b  # Interactive prompt

# Memory compaction & process inspection
aero memory --optimize      # Compact zRAM and drop pagecaches
aero memory --top           # List top memory consuming processes
```

---

## 🏗️ Building the Live ISO Locally

```bash
# Clone the repository
git clone https://github.com/ronitgupta138/aero-linux.git
cd aero-linux

# Run the automated live-build script (requires root)
sudo ./build/build.sh
```

---

## 🌐 Project Structure

```text
aero-linux/
├── .github/workflows/         # Automated ISO Release & CI Test Workflows
├── build/                     # Live ISO builder scripts, sysctl & package manifests
├── packages/
│   ├── aero-cli/              # Core System & AI Management CLI
│   └── aero-welcome/          # GTK3 First-Boot Quick Setup & Onboarding UI
├── desktop/                   # Sway, Waybar, Alacritty, and Fish dotfiles
└── web/                       # Landing Page & Documentation website
```

---

## 📜 License

Distributed under the **MIT License**. Created by Ronit Gupta & Open Source Contributors.
