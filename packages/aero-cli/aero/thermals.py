import os
import glob


def get_temperatures():
    thermals = []
    hwmon_paths = glob.glob("/sys/class/hwmon/hwmon*")
    
    for hpath in sorted(hwmon_paths):
        name = "Unknown"
        name_file = os.path.join(hpath, "name")
        if os.path.exists(name_file):
            try:
                with open(name_file) as f:
                    name = f.read().strip()
            except Exception:
                pass

        temp_inputs = glob.glob(os.path.join(hpath, "temp*_input"))
        for tfile in sorted(temp_inputs):
            try:
                with open(tfile) as f:
                    temp_c = int(f.read().strip()) / 1000.0
                
                label_file = tfile.replace("_input", "_label")
                label = ""
                if os.path.exists(label_file):
                    with open(label_file) as lf:
                        label = lf.read().strip()
                
                thermals.append({"chip": name, "label": label or "Core Temp", "temp_c": temp_c})
            except Exception:
                pass

    return thermals


def show_thermals():
    print("🌡️  \033[1;36mAERO HARDWARE THERMAL & FAN SENSORS\033[0m")
    print("═" * 55)

    thermals = get_temperatures()
    if not thermals:
        print("ℹ️ No hardware thermal sensors detected in /sys/class/hwmon.")
        return

    for t in thermals:
        temp = t["temp_c"]
        color = "\033[32m"  # Green
        if temp >= 75:
            color = "\033[31m"  # Red
        elif temp >= 60:
            color = "\033[33m"  # Yellow

        print(f" • \033[1m{t['chip']:<15}\033[0m ({t['label']:<12}) ➔ {color}{temp:.1f}°C\033[0m")
    print()
