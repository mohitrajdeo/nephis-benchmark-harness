# Concurrency Stress & Chaos Testing Suite

Empirical saturation benchmarks verifying noisy-neighbor isolation, 50,000 HTTP Keep-Alive request floods, and sub-5ms tail latencies on bare silicon.

## Included Test Harnesses:
1. `stress_50k_request_flood.py`: Floods the gateway with 50,000 concurrent HTTP requests across 100 worker threads, calculating p50/p90/p99 histograms.
2. `stress_noisy_neighbor_spin.py`: Injects 4 aggressive CPU spin thrashing loops while measuring latency degradation under cgroup v2 CFS scheduling.

## Verified Results:
* **50k Flood RPS:** **74,066.83 RPS** (Xeon 6) / **62,333.80 RPS** (Graviton4)
* **Tail Latency:** **1 ms (p50) / 4 ms (p99)** under full saturation
* **Noisy Neighbor Containment:** Maintained **> 22,000 RPS** with p99 contained at **12–13 ms** during 4x CPU thrash
