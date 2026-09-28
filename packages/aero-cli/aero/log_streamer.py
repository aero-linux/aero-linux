import os
import shutil
import subprocess
from typing import List, Dict, Any


def get_oom_events() -> List[str]:
    oom_lines = []
    if shutil.which("dmesg"):
        try:
            res = subprocess.run("sudo dmesg | grep -i 'killed process' || true", shell=True, capture_output=True, text=True)
            if res.stdout:
                oom_lines = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
        except Exception:
            pass
    return oom_lines


def audit_system_errors():
    print("\n📜 \033[1;36mAERO CRITICAL SYSTEM & KERNEL LOG AUDIT\033[0m")
    print("═" * 60)

    # 1. Check for OOM Killer events
    ooms = get_oom_events()
    if ooms:
        print(f"⚠️  \033[1;31mOut-Of-Memory (OOM) Events Detected ({len(ooms)}):\033[0m")
        for o in ooms[-5:]:
            print(f"   - {o}")
    else:
        print(" • OOM Killer Status:  \033[1;32m✔ Clean (Zero OOM kills)\033[0m")

    # 2. Check systemd failed services
    if shutil.which("systemctl"):
        try:
            res = subprocess.run("systemctl --failed --no-legend", shell=True, capture_output=True, text=True)
            failed = [l.strip() for l in res.stdout.strip().split("\n") if l.strip()]
            if failed:
                print(f" • Failed Services:   \033[1;31m{len(failed)} degraded\033[0m")
                for f in failed:
                    print(f"   - {f}")
            else:
                print(" • Systemd Services:   \033[1;32m✔ All units healthy\033[0m")
        except Exception:
            pass

    print("═" * 60 + "\n")
