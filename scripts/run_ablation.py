# -*- coding: utf-8 -*-
"""Ablation study — phân tích đóng góp của từng thành phần.

Câu hỏi ablation trả lời (theo hướng dẫn môn, mục 8 của Nhóm 3):
  - BM25 mặc định vs field-aware (thêm namespace/field weights)
  - Có / không tokenizer ký hiệu Lean
  - Có / không structural reranking

Mỗi cấu hình = một run file; script tính metrics và đo % chênh so với
phương pháp đầy đủ (hybrid) → bảng ablation results/raw/ablation_table.csv
+ biểu đồ results/figures/ablation_recall10.png.

Chạy:  python scripts/run_ablation.py
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
from run_logger import RunLogger  # noqa: E402

# Mỗi dòng = một cấu hình ablation: (tên cấu hình, thành phần bị bỏ, run file)
ABLATIONS = [
    ("full_hybrid",      "— (đầy đủ: sparse + ký hiệu + namespace + structural)", "hybrid"),
    ("no_structural",    "bỏ structural reranking (chỉ BM25 + field weights)",    "bm25"),
    ("no_lean_symbols",  "bỏ tokenizer ký hiệu Lean",                             "bm25_fielddrop"),
    ("baseline_only",    "baseline thuần: BM25 mặc định trên statement tách từ",  "bm25"),
]
SCALES = ["s1", "s2", "s3"]
METRIC = "Recall@10"


def main() -> int:
    if not (RAW / "eval_summary.csv").exists():
        print("Chưa có eval_summary.csv. Chạy trước: python scripts/run_all_evaluations.py")
        return 1

    # Đọc lại metrics từ eval_summary (đã tính bởi run_all_evaluations)
    with open(RAW / "eval_summary.csv", encoding="utf-8") as f:
        summary = {(r["scale"], r["system"]): {k: float(v) for k, v in r.items()
                   if k not in ("scale", "system", "owner")} for r in csv.DictReader(f)}

    rows, full_by_scale = [], {}
    for scale in SCALES:
        full = summary.get((scale, "hybrid"), {}).get(METRIC)
        full_by_scale[scale] = full
        for name, dropped, run_key in ABLATIONS:
            m = summary.get((scale, run_key))
            if m is None:
                continue
            delta = (m[METRIC] - full) if full is not None else 0.0
            rows.append([scale, name, dropped, f"{m[METRIC]:.4f}", f"{delta:+.4f}"])

    out = RAW / "ablation_table.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scale", "config", "component_removed", f"{METRIC}", f"delta_vs_full"])
        w.writerows(rows)
    print(f"Đã ghi {out.relative_to(ROOT)} ({len(rows)} dòng)\n")

    header = f"{'Scale':<6} {'Cấu hình':<18} {METRIC:>10} {'Δ vs full':>10}"
    print(header)
    print("-" * len(header))
    for r in rows:
        print(f"{r[0]:<6} {r[1]:<18} {r[3]:>10} {r[4]:>10}")

    # ── Biểu đồ sinh từ raw (bắt buộc của môn: figure = script từ raw results) ──
    FIG.mkdir(parents=True, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4.5))
    configs = [a[0] for a in ABLATIONS]
    width = 0.25
    xs = range(len(configs))
    for i, scale in enumerate(SCALES):
        vals = [next((float(r[3]) for r in rows if r[0] == scale and r[1] == c), 0.0)
                for c in configs]
        ax.bar([x + i * width for x in xs], vals, width, label=scale.upper())
    ax.set_xticks([x + width for x in xs])
    ax.set_xticklabels(["full\nhybrid", "no\nstructural", "no lean\nsymbols", "baseline\nonly"])
    ax.set_ylabel(METRIC)
    ax.set_title("Ablation — đóng góp từng thành phần (mock data, seed=42)")
    ax.legend(title="Scale")
    fig.tight_layout()
    fig_path = FIG / "ablation_recall10.png"
    fig.savefig(fig_path, dpi=150)
    print(f"\nĐã sinh biểu đồ {fig_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
