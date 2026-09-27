import time
import os
import tempfile
import multiprocessing


def cpu_worker(n):
    count = 0
    for i in range(1, n):
        count += i * i
    return count


def run_benchmark():
    print("⚡ \033[1;36mAERO DEVELOPER HARDWARE BENCHMARK\033[0m")
    print("═" * 55)

    # 1. CPU Multi-Core Benchmark
    print("⚙️  Benchmarking CPU Multi-Core Performance...")
    num_cores = multiprocessing.cpu_count()
    iterations = 3_000_000
    start_time = time.time()

    with multiprocessing.Pool(processes=num_cores) as pool:
        pool.map(cpu_worker, [iterations] * num_cores)

    cpu_time = time.time() - start_time
    cpu_score = int(10_000 / cpu_time) if cpu_time > 0 else 0
    print(f"   • Completed in: \033[33m{cpu_time:.3f}s\033[0m across {num_cores} cores")
    print(f"   • CPU Index Score: \033[1;32m{cpu_score}\033[0m")

    # 2. RAM Memory Bandwidth Benchmark
    print("\n🧠 Benchmarking RAM Memory Bandwidth...")
    block_size = 50 * 1024 * 1024  # 50 MB
    start_mem = time.time()
    data = bytearray(block_size)
    for _ in range(10):
        data[:] = b"0" * block_size
    mem_time = time.time() - start_mem
    mb_processed = (block_size * 10) / (1024 * 1024)
    mem_speed = mb_processed / mem_time if mem_time > 0 else 0
    print(f"   • Memory Throughput: \033[1;32m{mem_speed:.1f} MB/s\033[0m")

    # 3. Disk Write Speed Benchmark
    print("\n💾 Benchmarking Storage I/O Speed...")
    try:
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            disk_block = b"1" * (1024 * 1024)  # 1MB
            start_disk = time.time()
            for _ in range(100):  # 100MB
                tmp.write(disk_block)
            tmp.flush()
            os.fsync(tmp.fileno())
            disk_time = time.time() - start_disk
            disk_speed = 100 / disk_time if disk_time > 0 else 0
            print(f"   • Sequential Write: \033[1;32m{disk_speed:.1f} MB/s\033[0m (Time: {disk_time:.3f}s)")
    except Exception as e:
        print(f"   • Disk Test Skipped: {e}")

    print("\n" + "═" * 55)
    print("✅ Benchmark complete. High scores correlate with lower build & inference times.")
