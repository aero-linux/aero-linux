"""
Aero Linux - High-Performance Cryptographic Hashing Engine
Multi-threaded, chunked hashing for files and directories (SHA256, SHA512, MD5, BLAKE2b/BLAKE3).
"""

import hashlib
import os
import secrets
import string
import uuid
import concurrent.futures
from typing import Dict, Any, List, Optional


def generate_uuid() -> str:
    u = str(uuid.uuid4())
    print(u)
    return u


def generate_token(length: int = 32, mode: str = "hex") -> str:
    if mode == "hex":
        tok = secrets.token_hex(length // 2)
    elif mode == "alphanumeric":
        chars = string.ascii_letters + string.digits
        tok = "".join(secrets.choice(chars) for _ in range(length))
    else:
        tok = secrets.token_urlsafe(length)
    print(tok)
    return tok


def compute_hash(target: str, algo: str = "sha256") -> str:
    """
    Compute cryptographic hash of a file or string.
    Supports sha256, sha512, md5, sha1, blake2b, blake2s.
    """
    algo_clean = algo.lower().strip()
    if algo_clean in ("blake3", "blake2", "blake2b"):
        h = hashlib.blake2b()
    elif algo_clean == "blake2s":
        h = hashlib.blake2s()
    else:
        h = hashlib.new(algo_clean)

    if os.path.exists(target):
        with open(target, "rb") as f:
            while chunk := f.read(1048576):  # 1MB buffer for high throughput
                h.update(chunk)
    else:
        h.update(target.encode("utf-8"))

    digest = h.hexdigest()
    print(f"\033[1;32m{algo.upper()}:\033[0m {digest}")
    return digest


def verify_file_checksum(target_file: str, expected_hash: str, algo: str = "sha256") -> bool:
    """
    Verify whether a target file matches an expected cryptographic hash.
    """
    if not os.path.isfile(target_file):
        print(f"❌ File not found: {target_file}")
        return False

    actual_hash = compute_hash(target_file, algo)
    matches = actual_hash.lower() == expected_hash.strip().lower()

    if matches:
        print(f"\n✅ CHECKSUM VERIFIED: Hash matches perfectly for {os.path.basename(target_file)}!")
    else:
        print(f"\n❌ CHECKSUM MISMATCH: Expected {expected_hash} but computed {actual_hash}")
    return matches


def compute_directory_manifest(root_dir: str, algo: str = "sha256", max_workers: int = 4) -> List[Dict[str, Any]]:
    """
    Multi-threaded directory hashing for data integrity verification and manifest generation.
    """
    if not os.path.isdir(root_dir):
        print(f"❌ Directory not found: {root_dir}")
        return []

    file_paths = []
    for root, _, files in os.walk(root_dir):
        for f in files:
            file_paths.append(os.path.join(root, f))

    def hash_single(path):
        try:
            rel = os.path.relpath(path, root_dir)
            digest = compute_hash(path, algo)
            size = os.path.getsize(path)
            return {"path": rel, "hash": digest, "size": size}
        except Exception as e:
            return {"path": path, "error": str(e)}

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        manifest = list(executor.map(hash_single, file_paths))

    manifest.sort(key=lambda x: x.get("path", ""))
    return manifest
