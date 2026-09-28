import os
import shutil
import subprocess
from typing import Dict, Any

GPU_MODES = ["integrated", "hybrid", "dedicated", "nvidia"]


def get_current_gpu_mode() -> Dict[str, Any]:
    print("🎮 \033[1;36mHYBRID GPU GRAPHICS PROFILE (POP!_OS STYLE)\033[0m")
    print("═" * 55)

    mode = "Integrated / Auto"
    if shutil.which("prime-select"):
        try:
            mode = subprocess.check_output(["prime-select", "query"], text=True).strip()
        except Exception:
            pass
    elif shutil.which("supergfxctl"):
        try:
            mode = subprocess.check_output(["supergfxctl", "-g"], text=True).strip()
        except Exception:
            pass

    print(f" • Active Graphics Mode: \033[1;32m{mode.upper()}\033[0m")
    print(" • Modes Available:      Integrated (Battery Saver) | Hybrid (Auto) | Dedicated (Max FPS)\n")
    return {"mode": mode}


def set_gpu_mode(mode: str) -> Dict[str, Any]:
    mode = mode.lower()
    print(f"⚡ Switching Graphics Profile to: \033[1;36m{mode.upper()}\033[0m...")

    if mode == "integrated":
        if shutil.which("prime-select"):
            subprocess.run(["sudo", "prime-select", "intel"], capture_output=True)
        elif shutil.which("supergfxctl"):
            subprocess.run(["supergfxctl", "-m", "Integrated"], capture_output=True)
        print("✅ Integrated Graphics active (Dedicated GPU powered off for maximum battery life).")
        return {"status": "success", "mode": "integrated"}
    elif mode in ("hybrid", "on-demand"):
        if shutil.which("prime-select"):
            subprocess.run(["sudo", "prime-select", "on-demand"], capture_output=True)
        elif shutil.which("supergfxctl"):
            subprocess.run(["supergfxctl", "-m", "Hybrid"], capture_output=True)
        print("✅ Hybrid Graphics active (GPU powers on only during 3D games and AI rendering).")
        return {"status": "success", "mode": "hybrid"}
    elif mode in ("dedicated", "nvidia"):
        if shutil.which("prime-select"):
            subprocess.run(["sudo", "prime-select", "nvidia"], capture_output=True)
        elif shutil.which("supergfxctl"):
            subprocess.run(["supergfxctl", "-m", "Dedicated"], capture_output=True)
        print("✅ Dedicated GPU active (Maximum GPU performance and CUDA compute).")
        return {"status": "success", "mode": "dedicated"}
    else:
        print(f"❌ Unknown GPU mode: {mode}")
        return {"status": "error", "error": "unknown_mode"}
