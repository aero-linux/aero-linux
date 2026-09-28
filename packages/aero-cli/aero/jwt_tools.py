import base64
import datetime
import json
from typing import Dict, Any


def b64_encode_str(text: str) -> str:
    res = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    print(res)
    return res


def b64_decode_str(encoded: str) -> str:
    # Add padding if needed
    rem = len(encoded) % 4
    if rem > 0:
        encoded += "=" * (4 - rem)
    res = base64.b64decode(encoded.encode("utf-8")).decode("utf-8", errors="ignore")
    print(res)
    return res


def decode_jwt_token(token: str) -> Dict[str, Any]:
    parts = token.strip().split(".")
    if len(parts) < 2:
        print("❌ Invalid JWT token structure (must have at least header and payload).")
        return {}

    def decode_segment(seg: str) -> Dict[str, Any]:
        rem = len(seg) % 4
        if rem > 0:
            seg += "=" * (4 - rem)
        decoded = base64.urlsafe_b64decode(seg.encode("utf-8")).decode("utf-8", errors="ignore")
        return json.loads(decoded)

    try:
        header = decode_segment(parts[0])
        payload = decode_segment(parts[1])
    except Exception as e:
        print(f"❌ Failed to decode JWT payload: {e}")
        return {}

    print("\n🔑 \033[1;36mAERO SECURE LOCAL JWT DECODER\033[0m")
    print("═" * 56)
    print("• Header:")
    print(json.dumps(header, indent=2))
    print("\n• Payload Claims:")
    print(json.dumps(payload, indent=2))

    if "exp" in payload and isinstance(payload["exp"], (int, float)):
        exp_dt = datetime.datetime.fromtimestamp(payload["exp"])
        is_expired = datetime.datetime.now() > exp_dt
        status = "\033[1;31m(EXPIRED)\033[0m" if is_expired else "\033[1;32m(VALID)\033[0m"
        print(f"\n• Expiration: {exp_dt} {status}")
    print("═" * 56 + "\n")

    return {"header": header, "payload": payload}
