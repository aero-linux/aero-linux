# 🗺️ Aero Linux Strategic Engineering Roadmap & Release Timeline

This document defines the official architectural milestones, technical specifications, and release timeline for **Aero Linux** across the 2026–2027 release cycles.

---

## 📅 Master Engineering Timeline (2026 – 2027)

```
2026                                            2027
Sep          Nov               Jan                 Mar                            Jun / Jul
 ├─── v1.4 ───┼─────────────────┼───────────────────┼───────────────────────────────┤
 v1.4         v1.5              v1.6                v1.7                            v2.0
 Supernova    Pulsar            Quasar              Hyperion                        Singularity
 (Live)       (eBPF/MicroVMs)   (Swarm/Btrfs CoW)   (BORE Kernel/VRR)               (Rust aero-wm)
```

| Version | Codename | Target Horizon | Cadence | Architecture Focus | Status |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **v1.4** | **Supernova** | **September 2026** | Baseline | 49 GTK3 Apps, 312MB RAM, zRAM ZSTD, Dual Desktop, Local AI Runner, Live ISO | **✅ Production Live** |
| **v1.5** | **Pulsar** | **Mid-November 2026** | ~6 Weeks | Zero-Overhead eBPF Tracing Engine, Firecracker Ephemeral MicroVMs (<50ms) | **🔨 In Development** |
| **v1.6** | **Quasar** | **Mid-January 2027** | ~8 Weeks | Local Autonomous Multi-Agent Swarm, Atomic Btrfs CoW Rollbacks, Mesh VPN | **📋 Spec Complete** |
| **v1.7** | **Hyperion** | **Late March 2027** | ~8 Weeks | Custom `linux-aero` BORE Low-Latency Kernel, Wayland VRR Adaptive Sync | **📋 Planned** |
| **v2.0** | **Singularity** | **June / July 2027** | ~14 Weeks | Pure Rust Wayland Compositor (`aero-wm`), Declarative `aero.toml`, Zero X11 | **🚀 Flagship Target** |

---

## 🧭 Release & Versioning Philosophy

Aero Linux follows a strict **Semantic Systems Versioning** model:
1. **Major Releases (`vX.0.0`):** Fundamental compositor or kernel architecture transitions (e.g. `v2.0-Singularity`).
2. **Minor Milestone Releases (`v1.X.0`):** Major capability additions with celestial codenames (6–8 week engineering sprints).
3. **Point / Patch Releases (`v1.4.X`):** Weekly or bi-weekly bug fixes, security patches, desktop context menus, and UI polishes without altering the active milestone codename.

---

## 🌟 Milestone Specifications

---

### 🌟 1. Current Production: `v1.4-Supernova` (September 2026)
*Status: Production Live & Deployed*

* **Measured Memory Footprint:** 312MB cold-boot idle RAM on bare-metal AMD Ryzen 5600H hardware.
* **Zero-Terminal Developer Suite:** 49 instant-start native GTK3 developer applications (<18ms cold start, zero Electron bloat).
* **Dynamic In-Memory zRAM (ZSTD):** Default 100% RAM disk allocation with stream compression, eliminating disk swap stalls during heavy local builds or AI inference.
* **Dual Desktop Engine:** 1-click seamless toggle between floating Windows layout (for muscle memory) and Sway/Wayland cyber-tiling layout.
* **Local AI Studio (`aero ai`):** 1-click offline DeepSeek-R1, Llama 3, and Ollama model serving out of the box.
* **Release Artifacts:** Automated dynamic Debian packages (`.deb`), bootable Live ISO media (`.iso`), and 1-command curl installer.
* **Quality Assurance:** 130/130 passing unit tests with 100% CI coverage.

---

### ⚡ 2. Next Milestone: `v1.5-Pulsar` (Target: Mid-November 2026 / 6 Weeks)
*Focus: Kernel Tracing, Ephemeral Sandboxes & Network Observability*

#### 🎯 Technical Deliverables:
1. **Native eBPF Tracing Engine (`aero trace` / `aero-ebpf-gui`):**
   * Zero-overhead kernel probe monitoring for HTTP/gRPC latency, socket lifecycle, and disk I/O bottlenecks.
   * Real-time SVG/Cairo visual flamegraph generator for profiling CPU bottlenecks in Go, Rust, C++, Node.js, and Python processes.
   * Interactive TCP socket monitor tracking open ports, drops, and retransmits.
