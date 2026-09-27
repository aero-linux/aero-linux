import subprocess
import shutil


def check_docker() -> bool:
    if not shutil.which("docker"):
        print("❌ Docker CLI is not installed or not in PATH.")
        return False
    return True


def prune_docker() -> bool:
    if not check_docker():
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
        return

    print("🐳 \033[1;36mACTIVE DOCKER CONTAINERS RESOURCE USAGE\033[0m")
    print("═" * 60)
    try:
        subprocess.run(["docker", "stats", "--no-stream", "--format", "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"])
    except Exception as e:
        print(f"❌ Failed to get Docker stats: {e}")
