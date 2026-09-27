import subprocess
import shutil


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
    cron_entry = "0 3 * * * /usr/local/bin/aero pkg clean && /usr/local/bin/aero memory --optimize >/dev/null 2>&1\n"
    try:
        subprocess.run(f'(crontab -l 2>/dev/null; echo "{cron_entry}") | crontab -', shell=True, check=True)
        print("✅ Daily 3:00 AM maintenance cron scheduled successfully.")
        return True
    except Exception as e:
        print(f"❌ Failed to schedule cron: {e}")
        return False
