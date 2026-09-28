import json
import os
import shutil
import sys
import urllib.request
from typing import Optional


DEFAULT_AGENT_MODEL = "qwen2.5-coder:7b"
FALLBACK_AGENT_MODEL = "deepseek-r1:8b"


def ask_local_agent(prompt: str, model: Optional[str] = None, is_shell_query: bool = False):
    """Streams a response from local Ollama model tailored for systems and developer queries."""
    if not shutil.which("ollama"):
        print("❌ Ollama is not installed. Run 'aero ai init' first.")
        return

    # Select active model
    selected_model = model or DEFAULT_AGENT_MODEL
    
    # Check if model is available or get first available model
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=2) as resp:
            data = json.loads(resp.read().decode())
            available_models = [m.get("name") for m in data.get("models", [])]
            if available_models and selected_model not in available_models:
                # Fallback to any installed model
                selected_model = available_models[0]
    except Exception:
        print("⚠️  Local Ollama daemon is not responding. Starting service or fallback.")

    system_prompt = (
        "You are Aero Assistant, an expert Linux systems, kernel, and high-performance backend engineering AI. "
        "Provide direct, concise, practical terminal commands and high-performance code. Zero filler."
    )
    if is_shell_query:
        system_prompt = (
            "You are a Linux command generator for Aero Linux. "
            "Return ONLY the single best Linux terminal command to accomplish the user's task. No markdown, no explanation."
        )

    payload = {
        "model": selected_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "stream": True,
    }

    print(f"\n🤖 Aero Agent ({selected_model})")
    print("─" * 54)

    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            for line in resp:
                if line:
                    chunk = json.loads(line.decode("utf-8"))
                    msg = chunk.get("message", {}).get("content", "")
                    sys.stdout.write(msg)
                    sys.stdout.flush()
        print("\n" + "─" * 54 + "\n")
    except Exception as e:
        print(f"\n❌ Local AI Error: {e}")
        print("Tip: Ensure local Ollama is running ('aero ai init' or 'aero ai run').\n")
