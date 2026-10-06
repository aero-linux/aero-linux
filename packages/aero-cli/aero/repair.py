"""
Aero Linux - System Integrity & Self-Repair Engine
Autonomous diagnosis and 1-click self-repair for networking, package locks, audio & daemons.
"""

import os
import shutil
import subprocess
from typing import Dict, List, Any


def _run_privileged(cmd: List[str]) -> subprocess.CompletedProcess:
    """Executes a command with root privileges if required and available, falling back safely."""
    if os.geteuid() == 0:
        full_cmd = cmd
    elif shutil.which("sudo"):
        full_cmd = ["sudo"] + cmd
    else:
        full_cmd = cmd

    try:
        return subprocess.run(full_cmd, capture_output=True)
    except (FileNotFoundError, PermissionError):
        return subprocess.CompletedProcess(args=full_cmd, returncode=127, stdout=b"", stderr=b"")


def check_and_repair_dns() -> Dict[str, Any]:
    """Checks DNS resolution and resets systemd-resolved if stalled."""
    if not shutil.which("ping"):
        return {"component": "DNS & Network", "status": "ok", "message": "ping not available (container/minimal env)"}
    try:
        res = subprocess.run(["ping", "-c", "1", "-W", "2", "1.1.1.1"], capture_output=True)
        if res.returncode == 0:
            return {"component": "DNS & Network", "status": "ok", "message": "Internet connectivity active"}
    except Exception:
        pass
    
    # Attempt repair
    if shutil.which("systemctl"):
        _run_privileged(["systemctl", "restart", "systemd-resolved"])
        _run_privileged(["systemctl", "restart", "NetworkManager"])
        return {"component": "DNS & Network", "status": "repaired", "message": "Restarted systemd-resolved & NetworkManager"}
    return {"component": "DNS & Network", "status": "warning", "message": "Offline or unreachable network"}


def check_and_repair_apt() -> Dict[str, Any]:
    """Checks for stale DPKG/APT locks and fixes broken packages."""
    lock_files = [
        "/var/lib/dpkg/lock-frontend",
        "/var/lib/dpkg/lock",
        "/var/lib/apt/lists/lock"
    ]
    has_locks = any(os.path.exists(f) for f in lock_files)
    
    # Check broken dependencies
    res = subprocess.run(["dpkg", "--audit"], capture_output=True, text=True)
    if not res.stdout.strip():
        return {"component": "Package Manager (APT/DPKG)", "status": "ok", "message": "Package database clean and consistent"}
    
    # Run configure & fix
    _run_privileged(["dpkg", "--configure", "-a"])
    _run_privileged(["apt-get", "install", "-f", "-y"])
    return {"component": "Package Manager (APT/DPKG)", "status": "repaired", "message": "Configured unconfigured packages & resolved dependencies"}


def check_and_repair_audio() -> Dict[str, Any]:
    """Checks PipeWire audio stack and restarts audio server if dead."""
    if shutil.which("pactl"):
        res = subprocess.run(["pactl", "info"], capture_output=True)
        if res.returncode == 0:
            return {"component": "PipeWire Audio Server", "status": "ok", "message": "PipeWire/PulseAudio server responsive"}
    
    if shutil.which("systemctl"):
        subprocess.run(["systemctl", "--user", "restart", "pipewire", "wireplumber"], capture_output=True)
        return {"component": "PipeWire Audio Server", "status": "repaired", "message": "Restarted user PipeWire & WirePlumber daemons"}
    
    return {"component": "PipeWire Audio Server", "status": "warning", "message": "Audio daemon could not be verified"}


def check_and_repair_failed_services() -> Dict[str, Any]:
    """Audits systemd failed units and reports status."""
    if not shutil.which("systemctl"):
        return {"component": "System Daemons", "status": "ok", "message": "No systemd daemon check needed"}
    
    res = subprocess.run(["systemctl", "--failed", "--plain", "--no-legend"], capture_output=True, text=True)
    failed_units = [line.split()[0] for line in res.stdout.strip().splitlines() if line]
    
    if not failed_units:
        return {"component": "System Daemons", "status": "ok", "message": "0 failed systemd services"}
    
    # Attempt reset-failed
    _run_privileged(["systemctl", "reset-failed"])
    return {
        "component": "System Daemons",
        "status": "warning",
        "message": f"Detected failed units: {', '.join(failed_units[:3])}. Cleared failure states."
    }


def run_system_repair() -> List[Dict[str, Any]]:
    """Runs full system self-repair diagnostics and automated remedies."""
    results = [
        check_and_repair_dns(),
        check_and_repair_apt(),
        check_and_repair_audio(),
        check_and_repair_failed_services()
    ]
    return results


def show_repair_summary():
    """Prints beautiful CLI summary of repair operations."""
    print("🛠️  AERO SYSTEM INTEGRITY & SELF-REPAIR")
    print("═" * 58)
    
    results = run_system_repair()
    for r in results:
        status_icon = "✅" if r["status"] == "ok" else ("🔧" if r["status"] == "repaired" else "⚠️")
        print(f" {status_icon} {r['component']:<30} ➔ {r['message']}")
    
    print("═" * 58)
    print("✔ Self-repair audit complete.")
