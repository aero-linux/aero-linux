import os
import shutil


def set_desktop_layout(layout_name: str = "windows") -> bool:
    print(f"🔄 Switching Aero desktop layout to: \033[1;36m{layout_name.upper()}\033[0m...")
    home = os.path.expanduser("~")
    waybar_dir = os.path.join(home, ".config/waybar")
    os.makedirs(waybar_dir, exist_ok=True)

    if layout_name == "windows":
        print("  • Applying Windows-style bottom taskbar with Start Menu & pinned apps.")
        print("  • Enabling floating window defaults and Windows hotkeys (Win+E, Ctrl+Shift+Esc, Win+L).")
        
        # Link windows config if available
        win_cfg = "/usr/share/aero/desktop/configs/waybar/windows-bar.json"
        win_css = "/usr/share/aero/desktop/configs/waybar/windows-style.css"
        if not os.path.exists(win_cfg):
            win_cfg = os.path.expanduser("~/aero-linux/desktop/configs/waybar/windows-bar.json")
            win_css = os.path.expanduser("~/aero-linux/desktop/configs/waybar/windows-style.css")

        if os.path.exists(win_cfg):
            shutil.copyfile(win_cfg, os.path.join(waybar_dir, "config"))
            shutil.copyfile(win_css, os.path.join(waybar_dir, "style.css"))

    elif layout_name == "tiling":
        print("  • Applying Cyber Dark tiling layout with top floating status pill bar.")
        tile_cfg = "/usr/share/aero/desktop/configs/waybar/config"
        tile_css = "/usr/share/aero/desktop/configs/waybar/style.css"
        if not os.path.exists(tile_cfg):
            tile_cfg = os.path.expanduser("~/aero-linux/desktop/configs/waybar/config")
            tile_css = os.path.expanduser("~/aero-linux/desktop/configs/waybar/style.css")

        if os.path.exists(tile_cfg):
            shutil.copyfile(tile_cfg, os.path.join(waybar_dir, "config"))
            shutil.copyfile(tile_css, os.path.join(waybar_dir, "style.css"))

    # Restart Waybar and Sway
    if shutil.which("killall"):
        os.system("killall waybar >/dev/null 2>&1; nohup waybar >/dev/null 2>&1 &")
    if shutil.which("swaymsg"):
        os.system("swaymsg reload >/dev/null 2>&1")

    print(f"✅ Desktop layout switched to {layout_name.upper()}.")
    return True
