"""
Aero Linux - Interactive Developer CLI REPL & Shell
Real-time command execution prompt with inline hardware status, autocompletions and diagnostics.
"""

import os
import subprocess
import sys
import time
from aero.doctor import run_doctor
from aero.memory import get_memory_stats
from aero.power import get_current_profile


def run_aero_shell():
    print("\033[38;2;0;242;254m")
    print("  ___    ______ ____  ____     _____ __  __________    __ ")
    print(" /   |  / ____// __ \\/ __ \\   / ___// / / / ____/ /   / / ")
    print("/ /| | / __/  / /_/ / / / /   \\__ \\/ /_/ / __/ / /   / /  ")
    print("/ ___ |/ /___ / _, _/ /_/ /   ___/ / __  / /___/ /___/ /___")
    print("/_/  |_/_____//_/ |_|\\____/   /____/_/ /_/_____/_____/_____/")
    print("\033[0m")
    print("\033[1;37m⚡ Aero Linux Interactive Developer Shell v1.3.0-Nebula\033[0m")
    print("\033[90mType 'help' for available commands, 'doctor' for diagnostics, or 'exit' to quit.\033[0m\n")

    while True:
        try:
            profile = get_current_profile()
            prompt = f"\033[38;2;0;242;254m⚡ aero\033[0m \033[90m[{profile}]\033[0m \033[32m❯\033[0m "
            cmd_line = input(prompt).strip()
            
            if not cmd_line:
                continue

            parts = cmd_line.split()
            cmd = parts[0].lower()

            start_t = time.perf_counter()

            if cmd in ["exit", "quit", "q"]:
                print("\033[38;2;0;242;254m👋 Exiting Aero Shell. Happy hacking!\033[0m")
                break
            elif cmd in ["clear", "cls"]:
                os.system("clear" if os.name == "posix" else "cls")
            elif cmd in ["help", "?"]:
                _print_help()
            elif cmd == "doctor":
                doc = run_doctor()
                print(f"OS: {doc.get('os')} | Kernel: {doc.get('kernel')}")
                print(f"CPU: {doc['cpu'].get('model')} ({doc['cpu'].get('cores')} Cores) - Governor: {doc['cpu'].get('governor')}")
                print(f"RAM: {doc['memory'].get('total_mb')} MB Total (zRAM active: {doc['memory'].get('zram_active')})")
                print(f"Battery: {doc['battery'].get('percentage')}% ({doc['battery'].get('status')})")
            elif cmd == "memory":
                stats = get_memory_stats()
                print(f"RAM: {stats['used_mb']} MB / {stats['total_mb']} MB ({stats['percent_used']}%) | zRAM: {stats['zram_used_mb']} MB")
            elif cmd == "power":
                print(f"Active Power Governor Profile: \033[1;32m{profile}\033[0m")
            else:
                subprocess.run(["aero"] + parts)

            elapsed = (time.perf_counter() - start_t) * 1000
            print(f"\033[90m[⏱️ {elapsed:.1f}ms]\033[0m\n")

        except (KeyboardInterrupt, EOFError):
            print("\n\033[38;2;0;242;254m👋 Exiting Aero Shell.\033[0m")
            break


def _print_help():
    print("""
\033[1;37mAvailable Aero Shell Commands:\033[0m
  \033[36mdoctor\033[0m       - Run full hardware diagnostics & thermals
  \033[36mmemory\033[0m       - Inspect memory allocation & zRAM compaction
  \033[36mpower\033[0m        - View active TLP governor profile
  \033[36mvault\033[0m        - Manage encrypted developer credentials
  \033[36mgit\033[0m          - Multi-repository workspace status scan
  \033[36mports\033[0m        - Scan listening TCP/UDP dev server ports
  \033[36mspeed\033[0m        - Measure latency ping & DNS resolution speed
  \033[36mssl\033[0m          - Generate local HTTPS SSL/TLS certificates
  \033[36mfirewall\033[0m     - Inspect active UFW network rules
  \033[36mbenchmark\033[0m    - Run multi-core CPU & RAM benchmark
  \033[36mclear\033[0m        - Clear the terminal screen
  \033[36mexit\033[0m         - Exit interactive shell
""")
