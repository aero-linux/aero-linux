import json
import os
import subprocess
import shutil
from typing import List, Dict, Any

HISTORY_FILE = os.path.expanduser("~/.cache/aero/clipboard_history.json")


def ensure_history_dir():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)


def load_history() -> List[str]:
    ensure_history_dir()
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_history(history: List[str]):
    ensure_history_dir()
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history[:50], f, indent=2)
    except Exception:
        pass


def record_clipboard_entry(text: str):
    if not text or not text.strip():
        return
    text = text.strip()
    history = load_history()
    if text in history:
        history.remove(text)
    history.insert(0, text)
    save_history(history)


def check_clipboard() -> bool:
    return bool(shutil.which("wl-copy") or shutil.which("xclip"))


def clear_clipboard() -> bool:
    print("📋 Clearing clipboard buffers...")
    if shutil.which("wl-copy"):
        subprocess.run(["wl-copy", "--clear"])
    if os.path.exists(HISTORY_FILE):
        save_history([])
    print("✅ Clipboard buffer and history cleared.")
    return True


def show_clipboard_menu():
    history = load_history()
    if not history:
        subprocess.run(["notify-send", "Clipboard", "Clipboard history is empty"])
        return

    # If wofi is available, use it as GUI selector
    if shutil.which("wofi"):
        items_str = "\n".join([f"[{i+1}] {item[:60].replace(chr(10), ' ')}" for i, item in enumerate(history)])
        p = subprocess.Popen(["wofi", "--dmenu", "--prompt", "📋 Clipboard History (Win+V)"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        selected, _ = p.communicate(input=items_str)
        if selected:
            idx = int(selected.split("]")[0].replace("[", "")) - 1
            chosen_text = history[idx]
            if shutil.which("wl-copy"):
                p_copy = subprocess.Popen(["wl-copy"], stdin=subprocess.PIPE, text=True)
                p_copy.communicate(input=chosen_text)
            subprocess.run(["notify-send", "Clipboard", f"Copied to clipboard: {chosen_text[:30]}..."])
    else:
        print("\n📋 \033[1;36mAERO CLIPBOARD HISTORY\033[0m")
        for i, item in enumerate(history[:10]):
            print(f" [{i+1}] {item[:70]}")
