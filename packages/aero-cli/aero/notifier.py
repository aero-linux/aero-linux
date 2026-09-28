import os
import shutil
import subprocess
import sys


def send_notification(title: str, message: str = "", urgency: str = "normal", sound: bool = False) -> bool:
    print(f"\n🔔 \033[1;36m[AERO NOTIFICATION]\033[0m {title} {('- ' + message) if message else ''}")
    
    if sound:
        # Terminal bell
        sys.stdout.write("\a")
        sys.stdout.flush()

    if shutil.which("notify-send"):
        try:
            cmd = ["notify-send", "-u", urgency, "-a", "Aero Linux", "-i", "utilities-terminal", title, message]
            subprocess.run(cmd, capture_output=True)
            return True
        except Exception:
            pass
    return True
