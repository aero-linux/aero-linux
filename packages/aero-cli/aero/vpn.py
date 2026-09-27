import subprocess
import shutil


def check_vpn_status():
    print("🔒 \033[1;36mWIREGUARD & SECURE MESH VPN STATUS\033[0m")
    print("═" * 55)

    active_vpn = False
    
    # Check WireGuard
    if shutil.which("wg"):
        try:
            res = subprocess.run(["sudo", "wg", "show"], capture_output=True, text=True)
            if res.stdout.strip():
                print("Active WireGuard Tunnels:")
                print(res.stdout)
                active_vpn = True
        except Exception:
            pass

    # Check Tailscale
    if shutil.which("tailscale"):
        try:
            res = subprocess.run(["tailscale", "status"], capture_output=True, text=True)
            if "Tailscale is stopped" not in res.stdout:
                print("Tailscale Mesh Network:")
                print(res.stdout[:300])
                active_vpn = True
        except Exception:
            pass

    if not active_vpn:
        print("⚪ No active VPN or mesh tunnels running.")
    print()


def toggle_wireguard(interface: str, up: bool = True) -> bool:
    action = "up" if up else "down"
    print(f"🔒 Bringing WireGuard interface '{interface}' {action.upper()}...")
    if shutil.which("wg-quick"):
        res = subprocess.run(["sudo", "wg-quick", action, interface])
        return res.returncode == 0
    print("❌ wg-quick not found. Run 'sudo apt-get install -y wireguard-tools'.")
    return False
