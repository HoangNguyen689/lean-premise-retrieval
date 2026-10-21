"""Chạy toàn bộ đánh giá: mọi hệ thống × mọi scale → metrics + run logs.

Đây là script "một lệnh" của TV6:
  1. Đọc qrels + run file của từng hệ thống (BM25, fielddrop, hybrid, dense)
  2. Tính Recall@1/5/10/50, MRR, nDCG@10 qua 3 scale
  3. Sinh results/raw/eval_summary.csv và results/raw/runs/*.json (Phụ lục B)
  4. Phát hiện lệch định dạng run file bằng contract.py (fail sớm, không im lặng)

Chạy:  python scripts/run_all_evaluations.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW = ROOT / "results" / "raw"
sys.path.insert(0, str(ROOT / "src" / "evaluation"))

from contract import validate_csv  # noqa: E402  # type: ignore[import]
from metrics import evaluate_from_files  # noqa: E402  # type: ignore[import]
from run_logger import RunLogger  # RunLogger ghi JSON theo Phụ lục B  # type: ignore[import]

SYSTEMS = [
    # (tên, mô tả, nhóm sở hữu)
    ("bm25", "BM25 baseline (TV3) — TF-IDF/BM25 mặc định trên statement tách từ", "N3"),
    ("bm25_fielddrop", "Ablation: BM25 không thấy ký hiệu Lean (TV4)", "N3"),
    ("hybrid", "Hybrid sparse+structural reranker (TV4) — phương pháp chính N3", "N3"),
    ("dense", "Dense/ANN (Nhóm 4)", "N4"),
]
SCALES = ["s1", "s2", "s3"]


def fmt(v: float) -> str:
    return f"{v:.4f}"


def main() -> int:
    if not (RAW / "corpus_s1.csv").exists():
        print("Chưa có mock data. Chạy trước: python scripts/make_mock_end_to_end.py")
        return 1

    summary_rows = []
    for scale in SCALES:
        qrels_path = RAW / f"qrels_{scale}.csv"
        for system, desc, owner in SYSTEMS:
            run_path = RAW / f"run_{system}_{scale}.csv"
            if not run_path.exists():
                print(f"⚠ Bỏ qua {system}/{scale}: thiếu {run_path.name}")
                continue

            rep = validate_csv(run_path, "run")
            if not rep.ok:
                print(f"✗ {system}/{scale} vi phạm contract run file:")
                for e in rep.errors[:5]:
                    print(f"   {e}")
                continue

            log = RunLogger(
                parameters={"system": system, "scale": scale, "top_k": 50,
                            "recall_convention": "label2"},
                seed=42,
                data_version="mock-v0+split-v1.0",
            )
            try:
                metrics = evaluate_from_files(qrels_path, run_path)
                log.finish(
                    metrics=metrics,
                    artifacts=[str(run_path.relative_to(ROOT))],
                )
                summary_rows.append(
                    [scale, system, owner] + [fmt(metrics[k]) for k in
                     ["Recall@1", "Recall@5", "Recall@10", "Recall@50", "MRR", "nDCG@10"]]
                )
                pretty = ", ".join(f"{k}={v:.4f}" for k, v in metrics.items())
                print(f"✓ {scale}/{system:<15} {pretty}")
            except Exception as exc:  # noqa: BLE001
                log.fail(error=str(exc))
                print(f"✗ {scale}/{system}: {exc}")

    out = RAW / "eval_summary.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scale", "system", "owner", "Recall@1", "Recall@5",
                    "Recall@10", "Recall@50", "MRR", "nDCG@10"])
        w.writerows(summary_rows)
    print(f"\nĐã ghi {out.relative_to(ROOT)} ({len(summary_rows)} dòng)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
