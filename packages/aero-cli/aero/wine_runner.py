import os
import shutil
import subprocess
from typing import Dict, Any


def run_windows_app(exe_path: str, use_gamemode: bool = True) -> Dict[str, Any]:
    exe_path = os.path.abspath(exe_path)
    if not os.path.exists(exe_path):
        print(f"❌ File not found: {exe_path}")
        return {"status": "error", "error": "not_found"}

    print("🪟 \033[1;36mAERO WINDOWS COMPATIBILITY RUNNER (PROTON/WINE)\033[0m")
    print("═" * 55)
    print(f" • Target Executable: \033[1;33m{exe_path}\033[0m")

    # Check for GE-Proton or Wine
    proton_dirs = [
        os.path.expanduser("~/.local/share/proton-ge"),
        os.path.expanduser("~/.steam/root/compatibilitytools.d"),
    ]
    proton_bin = None
    for p_dir in proton_dirs:
        if os.path.exists(p_dir):
            for entry in os.scandir(p_dir):
                candidate = os.path.join(entry.path, "proton")
                if os.path.exists(candidate) and os.access(candidate, os.X_OK):
                    proton_bin = candidate
                    break

    runner = "wine"
    if proton_bin:
        runner = proton_bin
        print(f" • Proton Runtime:    \033[1;32m{proton_bin}\033[0m (Proton-GE)")
    elif shutil.which("wine"):
        print(" • Wine Runtime:      \033[1;32mSystem Wine\033[0m")
    else:
        print("ℹ️ Wine or GE-Proton not installed. Run: sudo apt install wine64")
        return {"status": "missing_wine", "path": exe_path}

    cmd = []
    if use_gamemode and shutil.which("gamemoderun"):
        cmd.append("gamemoderun")
        print(" • GameMode:          \033[1;32mActive\033[0m (CPU/GPU Performance Boost)")

    if runner == "wine":
        cmd.extend(["wine", exe_path])
    else:
        cmd.extend([runner, "run", exe_path])

    print("\n🚀 Launching Windows application...")
    try:
        p = subprocess.Popen(cmd)
        return {"status": "launched", "pid": p.pid, "runner": runner}
    except Exception as e:
        print(f"❌ Launch error: {e}")
        return {"status": "error", "error": str(e)}
