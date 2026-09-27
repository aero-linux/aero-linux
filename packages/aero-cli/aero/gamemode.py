import os
import subprocess
import shutil
import sys


def apply_gaming_optimizations():
    print("🎮 \033[1;36mActivating Aero GameMode Optimizations...\033[0m")
    
    # Set performance governor
    cpu_gov_path = "/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    if os.path.exists(cpu_gov_path):
        subprocess.run(["sudo", "tee", "/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"], input="performance", text=True, capture_output=True)
        print("  • CPU Governor switched to: \033[1;32mPERFORMANCE\033[0m")

    # Set AMD GPU to high performance if available
    amd_power_dpm = "/sys/class/drm/card0/device/power_dpm_force_performance_level"
    if os.path.exists(amd_power_dpm):
        subprocess.run(["sudo", "tee", amd_power_dpm], input="high", text=True, capture_output=True)
        print("  • GPU Power State switched to: \033[1;32mHIGH\033[0m")

    # Wine / DXVK environment variables
    os.environ["DXVK_ASYNC"] = "1"
    os.environ["MESA_GL_THREAD_FULL"] = "1"
    os.environ["__GL_THREADED_OPTIMIZATIONS"] = "1"
    os.environ["GAMEMODERUNEXEC"] = "1"


def restore_default_optimizations():
    print("🎮 Restoring balanced power profile...")
    subprocess.run(["sudo", "tee", "/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"], input="powersave", text=True, capture_output=True)


def run_game(command_args: list):
    if not command_args:
        print("❌ No game executable or command provided.")
        print("Usage: aero gamemode run <executable or steam appid>")
        return

    apply_gaming_optimizations()
    print(f"🚀 Launching: {' '.join(command_args)}\n")

    try:
        proc = subprocess.run(command_args)
        sys.exit(proc.returncode)
    except KeyboardInterrupt:
        pass
    finally:
        restore_default_optimizations()
