import os
import time
import shutil


def get_cpu_frequencies():
    freqs = []
    cpu_dir = "/sys/devices/system/cpu"
    if os.path.exists(cpu_dir):
        for entry in sorted(os.listdir(cpu_dir)):
            if entry.startswith("cpu") and entry[3:].isdigit():
                cur_freq_path = os.path.join(cpu_dir, entry, "cpufreq", "scaling_cur_freq")
                if os.path.exists(cur_freq_path):
                    try:
                        with open(cur_freq_path, "r") as f:
                            freqs.append(int(f.read().strip()) // 1000)
                    except Exception:
                        pass
    return freqs


def render_bar(percentage: float, width: int = 20, fill_char: str = "█", empty_char: str = "░") -> str:
    filled = int(width * (percentage / 100.0))
    return fill_char * filled + empty_char * (width - filled)


def run_live_monitor(interval: float = 1.0):
    print("\033[?25l", end="")  # Hide cursor
    try:
        while True:
            # Clear terminal screen
            print("\033[H\033[J", end="")
            
            # Read memory
            mem_total = 0
            mem_avail = 0
            if os.path.exists("/proc/meminfo"):
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            mem_total = int(line.split()[1]) // 1024
                        elif line.startswith("MemAvailable:"):
                            mem_avail = int(line.split()[1]) // 1024
            mem_used = max(0, mem_total - mem_avail)
            mem_pct = (mem_used / mem_total * 100) if mem_total else 0

            # Read CPU freqs
            freqs = get_cpu_frequencies()
            avg_freq = sum(freqs) // len(freqs) if freqs else 0

            # Read Battery
            bat_pct = 0
            bat_status = "N/A"
            if os.path.exists("/sys/class/power_supply/BAT0/capacity"):
                with open("/sys/class/power_supply/BAT0/capacity") as f:
                    bat_pct = int(f.read().strip())
                if os.path.exists("/sys/class/power_supply/BAT0/status"):
                    with open("/sys/class/power_supply/BAT0/status") as f:
                        bat_status = f.read().strip()

            # Render Dashboard
            print("⚡ \033[1;36mAERO SYSTEM MONITOR\033[0m — Live Metrics [Press Ctrl+C to Exit]")
            print("═" * 60)
            
            # CPU
            print(f"⚙️  \033[1mCPU Clocks:\033[0m  {len(freqs)} Logical Cores | Avg: \033[33m{avg_freq} MHz\033[0m")
            if freqs:
                core_str = " ".join([f"{f}M" for f in freqs[:8]])
                print(f"   Cores 0-7: {core_str}")

            # RAM
            print(f"\n🧠 \033[1mMemory:\033[0m      {mem_used}MB / {mem_total}MB [{render_bar(mem_pct)}] \033[32m{mem_pct:.1f}%\033[0m")
            
            # Battery
            if bat_status != "N/A":
                print(f"\n🔋 \033[1mBattery:\033[0m     {bat_pct}% ({bat_status}) [{render_bar(bat_pct, fill_char='■', empty_char='□')}]")

            print("\n" + "═" * 60)
            print("\033[90mPowered by Aero Linux Kernel Engine\033[0m")
            
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\033[?25h\n\nMonitor closed.")
    finally:
        print("\033[?25h", end="")
