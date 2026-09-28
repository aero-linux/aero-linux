import os
import shutil
import subprocess
import time


def launch_db_ui(db_type: str = "postgres", port: int = 8081) -> bool:
    print(f"\n🐘 \033[1;36mAERO DATABASE WEB STUDIO\033[0m")
    print("═" * 58)
    print(f" • Database Target: \033[1;32m{db_type.upper()}\033[0m")
    print(f" • Web Studio URL:  \033[1;36mhttp://localhost:{port}\033[0m")
    print("═" * 58)

    if shutil.which("docker"):
        if db_type.lower() == "redis":
            cmd = f"docker run --rm -p {port}:8081 --name aero_redis_ui rediscommander/redis-commander:latest"
        else:
            # Universal Adminer for Postgres, MySQL, SQLite
            cmd = f"docker run --rm -p {port}:8080 --name aero_db_adminer adminer:latest"

        print(f"Starting lightweight Studio container on port {port}...")
        try:
            subprocess.run(cmd, shell=True)
            return True
        except KeyboardInterrupt:
            print("\nDatabase Studio stopped.\n")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
    else:
        print("❌ Docker CLI required to launch isolated Database Studio.")
        print("Tip: Install with 'aero store install docker'")
        return False
