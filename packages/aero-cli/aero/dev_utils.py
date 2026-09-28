import subprocess
import time
from typing import Dict, Any


def convert_color(hex_code: str) -> Dict[str, Any]:
    hex_code = hex_code.lstrip("#")
    if len(hex_code) == 3:
        hex_code = "".join(c * 2 for c in hex_code)
    
    if len(hex_code) != 6:
        print(f"❌ Invalid hex color '#{hex_code}' (must be 3 or 6 hex digits).")
        return {}

    r = int(hex_code[0:2], 16)
    g = int(hex_code[2:4], 16)
    b = int(hex_code[4:6], 16)

    # Calculate luminance
    lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0

    print(f"\n🎨 \033[1;36mAERO COLOR INSPECTOR & CONVERTER\033[0m")
    print("═" * 56)
    print(f" • HEX:      #{hex_code.upper()}")
    print(f" • RGB:      rgb({r}, {g}, {b})")
    print(f" • Swatch:   \033[48;2;{r};{g};{b}m      \033[0m (Luminance: {lum:.2f})")
    print("═" * 56 + "\n")

    return {"hex": f"#{hex_code.upper()}", "r": r, "g": g, "b": b, "luminance": round(lum, 2)}


def time_execution(command: str) -> Dict[str, Any]:
    print(f"\n⏱️  \033[1;36mMEASURING COMMAND EXECUTION TIME:\033[0m {command}")
    print("═" * 58)
    
    t0 = time.perf_counter()
    res = subprocess.run(command, shell=True)
    t1 = time.perf_counter()
    
    elapsed_sec = t1 - t0
    elapsed_ms = elapsed_sec * 1000.0

    print("─" * 58)
    print(f" • Real Time:   \033[1;32m{elapsed_sec:.4f} s\033[0m ({elapsed_ms:.2f} ms)")
    print(f" • Exit Code:   {res.returncode}")
    print("═" * 58 + "\n")
    return {"command": command, "elapsed_sec": round(elapsed_sec, 4), "exit_code": res.returncode}
