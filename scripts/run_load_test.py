# -*- coding: utf-8 -*-
"""Load test — 1/10/50 truy vấn đồng thời trên hệ hybrid (tuần 7, mức tải).

Đo QPS và P50/P95 latency khi nhiều client gọi search song song.
Dùng ThreadPoolExecutor để mô phỏng đồng thời; index build 1 lần, share readonly
— đúng kịch bản serving thật (index dùng chung, request song song).

Chạy:  python scripts/run_load_test.py
"""
from __future__ import annotations

import csv
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Windows console (CMD) thường dùng cp1252/cp437 — không chứa chữ tiếng Việt.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
REAL = ROOT / "results" / "real"
sys.path.insert(0, str(ROOT / "src" / "retrieval"))
sys.path.insert(0, str(ROOT / "src" / "evaluation"))

from systems import RetrievalSystem  # noqa: E402
from run_logger import RunLogger  # noqa: E402

DATA_VERSION = "leandojo-benchmark-4@29dcec07+split-v1.0"
SCALE = "s2"  # load test trên 50K corpus (đại diện; s3 quá nặng cho máy cá nhân)
CONCURRENCY = [1, 10, 50]
N_REQUESTS = 200  # số request mỗi mức


def percentile(vals: list[float], p: float) -> float:
    s = sorted(vals)
    return s[min(int(len(s) * p / 100), len(s) - 1)]


def main() -> int:
    random.seed(42)
    corpus = list(csv.DictReader(open(REAL / f"corpus_{SCALE}.csv", encoding="utf-8")))
    queries = list(csv.DictReader(open(REAL / f"queries_{SCALE}.csv", encoding="utf-8")))
    system = RetrievalSystem("hybrid", corpus)
    print(f"Load test trên hybrid/{SCALE.upper()} — {len(corpus)} declarations, "
          f"{len(queries)} queries pool")

    rows = []
    for conc in CONCURRENCY:
        qids = [random.choice(queries) for _ in range(N_REQUESTS)]
        log = RunLogger(
            parameters={"system": "hybrid", "scale": SCALE, "concurrency": conc,
                        "n_requests": N_REQUESTS},
            seed=42, data_version=DATA_VERSION,
        )
        t0 = time.perf_counter()
        lat_ms: list[float] = []

        from concurrent.futures import ThreadPoolExecutor
        def worker(q):
            t1 = time.perf_counter()
            system.search(q, top_k=50)
            return (time.perf_counter() - t1) * 1000

        with ThreadPoolExecutor(max_workers=conc) as ex:
            lat_ms = list(ex.map(worker, qids))
        wall = time.perf_counter() - t0

        qps = N_REQUESTS / wall
        p50, p95 = percentile(lat_ms, 50), percentile(lat_ms, 95)
        log.finish(metrics={"qps": round(qps, 2), "p50_ms": round(p50, 2),
                            "p95_ms": round(p95, 2),
                            "mean_ms": round(sum(lat_ms) / len(lat_ms), 2)},
                   artifacts=["results/real/load_test.csv"])
        rows.append([SCALE, conc, N_REQUESTS, round(qps, 2), round(p50, 2), round(p95, 2)])
        print(f"  {conc:>3} client đồng thời: QPS={qps:8.2f}  P50={p50:8.2f}ms  "
              f"P95={p95:8.2f}ms")

    out = REAL / "load_test.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scale", "concurrency", "n_requests", "qps", "p50_ms", "p95_ms"])
        w.writerows(rows)
    print(f"\nĐã ghi {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
