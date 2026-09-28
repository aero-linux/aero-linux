import os
import subprocess


def compact_memory() -> dict:
    result = {"zram_compacted": False, "caches_dropped": False, "memory_freed_mb": 0}

    before_mem = 0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    before_mem = int(line.split()[1]) // 1024
    except Exception:
        pass

    # zRAM compaction
    compact_file = "/sys/block/zram0/compact"
    if os.path.exists(compact_file):
        try:
            with open(compact_file, "w") as f:
                f.write("1")
            result["zram_compacted"] = True
        except PermissionError:
            subprocess.run(["sudo", "tee", compact_file], input="1", text=True, capture_output=True)
            result["zram_compacted"] = True
        except Exception:
            pass

    # Drop dentries and pagecache safely
    try:
        subprocess.run(["sudo", "sync"], capture_output=True)
        drop_caches = "/proc/sys/vm/drop_caches"
        subprocess.run(["sudo", "tee", drop_caches], input="3", text=True, capture_output=True)
        result["caches_dropped"] = True
    except Exception:
        pass

    after_mem = 0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    after_mem = int(line.split()[1]) // 1024
    except Exception:
        pass

    result["memory_freed_mb"] = max(0, after_mem - before_mem)
    return result


def get_memory_stats() -> dict:
    total_mb, avail_mb, free_mb = 0, 0, 0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split()
                if line.startswith("MemTotal:"):
                    total_mb = int(parts[1]) // 1024
                elif line.startswith("MemAvailable:"):
                    avail_mb = int(parts[1]) // 1024
                elif line.startswith("MemFree:"):
                    free_mb = int(parts[1]) // 1024
    except Exception:
        pass

    used_mb = max(0, total_mb - avail_mb)
    pct = round((used_mb / total_mb * 100), 1) if total_mb > 0 else 0

    zram_total, zram_used = 0, 0
    if os.path.exists("/sys/block/zram0/disksize"):
        try:
            with open("/sys/block/zram0/disksize") as f:
                zram_total = int(f.read().strip()) // (1024 * 1024)
            with open("/sys/block/zram0/mem_used_total") as f:
                zram_used = int(f.read().strip()) // (1024 * 1024)
        except Exception:
            pass

    zram_pct = round((zram_used / zram_total * 100), 1) if zram_total > 0 else 0

    return {
        "total_mb": total_mb,
        "available_mb": avail_mb,
        "used_mb": used_mb,
        "percent_used": pct,
        "zram_total_mb": zram_total,
        "zram_used_mb": zram_used,
        "zram_percent": zram_pct,
    }


def get_top_memory_processes(limit: int = 10) -> list:
    processes = []
    try:
        res = subprocess.run(
            ["ps", "-eo", "pid,user,%mem,rss,comm", "--sort=-rss"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if res.returncode == 0:
            lines = res.stdout.strip().split("\n")[1 : limit + 1]
            for line in lines:
                parts = line.split(None, 4)
                if len(parts) >= 5:
                    rss_mb = int(parts[3]) // 1024
                    processes.append({
                        "pid": int(parts[0]),
                        "user": parts[1],
                        "mem_percent": float(parts[2]),
                        "rss_mb": rss_mb,
                        "command": parts[4],
                    })
    except Exception:
        pass
    return processes
