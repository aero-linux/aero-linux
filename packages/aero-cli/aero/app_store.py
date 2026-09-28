import os
import shutil
import subprocess
from typing import Dict, Any, List


APP_CATALOG: Dict[str, Dict[str, Any]] = {
    "vscode": {
        "name": "Visual Studio Code",
        "category": "Development",
        "description": "Code editing redefined. Industry-standard IDE.",
        "cmd_install": "flatpak install -y flathub com.visualstudio.code || sudo apt-get install -y code",
        "installed_check": "code",
    },
    "brave": {
        "name": "Brave Browser",
        "category": "Web Browsers",
        "description": "Fast, privacy-focused browser with ad-blocker.",
        "cmd_install": "flatpak install -y flathub com.brave.Browser || sudo apt-get install -y brave-browser",
        "installed_check": "brave-browser",
    },
    "docker": {
        "name": "Docker Engine & Compose",
        "category": "Containers & Cloud",
        "description": "Container virtualization runtime for modern dev.",
        "cmd_install": "sudo apt-get install -y docker.io docker-compose && sudo usermod -aG docker $USER",
        "installed_check": "docker",
    },
    "obsidian": {
        "name": "Obsidian Note-Taking",
        "category": "Productivity",
        "description": "Local-first markdown knowledge base and second brain.",
        "cmd_install": "flatpak install -y flathub md.obsidian.Obsidian",
        "installed_check": "obsidian",
    },
    "postman": {
        "name": "Postman API Client",
        "category": "API & Backend",
        "description": "Design, test, and mock REST/GraphQL APIs.",
        "cmd_install": "flatpak install -y flathub com.getpostman.Postman",
        "installed_check": "postman",
    },
    "dbeaver": {
        "name": "DBeaver Community",
        "category": "Databases",
        "description": "Universal database GUI tool for PostgreSQL, MySQL, Redis, SQLite.",
        "cmd_install": "flatpak install -y flathub io.dbeaver.DBeaverCommunity",
        "installed_check": "dbeaver",
    },
    "neovim": {
        "name": "Neovim (v0.10+)",
        "category": "Development",
        "description": "Vim-fork focused on extensibility and usability.",
        "cmd_install": "sudo apt-get install -y neovim",
        "installed_check": "nvim",
    },
    "discord": {
        "name": "Discord",
        "category": "Communication",
        "description": "All-in-one voice and text chat for developers.",
        "cmd_install": "flatpak install -y flathub com.discordapp.Discord",
        "installed_check": "discord",
    },
    "ghostty": {
        "name": "Ghostty / Alacritty Terminal",
        "category": "Terminal & Shell",
        "description": "Ultra-fast GPU-accelerated Wayland terminal emulator.",
        "cmd_install": "sudo apt-get install -y alacritty",
        "installed_check": "alacritty",
    },
}


def list_apps(category: str = ""):
    print("\n📦 \033[1;36mAERO DEVELOPER APP STORE & 1-CLICK CATALOG\033[0m")
    print("═" * 68)
    print(f" {'ID':<12} {'APPLICATION NAME':<26} {'CATEGORY':<18} {'STATUS'}")
    print("─" * 68)

    for app_id, info in APP_CATALOG.items():
        if category and category.lower() not in info["category"].lower():
            continue
        
        installed = shutil.which(info["installed_check"]) is not None
        status_str = "\033[1;32m✔ Installed\033[0m" if installed else "\033[1;30mAvailable\033[0m"
        print(f" {app_id:<12} {info['name']:<26} {info['category']:<18} {status_str}")
    print("═" * 68)
    print("Install any app with: \033[1;33maero store install <id>\033[0m\n")


def install_app(app_id: str) -> bool:
    app_id = app_id.lower().strip()
    if app_id not in APP_CATALOG:
        print(f"❌ Unknown app ID '{app_id}'. Run 'aero store list' to view available software.")
        return False

    info = APP_CATALOG[app_id]
    print(f"\n🚀 Installing \033[1;32m{info['name']}\033[0m ({info['category']})...")
    print(f"Command: {info['cmd_install']}")

    try:
        res = subprocess.run(info["cmd_install"], shell=True)
        if res.returncode == 0:
            print(f"\n\033[1;32m✔ {info['name']} installed successfully!\033[0m\n")
            return True
        else:
            print(f"\n❌ Installation exited with status code {res.returncode}.\n")
            return False
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return False
