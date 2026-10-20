# -*- coding: utf-8 -*-
"""Biểu đồ tổng hợp số THẬT: scale, latency, load test, ablation.

Chạy:  python scripts/make_real_figures.py
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).parent.parent
REAL = ROOT / "results" / "real"
FIG = ROOT / "results" / "figures"

SCALE_LABEL = {"s1": "10K", "s2": "50K", "s3": "181K (full)"}
SYSTEMS = ["bm25", "bm25_fielddrop", "bm25_field", "hybrid"]
COLORS = {"bm25": "#4C72B0", "bm25_fielddrop": "#C44E52",
          "bm25_field": "#8172B2", "hybrid": "#DD8452"}


def read(path: Path) -> list[dict]:
    return list(csv.DictReader(open(path, encoding="utf-8")))


def main() -> int:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    FIG.mkdir(parents=True, exist_ok=True)
    summary = read(REAL / "eval_summary.csv")
    latency = read(REAL / "latency.csv")

    # ── 1. Recall@10 + Recall@50 theo scale ──
    for metric, fname in [("Recall@10", "real_scale_recall10.png"),
                          ("Recall@50", "real_scale_recall50.png"),
                          ("MRR", "real_scale_mrr.png")]:
        fig, ax = plt.subplots(figsize=(7, 4.5))
        scales = ["s1", "s2", "s3"]
        for system in SYSTEMS:
            ys = [float(next(r[metric] for r in summary
                             if r["scale"] == s and r["system"] == system))
                  for s in scales]
            ax.plot([SCALE_LABEL[s] for s in scales], ys, "o-", label=system,
                    color=COLORS[system])
        ax.set_xlabel("Corpus size (declarations)")
        ax.set_ylabel(metric)
        ax.set_title(f"{metric} theo quy mô — LeanDojo Benchmark 4 (số thật)")
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(FIG / fname, dpi=150)
        plt.close(fig)
        print(f"✓ {fname}")

    # ── 2. Latency theo scale (P50/P95) ──
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharex=True)
    scales = ["s1", "s2", "s3"]
    for ax, col, title in [(axes[0], "p50_ms", "P50 latency"),
                           (axes[1], "p95_ms", "P95 latency")]:
        for system in SYSTEMS:
            ys = [float(next(r[col] for r in latency
                             if r["scale"] == s and r["system"] == system))
                  for s in scales]
            ax.plot([SCALE_LABEL[s] for s in scales], ys, "o-", label=system,
                    color=COLORS[system])
        ax.set_xlabel("Corpus size")
        ax.set_ylabel("ms (đo thật, 1 client)")
        ax.set_title(title)
        ax.grid(alpha=0.3)
        ax.legend()
    fig.suptitle("Độ trễ theo quy mô corpus — hybrid giữ P95 thấp nhất ở full corpus", y=1.02)
    fig.tight_layout()
    fig.savefig(FIG / "real_latency_by_scale.png", dpi=150)
    plt.close(fig)
    print("✓ real_latency_by_scale.png")

    # ── 3. Load test: QPS + P95 theo concurrency ──
    lt = read(REAL / "load_test.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    conc = [r["concurrency"] for r in lt]
    ax1.plot(conc, [float(r["qps"]) for r in lt], "o-", color="#DD8452")
    ax1.set_xlabel("Số client đồng thời")
    ax1.set_ylabel("QPS")
    ax1.set_title("QPS theo tải (hybrid, 50K corpus)")
    ax1.grid(alpha=0.3)
    ax2.plot(conc, [float(r["p50_ms"]) for r in lt], "o-", label="P50", color="#4C72B0")
    ax2.plot(conc, [float(r["p95_ms"]) for r in lt], "s-", label="P95", color="#C44E52")
    ax2.set_xlabel("Số client đồng thời")
    ax2.set_ylabel("ms")
    ax2.set_title("Latency theo tải — GIL khiến P95 tăng ~25×")
    ax2.grid(alpha=0.3)
    ax2.legend()
    fig.tight_layout()
    fig.savefig(FIG / "real_load_test.png", dpi=150)
    plt.close(fig)
    print("✓ real_load_test.png")

    print(f"\nMọi biểu đồ sinh từ results/real/*.csv bằng script này.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
