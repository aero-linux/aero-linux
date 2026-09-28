import os
import subprocess


PALETTES = {
    "cyber-cyan": {
        "bg": "#08090d",
        "primary": "#00f2fe",
        "secondary": "#4facfe",
        "grid": "rgba(0, 242, 254, 0.05)",
    },
    "tokyo-night": {
        "bg": "#1a1b26",
        "primary": "#7aa2f7",
        "secondary": "#bb9af7",
        "grid": "rgba(122, 162, 247, 0.06)",
    },
    "nord": {
        "bg": "#2e3440",
        "primary": "#88c0d0",
        "secondary": "#81a1c1",
        "grid": "rgba(136, 192, 208, 0.05)",
    },
    "gruvbox": {
        "bg": "#282828",
        "primary": "#fabd2f",
        "secondary": "#fe8019",
        "grid": "rgba(250, 189, 47, 0.05)",
    },
}


def generate_wallpaper_svg(palette_name: str = "cyber-cyan", output_path: str = "") -> str:
    p = PALETTES.get(palette_name.lower(), PALETTES["cyber-cyan"])
    if not output_path:
        cfg_dir = os.path.expanduser("~/.config/aero")
        os.makedirs(cfg_dir, exist_ok=True)
        output_path = os.path.join(cfg_dir, "wallpaper.svg")

    svg_content = f"""<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p['primary']}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{p['bg']}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['primary']}" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="{p['secondary']}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
      <path d="M 60 0 L 0 0 0 60" fill="none" stroke="{p['grid']}" stroke-width="1"/>
    </pattern>
  </defs>

  <!-- Background Base -->
  <rect width="1920" height="1080" fill="{p['bg']}"/>
  
  <!-- Subtle Grid -->
  <rect width="1920" height="1080" fill="url(#grid)"/>
  
  <!-- Center Ambient Glow -->
  <circle cx="960" cy="540" r="600" fill="url(#glow)"/>

  <!-- Minimalist Cyber Geometry -->
  <path d="M 200 1080 L 700 400 L 1220 400 L 1720 1080" fill="none" stroke="url(#lineGrad)" stroke-width="2"/>
  <path d="M 400 1080 L 800 520 L 1120 520 L 1520 1080" fill="none" stroke="url(#lineGrad)" stroke-width="1" stroke-dasharray="8 6"/>

  <!-- Subtle Emblem -->
  <text x="960" y="530" font-family="'JetBrains Mono', monospace" font-size="44" font-weight="900" fill="{p['primary']}" fill-opacity="0.25" text-anchor="middle" letter-spacing="8">⚡ AERO LINUX</text>
  <text x="960" y="570" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="600" fill="{p['secondary']}" fill-opacity="0.2" text-anchor="middle" letter-spacing="4">HIGH-PERFORMANCE AI &amp; DEVELOPER OS</text>
</svg>"""

    with open(output_path, "w") as f:
        f.write(svg_content)

    print(f"🎨 Generated '{palette_name}' cyber wallpaper ➔ {output_path}")
    return output_path


def set_desktop_wallpaper(palette_name: str = "cyber-cyan"):
    path = generate_wallpaper_svg(palette_name)
    # If swaybg is available, set wallpaper dynamically
    try:
        subprocess.run(["swaymsg", "output", "*", "bg", path, "fill"], capture_output=True)
        print("✅ Live Wayland wallpaper updated.")
    except Exception:
        pass
