import subprocess
import shutil
import os
from typing import Dict, Any


def show_display_info() -> Dict[str, Any]:
    print("🖥️  \033[1;36mWAYLAND & DISPLAY HARDWARE STATUS\033[0m")
    print("═" * 55)

    session = os.environ.get("XDG_SESSION_TYPE", "unknown")
    wm = os.environ.get("XDG_CURRENT_DESKTOP", "unknown")
    print(f" • Session Type:       \033[1;32m{session.upper()}\033[0m")
    print(f" • Compositor/Desktop: \033[1;32m{wm}\033[0m")

    if shutil.which("swaymsg"):
        try:
            res = subprocess.run(["swaymsg", "-t", "get_outputs"], capture_output=True, text=True)
            if res.returncode == 0:
                print("\nActive Displays (Sway IPC):")
                print(res.stdout[:500])
                return {"session": session, "wm": wm}
        except Exception:
            pass

    if shutil.which("wlr-randr"):
        res = subprocess.run(["wlr-randr"], capture_output=True, text=True)
        print("\nActive Displays (wlr-randr):")
        print(res.stdout)
    elif shutil.which("xrandr"):
        res = subprocess.run(["xrandr", "--current"], capture_output=True, text=True)
        for line in res.stdout.split("\n"):
            if " connected " in line:
                print(f" • Connected Output: \033[1;33m{line.strip()}\033[0m")
    else:
        print("ℹ️ Standard DRM kernel display active.")
    print()
    return {"session": session, "wm": wm}


def set_night_light(enable: bool = True, temp_k: int = 4500) -> bool:
    print(f"🌙 \033[1;36mAERO NIGHT LIGHT (BLUE LIGHT FILTER)\033[0m")
    print("═" * 55)
    if enable:
        print(f" • Applying warm eye-protection temperature: \033[1;33m{temp_k}K\033[0m")
        # Kill existing gammastep or wlsunset
        subprocess.run("killall gammastep wlsunset 2>/dev/null", shell=True)
        if shutil.which("wlsunset"):
            subprocess.Popen(f"wlsunset -t {temp_k} -T 6500", shell=True)
        elif shutil.which("gammastep"):
            subprocess.Popen(f"gammastep -O {temp_k}", shell=True)
        print("✅ Night light enabled.")
        return True
    else:
        print(" • Restoring standard daylight color temperature (6500K)...")
        subprocess.run("killall gammastep wlsunset 2>/dev/null", shell=True)
        if shutil.which("gammastep"):
            subprocess.run("gammastep -x 2>/dev/null", shell=True)
        print("✅ Night light disabled.")
        return False
