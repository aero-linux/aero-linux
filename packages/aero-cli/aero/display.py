import subprocess
import shutil
import os


def show_display_info():
    print("🖥️  \033[1;36mWAYLAND & DISPLAY HARDWARE STATUS\033[0m")
    print("═" * 55)

    # Check session type
    session = os.environ.get("XDG_SESSION_TYPE", "unknown")
    wm = os.environ.get("XDG_CURRENT_DESKTOP", "unknown")
    print(f" • Session Type:       \033[1;32m{session.upper()}\033[0m")
    print(f" • Compositor/Desktop: \033[1;32m{wm}\033[0m")

    # Check Sway outputs
    if shutil.which("swaymsg"):
        try:
            res = subprocess.run(["swaymsg", "-t", "get_outputs"], capture_output=True, text=True)
            if res.returncode == 0:
                print("\nActive Displays (Sway IPC):")
                print(res.stdout[:500])
                return
        except Exception:
            pass

    # Check xrandr / wlr-randr
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
