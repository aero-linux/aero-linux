import os
import shutil
import subprocess

ENVIRONMENTS = {
    "node": {
        "image": "node:22-alpine",
        "description": "Node.js 22 LTS, TypeScript, npm, and yarn",
        "cmd": "sh",
    },
    "python": {
        "image": "python:3.12-slim",
        "description": "Python 3.12, pip, and virtualenv",
        "cmd": "bash",
    },
    "rust": {
        "image": "rust:latest",
        "description": "Rust toolchain (rustc, cargo, clippy)",
        "cmd": "bash",
    },
    "go": {
        "image": "golang:1.23-alpine",
        "description": "Go 1.23 standard developer environment",
        "cmd": "sh",
    },
    "c": {
        "image": "gcc:latest",
        "description": "GCC, Clang, GDB, CMake, and Make build toolchain",
        "cmd": "bash",
    },
    "postgres": {
        "image": "postgres:16-alpine",
        "description": "PostgreSQL 16 Database Server (Port 5432)",
        "cmd": "postgres",
        "service": True,
        "ports": ["5432:5432"],
        "env": ["POSTGRES_PASSWORD=postgres", "POSTGRES_USER=postgres", "POSTGRES_DB=devdb"],
    },
    "redis": {
        "image": "redis:7-alpine",
        "description": "Redis 7 In-Memory Cache Server (Port 6379)",
        "cmd": "redis-server",
        "service": True,
        "ports": ["6379:6379"],
    },
}


def list_dev_environments():
    print("⚡ Available Aero Isolated Dev Environments:")
    print("--------------------------------------------------")
    for name, info in ENVIRONMENTS.items():
        tag = "[Service]" if info.get("service") else "[Interactive]"
        print(f" • {name:<10} {tag:<15} - {info['description']}")
    print("\nRun: 'aero dev run <env>' to launch in current directory.")


def run_dev_environment(env_name: str, detached: bool = False) -> bool:
    if env_name not in ENVIRONMENTS:
        print(f"❌ Unknown environment: {env_name}")
        list_dev_environments()
        return False

    if not shutil.which("docker") and not shutil.which("podman"):
        print("❌ Docker or Podman is required. Run 'sudo apt-get install -y docker.io' to install.")
        return False

    runtime = "docker" if shutil.which("docker") else "podman"
    env_info = ENVIRONMENTS[env_name]
    cwd = os.getcwd()

    print(f"🚀 Launching {env_name} environment ({env_info['image']})...")

    if env_info.get("service"):
        port_args = []
        for p in env_info.get("ports", []):
            port_args.extend(["-p", p])
        
        env_args = []
        for e in env_info.get("env", []):
            env_args.extend(["-e", e])

        cmd = [runtime, "run", "-d", "--name", f"aero-dev-{env_name}"] + port_args + env_args + [env_info["image"]]
        res = subprocess.run(cmd)
        if res.returncode == 0:
            print(f"✅ {env_name.capitalize()} service started in background (Container: aero-dev-{env_name})")
            return True
        return False
    else:
        cmd = [
            runtime, "run", "--rm", "-it",
            "-v", f"{cwd}:/workspace",
            "-w", "/workspace",
            env_info["image"],
            env_info["cmd"],
        ]
        res = subprocess.run(cmd)
        return res.returncode == 0
