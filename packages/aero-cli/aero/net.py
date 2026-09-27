import subprocess

DNS_PROVIDERS = {
    "cloudflare": {"dns1": "1.1.1.1", "dns2": "1.0.0.1", "name": "Cloudflare Privacy DNS"},
    "quad9": {"dns1": "9.9.9.9", "dns2": "149.112.112.112", "name": "Quad9 Malware Blocking DNS"},
    "google": {"dns1": "8.8.8.8", "dns2": "8.8.4.4", "name": "Google Public DNS"},
}


def enable_bbr() -> bool:
    print("⚡ Enabling Google BBR TCP Congestion Control...")
    try:
        subprocess.run(["sudo", "modprobe", "tcp_bbr"], check=True)
        conf = "net.core.default_qdisc=fq\nnet.ipv4.tcp_congestion_control=bbr\n"
        subprocess.run(["sudo", "tee", "/etc/sysctl.d/99-bbr.conf"], input=conf, text=True, check=True)
        subprocess.run(["sudo", "sysctl", "--system"], check=True, capture_output=True)
        print("✅ BBR TCP congestion control active (higher bandwidth, lower latency bufferbloat).")
        return True
    except Exception as e:
        print(f"❌ Failed to enable BBR: {e}")
        return False


def set_dns(provider_name: str) -> bool:
    if provider_name not in DNS_PROVIDERS:
        print(f"❌ Unknown provider: {provider_name}. Choose from: {list(DNS_PROVIDERS.keys())}")
        return False

    prov = DNS_PROVIDERS[provider_name]
    print(f"🌐 Setting DNS to {prov['name']} ({prov['dns1']}, {prov['dns2']})...")

    # Configure resolved.conf or resolv.conf
    try:
        conf = f"[Resolve]\nDNS={prov['dns1']} {prov['dns2']}\nDNSOverTLS=yes\n"
        subprocess.run(["sudo", "tee", "/etc/systemd/resolved.conf.d/10-aero-dns.conf"], input=conf, text=True)
        subprocess.run(["sudo", "systemctl", "restart", "systemd-resolved"], capture_output=True)
        print(f"✅ DNS switched to {prov['name']} with DNS-over-TLS encryption.")
        return True
    except Exception as e:
        print(f"❌ Failed to set DNS: {e}")
        return False


def optimize_wifi_latency() -> bool:
    print("📶 Disabling WiFi power-save mode to eliminate packet jitter...")
    try:
        conf = "[connection]\nwifi.powersave = 2\n"
        subprocess.run(["sudo", "tee", "/etc/NetworkManager/conf.d/default-wifi-powersave-on.conf"], input=conf, text=True)
        subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"], capture_output=True)
        print("✅ WiFi power-save disabled for minimal gaming/SSH latency.")
        return True
    except Exception as e:
        print(f"❌ Failed to tune WiFi: {e}")
        return False
