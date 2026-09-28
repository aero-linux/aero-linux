import os
import shutil
import subprocess
from typing import Dict, Any


def get_firewall_status() -> Dict[str, Any]:
    active = False
    rules = []
    if shutil.which("ufw"):
        try:
            res = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True)
            active = "Status: active" in res.stdout
            for line in res.stdout.split("\n"):
                if "ALLOW" in line or "DENY" in line:
                    rules.append(line.strip())
        except Exception:
            pass
    return {"active": active, "rules": rules}


def show_firewall_status():
    print("\n🛡️  \033[1;36mAERO DEVELOPER FIREWALL & SECURITY RULES\033[0m")
    print("═" * 56)
    st = get_firewall_status()
    print(f" • Firewall Status: {'\033[1;32m✅ Active\033[0m' if st['active'] else '\033[1;33m⚠️  Disabled\033[0m'}")
    if st["rules"]:
        print(" • Active Port Whitelist Rules:")
        for r in st["rules"]:
            print(f"   - {r}")
    else:
        print(" • No custom port rules configured.")
    print("═" * 56 + "\n")


def allow_port(port: int, proto: str = "tcp") -> bool:
    print(f"🛡️  Allowing inbound traffic on port {port}/{proto}...")
    try:
        cmd = f"sudo ufw allow {port}/{proto}"
        subprocess.run(cmd, shell=True, capture_output=True)
        print(f"✅ Port {port}/{proto} whitelisted.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def block_all_inbound() -> bool:
    print("🛡️  Setting default policy: BLOCK all unsolicited inbound connections...")
    try:
        subprocess.run("sudo ufw default deny incoming && sudo ufw default allow outgoing && sudo ufw enable", shell=True, capture_output=True)
        print("✅ Strict firewall lockdown enabled.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
