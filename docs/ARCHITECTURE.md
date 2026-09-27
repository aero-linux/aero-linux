# ⚡ Aero Linux — Technical Architecture Specification

Aero Linux is an ultra-lean, high-performance Linux distribution designed for **software engineers, systems developers, and local AI workloads**.

---

## 1. Operating System Fundamentals

| Component | Technology | Target / Footprint |
| :--- | :--- | :--- |
| **Base Distribution** | Debian 12 / Ubuntu 24.04 Minimal Base | Zero telemetry, no snapd overhead |
| **Window Manager** | Sway (Wayland Native i3-compatible) | Sub-350MB idle RAM consumption |
| **Status Bar** | Waybar with custom C/Shell telemetry pills | Live zRAM, AI status, power profiles |
| **Terminal Emulator** | Alacritty (GPU-accelerated) | Sub-10ms input latency |
| **Shell Environment** | Fish Shell + Aero Quick Command Aliases | Instant tab completions & syntax highlighting |
| **Display Manager** | Greetd with tuigreet | Direct Wayland session launch |

---

## 2. Memory & Virtual Storage Architecture (zRAM ZSTD)

Traditional SSD swap causes catastrophic IO latency spikes during heavy builds and local model inference. Aero Linux uses a **zero-swap, dynamic in-memory compressed block device**:

```text
[ Physical RAM (16GB) ]
  ├── Active User Space (~5GB - IDE, Docker, Local LLM)
  ├── Pagecache & Buffer Cache (~3GB)
  └── Dynamic zRAM Device (/dev/zram0, ~8GB)
        └── Compressed with ZSTD algorithm (2.8:1 average ratio)
            ➔ Effectively yields ~24GB to ~28GB of usable memory headroom
```

---

## 3. Local AI / ML Workstation Stack

Aero Linux includes native 1-click execution for local large language models:
- **Ollama Engine:** Pre-configured systemd unit bound to `127.0.0.1:11434`.
- **GPU Acceleration:** Automated detection for NVIDIA CUDA (`nvidia-drm.modeset=1`) and AMD ROCm (`/dev/kfd` permissions).
- **Container Isolation:** Native Docker Engine with NVIDIA Container Toolkit pre-wired.

---

## 4. Power & Thermal Management

Powered by custom TLP configurations and ACPI hardware hooks:
- **`battery`:** Caps CPU frequency to energy-efficient P-States, disables turbo boost, forces quiet fans.
- **`balanced`:** Dynamic frequency scaling.
- **`boost` / `gaming`:** Maximum multi-core clock speeds, GPU power level to `high`, DXVK asynchronous shader pipeline.
- **Battery Cap:** Direct sysfs threshold control (`/sys/class/power_supply/BAT0/charge_control_end_threshold`).
