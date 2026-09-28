import os
import shutil
import subprocess
from typing import Dict, Any, List


def get_phone_devices() -> List[Dict[str, Any]]:
    devices = []
    if shutil.which("kdeconnect-cli"):
        try:
            out = subprocess.check_output(["kdeconnect-cli", "-a", "--id-name-only"], text=True)
            for line in out.splitlines():
                if line.strip():
                    parts = line.strip().split(" ", 1)
                    dev_id = parts[0]
                    dev_name = parts[1] if len(parts) > 1 else "Phone"
                    devices.append({"id": dev_id, "name": dev_name, "reachable": True})
        except Exception:
            pass
    return devices


def show_phone_status() -> Dict[str, Any]:
    print("📱 \033[1;36mAERO PHONE LINK & WIRELESS SYNC (ZORIN CONNECT STYLE)\033[0m")
    print("═" * 55)

    if not shutil.which("kdeconnect-cli"):
        print(" • Phone Link Service: \033[1;33mNot Installed\033[0m")
        print(" • To enable wireless phone sync (Android/iOS), run:")
        print("   \033[1;32msudo apt install kdeconnect\033[0m (or install via Aero App Store)\n")
        return {"status": "not_installed", "devices": []}

    devices = get_phone_devices()
    if not devices:
        print(" • No phone currently paired over Wi-Fi.")
        print(" • Open KDE Connect / Zorin Connect app on your phone to pair.\n")
    else:
        print(f" • Paired Devices: \033[1;32m{len(devices)}\033[0m\n")
        for dev in devices:
            print(f" 📱 {dev['name']} (ID: {dev['id']})")
        print()
    return {"status": "ready", "devices": devices}


def send_file_to_phone(file_path: str, device_id: str = "") -> bool:
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    if shutil.which("kdeconnect-cli"):
        cmd = ["kdeconnect-cli", "--share", file_path]
        if device_id:
            cmd.extend(["-d", device_id])
        subprocess.run(cmd)
        print(f"✅ Sent {file_path} to mobile device.")
        return True
    print("ℹ️ kdeconnect-cli is required to beam files to phone.")
    return False
