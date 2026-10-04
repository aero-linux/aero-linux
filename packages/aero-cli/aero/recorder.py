import datetime
import os
import signal
import subprocess
import shutil
import time
from typing import Dict, Any

PID_FILE = "/tmp/aero_recorder.pid"
RECORDINGS_DIR = os.path.expanduser("~/Videos/Recordings")


def ensure_rec_dir():
    os.makedirs(RECORDINGS_DIR, exist_ok=True)


def is_recording_active() -> bool:
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


def start_recording(is_gif: bool = False, region: bool = False) -> Dict[str, Any]:
    ensure_rec_dir()
    if is_recording_active():
        print("⚠️ Screen recording is already in progress. Run: aero rec stop")
        return {"status": "already_recording"}

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ext = "gif" if is_gif else "mp4"
    out_path = os.path.join(RECORDINGS_DIR, f"recording_{timestamp}.{ext}")

    print(f"🎬 \033[1;36mSTARTING WAYLAND SCREEN RECORDING\033[0m")
    print("═" * 50)
    print(f" • Output File: \033[1;33m{out_path}\033[0m")
    print(f" • Mode:        \033[1;32m{'Region Selection' if region else 'Full Screen'}\033[0m")

    cmd = []
    if shutil.which("wf-recorder"):
        cmd = ["wf-recorder", "-f", out_path]
        if region and shutil.which("slurp"):
            try:
                geom = subprocess.check_output("slurp", shell=True, text=True).strip()
                if geom:
                    cmd.extend(["-g", geom])
            except Exception:
                pass
        p = subprocess.Popen(cmd)
        with open(PID_FILE, "w") as f:
            f.write(str(p.pid))
        if shutil.which("notify-send"):
            subprocess.run(["notify-send", "🎥 Recording Started", f"Saving to {out_path} (Press Ctrl+Shift+R or aero rec stop)"], capture_output=True)
        return {"status": "started", "pid": p.pid, "path": out_path}
    else:
        print("ℹ️ wf-recorder is not installed. To record screen, run: sudo apt install wf-recorder")
        return {"status": "missing_wf_recorder", "path": out_path}


def stop_recording() -> Dict[str, Any]:
    print("🛑 \033[1;36mSTOPPING SCREEN RECORDING\033[0m")
    print("═" * 50)
    if not os.path.exists(PID_FILE):
        print(" • No active screen recording process found.")
        return {"status": "not_recording"}

    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGINT)
        time.sleep(0.5)
        os.remove(PID_FILE)
        print("✅ Screen recording stopped and saved to ~/Videos/Recordings/")
        if shutil.which("notify-send"):
            subprocess.run(["notify-send", "🎥 Recording Saved", "Saved to ~/Videos/Recordings/"], capture_output=True)
        return {"status": "stopped", "pid": pid}
    except Exception as e:
        print(f"❌ Error stopping recording: {e}")
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        return {"status": "error", "error": str(e)}
