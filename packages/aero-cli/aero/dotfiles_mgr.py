import os
import tarfile
import time
from typing import List


DOTFILE_TARGETS: List[str] = [
    "~/.config/aero",
    "~/.config/sway",
    "~/.config/waybar",
    "~/.config/alacritty",
    "~/.config/fish",
    "~/.gitconfig",
    "~/.bashrc",
]


def export_dotfiles(out_dir: str = ".") -> str:
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    tar_name = f"aero_dotfiles_backup_{timestamp}.tar.gz"
    tar_path = os.path.join(out_dir, tar_name)

    print(f"\n📦 \033[1;36mEXPORTING DEVELOPER DOTFILES & DESKTOP CONFIGS\033[0m")
    print("═" * 58)

    with tarfile.open(tar_path, "w:gz") as tar:
        for t in DOTFILE_TARGETS:
            exp_path = os.path.expanduser(t)
            if os.path.exists(exp_path):
                arcname = os.path.relpath(exp_path, os.path.expanduser("~"))
                tar.add(exp_path, arcname=arcname)
                print(f" • Archived: \033[1;32m{t}\033[0m")
            else:
                print(f" • Skipped:  {t} (not present)")

    print("─" * 58)
    print(f"✅ Dotfiles bundle generated: \033[1;32m{tar_path}\033[0m")
    print("═" * 58 + "\n")
    return tar_path


def import_dotfiles(tar_path: str) -> bool:
    if not os.path.exists(tar_path):
        print(f"❌ Backup archive not found: {tar_path}")
        return False

    print(f"\n📥 \033[1;36mRESTORING DEVELOPER CONFIGS FROM: {tar_path}\033[0m")
    try:
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=os.path.expanduser("~"))
        print("\033[1;32m✔ All dotfiles restored successfully!\033[0m\n")
        return True
    except Exception as e:
        print(f"❌ Error restoring archive: {e}")
        return False
