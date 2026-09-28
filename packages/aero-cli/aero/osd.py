import os
import subprocess
import shutil
from typing import Dict, Any


def get_current_volume() -> int:
    try:
        out = subprocess.check_output("pactl get-sink-volume @DEFAULT_SINK@", shell=True, text=True)
        # Parse percentage (e.g. 65%)
        for part in out.split("/"):
            part = part.strip()
            if part.endswith("%"):
                return int(part.replace("%", ""))
    except Exception:
        pass
    return 50


def get_current_brightness() -> int:
    try:
        max_b = int(subprocess.check_output("brightnessctl max", shell=True, text=True).strip())
        cur_b = int(subprocess.check_output("brightnessctl get", shell=True, text=True).strip())
        if max_b > 0:
            return int((cur_b / max_b) * 100)
    except Exception:
        pass
    return 75


def dispatch_osd(category: str, title: str, message: str, value: int = -1):
    cmd = [
        "notify-send",
        "-h", f"string:x-canonical-private-synchronous:osd_{category}",
        "-t", "1200",
    ]
    if value >= 0:
        cmd.extend(["-h", f"int:value:{value}"])
    cmd.extend([title, message])
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1.0)
    except Exception:
        pass


def handle_osd_action(action: str) -> Dict[str, Any]:
    res = {"action": action, "value": 0}
    if action == "volume-up":
        subprocess.run("pactl set-sink-volume @DEFAULT_SINK@ +5% 2>/dev/null || wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+ 2>/dev/null", shell=True)
        vol = get_current_volume()
        dispatch_osd("volume", "Volume", f"🔊 {vol}%", vol)
        res["value"] = vol
    elif action == "volume-down":
        subprocess.run("pactl set-sink-volume @DEFAULT_SINK@ -5% 2>/dev/null || wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%- 2>/dev/null", shell=True)
        vol = get_current_volume()
        dispatch_osd("volume", "Volume", f"🔉 {vol}%", vol)
        res["value"] = vol
    elif action == "mute":
        subprocess.run("pactl set-sink-mute @DEFAULT_SINK@ toggle 2>/dev/null || wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle 2>/dev/null", shell=True)
        dispatch_osd("volume", "Audio", "🔇 Muted / Toggled")
    elif action == "mic-mute":
        subprocess.run("pactl set-source-mute @DEFAULT_SOURCE@ toggle 2>/dev/null || wpctl set-mute @DEFAULT_AUDIO_SOURCE@ toggle 2>/dev/null", shell=True)
        dispatch_osd("mic", "Microphone", "🎤 Mic Mute Toggled")
    elif action == "brightness-up":
        subprocess.run("brightnessctl set +5% 2>/dev/null", shell=True)
        bright = get_current_brightness()
        dispatch_osd("brightness", "Brightness", f"☀️ {bright}%", bright)
        res["value"] = bright
    elif action == "brightness-down":
        subprocess.run("brightnessctl set 5%- 2>/dev/null", shell=True)
        bright = get_current_brightness()
        dispatch_osd("brightness", "Brightness", f"🔅 {bright}%", bright)
        res["value"] = bright
    elif action in ("play-pause", "next", "prev"):
        if shutil.which("playerctl"):
            cmd_map = {"play-pause": "play-pause", "next": "next", "prev": "previous"}
            subprocess.run(f"playerctl {cmd_map[action]} 2>/dev/null", shell=True)
            try:
                track = subprocess.check_output("playerctl metadata --format '{{title}} - {{artist}}' 2>/dev/null", shell=True, text=True).strip()
                if track:
                    dispatch_osd("media", "Media Player", f"🎵 {track}")
            except Exception:
                pass
    return res
