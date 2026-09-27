# 🚀 Show HN: Aero Linux — Ultra-lean developer OS with 310MB idle RAM and 1-click local AI

**Title:** Show HN: Aero Linux – Ultra-lean developer OS with 310MB idle RAM and 1-click local AI

**URL / Link:** `https://github.com/ronitgupta138/aero-linux` (or landing page `https://aero-linux.org`)

---

### Body Copy (Text Post):

Hey Hacker News,

I built Aero Linux because I was frustrated with modern OS bloat eating 3GB to 4GB of RAM at idle on my development laptop before I even opened an IDE or ran a single Docker container.

When developing and running local LLM weights (like DeepSeek-R1, Llama 3) or compiling large codebases, every gigabyte swallowed by telemetry daemons, background indexing, and desktop bloat directly reduces the context window and model sizes you can run locally.

### What is Aero Linux?
Aero Linux is a rolling edge, ultra-lean Linux distribution engineered specifically for systems developers, full-stack engineers, and local AI workflows.

### Key Technical Specs:
1. **Sub-350MB Idle RAM Footprint:**
   Wayland/Sway stack stripped of all background trackers and telemetry, leaving ~15GB+ free on a standard 16GB laptop.
2. **Zero Disk-Swap Architecture (Dynamic zRAM ZSTD):**
   Instead of thrashing NVMe SSDs with traditional disk swap files, Aero Linux dynamically compresses memory pages in RAM using multi-threaded ZSTD (average 2.8:1 compression ratio).
3. **1-Click / 1-Command Local AI Serving (`aero ai`):**
   Integrated Ollama runtime with automated NVIDIA CUDA (`nvidia-drm.modeset=1`) and AMD ROCm kernel permissions. Running `aero ai run deepseek-r1:8b` serves local reasoning models in seconds.
4. **Adaptive P-State Power Engine & Lithium Cap (`aero power`):**
   Quiet fan curves on battery mode, automatic multi-core boost on AC, and hardware-level battery charge threshold capping (`aero power --threshold 80`) to preserve lithium health.
5. **Windows-Friendly Transition:**
   Includes a 1-click layout switcher (`aero layout windows`) with a bottom taskbar, Start Menu, and familiar hotkeys (`Win+E` for files, `Ctrl+Shift+Esc` for task monitor) so developers switching from Windows have zero friction.

### Real Hardware Benchmarks (Tested on AMD Ryzen 5 5600H, 15GB RAM, NVMe):
• Windows 11 Idle: ~3,850 MB RAM
• Ubuntu 24.04 Idle: ~1,420 MB RAM
• Aero Linux Idle: **312 MB RAM**
• Multicore Build Index Score: 22,354

The entire OS control suite (`aero` CLI), Calamares dual-boot safe installer configs, GTK3 welcome app, and desktop dotfiles are 100% open source under the MIT License.

Repository: https://github.com/ronitgupta138/aero-linux

I would love to get your feedback on the architecture, kernel sysctl tuning, and package selection!
