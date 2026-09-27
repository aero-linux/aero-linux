import os
import shutil
import subprocess
from datetime import datetime


def create_snapshot(comments: str = "") -> bool:
    tag = comments if comments else f"aero-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    print(f"📸 Creating system restore snapshot: {tag}...")

    if shutil.which("timeshift"):
        res = subprocess.run(["sudo", "timeshift", "--create", "--comments", tag, "--tags", "D"])
        if res.returncode == 0:
            print(f"✅ Snapshot '{tag}' created successfully with Timeshift.")
            return True

    # Fallback to Btrfs subvolume snapshot if root is btrfs
    try:
        check = subprocess.run(["findmnt", "-n", "-o", "FSTYPE", "/"], capture_output=True, text=True)
        if "btrfs" in check.stdout:
            os_subvol = "/.snapshots"
            subprocess.run(["sudo", "mkdir", "-p", os_subvol], check=True)
            res = subprocess.run(["sudo", "btrfs", "subvolume", "snapshot", "-r", "/", f"{os_subvol}/{tag}"])
            if res.returncode == 0:
                print(f"✅ Btrfs subvolume snapshot '{tag}' created successfully.")
                return True
    except Exception:
        pass

    print("⚠️ Timeshift or Btrfs not configured on this filesystem.")
    return False


def list_snapshots():
    print("📸 System Restore Snapshots:")
    print("--------------------------------------------------")
    if shutil.which("timeshift"):
        subprocess.run(["sudo", "timeshift", "--list"])
        return

    try:
        check = subprocess.run(["findmnt", "-n", "-o", "FSTYPE", "/"], capture_output=True, text=True)
        if "btrfs" in check.stdout and os.path.exists("/.snapshots"):
            subprocess.run(["sudo", "btrfs", "subvolume", "list", "/.snapshots"])
            return
    except Exception:
        pass

    print("No active snapshot daemon found. Run 'sudo apt-get install -y timeshift' to enable automated restore points.")


def restore_snapshot(tag: str) -> bool:
    print(f"🔄 Preparing system restore from snapshot '{tag}'...")
    if shutil.which("timeshift"):
        res = subprocess.run(["sudo", "timeshift", "--restore", "--snapshot", tag])
        return res.returncode == 0
    print("❌ Automated restore requires Timeshift CLI.")
    return False
