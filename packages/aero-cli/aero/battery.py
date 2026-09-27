import os
from typing import Any, Dict


def get_battery_health() -> Dict[str, Any]:
    bat_path = "/sys/class/power_supply/BAT0"
    if not os.path.exists(bat_path):
        return {"present": False}

    info: Dict[str, Any] = {"present": True}
    
    # Read capacity
    try:
        with open(os.path.join(bat_path, "capacity")) as f:
            info["percentage"] = int(f.read().strip())
    except Exception:
        info["percentage"] = 0

    # Read status
    try:
        with open(os.path.join(bat_path, "status")) as f:
            info["status"] = f.read().strip()
    except Exception:
        info["status"] = "Unknown"

    # Read design vs full capacity
    energy_full = None
    energy_design = None
    
    for full_name in ["energy_full", "charge_full"]:
        p = os.path.join(bat_path, full_name)
        if os.path.exists(p):
            with open(p) as f:
                energy_full = int(f.read().strip())
            break

    for design_name in ["energy_full_design", "charge_full_design"]:
        p = os.path.join(bat_path, design_name)
        if os.path.exists(p):
            with open(p) as f:
                energy_design = int(f.read().strip())
            break

    if energy_full and energy_design:
        info["health_percentage"] = round((energy_full / energy_design) * 100, 1)
        info["energy_full_wh"] = round(energy_full / 1_000_000, 1)
        info["energy_design_wh"] = round(energy_design / 1_000_000, 1)
    else:
        info["health_percentage"] = 100.0

    # Cycle count
    cycle_file = os.path.join(bat_path, "cycle_count")
    if os.path.exists(cycle_file):
        try:
            with open(cycle_file) as f:
                info["cycle_count"] = int(f.read().strip())
        except Exception:
            info["cycle_count"] = "N/A"
    else:
        info["cycle_count"] = "N/A"

    return info


def show_battery_health():
    print("🔋 \033[1;36mAERO BATTERY & LITHIUM WEAR AUDIT\033[0m")
    print("═" * 55)

    health = get_battery_health()
    if not health.get("present"):
        print("ℹ️ No battery detected (Desktop or AC power).")
        return

    print(f" • Current Charge:    \033[1;32m{health.get('percentage')}% ({health.get('status')})\033[0m")
    print(f" • Battery Health:    \033[1;33m{health.get('health_percentage')}%\033[0m capacity retained")
    if "energy_full_wh" in health:
        print(f" • Usable Capacity:   {health['energy_full_wh']} Wh (Original: {health['energy_design_wh']} Wh)")
    print(f" • Charge Cycles:     {health.get('cycle_count')}")

    # Charge threshold check
    thresh_file = "/sys/class/power_supply/BAT0/charge_control_end_threshold"
    if os.path.exists(thresh_file):
        with open(thresh_file) as f:
            t = f.read().strip()
        print(f" • Hardware Cap:      \033[1;36m{t}%\033[0m (Cap with: 'aero power --threshold 80')")
    print()
