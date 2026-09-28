import shutil
import subprocess
import time


def start_tunnel(port: int = 3000) -> bool:
    print(f"\n🌐 \033[1;36mAERO INSTANT PUBLIC HTTPS TUNNEL\033[0m")
    print("═" * 58)
    print(f" • Forwarding Local Port: \033[1;32mhttp://localhost:{port}\033[0m")

    # 1. Check if cloudflared is installed
    if shutil.which("cloudflared"):
        print(" • Using: Cloudflare Quick Tunnels (Encrypted Zero-Trust)")
        cmd = f"cloudflared tunnel --url http://localhost:{port}"
    else:
        # Fallback to zero-dependency SSH tunnel via localhost.run
        print(" • Using: Zero-Dependency SSH Tunnel (localhost.run)")
        cmd = f"ssh -R 80:localhost:{port} nokey@localhost.run"

    print("─" * 58)
    print(f"Executing: {cmd}")
    print("Press Ctrl+C to close tunnel.\n")
    try:
        subprocess.run(cmd, shell=True)
        return True
    except KeyboardInterrupt:
        print("\n\033[1;33m✔ Tunnel closed cleanly.\033[0m\n")
        return True
    except Exception as e:
        print(f"❌ Error opening tunnel: {e}")
        return False
