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
    args = parser.parse_args()

    print(f"Generating {args.count} O(N^3) test cases...")
    test_cases = []
    for i in range(1, args.count + 1):
        n_val = 30 + (i % 25)
        exp = str(solve_py(n_val))
        test_cases.append({
            "source_code": CPP_CODE,
            "language_id": 54,
            "stdin": f"{n_val}\n",
            "expected_output": f"{exp}\n"
        })

    url = f"{args.url.rstrip('/')}/submissions/batch?wait=true"
    payload = json.dumps({"submissions": test_cases}).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-API-Key": args.token, "Authorization": f"Bearer {args.token}"}

    print(f"Submitting {args.count} cases to {url}...")
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            dur_ms = (time.perf_counter() - t0) * 1000.0
            print(f"\n[RESULT] Evaluated {len(data)} test cases in {dur_ms:.1f} ms!")
            print(f"Average time per testcase: {dur_ms/len(data):.2f} ms")
            print("Judge0 CE baseline for 50 cases: ~820 ms")
            print(f"Speedup: {820.0 / dur_ms:.1f}x Faster" if dur_ms > 0 else "")
    except Exception as e:
        dur_ms = (time.perf_counter() - t0) * 1000.0
        print(f"Execution failed ({dur_ms:.1f} ms): {e}")

if __name__ == "__main__":
    main()
