"""Tạo corpus tổng hợp ×F bằng cách nhân bản premise (đánh lại premise_id) để đo build và skew ở quy mô lớn hơn.

CHỈ dùng cho thí nghiệm build/skew. Không dùng để đo chất lượng truy hồi (văn bản trùng lặp nên
không có ý nghĩa về recall). Phân phối term giữ nguyên, df của mọi term tăng đúng F lần.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--factor", type=int, default=5)
    ap.add_argument("--processed", default="data/processed")
    args = ap.parse_args()
    root = Path(args.processed)
    t = pq.read_table(root / "premises.parquet", columns=["premise_id", "name", "namespace", "statement"])
    n = t.num_rows
    parts = []
    for i in range(args.factor):
        parts.append(t.set_column(0, "premise_id", pa.array(np.arange(i * n, (i + 1) * n, dtype=np.int64))))
    out = root / "synthetic"
    out.mkdir(exist_ok=True)
    path = out / f"premises_x{args.factor}.parquet"
    pq.write_table(pa.concat_tables(parts), path, compression="zstd")
    print(f"{path}: {n * args.factor} bản ghi")


if __name__ == "__main__":
    main()
