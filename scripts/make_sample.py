"""Tạo data_sample/ (được commit vào Git) để người khác chạy thử pipeline mà không cần tải toàn bộ dữ liệu.

Gồm 200 truy vấn random/test (seed 42), qrels của chúng, toàn bộ premise đúng tương ứng và premise ngẫu nhiên
cho đủ ~1.000 premise. premise_id giữ nguyên như bản đầy đủ. Nguồn: LeanDojo Benchmark 4 v10 (CC BY 2.0),
văn bản Lean thuộc mathlib4/Lean 4/Batteries (Apache-2.0); xem docs/license_note.md.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    src = ROOT / "data" / "processed"
    out = ROOT / "data_sample"
    out.mkdir(exist_ok=True)
    rng = np.random.default_rng(42)
    q = pq.read_table(src / "queries.parquet").to_pandas()
    q = q[(q.split_strategy == "random") & (q.split == "test")]
    q = q.loc[rng.choice(q.index.to_numpy(), size=200, replace=False)].sort_values("query_id")
    qr = pq.read_table(src / "qrels.parquet").to_pandas()
    qr = qr[qr.query_id.isin(set(q.query_id))]
    prem = pq.read_table(src / "premises.parquet").to_pandas()
    gold = set(qr.premise_id)
    others = rng.permutation(np.setdiff1d(prem.premise_id.to_numpy(), list(gold)))[: max(0, 1000 - len(gold))]
    keep = sorted(gold | set(others.tolist()))
    prem = prem[prem.premise_id.isin(keep)]
    prem.to_json(out / "premises.jsonl", orient="records", lines=True, force_ascii=False)
    q.to_json(out / "queries.jsonl", orient="records", lines=True, force_ascii=False)
    qr.to_json(out / "qrels.jsonl", orient="records", lines=True)
    info = {"source": "LeanDojo Benchmark 4 v10 (Zenodo 12740403), mathlib4 commit 29dcec07",
            "n_premises": len(prem), "n_queries": len(q), "n_qrels": len(qr), "seed": 42,
            "note": "premise_id giống bản đầy đủ; chỉ để chạy thử, không dùng để báo cáo kết quả"}
    (out / "SAMPLE_INFO.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
    print(info)


if __name__ == "__main__":
    main()
