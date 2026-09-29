# ⚡ Aero Linux — Technical Architecture Specification

Aero Linux is an ultra-lean, high-performance developer Linux distribution engineered for **systems programmers, backend engineers, and local AI builders**.

---

## 1. Operating System Fundamentals

| Component | Technology | Target / Footprint |
| :--- | :--- | :--- |
| **Base Distribution** | Debian 12 / Ubuntu 24.04 Minimal Base | Zero telemetry, no snapd overhead, pure APT |
| **Desktop Architecture** | Dual Engine (Sway Tiling / Cinnamon Floating) | Measured 312MB cold-boot idle RAM footprint |
| **Status Bar** | Waybar with custom C/Shell telemetry pills | Live zRAM, Dev Ports (`:3000 :8080`), AI status, power profiles |
| **Terminal Emulator** | Alacritty (GPU-accelerated) | Sub-10ms input latency, JetBrains Mono font |
| **Shell Environment** | Fish Shell + Aero Quick Command Aliases | Instant tab completions, syntax highlighting & git status |
| **Display Manager** | Greetd with tuigreet | Direct Wayland session launch with zero display server bloat |
| **Developer GUI Suite** | 49 Native PyGObject/GTK3 applications | Sub-18ms cold start, 15MB baseline RAM, zero Electron |

---

## 2. Memory & Virtual Storage Architecture (zRAM ZSTD)

Traditional SSD disk swap causes catastrophic IO latency spikes and disk thrashing during heavy compilations and local model inference. Aero Linux replaces disk swap with a **high-throughput, in-memory compressed block device**:

```text
[ Physical RAM (16GB) ]
  ├── Active User Space (~5GB - IDE, Compilers, Docker, Local LLMs)
  ├── Pagecache & Buffer Cache (~3GB)
  └── Dynamic zRAM Device (/dev/zram0, ~8GB)
        └── Compressed with ZSTD algorithm (2.8:1 average ratio)
            ➔ Effectively yields ~24GB to ~28GB of usable memory headroom
```

### Key Memory Parameters:
* **Compression Algorithm:** `zstd` (high compression speed and low decompression latency).
* **Disk Size:** 100% of physical RAM (`/etc/systemd/zram-generator.conf`).
* **Swappiness:** `vm.swappiness = 180` (prioritizes memory compaction in zRAM before file pagecache eviction).
* **Direct Page Compaction:** `aero memory --optimize` flushes uncompressed dirty pages and trims kernel slab caches.

---

## 3. Dual Desktop Engine Architecture

Aero Linux eliminates desktop lock-in by providing a 1-click toggle between two paradigms without losing system configuration or application state:

1. **🪟 Windows Floating Mode (`aero layout windows`):**
   * Familiar bottom taskbar with **⚡ Start Menu**, pinned application launchers, system tray, and floating window defaults.
   * Native hotkey mappings: `Win+E` (File Explorer), `Ctrl+Shift+Esc` (Task Manager), `Alt+Tab` (Window Switcher), `Win+L` (Lock Screen), `Win+A` (Quick Settings).
2. **⚡ Cyber Tiling Mode (`aero layout tiling`):**
   * Cyber Dark Sway auto-tiling window manager with smart gaps and floating translucent Waybar status bar.
   * Raycast-style universal command bar (`Alt+Space` / `aero-spotlight`) and global hotkeys (`Win+Enter` Terminal, `Win+Shift+Q` Kill Window, `Win+1-5` Workspaces).

---

## 4. Local AI & Systems Development Workstation Stack

Aero Linux ships with native 1-click execution for local large language models and containerized dev environments:
* **Ollama Inference Engine:** Pre-configured systemd daemon bound to `127.0.0.1:11434`.
* **GPU Hardware Acceleration:** Automated detection for NVIDIA CUDA (`nvidia-drm.modeset=1`) and AMD ROCm (`/dev/kfd` permissions).
* **Inference Calculators:** Integrated `aero ai calc` computing model weights, KV cache sizing, and RAM fitting for 8B, 14B, 32B, and 70B quantized models.
* **Developer Containers:** Native Docker Engine with NVIDIA Container Toolkit pre-wired.

---

## 5. Power, Thermal & Battery Lifespan Management

Powered by custom TLP configurations, ACPI hardware hooks, and P-State governors:
* **`battery` (Quiet):** Caps CPU frequency to energy-efficient P-States, disables turbo boost, forces silent fan curves.
* **`balanced` (Default):** Dynamic frequency scaling matching active workloads.
* **`boost` / `gaming` (High Performance):** Maximum multi-core clock speeds, GPU power level to `high`, DXVK asynchronous shader pipeline.
* **Battery Longevity Cap:** Direct sysfs threshold control (`/sys/class/power_supply/BAT0/charge_control_end_threshold`) capping charge at 80% to double lithium battery longevity during desk power sessions.

---

## 6. Zero-Terminal Graphical Application Suite (49 Apps)

Aero Linux includes **49 dedicated native GTK3 graphical applications** covering every layer of development, security, hardware tuning, and systems administration:
* **AI & LLM:** `aero-ai-gui` (Local LLM Studio), `aero-agent` (Terminal Assistant).
* **Database & APIs:** `aero-db-gui` (SQLite Studio), `aero-api-gui` (Native REST Client), `aero-mock-gui` (Mock Server & Webhooks).
* **Security & Keys:** `aero-vault-gui` (Encrypted Keyring), `aero-ssh-gui` (SSH Bookmarks), `aero-ssl-gui` (Dev HTTPS Certs), `aero-firewall-gui` (UFW Shield).
* **Systems & Telemetry:** `aero-monitor` (Task Manager), `aero-ports-gui` (Dev Port Inspector), `aero-disk-gui` (Disk Visualizer), `aero-power-gui` (Battery Studio), `aero-cleaner-gui` (System Purger), `aero-snapshots-gui` (TimeMachine Restore Points).
* **Desktop Ergonomics:** `aero-spotlight` (Raycast-style Launcher), `aero-notes-gui` (Markdown Scratchpad), `aero-color-gui` (Screen Color Dropper), `aero-shortcuts-gui` (Cheatsheet Guide), `aero-gamehub` (Proton Game Launcher).

---

## 7. Strategic Roadmap

For upcoming milestones (`v1.5-Pulsar`, `v1.6-Quasar`, `v1.7-Hyperion`, and `v2.0-Singularity`), see [docs/ROADMAP.md](ROADMAP.md).
