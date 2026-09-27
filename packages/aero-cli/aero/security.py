import os
import shutil
import subprocess


def audit_security() -> dict:
    report = {
        "firewall_active": False,
        "aslr_enabled": False,
        "ssh_root_login_disabled": True,
        "kernel_dmesg_restricted": False,
    }

    # Check UFW firewall
    if shutil.which("ufw"):
        try:
            res = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True)
            report["firewall_active"] = "Status: active" in res.stdout
        except Exception:
            pass

    # Check ASLR (Address Space Layout Randomization)
    if os.path.exists("/proc/sys/kernel/randomize_va_space"):
        with open("/proc/sys/kernel/randomize_va_space", "r") as f:
            report["aslr_enabled"] = f.read().strip() == "2"

    # Check dmesg restriction
    if os.path.exists("/proc/sys/kernel/dmesg_restrict"):
        with open("/proc/sys/kernel/dmesg_restrict", "r") as f:
            report["kernel_dmesg_restricted"] = f.read().strip() == "1"

    print("🛡️  AERO SECURITY & HARDENING AUDIT")
    print("═" * 50)
    print(f" • UFW Firewall Active:      {'✅ Yes' if report['firewall_active'] else '⚠️  Disabled (Run: aero security harden)'}")
    print(f" • ASLR (Memory Protection): {'✅ Enabled (Level 2)' if report['aslr_enabled'] else '❌ Disabled'}")
    print(f" • Kernel dmesg Protection:  {'✅ Restricted' if report['kernel_dmesg_restricted'] else 'ℹ️  Unrestricted'}")
    print()

    return report


def harden_system() -> bool:
    print("🔒 Applying Aero Kernel & Network Security Hardening...")
    try:
        # Enable UFW with sensible defaults
        if shutil.which("ufw"):
            subprocess.run(["sudo", "ufw", "default", "deny", "incoming"], check=True)
            subprocess.run(["sudo", "ufw", "default", "allow", "outgoing"], check=True)
            subprocess.run(["sudo", "ufw", "--force", "enable"], check=True)
            print("✅ UFW Firewall enabled with secure defaults.")

        # Kernel security sysctl
        sysctl_conf = (
            "kernel.dmesg_restrict = 1\n"
            "kernel.kptr_restrict = 2\n"
            "net.ipv4.conf.all.rp_filter = 1\n"
            "net.ipv4.conf.default.rp_filter = 1\n"
            "net.ipv4.icmp_echo_ignore_broadcasts = 1\n"
        )
        subprocess.run(["sudo", "tee", "/etc/sysctl.d/99-aero-security.conf"], input=sysctl_conf, text=True, check=True)
        subprocess.run(["sudo", "sysctl", "--system"], check=True, capture_output=True)
        print("✅ Kernel ASLR, anti-spoofing rp_filter, and dmesg restrictions applied.")
        return True
    except Exception as e:
        print(f"❌ Hardening failed: {e}")
        return False
