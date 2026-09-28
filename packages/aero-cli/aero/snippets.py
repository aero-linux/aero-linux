import json
import os
from typing import Dict, Any


DEFAULT_SNIPPETS: Dict[str, Dict[str, str]] = {
    "docker-prune": {
        "desc": "Deep purge of all stopped containers, unused images, and build caches",
        "cmd": "docker system prune -a --volumes -f",
        "category": "Docker",
    },
    "git-undo-commit": {
        "desc": "Undo last git commit while keeping all changes staged",
        "cmd": "git reset --soft HEAD~1",
        "category": "Git",
    },
    "git-discard-all": {
        "desc": "Hard reset workspace and remove all untracked files",
        "cmd": "git reset --hard HEAD && git clean -fd",
        "category": "Git",
    },
    "port-find": {
        "desc": "Find PID and process holding a specific network port",
        "cmd": "lsof -i :3000",
        "category": "Networking",
    },
    "extract-tar": {
        "desc": "Extract gzip compressed tarball archive to current folder",
        "cmd": "tar -xzf archive.tar.gz",
        "category": "Archiving",
    },
    "generate-sha256": {
        "desc": "Compute cryptographic SHA256 checksum of a file",
        "cmd": "sha256sum filename.iso",
        "category": "Security",
    },
    "ffmpeg-compress": {
        "desc": "Transcode video to efficient H.265 / HEVC MP4 format",
        "cmd": "ffmpeg -i input.mp4 -vcodec libx265 -crf 28 output.mp4",
        "category": "Media",
    },
}


def list_snippets(filter_cat: str = ""):
    print("\n⚡ \033[1;36mAERO DEVELOPER COMMAND SNIPPET VAULT\033[0m")
    print("═" * 68)
    print(f" {'KEY':<18} {'CATEGORY':<14} {'DESCRIPTION'}")
    print("─" * 68)

    for k, v in DEFAULT_SNIPPETS.items():
        if filter_cat and filter_cat.lower() not in v["category"].lower():
            continue
        print(f" \033[1;33m{k:<18}\033[0m {v['category']:<14} {v['desc']}")
        print(f"   \033[1;30m$ {v['cmd']}\033[0m")
    print("═" * 68 + "\n")


def search_snippets(query: str):
    q = query.lower()
    matches = {k: v for k, v in DEFAULT_SNIPPETS.items() if q in k or q in v["desc"].lower() or q in v["cmd"].lower()}
    print(f"\n🔍 Matching snippets for: '{query}' ({len(matches)} found)")
    print("═" * 68)
    for k, v in matches.items():
        print(f" • \033[1;32m{k}\033[0m: {v['desc']}")
        print(f"   \033[1;36m{v['cmd']}\033[0m")
    print("═" * 68 + "\n")
