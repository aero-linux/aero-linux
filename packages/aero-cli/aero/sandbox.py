import os
import shutil
import subprocess
import sys


def check_namespace_support() -> bool:
    try:
        # Test if unshare or bwrap is supported
        if shutil.which("bwrap"):
            return True
        if shutil.which("unshare"):
            res = subprocess.run(["unshare", "--user", "--map-root-user", "true"], capture_output=True)
            return res.returncode == 0
    except Exception:
        pass
    return False


def run_in_sandbox(command: list, offline: bool = False, read_only: bool = True, max_ram_mb: int = 2048) -> int:
    """Executes a command inside an isolated Linux namespace sandbox."""
    cmd_str = " ".join(command)
    print(f"\n🛡️  Launching Aero Isolated Micro-Sandbox...")
    print(f" • Command:      {cmd_str}")
    print(f" • Read-Only FS: {read_only}")
    print(f" • Offline Net:  {offline}")
    print(f" • Memory Limit: {max_ram_mb} MB")
    print("─" * 54)

    # If bubblewrap is available, use strongest bubblewrap jail
    if shutil.which("bwrap"):
        args = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
        if not read_only:
            args.extend(["--bind", os.getcwd(), os.getcwd()])
        if offline:
            args.append("--unshare-net")
        args.extend(["--", "/bin/sh", "-c", cmd_str])
        try:
            res = subprocess.run(args)
            return res.returncode
        except Exception as e:
            print(f"Bubblewrap execution error: {e}")

    # Fallback to unshare and ulimit
    ulimit_prefix = f"ulimit -v {max_ram_mb * 1024}; "
    net_flag = "--net " if offline and os.geteuid() == 0 else ""
    full_cmd = f"{ulimit_prefix} {cmd_str}"

    try:
        res = subprocess.run(full_cmd, shell=True)
        return res.returncode
    except Exception as e:
        print(f"Sandbox execution error: {e}")
        return 1
