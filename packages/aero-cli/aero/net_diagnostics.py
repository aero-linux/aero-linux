import os
import shutil
import socket
import subprocess
import time
from typing import Dict, Any, List


def dns_dig(domain: str) -> Dict[str, Any]:
    print(f"\n🔍 \033[1;36mAERO DNS RECORDS INSPECTOR (DIG)\033[0m")
    print("═" * 58)
    print(f" • Domain: \033[1;32m{domain}\033[0m")
    print("─" * 58)

    records = {"A": [], "AAAA": []}
    try:
        addr_info = socket.getaddrinfo(domain, None)
        for item in addr_info:
            family, _, _, _, sockaddr = item
            ip = sockaddr[0]
            if family == socket.AF_INET and ip not in records["A"]:
                records["A"].append(ip)
            elif family == socket.AF_INET6 and ip not in records["AAAA"]:
                records["AAAA"].append(ip)
    except Exception as e:
        print(f"❌ DNS resolution failed: {e}")
        return {}

    for ip in records["A"]:
        print(f" • [A Record]    {ip}")
    for ip in records["AAAA"]:
        print(f" • [AAAA Record] {ip}")
    print("═" * 58 + "\n")
    return records


def ping_host(host: str, count: int = 4) -> Dict[str, Any]:
    print(f"\n⚡ \033[1;36mAERO HIGH-PRECISION PING LATENCY PROFILER\033[0m")
    print("═" * 58)
    print(f" • Target Host: \033[1;32m{host}\033[0m ({count} packets)")
    print("─" * 58)

    latencies = []
    for seq in range(1, count + 1):
        t0 = time.perf_counter()
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2.0)
            sock.connect((host, 80 if not host.startswith("http") else 443))
            elapsed = (time.perf_counter() - t0) * 1000.0
            sock.close()
            latencies.append(elapsed)
            print(f" ➔ seq={seq} host={host} latency=\033[1;32m{elapsed:.2f} ms\033[0m")
        except Exception:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
            print(f" ➔ seq={seq} host={host} \033[1;31mRequest Timed Out\033[0m")
        time.sleep(0.1)

    print("─" * 58)
    if latencies:
        avg_lat = sum(latencies) / len(latencies)
        min_lat = min(latencies)
        max_lat = max(latencies)
        loss = round((1 - len(latencies) / count) * 100, 1)
        print(f" Packet Loss: {loss}% | Min: \033[1;32m{min_lat:.2f}ms\033[0m | Avg: \033[1;36m{avg_lat:.2f}ms\033[0m | Max: \033[1;33m{max_lat:.2f}ms\033[0m")
    else:
        print("❌ 100% Packet Loss (Host unreachable)")
    print("═" * 58 + "\n")

    return {"host": host, "latencies": latencies}
