"""Unit test cho metrics.py — kết quả đối chiếu tính tay.

Chạy: python tests/test_metrics.py
"""
import sys
from pathlib import Path

# Windows console (CMD) thường dùng cp1252/cp437 — không chứa chữ tiếng Việt.
# Buộc stdout/stderr dùng UTF-8 (Python 3.7+) để không crash khi in tiếng Việt.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "evaluation"))

from metrics import QueryResult, dcg_at_k, evaluate, ndcg_at_k, recall_at_k, reciprocal_rank

PASS = 0
FAIL = 0


def check(name: str, got, expected, tol=1e-9):
    global PASS, FAIL
    ok = abs(got - expected) < tol if isinstance(expected, float) else got == expected
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}: got={got}, expected={expected}")
    if ok:
        PASS += 1
    else:
        FAIL += 1


# ── Dữ liệu kiểm tra tay ─────────────────────────────────────────
# Truy vấn q1: gold = {P3, P7}; hệ thống trả về top-5: P1 P2 P3 P4 P5
q1 = QueryResult("q1", ["P1", "P2", "P3", "P4", "P5"], gold_premises={"P3", "P7"})

# Recall@5: chỉ P3 trong top5 → 1/2 = 0.5
check("Recall@5 q1", recall_at_k(q1, 5), 0.5)
# Recall@1: không có → 0.0
check("Recall@1 q1", recall_at_k(q1, 1), 0.0)
# Recall@2: 0.0 (P3 ở hạng 3)
check("Recall@2 q1", recall_at_k(q1, 2), 0.0)
# MRR: P3 ở hạng 3 → 1/3
check("RR q1", reciprocal_rank(q1), 1 / 3)

# Truy vấn q2: gold = {P1}; hệ thống trả P1 hạng 1
q2 = QueryResult("q2", ["P1", "P9"], gold_premises={"P1"})
check("Recall@1 q2", recall_at_k(q2, 1), 1.0)
check("RR q2", reciprocal_rank(q2), 1.0)

# Truy vấn q3: không có kết quả liên quan trong top-k
q3 = QueryResult("q3", ["P8", "P9"], gold_premises={"P1"})
check("Recall@10 q3", recall_at_k(q3, 10), 0.0)
check("RR q3", reciprocal_rank(q3), 0.0)

# include_partial: q4 gold={P5}, partial={P2}
q4 = QueryResult("q4", ["P2", "P6"], gold_premises={"P5"}, gold_partial={"P2"})
check("Recall@1 q4 (chỉ gold)", recall_at_k(q4, 1), 0.0)
# có partial: gold mở rộng thành {P5, P2}, top1 chứa P2 → 1/2
check("Recall@1 q4 (có partial)", recall_at_k(q4, 1, include_partial=True), 0.5)
# RR cũng đếm partial
check("RR q4 (có partial)", reciprocal_rank(q4), 1.0)

# ── nDCG@k kiểm tra tay ──────────────────────────────────────────
# q1 ranked: P1(0) P2(0) P3(2) P4(0) P5(0); gold={P3,P7} (2 relevant)
# DCG@5 = (2^2-1)/log2(4) = 1.5
# IDCG@5: ideal gains [2,2] → 3/log2(2) + 3/log2(3) = 3 + 1.89279 = 4.89279
# nDCG@5 = 1.5 / 4.89279 ≈ 0.30657
import math
idcg_q1 = 3 / 1 + 3 / math.log2(3)
check("nDCG@5 q1", ndcg_at_k(q1, 5), 1.5 / idcg_q1, tol=1e-4)

# Trường hợp hoàn hảo: gold đứng đầu
q5 = QueryResult("q5", ["P1", "P2"], gold_premises={"P1"})
check("nDCG@2 q5 hoàn hảo", ndcg_at_k(q5, 2), 1.0)

# ── Macro-average trên nhiều query ───────────────────────────────
avg = evaluate([q1, q2], ks=(5,))
# Recall@5 avg = (0.5 + 1.0) / 2 = 0.75
check("Macro Recall@5", avg["Recall@5"], 0.75)
# MRR avg = (1/3 + 1) / 2 ≈ 0.6667
check("Macro MRR", avg["MRR"], (1 / 3 + 1) / 2)

print(f"\n{'='*50}\nKết quả: {PASS} PASS, {FAIL} FAIL")
sys.exit(1 if FAIL else 0)
