import datetime
import os
from aero.wallpaper import set_desktop_wallpaper
from aero.power import get_current_profile


def auto_apply_dynamic_theme() -> str:
    now = datetime.datetime.now().time()
    profile = get_current_profile()

    # If running on power-saver battery profile
    if profile == "powersave" or profile == "battery":
        theme = "gruvbox"
        reason = "Battery Saver active"
    elif datetime.time(7, 0) <= now <= datetime.time(18, 30):
        theme = "nord"
        reason = "Daytime Lighting (7:00 AM - 6:30 PM)"
    else:
        theme = "cyber-cyan"
        reason = "Night / OLED Dark Mode"

    print(f"\n🎨 \033[1;36mAERO DYNAMIC THEME SCHEDULER\033[0m")
    print("═" * 56)
    print(f" • Trigger:       {reason}")
    print(f" • Applying:      \033[1;32m{theme}\033[0m palette")
    
    set_desktop_wallpaper(theme)
    print("═" * 56 + "\n")
    return theme
