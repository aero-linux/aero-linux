import json
import os
import shutil
import subprocess
import threading
import time
from typing import Dict, Any

PID_FILE = "/tmp/aero_autotile.pid"


def is_autotile_running() -> bool:
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            return True
        except (ValueError, OSError):
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
            return False
    return False


def switch_split_direction():
    if not shutil.which("swaymsg"):
        return
    try:
        # Query focused window geometry
        tree_raw = subprocess.check_output(["swaymsg", "-t", "get_tree"], text=True)
        tree = json.loads(tree_raw)

        def find_focused(node):
            if node.get("focused"):
                return node
            for child in node.get("nodes", []) + node.get("floating_nodes", []):
                res = find_focused(child)
                if res:
                    return res
            return None

        focused = find_focused(tree)
        if focused and "rect" in focused:
            rect = focused["rect"]
            w = rect.get("width", 0)
            h = rect.get("height", 0)
            if w >= h and w > 0:
                subprocess.run(["swaymsg", "split", "horizontal"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif h > w:
                subprocess.run(["swaymsg", "split", "vertical"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def run_autotile_loop():
    if not shutil.which("swaymsg"):
        return
    try:
        proc = subprocess.Popen(
            ["swaymsg", "-t", "subscribe", "-m", '["window"]'],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if proc.stdout:
            for line in proc.stdout:
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                    change = event.get("change")
                    if change in ("focus", "new", "init"):
                        switch_split_direction()
                except Exception:
                    pass
    except Exception:
        pass


def start_autotiling() -> Dict[str, Any]:
    print("⚡ \033[1;36mAERO AUTO-TILING ENGINE (DYNAMIC BSP/SPIRAL)\033[0m")
    print("═" * 55)
    if is_autotile_running():
        print(" • Auto-tiling daemon is already active.")
        return {"status": "already_active"}

    if not shutil.which("swaymsg"):
        print("ℹ️ Sway compositor is not running in this session.")
        return {"status": "compositor_not_running"}

    p = subprocess.Popen(["python3", "-c", "import aero.autotile; aero.autotile.run_autotile_loop()"])
    with open(PID_FILE, "w") as f:
        f.write(str(p.pid))
    print("✅ Auto-tiling daemon started (Golden Ratio alternating horizontal/vertical splits).\n")
    return {"status": "started", "pid": p.pid}


def stop_autotiling() -> Dict[str, Any]:
    print("🛑 Stopping Aero auto-tiling daemon...")
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 15)
            os.remove(PID_FILE)
            print("✅ Auto-tiling stopped.")
            return {"status": "stopped"}
        except Exception:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
    print(" • Auto-tiling is not running.")
    return {"status": "not_running"}
