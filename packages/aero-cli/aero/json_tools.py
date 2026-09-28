import json
import os
import sys
from typing import Any, Optional


def load_json_data(target: str) -> Any:
    if os.path.exists(target):
        with open(target, "r", errors="ignore") as f:
            return json.load(f)
    return json.loads(target)


def format_json_str(target: str, indent: int = 2) -> str:
    data = load_json_data(target)
    formatted = json.dumps(data, indent=indent)
    print(formatted)
    return formatted


def minify_json_str(target: str) -> str:
    data = load_json_data(target)
    minified = json.dumps(data, separators=(",", ":"))
    print(minified)
    return minified


def query_json_path(target: str, path: str) -> Any:
    data = load_json_data(target)
    parts = path.split(".")
    cur = data
    for p in parts:
        if isinstance(cur, dict):
            cur = cur.get(p)
        elif isinstance(cur, list) and p.isdigit():
            idx = int(p)
            if 0 <= idx < len(cur):
                cur = cur[idx]
            else:
                cur = None
        else:
            cur = None
        if cur is None:
            break
    print(json.dumps(cur, indent=2) if isinstance(cur, (dict, list)) else cur)
    return cur
