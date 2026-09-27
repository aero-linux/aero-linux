import os
import shutil
import subprocess
import sys


def get_cpu_info() -> dict:
    info = {"model": "Unknown", "cores": os.cpu_count() or 1, "governor": "Unknown"}
    try:
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r") as f:
                for line in f:
                    if "model name" in line:
                        info["model"] = line.split(":", 1)[1].strip()
                        break
        gov_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
        if os.path.exists(gov_path):
            with open(gov_path, "r") as f:
                info["governor"] = f.read().strip()
    except Exception:
        pass
    return info


def get_memory_info() -> dict:
    mem = {"total_mb": 0, "available_mb": 0, "zram_active": False, "zram_size_mb": 0}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split()
                if parts[0] == "MemTotal:":
                    mem["total_mb"] = int(parts[1]) // 1024
                elif parts[0] == "MemAvailable:":
                    mem["available_mb"] = int(parts[1]) // 1024

        if os.path.exists("/sys/block/zram0"):
            mem["zram_active"] = True
            with open("/sys/block/zram0/disksize", "r") as f:
                mem["zram_size_mb"] = int(f.read().strip()) // (1024 * 1024)
    except Exception:
        pass
    return mem


def get_gpu_info() -> list:
    gpus = []
    # Check NVIDIA
    if shutil.which("nvidia-smi"):
        try:
            res = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0:
                for line in res.stdout.strip().split("\n"):
                    if line.strip():
                        parts = [p.strip() for p in line.split(",")]
                        gpus.append({
                            "vendor": "NVIDIA",
                            "model": parts[0],
                            "vram": parts[1] if len(parts) > 1 else "Unknown",
                            "driver": parts[2] if len(parts) > 2 else "Unknown",
                            "cuda": True,
                        })
        except Exception:
            pass

    # Check AMD/Intel via lspci or DRI
    if not gpus and shutil.which("lspci"):
        try:
            res = subprocess.run(["lspci"], capture_output=True, text=True, timeout=5)
            for line in res.stdout.split("\n"):
                if "VGA compatible controller" in line or "3D controller" in line:
                    if "AMD" in line or "Advanced Micro Devices" in line or "Radeon" in line:
                        gpus.append({
                            "vendor": "AMD",
                            "model": line.split(":", 2)[-1].strip(),
                            "rocm_ready": os.path.exists("/dev/kfd"),
                        })
                    elif "Intel" in line:
                        gpus.append({
                            "vendor": "Intel",
                            "model": line.split(":", 2)[-1].strip(),
                            "oneapi_ready": True,
                        })
        except Exception:
            pass
    return gpus


def get_battery_info() -> dict:
    bat = {"present": False, "percentage": 0, "status": "Unknown", "threshold_supported": False}
    power_supply = "/sys/class/power_supply"
    if os.path.exists(power_supply):
        for supply in os.listdir(power_supply):
            if supply.startswith("BAT"):
                bat_dir = os.path.join(power_supply, supply)
                bat["present"] = True
                try:
                    with open(os.path.join(bat_dir, "capacity"), "r") as f:
                        bat["percentage"] = int(f.read().strip())
                    with open(os.path.join(bat_dir, "status"), "r") as f:
                        bat["status"] = f.read().strip()
                    if os.path.exists(os.path.join(bat_dir, "charge_control_end_threshold")):
                        bat["threshold_supported"] = True
                except Exception:
                    pass
                break
    return bat


def run_doctor() -> dict:
    cpu = get_cpu_info()
    mem = get_memory_info()
    gpus = get_gpu_info()
    bat = get_battery_info()

    ai_stack = {
        "docker": shutil.which("docker") is not None,
        "ollama": shutil.which("ollama") is not None,
        "python": sys.version.split()[0],
        "git": shutil.which("git") is not None,
    }

    report = {
        "os": "Aero Linux (Rolling Edge)",
        "kernel": os.uname().release,
        "cpu": cpu,
        "memory": mem,
        "gpus": gpus,
        "battery": bat,
        "ai_stack": ai_stack,
    }
    return report
