# -*- coding: utf-8 -*-
"""Demo end-to-end evaluation pipeline (tuần 1).

Mô phỏng: query set v0 (20 truy vấn) + một hệ thống BM25 giả lập trên
corpus nhỏ → sinh run file + qrels → tính metrics bằng metrics.py.

Mục đích: chứng minh evaluation pipeline chạy được TRƯỚC khi có corpus thật
(tuần 2 thay corpus giả bằng LeanDojo sample).
"""
import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "src" / "evaluation"))

from metrics import evaluate_from_files

random.seed(42)

# ── 1. Corpus giả: 200 premise P0001..P0200 với namespace ngẫu nhiên ──
TOPICS = ["RingTheory", "GroupTheory", "LinearAlgebra", "Topology",
          "MeasureTheory", "NumberTheory", "Order", "SetTheory",
          "CategoryTheory", "Analysis"]
corpus = [f"P{i:04d}" for i in range(1, 201)]

# ── 2. Sinh qrels: mỗi query gán 3-8 premise gold (giả lập từ LeanDojo trace) ──
queries = list(csv.DictReader(open(ROOT / "configs" / "query_set_v0.csv", encoding="utf-8")))
qrels_rows = []
gold_map = {}
for q in queries:
    n_gold = random.randint(2, 5)
    n_partial = random.randint(1, 3)
    golds = random.sample(corpus, n_gold)
    partials = random.sample([p for p in corpus if p not in golds], n_partial)
    gold_map[q["query_id"]] = golds
    for p in golds:
        qrels_rows.append([q["query_id"], p, 2])
    for p in partials:
        qrels_rows.append([q["query_id"], p, 1])

# ── 3. Sinh run file: hệ thống "BM25 giả" trả top-50, nhét 1-2 gold ngẫu nhiên ──
run_rows = []
for q in queries:
    qid = q["query_id"]
    ranked = random.sample([p for p in corpus if p not in gold_map[qid]], 48)
    hits = random.sample(gold_map[qid], random.randint(1, 2))
    for h in hits:
        ranked.insert(random.randint(0, 20), h)
    run_rows.extend([qid, p] for p in ranked[:50])

# ── 4. Ghi file ──
raw_dir = ROOT / "results" / "raw"
raw_dir.mkdir(parents=True, exist_ok=True)
qrels_path = raw_dir / "qrels_demo.csv"
run_path = raw_dir / "run_bm25_mock.csv"
with open(qrels_path, "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows([["query_id", "premise_id", "relevance"]] + qrels_rows)
with open(run_path, "w", encoding="utf-8", newline="") as f:
    csv.writer(f).writerows([["query_id", "premise_id"]] + run_rows)

# ── 5. Tính metrics ──
print(f"qrels: {qrels_path}  ({len(qrels_rows)} nhãn)")
print(f"run:   {run_path}  ({len(run_rows)} dòng)\n")
metrics = evaluate_from_files(qrels_path, run_path)
print(f"{'Metric':<12} {'Giá trị':>8}")
print("-" * 22)
for name, val in metrics.items():
    print(f"{name:<12} {val:>8.4f}")
