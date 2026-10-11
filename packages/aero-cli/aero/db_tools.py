import subprocess
import shutil
import sqlite3
import os
from typing import Dict, Any, List

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


def run_sql_migration(sql_file: str, db_target: str = "sqlite") -> bool:
    """
    Execute a raw SQL migration script against SQLite or a containerized database.
    """
    if not os.path.isfile(sql_file):
        print(f"❌ SQL migration file not found: {sql_file}")
        return False

    with open(sql_file, "r") as f:
        sql_content = f.read()

    print(f"\n📦 RUNNING SQL MIGRATION: {os.path.basename(sql_file)} ➔ {db_target}")
    print("═" * 60)

    if db_target.endswith(".db") or db_target.endswith(".sqlite") or db_target == "sqlite":
        db_path = db_target if db_target != "sqlite" else "aero_dev.sqlite"
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.executescript(sql_content)
            conn.commit()
            conn.close()
            print(f"✅ Migration executed successfully against SQLite: {db_path}")
            return True
        except Exception as e:
            print(f"❌ SQLite migration error: {e}")
            return False

    print(f"⚠️  Target '{db_target}' is an external database; ensure driver is configured.")
    return True


def inspect_sqlite_schema(sqlite_file: str) -> List[Dict[str, Any]]:
    """
    Inspect tables and column schemas of an existing SQLite database.
    """
    if not os.path.isfile(sqlite_file):
        print(f"❌ SQLite file not found: {sqlite_file}")
        return []

    tables_info = []
    try:
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = [r[0] for r in cursor.fetchall()]

        print(f"\n📊 SQLITE SCHEMA INSPECTOR: {os.path.basename(sqlite_file)}")
        print("═" * 60)
        for tbl in tables:
            cursor.execute(f"PRAGMA table_info('{tbl}');")
            columns = [{"id": col[0], "name": col[1], "type": col[2], "notnull": col[3]} for col in cursor.fetchall()]
            tables_info.append({"table": tbl, "columns": columns})
            col_names = ", ".join([f"{c['name']} ({c['type']})" for c in columns])
            print(f" • Table \033[1;36m{tbl}\033[0m: {col_names}")
        print("═" * 60 + "\n")
        conn.close()
    except Exception as e:
        print(f"❌ Error inspecting SQLite schema: {e}")
    return tables_info
