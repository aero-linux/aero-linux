import hashlib
import os
import secrets
import string
import uuid
from typing import Dict, Any


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
    h = hashlib.new(algo.lower())
    if os.path.exists(target):
        with open(target, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
    else:
        h.update(target.encode("utf-8"))
    
    digest = h.hexdigest()
    print(f"\033[1;32m{algo.upper()}:\033[0m {digest}")
    return digest
