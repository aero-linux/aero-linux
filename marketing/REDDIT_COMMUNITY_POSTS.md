# 🔴 Reddit Tech Community Launch Posts

---

## 1. r/linux (Tone: First-principles engineering, performance metrics, open source)

**Title:** Built Aero Linux — an ultra-lean developer distro with 310MB idle RAM, dynamic zRAM ZSTD, and 1-click local LLM serving

**Post Body:**
```text
Hey r/linux,

Like many of you, I've noticed modern Linux desktop installations creeping up in resource usage, often idling at 1.4GB to 2GB with snapd, telemetry, and background services running out of the box.

I built Aero Linux as a specialized developer workstation operating system focused on raw speed, low memory overhead, and native local AI support:

• Idle Footprint: ~312MB on modern x86_64 hardware (Sway + Waybar).
• Dynamic zRAM: Uses multi-threaded ZSTD compression (default ~2.8:1 ratio) to replace traditional SSD swap files, completely eliminating SSD IO stutter under heavy compilation or model loading.
• Native Local AI: Pre-wired Ollama, Docker, and automated NVIDIA CUDA modesetting (`nvidia-drm.modeset=1`) and AMD ROCm kernel permissions via `aero gpu setup`.
• Battery Preservation: Direct sysfs lithium charge threshold capping (`aero power --threshold 80`).
• Dual-Boot Safety: Calamares configured with active ESP detection to protect Windows/BitLocker installations.

Source code and configs are available under the MIT license on GitHub:
https://github.com/ronitgupta138/aero-linux

Would love to hear your thoughts on the sysctl defaults and package selection!
```

---

## 2. r/LocalLLaMA (Tone: Maximizing VRAM & system RAM for model context)

**Title:** Aero Linux — Freeing ~1.5GB to 3.5GB of RAM for local LLMs (310MB idle RAM OS + 1-click Ollama/vLLM)

**Post Body:**
```text
When running local models (like DeepSeek-R1 8B, Llama 3, or Qwen 2.5) on laptops with 16GB or 32GB RAM, running Windows 11 eats ~3.8GB RAM and Ubuntu eats ~1.4GB at idle.

That lost RAM directly dictates whether you can fit a Q4/Q8 quantization or hold a 16k context window without offloading to disk swap.

Aero Linux was built specifically to solve this:
1. 310MB idle RAM consumption leaving 15GB+ available for model weights on a 16GB machine.
2. Dynamic zRAM ZSTD compression doubling effective memory headroom.
3. 1-Command execution: `aero ai run deepseek-r1:8b` serves models instantly.
4. Automated NVIDIA CUDA & ROCm driver setup with Wayland KMS modesetting.

GitHub: https://github.com/ronitgupta138/aero-linux
```
