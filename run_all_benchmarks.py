#!/usr/bin/env python3
"""
NEPHIS Cloud: Master Benchmark & Stress Test Runner
Runs all independent product benchmark suites and outputs a consolidated report.
"""
import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SUITES_DIR = BASE_DIR / "suites"

def run_suite(suite_name, script_name):
    script_path = SUITES_DIR / suite_name / script_name
    print(f"\n{'='*75}")
    print(f" RUNNING BENCHMARK: [{suite_name.upper()}] {script_name}")
    print(f"{'='*75}")
    subprocess.run([sys.executable, str(script_path)])

def main():
    print("===========================================================================")
    print(" NEPHIS CLOUD: REPRODUCIBLE MULTI-ARCH BENCHMARK TESTBED")
    print("===========================================================================")

    suites = [
        ("eschaton", "benchmark_100_cases.py"),
        ("thanaton", "benchmark_thanaton_vs_docker.py"),
        ("mnemon_db", "benchmark_xfs_reflink.py"),
        ("acheron", "benchmark_ebpf_compression.py"),
        ("stress_and_chaos", "stress_50k_request_flood.py"),
    ]

    for suite, script in suites:
        run_suite(suite, script)

    print(f"\n{'='*75}")
    print(" ALL BENCHMARK SUITES COMPLETED SUCCESSFULLY!")
    print(" Full raw hardware receipts: results/live_test_receipts_master.json")
    print(f"{'='*75}")

if __name__ == "__main__":
    main()
