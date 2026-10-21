"""export_n4_shared.py — Xuất gói chia sẻ đúng schema Nhóm 4 yêu cầu (thống nhất 2026-10-18).

Nhóm 4 đề nghị 6 mục thống nhất; 5/6 đã có trong data contract v1.1. Script này
sinh đúng 2 file JSONL họ nêu + checksum, đặt vào results/n4_shared/:
  - corpus.jsonl   — {id, name, statement, namespace, source_commit}
  - queries.jsonl  — {id, statement, relevant_ids, split:"test", pool_id:"shared-frozen-pool"}
  - checksums.txt  — SHA-256 của corpus.jsonl + queries.jsonl (để N4 xác nhận)

Chỉ dùng file có sẵn (results/real/) — KHÔNG cần dataset raw.

Chạy:  python scripts/export_n4_shared.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
REAL = ROOT / "results" / "real"
OUT = ROOT / "results" / "n4_shared"

MATHLIB_COMMIT = "29dcec074de168ac2bf835a77ef68bbe069194c5"
POOL_ID = "shared-frozen-pool"
DATA_VERSION = "leandojo-benchmark-4@29dcec07+split-v1.0"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    corpus_path = REAL / "corpus_s3.csv"
    queries_path = REAL / "queries_s3.csv"
    qrels_path = REAL / "qrels_s3.csv"
    for p in [corpus_path, queries_path, qrels_path]:
        if not p.exists():
            print(f"✗ Thiếu {p.name} — chạy download_data.py trước.")
            return 1
    OUT.mkdir(parents=True, exist_ok=True)

    # ── corpus.jsonl — schema N4: id, name, statement, namespace, source_commit ──
    n = 0
    with open(OUT / "corpus.jsonl", "w", encoding="utf-8") as out, \
         open(corpus_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.write(json.dumps({
                "id": row["id"],
                "name": row["id"],  # name = full_name (không tách được name riêng — ghi chú trong contract)
                "statement": row["statement"],
                "namespace": row["namespace"],
                "source_commit": MATHLIB_COMMIT,
            }, ensure_ascii=False) + "\n")
            n += 1
    print(f"✓ corpus.jsonl: {n:,} declarations")

    # ── queries.jsonl — schema N4: id, statement, relevant_ids, split, pool_id ──
    # relevant_ids = các premise nhãn 2 (đúng trực tiếp từ proof trace)
    golds: dict[str, list[str]] = {}
    with open(qrels_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if int(row["relevance"]) == 2:
                golds.setdefault(row["query_id"], []).append(row["premise_id"])
    n = 0
    with open(OUT / "queries.jsonl", "w", encoding="utf-8") as out, \
         open(queries_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            qid = row["id"]
            out.write(json.dumps({
                "id": qid,
                "statement": row["statement"],
                "relevant_ids": sorted(golds.get(qid, [])),
                "split": "test",
                "pool_id": POOL_ID,
            }, ensure_ascii=False) + "\n")
            n += 1
    print(f"✓ queries.jsonl: {n:,} queries (relevant_ids = nhãn 2, mean "
          f"{sum(len(v) for v in golds.values()) / max(len(golds), 1):.1f}/query)")

    # ── checksums.txt ──
    with open(OUT / "checksums.txt", "w", encoding="utf-8") as out:
        out.write(f"# Gói chia sẻ N3→N4 — {DATA_VERSION}\n")
        out.write(f"# pool_id: {POOL_ID}\n")
        for name in ["corpus.jsonl", "queries.jsonl"]:
            out.write(f"{sha256(OUT / name)}  {name}\n")
    print(f"✓ checksums.txt (SHA-256)")

    # ── meta:eligible-rule xác nhận ──
    (OUT / "eligible_rule.txt").write_text(
        "QUY TẮC ELIGIBLE PREMISE (N3 xác nhận, khớp đề nghị của N4):\n"
        "1. Theorem truy vấn KHÔNG được phép xuất hiện trong kết quả truy hồi của chính nó\n"
        "   (đã cài trong src/retrieval/systems.py — lọc self trước khi cắt top_k).\n"
        "2. Premise pool = toàn bộ corpus.jsonl trừ chính theorem truy vấn (frozen trước\n"
        "   mọi run — pool_id: shared-frozen-pool).\n"
        "3. 56 nhãn-2 là theorem thuộc test split KHÁC được dùng làm premise của query —\n"
        "   hợp lệ (premise giữa các theorem test với nhau), giữ nguyên trong relevant_ids.\n",
        encoding="utf-8")
    print(f"✓ eligible_rule.txt")

    print(f"\nGói: {OUT} — gửi cho N4 (nén zip ~15 MB).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
