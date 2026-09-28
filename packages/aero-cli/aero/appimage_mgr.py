import glob
import os
import re
import shutil
import subprocess
import tempfile
from typing import Dict, Any, List


def integrate_appimage(appimage_path: str) -> Dict[str, Any]:
    appimage_path = os.path.abspath(appimage_path)
    if not os.path.exists(appimage_path):
        print(f"❌ File not found: {appimage_path}")
        return {"status": "error", "error": "not_found"}

    base_name = os.path.splitext(os.path.basename(appimage_path))[0]
    clean_slug = re.sub(r'[^a-zA-Z0-9_\-]', '', base_name.lower().replace(" ", "-"))
    clean_title = base_name.replace("-x86_64", "").replace(".AppImage", "").replace("-", " ").title()

    bin_dir = os.path.expanduser("~/.local/bin")
    apps_dir = os.path.expanduser("~/.local/share/applications")
    icons_dir = os.path.expanduser("~/.local/share/icons/hicolor/256x256/apps")
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(apps_dir, exist_ok=True)
    os.makedirs(icons_dir, exist_ok=True)

    dest_bin = os.path.join(bin_dir, f"{clean_slug}.AppImage")
    shutil.copyfile(appimage_path, dest_bin)
    os.chmod(dest_bin, 0o755)

    icon_path = ""
    app_categories = "Utility;Development;"

    # Deep inspection: extract embedded icon and metadata from AppImage squashfs
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            # Extract metadata without running full payload
            subprocess.run(
                [dest_bin, "--appimage-extract", "*.desktop"],
                cwd=tmpdir,
                capture_output=True,
                timeout=5
            )
            subprocess.run(
                [dest_bin, "--appimage-extract", "*.png"],
                cwd=tmpdir,
                capture_output=True,
                timeout=5
            )
            subprocess.run(
                [dest_bin, "--appimage-extract", "*.svg"],
                cwd=tmpdir,
                capture_output=True,
                timeout=5
            )

            # Search extracted icons
            found_icons = glob.glob(os.path.join(tmpdir, "squashfs-root", "*.png")) + \
                          glob.glob(os.path.join(tmpdir, "squashfs-root", "*.svg"))
            if found_icons:
                chosen_icon = found_icons[0]
                ext = os.path.splitext(chosen_icon)[1]
                dest_icon = os.path.join(icons_dir, f"{clean_slug}{ext}")
                shutil.copyfile(chosen_icon, dest_icon)
                icon_path = dest_icon

            # Search extracted desktop entry
            found_desktops = glob.glob(os.path.join(tmpdir, "squashfs-root", "*.desktop"))
            if found_desktops:
                with open(found_desktops[0], "r") as f:
                    for line in f:
                        if line.startswith("Name="):
                            clean_title = line.split("=", 1)[1].strip()
                        elif line.startswith("Categories="):
                            app_categories = line.split("=", 1)[1].strip()
        except Exception:
            pass

    # Generate Linux Mint standard .desktop launcher
    desktop_file = os.path.join(apps_dir, f"aero-appimage-{clean_slug}.desktop")
    desktop_content = f"""[Desktop Entry]
Name={clean_title}
GenericName={clean_title} (AppImage)
Comment={clean_title} Portable Linux AppImage
Exec="{dest_bin}" %U
Icon={icon_path if icon_path else "application-x-executable"}
Terminal=false
Type=Application
Categories={app_categories}
StartupNotify=true
X-AppImage-Version=1.0
X-Aero-Managed=true
"""
    with open(desktop_file, "w") as f:
        f.write(desktop_content)

    # Refresh desktop launcher cache
    if shutil.which("update-desktop-database"):
        subprocess.run(["update-desktop-database", apps_dir], capture_output=True)

    print(f"📦 \033[1;36mAERO LINUX APPIMAGE INTEGRATION ENGINE\033[0m")
    print("═" * 58)
    print(f" • Application:   \033[1;32m{clean_title}\033[0m")
    print(f" • Executable:    \033[1;33m{dest_bin}\033[0m")
    print(f" • Icon Extracted:\033[1;36m{icon_path if icon_path else 'Default System Icon'}\033[0m")
    print(f" • Start Menu:    \033[1;32m{desktop_file}\033[0m")
    print("═" * 58)
    print("✅ AppImage deeply integrated with Start Menu & file associations.\n")

    subprocess.run([
        "notify-send",
        "-i", icon_path if icon_path else "application-x-executable",
        "📦 AppImage Installed",
        f"{clean_title} has been added to your Start Menu."
    ], capture_output=True)

    return {
        "status": "installed",
        "name": clean_title,
        "slug": clean_slug,
        "bin": dest_bin,
        "icon": icon_path,
        "desktop": desktop_file
    }


def list_appimages() -> List[Dict[str, Any]]:
    apps_dir = os.path.expanduser("~/.local/share/applications")
    results = []
    if not os.path.exists(apps_dir):
        return results

    for fname in os.listdir(apps_dir):
        if fname.startswith("aero-appimage-") and fname.endswith(".desktop"):
            fpath = os.path.join(apps_dir, fname)
            name = fname
            with open(fpath, "r") as f:
                for line in f:
                    if line.startswith("Name="):
                        name = line.split("=", 1)[1].strip()
                        break
            results.append({"name": name, "file": fpath})
    return results


def remove_appimage(slug: str) -> Dict[str, Any]:
    slug = slug.lower().replace(" ", "-")
    bin_path = os.path.expanduser(f"~/.local/bin/{slug}.AppImage")
    desktop_path = os.path.expanduser(f"~/.local/share/applications/aero-appimage-{slug}.desktop")

    removed = False
    if os.path.exists(bin_path):
        os.remove(bin_path)
        removed = True
    if os.path.exists(desktop_path):
        os.remove(desktop_path)
        removed = True

    if removed:
        print(f"🗑️  Removed AppImage: {slug}")
        return {"status": "removed", "slug": slug}
    print(f"❌ AppImage not found: {slug}")
    return {"status": "not_found", "slug": slug}
