import base64
import hashlib
import json
import os
import secrets
from typing import Dict, Optional


VAULT_DIR = os.path.expanduser("~/.config/aero")
VAULT_FILE = os.path.join(VAULT_DIR, "vault.enc")
KEY_FILE = os.path.join(VAULT_DIR, ".vault_key")


def _get_or_create_master_key() -> bytes:
    os.makedirs(VAULT_DIR, exist_ok=True)
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    
    # Generate 32-byte secure machine key
    key = secrets.token_bytes(32)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    os.chmod(KEY_FILE, 0o600)
    return key


def _xor_cipher(data: bytes, key: bytes) -> bytes:
    """Fast, self-contained XOR stream cipher with SHA-256 key schedule."""
    out = bytearray(len(data))
    key_stream = bytearray()
    counter = 0
    while len(key_stream) < len(data):
        h = hashlib.sha256(key + counter.to_bytes(4, "big")).digest()
        key_stream.extend(h)
        counter += 1
    
    for i in range(len(data)):
        out[i] = data[i] ^ key_stream[i]
    return bytes(out)


def _load_vault() -> Dict[str, str]:
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        key = _get_or_create_master_key()
        with open(VAULT_FILE, "rb") as f:
            encrypted = f.read()
        decrypted = _xor_cipher(encrypted, key)
        return json.loads(decrypted.decode("utf-8"))
    except Exception:
        return {}


def _save_vault(vault_data: Dict[str, str]):
    os.makedirs(VAULT_DIR, exist_ok=True)
    key = _get_or_create_master_key()
    raw = json.dumps(vault_data).encode("utf-8")
    encrypted = _xor_cipher(raw, key)
    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted)
    os.chmod(VAULT_FILE, 0o600)


def vault_set(key: str, value: str):
    data = _load_vault()
    data[key] = value
    _save_vault(data)
    print(f"🔒 Secret '{key}' safely stored in Aero Vault.")


def vault_get(key: str) -> Optional[str]:
    data = _load_vault()
    val = data.get(key)
    if val is not None:
        print(f"{val}")
    else:
        print(f"❌ Key '{key}' not found in Aero Vault.")
    return val


def vault_list():
    data = _load_vault()
    print("\n🔐 AERO SECURE DEVELOPER VAULT")
    print("═" * 54)
    if not data:
        print(" • (Vault is empty. Add keys with: aero vault set KEY VALUE)")
    else:
        for k in data.keys():
            masked = "•" * 12
            print(f" • {k:<25} ➔ {masked}")
    print("═" * 54 + "\n")


def vault_delete(key: str) -> bool:
    data = _load_vault()
    if key in data:
        del data[key]
        _save_vault(data)
        print(f"🗑️  Deleted '{key}' from Aero Vault.")
        return True
    print(f"❌ Key '{key}' not found.")
    return False


def vault_export_env():
    data = _load_vault()
    for k, v in data.items():
        print(f'export {k}="{v}"')
