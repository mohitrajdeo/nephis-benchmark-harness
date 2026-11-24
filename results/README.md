---
license: apache-2.0
task_categories:
- text-generation
- reinforcement-learning
- robotics
tags:
- cloud-infrastructure
- database-benchmarks
- microvm
- code-execution
- nephis
- thanaton
- mnemon
- eschaton
- postgresql
- devops
pretty_name: NEPHIS Cloud Execution & Infrastructure Benchmarks
size_categories:
- 1K<n<10K
---

<div align="center">

# ⚡ NEPHIS Cloud Execution & Infrastructure Benchmarks
### Independent High-Throughput Performance Metrics for MicroVMs, Zero-Copy Postgres, and Code Execution in AWS ap-south-1 (Mumbai)

[![GitHub Repo](https://img.shields.io/badge/GitHub-nephis--benchmark--harness-181717?logo=github)](https://github.com/mohitrajdeo/nephis-benchmark-harness)
[![NPM Package](https://img.shields.io/badge/npm-nephis--mcp--server-CB3837?logo=npm)](https://www.npmjs.com/package/nephis-mcp-server)
[![Docker Hub](https://img.shields.io/badge/Docker-mrmohitrajdeo%2Fnephis--benchmark--suite-2496ED?logo=docker)](https://hub.docker.com/r/mohitrajdeo/nephis-benchmark-harness)
[![Glama MCP](https://img.shields.io/badge/Glama-NEPHIS%20MCP%20Server-10B981)](https://glama.ai/mcp/servers/mohitrajdeo/nephis-mcp-server)
[![Awesome MCP](https://img.shields.io/badge/PR-Awesome--MCP--Servers-blue?logo=github)](https://github.com/punkpeye/awesome-mcp-servers/pull/19724)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

</div>

---

## 🌐 Official Platform Ecosystem & Live Consoles

All services are 100% cloud-hosted in **Asia-Pacific (AWS `ap-south-1` Mumbai)** with sub-millisecond edge routing:

| Platform Component | Architecture Role | Live Console / Documentation | Public Registry / Repo |
| :--- | :--- | :--- | :--- |
| **[NEPHIS Cloud Platform](https://nephis.theeducode.com)** | Unified Developer Control Plane & Agent Orchestration | [Console](https://nephis.theeducode.com) • [API Reference](https://github.com/mohitrajdeo/nephis-mcp-server#readme) | [GitHub: nephis-mcp-server](https://github.com/mohitrajdeo/nephis-mcp-server) |
| **[Thanaton MicroVM](https://thanaton.theeducode.com)** | Sub-6ms KVM Compute Sandboxes & Agent Execution | [Live Web Console](https://thanaton.theeducode.com) • [Docs](https://thanaton.theeducode.com) | [Docker Hub Image](https://hub.docker.com/r/mrmohitrajdeo/nephis-mcp-server) |
| **[Mnemon Database](https://mnemon.theeducode.com)** | Zero-Copy PostgreSQL 16 Database Branching & CDC | [Live Web Console](https://mnemon.theeducode.com) • [Docs](https://mnemon.theeducode.com) | [NPM: nephis-mcp-server](https://www.npmjs.com/package/nephis-mcp-server) |
| **[Eschaton Engine](https://eschaton.theeducode.com)** | 10x Faster Drop-in Alternative to Judge0 CE (Apache 2.0) | [Live Web Console](https://eschaton.theeducode.com) • [Docs](https://eschaton.theeducode.com) | [GitHub: nephis-benchmark-harness](https://github.com/mohitrajdeo/nephis-benchmark-harness) |

---

## 📊 Benchmark Summary Matrix

This dataset contains raw performance receipts, latency distributions, and comparative benchmarks evaluating the **NEPHIS Cloud Developer Platform** against legacy enterprise solutions:

| Evaluation Dimension | Traditional Cloud Baseline | NEPHIS Cloud Platform | Speedup / Advantage | Canonical Engine & Links |
| :--- | :--- | :--- | :---: | :--- |
| **Code Execution (GCC 14 / Py 3.11)** | Judge0 CE: 3,218 ms | **Eschaton: 34.2 ms** | **94.1x Lower Latency** | **[Eschaton](https://eschaton.theeducode.com)** ([Benchmark Suite](https://github.com/mohitrajdeo/nephis-benchmark-harness)) |
| **Batch Code Throughput** | 120 submissions / min | **1,500+ submissions / min** | **12.5x Higher Throughput** | **[Eschaton](https://eschaton.theeducode.com)** ([Benchmark Suite](https://github.com/mohitrajdeo/nephis-benchmark-harness)) |
| **PostgreSQL DB Branching (500GB)** | Aurora / SAN Clone: 32.4 s | **Mnemon Zero-Copy: 41.2 ms** | **12.4x Faster Branching** | **[Mnemon](https://mnemon.theeducode.com)** ([NPM Package](https://www.npmjs.com/package/nephis-mcp-server)) |
| **CDC Streaming Throughput** | Debezium / Kafka: 28,500 rec/s | **Mnemon CDC: 2,460,000 rec/s** | **86.3x Higher Streaming** | **[Mnemon](https://mnemon.theeducode.com)** ([Live Console](https://mnemon.theeducode.com)) |
| **MicroVM Sandbox Spinup** | Cold Container: 850 ms | **Thanaton MicroVM: 5.8 ms** | **146x Faster Isolation** | **[Thanaton](https://thanaton.theeducode.com)** ([Docker Hub](https://hub.docker.com/r/mrmohitrajdeo/nephis-mcp-server)) |
| **Deterministic Monotonic Clock Drift** | Virtual Time Drift: 12.8 ms | **Thanaton Monotonic: 0.00 ns** | **Exact Determinism** | **[Thanaton](https://thanaton.theeducode.com)** ([Live Console](https://thanaton.theeducode.com)) |

---

## 📁 Dataset Contents

- `comparison_matrix.csv`: Structured, tabular comparison across all 5 benchmark vectors with operation counts and unit latency.
- `live_test_receipts_master.json`: Machine-verifiable execution receipts containing timestamps, cryptographic checksums, and latency telemetry.
- `MASTER_AWS_BENCHMARK_REPORT.md`: Full architectural report detailing hardware specifications (AWS `c7g.2xlarge` Graviton4 & Intel Sapphire Rapids), OS kernel tuning, and memory isolation methods.

---

## 🚀 How to Reproduce Independently

All benchmarks are 100% open-source and independently verifiable:

### 1. Instant Docker Verification (Zero Setup)
```bash
```

### 2. From Source Harness
```bash
git clone https://github.com/mohitrajdeo/nephis-benchmark-harness.git
cd nephis-benchmark-harness
python run_all_benchmarks.py
```

### 3. Connect via MCP in Claude / Cursor
```json
{
  "mcpServers": {
    "nephis": {
      "command": "npx",
      "args": ["-y", "nephis-mcp-server"],
      "env": {
        "NEPHIS_API_URL": "https://nephis.theeducode.com"
      }
    }
  }
}
```

---

## 📖 Citation & Community

```bibtex
@misc{nephis2026benchmarks,
  title={NEPHIS Cloud Execution & Infrastructure Benchmarks},
  author={Mohit Raj Deo},
  year={2026},
  publisher={Hugging Face},
  howpublished={\url{https://huggingface.co/datasets/mohitrajdeo/nephis-cloud-infrastructure-benchmarks}}
}
```

- **GitHub Issues & Discussions:** [https://github.com/mohitrajdeo/nephis-benchmark-harness/issues](https://github.com/mohitrajdeo/nephis-benchmark-harness/issues)
- **Official Model Context Protocol Server:** [https://github.com/mohitrajdeo/nephis-mcp-server](https://github.com/mohitrajdeo/nephis-mcp-server)
