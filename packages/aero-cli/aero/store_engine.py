import os
import shutil
import subprocess
from typing import Dict, Any, List
from aero.app_store import APP_CATALOG
from aero.appimage_mgr import list_appimages


def search_universal_store(query: str) -> List[Dict[str, Any]]:
    query = query.lower().strip()
    results = []

    # 1. Search Curated Developer Catalog
    for app_id, info in APP_CATALOG.items():
        if query in app_id or query in info["name"].lower() or query in info["description"].lower() or query in info["category"].lower():
            is_installed = bool(shutil.which(info["installed_check"]))
            results.append({
                "id": app_id,
                "name": info["name"],
                "source": "Aero Curated",
                "category": info["category"],
                "description": info["description"],
                "installed": is_installed,
                "type": "native"
            })

    # 2. Search Installed AppImages
    appimgs = list_appimages()
    for app in appimgs:
        if query in app["name"].lower():
            results.append({
                "id": app["name"],
                "name": app["name"],
                "source": "AppImage (Local)",
                "category": "AppImage",
                "description": f"Installed portable AppImage ({app['file']})",
                "installed": True,
                "type": "appimage"
            })

    # 3. Search Flathub if flatpak is installed
    if shutil.which("flatpak") and len(query) >= 3:
        try:
            res = subprocess.run(["flatpak", "search", query], capture_output=True, text=True, timeout=4)
            for line in res.stdout.splitlines()[:5]:
                parts = line.split("\t")
                if len(parts) >= 3:
                    results.append({
                        "id": parts[1].strip(),
                        "name": parts[0].strip(),
                        "source": "Flathub (Sandbox)",
                        "category": "Flatpak",
                        "description": parts[2].strip(),
                        "installed": False,
                        "type": "flatpak"
                    })
        except Exception:
            pass

    return results


def print_store_search_results(query: str):
    print(f"🛍️  \033[1;36mAERO UNIVERSAL SOFTWARE SEARCH: '{query}'\033[0m")
    print("═" * 70)
    results = search_universal_store(query)
    if not results:
        print(f" • No packages found matching '{query}'.")
        print("═" * 70)
        return

    for item in results:
        status = " \033[1;32m[Installed]\033[0m" if item["installed"] else ""
        source_badge = f"\033[1;33m[{item['source']}]\033[0m"
        print(f" • \033[1;37m{item['name']:<28}\033[0m {source_badge:<25} {status}")
        print(f"   \033[0;90m{item['description'][:65]}...\033[0m\n")
    print("═" * 70)
    print(f"Total results: {len(results)}\n")
