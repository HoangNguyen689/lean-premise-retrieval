"""Chạy 4 hệ retrieval thật trên 3 scale → run file + metrics + latency.

Một lệnh thay thế toàn bộ mock: đọc results/real/{corpus,queries,qrels}_{scale}.csv,
chạy bm25 / bm25_fielddrop / bm25_field / hybrid, ghi:
  results/real/run_{system}_{scale}.csv   (run file chuẩn: query_id, premise_id)
  results/real/eval_summary.csv           (metrics thật)
  results/real/latency_{scale}.csv        (P50/P95 ms mỗi hệ - đo thật)
  results/raw/eval_summary_real.csv       (bản tổng hợp cho các script TV6 cũ)

Chạy:  python scripts/run_real_retrieval.py
"""
from __future__ import annotations

import csv
import sys
import time
from pathlib import Path

# Windows console (CMD) thường dùng cp1252/cp437 - không chứa chữ tiếng Việt.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

ROOT = Path(__file__).parent.parent
REAL = ROOT / "results" / "real"
sys.path.insert(0, str(ROOT / "src" / "retrieval"))
sys.path.insert(0, str(ROOT / "src" / "evaluation"))

from systems import RetrievalSystem  # noqa: E402  # type: ignore[import]
from metrics import evaluate_from_files  # noqa: E402  # type: ignore[import]
from run_logger import RunLogger  # noqa: E402  # type: ignore[import]

SCALES = ["s1", "s2", "s3"]
SYSTEMS = ["bm25", "bm25_fielddrop", "bm25_field", "hybrid"]
DATA_VERSION = "leandojo-benchmark-4@29dcec07+split-v1.0"


def load_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def percentile(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    idx = min(int(len(s) * p / 100), len(s) - 1)
    return s[idx]


def main() -> int:
    summary_rows, latency_rows = [], []
    for scale in SCALES:
        corpus = load_csv(REAL / f"corpus_{scale}.csv")
        queries = load_csv(REAL / f"queries_{scale}.csv")
        print(f"\n=== {scale.upper()}: corpus {len(corpus)}, queries {len(queries)} ===")

        for sys_name in SYSTEMS:
            log = RunLogger(
                parameters={"system": sys_name, "scale": scale, "top_k": 50,
                            "k1": 1.5, "b": 0.75},
                seed=42, data_version=DATA_VERSION,
            )
            try:
                t0 = time.time()
                system = RetrievalSystem(sys_name, corpus)
                build_s = time.time() - t0

                # latency đo trên từng query (đơn lẻ)
                lat_ms, run_rows = [], []
                for q in queries:
                    t1 = time.perf_counter()
                    ranked = system.search(q, top_k=50)
                    lat_ms.append((time.perf_counter() - t1) * 1000)
                    run_rows.extend([q["id"], pid] for pid in ranked)

                run_path = REAL / f"run_{sys_name}_{scale}.csv"
                with open(run_path, "w", encoding="utf-8", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["query_id", "premise_id"])
                    w.writerows(run_rows)

                metrics = evaluate_from_files(REAL / f"qrels_{scale}.csv", run_path)
                log.finish(metrics={**metrics,
                                    "index_build_s": round(build_s, 3),
                                    "p50_ms": round(percentile(lat_ms, 50), 3),
                                    "p95_ms": round(percentile(lat_ms, 95), 3),
                                    "qps_1client": round(1000 / (sum(lat_ms) / len(lat_ms)), 1)},
                           artifacts=[str(run_path.relative_to(ROOT))])

                summary_rows.append([scale, sys_name, "N3"] +
                                    [f"{metrics[k]:.4f}" for k in
                                     ["Recall@1", "Recall@5", "Recall@10", "Recall@50",
                                      "MRR", "nDCG@10"]])
                latency_rows.append([scale, sys_name, round(build_s, 2),
                                     round(percentile(lat_ms, 50), 2),
                                     round(percentile(lat_ms, 95), 2),
                                     round(1000 / (sum(lat_ms) / len(lat_ms)), 1)])
                pretty = ", ".join(f"{k}={v:.4f}" for k, v in metrics.items())
                print(f"✓ {sys_name:<15} build {build_s:5.1f}s  "
                      f"P50={percentile(lat_ms, 50):6.2f}ms P95={percentile(lat_ms, 95):7.2f}ms")
                print(f"  {pretty}")
            except Exception as exc:  # noqa: BLE001
                log.fail(error=str(exc))
                print(f"✗ {sys_name}: {exc}")
                raise

    # eval_summary (dùng bởi run_ablation/run_comparison/make_figures hiện có)
    with open(REAL / "eval_summary.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scale", "system", "owner", "Recall@1", "Recall@5",
                    "Recall@10", "Recall@50", "MRR", "nDCG@10"])
        w.writerows(summary_rows)
    with open(REAL / "latency.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scale", "system", "index_build_s", "p50_ms", "p95_ms", "qps_1client"])
        w.writerows(latency_rows)

    # copy eval_summary sang results/raw để các script TV6 cũ chạy tiếp không sửa gì
    (ROOT / "results" / "raw" / "eval_summary.csv").write_text(
        (REAL / "eval_summary.csv").read_text(encoding="utf-8"), encoding="utf-8")

    print(f"\nĐã ghi: {REAL / 'eval_summary.csv'}, {REAL / 'latency.csv'} "
          f"+ 12 run files + 12 run logs JSON")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
