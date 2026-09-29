"""
Aero Linux - Docker & Container Orchestration Engine
High-performance container lifecycle telemetry, automated cleanup, and status monitor.
"""

import subprocess
import shutil
from typing import List, Dict, Any


def check_docker() -> bool:
    if not shutil.which("docker"):
        return False
    return True


def get_containers_list(all_containers: bool = True) -> List[Dict[str, Any]]:
    if not check_docker():
        return []

    cmd = ["docker", "ps", "--format", "{{.ID}}|{{.Names}}|{{.Image}}|{{.Status}}|{{.Ports}}|{{.State}}"]
    if all_containers:
        cmd.append("-a")

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if res.returncode != 0:
            return []

        containers = []
        for line in res.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 6:
                containers.append({
                    "id": parts[0],
                    "name": parts[1],
                    "image": parts[2],
                    "status": parts[3],
                    "ports": parts[4],
                    "state": parts[5],
                })
        return containers
    except Exception:
        return []


def container_action(container_id: str, action: str) -> bool:
    if not check_docker():
        return False
    if action not in ["start", "stop", "restart", "kill", "rm", "pause", "unpause"]:
        return False

    try:
        res = subprocess.run(["docker", action, container_id], capture_output=True, text=True, timeout=10)
        return res.returncode == 0
    except Exception:
        return False


def get_container_logs(container_id: str, tail: int = 100) -> str:
    if not check_docker():
        return "Docker is not installed or not running."
    try:
        res = subprocess.run(["docker", "logs", "--tail", str(tail), container_id], capture_output=True, text=True, timeout=5)
        return res.stdout if res.returncode == 0 else res.stderr
    except Exception as e:
        return f"Error reading logs: {e}"


def prune_docker() -> bool:
    if not check_docker():
        print("❌ Docker CLI is not installed or not in PATH.")
        return False

    print("🧹 \033[1;36mPruning unused Docker images, dangling volumes, and buildcache...\033[0m")
    try:
        subprocess.run(["docker", "system", "prune", "-a", "--volumes", "-f"], check=True)
        print("✅ Docker system pruned successfully. Disk space recovered.")
        return True
    except Exception as e:
        print(f"❌ Failed to prune Docker: {e}")
        return False


def show_docker_stats():
    if not check_docker():
        print("❌ Docker CLI is not installed or not in PATH.")
        return

    print("🐳 \033[1;36mACTIVE DOCKER CONTAINERS RESOURCE USAGE\033[0m")
    print("═" * 60)
    try:
        subprocess.run(["docker", "stats", "--no-stream", "--format", "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"])
    except Exception as e:
        print(f"❌ Failed to get Docker stats: {e}")
