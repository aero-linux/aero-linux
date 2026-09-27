import os
import shutil
import subprocess
import urllib.request


def install_ollama() -> bool:
    if shutil.which("ollama"):
        return True

    print("🚀 Installing Ollama (high-performance local AI runtime)...")
    try:
        # Run standard one-line install
        res = subprocess.run(
            "curl -fsSL https://ollama.com/install.sh | sh",
            shell=True,
            capture_output=True,
            text=True,
        )
        return res.returncode == 0 and shutil.which("ollama") is not None
    except Exception as e:
        print(f"Error installing Ollama: {e}")
        return False


def get_ai_status() -> dict:
    status = {
        "ollama_installed": shutil.which("ollama") is not None,
        "ollama_running": False,
        "models": [],
    }

    if status["ollama_installed"]:
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    import json

                    data = json.loads(resp.read().decode())
                    status["ollama_running"] = True
                    status["models"] = [m.get("name") for m in data.get("models", [])]
        except Exception:
            pass

    return status


def pull_model(model_name: str) -> bool:
    if not shutil.which("ollama"):
        print("Ollama is not installed. Run 'aero ai init' first.")
        return False

    print(f"📥 Pulling AI model: {model_name}...")
    try:
        proc = subprocess.run(["ollama", "pull", model_name])
        return proc.returncode == 0
    except Exception as e:
        print(f"Failed to pull model: {e}")
        return False


def run_model(model_name: str):
    if not shutil.which("ollama"):
        print("Ollama is not installed. Run 'aero ai init' first.")
        return

    print(f"⚡ Launching interactive session with {model_name}...")
    subprocess.run(["ollama", "run", model_name])
