import os
import subprocess
import shutil

NERD_FONTS = {
    "jetbrains-mono": {
        "url": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.tar.xz",
        "name": "JetBrains Mono Nerd Font",
    },
    "fira-code": {
        "url": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.tar.xz",
        "name": "Fira Code Nerd Font",
    },
    "hack": {
        "url": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Hack.tar.xz",
        "name": "Hack Nerd Font",
    },
}


def list_fonts():
    print("🔤 \033[1;36mAERO DEVELOPER NERD FONTS\033[0m")
    print("═" * 55)
    for key, info in NERD_FONTS.items():
        print(f" • \033[1;33m{key:<18}\033[0m ➔  {info['name']}")
    print("\nRun: 'aero font install <name>' to download and configure.")


def install_font(font_key: str) -> bool:
    if font_key not in NERD_FONTS:
        print(f"❌ Unknown font: {font_key}")
        list_fonts()
        return False

    font = NERD_FONTS[font_key]
    font_dir = os.path.expanduser(f"~/.local/share/fonts/{font_key}")
    os.makedirs(font_dir, exist_ok=True)

    print(f"📥 Downloading and installing \033[1;32m{font['name']}\033[0m...")
    tar_path = f"/tmp/{font_key}.tar.xz"
    
    try:
        subprocess.run(["curl", "-sL", "-o", tar_path, font["url"]], check=True)
        subprocess.run(["tar", "-xf", tar_path, "-C", font_dir], check=True)
        if os.path.exists(tar_path):
            os.remove(tar_path)
        
        # Refresh font cache
        subprocess.run(["fc-cache", "-f", font_dir], capture_output=True)
        print(f"✅ {font['name']} installed and font cache updated.")
        return True
    except Exception as e:
        print(f"❌ Failed to install font: {e}")
        return False
