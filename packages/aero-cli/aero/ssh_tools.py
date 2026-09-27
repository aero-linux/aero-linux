import os
import subprocess
import shutil


def check_ssh_status():
    print("🔑 \033[1;36mAERO SSH KEY & SECURITY AUDIT\033[0m")
    print("═" * 55)

    ssh_dir = os.path.expanduser("~/.ssh")
    if not os.path.exists(ssh_dir):
        print("ℹ️ No ~/.ssh directory found. Run 'aero ssh gen' to create an Ed25519 keypair.")
        return

    keys = []
    for f in os.listdir(ssh_dir):
        if f.endswith(".pub"):
            priv = f[:-4]
            keys.append((f, priv))

    if not keys:
        print("⚪ No public SSH keys found. Run 'aero ssh gen' to generate one.")
        return

    print("Found Public SSH Keys:")
    for pub, priv in keys:
        priv_path = os.path.join(ssh_dir, priv)
        pub_path = os.path.join(ssh_dir, pub)
        perm = oct(os.stat(priv_path).st_mode)[-3:] if os.path.exists(priv_path) else "N/A"
        print(f" • \033[1;32m{pub}\033[0m (Private key perms: {perm})")
    print()


def generate_ed25519_key(email: str = "developer@aero-linux.org"):
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
    key_path = os.path.join(ssh_dir, "id_ed25519")

    if os.path.exists(key_path):
        print(f"⚠️ SSH key already exists at: {key_path}")
        return

    print(f"🔑 Generating Ed25519 SSH keypair ({email})...")
    subprocess.run(["ssh-keygen", "-t", "ed25519", "-C", email, "-f", key_path, "-N", ""])
    print(f"✅ SSH key generated at: {key_path}")


def copy_public_key():
    ssh_dir = os.path.expanduser("~/.ssh")
    for f in ["id_ed25519.pub", "id_rsa.pub"]:
        pub_path = os.path.join(ssh_dir, f)
        if os.path.exists(pub_path):
            with open(pub_path) as kf:
                key_text = kf.read().strip()
            
            print(f"📋 Public Key (~/.ssh/{f}):\n\n\033[1;36m{key_text}\033[0m\n")
            
            if shutil.which("wl-copy"):
                subprocess.run(["wl-copy"], input=key_text, text=True)
                print("✅ Copied to Wayland clipboard.")
            elif shutil.which("xclip"):
                subprocess.run(["xclip", "-selection", "clipboard"], input=key_text, text=True)
                print("✅ Copied to X11 clipboard.")
            return

    print("❌ No public SSH key found. Run 'aero ssh gen' first.")


def test_github_auth():
    print("🌐 Testing SSH authentication to GitHub (git@github.com)...")
    res = subprocess.run(["ssh", "-T", "-o", "StrictHostKeyChecking=accept-new", "git@github.com"], capture_output=True, text=True)
    output = res.stderr or res.stdout
    print(output.strip())
