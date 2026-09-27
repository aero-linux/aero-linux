import subprocess
import shutil


def check_clipboard() -> bool:
    return bool(shutil.which("wl-copy") or shutil.which("xclip"))


def clear_clipboard() -> bool:
    print("📋 Clearing clipboard buffers...")
    if shutil.which("wl-copy"):
        subprocess.run(["wl-copy", "--clear"])
        print("✅ Wayland clipboard buffer cleared.")
        return True
    elif shutil.which("xclip"):
        subprocess.run(["xclip", "-selection", "clipboard", "/dev/null"])
        print("✅ X11 clipboard buffer cleared.")
        return True
    print("ℹ️ No clipboard CLI found (wl-clipboard or xclip).")
    return False
