import os
import shutil
import subprocess
from typing import Dict, Any

ACCENT_PRESETS = {
    "cyan": {"hex": "#00f2fe", "name": "Cyber Cyan", "glow": "rgba(0, 242, 254, 0.4)"},
    "purple": {"hex": "#a855f7", "name": "Electric Purple", "glow": "rgba(168, 85, 247, 0.4)"},
    "emerald": {"hex": "#10b981", "name": "Matrix Emerald", "glow": "rgba(16, 185, 129, 0.4)"},
    "rose": {"hex": "#f43f5e", "name": "Neon Rose", "glow": "rgba(244, 63, 94, 0.4)"},
    "amber": {"hex": "#f59e0b", "name": "Solar Amber", "glow": "rgba(245, 158, 11, 0.4)"},
    "arctic": {"hex": "#88c0d0", "name": "Nord Arctic", "glow": "rgba(136, 192, 208, 0.4)"},
}


def list_accents():
    print("🎨 \033[1;36mAERO DESKTOP ACCENT COLOR STUDIO\033[0m")
    print("═" * 55)
    for key, info in ACCENT_PRESETS.items():
        print(f" • \033[1;33m{key:<8}\033[0m ➔ {info['name']:<18} ({info['hex']})")
    print("\nUsage: aero theme accent <color_name_or_hex>\n")


def apply_accent_color(accent_name: str) -> Dict[str, Any]:
    accent_name = accent_name.lower().lstrip("#")
    info = ACCENT_PRESETS.get(accent_name)
    hex_code = info["hex"] if info else f"#{accent_name}"
    name = info["name"] if info else hex_code

    print(f"🎨 Applying Aero Accent Color: \033[1;36m{name}\033[0m ({hex_code})...")

    # Update Sway focused border
    if shutil.which("swaymsg"):
        subprocess.run(
            ["swaymsg", f"client.focused {hex_code} #0a0b0e #f8fafc {hex_code} {hex_code}"],
            capture_output=True
        )

    # Trigger desktop notification
    subprocess.run(["notify-send", "🎨 Accent Color Applied", f"Desktop theme updated to {name}"])
    print(f"✅ Desktop accent color applied successfully.\n")
    return {"status": "applied", "accent": hex_code, "name": name}
