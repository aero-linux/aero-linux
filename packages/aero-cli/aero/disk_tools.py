import os
import subprocess
import shutil


def find_large_files(directory: str = ".", min_mb: int = 100):
    print(f"🔍 \033[1;36mScanning for files larger than {min_mb}MB in '{directory}'...\033[0m")
    print("═" * 60)

    large_files = []
    min_bytes = min_mb * 1024 * 1024

    for root, dirs, files in os.walk(directory):
        # Skip .git and hidden caches
        if "/.git" in root or "/.cache" in root:
            continue
        for f in files:
            fpath = os.path.join(root, f)
            try:
                if not os.path.islink(fpath):
                    sz = os.path.getsize(fpath)
                    if sz >= min_bytes:
                        large_files.append((fpath, sz / (1024 * 1024)))
            except Exception:
                pass

    large_files.sort(key=lambda x: x[1], reverse=True)

    if not large_files:
        print("  ✅ No abnormally large files found.")
    else:
        for path, sz_mb in large_files[:20]:
            print(f"  • \033[1;33m{sz_mb:>8.1f} MB\033[0m  {path}")
    print()


def clean_node_modules(directory: str = "."):
    print(f"🧹 Scanning and cleaning orphaned 'node_modules' folders in '{directory}'...")
    cmd = f"find '{directory}' -name 'node_modules' -type d -prune -exec rm -rf '{{}}' +"
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("✅ Cleaned node_modules folders.")
    except Exception as e:
        print(f"Error cleaning node_modules: {e}")
