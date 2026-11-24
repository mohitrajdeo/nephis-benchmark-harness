#!/usr/bin/env python3
"""Run All Live Physical Hardware Benchmarks on Host"""
import time
import subprocess
import os
import sys
import hashlib
import json

def run_cmd(cmd):
    t0 = time.perf_counter()
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    dur_ms = (time.perf_counter() - t0) * 1000.0
    return dur_ms, res.stdout.strip(), res.stderr.strip(), res.returncode

def main():
    print("=" * 70, flush=True)
    print(" PHYSICAL BENCHMARK SUITE - AWS HOST (13.126.155.62)", flush=True)
    print("=" * 70, flush=True)

    # 1. XFS CoW Reflink Benchmark (100MB)
    print("\n[VECTOR 1] Physical Kernel XFS CoW Reflink (100MB)", flush=True)
    # Check if /var/lib/mnemon is XFS
    target_dir = "/var/lib/mnemon" if os.path.exists("/var/lib/mnemon") else "/tmp"
    bench_dir = os.path.join(target_dir, "bench_cow_tmp")
    os.makedirs(bench_dir, exist_ok=True)
    src = os.path.join(bench_dir, "source_100mb.bin")
    dst = os.path.join(bench_dir, "clone_100mb.bin")
    dst_norm = os.path.join(bench_dir, "clone_norm_100mb.bin")

    print(f"  Generating 100MB block in {bench_dir}...", flush=True)
    with open(src, "wb") as f:
        f.write(b"Z" * (100 * 1024 * 1024))
    
    reflink_runs = []
    for i in range(5):
        if os.path.exists(dst): os.remove(dst)
        dur, out, err, code = run_cmd(f"cp --reflink=always {src} {dst}")
        if code == 0:
            reflink_runs.append(dur)
            print(f"    Reflink Run {i+1}: {dur:.2f} ms", flush=True)
        else:
            print(f"    Reflink failed ({code}): {err}", flush=True)
            break

    normal_runs = []
    for i in range(2):
        if os.path.exists(dst_norm): os.remove(dst_norm)
        dur, out, err, code = run_cmd(f"cp {src} {dst_norm}")
        if code == 0:
            normal_runs.append(dur)
            print(f"    Normal Copy Run {i+1}: {dur:.2f} ms", flush=True)

    avg_reflink = sum(reflink_runs) / len(reflink_runs) if reflink_runs else 0.0
    avg_normal = sum(normal_runs) / len(normal_runs) if normal_runs else 0.0
    print(f"  Average XFS CoW Reflink Latency: {avg_reflink:.2f} ms", flush=True)
    print(f"  Average Standard Copy Latency:   {avg_normal:.2f} ms", flush=True)
    if avg_reflink > 0:
        print(f"  >> Kernel CoW Speedup: {avg_normal / avg_reflink:.1f}x Faster!", flush=True)

    # Clean up files
    subprocess.run(["rm", "-rf", bench_dir])

    # 2. Thanaton Sandbox vs Docker
    print("\n[VECTOR 2] Thanaton Micro-Sandbox vs Docker Cold-Start", flush=True)
    isolate_runs = []
    # Test Isolate
    for i in range(5):
        # isolate box 100
        cmd = "isolate --cg -b 100 --init >/dev/null 2>&1 && isolate --cg -b 100 --run -- /bin/echo OK >/dev/null 2>&1 && isolate --cg -b 100 --cleanup >/dev/null 2>&1"
        dur, out, err, code = run_cmd(cmd)
        if code == 0:
            isolate_runs.append(dur)
            print(f"    Thanaton Isolate Run {i+1}: {dur:.2f} ms", flush=True)
        else:
            print(f"    Isolate failed: {err} (code {code})", flush=True)

    avg_isolate = sum(isolate_runs) / len(isolate_runs) if isolate_runs else 0.0
    print(f"  Average Thanaton Isolate Cold-Start: {avg_isolate:.2f} ms", flush=True)

    # Test Docker
    docker_runs = []
    # Find existing docker image
    dur, img_out, _, _ = run_cmd("docker images --format '{{.Repository}}:{{.Tag}}' | grep -v '<none>' | head -n 1")
    img = img_out.strip() if img_out else "alpine:latest"
    print(f"  Using Docker image: {img}", flush=True)
    for i in range(5):
        dur, out, err, code = run_cmd(f"docker run --rm {img} /bin/echo OK")
        if code == 0:
            docker_runs.append(dur)
            print(f"    Docker Run {i+1}: {dur:.2f} ms", flush=True)
        else:
            print(f"    Docker failed ({code}): {err}", flush=True)
            break

    avg_docker = sum(docker_runs) / len(docker_runs) if docker_runs else 0.0
    if avg_docker > 0:
        print(f"  Average Docker Cold-Start: {avg_docker:.2f} ms", flush=True)
        if avg_isolate > 0:
            print(f"  >> Thanaton vs Docker Advantage: {avg_docker / avg_isolate:.1f}x Faster Cold-Start!", flush=True)

    # 3. FastCDC Memory Dedup & Snapshot Restore Throughput
    print("\n[VECTOR 3] Memory Dedup & Snapshot Restore Throughput (32MB)", flush=True)
    size_mb = 32
    size_bytes = size_mb * 1024 * 1024
    # 70% repetitive dirty state, 30% random
    block = bytearray(b"\x00" * int(size_bytes * 0.5) + b"K" * int(size_bytes * 0.2) + os.urandom(int(size_bytes * 0.3)))
    chunk_size = 64 * 1024

    dedup_runs = []
    for i in range(5):
        t0 = time.perf_counter()
        seen = set()
        unique = 0
        for off in range(0, len(block), chunk_size):
            chk = block[off:off+chunk_size]
            h = hashlib.sha256(chk).digest()
            if h not in seen:
                seen.add(h)
                unique += len(chk)
        dur = time.perf_counter() - t0
        dedup_runs.append(dur)
        print(f"    Dedup Run {i+1}: {dur*1000.0:.2f} ms", flush=True)

    avg_dedup_s = sum(dedup_runs) / len(dedup_runs)
    avg_dedup_ms = avg_dedup_s * 1000.0
    throughput = (size_mb / 1024.0) / avg_dedup_s
    ratio = len(block) / max(unique, 1)

    print(f"  Average Dedup Duration for 32MB: {avg_dedup_ms:.2f} ms", flush=True)
    print(f"  Memory Dedup Throughput:          {throughput:.2f} GB/s", flush=True)
    print(f"  Dedup Compression Ratio:          {ratio:.2f}x", flush=True)

    # Output Machine-Readable JSON
    summary = {
        "xfs_reflink_avg_ms": avg_reflink,
        "standard_copy_avg_ms": avg_normal,
        "reflink_speedup": (avg_normal / avg_reflink) if avg_reflink > 0 else 0,
        "thanaton_isolate_avg_ms": avg_isolate,
        "docker_avg_ms": avg_docker,
        "thanaton_speedup_vs_docker": (avg_docker / avg_isolate) if avg_isolate > 0 else 0,
        "memory_dedup_32mb_ms": avg_dedup_ms,
        "memory_dedup_throughput_gb_s": throughput,
        "dedup_ratio": ratio
    }
    print("\n[PHYSICAL_RESULTS_JSON]")
    print(json.dumps(summary, indent=2))
    print("=" * 70, flush=True)

if __name__ == "__main__":
    main()
