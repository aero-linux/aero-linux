import subprocess
import shutil
import os


def check_kvm() -> bool:
    return os.path.exists("/dev/kvm") and os.access("/dev/kvm", os.R_OK | os.W_OK)


def run_iso_in_vm(iso_path: str, memory_mb: int = 4096, cores: int = 4):
    if not os.path.exists(iso_path):
        print(f"❌ ISO file not found: {iso_path}")
        return False

    if not shutil.which("qemu-system-x86_64"):
        print("❌ QEMU not found. Run 'sudo apt-get install -y qemu-system-x86' to enable micro-VMs.")
        return False

    kvm_flag = ["-enable-kvm"] if check_kvm() else []
    print(f"⚡ Launching Aero Micro-VM ({iso_path})...")
    print(f" • RAM: {memory_mb}MB | Cores: {cores} | KVM Acceleration: {'✅ Active' if kvm_flag else '⚪ Emulated'}")

    cmd = [
        "qemu-system-x86_64",
        "-m", str(memory_mb),
        "-smp", str(cores),
        "-cdrom", iso_path,
        "-boot", "d",
        "-vga", "virtio",
        "-display", "default,show-cursor=on",
    ] + kvm_flag

    try:
        subprocess.run(cmd)
        return True
    except Exception as e:
        print(f"VM launch error: {e}")
        return False
