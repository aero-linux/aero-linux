import subprocess
import shutil

DATABASES = {
    "postgres": {
        "image": "postgres:16-alpine",
        "container": "aero-db-postgres",
        "port": "5432:5432",
        "env": ["POSTGRES_PASSWORD=postgres", "POSTGRES_USER=postgres", "POSTGRES_DB=aero_dev"],
        "desc": "PostgreSQL 16 Relational DB (Port 5432, User/Pass: postgres)",
    },
    "redis": {
        "image": "redis:7-alpine",
        "container": "aero-db-redis",
        "port": "6379:6379",
        "env": [],
        "desc": "Redis 7 In-Memory Cache (Port 6379)",
    },
    "mysql": {
        "image": "mysql:8.0",
        "container": "aero-db-mysql",
        "port": "3306:3306",
        "env": ["MYSQL_ROOT_PASSWORD=root", "MYSQL_DATABASE=aero_dev"],
        "desc": "MySQL 8.0 Relational DB (Port 3306, User/Pass: root/root)",
    },
    "mongo": {
        "image": "mongo:7.0",
        "container": "aero-db-mongo",
        "port": "27017:27017",
        "env": [],
        "desc": "MongoDB 7.0 Document DB (Port 27017)",
    },
    "clickhouse": {
        "image": "clickhouse/clickhouse-server:latest",
        "container": "aero-db-clickhouse",
        "port": "8123:8123",
        "env": [],
        "desc": "ClickHouse Columnar Analytics DB (Port 8123)",
    },
}


def list_databases():
    print("🗄️  \033[1;36mAERO LOCAL DATABASE SUITE\033[0m")
    print("═" * 65)
    for key, info in DATABASES.items():
        print(f" • \033[1;33m{key:<12}\033[0m ➔  {info['desc']}")
    print("\nRun: 'aero db start <name>' to launch in background.")


def start_database(db_key: str) -> bool:
    if db_key not in DATABASES:
        print(f"❌ Unknown database: {db_key}")
        list_databases()
        return False

    runtime = "docker" if shutil.which("docker") else "podman"
    if not shutil.which(runtime):
        print("❌ Docker or Podman is required to spin up local database engines.")
        return False

    db = DATABASES[db_key]
    print(f"🚀 Starting \033[1;32m{db_key.capitalize()}\033[0m ({db['image']})...")

    # Stop existing container if running
    subprocess.run([runtime, "rm", "-f", db["container"]], capture_output=True)

    cmd = [runtime, "run", "-d", "--name", db["container"], "-p", db["port"]]
    for e in db["env"]:
        cmd.extend(["-e", e])
    cmd.append(db["image"])

    res = subprocess.run(cmd)
    if res.returncode == 0:
        print(f"✅ {db_key.capitalize()} is running on port {db['port'].split(':')[0]} (Container: {db['container']}).")
        return True
    return False


def stop_database(db_key: str) -> bool:
    if db_key not in DATABASES:
        print(f"❌ Unknown database: {db_key}")
        return False

    runtime = "docker" if shutil.which("docker") else "podman"
    db = DATABASES[db_key]
    print(f"🛑 Stopping container {db['container']}...")
    res = subprocess.run([runtime, "rm", "-f", db["container"]], capture_output=True)
    if res.returncode == 0:
        print(f"✅ {db_key.capitalize()} stopped.")
        return True
    return False
