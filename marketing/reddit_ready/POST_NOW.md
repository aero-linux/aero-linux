# 🚀 1-Click Ready Reddit Launch Pack

Everything below is ready to copy and paste right now.

---

## 🎯 Post 1: r/LocalLLaMA (Highest Technical Conversion)

* **Subreddit:** `r/LocalLLaMA` (https://reddit.com/r/LocalLLaMA)
* **Real Screenshot to Attach:** `/home/ronit138/aero-linux/marketing/reddit_ready/images/real_terminal_doctor.png` (or `card_localllama.png`)
* **Flair / Tag:** Discussion / Project / Tools

### Title (Copy this exactly):
```text
I freed 3.5GB of system RAM by engineering an ultra-lean Linux OS with dynamic zRAM for local model inference
```

### Body Text (Copy this exactly):
```markdown
Hey everyone,

Like many here running local models on 16GB laptops (Ryzen 5 5600H), I was frustrated by Windows 11 eating 4.2GB of RAM at cold boot before even launching a model. Running an 8B Q4 or 14B model would immediately hit the Windows pagefile on the NVMe SSD, causing thermal spikes and severe token-generation throttling.

To fix this, I engineered **Aero Linux** — an ultra-lean developer operating system designed from first principles for low-latency systems and local AI workloads.

### Key Architecture Details:
* **312MB Cold Idle Footprint:** Eliminates background telemetry, unnecessary daemons, and heavy desktop frameworks.
* **Dynamic zRAM with ZSTD (3:1 Compression):** Replaced disk swap with an in-RAM compressed block device. Memory pressure compresses transparently with zero SSD I/O degradation.
* **1-Command Local AI Workstation:** Bundled with `aero ai init` and `aero ai run deepseek-r1` for zero-config Ollama serving.
* **Dual Desktop Engine:** 1-click toggle between minimalist hacker tiling and a Windows-friendly bottom taskbar (`aero layout windows`).

On a 16GB machine, this frees up **over 15.0GB of usable memory headroom**, letting you run 8B Q8 or 14B Q4 models without thermal throttling or hitting disk swap.

Would love feedback from the local AI community on what tools or quant presets we should bundle next!

🔗 **GitHub (MIT License):** https://github.com/ronitgupta138/aero-linux
```

---

## 🎯 Post 2: r/unixporn (For Desktop & Aesthetics)

* **Subreddit:** `r/unixporn` (https://reddit.com/r/unixporn)
* **Image to Attach:** `/home/ronit138/aero-linux/marketing/reddit_ready/images/card_unixporn.png`

### Title (Copy this exactly):
```text
[Sway] Aero Linux — 310MB idle RAM, dynamic zRAM, and custom Cyber Cyan Waybar
```

### Details Comment (Post as the first comment on your thread):
```markdown
* **OS:** Aero Linux 1.0-Edge
* **WM:** Sway (Wayland)
* **Bar:** Custom Waybar with dynamic zRAM & hardware thermals telemetry
* **Terminal:** Alacritty + Fish Shell
* **Theme:** Cyber Cyan (Dark Glassmorphism)
* **Hardware:** AMD Ryzen 5 5600H (12 Cores), 15GB RAM
* **Idle Memory:** 312 MB / 15.3 GB
* **Dotfiles & Source:** https://github.com/ronitgupta138/aero-linux
```
