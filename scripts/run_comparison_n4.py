# -*- coding: utf-8 -*-
"""Comparison Nhóm 3 (sparse/hybrid) vs Nhóm 4 (dense/ANN) — nhiệm vụ tuần 9.

Đọc eval_summary.csv (N3 tự tính) + run_dense_*.csv (N4 giao, theo data contract
§7) và sinh:
  - results/raw/comparison_table.csv  — bảng so sánh trên cùng split
  - results/figures/comparison_recall10_by_scale.png — biểu đồ cột theo scale
  - results/figures/comparison_tradeoff.png — trade-off chất lượng (x) vs chi phí (y)

Quy tắc công bằng (theo data contract §6): cùng split, cùng qrels, cùng quy ước
Recall (nhãn 2), cùng phần cứng. Nếu N4 chưa giao run file thật → dùng run file
mock có nhãn `mock: yes` trong kết quả và cảnh báo rõ trong báo cáo.

Chạy:  python scripts/run_comparison_n4.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW = ROOT / "results" / "raw"
FIG = ROOT / "results" / "figures"
sys.path.insert(0, str(ROOT / "src" / "evaluation"))

from metrics import evaluate_from_files  # noqa: E402

SCALES = ["s1", "s2", "s3"]
SCALE_LABEL = {"s1": "10K", "s2": "50K", "s3": "full (100K)"}
N3_SYSTEMS = ["bm25", "hybrid"]
N4_SYSTEMS = ["dense"]  # Nhóm 4: exact cosine và ANN — mock 1 cột, thay khi N4 giao thật

# Chi phí mô phỏng (index size MB, build time s, P95 ms) — thay bằng đo thật tuần 7.
# Đây là chỗ duy nhất TV5 phải cập nhật số liệu thật; đánh giá chất lượng không phụ thuộc.
COST_MOCK = {
    "s1": {"bm25": (2.1, 4.2, 1.8), "hybrid": (2.4, 5.1, 2.3), "dense": (12.8, 38.0, 6.5)},
    "s2": {"bm25": (10.4, 22.0, 2.0), "hybrid": (11.9, 26.4, 3.1), "dense": (63.9, 196.0, 8.9)},
    "s3": {"bm25": (21.2, 45.3, 2.9), "hybrid": (24.1, 54.0, 4.0), "dense": (127.8, 402.0, 12.4)},
}


def load_metrics() -> dict[tuple[str, str], dict[str, float]]:
    with open(RAW / "eval_summary.csv", encoding="utf-8") as f:
        return {(r["scale"], r["system"]): {k: float(v) for k, v in r.items()
                if k not in ("scale", "system", "owner")} for r in csv.DictReader(f)}


def main() -> int:
    if not (RAW / "eval_summary.csv").exists():
        print("Chạy trước: python scripts/run_all_evaluations.py")
        return 1
    metrics = load_metrics()

    # Nếu N4 giao run file thật (run_dense_real_*.csv) → dùng thay mock
    dense_source = "mock (N4 chưa giao run thật — đánh dấu trong báo cáo)"
    for scale in SCALES:
        real = RAW / f"run_dense_real_{scale}.csv"
        if real.exists():
            m = evaluate_from_files(RAW / f"qrels_{scale}.csv", real)
            metrics[("s1" if scale == "s1" else scale, "dense")] = m
            dense_source = f"run_dense_real_*.csv do N4 giao"

    rows = []
    for scale in SCALES:
        for system in N3_SYSTEMS + N4_SYSTEMS:
            m = metrics.get((scale, system))
            if m is None:
                continue
            owner = "N4" if system in N4_SYSTEMS else "N3"
            cost = COST_MOCK[scale][system]
            rows.append([scale, SCALE_LABEL[scale], system, owner,
                         f"{m['Recall@10']:.4f}", f"{m['MRR']:.4f}",
                         f"{cost[2]:.1f}", f"{cost[0]:.1f}", f"{cost[1]:.1f}"])

    out = RAW / "comparison_table.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scale", "corpus_size", "system", "owner", "Recall@10", "MRR",
                    "p95_ms", "index_mb", "build_s"])
        w.writerows(rows)
    print(f"Đã ghi {out.relative_to(ROOT)} — nguồn dense: {dense_source}\n")

    hdr = f"{'Scale':<14} {'Hệ thống':<10} {'Owner':<5} {'Recall@10':>10} {'MRR':>8} {'P95 ms':>8}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r[1]:<14} {r[2]:<10} {r[3]:>4}   {r[4]:>8} {r[5]:>8} {r[6]:>8}")

    # ── Biểu đồ từ raw ──
    FIG.mkdir(parents=True, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    systems = N3_SYSTEMS + N4_SYSTEMS
    colors = {"bm25": "#4C72B0", "hybrid": "#DD8452", "dense": "#55A868"}
    width = 0.8 / len(systems)
    xs = range(len(SCALES))
    for i, system in enumerate(systems):
        vals = [next((float(r[4]) for r in rows if r[0] == s and r[2] == system), 0.0)
                for s in SCALES]
        ax1.bar([x + i * width / len(systems) for x in xs], vals,
                width / len(systems), label=system, color=colors[system])
    ax1.set_xticks([x + 0.5 * width / 2 for x in xs])
    ax1.set_xticklabels([SCALE_LABEL[s] for s in SCALES])
    ax1.set_ylabel("Recall@10")
    ax1.set_title("Chất lượng theo scale (cùng split N3×N4)")
    ax1.legend()

    for system in systems:
        pts = [(float(r[6]), float(r[4])) for r in rows if r[2] == system]
        pts.sort()
        ax2.plot([p[0] for p in pts], [p[1] for p in pts], "o-",
                 label=system, color=colors[system])
    ax2.set_xlabel("P95 latency (ms)")
    ax2.set_ylabel("Recall@10")
    ax2.set_title("Trade-off chất lượng ↔ độ trễ (mỗi điểm = 1 scale)")
    ax2.legend()

    fig.tight_layout()
    fig_path = FIG / "comparison_n3_n4.png"
    fig.savefig(fig_path, dpi=150)
    print(f"\nĐã sinh biểu đồ {fig_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
