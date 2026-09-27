import os
import shutil

THEMES = {
    "cyber-cyan": {
        "accent": "#00f2fe",
        "bg": "#0a0b0e",
        "card": "#141824",
        "text": "#f8fafc",
        "name": "Cyber Cyan (Default Aero)",
    },
    "tokyo-night": {
        "accent": "#7aa2f7",
        "bg": "#1a1b26",
        "card": "#24283b",
        "text": "#c0caf5",
        "name": "Tokyo Night",
    },
    "nord": {
        "accent": "#88c0d0",
        "bg": "#2e3440",
        "card": "#3b4252",
        "text": "#eceff4",
        "name": "Nord Arctic",
    },
    "gruvbox": {
        "accent": "#fe8019",
        "bg": "#282828",
        "card": "#3c3836",
        "text": "#ebdbb2",
        "name": "Gruvbox Dark",
    },
}


def list_themes():
    print("🎨 \033[1;36mAERO DESKTOP THEMES & PALETTES\033[0m")
    print("═" * 55)
    for key, info in THEMES.items():
        print(f" • \033[1;33m{key:<15}\033[0m ➔  {info['name']} (Accent: {info['accent']})")
    print("\nRun: 'aero theme set <name>' to switch desktop styling.")


def set_theme(theme_name: str) -> bool:
    if theme_name not in THEMES:
        print(f"❌ Unknown theme: {theme_name}")
        list_themes()
        return False

    theme = THEMES[theme_name]
    print(f"🎨 Applying theme: \033[1;32m{theme['name']}\033[0m...")

    # Write theme state to ~/.config/aero/theme.conf
    config_dir = os.path.expanduser("~/.config/aero")
    os.makedirs(config_dir, exist_ok=True)
    theme_file = os.path.join(config_dir, "theme.conf")

    with open(theme_file, "w") as f:
        f.write(f"THEME={theme_name}\nACCENT={theme['accent']}\nBG={theme['bg']}\n")

    # Reload Sway / Waybar if active
    if shutil.which("swaymsg"):
        os.system("swaymsg reload >/dev/null 2>&1")
    if shutil.which("killall"):
        os.system("killall -SIGUSR2 waybar >/dev/null 2>&1")

    print(f"✅ Desktop theme switched to {theme['name']}.")
    return True
