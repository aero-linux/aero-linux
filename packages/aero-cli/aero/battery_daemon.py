import glob
import os
import subprocess
from typing import Dict, Any


def check_battery_alerts() -> Dict[str, Any]:
    bat_paths = glob.glob("/sys/class/power_supply/BAT*")
    if not bat_paths:
        return {"status": "no_battery", "capacity": 100}

    bat_path = bat_paths[0]
    cap_file = os.path.join(bat_path, "capacity")
    status_file = os.path.join(bat_path, "status")

    capacity = 100
    status = "Unknown"

    if os.path.exists(cap_file):
        with open(cap_file, "r") as f:
            capacity = int(f.read().strip())
    if os.path.exists(status_file):
        with open(status_file, "r") as f:
            status = f.read().strip()

    alert_level = "normal"
    if status.lower() == "discharging":
        if capacity <= 5:
            alert_level = "critical"
            subprocess.run([
                "notify-send", "-u", "critical",
                "⚠️ CRITICAL BATTERY (5%)",
                "System will suspend shortly to prevent data loss. Connect AC adapter immediately!"
            ])
        elif capacity <= 15:
            alert_level = "low"
            subprocess.run([
                "notify-send", "-u", "normal",
                "🔋 Low Battery Warning",
                f"Battery is at {capacity}%. Please plug in your charger."
            ])

    return {"capacity": capacity, "status": status, "alert": alert_level}
