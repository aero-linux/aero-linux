import urllib.request
import time
import concurrent.futures


def bench_url(url: str, requests_count: int = 100, concurrency: int = 10):
    print(f"⚡ \033[1;36mAERO API & HTTP LOAD BENCHMARK\033[0m")
    print("═" * 55)
    print(f" • Target URL:   \033[1;33m{url}\033[0m")
    print(f" • Total Req:    {requests_count}")
    print(f" • Concurrency:  {concurrency}\n")

    latencies = []
    errors = 0

    def make_req():
        nonlocal errors
        start = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AeroBench/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                resp.read(1024)
            lat = (time.time() - start) * 1000.0  # ms
            latencies.append(lat)
        except Exception:
            errors += 1

    total_start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(make_req) for _ in range(requests_count)]
        concurrent.futures.wait(futures)
    total_time = time.time() - total_start

    successful = len(latencies)
    rps = successful / total_time if total_time > 0 else 0
    avg_lat = sum(latencies) / len(latencies) if latencies else 0
    latencies.sort()
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0
    p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0

    print("📊 Benchmark Results:")
    print(f" • Completed In:    \033[33m{total_time:.3f}s\033[0m")
    print(f" • Throughput:      \033[1;32m{rps:.1f} req/sec\033[0m")
    print(f" • Avg Latency:     {avg_lat:.2f} ms")
    print(f" • P95 Latency:     {p95:.2f} ms")
    print(f" • P99 Latency:     {p99:.2f} ms")
    print(f" • Failed Requests: {'0' if errors == 0 else f'\033[31m{errors}\033[0m'}")
    print()
