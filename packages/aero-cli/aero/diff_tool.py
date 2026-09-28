import difflib
import os
from typing import Dict, Any


def show_file_diff(file_a: str, file_b: str) -> Dict[str, Any]:
    if not os.path.exists(file_a):
        print(f"❌ File not found: {file_a}")
        return {"error": "file_a_missing"}
    if not os.path.exists(file_b):
        print(f"❌ File not found: {file_b}")
        return {"error": "file_b_missing"}

    with open(file_a, "r", errors="ignore") as fa:
        lines_a = fa.readlines()
    with open(file_b, "r", errors="ignore") as fb:
        lines_b = fb.readlines()

    diff = list(difflib.unified_diff(lines_a, lines_b, fromfile=file_a, tofile=file_b))

    print(f"\n📊 \033[1;36mAERO CODE & FILE DIFF INSPECTOR\033[0m")
    print("═" * 60)
    
    if not diff:
        print("\033[1;32m✔ Files are 100% identical (0 differences).\033[0m")
        print("═" * 60 + "\n")
        return {"identical": True, "additions": 0, "deletions": 0}

    adds = 0
    dels = 0
    for line in diff:
        line_str = line.rstrip("\n")
        if line_str.startswith("+++") or line_str.startswith("---"):
            print(f"\033[1;37m{line_str}\033[0m")
        elif line_str.startswith("@@"):
            print(f"\033[1;36m{line_str}\033[0m")
        elif line_str.startswith("+"):
            adds += 1
            print(f"\033[1;32m{line_str}\033[0m")
        elif line_str.startswith("-"):
            dels += 1
            print(f"\033[1;31m{line_str}\033[0m")
        else:
            print(f" {line_str}")

    print("─" * 60)
    print(f"Summary: \033[1;32m+{adds} additions\033[0m, \033[1;31m-{dels} deletions\033[0m")
    print("═" * 60 + "\n")
    return {"identical": False, "additions": adds, "deletions": dels}
