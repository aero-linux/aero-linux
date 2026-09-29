# 🗺️ Aero Linux Strategic Engineering Roadmap

This document outlines the official architectural milestones and release progression for **Aero Linux**, from the current production release through the next-generation systems roadmap.

---

## 🌟 Current Production: `v1.4-Supernova` (Live)
- [x] **Sub-350MB Idle RAM Baseline:** Measured 312MB cold boot on bare-metal AMD Ryzen 5600H.
- [x] **Zero-Terminal Developer Suite:** 49 instant-start native GTK3 applications (<18ms cold start, zero Electron).
- [x] **Dynamic In-Memory zRAM (ZSTD):** Default 100% RAM allocation with stream compression, eliminating swap thrashing.
- [x] **Dual Desktop Engine:** 1-click seamless toggle between floating Windows layout and Sway cyber-tiling layout.
- [x] **Built-in Local AI Studio (`aero ai`):** 1-click offline DeepSeek-R1 and Ollama inference runner.
- [x] **Release Packaging:** Automated Debian packaging (`.deb`), bootable Live ISO media, and 1-command installer.
- [x] **Test & Quality Suite:** 130/130 passing unit tests with 100% CI coverage.

---

## ⚡ Next Milestone: `v1.5-Pulsar` (eBPF & MicroVMs)
*Target: Systems Telemetry & Ephemeral Sandbox Environments*

- [ ] **Native eBPF Tracing Engine:**
  - Zero-overhead kernel probe monitoring for HTTP/gRPC latency, file I/O bottlenecks, and TCP connection tracing.
  - Visual GTK3 eBPF flamegraph generator (`aero-ebpf-gui`).
- [ ] **Ephemeral MicroVM Sandboxes:**
  - 1-command ephemeral Linux MicroVM provisioning via Firecracker (<50ms boot time).
  - Test dirty code, third-party binaries, and untrusted scripts in isolated hardware virtualized sandboxes.
- [ ] **Developer Context Actions Expansion:**
  - Multi-threaded checksum hashing and git workspace diff analyzers.

---

## 🌌 `v1.6-Quasar` (Multi-Agent Swarms & Immutable Btrfs)
*Target: Autonomous Developer Workflows & System Resilience*

- [ ] **Local Multi-Agent Swarm Orchestrator:**
  - Autonomous multi-agent coordination running directly against local Ollama/DeepSeek models.
  - Parallel background code review, security scanning, and test-case generation.
- [ ] **Atomic Btrfs Subvolume Snapshots:**
  - Copy-on-Write (CoW) system snapshots before major package upgrades (`apt`).
  - Instant boot-menu rollbacks via GRUB if any system update causes regressions.
- [ ] **Zero-Config Tailscale & WireGuard Mesh:**
  - Built-in secure developer mesh networking for seamless SSH and private database access across devices.

---

## ☀️ `v1.7-Hyperion` (Custom `linux-aero` Kernel)
*Target: Low-Latency Kernel Tuning & Maximum Gaming/Compute Efficiency*

- [ ] **Custom `linux-aero` BORE Kernel:**
  - Burst-Oriented Response Enhancer (BORE) CPU scheduler for ultra-low latency desktop interactivity under 100% CPU load.
  - Pre-compiled full ZSTD compression, PREEMPT_DYNAMIC, and optimized AMD/Intel P-State drivers.
- [ ] **Wayland VRR & Adaptive Sync:**
  - Native Variable Refresh Rate (FreeSync / G-Sync) tearing protocols enabled for high-refresh-rate developer monitors.
- [ ] **Real-Time Audio Latency Buffer:**
  - PipeWire Pro-Audio preset tuning down to sub-5ms round-trip latency.

---

## 🚀 `v2.0-Singularity` (Rust `aero-wm` Compositor)
*Target: The Next-Generation Zero-Dependency Pure Wayland Desktop*

- [ ] **Native Rust Wayland Compositor (`aero-wm`):**
  - Custom standalone compositor built on Smithay with zero legacy X11 dependencies.
  - Native fractional HiDPI scaling, smooth spring-physics animations, and sub-1ms frame presentation.
- [ ] **Unified Declarative Config Format (`aero.toml`):**
  - Single central configuration file for window management, keybindings, topbar telemetry, and power profiles with instant live-reloading.
- [ ] **Zero-Copy GPU Buffer Sharing:**
  - Direct DMA-BUF sharing for ultra-fast screen capture, region snips, and local LLM visual processing.
