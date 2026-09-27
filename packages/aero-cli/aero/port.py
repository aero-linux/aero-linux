import subprocess
import shutil
import os
import signal


def list_ports():
    print("🔌 \033[1;36mACTIVE LISTENING PORTS & DEV SERVICES\033[0m")
    print("═" * 65)
    print(f"  \033[1m{'PORT':<8} {'PROTO':<8} {'PID':<8} {'PROCESS':<20} {'SERVICE'}\033[0m")
    print("─" * 65)

    if not shutil.which("ss"):
        print("❌ 'ss' command not found.")
        return

    res = subprocess.run(["ss", "-tulpn"], capture_output=True, text=True)
    lines = res.stdout.strip().split("\n")

    found_any = False
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 5:
            proto = parts[0]
            local_addr = parts[4]
            port = local_addr.split(":")[-1] if ":" in local_addr else local_addr
            
            pid_info = parts[6] if len(parts) >= 7 else "-"
            pid = "-"
            pname = "-"
            
            if 'pid=' in pid_info:
                try:
                    pid = pid_info.split('pid=')[1].split(',')[0]
                    pname = pid_info.split('users:(("')[1].split('"')[0]
                except Exception:
                    pass

            service_tag = ""
            if port == "5432": service_tag = "PostgreSQL"
            elif port == "6379": service_tag = "Redis"
            elif port == "3000": service_tag = "Node/Next.js/React"
            elif port == "8000": service_tag = "FastAPI/Django"
            elif port == "11434": service_tag = "Ollama Local AI"
            elif port == "8080": service_tag = "Web Dev Server"

            print(f"  \033[1;33m{port:<8}\033[0m {proto:<8} {pid:<8} \033[1;36m{pname:<20}\033[0m {service_tag}")
            found_any = True

    if not found_any:
        print("  No active listening ports found.")
    print()


def kill_port(port: str) -> bool:
    print(f"🛑 Terminating process listening on port {port}...")
    res = subprocess.run(["ss", "-tulpn"], capture_output=True, text=True)
    for line in res.stdout.split("\n"):
        if f":{port} " in line or f":{port}\t" in line:
            if "pid=" in line:
                try:
                    pid_str = line.split("pid=")[1].split(",")[0]
                    pid = int(pid_str)
                    os.kill(pid, signal.SIGTERM)
                    print(f"✅ Sent SIGTERM to PID {pid} on port {port}.")
                    return True
                except Exception as e:
                    print(f"❌ Failed to kill PID: {e}")
                    return False
    print(f"ℹ️ No process found listening on port {port}.")
    return False
