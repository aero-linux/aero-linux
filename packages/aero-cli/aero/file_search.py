import fnmatch
import os
import re
from typing import List, Dict, Any

IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".cache", "target", "build", "dist", ".venv", "venv"}


def search_files_by_name(pattern: str, root_dir: str = ".") -> List[str]:
    root_dir = os.path.abspath(root_dir)
    matches = []
    print(f"🔍 \033[1;36mSEARCHING FILES: {pattern}\033[0m")
    print("═" * 55)

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if fnmatch.fnmatch(f.lower(), pattern.lower()):
                full_p = os.path.join(root, f)
                rel_p = os.path.relpath(full_p, root_dir)
                matches.append(rel_p)
                if len(matches) <= 25:
                    print(f" 📄 {rel_p}")

    if len(matches) > 25:
        print(f" ... and {len(matches) - 25} more files.")
    print(f"\n✔ Found \033[1;32m{len(matches)}\033[0m matching file(s).\n")
    return matches


def search_text_content(query: str, root_dir: str = ".", max_matches: int = 30) -> List[Dict[str, Any]]:
    root_dir = os.path.abspath(root_dir)
    results = []
    print(f"🔎 \033[1;36mSEARCHING TEXT CONTENT: '{query}'\033[0m")
    print("═" * 55)

    regex = re.compile(re.escape(query), re.IGNORECASE)

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            full_p = os.path.join(root, file)
            # Skip binary files & large files > 2MB
            try:
                if os.path.getsize(full_p) > 2 * 1024 * 1024:
                    continue
                with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
                    for line_num, line in enumerate(f, start=1):
                        if regex.search(line):
                            rel_p = os.path.relpath(full_p, root_dir)
                            results.append({
                                "file": rel_p,
                                "line": line_num,
                                "text": line.strip()
                            })
                            if len(results) <= max_matches:
                                print(f" \033[1;34m{rel_p}:{line_num}\033[0m ➔ {line.strip()[:80]}")
                            if len(results) >= max_matches:
                                break
            except Exception:
                pass
        if len(results) >= max_matches:
            break

    print(f"\n✔ Found \033[1;32m{len(results)}\033[0m match(es).\n")
    return results
