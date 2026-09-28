import socket
import ssl
import time
from typing import Dict, Any


DNS_SERVERS = {
    "Cloudflare (1.1.1.1)": "1.1.1.1",
    "Google (8.8.8.8)": "8.8.8.8",
    "Quad9 (9.9.9.9)": "9.9.9.9",
    "OpenDNS (208.67.222.222)": "208.67.222.222",
}


def trace_tcp_tls_latency(host: str = "github.com", port: int = 443) -> Dict[str, Any]:
    print(f"\n⚡ Measuring network socket & TLS handshake latency to: {host}:{port}...")
    
    # 1. DNS Resolution Time
    t0 = time.perf_counter()
    try:
        ip = socket.gethostbyname(host)
        t_dns = (time.perf_counter() - t0) * 1000.0
    except Exception as e:
        print(f"❌ DNS Resolution failed: {e}")
        return {}

    # 2. TCP Connect (SYN-ACK) Time
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    t0 = time.perf_counter()
    try:
        sock.connect((ip, port))
        t_tcp = (time.perf_counter() - t0) * 1000.0
    except Exception as e:
        print(f"❌ TCP Connection failed: {e}")
        sock.close()
        return {}

    # 3. TLS Handshake Time (if port 443)
    t_tls = 0.0
    if port == 443:
        context = ssl.create_default_context()
        t0 = time.perf_counter()
        try:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                t_tls = (time.perf_counter() - t0) * 1000.0
                cipher = ssock.cipher()
                tls_version = ssock.version()
        except Exception as e:
            t_tls = -1.0
            cipher = ("N/A", "N/A", 0)
            tls_version = "N/A"
    else:
        sock.close()
        cipher = ("Plain TCP", "", 0)
        tls_version = "None"

    total_latency = t_dns + t_tcp + (t_tls if t_tls > 0 else 0)

    print("\n🌐 AERO NETWORK & TLS LATENCY TRACE")
    print("═" * 54)
    print(f" • Target Host:          {host} ({ip}:{port})")
    print(f" • DNS Lookup Latency:   {t_dns:.2f} ms")
    print(f" • TCP SYN-ACK Latency:  {t_tcp:.2f} ms")
    if port == 443:
        cipher_name = cipher[0] if cipher else "Unknown"
        print(f" • TLS Handshake Time:   {t_tls:.2f} ms ({tls_version}, {cipher_name})")
    print("─" * 54)
    print(f" • Total Time-to-First:  \033[1;32m{total_latency:.2f} ms\033[0m")
    print("═" * 54 + "\n")

    return {
        "host": host,
        "ip": ip,
        "dns_ms": round(t_dns, 2),
        "tcp_ms": round(t_tcp, 2),
        "tls_ms": round(t_tls, 2),
        "total_ms": round(total_latency, 2),
    }


def trace_dns_benchmark(domain: str = "google.com") -> Dict[str, float]:
    print(f"\n⚡ Benchmarking DNS lookup response times for '{domain}'...")
    results = {}
    for name, ip in DNS_SERVERS.items():
        t0 = time.perf_counter()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(2.0)
            sock.connect((ip, 53))
            elapsed = (time.perf_counter() - t0) * 1000.0
            sock.close()
            results[name] = round(elapsed, 2)
            print(f" • {name:<26}: \033[1;36m{elapsed:.2f} ms\033[0m")
        except Exception:
            results[name] = -1.0
            print(f" • {name:<26}: ❌ Timeout")
    return results
