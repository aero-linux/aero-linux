"""
Aero Linux - Cron & Scheduled Task Automation Engine
Structured crontab management, human-readable schedule parsing, and automated maintenance.
"""

import subprocess
import shutil
from typing import List, Dict, Any


def humanize_cron(schedule: str) -> str:
    schedule = schedule.strip()
    presets = {
        "* * * * *": "Every minute",
        "*/5 * * * *": "Every 5 minutes",
        "*/15 * * * *": "Every 15 minutes",
        "0 * * * *": "Every hour (at minute 0)",
        "0 0 * * *": "Daily at midnight (00:00)",
        "0 3 * * *": "Daily at 3:00 AM",
        "0 12 * * *": "Daily at noon (12:00)",
        "0 0 * * 0": "Weekly on Sunday (00:00)",
        "0 0 1 * *": "Monthly on 1st day (00:00)",
        "@reboot": "At system startup (@reboot)",
    }
    if schedule in presets:
        return presets[schedule]
    
    parts = schedule.split()
    if len(parts) == 5:
        m, h, dom, mon, dow = parts
        if m.startswith("*/"):
            return f"Every {m[2:]} minutes"
        if h.startswith("*/"):
            return f"Every {h[2:]} hours"
        if dom == "*" and mon == "*" and dow == "*":
            return f"Daily at {h}:{m.zfill(2)}"
    return f"Custom schedule: {schedule}"


def get_cron_jobs() -> List[Dict[str, Any]]:
    jobs = []
    try:
        res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
        if res.returncode != 0:
            return []

        for line in res.stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            
            is_disabled = line.startswith("#DISABLED#")
            active_line = line[10:].strip() if is_disabled else line
            
            if active_line.startswith("#") and not is_disabled:
                continue

            parts = active_line.split(None, 5)
            if len(parts) >= 6:
                schedule = " ".join(parts[:5])
                cmd = parts[5]
                jobs.append({
                    "schedule": schedule,
                    "human": humanize_cron(schedule),
                    "command": cmd,
                    "enabled": not is_disabled,
                    "raw": line,
                })
            elif len(parts) >= 2 and parts[0].startswith("@"):
                schedule = parts[0]
                cmd = " ".join(parts[1:])
                jobs.append({
                    "schedule": schedule,
                    "human": humanize_cron(schedule),
                    "command": cmd,
                    "enabled": not is_disabled,
                    "raw": line,
                })
    except Exception:
        pass
    return jobs


def save_cron_jobs(jobs: List[Dict[str, Any]]) -> bool:
    lines = []
    for j in jobs:
        schedule = j.get("schedule", "* * * * *")
        cmd = j.get("command", "")
        if not j.get("enabled", True):
            lines.append(f"#DISABLED#{schedule} {cmd}")
        else:
            lines.append(f"{schedule} {cmd}")
    
    new_crontab = "\n".join(lines) + "\n"
    try:
        proc = subprocess.run(["crontab", "-"], input=new_crontab, text=True, capture_output=True)
        return proc.returncode == 0
    except Exception:
        return False


def add_cron_job(schedule: str, command: str) -> bool:
    jobs = get_cron_jobs()
    jobs.append({
        "schedule": schedule.strip(),
        "command": command.strip(),
        "enabled": True,
    })
    return save_cron_jobs(jobs)


def delete_cron_job(index: int) -> bool:
    jobs = get_cron_jobs()
    if 0 <= index < len(jobs):
        jobs.pop(index)
        return save_cron_jobs(jobs)
    return False


def toggle_cron_job(index: int) -> bool:
    jobs = get_cron_jobs()
    if 0 <= index < len(jobs):
        jobs[index]["enabled"] = not jobs[index]["enabled"]
        return save_cron_jobs(jobs)
    return False


def show_cron_status():
    print("⏰ \033[1;36mAERO SYSTEMD TIMERS & MAINTENANCE JOBS\033[0m")
    print("═" * 60)

    if shutil.which("systemctl"):
        try:
            res = subprocess.run(["systemctl", "list-timers", "--no-pager"], capture_output=True, text=True)
            lines = res.stdout.strip().split("\n")
            for line in lines[:10]:
                print(f"  {line}")
        except Exception as e:
            print(f"Failed to query systemd timers: {e}")
    print()


def enable_auto_maintenance():
    print("⚡ Enabling automated Aero maintenance jobs (Daily cache prune + zRAM compaction)...")
    cron_entry = "0 3 * * * /usr/local/bin/aero clean && /usr/local/bin/aero memory >/dev/null 2>&1\n"
    try:
        subprocess.run(f'(crontab -l 2>/dev/null; echo "{cron_entry}") | crontab -', shell=True, check=True)
        print("✅ Daily 3:00 AM maintenance cron scheduled successfully.")
        return True
    except Exception as e:
        print(f"❌ Failed to schedule cron: {e}")
        return False
