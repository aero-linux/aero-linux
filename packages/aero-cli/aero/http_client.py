import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any


def http_request(url: str, method: str = "GET", data_str: str = "", headers_dict: Dict[str, str] | None = None) -> Dict[str, Any]:
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    headers = headers_dict or {}
    if "User-Agent" not in headers:
        headers["User-Agent"] = "Aero-HTTP-Client/1.0"

    print(f"\n📡 \033[1;36mAERO HTTP CLIENT\033[0m")
    print("═" * 60)
    print(f" • Request: \033[1;32m{method.upper()}\033[0m {url}")

    req_data = data_str.encode("utf-8") if data_str else None
    if req_data and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=req_data, headers=headers, method=method.upper())

    t0 = time.perf_counter()
    status_code = 0
    resp_headers = {}
    body_text = ""

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            status_code = resp.status
            resp_headers = dict(resp.getheaders())
            body_bytes = resp.read()
            body_text = body_bytes.decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        status_code = e.code
        resp_headers = dict(e.headers)
        body_text = e.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("═" * 60 + "\n")
        return {"error": str(e)}

    status_color = "\033[1;32m" if 200 <= status_code < 300 else "\033[1;31m"
    print(f" • Status:  {status_color}{status_code}\033[0m (Latency: \033[1;36m{elapsed_ms:.2f} ms\033[0m)")
    print("─" * 60)
    print("Response Headers:")
    for k, v in list(resp_headers.items())[:6]:
        print(f"  {k}: {v}")
    print("─" * 60)
    print("Response Body:")
    try:
        parsed = json.loads(body_text)
        print(json.dumps(parsed, indent=2)[:1500])
    except Exception:
        print(body_text[:1500])
    print("═" * 60 + "\n")

    return {
        "status": status_code,
        "latency_ms": round(elapsed_ms, 2),
        "headers": resp_headers,
        "body": body_text,
    }
