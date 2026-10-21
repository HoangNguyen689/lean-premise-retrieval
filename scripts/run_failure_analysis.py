"""Failure analysis — 30 failure cases được phân loại (nhiệm vụ tuần 8 của TV6).

Với mỗi query, hệ thống bị coi là FAIL khi Recall@10 < 1.0 (bỏ sót premise
relevant trực tiếp trong top-10). Script:
  1. Xếp hạng query tệ nhất theo Recall@10 của phương pháp chính (hybrid)
  2. Rút 30 case tệ nhất, phân loại lỗi theo taxonomy (xem docs/evaluation_protocol.md):
       - empty_overlap : query không khớp token nào với gold premise
       - symbol_heavy  : statement chứa nhiều ký hiệu Lean (≥ 3) — tokenizer yếu
       - few_gold      : gold premise ít (≤ 2) — 1 premise trượt là mất nặng recall
       - many_gold     : gold premise nhiều (≥ 5) — khó gom đủ trong top-10
       - cross_topic   : gold premise nằm lệch namespace/query topic
  3. Ghi results/raw/failure_cases.csv (30 dòng, mỗi dòng 1 case có phân loại)
  4. Ghi results/raw/failure_taxonomy.csv (tổng hợp theo loại)

Chạy:  python scripts/run_failure_analysis.py
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent
REAL = ROOT / "results" / "real"
OUT = ROOT / "results" / "raw"
sys.path.insert(0, str(ROOT / "src" / "evaluation"))

from metrics import QueryResult, load_qrels_csv, load_run_csv, recall_at_k  # noqa: E402  # type: ignore[import]

SYSTEMS = ["hybrid", "bm25", "bm25_fielddrop"]  # chính + đối chứng (dữ liệu thật)
SCALE = "s3"               # phân tích trên scale lớn nhất
TOP_N = 30                 # số failure cases yêu cầu (môn học: 30 cases)
SYMBOLS = ["∀", "∃", "∈", "⊆", "⋃", "↦", "ℕ", "ℤ", "→", "∧", "∨", "¬"]


def classify(q: dict, qr: QueryResult, corpus_ns: dict[str, str],
             query_topic: str) -> list[str]:
    """Gán 1+ nhãn lỗi cho một query fail (một case có thể thuộc nhiều loại)."""
    labels = []
    qwords = set(q["statement"].lower().split())
    gold_words = set()
    for p in qr.gold_premises:
        gold_words |= set(corpus_ns.get(p, "").lower().replace("_", " ").split())

    overlap = qwords & gold_words
    n_sym = sum(1 for ch in q["statement"] if ch in SYMBOLS)
    if len(qwords) == 0 or not overlap:
        labels.append("empty_overlap")
    if n_sym >= 3:
        labels.append("symbol_heavy")
    if len(qr.gold_premises) <= 2:
        labels.append("few_gold")
    if len(qr.gold_premises) >= 5:
        labels.append("many_gold")
    # cross_topic: gold premise thuộc namespace khác hẳn namespace dự kiến của query
    gold_ns = {corpus_ns.get(p, "") for p in qr.gold_premises}
    if query_topic and gold_ns and all(query_topic.lower() not in ns.lower() for ns in gold_ns):
        labels.append("cross_topic")
    if not labels:
        labels.append("rank_trouble")  # có khớp token nhưng xếp hạng tệ
    return labels


def main() -> int:
    qrels = load_qrels_csv(REAL / f"qrels_{SCALE}.csv")

    corpus_ns: dict[str, str] = {}
    with open(REAL / f"corpus_{SCALE}.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            corpus_ns[row["id"]] = row["statement_natural"]

    queries: dict[str, dict] = {}
    with open(REAL / f"queries_{SCALE}.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            queries[row["id"]] = row

    runs_by_system = {s: load_run_csv(REAL / f"run_{s}_{SCALE}.csv") for s in SYSTEMS}

    # Mỗi cặp (hệ thống, query) có recall@10 < 1.0 là một case ứng viên.
    # Sắp theo recall tăng dần rồi rút TOP_N case tệ nhất.
    candidates = []
    for system, runs in runs_by_system.items():
        for qid, qrel in qrels.items():
            qr = QueryResult(qid, runs.get(qid, []),
                             {p for p, r in qrel.items() if r == 2},
                             {p for p, r in qrel.items() if r == 1})
            r10 = recall_at_k(qr, 10)
            if r10 < 1.0:
                candidates.append((r10, system, qid, qr))

    candidates.sort(key=lambda t: (t[0], t[2], t[1]))
    picked = candidates[:TOP_N]

    # query topic: dùng cột namespace của queries file (topic ban đầu)
    rows = []
    label_counts: Counter = Counter()
    for r10, system, qid, qr in picked:
        q = queries.get(qid, {})
        labels = classify(q, qr, corpus_ns, q.get("namespace", ""))
        for lb in labels:
            label_counts[lb] += 1
        missing = qr.gold_premises - set(runs_by_system[system].get(qid, [])[:10])
        rows.append([
            qid, system, q.get("namespace", ""), f"{r10:.2f}",
            len(qr.gold_premises),
            ";".join(sorted(missing)) or "—",
            ";".join(labels),
        ])

    out = OUT / "failure_cases.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["query_id", "system", "topic", "recall@10", "n_gold",
                    "missing_premises", "failure_types"])
        w.writerows(rows)
    print(f"Đã ghi {out.relative_to(ROOT)}: {len(rows)} failure cases "
          f"(tổng {len(candidates)} cặp hệ×query có recall < 1.0)\n")

    tax = OUT / "failure_taxonomy.csv"
    with open(tax, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["failure_type", "n_cases", "share_%"])
        total = sum(label_counts.values())
        for lb, n in label_counts.most_common():
            w.writerow([lb, n, f"{n / total:.1%}"])
    print(f"Đã ghi {tax.relative_to(ROOT)}\n")

    print(f"{'Loại lỗi':<16} {'Số case':>8} {'Tỷ lệ':>8}")
    print("-" * 34)
    for lb, n in label_counts.most_common():
        print(f"{lb:<16} {n:>8} {n / total:>8.1%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
