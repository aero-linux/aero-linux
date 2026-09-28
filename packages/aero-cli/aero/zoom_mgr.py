import json
import os
import shutil
import subprocess
from typing import Dict, Any

STATE_FILE = os.path.expanduser("~/.config/aero/zoom_state.json")
ZOOM_STEPS = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5]


def _get_current_scale() -> float:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                return float(data.get("scale", 1.0))
        except Exception:
            pass
    return 1.0


def _save_scale(scale: float):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"scale": scale}, f)


def set_zoom(scale: float) -> Dict[str, Any]:
    scale = max(1.0, min(3.0, round(scale, 2)))
    _save_scale(scale)

    # Apply via Sway IPC if available
    if shutil.which("swaymsg"):
        subprocess.run(
            ["swaymsg", f"output * scale {scale}"],
            capture_output=True
        )

    pct = int(scale * 100)
    print(f"🔍 \033[1;36mAERO DESKTOP MAGNIFIER\033[0m: \033[1;32m{pct}%\033[0m (Scale: {scale}x)")

    # Send synchronous desktop OSD overlay
    subprocess.run([
        "notify-send",
        "-t", "1200",
        "-h", "string:x-canonical-private-synchronous:osd_zoom",
        "🔍 Desktop Magnifier",
        f"Zoom Level: {pct}%"
    ], capture_output=True)

    return {"status": "ok", "scale": scale, "percent": pct}


def zoom_in() -> Dict[str, Any]:
    curr = _get_current_scale()
    next_scale = ZOOM_STEPS[-1]
    for s in ZOOM_STEPS:
        if s > curr:
            next_scale = s
            break
    return set_zoom(next_scale)


def zoom_out() -> Dict[str, Any]:
    curr = _get_current_scale()
    prev_scale = ZOOM_STEPS[0]
    for s in reversed(ZOOM_STEPS):
        if s < curr:
            prev_scale = s
            break
    return set_zoom(prev_scale)


def zoom_reset() -> Dict[str, Any]:
    return set_zoom(1.0)


def zoom_peek(scale: float = 1.35, duration: float = 1.8) -> Dict[str, Any]:
    """Momentary peek zoom: magnifies display and auto-resets when gesture ends / timeout."""
    import threading
    import time

    set_zoom(scale)

    def _auto_reset():
        time.sleep(duration)
        zoom_reset()

    thread = threading.Thread(target=_auto_reset, daemon=True)
    thread.start()
    return {"status": "peeking", "scale": scale, "duration": duration}
