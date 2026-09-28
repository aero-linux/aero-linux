import os
import shutil
import subprocess
import time
from typing import Dict, Any


def get_ac_power_status() -> bool:
    """Returns True if AC power is connected, False if on battery."""
    ac_paths = [
        "/sys/class/power_supply/AC/online",
        "/sys/class/power_supply/ADP1/online",
        "/sys/class/power_supply/ACAD/online",
        "/sys/class/power_supply/BAT0/status",
    ]
    for p in ac_paths:
        if os.path.exists(p):
            try:
                with open(p, "r") as f:
                    val = f.read().strip()
                    if val == "1" or val.lower() == "charging" or val.lower() == "full":
                        return True
                    elif val == "0" or val.lower() == "discharging":
                        return False
            except Exception:
                pass
    return True  # Default to AC if undetermined


def apply_power_state(is_ac: bool) -> Dict[str, Any]:
    state = "AC (High Performance)" if is_ac else "Battery (Power Saver & Silent)"
    print(f"⚡ \033[1;36mAERO AUTONOMOUS POWER GOVERNOR\033[0m: \033[1;32m{state}\033[0m")

    # 1. TLP Profile
    if shutil.which("tlp"):
        mode = "ac" if is_ac else "bat"
        subprocess.run(["tlp", mode], capture_output=True)

    # 2. CPU Boost Policy
    boost_path = "/sys/devices/system/cpu/cpufreq/boost"
    if os.path.exists(boost_path):
        try:
            with open(boost_path, "w") as f:
                f.write("1" if is_ac else "0")
        except Exception:
            pass

    # 3. Notification
    msg = "Full Turbo Performance Unlocked" if is_ac else "Power Saver & Whisper-Quiet Cooling Active"
    icon = "battery-charging" if is_ac else "battery-good"
    subprocess.run([
        "notify-send",
        "-i", icon,
        "-h", "string:x-canonical-private-synchronous:osd_power",
        "⚡ Power Source Changed",
        f"Switching to {state} — {msg}"
    ], capture_output=True)

    return {"is_ac": is_ac, "state": state, "status": "applied"}


def start_power_daemon():
    print("⚡ Starting Aero Autonomous Power Daemon...")
    last_state = None
    while True:
        current_state = get_ac_power_status()
        if current_state != last_state:
            apply_power_state(current_state)
            last_state = current_state
        time.sleep(5)
