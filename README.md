# CIEL Sovereign Fabric: Reproducible Benchmark Harness

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://www.python.org/)
[![Reproducible](https://img.shields.io/badge/Benchmarks-Independently_Verifiable-purple.svg)](run_benchmark.py)

An open-source, independently verifiable benchmark suite comparing **CIEL Sovereign Fabric (Eschaton)** against **Official Judge0 CE** across real-world algorithmic workloads.

---

## 1. Test Methodology & Hardware Declaration

To eliminate vendor bias, all tests are executed under strict parity:
* **Hardware Baseline:** AWS EC2 `c8i.large` Virtual Machine (2 vCPUs @ 2.7 GHz Intel Xeon 6975P-C, 4 GiB Memory, Ubuntu 24.04 LTS).
* **Workload:** 50 distinct test cases for array aggregation and algorithmic evaluation.
* **Compression & Serialization:** Identical block compression and JSON formatting.
* **Cold vs. Warm:** Separate metrics for cold sandbox initialization vs. warm parallel worker evaluation.

---

## 2. Quickstart: Run the Benchmark in 10 Seconds

### Prerequisites
* Python 3.8+ (No external pip dependencies required — uses standard library)

```bash
# 1. Clone the repository
git clone https://github.com/MOHITRAJDEO12345/ciel-benchmark-harness.git
cd ciel-benchmark-harness

# 2. Run the automated benchmark against the live CIEL cluster
python run_benchmark.py
```

### Comparing Against Your Own Local Judge0 Instance
If you run an existing Judge0 Docker cluster locally (`localhost:2358`):
```bash
python run_benchmark.py --judge0-url="http://localhost:2358" --ciel-url="https://ciel.theeducode.com/v1" --cases=50
```

---

## 3. Verified Performance Results (AWS EC2 c8i.large)

| Workload Metric | Official Judge0 CE | CIEL Sovereign Fabric | Verified Improvement |
| :--- | :--- | :--- | :--- |
| **Python Cold Start** | ~485 ms | **~75 ms** | **6.4x Faster** |
| **C++ 50 Test Cases Batch** | ~820 ms | **~135 ms** | **6.1x Faster** |
| **Python 50 Test Cases Batch** | ~940 ms | **~155 ms** | **6.0x Faster** |
| **Memory Footprint (Idle)** | 650 MB (Docker+Redis) | **48 MB (Native Daemon)** | **13.5x Lower** |
| **Throughput Density (2 vCPU)** | 14 req/sec | **72 req/sec** | **5.1x Higher** |

---

## 4. Why CIEL Outperforms Docker Virtualization

1. **Lock-Free Process Dispatcher:** CIEL eliminates container cold-start fork/exec latency by maintaining pre-warmed, cgroup-isolated worker pools in memory.
2. **Zero-Copy Shared-Memory IPC:** Test inputs and standard output/error buffers are mapped directly into worker memory via shared memory pages, bypassing socket serialization bottlenecks.
3. **RAM Binary Cache:** Pre-compiled C++, C, and Java binaries are cached in RAM (`/dev/shm`), dropping repeat compilation from 200ms to 0.1ms.
4. **100% Judge0 Drop-In Parity:** Fully compatible with `/submissions` and `/submissions/batch` endpoints.

---

## 5. Live Production Receipts & API Reference

- **Live Production API Docs:** [https://compiler.theeducode.com/api](https://compiler.theeducode.com/api)
- **Interactive Web Playground:** [https://ciel.theeducode.com/alpha-test.html](https://ciel.theeducode.com/alpha-test.html)
- **Architecture & Technical FAQs:** [https://ciel.theeducode.com/](https://ciel.theeducode.com/)

---

## 6. License

Apache 2.0. Open-source and freely reproducible.
