import os
import subprocess
from typing import List, Dict, Any


def get_active_turbo_mounts() -> List[Dict[str, Any]]:
    mounts = []
    try:
        with open("/proc/mounts") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3 and parts[2] == "tmpfs" and "aero_turbo" in parts[3]:
                    mounts.append({
                        "device": parts[0],
                        "mountpoint": parts[1],
                        "options": parts[3],
                    })
    except Exception:
        pass
    return mounts


def mount_turbo_ramdisk(target_path: str = "./target", size_mb: int = 4096) -> bool:
    target_path = os.path.abspath(target_path)
    os.makedirs(target_path, exist_ok=True)

    print(f"\n🚀 \033[1;36mAERO TURBO RAM-DISK COMPILATION ACCELERATOR\033[0m")
    print("═" * 60)
    print(f" • Target Build Directory: \033[1;32m{target_path}\033[0m")
    print(f" • Allocated RAM-Disk:     \033[1;36m{size_mb} MB (tmpfs in zRAM/RAM)\033[0m")
    print(" • Throughput Expected:    \033[1;32m~10,000+ MB/s (Zero SSD Wear)\033[0m")
    print("─" * 60)

    cmd = f"sudo mount -t tmpfs -o size={size_mb}M,comment=aero_turbo tmpfs '{target_path}'"
    try:
        res = subprocess.run(cmd, shell=True)
        if res.returncode == 0:
            print(f"✔ Turbo RAM-Disk mounted at: {target_path}")
            print("Compile tasks (cargo build, npm run build, make) will run in RAM.\n")
            return True
        else:
            print(f"❌ Failed to mount tmpfs. Exit code: {res.returncode}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def unmount_turbo_ramdisk(target_path: str = "./target") -> bool:
    target_path = os.path.abspath(target_path)
    print(f"Unmounting Turbo RAM-Disk at: {target_path}...")
    try:
        res = subprocess.run(f"sudo umount '{target_path}'", shell=True)
        if res.returncode == 0:
            print("✔ Unmounted successfully.")
            return True
        else:
            print("❌ Unmount failed or target is not mounted.")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
