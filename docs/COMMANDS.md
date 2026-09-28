# 🛠️ Aero Linux CLI (`aero`) — Complete Command Reference

The `aero` CLI is the core system, AI, and developer management utility in Aero Linux.

---

### 1. System & Hardware Diagnostics
* `aero doctor`: Complete hardware, CPU, RAM, GPU, battery, and AI readiness audit.
* `aero temp`: Live per-core CPU, GPU, and NVMe hardware temperature readout.
* `aero battery`: Detailed lithium health, design vs usable Wh capacity, and charge cycles.
* `aero benchmark`: High-throughput multi-core CPU, RAM bandwidth, and disk IO speed benchmark.
* `aero monitor`: Live interactive terminal dashboard with real-time CPU core frequencies.
* `aero logs [error|kernel|boot]`: Intelligent system log and kernel panic parser.

---

### 2. Power & Battery Management
* `aero power [battery|balanced|boost|gaming]`: Switch adaptive P-State CPU power profiles.
* `aero power --threshold 80`: Cap hardware battery charging at 80% to preserve lithium lifespan.
* `aero bt [on|off|status]`: Bluetooth controller power toggle to save battery when mobile.

---

### 3. Memory & Optimization
* `aero memory --optimize`: Compact zRAM compressed pages and drop filesystem caches.
* `aero memory --top`: List top 10 memory-consuming processes.
* `aero pkg clean`: Prune orphaned packages and clean APT/Flatpak caches.
* `aero disk top`: Find large files ($>100\text{MB}$) consuming storage.
* `aero disk clean-node-modules`: Clean nested `node_modules` folders across projects.

---

### 4. Local AI / ML Workstation
* `aero ai init`: 1-click installation and configuration of local Ollama runtime.
* `aero ai status`: Check daemon health and installed model weights.
* `aero ai pull <model>`: Download models (e.g. `deepseek-r1:8b`, `llama3.2`, `qwen2.5-coder`).
* `aero ai run <model>`: Start interactive terminal prompt with local LLM.
* `aero ai calc --params <N> --quant <Q>`: Calculate model weights, KV cache, and RAM/zRAM requirements.
* `aero ai bench [model]`: Measure time-to-first-token (TTFT) and token/sec inference throughput.
* `aero gpu setup`: Automated CUDA driver / ROCm setup with Wayland modesetting.

---

### 5. Developer Tools & Workspaces
* `aero dev list`: List available containerized sandboxes.
* `aero dev run [node|python|rust|go|c]`: Spin up isolated workspace in current directory.
* `aero db start [postgres|redis|mysql|mongo|clickhouse]`: 1-command local background database.
* `aero cert generate [domain]`: 1-command trusted local SSL/TLS certificate generator for HTTPS.
* `aero clean [--dry-run]`: Deep system de-bloater (prunes npm, pip, apt, docker caches).
* `aero trace [ping <host>|dns]`: Network socket connect, TLS handshake, and DNS latency tracer.
* `aero vault [set|get|list|delete|export]`: Local encrypted developer keyring & .env manager.
* `aero live [--port 8080]`: Real-time developer web telemetry streaming dashboard.
* `aero notify <title> [msg] [--sound]`: Desktop notification broadcaster and build finished alert.
* `aero port list`: Show active listening developer ports and bound processes.
* `aero port kill <port>`: Terminate process listening on a specific port.
* `aero env check`: Audit installed SDKs (Node, Python, C, Rust, Go, Java, Docker).
* `aero api bench <url>`: Run concurrent HTTP load tests (req/sec, p95/p99 latency).
* `aero share [path]`: Zero-config local network HTTP file sharing server.
* `aero ssh [status|gen|copy|test]`: Ed25519 SSH key management and GitHub auth test.
* `aero git [status|clean|graph|churn]`: Branch tracking, ASCII commit graph, and code churn analyzer.

---

### 6. Desktop Customization & Kernel
* `aero layout [windows|tiling]`: 1-click toggle between Windows Start taskbar and Hacker Tiling.
* `aero kernel [audit|profile <name>]`: Low-latency vs throughput kernel scheduler tuning.
* `aero wallpaper [set|generate]`: Procedural vector cyber wallpapers (`cyber-cyan`, `tokyo-night`, `nord`, `gruvbox`).
* `aero theme [list|set <name>]`: Switch themes (`cyber-cyan`, `tokyo-night`, `nord`, `gruvbox`).
* `aero font install [jetbrains-mono|fira-code|hack]`: 1-click Nerd Font installation.
* `aero net bbr`: Enable Google BBR TCP congestion control.
* `aero net dns [cloudflare|quad9|google]`: Switch to encrypted DNS-over-TLS.
* `aero net wifi`: Disable WiFi power-saving jitter for low-latency networking.
* `aero security [audit|harden]`: UFW firewall and kernel ASLR hardening.
* `aero snapshot [create|list|restore]`: Zero-latency system restore points via Timeshift/Btrfs.
* `aero keys`: Display desktop keyboard shortcuts cheatsheet.
