import os
import glob
import subprocess
import shutil
from typing import List, Dict, Any


def list_usb_drives() -> List[Dict[str, Any]]:
    drives = []
    block_devices = glob.glob("/sys/block/sd*")
    for bd in block_devices:
        dev_name = os.path.basename(bd)
        dev_path = f"/dev/{dev_name}"
        
        # Check if removable
        removable = False
        rem_file = os.path.join(bd, "removable")
        if os.path.exists(rem_file):
            with open(rem_file) as f:
                removable = f.read().strip() == "1"

        # Size in GB
        size_gb = 0.0
        size_file = os.path.join(bd, "size")
        if os.path.exists(size_file):
            with open(size_file) as f:
                size_gb = round((int(f.read().strip()) * 512) / (1024**3), 2)

        # Model
        model = "USB Flash Drive"
        model_file = os.path.join(bd, "device", "model")
        if os.path.exists(model_file):
            with open(model_file) as f:
                model = f.read().strip()

        if removable or size_gb <= 128:
            drives.append({
                "device": dev_path,
                "name": dev_name,
                "model": model,
                "size_gb": size_gb,
                "removable": removable
            })
    return drives


def flash_iso(iso_path: str, target_dev: str) -> bool:
    if not os.path.exists(iso_path):
        print(f"❌ ISO file not found: {iso_path}")
        return False

    if not target_dev.startswith("/dev/sd") or target_dev.startswith("/dev/nvme"):
        print(f"❌ Safety Error: Target device '{target_dev}' is protected or not a valid USB drive.")
        return False

    print(f"\n💾 \033[1;36mAERO USB LIVE MEDIA FLASHER\033[0m")
    print("═" * 58)
    print(f" • ISO Source:   \033[1;32m{iso_path}\033[0m")
    print(f" • Target Drive: \033[1;31m{target_dev}\033[0m (ALL DATA WILL BE OVERWRITTEN)")
    print("═" * 58)

    cmd = f"sudo dd if='{iso_path}' of='{target_dev}' bs=4M status=progress oflag=sync"
    print(f"Executing: {cmd}\n")
    try:
        res = subprocess.run(cmd, shell=True)
        if res.returncode == 0:
            print("\n\033[1;32m✔ ISO Flashing Completed Successfully! Drive is bootable.\033[0m\n")
            return True
        else:
            print(f"\n❌ Error flashing ISO. Exit code: {res.returncode}\n")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
