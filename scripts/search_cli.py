"""Search CLI - truy vấn premise mathlib4 từ dòng lệnh (sản phẩm bàn giao TV5).

Ví dụ:
    python scripts/search_cli.py "Every finite integral domain is a field"
    python scripts/search_cli.py "Nat.add_comm" --system hybrid --top 10
    python scripts/search_cli.py "continuous function compact" --system bm25_field --show-statement
"""
from __future__ import annotations

import argparse
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

from rankers import RetrievalSystem  # noqa: E402  # type: ignore[import]

_cache: dict[str, RetrievalSystem] = {}


def get_system(name: str, scale: str) -> RetrievalSystem:
    key = f"{name}:{scale}"
    if key not in _cache:
        corpus = list(csv.DictReader(
            open(REAL / f"corpus_{scale}.csv", encoding="utf-8")))
        _cache[key] = RetrievalSystem(name, corpus)
    return _cache[key]


def main() -> int:
    ap = argparse.ArgumentParser(description="Truy hồi premise mathlib4 (Nhóm 3)")
    ap.add_argument("query", help="Câu truy vấn (tiếng Anh hoặc statement Lean)")
    ap.add_argument("--system", default="hybrid",
                    choices=["bm25", "bm25_fielddrop", "bm25_field", "hybrid"])
    ap.add_argument("--scale", default="s1", choices=["s1", "s2", "s3", "full"],
                    help="Corpus dùng (mặc định s1=10K để nhanh)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--show-statement", action="store_true",
                    help="In statement Lean của mỗi kết quả")
    args = ap.parse_args()

    scale = "s3" if args.scale == "full" else args.scale
    system = get_system(args.system, scale)

    q = {"id": "QCLI", "statement": args.query, "namespace": "",
         "file_path": "", "statement_natural": ""}
    t0 = time.perf_counter()
    ranked = system.search(q, top_k=args.top)
    elapsed = (time.perf_counter() - t0) * 1000

    corpus_by_id = {d["id"]: d for d in system.docs}
    print(f"\nTruy vấn: {args.query!r}")
    print(f"Hệ: {args.system} | corpus: {scale} | thời gian: {elapsed_ms:.1f} ms\n" if False else "")
    print(f"Hệ: {args.system} | corpus: {scale} | {len(system.docs)} declarations | "
          f"{elapsed:.1f} ms")
    print("-" * 78)
    for i, pid in enumerate(ranked, 1):
        d = corpus_by_id.get(pid, {})
        ns = d.get("namespace", "?")
        if args.show_statement:
            stmt = (d.get("statement", "") or "")[:140].replace("\n", " ")
            print(f"{i:>3}. {pid}")
            print(f"     namespace: {ns} | file: {d.get('file_path', '?')}:{d.get('line_start', '?')}")
            print(f"     {stmt}")
        else:
            print(f"{i:>3}. {pid:<55} [{ns}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
