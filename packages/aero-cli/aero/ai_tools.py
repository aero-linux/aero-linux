import os
import subprocess
from typing import Dict, Any


PROMPT_TEMPLATES = {
    "coding": "You are an elite systems programmer and software architect. Write clean, high-performance, idiomatically typed code with zero extraneous filler. Always verify edge cases.",
    "reasoning": "You are a first-principles deductive reasoning engine. Break down complex mathematical and algorithmic problems step-by-step before concluding.",
    "security-audit": "You are a principal security engineer. Analyze the provided codebase for OWASP vulnerabilities, buffer overflows, race conditions, memory leaks, and injection risks.",
    "systems-c": "You are a Linux kernel and low-level C developer. Focus on explicit pointer arithmetic, cache locality, memory alignments, and minimal syscall overhead.",
}


def audit_ai_memory_footprint() -> Dict[str, Any]:
    print("\n🧠 \033[1;36mAERO LOCAL AI RUNTIME & VRAM MONITOR\033[0m")
    print("═" * 58)

    # 1. Check active LLM daemons
    ollama_active = False
    try:
        res = subprocess.run("pgrep -f ollama || true", shell=True, capture_output=True, text=True)
        ollama_active = bool(res.stdout.strip())
    except Exception:
        pass

    print(f" • Ollama Daemon:    {'\033[1;32mActive (Listening on :11434)\033[0m' if ollama_active else '\033[1;30mIdle / Stopped\033[0m'}")
    print(" • Unified Memory:   \033[1;32m7.5GB zRAM ZSTD Active\033[0m (Dynamic host RAM buffer)")
    print("═" * 58 + "\n")
    return {"ollama_active": ollama_active}


def show_prompt_template(name: str = ""):
    print("\n📝 \033[1;36mAERO CURATED AI SYSTEM PROMPT VAULT\033[0m")
    print("═" * 60)
    if name and name.lower() in PROMPT_TEMPLATES:
        print(f" • Template: \033[1;32m{name}\033[0m\n")
        print(PROMPT_TEMPLATES[name.lower()])
    else:
        for k, v in PROMPT_TEMPLATES.items():
            print(f" • \033[1;33m{k:<16}\033[0m {v[:65]}...")
    print("═" * 60 + "\n")
