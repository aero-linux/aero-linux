import os
import shutil
from typing import List, Dict, Any

TRASH_FILES = os.path.expanduser("~/.local/share/Trash/files")
TRASH_INFO = os.path.expanduser("~/.local/share/Trash/info")


def get_trash_items() -> List[Dict[str, Any]]:
    items = []
    if not os.path.exists(TRASH_FILES):
        return items
    for entry in os.scandir(TRASH_FILES):
        size = 0
        if entry.is_file():
            size = entry.stat().st_size
        items.append({
            "name": entry.name,
            "path": entry.path,
            "size_kb": round(size / 1024, 2)
        })
    return items


def list_trash_contents():
    print("🗑️  \033[1;36mAERO RECYCLE BIN / TRASH\033[0m")
    print("═" * 55)
    items = get_trash_items()
    if not items:
        print(" • Trash is currently empty.")
        return
    print(f" • Total Items in Trash: \033[1;33m{len(items)}\033[0m\n")
    for it in items[:15]:
        print(f" 🗑️  {it['name']:<35} ({it['size_kb']} KB)")
    if len(items) > 15:
        print(f" ... and {len(items) - 15} more items.")
    print()


def empty_trash_bin() -> bool:
    print("🗑️  Emptying Recycle Bin / Trash...")
    if os.path.exists(TRASH_FILES):
        shutil.rmtree(TRASH_FILES, ignore_errors=True)
        os.makedirs(TRASH_FILES, exist_ok=True)
    if os.path.exists(TRASH_INFO):
        shutil.rmtree(TRASH_INFO, ignore_errors=True)
        os.makedirs(TRASH_INFO, exist_ok=True)
    print("✅ Trash emptied successfully.")
    return True
