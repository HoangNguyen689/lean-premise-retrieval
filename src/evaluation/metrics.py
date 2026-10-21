"""Evaluation metrics cho Nhóm 3 - Lean Premise Retrieval.

TV6 (Evaluation) dùng module này để tính Recall@k, MRR, nDCG@k
từ danh sách ranking của bất kỳ hệ thống truy hồi nào (BM25, hybrid, ...).

Quy ước xem docs/evaluation_protocol.md §3.
"""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class QueryResult:
    """Kết quả truy hồi của 1 truy vấn.

    Attributes:
        query_id: định danh truy vấn.
        ranked_premises: danh sách premise ID xếp theo hệ thống, index 0 = hạng 1.
        gold_premises: set premise ID liên quan (nhãn 2 - relevant trực tiếp).
        gold_partial: set premise ID liên quan gián tiếp (nhãn 1). Optional.
    """

    query_id: str
    ranked_premises: list[str]
    gold_premises: set[str]
    gold_partial: set[str] = field(default_factory=set)


def recall_at_k(result: QueryResult, k: int, include_partial: bool = False) -> float:
    """Recall@k của một truy vấn. include_partial=True thì tính cả nhãn 1."""
    gold = set(result.gold_premises)
    if include_partial:
        gold = gold | set(result.gold_partial)
    if not gold:
        return 0.0
    top_k = result.ranked_premises[:k]
    hits = sum(1 for p in top_k if p in gold)
    return hits / len(gold)


def reciprocal_rank(result: QueryResult, k: int | None = None) -> float:
    """RR của một truy vấn: 1/rank của kết quả liên quan đầu tiên (nhãn 2 trước, rồi 1)."""
    gold = set(result.gold_premises)
    partial = set(result.gold_partial)
    candidates = result.ranked_premises[:k] if k else result.ranked_premises
    for rank, premise in enumerate(candidates, start=1):
        if premise in gold or premise in partial:
            return 1.0 / rank
    return 0.0


def dcg_at_k(gains: list[float], k: int) -> float:
    """DCG@k với gain = 2^rel - 1."""
    return sum((2**rel - 1) / _log2(i + 2) for i, rel in enumerate(gains[:k]))


def ndcg_at_k(result: QueryResult, k: int) -> float:
    """nDCG@k của một truy vấn. rel=2 cho gold, rel=1 cho partial, còn lại 0.

    IDCG tính trên toàn bộ relevant của query (kể cả premise chưa xuất hiện
    trong ranked list) - theo định nghĩa chuẩn của Burges et al.
    """
    gold = set(result.gold_premises)
    partial = set(result.gold_partial)

    def gain(premise: str) -> int:
        if premise in gold:
            return 2
        if premise in partial:
            return 1
        return 0

    gains = [gain(p) for p in result.ranked_premises[:k]]
    ideal_gains = sorted([2] * len(gold) + [1] * len(partial), reverse=True)
    idcg = dcg_at_k(ideal_gains, k)
    if idcg == 0:
        return 0.0
    return dcg_at_k(gains, k) / idcg


def evaluate(
    results: list[QueryResult],
    ks: tuple[int, ...] = (1, 5, 10, 50),
    include_partial: bool = False,
) -> dict[str, float]:
    """Tính macro-average mọi chỉ số cho một hệ thống.

    Returns:
        dict với key dạng 'Recall@10', 'MRR', 'nDCG@10'.
    """
    metrics: dict[str, float] = {}
    for k in ks:
        metrics[f"Recall@{k}"] = mean(recall_at_k(r, k, include_partial) for r in results)
    metrics["MRR"] = mean(reciprocal_rank(r) for r in results)
    metrics["nDCG@10"] = mean(ndcg_at_k(r, 10) for r in results)
    return metrics


def load_qrels_csv(path: str | Path) -> dict[str, dict[str, int]]:
    """Đọc qrels CSV: cột query_id, premise_id, relevance (0/1/2)."""
    qrels: dict[str, dict[str, int]] = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            qrels.setdefault(row["query_id"], {})[row["premise_id"]] = int(
                row["relevance"]
            )
    return qrels


def load_run_csv(path: str | Path) -> dict[str, list[str]]:
    """Đọc kết quả hệ thống CSV: cột query_id, premise_id (đã xếp hạng theo dòng)."""
    runs: dict[str, list[str]] = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            runs.setdefault(row["query_id"], []).append(row["premise_id"])
    return runs


def evaluate_from_files(
    qrels_path: str | Path,
    run_path: str | Path,
    ks: tuple[int, ...] = (1, 5, 10, 50),
    include_partial: bool = False,
) -> dict[str, float]:
    """Tiện ích: tính metrics trực tiếp từ 2 file CSV (qrels + run)."""
    qrels = load_qrels_csv(qrels_path)
    runs = load_run_csv(run_path)
    results = []
    for qid, qrel in qrels.items():
        ranked = runs.get(qid, [])
        gold = {p for p, rel in qrel.items() if rel == 2}
        partial = {p for p, rel in qrel.items() if rel == 1}
        results.append(
            QueryResult(
                query_id=qid,
                ranked_premises=ranked,
                gold_premises=gold,
                gold_partial=partial,
            )
        )
    return evaluate(results, ks=ks, include_partial=include_partial)


def _log2(x: float) -> float:
    import math

    return math.log2(x)


def mean(values) -> float:
    values = list(values)
    if not values:
        return 0.0
    return sum(values) / len(values)
