"""Metric truy hồi theo từng truy vấn và trung bình.

- Recall@k = |gold ∩ top-k| / |gold|  (định nghĩa dùng trong LeanDojo/ReProver)
- MRR      = 1 / hạng của premise đúng đầu tiên (0 nếu không có trong danh sách trả về)
- nDCG@k   = nhãn nhị phân, log2
"""
from __future__ import annotations

import math
from typing import Iterable, Sequence

import numpy as np

DEFAULT_KS = (1, 5, 10, 50)


def recall_at_k(ranked: Sequence[int], gold: set[int], k: int) -> float:
    if not gold:
        raise ValueError("truy vấn không có premise đúng")
    return len(gold.intersection(ranked[:k])) / len(gold)


def reciprocal_rank(ranked: Sequence[int], gold: set[int]) -> float:
    for i, pid in enumerate(ranked, start=1):
        if pid in gold:
            return 1.0 / i
    return 0.0


def ndcg_at_k(ranked: Sequence[int], gold: set[int], k: int) -> float:
    dcg = sum(1.0 / math.log2(i + 1) for i, pid in enumerate(ranked[:k], start=1) if pid in gold)
    ideal = sum(1.0 / math.log2(i + 1) for i in range(1, min(len(gold), k) + 1))
    return dcg / ideal


def per_query(ranked: Sequence[int], gold: set[int], ks: Iterable[int] = DEFAULT_KS) -> dict[str, float]:
    row = {f"R@{k}": recall_at_k(ranked, gold, k) for k in ks}
    row["MRR"] = reciprocal_rank(ranked, gold)
    row["nDCG@10"] = ndcg_at_k(ranked, gold, 10)
    return row


def aggregate(rows: list[dict[str, float]]) -> dict[str, float]:
    keys = rows[0].keys() if rows else []
    return {k: float(np.mean([r[k] for r in rows])) for k in keys}


def paired_cluster_bootstrap(a: Sequence[float], b: Sequence[float], clusters: Sequence, n_boot: int = 10000,
                             seed: int = 42, estimand: str = "query") -> dict[str, float]:
    """Paired bootstrap theo cụm (ví dụ theorem): lấy mẫu cụm có hoàn lại, mang theo mọi truy vấn của cụm.

    estimand="query":   chênh lệch trung bình theo truy vấn (query-macro), giống metric chính của báo cáo
    estimand="cluster": chênh lệch trung bình của trung bình từng cụm (theorem-macro, mỗi theorem nặng như nhau)
    Trả delta (b - a) trên toàn bộ dữ liệu, khoảng tin cậy 95% theo phân vị, p một phía (tỉ lệ mẫu bootstrap có
    chênh lệch <= 0; độ phân giải 1/n_boot) và p hai phía = 2 min(p, 1 - p)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape or len(clusters) != a.size:
        raise ValueError("a, b và clusters phải cùng độ dài")
    d = b - a
    _, inv = np.unique(np.asarray(clusters, dtype=object).astype(str), return_inverse=True)
    sums = np.bincount(inv, weights=d)
    sizes = np.bincount(inv).astype(float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, sums.size, size=(n_boot, sums.size))
    if estimand == "query":
        point = d.mean()
        boots = sums[idx].sum(axis=1) / sizes[idx].sum(axis=1)
    elif estimand == "cluster":
        means = sums / sizes
        point = means.mean()
        boots = means[idx].mean(axis=1)
    else:
        raise ValueError("estimand phải là 'query' hoặc 'cluster'")
    p1 = float((boots <= 0).mean())
    return {"delta": float(point), "ci95_low": float(np.percentile(boots, 2.5)),
            "ci95_high": float(np.percentile(boots, 97.5)), "p_value": p1,
            "p_two_sided": float(min(1.0, 2 * min(p1, 1 - p1))), "n_clusters": int(sums.size), "n_boot": n_boot}


def holm(pvalues: Sequence[float]) -> list[float]:
    """Hiệu chỉnh Holm cho một họ giả thuyết; trả p đã hiệu chỉnh theo đúng thứ tự đầu vào."""
    p = np.asarray(pvalues, dtype=float)
    order = np.argsort(p)
    m = p.size
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[i]))
        adj[i] = running
    return adj.tolist()


def paired_bootstrap(a: Sequence[float], b: Sequence[float], n_boot: int = 10000, seed: int = 42) -> dict[str, float]:
    """So sánh hai hệ thống trên cùng tập truy vấn: trả chênh lệch trung bình (b - a),
    khoảng tin cậy 95% và p-value một phía (tỉ lệ mẫu bootstrap có chênh lệch ≤ 0)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.shape != b.shape:
        raise ValueError("hai hệ thống phải có cùng tập truy vấn")
    d = b - a
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, d.size, size=(n_boot, d.size))
    means = d[idx].mean(axis=1)
    return {
        "delta": float(d.mean()),
        "ci95_low": float(np.percentile(means, 2.5)),
        "ci95_high": float(np.percentile(means, 97.5)),
        "p_value": float((means <= 0).mean()),
    }
