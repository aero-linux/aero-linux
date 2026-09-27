import shutil
import subprocess


def update_packages() -> bool:
    print("🔄 Updating system package repositories...")
    success = True
    if shutil.which("apt-get"):
        print("📦 Updating APT repositories...")
        res = subprocess.run(["sudo", "apt-get", "update"])
        if res.returncode != 0:
            success = False

    if shutil.which("flatpak"):
        print("📦 Updating Flatpak repositories...")
        subprocess.run(["flatpak", "update", "-y"])

    return success


def clean_system() -> dict:
    print("🧹 Cleaning system package caches and orphaned dependencies...")
    freed_info = {"apt_cleaned": False, "orphans_removed": False, "flatpak_cleaned": False}

    if shutil.which("apt-get"):
        subprocess.run(["sudo", "apt-get", "autoremove", "-y", "--purge"], capture_output=True)
        subprocess.run(["sudo", "apt-get", "clean"], capture_output=True)
        subprocess.run(["sudo", "apt-get", "autoclean"], capture_output=True)
        freed_info["apt_cleaned"] = True
        freed_info["orphans_removed"] = True

    if shutil.which("flatpak"):
        subprocess.run(["flatpak", "uninstall", "--unused", "-y"], capture_output=True)
        freed_info["flatpak_cleaned"] = True

    print("✅ System caches and unused dependencies pruned successfully.")
    return freed_info


def install_packages(packages: list) -> bool:
    if not packages:
        print("❌ No packages specified.")
        return False

    if shutil.which("apt-get"):
        print(f"📦 Installing {len(packages)} packages via APT...")
        cmd = ["sudo", "apt-get", "install", "-y"] + packages
        res = subprocess.run(cmd)
        return res.returncode == 0
    return False
