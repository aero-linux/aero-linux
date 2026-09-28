import os
import shutil
import subprocess
from typing import Dict, Any


def integrate_appimage(appimage_path: str) -> Dict[str, Any]:
    appimage_path = os.path.abspath(appimage_path)
    if not os.path.exists(appimage_path):
        print(f"❌ File not found: {appimage_path}")
        return {"status": "error", "error": "not_found"}

    base_name = os.path.splitext(os.path.basename(appimage_path))[0]
    clean_name = base_name.replace("-x86_64", "").replace(".AppImage", "").replace("-", " ").title()

    bin_dir = os.path.expanduser("~/.local/bin")
    apps_dir = os.path.expanduser("~/.local/share/applications")
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(apps_dir, exist_ok=True)

    dest_bin = os.path.join(bin_dir, os.path.basename(appimage_path))
    shutil.copyfile(appimage_path, dest_bin)
    os.chmod(dest_bin, 0o755)

    desktop_file = os.path.join(apps_dir, f"appimage-{base_name.lower()}.desktop")
    desktop_content = f"""[Desktop Entry]
Name={clean_name}
Comment={clean_name} Portable AppImage
Exec={dest_bin}
Icon=application-x-executable
Terminal=false
Type=Application
Categories=Utility;Development;
"""
    with open(desktop_file, "w") as f:
        f.write(desktop_content)

    print(f"📦 \033[1;36mINTEGRATING APPIMAGE APPLICATION\033[0m")
    print("═" * 55)
    print(f" • Name:        \033[1;32m{clean_name}\033[0m")
    print(f" • Executable:  \033[1;33m{dest_bin}\033[0m")
    print(f" • Launcher:    \033[1;32m{desktop_file}\033[0m")
    print("\n✅ AppImage integrated into Start Menu and Application Switcher.\n")

    subprocess.run(["notify-send", "📦 AppImage Installed", f"{clean_name} is now available in the Start Menu"])
    return {"status": "installed", "name": clean_name, "bin": dest_bin, "desktop": desktop_file}
