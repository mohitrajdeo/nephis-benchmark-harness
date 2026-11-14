#!/usr/bin/env python3
"""Eschaton Node.js 22 JIT Execution & Memory Benchmark"""
import json
import urllib.request
import time
import argparse

JS_CODE = """const fs = require('fs');
const input = fs.readFileSync(0, 'utf-8').trim().split(/\s+/);
if (input.length > 0 && input[0] !== '') {
    const n = parseInt(input[0], 10);
    let sum = 0n;
    for (let i = 1; i <= n; i++) sum += BigInt(input[i]);
    console.log(sum.toString());
}
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://nephis.theeducode.com/v1")
    parser.add_argument("--token", default="esk_live_demo10k")
    args = parser.parse_args()

    data = "1000 " + " ".join(str(i) for i in range(1000))
    payload = json.dumps({"source_code": JS_CODE, "language_id": 63, "stdin": data}).encode("utf-8")
    headers = {"Content-Type": "application/json", "X-API-Key": args.token, "Authorization": f"Bearer {args.token}"}

    print(f"Evaluating Node.js 22 BigInt calculation (1,000 integers) at {args.url}...")
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(f"{args.url.rstrip('/')}/submissions?wait=true", data=payload, headers=headers)
        with urllib.request.urlopen(req, timeout=10.0) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            dur_ms = (time.perf_counter() - t0) * 1000.0
            print(f"Execution succeeded in {dur_ms:.1f} ms! Server status: {res.get('status', {}).get('description')}")
    except Exception as e:
        print(f"Evaluation error: {e}")

if __name__ == "__main__":
    main()
