import subprocess
import shutil

LATENCY_PRESETS = {
    "low": "128/48000",      # ~2.6ms buffer latency (ideal for music production/gaming)
    "medium": "256/48000",   # ~5.3ms buffer latency (balanced)
    "high": "1024/48000",    # ~21.3ms buffer latency (maximum power saving)
}


def check_audio_status():
    print("🎵 \033[1;36mPIPEWIRE LOW-LATENCY AUDIO ENGINE\033[0m")
    print("═" * 55)

    if shutil.which("pw-cli"):
        print(" • Audio Server:   \033[1;32mPipeWire (Native)\033[0m")
    elif shutil.which("pactl"):
        print(" • Audio Server:   \033[1;32mPulseAudio / PipeWire-Pulse\033[0m")
    else:
        print(" • Audio Server:   ALSA Direct")

    if shutil.which("pw-top"):
        print(" • Live Monitor:   Run 'pw-top' for real-time DSP cycle load")
    print()


def set_audio_latency(preset: str = "low") -> bool:
    if preset not in LATENCY_PRESETS:
        print(f"❌ Unknown preset: {preset}. Choose from: {list(LATENCY_PRESETS.keys())}")
        return False

    quantum = LATENCY_PRESETS[preset]
    print(f"⚡ Setting PipeWire quantum buffer to {preset.upper()} latency ({quantum})...")

    if shutil.which("pw-metadata"):
        try:
            subprocess.run(["pw-metadata", "-n", "settings", "0", "clock.force-quantum", quantum.split("/")[0]], check=True)
            print(f"✅ PipeWire audio buffer locked to {quantum} (Ultra-low latency active).")
            return True
        except Exception as e:
            print(f"❌ Failed to set PipeWire quantum: {e}")
            return False
    print("ℹ️ pw-metadata not available. Audio running on standard ALSA/Pulse defaults.")
    return False
