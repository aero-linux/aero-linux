import os
import time
import subprocess
from typing import Dict, Any


def get_cpu_stat_snapshot() -> Dict[str, list]:
    cores = {}
    try:
        with open("/proc/stat", "r") as f:
            for line in f:
                parts = line.split()
                if parts and parts[0].startswith("cpu"):
                    cores[parts[0]] = [int(x) for x in parts[1:8]]
    except Exception:
        pass
    return cores


def calculate_cpu_usage(snap1: Dict[str, list], snap2: Dict[str, list]) -> Dict[str, float]:
    usage = {}
    for cpu, v1 in snap1.items():
        if cpu in snap2:
            v2 = snap2[cpu]
            delta = [v2[i] - v1[i] for i in range(len(v1))]
            total = sum(delta)
            idle = delta[3] + delta[4] # idle + iowait
            usage[cpu] = round(100.0 * (1.0 - (idle / total)), 1) if total > 0 else 0.0
    return usage


def profile_cpu_load(duration_sec: float = 1.0) -> Dict[str, Any]:
    print(f"\n⚡ Sampling per-core CPU load and context switches over {duration_sec}s...")
    
    # Read initial context switches
    cs1 = 0
    try:
        with open("/proc/stat", "r") as f:
            for line in f:
                if line.startswith("ctxt"):
                    cs1 = int(line.split()[1])
    except Exception:
        pass

    s1 = get_cpu_stat_snapshot()
    time.sleep(duration_sec)
    s2 = get_cpu_stat_snapshot()

    cs2 = 0
    try:
        with open("/proc/stat", "r") as f:
            for line in f:
                if line.startswith("ctxt"):
                    cs2 = int(line.split()[1])
    except Exception:
        pass

    usages = calculate_cpu_usage(s1, s2)
    ctxt_rate = int((cs2 - cs1) / duration_sec) if duration_sec > 0 else 0

    print("\n📊 AERO LOW-LEVEL CPU PROFILER")
    print("═" * 54)
    total_cpu = usages.get("cpu", 0.0)
    print(f" • Total CPU Utilization: {total_cpu}%")
    print(f" • Context Switch Rate:   {ctxt_rate:,} switches/sec")
    print("─" * 54)
    
    # Print per-core table
    core_keys = sorted([k for k in usages.keys() if k != "cpu"], key=lambda x: int(x[3:]) if x[3:].isdigit() else 0)
    for i in range(0, len(core_keys), 2):
        c1 = core_keys[i]
        c2 = core_keys[i+1] if i+1 < len(core_keys) else None
        bar1 = "█" * int(usages[c1] / 10) + "░" * (10 - int(usages[c1] / 10))
        if c2:
            bar2 = "█" * int(usages[c2] / 10) + "░" * (10 - int(usages[c2] / 10))
            print(f"   {c1:<5} [{bar1}] {usages[c1]:>5.1f}%   |   {c2:<5} [{bar2}] {usages[c2]:>5.1f}%")
        else:
            print(f"   {c1:<5} [{bar1}] {usages[c1]:>5.1f}%")
    print("═" * 54 + "\n")
    return {"total_usage": total_cpu, "context_switches_per_sec": ctxt_rate, "cores": usages}


def audit_io_scheduler():
    print("\n💾 AERO STORAGE I/O SCHEDULER & LATENCY AUDIT")
    print("═" * 54)
    block_devices = os.listdir("/sys/block") if os.path.exists("/sys/block") else []
    for dev in block_devices:
        if dev.startswith("nvme") or dev.startswith("sd"):
            sched_path = f"/sys/block/{dev}/queue/scheduler"
            rot_path = f"/sys/block/{dev}/queue/rotational"
            sched = "unknown"
            is_ssd = True
            if os.path.exists(sched_path):
                with open(sched_path) as f:
                    sched = f.read().strip()
            if os.path.exists(rot_path):
                with open(rot_path) as f:
                    is_ssd = f.read().strip() == "0"
            print(f" • Device /{dev:<8} (Type: {'NVMe/SSD' if is_ssd else 'HDD'})")
            print(f"   - Scheduler: {sched}")
    print("═" * 54 + "\n")
