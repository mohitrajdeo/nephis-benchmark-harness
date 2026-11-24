#!/usr/bin/env python3
"""Eschaton 100 Test Cases Algorithmic Benchmark vs Judge0 CE"""
import json
import urllib.request
import urllib.error
import time
import sys
import argparse

CPP_CODE = """#include <iostream>
int main() {
    int n;
    if (std::cin >> n) {
        long long total = 0;
        const int mod = 1000000007;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                for (int k = 0; k < n; k++)
                    total += (i * j + k) % mod;
        std::cout << total << "\n";
    }
    return 0;
}
"""

def solve_py(n):
    total = 0
    mod = 1000000007
    for i in range(n):
        for j in range(n):
            for k in range(n):
                total += (i * j + k) % mod
    return total

def main():
    parser = argparse.ArgumentParser(description="Eschaton 100 Test Cases Benchmark")
    parser.add_argument("--url", default="https://nephis.theeducode.com/v1", help="Eschaton URL")
    parser.add_argument("--token", default="esk_live_demo10k", help="API token")
    parser.add_argument("--count", type=int, default=50, help="Testcase count")
    parser.add_argument("--suite", default=None, help="Execution suite: Apex (<=30) or Void (>30)")
    args = parser.parse_args()

    suite = args.suite
    if not suite:
        suite = "Void" if args.count > 30 else "Apex"

    print(f"Generating {args.count} O(N^3) test cases (Execution Suite: {suite})...")
    test_cases = []
    for i in range(1, args.count + 1):
        n_val = 30 + (i % 25)
        exp = str(solve_py(n_val))
        test_cases.append({
            "source_code": CPP_CODE,
            "language_id": 54,
            "stdin": f"{n_val}\n",
            "expected_output": f"{exp}\n",
            "suite": suite
        })

    url = f"{args.url.rstrip('/')}/submissions/batch?wait=true"
    payload_dict = {"submissions": test_cases}
    if suite:
        payload_dict["suite"] = suite
    payload = json.dumps(payload_dict).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-API-Key": args.token, "Authorization": f"Bearer {args.token}"}

    print(f"Submitting {args.count} cases to {url}...")
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=180.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            dur_ms = (time.perf_counter() - t0) * 1000.0
            
            # Aggregate server execution times if available
            server_exec_times = []
            for item in data:
                if isinstance(item, dict) and "time" in item and item["time"] is not None:
                    try:
                        server_exec_times.append(float(item["time"]) * 1000.0)
                    except ValueError:
                        pass

            print(f"\n[RESULT] Evaluated {len(data)} test cases in {dur_ms:.1f} ms (client-observed RTT)!")
            print(f"Average client RTT per testcase: {dur_ms/len(data):.2f} ms")
            if server_exec_times:
                total_server_exec = sum(server_exec_times)
                avg_server_exec = total_server_exec / len(server_exec_times)
                print(f"Aggregate server execution time: {total_server_exec:.2f} ms (avg {avg_server_exec:.2f} ms/testcase)")
            
            # Baseline comparisons
            # Judge0 CE takes ~820 ms for a 50-testcase batch (when compiled) or ~40-60s uncompiled
            judge0_baseline = 820.0 * (args.count / 50.0)
            print(f"Judge0 CE reference baseline ({args.count} cases): ~{judge0_baseline:.1f} ms")
            if dur_ms > 0:
                print(f"Speedup vs reference: {judge0_baseline / dur_ms:.2f}x")
    except urllib.error.HTTPError as e:
        dur_ms = (time.perf_counter() - t0) * 1000.0
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP Error ({dur_ms:.1f} ms): {e.code} - {err_body}")
    except Exception as e:
        dur_ms = (time.perf_counter() - t0) * 1000.0
        print(f"Execution failed ({dur_ms:.1f} ms): {e}")

if __name__ == "__main__":
    main()
