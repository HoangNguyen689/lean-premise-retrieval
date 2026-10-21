"""Sinh toàn bộ biểu đồ từ raw results (yêu cầu môn: figure = script từ raw).

Các biểu đồ:
  1. scale_recall10.png       - Recall@10 của 4 hệ thống qua 3 mức corpus
  2. scale_mrr.png            - MRR qua 3 mức
  3. ablation_recall10.png    - (sinh bởi run_ablation.py, script này bỏ qua nếu có)
  4. comparison_n3_n4.png     - (sinh bởi run_comparison_n4.py)

Chạy:  python scripts/make_figures.py
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW = ROOT / "results" / "raw"
FIG = ROOT / "results" / "figures"

SCALE_LABEL = {"s1": "10K corpus", "s2": "50K corpus", "s3": "full (100K)"}
SYSTEMS = ["bm25", "bm25_fielddrop", "hybrid", "dense"]
COLORS = {"bm25": "#4C72B0", "bm25_fielddrop": "#C44E52",
          "hybrid": "#DD8452", "dense": "#55A868"}


def read_summary() -> dict:
    with open(RAW / "eval_summary.csv", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    data = defaultdict(dict)
    for r in rows:
        data[r["system"]][r["scale"]] = {k: float(v) for k, v in r.items()
                                         if k not in ("scale", "system", "owner")}
    return data


def main() -> int:
    if not (RAW / "eval_summary.csv").exists():
        print("Chạy trước: python scripts/run_all_evaluations.py")
        return 1
    data = read_summary()
    FIG.mkdir(parents=True, exist_ok=True)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    scales = ["s1", "s2", "s3"]
    for metric, fname in [
        ("Recall@10", "scale_recall10.png"),
        ("MRR", "scale_mrr.png"),
        ("Recall@50", "scale_recall50.png"),
    ]:
        title = metric
        fig, ax = plt.subplots(figsize=(7, 4.5))
        for system in SYSTEMS:
            ys = [data.get(system, {}).get(s, {}).get(metric, 0.0) for s in scales]
            ax.plot([SCALE_LABEL[s] for s in scales], ys, "o-",
                    label=system, color=COLORS[system])
        ax.set_ylabel(metric)
        ax.set_xlabel("Corpus size")
        ax.set_title(f"{metric} theo quy mô corpus (mock data, seed=42)")
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        path = FIG / fname
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"✓ {path.relative_to(ROOT)}")

    print("\nXong. Mọi biểu đồ sinh từ results/raw/eval_summary.csv bằng script.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
