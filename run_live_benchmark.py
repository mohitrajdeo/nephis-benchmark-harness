#!/usr/bin/env python3
"""Measure live cloud endpoints with real account keys and write raw results.

No hardcoded baselines. Every number below is measured on the run.
"""
import json
import os
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://nephis.theeducode.com"
MNEMON_KEY = os.environ.get("NEPHIS_API_KEY", "")
THANATON_KEY = os.environ.get("THANATON_API_KEY", "")
TENANT = os.environ.get("MNEMON_TENANT", "b7de0a5a-3e48-41eb-afc2-f62d5d4483b1")
UA = "nephis-benchmark-harness/1.0"

if not MNEMON_KEY or not THANATON_KEY:
    print("NEPHIS_API_KEY and THANATON_API_KEY must be set", file=sys.stderr)
    sys.exit(1)


def call(path, key, method="GET", body=None, samples=1):
    headers = {"Accept": "application/json", "User-Agent": UA}
    if key:
        headers["X-API-Key"] = key
        headers["Authorization"] = f"Bearer {key}"
    if body is not None:
        headers["Content-Type"] = "application/json"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    timings = []
    last_body = None
    status = None
    for _ in range(samples):
        req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                raw = resp.read().decode("utf-8", "replace")
                status = resp.status
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace")
            status = exc.code
        except Exception as exc:
            raw = json.dumps({"error": str(exc)})
            status = "ERR"
        timings.append((time.perf_counter() - t0) * 1000.0)
        last_body = raw[:4000]
    ordered = sorted(timings)
    return {
        "endpoint": path,
        "method": method,
        "samples": samples,
        "status": status,
        "latency_ms": {
            "min": round(ordered[0], 2),
            "p50": round(statistics.median(ordered), 2),
            "p95": round(ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))], 2),
            "max": round(ordered[-1], 2),
        },
        "response_excerpt": last_body,
    }


def main():
    started = datetime.now(timezone.utc).isoformat()
    results = {
        "run_at": started,
        "target": BASE,
        "source": "live cloud, real account keys",
        "tenant": TENANT,
        "measurements": [],
    }

    checks = [
        ("mnemon metrics catalog", "/v1/metrics/catalog", MNEMON_KEY, "GET", None, 1),
        ("thanaton fleet metrics", "/api/v1/metrics/fleet/overview", THANATON_KEY, "GET", None, 1),
        ("account", "/v1/account", MNEMON_KEY, "GET", None, 1),
        ("branch inventory", f"/v1/tenants/branches?tenant={TENANT}", MNEMON_KEY, "GET", None, 1),
        ("tenant telemetry", "/v1/status", MNEMON_KEY, "GET", None, 1),
        ("sql select 1", f"/v1/databases/{TENANT}/sql", MNEMON_KEY, "POST", {"query": "SELECT 1 AS probe"}, 1),
    ]

    for label, path, key, method, body, n in checks:
        m = call(path, key, method, body, n)
        m["label"] = label
        results["measurements"].append(m)
        print(f"{label:28s} {str(m['status']):4s} p50={m['latency_ms']['p50']:8.2f} ms  p95={m['latency_ms']['p95']:8.2f} ms")

    out = Path(__file__).resolve().parent / "results" / "live_benchmark.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
