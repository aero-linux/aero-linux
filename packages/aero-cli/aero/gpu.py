import os
import shutil
import subprocess
from aero.doctor import get_gpu_info


def setup_nvidia_driver() -> bool:
    print("🔍 Detecting NVIDIA hardware...")
    gpus = get_gpu_info()
    nvidia_gpus = [g for g in gpus if g.get("vendor") == "NVIDIA"]

    if not nvidia_gpus:
        print("⚠️ No NVIDIA GPU detected on this system.")
        return False

    gpu = nvidia_gpus[0]
    print(f"🎮 Found: {gpu['model']}")
    print("📦 Installing official NVIDIA proprietary driver and Container Toolkit for AI...")

    try:
        # 1. Update repos & install driver
        cmd = "sudo apt-get update && sudo apt-get install -y nvidia-driver-550 nvidia-utils-550 nvidia-dkms-550"
        subprocess.run(cmd, shell=True, check=True)

        # 2. Configure Wayland KMS Modeset in modprobe
        modprobe_conf = "/etc/modprobe.d/nvidia-modeset.conf"
        content = "options nvidia-drm modeset=1 fbdev=1\n"
        subprocess.run(["sudo", "tee", modprobe_conf], input=content, text=True, capture_output=True)

        # 3. Configure Wayland environment variables
        env_file = "/etc/environment.d/10-aero-nvidia.conf"
        os.makedirs(os.path.dirname(env_file), exist_ok=True)
        env_content = (
            "GBM_BACKEND=nvidia-drm\n"
            "__GLX_VENDOR_LIBRARY_NAME=nvidia\n"
            "LIBVA_DRIVER_NAME=nvidia\n"
            "WLR_NO_HARDWARE_CURSORS=1\n"
        )
        subprocess.run(["sudo", "tee", env_file], input=env_content, text=True, capture_output=True)

        # 4. Install NVIDIA Container Toolkit for Docker AI workloads
        print("🐳 Setting up NVIDIA Container Toolkit for Docker...")
        docker_setup = (
            "curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg && "
            "curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | "
            "sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | "
            "sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list && "
            "sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit && "
            "sudo nvidia-ctk runtime configure --runtime=docker || true"
        )
        subprocess.run(docker_setup, shell=True)

        print("✅ NVIDIA driver & AI Container Toolkit configured successfully!")
        print("ℹ️  Please reboot for kernel modeset parameters to take effect.")
        return True
    except Exception as e:
        print(f"❌ Failed to configure NVIDIA driver: {e}")
        return False


def setup_rocm_driver() -> bool:
    print("🔍 Detecting AMD GPU hardware...")
    gpus = get_gpu_info()
    amd_gpus = [g for g in gpus if g.get("vendor") == "AMD"]

    if not amd_gpus:
        print("⚠️ No AMD GPU detected on this system.")
        return False

    print(f"🎮 Found: {amd_gpus[0]['model']}")
    print("📦 Configuring AMD ROCm kernel permissions for PyTorch and Ollama...")

    try:
        user = os.environ.get("USER", "root")
        subprocess.run(f"sudo usermod -a -G render,video {user}", shell=True, check=True)
        # Add HSA override for consumer RDNA2/RDNA3 GPUs
        env_file = "/etc/environment.d/10-aero-rocm.conf"
        os.makedirs(os.path.dirname(env_file), exist_ok=True)
        subprocess.run(
            ["sudo", "tee", env_file],
            input="HSA_OVERRIDE_GFX_VERSION=10.3.0\nROCR_VISIBLE_DEVICES=all\n",
            text=True,
            capture_output=True,
        )
        print("✅ AMD ROCm AI runtime environment configured successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to configure ROCm driver: {e}")
        return False
