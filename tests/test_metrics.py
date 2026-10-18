import math

import pytest

from n3.eval import metrics


def test_recall_mrr_ndcg_hand_computed():
    ranked = [7, 3, 9, 1, 5]
    gold = {3, 5}
    assert metrics.recall_at_k(ranked, gold, 1) == 0.0
    assert metrics.recall_at_k(ranked, gold, 2) == 0.5
    assert metrics.recall_at_k(ranked, gold, 5) == 1.0
    assert metrics.reciprocal_rank(ranked, gold) == 0.5
    expected = (1 / math.log2(3) + 1 / math.log2(6)) / (1 + 1 / math.log2(3))
    assert metrics.ndcg_at_k(ranked, gold, 10) == pytest.approx(expected)


def test_not_found():
    assert metrics.reciprocal_rank([1, 2], {9}) == 0.0
    assert metrics.recall_at_k([1, 2], {9}, 10) == 0.0


def test_empty_gold_is_error():
    with pytest.raises(ValueError):
        metrics.recall_at_k([1], set(), 1)


def test_bootstrap_detects_clear_improvement():
    a = [0.0] * 50 + [1.0] * 50
    b = [1.0] * 100
    res = metrics.paired_bootstrap(a, b, n_boot=2000)
    assert res["delta"] == 0.5 and res["p_value"] < 0.01


def test_cluster_bootstrap_point_estimates_hand_computed():
    # cụm A: 3 truy vấn, mỗi truy vấn tăng 1; cụm B: 1 truy vấn không đổi
    a = [0.0, 0.0, 0.0, 0.0]
    b = [1.0, 1.0, 1.0, 0.0]
    clusters = ["A", "A", "A", "B"]
    q = metrics.paired_cluster_bootstrap(a, b, clusters, n_boot=2000, estimand="query")
    c = metrics.paired_cluster_bootstrap(a, b, clusters, n_boot=2000, estimand="cluster")
    assert q["delta"] == pytest.approx(0.75)        # trung bình theo truy vấn
    assert c["delta"] == pytest.approx(0.5)         # trung bình của trung bình từng cụm
    assert q["n_clusters"] == 2


def test_cluster_bootstrap_wider_than_query_bootstrap_for_correlated_queries():
    # 20 cụm, mỗi cụm 10 truy vấn cùng một chênh lệch: các truy vấn trong cụm không độc lập
    import numpy as np
    rng = np.random.default_rng(0)
    effects = rng.normal(0.05, 0.2, 20)
    d = np.repeat(effects, 10)
    clusters = np.repeat(np.arange(20), 10)
    plain = metrics.paired_bootstrap(np.zeros_like(d), d)
    clus = metrics.paired_cluster_bootstrap(np.zeros_like(d), d, clusters)
    assert clus["ci95_high"] - clus["ci95_low"] > 2 * (plain["ci95_high"] - plain["ci95_low"])


def test_holm_hand_computed():
    assert metrics.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
