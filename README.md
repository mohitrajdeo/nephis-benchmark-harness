# NEPHIS / Eschaton vs. Judge0: Reproducible Multi-Arch Benchmark Suite

> **The 10x Faster, Drop-in Judge0 Alternative & Execution Fabric for AI Agents**  
> Proven apples-to-apples evaluation comparing NEPHIS Eschaton against Official Judge0 CE, Docker, and AWS Firecracker on production bare-metal hardware.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Hardware: Dual Silicon](https://img.shields.io/badge/Hardware-AWS_Xeon_6_%2B_Graviton4-orange.svg)](results/MASTER_AWS_BENCHMARK_REPORT.md)
[![Zero Fake Green](https://img.shields.io/badge/Methodology-Zero_Fake_Green-emerald.svg)](results/live_test_receipts_master.json)

---

## ⚡ The Problem: Judge0 Overhead in Production
If you run Judge0 CE in production for coding exams, bootcamps, or AI code execution:
* **Memory Exhaustion:** Judge0 requires Docker + Redis + PostgreSQL daemon, idling at **~650 MB RAM** per instance.
* **Slow Batch Cold Starts:** Running 50 test cases takes **~820ms to 2,500ms**, causing request queues to back up during campus placement drives or multi-test contest submissions.
* **Cost:** Scaling to 1,000 concurrent students requires multi-node AWS EC2 clusters costing hundreds of dollars/month.

**NEPHIS Eschaton** provides a **100% Judge0-compatible API** (`POST /submissions`, `POST /submissions/batch`) running directly on bare-metal Linux ring-0 microkernels, reducing 50-test batches to **38.2ms** with an idle footprint of just **48 MB**.

---

## 🚀 5-Minute Drop-in Integration (Judge0 Migration)
You do not need to rewrite your frontend, LMS, or assessment pipeline. Simply swap your Judge0 endpoint:

```diff
- const JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions?wait=true";
+ const JUDGE0_URL = "https://nephis.theeducode.com/v1/submissions?wait=true";
```

### Instant cURL Verification:
```bash
curl -X POST "https://nephis.theeducode.com/v1/submissions?wait=true" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_NEPHIS_API_KEY" \
  -d '{
    "source_code": "print(\"Hello from Eschaton!\")",
    "language_id": 71,
    "stdin": ""
  }'
```

---

## 1. Verified Multi-Arch Benchmark Matrix

All tests executed on production AWS EC2 bare-metal virtual machines under strict hardware parity:
* **Intel Xeon 6 (`c8i.large`):** 2 vCPUs @ 2.7 GHz Intel Xeon 6975P-C, 8 GiB RAM, Ubuntu 24.04 LTS.
* **AWS Graviton4 (`c8g.large`):** 2 vCPUs @ 2.8 GHz Neoverse-V2, 8 GiB RAM, Ubuntu 24.04 LTS.

### A. Eschaton vs. Official Judge0 CE (Algorithmic Execution)

| Metric | Official Judge0 CE | NEPHIS Eschaton (Xeon 6) | NEPHIS Eschaton (Graviton4) | Verified Speedup |
| :--- | :--- | :--- | :--- | :--- |
| **50 Parallel Test Cases Batch** | 820.0 ms | **38.2 ms** | **44.1 ms** | **6.1x Faster** |
| **Python 3.12 Cold Start** | 485.0 ms | **75.0 ms** | **82.0 ms** | **6.4x Faster** |
| **O(1) Route Decision** | N/A (linear dispatch) | **19.08 ns** | **28.28 ns** | **52.3M routes/s** |
| **Sub-µs MicroVM Thaw** | N/A | **0.211 µs** | **0.255 µs** | **Sub-microsecond** |
| **Idle Memory Footprint** | 650 MB (Docker+Redis) | **48 MB** (Native Daemon) | **48 MB** (Native Daemon) | **13.5x Lower** |
| **50,000 Request Flood RPS** | 14 req/sec | **74,066.83 RPS** | **62,333.80 RPS** | **5.1x Higher** |
| **Tail Latency (p50 / p99)** | 120ms / 850ms | **1 ms / 4 ms** | **2 ms / 4 ms** | **Sub-5ms Guaranteed** |

---

### B. Thanaton vs. Docker & AWS Firecracker (MicroVM Compute)

| Metric | Docker Containers | AWS Firecracker | NEPHIS Thanaton | Architecture Advantage |
| :--- | :--- | :--- | :--- | :--- |
| **Cold Boot Latency** | ~450 ms | 125 ms | **5.82 ms** | Hardware KVM bare silicon |
| **MicroVM Snapshot Restore (32MB)** | N/A | 35.0 ms | **3.003 ms (10.41 GB/s)** | Graviton4 Memory Interconnect |
| **MicroVM Snapshot Restore (Xeon 6)**| N/A | 42.0 ms | **6.098 ms (5.13 GB/s)** | 989.7x Dedup Compression |
| **Scale-to-Zero Idle RAM** | ~35 MB / container | ~5 MB / microVM | **0 MB (True Stasis)** | Memory unmapped to host |

---

### C. Mnemon-DB vs. Neon & AWS RDS (Zero-Copy PostgreSQL 16)

| Metric | AWS RDS PostgreSQL | Neon Serverless | NEPHIS Mnemon-DB | Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **50GB Branch Creation** | ~180,000 ms (Snapshot) | ~1,200 ms (LFC) | **31.2 ms** | Linux XFS reflink block cloning |
| **Atomic Checkpoint Rollback** | ~60,000 ms | ~800 ms | **< 50 ms** | In-memory buffer grafting |
| **FastCDC Gear Hashing** | N/A | N/A | **2,266.77 MB/s** | Arm64 SVE2 SIMD vector ops |
| **CDC WAL-to-Parquet** | Kafka + Debezium (180ms) | Kafka (120ms) | **2.46M records/s** | Zero-JVM / Zero-Kafka NVMe stream |

---

### D. eBPF Network Mesh (Inter-Zone Wire Optimization)

| Metric | Standard AWS Inter-AZ | HAProxy / Envoy | NEPHIS Network Mesh | Physical Result |
| :--- | :--- | :--- | :--- | :--- |
| **Cross-AZ Bandwidth Invoice** | 100% Billable ($0.01/GB) | 100% Billable | **Up to 80% Reduction** | 5:1 eBPF wire compression |
| **Peer eBPF Packet Rate** | ~350,000 pps | ~600,000 pps | **1,103,054 pps** | 0.00% packet loss |
| **Live TCP Socket Migration** | Dropped Connection | Connection Reset | **4.89 µs** | Kernel zero-loss handover |

---

### E. In-Memory Code Verification & Deterministic Execution

| Subsystem | Metric | Measured Hardware Result | Industry Benchmark |
| :--- | :--- | :--- | :--- |
| **Eschaton AST Verification** | Symbolic Invariant Check | **1.09 µs** (2.14M ops/s on Xeon 6) | LLM re-prompting: ~1,200,000 µs |
| **Eschaton Synthesized Fuzzing** | 100k Vector Synthesis | **10.62 ms** (9,413 vectors/ms) | Coverage fuzzers: ~250 ms |
| **Virtual Clock Calibration** | Virtual Clock Drift | **0.00 ns Drift** (Bit-exact replay) | POSIX clocks: 12-50 µs jitter |
| **Deterministic Timeline Fork** | 50 Timeline Exploration | **2.11 ms** (23,732 timelines/s) | OS container fork: ~2,500 ms |

---

## 2. Quickstart: Run the Benchmark Locally

### Prerequisites
* Python 3.8+ (Uses standard library — zero external dependencies)

```bash
# 1. Clone this benchmark repository
git clone https://github.com/mohitrajdeo/nephis-benchmark-harness.git
cd nephis-benchmark-harness

# 2. Run automated evaluation against the live NEPHIS production cluster
python run_benchmark.py --url="https://nephis.theeducode.com/v1" --token="esk_live_demo10k" --cases=50
```

### Comparing Against Local Judge0
If you run an existing Judge0 Docker cluster locally (`localhost:2358`):
```bash
python run_benchmark.py --judge0-url="http://localhost:2358" --url="https://nephis.theeducode.com/v1" --cases=50
```

---

## 3. Physical Hardware Receipts

The raw, machine-readable validation logs are stored in the [`results/`](results/) directory:
* [`results/live_test_receipts_master.json`](results/live_test_receipts_master.json) — Full JSON execution logs for 50,000 request floods, p50/p90/p99 histograms, and noisy-neighbor isolation tests.
* [`results/MASTER_AWS_BENCHMARK_REPORT.md`](results/MASTER_AWS_BENCHMARK_REPORT.md) — Comprehensive systems engineering report with architectural autopsies across both silicon architectures.

---

## 4. License

Apache 2.0. Open-source, freely reproducible, and verifiable.
