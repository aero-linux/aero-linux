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
    "java": {
        "image": "eclipse-temurin:21-jdk-alpine",
        "description": "Eclipse Temurin OpenJDK 21 LTS, Maven, Gradle",
        "cmd": "sh",
    },
    "ai": {
        "image": "python:3.11-slim",
        "description": "AI & ML Stack: PyTorch, Transformers, HuggingFace",
        "cmd": "bash",
    },
}


NATIVE_STACKS = {
    "node": "curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs",
    "rust": "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y",
    "python": "sudo apt-get install -y python3 python3-pip python3-venv python3-dev",
    "java": "sudo apt-get install -y openjdk-21-jdk maven gradle",
    "docker": "sudo apt-get install -y docker.io docker-compose && sudo usermod -aG docker $USER",
    "c": "sudo apt-get install -y build-essential cmake gdb clang valgrind",
}


def install_native_stack(stack_name: str) -> bool:
    stack_name = stack_name.lower().strip()
    if stack_name not in NATIVE_STACKS:
        print(f"❌ Unknown native stack: {stack_name}")
        print(f"Available stacks: {', '.join(NATIVE_STACKS.keys())}")
        return False

    cmd = NATIVE_STACKS[stack_name]
    print(f"⚡ \033[1;36mINSTALLING NATIVE DEVELOPER STACK: {stack_name.upper()}\033[0m")
    print("═" * 58)
    print(f"Executing: {cmd}\n")
    res = subprocess.run(cmd, shell=True)
    if res.returncode == 0:
        print(f"\n✅ {stack_name.upper()} developer stack installed successfully.")
        return True
    return False


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
