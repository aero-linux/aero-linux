import os
import shutil
import subprocess
from typing import Dict, Any


def get_disk_free_mb() -> int:
    try:
        st = os.statvfs("/")
        return int((st.f_bavail * st.f_frsize) / (1024 * 1024))
    except Exception:
        return 0


def deep_system_clean(dry_run: bool = False) -> Dict[str, Any]:
    print("\n🧹 \033[1;36mAERO INTELLIGENT DEEP DE-BLOATER & CACHE CLEANER\033[0m")
    print("═" * 56)

    free_before = get_disk_free_mb()
    actions = []

    # 1. Python Pycache in home
    pycache_cmd = "find $HOME/.cache -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true"
    actions.append(("Python __pycache__ in ~/.cache", pycache_cmd))

    # 2. Pip cache
    pip_cache = os.path.expanduser("~/.cache/pip")
    if os.path.exists(pip_cache):
        actions.append(("Python Pip Cache (~/.cache/pip)", f"rm -rf {pip_cache}"))

    # 3. NPM Cache
    if shutil.which("npm"):
        actions.append(("NPM Global Cache", "npm cache clean --force 2>/dev/null || true"))

    # 4. Systemd Journal Vacuum (Keep last 3 days)
    if shutil.which("journalctl"):
        actions.append(("Systemd Journal Logs (>3 days)", "sudo journalctl --vacuum-time=3d 2>/dev/null || true"))

    # 5. APT Archive & Orphan cleanup
    if shutil.which("apt-get"):
        actions.append(("APT Package Archives & Autoremove", "sudo apt-get autoremove -y -qq && sudo apt-get clean"))

    # 6. Flatpak unused runtimes
    if shutil.which("flatpak"):
        actions.append(("Flatpak Unused Runtimes", "flatpak uninstall --unused -y 2>/dev/null || true"))

    # 7. Docker builder cache
    if shutil.which("docker"):
        actions.append(("Docker Builder Cache & Dangling Images", "docker builder prune -f 2>/dev/null || true"))

    for name, cmd in actions:
        if dry_run:
            print(f" • [Dry-Run] Would prune: {name}")
        else:
            print(f" • Cleaning: {name}...")
            try:
                subprocess.run(cmd, shell=True, capture_output=True)
                print(f"   \033[1;32m✔ Pruned\033[0m")
            except Exception as e:
                print(f"   ⚠️  Skipped: {e}")

    free_after = get_disk_free_mb()
    freed_mb = max(0, free_after - free_before)

    print("─" * 56)
    if not dry_run:
        print(f"✅ Deep Clean Complete! Reclaimed: \033[1;32m{freed_mb} MB\033[0m storage.")
    print("═" * 56 + "\n")
    return {"freed_mb": freed_mb, "free_before_mb": free_before, "free_after_mb": free_after}
