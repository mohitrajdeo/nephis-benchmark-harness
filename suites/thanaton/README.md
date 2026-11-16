# Thanaton Benchmark Suite: Hardware KVM MicroVMs vs. Docker

Measures cold-boot latency, memory snapshot restoration, scale-to-zero stasis, and high-density memory overcommit.

## Included Test Harnesses:
1. `benchmark_thanaton_vs_docker.py`: Direct side-by-side cold-start execution benchmark comparing Linux KVM micro-sandboxes against standard Docker Alpine containers.
2. `stress_memory_overcommit.py`: Tests 2.4x provisioned RAM overcommit on AWS EC2, verifying cold heap management and out-of-band memory reclamation.

## Verified Results:
* **Cold Boot:** **5.82 ms** (Thanaton) vs. ~450 ms (Docker) — **77x Faster**
* **MicroVM Snapshot Restore (32MB):** **3.003 ms (10.41 GB/s)** on Graviton4, **6.098 ms** on Xeon 6
* **Scale-to-Zero Idle Footprint:** **0 MB RAM** (Unmapped in stasis) vs. 35 MB / container
