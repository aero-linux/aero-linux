import shutil
import subprocess


def show_logs(log_type: str = "error"):
    if not shutil.which("journalctl"):
        print("❌ journalctl not available on this system.")
        return

    print(f"📋 \033[1;36mAERO SYSTEM LOGS\033[0m — Mode: \033[1;33m{log_type.upper()}\033[0m")
    print("═" * 60)

    if log_type == "error":
        cmd = ["journalctl", "-p", "3", "-xb", "--no-pager", "-n", "30"]
        print("Showing last 30 high-priority system errors (p=3) since current boot:\n")
    elif log_type == "kernel":
        cmd = ["dmesg", "-T", "-l", "err,warn"]
        print("Showing kernel error and warning messages:\n")
    elif log_type == "boot":
        cmd = ["systemd-analyze", "blame"]
        print("Showing system boot time breakdown (slowest services first):\n")
    else:
        cmd = ["journalctl", "-xe", "--no-pager", "-n", "30"]

    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"Failed to read logs: {e}")
    print()
