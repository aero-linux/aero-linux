import json
import os
import shutil
import subprocess
import time
import urllib.request
from typing import Dict, Any


QUANT_BITS = {
    "fp16": 16.0,
    "q8_0": 8.5,
    "q6_k": 6.6,
    "q5_k_m": 5.5,
    "q4_k_m": 4.5,
    "q3_k_m": 3.4,
    "q2_k": 2.6,
}


def install_ollama() -> bool:
    if shutil.which("ollama"):
        return True

    print("🚀 Installing Ollama (high-performance local AI runtime)...")
    try:
        res = subprocess.run(
            "curl -fsSL https://ollama.com/install.sh | sh",
            shell=True,
            capture_output=True,
            text=True,
        )
        return res.returncode == 0 and shutil.which("ollama") is not None
    except Exception as e:
        print(f"Error installing Ollama: {e}")
        return False


def get_ai_status() -> dict:
    status = {
        "ollama_installed": shutil.which("ollama") is not None,
        "ollama_running": False,
        "models": [],
    }

    if status["ollama_installed"]:
        try:
            req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode())
                    status["ollama_running"] = True
                    status["models"] = [m.get("name") for m in data.get("models", [])]
        except Exception:
            pass

    return status


def pull_model(model_name: str) -> bool:
    if not shutil.which("ollama"):
        print("Ollama is not installed. Run 'aero ai init' first.")
        return False

    print(f"📥 Pulling AI model: {model_name}...")
    try:
        proc = subprocess.run(["ollama", "pull", model_name])
        return proc.returncode == 0
    except Exception as e:
        print(f"Failed to pull model: {e}")
        return False


def run_model(model_name: str):
    if not shutil.which("ollama"):
        print("Ollama is not installed. Run 'aero ai init' first.")
        return

    print(f"⚡ Launching interactive session with {model_name}...")
    subprocess.run(["ollama", "run", model_name])


def calc_model_memory(params_b: float, quant: str = "q4_k_m", context_len: int = 4096) -> Dict[str, Any]:
    """Calculates weight size, KV cache, and total RAM requirements for local LLM execution."""
    bits = QUANT_BITS.get(quant.lower(), 4.5)
    
    # Model weights size in GB
    weights_gb = (params_b * 10**9 * bits) / (8 * 1024**3)
    
    # Estimated KV Cache size (2 * layers * heads * dim * context_len * bytes) ~ roughly 0.5MB per 1k tokens for 7B/8B
    kv_cache_gb = (params_b / 8.0) * (context_len / 4096.0) * 0.5
    
    # Runtime context overhead (CUDA/ROCm/Vulkan activation buffers)
    overhead_gb = 0.8
    total_ram_needed_gb = round(weights_gb + kv_cache_gb + overhead_gb, 2)
    
    # Read physical host RAM
    total_phys_gb = 16.0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    total_phys_gb = round(int(line.split()[1]) / (1024 * 1024), 2)
                    break
    except Exception:
        pass
    
    fits_phys = total_ram_needed_gb <= (total_phys_gb - 1.0)
    # Effective RAM with 7.5GB zRAM ZSTD
    effective_ram_gb = total_phys_gb + 6.0
    fits_zram = total_ram_needed_gb <= (effective_ram_gb - 1.0)
    
    return {
        "params_b": params_b,
        "quant": quant,
        "weights_gb": round(weights_gb, 2),
        "kv_cache_gb": round(kv_cache_gb, 2),
        "total_needed_gb": total_ram_needed_gb,
        "host_ram_gb": total_phys_gb,
        "fits_physical_ram": fits_phys,
        "fits_with_aero_zram": fits_zram,
    }


def print_memory_calc(params_b: float, quant: str = "q4_k_m", context_len: int = 4096):
    res = calc_model_memory(params_b, quant, context_len)
    print("\n🧠 AERO AI MODEL MEMORY CALCULATOR")
    print("═" * 54)
    print(f" • Model Parameters:     {res['params_b']} Billion")
    print(f" • Quantization:         {res['quant']} ({QUANT_BITS.get(res['quant'].lower(), 4.5)} bits/weight)")
    print(f" • Context Window:       {context_len} tokens")
    print("─" * 54)
    print(f" • Model Weights Size:   {res['weights_gb']} GB")
    print(f" • KV Cache Buffer:      {res['kv_cache_gb']} GB")
    print(f" • Total RAM Required:   {res['total_needed_gb']} GB")
    print(f" • Host Physical RAM:    {res['host_ram_gb']} GB")
    print("─" * 54)
    if res['fits_physical_ram']:
        print(" • Physical RAM Status:  ✅ Fits directly in uncompressed RAM")
    elif res['fits_with_aero_zram']:
        print(" • Physical RAM Status:  ⚠️  Exceeds raw RAM, but ✅ FITS CLEANLY in Aero zRAM (ZSTD)")
    else:
        print(" • Physical RAM Status:  ❌ Model requires more RAM than available")
    print("═" * 54)


def benchmark_model_speed(model_name: str = "deepseek-r1:8b", prompt: str = "Explain the difference between zRAM and SSD swap in 50 words."):
    """Measures TTFT and tokens per second throughput."""
    if not shutil.which("ollama"):
        print("Ollama is not running. Start it with 'aero ai init'.")
        return None

    print(f"\n⚡ Benchmarking local inference speed for '{model_name}'...")
    req_data = json.dumps({
        "model": model_name,
        "prompt": prompt,
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=req_data, headers={"Content-Type": "application/json"})
    
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=60) as resp:
            t1 = time.time()
            data = json.loads(resp.read().decode())
            
            total_duration_ns = data.get("total_duration", (t1 - t0) * 1e9)
            eval_count = data.get("eval_count", 0)
            eval_duration_ns = data.get("eval_duration", 1)
            
            tok_per_sec = round((eval_count / (eval_duration_ns / 1e9)), 2) if eval_duration_ns > 0 else 0.0
            ttft_ms = round((data.get("prompt_eval_duration", 0) / 1e6), 2)
            
            print("═" * 54)
            print(f" • Model:                {model_name}")
            print(f" • Tokens Generated:     {eval_count} tokens")
            print(f" • Time to First Token:  {ttft_ms} ms")
            print(f" • Inference Throughput: {tok_per_sec} tokens/sec")
            print(f" • Total Latency:        {round(t1 - t0, 2)} seconds")
            print("═" * 54)
            return {"tokens_per_sec": tok_per_sec, "ttft_ms": ttft_ms, "eval_count": eval_count}
    except Exception as e:
        print(f"Benchmark error: {e}")
        return None
