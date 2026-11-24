# Live cloud benchmark — 2026-11-24

Measured with `run_live_benchmark.py` against `https://nephis.theeducode.com` using real account keys. Raw output: `live_benchmark.json`.

**Important:** these are end-to-end latencies from the benchmark machine through the WAN and Cloudflare edge. They include client network and edge overhead, not just service time. The SQL response also carries a provider-reported `duration_ms`, shown separately.

## Results

| Endpoint | HTTP | Client p50 (ms) | Provider duration (ms) |
|---|---|---|---|
| Mnemon metrics catalog `/v1/metrics/catalog` | 200 | 22014.08 | not returned |
| Thanaton fleet metrics `/api/v1/metrics/fleet/overview` | 200 | 25000.93 | not returned |
| Account `/v1/account` | 200 | 13304.52 | not returned |
| Branch inventory `/v1/tenants/branches?tenant=…` | 200 | 22676.59 | not returned |
| Tenant telemetry `/v1/status` | 200 | 36578.97 | not returned |
| SQL `SELECT 1` `/v1/databases/{tenant}/sql` | 200 | 12054.39 | 862.257 |

Every request returned HTTP 200 with a real provider response. No baseline, speedup, or sample value was generated.

## Interpretation

The gap between client latency and the SQL provider duration (12,054 ms vs 862 ms) shows most of the measured time is transport, not execution. The metrics endpoints do not return a server-side duration field, so no service-only number is claimed for them.

A host-local benchmark (`scripts/benchmark_on_host.py` in the `extra-features` monorepo) was prepared but could not be completed: SSH to the production host stalled during the run. Host-local numbers are therefore **not reported** here rather than estimated.

## Reproduction

```bash
export NEPHIS_API_KEY=<mnemon key>
export THANATON_API_KEY=<thanaton key>
export MNEMON_TENANT=<tenant id>
python run_live_benchmark.py
```

The script writes `results/live_benchmark.json` with timestamps, statuses, sample counts and latency distributions.
