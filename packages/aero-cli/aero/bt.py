import subprocess
import shutil


def check_bt_status():
    print("📶 \033[1;36mBLUETOOTH CONTROLLER & DEVICE STATUS\033[0m")
    print("═" * 55)

    if not shutil.which("bluetoothctl"):
        print("ℹ️ bluetoothctl not found.")
        return

    try:
        res = subprocess.run(["bluetoothctl", "show"], capture_output=True, text=True)
        powered = "Powered: yes" in res.stdout
        print(f" • Controller State: {'\033[1;32mPOWERED ON\033[0m' if powered else '\033[90mPOWERED OFF (Battery Saving)\033[0m'}")
        
        dev_res = subprocess.run(["bluetoothctl", "devices", "Connected"], capture_output=True, text=True)
        conns = dev_res.stdout.strip().split("\n")
        if conns and conns[0]:
            print("Connected Devices:")
            for d in conns:
                print(f"   • {d}")
        else:
            print(" • Connected Devices: None")
    except Exception as e:
        print(f"Bluetooth error: {e}")
    print()


def toggle_bt_power(state: bool = False):
    action = "on" if state else "off"
    print(f"📶 Turning Bluetooth radio {action.upper()}...")
    if shutil.which("bluetoothctl"):
        try:
            subprocess.run(["bluetoothctl", "power", action], check=True, capture_output=True)
            print(f"✅ Bluetooth is now {action.upper()}.")
            return True
        except Exception as e:
            print(f"❌ Failed: {e}")
            return False
    return False
