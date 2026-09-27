import os
import subprocess


PROFILES = {
    "battery": {
        "governor": "powersave",
        "energy_perf": "power",
        "boost": "0",
        "description": "Maximum battery preservation, CPU boost off, silent fans",
    },
    "balanced": {
        "governor": "powersave",
        "energy_perf": "balance_performance",
        "boost": "1",
        "description": "Adaptive dynamic scaling with automatic boost on active load",
    },
    "boost": {
        "governor": "performance",
        "energy_perf": "performance",
        "boost": "1",
        "description": "High performance profile with sustained clock frequency",
    },
    "gaming": {
        "governor": "performance",
        "energy_perf": "performance",
        "boost": "1",
        "description": "Ultra low-latency game & AI compute profile with GameMode",
    },
}


def get_current_profile() -> str:
    gov_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    boost_path = "/sys/devices/system/cpu/cpufreq/boost"
    if not os.path.exists(gov_path):
        return "balanced"

    try:
        with open(gov_path, "r") as f:
            gov = f.read().strip()
        boost = "1"
        if os.path.exists(boost_path):
            with open(boost_path, "r") as f:
                boost = f.read().strip()

        if gov == "performance":
            return "boost"
        elif gov == "powersave" and boost == "0":
            return "battery"
        else:
            return "balanced"
    except Exception:
        return "balanced"


def set_profile(profile_name: str) -> bool:
    if profile_name not in PROFILES:
        raise ValueError(f"Unknown profile: {profile_name}. Available: {list(PROFILES.keys())}")

    prof = PROFILES[profile_name]

    # Set governor for all CPUs
    cpu_dir = "/sys/devices/system/cpu"
    if os.path.exists(cpu_dir):
        for entry in os.listdir(cpu_dir):
            if entry.startswith("cpu") and entry[3:].isdigit():
                gov_file = os.path.join(cpu_dir, entry, "cpufreq", "scaling_governor")
                if os.path.exists(gov_file):
                    try:
                        with open(gov_file, "w") as f:
                            f.write(prof["governor"])
                    except PermissionError:
                        subprocess.run(
                            ["sudo", "tee", gov_file],
                            input=prof["governor"],
                            text=True,
                            capture_output=True,
                        )

                epp_file = os.path.join(cpu_dir, entry, "cpufreq", "energy_performance_preference")
                if os.path.exists(epp_file):
                    try:
                        with open(epp_file, "w") as f:
                            f.write(prof["energy_perf"])
                    except PermissionError:
                        subprocess.run(
                            ["sudo", "tee", epp_file],
                            input=prof["energy_perf"],
                            text=True,
                            capture_output=True,
                        )

    # Set boost
    boost_path = "/sys/devices/system/cpu/cpufreq/boost"
    if os.path.exists(boost_path):
        try:
            with open(boost_path, "w") as f:
                f.write(prof["boost"])
        except PermissionError:
            subprocess.run(
                ["sudo", "tee", boost_path],
                input=prof["boost"],
                text=True,
                capture_output=True,
            )

    return True


def set_charge_threshold(threshold: int = 80) -> bool:
    if not (20 <= threshold <= 100):
        raise ValueError("Threshold must be between 20 and 100 percent")

    power_supply = "/sys/class/power_supply"
    if os.path.exists(power_supply):
        for supply in os.listdir(power_supply):
            if supply.startswith("BAT"):
                thresh_file = os.path.join(power_supply, supply, "charge_control_end_threshold")
                if os.path.exists(thresh_file):
                    try:
                        with open(thresh_file, "w") as f:
                            f.write(str(threshold))
                        return True
                    except PermissionError:
                        res = subprocess.run(
                            ["sudo", "tee", thresh_file],
                            input=str(threshold),
                            text=True,
                            capture_output=True,
                        )
                        return res.returncode == 0
    return False
