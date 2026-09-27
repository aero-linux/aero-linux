import os
import tarfile
from datetime import datetime

from typing import Optional

CONFIG_PATHS = [
    ".config/sway",
    ".config/waybar",
    ".config/alacritty",
    ".config/fish",
    ".gitconfig",
]


def export_backup(output_path: Optional[str] = None) -> str:
    home = os.path.expanduser("~")
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(home, f"aero-dotfiles-backup-{timestamp}.tar.gz")

    print(f"📦 Exporting Aero desktop configurations to: {output_path}...")
    
    with tarfile.open(output_path, "w:gz") as tar:
        for rel_path in CONFIG_PATHS:
            full_path = os.path.join(home, rel_path)
            if os.path.exists(full_path):
                tar.add(full_path, arcname=rel_path)
                print(f"  • Added: ~/{rel_path}")

    print(f"✅ Backup created successfully: {output_path}")
    return output_path


def import_backup(archive_path: str) -> bool:
    if not os.path.exists(archive_path):
        print(f"❌ Backup archive not found: {archive_path}")
        return False

    home = os.path.expanduser("~")
    print(f"📥 Restoring Aero configurations from: {archive_path}...")

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=home)
        print("✅ Aero desktop configurations restored successfully.")
        return True
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False