2. **Ephemeral MicroVM Sandboxes (`aero vm`):**
   * 1-command ephemeral Linux MicroVM provisioning via Firecracker (<50ms cold boot).
   * Safe sandbox execution for testing untrusted PRs, suspicious binaries, and container builds with hardware-level isolation.
   * Automated snapshotting and instant teardown upon exit.
3. **Advanced Zero-Terminal Context Menus:**
   * Right-click SQLite/Postgres visual schema migrations.
   * Direct file manager multi-threaded SHA256/BLAKE3 hashing.

---

### 🌌 3. Milestone: `v1.6-Quasar` (Target: Mid-January 2027 / 8 Weeks)
*Focus: Autonomous Developer Workflows & Immutable System Resilience*

#### 🎯 Technical Deliverables:
1. **Local Autonomous Multi-Agent Swarm (`aero swarm`):**
   * Multi-agent developer daemon running directly against local Ollama/DeepSeek-R1 models.
   * Parallel background subagents for automated code review, security threat audits, and test case generation across local Git workspaces.
   * Zero external API dependency and 100% offline air-gapped security.
2. **Atomic Btrfs Subvolume Snapshots & Rollback:**
   * Automated Copy-on-Write (CoW) system snapshots triggered before `apt` upgrades or system package changes.
   * 1-click boot-time rollback available directly in the GRUB bootloader menu.
3. **Zero-Config Developer Mesh Networking:**
   * Integrated WireGuard and Tailscale mesh tunnels with native GTK3 switcher (`aero-tunnel-gui`).
   * Seamless end-to-end encrypted device-to-device SSH and private database access.

---

### ☀️ 4. Milestone: `v1.7-Hyperion` (Target: Late March 2027 / 8 Weeks)
*Focus: Custom Kernel Scheduling, Display VRR & Low-Latency Audio*

#### 🎯 Technical Deliverables:
1. **Custom `linux-aero` BORE Kernel:**
   * Custom-compiled Linux kernel with the **BORE (Burst-Oriented Response Enhancer)** CPU scheduler.
   * Tuned for interactive responsiveness under 100% CPU compiling load.
   * Pre-compiled with full ZSTD compression, 1000Hz timer frequency, and optimized AMD P-State / Intel EEVDF scaling.
2. **Wayland Adaptive Sync & Variable Refresh Rate (VRR):**
   * Native FreeSync and G-Sync tearing protocol integration for ultra-smooth rendering on high-refresh developer displays (144Hz–240Hz+).
3. **Sub-5ms Pro-Audio Latency Stack:**
   * Low-latency PipeWire Pro-Audio profile switching with real-time jack routing.

---

### 🚀 5. Major Milestone: `v2.0-Singularity` (Target: June / July 2027 / 14 Weeks)
*Focus: Pure Rust Native Wayland Compositor & Declarative Architecture*

#### 🎯 Technical Deliverables:
1. **Native Rust Wayland Compositor (`aero-wm`):**
   * Custom standalone Wayland compositor engineered in Rust using the **Smithay** framework.
   * 100% pure Wayland architecture with zero legacy X11 or Xwayland overhead.
   * Fractional HiDPI scaling, smooth spring-physics window animations, and sub-1ms frame presentation.
2. **Unified Declarative Configuration (`~/.config/aero/aero.toml`):**
   * Single declarative configuration file controlling window management rules, keybindings, Waybar telemetry modules, and power profiles.
   * Inotify-based zero-latency hot reloading without restarting the session.
3. **Direct DMA-BUF Zero-Copy Screen Engine:**
   * Direct GPU buffer sharing for ultra-fast screen capture, regional snips, and local LLM visual processing.

---

## 🌌 Celestial Codename Taxonomy

Aero Linux uses a dedicated celestial, relativistic physics, and aerospace naming taxonomy to ensure consistent, evocative identity across future releases:

* **Stellar Phenomena:** `Supernova`, `Pulsar`, `Quasar`, `Hyperion`, `Singularity`, `Magnetar`, `Aurora`, `Zenith`.
* **Deep Space & Constellations:** `Andromeda`, `Orion`, `Cygnus`, `Polaris`, `Pegasus`, `Centaurus`, `Sirius`.
* **Relativistic & Quantum Physics:** `Event Horizon`, `Tachyon`, `Chronos`, `Graviton`, `Photon`.
