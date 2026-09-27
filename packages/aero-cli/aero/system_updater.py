import subprocess
import shutil
import platform


def check_system_kernel():
    print("🐧 \033[1;36mAERO KERNEL & OS VERSION AUDIT\033[0m")
    print("═" * 55)
    print(f" • Architecture:   \033[1;32m{platform.machine()}\033[0m")
    print(f" • Active Kernel:  \033[1;33m{platform.release()}\033[0m")
    print(f" • OS Release:     Aero Linux 1.0 (Rolling Edge)")
    print(f" • Low-Latency:    {'✅ Active' if 'lowlatency' in platform.release() or 'xanmod' in platform.release() or 'zen' in platform.release() else 'ℹ️ Standard'}")
    print()


def update_aero_os():
    print("🚀 \033[1;36mUpdating Aero Linux Core Suite & System Packages...\033[0m")
    
    if shutil.which("apt-get"):
        print("1. Upgrading system base packages...")
        subprocess.run(["sudo", "apt-get", "update"])
        subprocess.run(["sudo", "apt-get", "upgrade", "-y"])

    if shutil.which("pip"):
        print("2. Upgrading Aero CLI suite...")
        subprocess.run(["pip", "install", "--upgrade", "aero-cli"], capture_output=True)

    print("✅ System upgrade complete.")
