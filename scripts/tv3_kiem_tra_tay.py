# -*- coding: utf-8 -*-
"""TV3 — Kiểm chứng bằng tay 1 query cho baseline BM25 (dùng khi báo cáo/bảo vệ).

In ra:
  1. token của query;
  2. top-5 của baseline `bm25` (systems.py, k1=1.5, b=0.75);
  3. điểm BM25 của kết quả hạng 1 tách theo từng token (tf, df, idf, đóng góp)
     → cộng lại phải BẰNG điểm hệ thống trả về;
  4. Recall@10 và RR tính tay → phải BẰNG metrics.py.

Chạy:  python scripts/tv3_kiem_tra_tay.py
       python scripts/tv3_kiem_tra_tay.py --scale s1 --query QAdjoinRoot.isRoot_root
"""
import argparse
import csv
import math
import sys
from collections import Counter
from pathlib import Path

for s in (sys.stdout, sys.stderr):
    if s.encoding and s.encoding.lower() not in ("utf-8", "utf8"):
        s.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "retrieval"))
sys.path.insert(0, str(ROOT / "src" / "evaluation"))
from metrics import QueryResult, recall_at_k, reciprocal_rank  # noqa: E402
from systems import RetrievalSystem, tokenize  # noqa: E402


def load(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", default="s1")
    ap.add_argument("--query", default="", help="bỏ trống = tự chọn query đầu tiên có kết quả đúng trong top-10")
    a = ap.parse_args()
    real = ROOT / "results" / "real"
    corpus = load(real / f"corpus_{a.scale}.csv")
    queries = {q["id"]: q for q in load(real / f"queries_{a.scale}.csv")}
    gold_of = {}
    for r in load(real / f"qrels_{a.scale}.csv"):
        if r["relevance"] == "2":
            gold_of.setdefault(r["query_id"], set()).add(r["premise_id"])

    system = RetrievalSystem("bm25", corpus)      # baseline chính thức
    idx = system.index
    qid = a.query or next(q for q in sorted(gold_of) if q in queries
                          and set(system.search(queries[q], 10)) & gold_of[q])
    q, gold = queries[qid], gold_of.get(qid, set())
    toks = tokenize(q["statement"], True)

    print("=" * 75)
    print(f"QUERY: {qid}\n  {' '.join(q['statement'].split())[:250]}")
    print(f"  Token ({len(toks)}): {toks}")
    print(f"  Premise đúng (nhãn 2): {sorted(gold)}")
    print(f"\nN = {idx.N}   avgdl = {idx.avgdl:.2f}   k1 = {idx.k1}   b = {idx.b}")

    ranked = system.search(q, top_k=50)           # đã lọc chính theorem truy vấn
    scores = dict(idx.search(toks, 60))
    print("\nTop-5 BM25:")
    for r, p in enumerate(ranked[:5], 1):
        print(f"  {r}. {p:<55} {scores[p]:8.4f}{'   <- ĐÚNG' if p in gold else ''}")

    top = ranked[0]
    i = idx.doc_ids.index(top)
    dl = idx.doc_len[i]
    print(f"\nTách điểm của hạng 1 '{top}'  (|D| = {dl})")
    print(f"  {'token':<14}{'qtf':>4}{'tf':>4}{'df':>8}{'idf':>8}{'đóng góp':>10}")
    total = 0.0
    for t, qtf in Counter(toks).items():
        tf = idx.tf[i].get(t, 0)
        if not tf:
            continue
        df = idx.df[t]
        idf = math.log(1 + (idx.N - df + 0.5) / (df + 0.5))
        c = qtf * idf * tf * (idx.k1 + 1) / (tf + idx.k1 * (1 - idx.b + idx.b * dl / idx.avgdl))
        total += c
        print(f"  {t!r:<14}{qtf:>4}{tf:>4}{df:>8}{idf:>8.3f}{c:>10.4f}")
    print(f"  Tổng tính tay = {total:.4f} | hệ thống = {scores[top]:.4f}  "
          f"{'✓ KHỚP' if abs(total - scores[top]) < 1e-9 else '✗ LỆCH'}")

    pos = {g: ranked.index(g) + 1 for g in gold if g in ranked}
    hit10 = sum(1 for r in pos.values() if r <= 10)
    rr = 1 / min(pos.values()) if pos else 0.0
    res = QueryResult(qid, ranked, gold)
    print(f"\nHạng của premise đúng: {pos or '(không có trong top-50)'}")
    print(f"  Recall@10 tay = {hit10}/{len(gold)} = {hit10 / len(gold):.4f} | metrics.py = {recall_at_k(res, 10):.4f}")
    print(f"  RR tay = {rr:.4f} | metrics.py = {reciprocal_rank(res):.4f}")


if __name__ == "__main__":
    main()
