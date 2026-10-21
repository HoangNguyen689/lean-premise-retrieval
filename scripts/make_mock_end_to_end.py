"""Mock end-to-end data — thay người khác khi họ chậm (kịch bản phòng hờ TV6).

Tạo đầy đủ artifact theo data_contract_v1.md cho MỌI mức scale, để TV6
(Evaluation) chạy được toàn bộ pipeline mà không phụ thuộc TV1-TV5 hay Nhóm 4:
  - corpus_{s1,s2,full}.csv   (premise pool, 6 field contract)
  - queries_{s1,s2,full}.csv  (query set, 6 field contract)
  - qrels_{s1,s2,full}.csv    (nhãn 0/1/2, pooling)
  - run_bm25_{s1,s2,full}.csv         (TV3 — BM25 baseline)
  - run_bm25_fielddrop_{s1,s2,full}.csv (TV4 — BM25 bỏ field ký hiệu — ablation)
  - run_hybrid_{s1,s2,full}.csv       (TV4 — hybrid reranker — phương pháp chính)
  - run_dense_{s1,s2,full}.csv        (Nhóm 4 — dense/ANN)
  - run_latency_{s1,s2,full}.csv      (TV5 — P50/P95 latency mỗi hệ)

Cách mô phỏng "thực tế vừa đủ": mỗi query được gán premise "tốt" dựa trên
match token giữa statement query và statement premise (giống BM25 thật hơn là
ngẫu nhiên thuần), sau đó mỗi hệ thống thêm nhiễu khác nhau:
  - BM25:      khớp token nhưng chỉ thấy từ khóa, hay trượt hạng bởi từ phổ biến
  - bm25_fielddrop: như BM25 nhưng "mù" với statement chứa ký hiệu Lean (ℕ, ∀, ↦)
  - hybrid:    BM25 + boost từ namespace/dependency → recall cao hơn
  - dense:     semantic, tốt với câu tự nhiên nhưng yếu với ký hiệu Lean
Mức thân thiện được hiệu chỉnh để hybrid > dense > bm25 > fielddrop về Recall@10
— phản ánh giả thuyết RQ1/RQ2; khi có dữ liệu thật, thay run file bằng kết quả
thật, mọi script đánh giá không đổi.

Chạy:  python scripts/make_mock_end_to_end.py
Xóa:   python scripts/make_mock_end_to_end.py --clean
"""
from __future__ import annotations

import argparse
import csv
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
RAW = ROOT / "results" / "raw"
sys.path.insert(0, str(ROOT / "src" / "evaluation"))

from contract import validate_csv  # noqa: E402

random.seed(42)
DATA_VERSION = "mock-v0+split-v1.0"
TOP_K = 50

# ── 1. Vốn từ Lean/mathlib để sinh corpus giả lập ─────────────────────────
NAMESPACES = {
    "algebra": ["Mathlib.Algebra.Group.Basic", "Mathlib.Algebra.Ring.Basic",
                "Mathlib.Algebra.Field.Basic", "Mathlib.RingTheory.Ideal"],
    "analysis": ["Mathlib.Analysis.Calculus.Deriv", "Mathlib.Analysis.NormedSpace.Basic",
                 "Mathlib.Topology.UniformConvergence", "Mathlib.MeasureTheory.Measure.Lebesgue"],
    "number_theory": ["Mathlib.NumberTheory.Primes", "Mathlib.Data.Nat.GCD",
                      "Mathlib.Data.Nat.Factorization"],
    "set_theory": ["Mathlib.Order.SetNotation", "Mathlib.SetTheory.Cardinal.Basic"],
    "topology": ["Mathlib.Topology.Connectedness", "Mathlib.Topology.Compactness",
                 "Mathlib.Topology.ProductTopology"],
    "category": ["Mathlib.CategoryTheory.Mono", "Mathlib.CategoryTheory.Limits.Shapes"],
    "hard_edge": ["Mathlib.Data.Nat.Defs", "Mathlib.Analysis.Calculus.Deriv.Mul"],
}
NATURAL = {
    "algebra": ["group", "subgroup", "ring", "ideal", "field", "product", "homomorphism",
                "integral domain", "principal", "polynomial", "unit", "inverse"],
    "analysis": ["continuous", "limit", "derivative", "convergent", "measure", "norm",
                 "compact", "maximum", "uniform", "banach", "sequence", "bounded"],
    "number_theory": ["prime", "gcd", "divides", "factor", "natural number", "integer",
                      "infinitely many", "positive"],
    "set_theory": ["union", "power set", "inclusion", "surjection", "cardinal", "subset",
                   "partially ordered", "commutative"],
    "topology": ["connected", "compact", "product", "continuous image", "open", "closed",
                 "cover", "space"],
    "category": ["monomorphism", "composition", "functor", "morphism", "epimorphism",
                 "isomorphism", "category", "limits"],
    "hard_edge": ["vector space", "basis", "complete", "derivative", "power", "addition",
                  "zero", "natural"],
}
SYMBOLS = ["∀", "∃", "∈", "⊆", "⋃", "↦", "ℕ", "ℤ", "→", "∧", "∨", "¬", "=", "+", "×", "∘"]

# seed theorems của query set v0 — dùng đúng statement đã chốt ở tuần 1
QUERY_STATEMENTS: dict[str, tuple[str, str]] = {}
for row in csv.DictReader(open(ROOT / "configs" / "query_set_v0.csv", encoding="utf-8")):
    QUERY_STATEMENTS[row["query_id"]] = (row["topic"], row["statement_raw"])


def leanify(words: list[str], n_sym: int) -> str:
    """Biến cụm từ tự nhiên thành pseudo-statement Lean."""
    sym = " ".join(random.choices(SYMBOLS, k=n_sym))
    return f"theorem mock : ∀ {' '.join(words[:3])}, {sym} {' '.join(words[3:])}"


def build_corpus(n: int) -> list[dict]:
    """Sinh n premise theo contract: id, statement, statement_natural, namespace, file_path, line_start."""
    rows, seen = [], set()
    while len(rows) < n:
        topic = random.choice(list(NAMESPACES))
        ns = random.choice(NAMESPACES[topic])
        words = random.sample(NATURAL[topic], k=min(4, len(NATURAL[topic])))
        extra = random.choice(NATURAL[topic])
        words = words + [extra]
        pid = f"P{len(rows) + 1:05d}"
        if pid in seen:
            continue
        seen.add(pid)
        rows.append({
            "id": pid,
            "statement": leanify(words, random.randint(1, 3)),
            "statement_natural": " ".join(words),
            "namespace": ns.split(".")[-1],
            "file_path": f"{ns.replace('.', '/')}.lean",
            "line_start": random.randint(1, 900),
            "topic": topic,  # cột nội bộ — validator bỏ qua cột thừa
        })
    return rows


def token_overlap(query_words: list[str], premise_words: list[str]) -> float:
    q = set(query_words)
    p = set(premise_words)
    if not q:
        return 0.0
    return len(q & p) / len(q)


def make_qrels(corpus: list[dict], queries: list[dict]) -> tuple[list[list], dict[str, list[str]]]:
    """Gán gold (nhãn 2) theo token overlap cao nhất, partial (nhãn 1) cùng namespace/file."""
    by_ns: dict[str, list[dict]] = {}
    for r in corpus:
        by_ns.setdefault(r["namespace"], []).append(r)
    qrels, gold_map = [], {}
    for q in queries:
        qwords = q["statement_natural"].lower().split()
        scored = sorted(
            ((token_overlap(qwords, r["statement_natural"].lower().split()), r) for r in corpus),
            key=lambda t: (-t[0], t[1]["id"]),
        )
        top = [r for s, r in scored if s > 0][: random.randint(2, 5)]
        if not top:
            top = [scored[0][1]]
        gold_map[q["query_id"]] = [r["id"] for r in top]
        partial_pool = by_ns.get(top[0]["namespace"], []) + random.sample(corpus, 30)
        seen_ids: dict[str, None] = {}
        for r in partial_pool:
            if r["id"] not in gold_map[q["query_id"]]:
                seen_ids.setdefault(r["id"], None)
        partials = list(seen_ids)[: random.randint(1, 3)]
        for pid in gold_map[q["query_id"]]:
            qrels.append([q["query_id"], pid, 2])
        for pid in partials:
            qrels.append([q["query_id"], pid, 1])
    return qrels, gold_map


def simulate_run(name: str, corpus: list[dict], queries: list[dict],
                 gold_map: dict[str, list[str]], qrels_rows: list[list]) -> list[list]:
    """Sinh run file top-50 cho một hệ thống theo 'persona' mô phỏng."""
    rows = []
    for q in queries:
        qid = q["query_id"]
        qwords = q["statement_natural"].lower().split()
        gold = gold_map[qid]
        partial_ids = {p for g, p, rel in qrels_rows if g == qid and rel == 1}
        scored = []
        for r in corpus:
            base = token_overlap(qwords, r["statement_natural"].lower().split())
            if base == 0 and r["id"] not in gold:
                continue
            noise = random.uniform(0, 0.3)
            if name == "bm25":
                score = base + noise - 0.15 * (r["namespace"].lower() in qwords and 1 or 0)
            elif name == "bm25_fielddrop":
                # "mù" ký hiệu: statement có ký hiệu Lean → mất tín hiệu (giả lập RQ1)
                if any(s in r["statement"] for s in SYMBOLS[:8]):
                    score = base * 0.35 + noise
                else:
                    score = base + noise
            elif name == "hybrid":
                # boost structural: cùng namespace với gold → cộng điểm
                ns_boost = 0.18 if any(
                    r["namespace"] == c["namespace"] for c in corpus if c["id"] in gold
                ) else 0.0
                score = base + ns_boost + noise * 0.6
            elif name == "dense":
                # semantic: tốt với câu tự nhiên, thêm khả năng bắt gold ở hạng khá
                score = base * 0.9 + random.uniform(0, 0.22)
            else:
                raise ValueError(name)
            scored.append((score, r["id"]))
        scored.sort(key=lambda t: -t[0])
        ranked = [pid for _, pid in scored[:TOP_K]]
        # đảm bảo có tín hiệu: 1-2 gold lọt top (trừ hybrid/dense mạnh hơn)
        n_hit = {"bm25": random.randint(1, 2), "bm25_fielddrop": random.randint(0, 1),
                 "hybrid": random.randint(2, 4), "dense": random.randint(2, 3)}[name]
        for g in random.sample(gold, min(n_hit, len(gold))):
            if g not in ranked:
                ranked[random.randint(0, len(ranked) - 1)] = g
        rows.extend([qid, pid] for pid in ranked)
    return rows


def write_csv(path: Path, header: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows([header] + rows)


def build_scale(n_premises: int, n_queries: int, scale: str) -> None:
    corpus = build_corpus(n_premises)
    qids = sorted(QUERY_STATEMENTS)[:n_queries]
    queries = [
        {"query_id": qid, "statement_raw": s, "statement_natural": s.lower(),
         "namespace": QUERY_STATEMENTS[qid][0], "file_path": f"{QUERY_STATEMENTS[qid][0]}.lean",
         "line_start": i + 1}
        for i, (qid, (topic, s)) in enumerate(sorted(QUERY_STATEMENTS.items())[:n_queries])
    ]
    # queries vẫn giữ statement_raw nguyên văn từ query set v0
    for i, q in enumerate(queries):
        q["statement_raw"] = QUERY_STATEMENTS[q["query_id"]][1]
        q["statement_natural"] = QUERY_STATEMENTS[q["query_id"]][1].lower()

    write_csv(RAW / f"corpus_{scale}.csv",
              ["id", "statement", "statement_natural", "namespace", "file_path", "line_start"],
              [[r["id"], r["statement"], r["statement_natural"], r["namespace"],
                r["file_path"], r["line_start"]] for r in corpus])

    write_csv(RAW / f"queries_{scale}.csv",
              ["id", "statement", "statement_natural", "namespace", "file_path", "line_start"],
              [[q["query_id"], q["statement_raw"], q["statement_natural"], q["namespace"],
                q["file_path"], q["line_start"]] for q in queries])

    qrels, gold_map = make_qrels(corpus, queries)
    write_csv(RAW / f"qrels_{scale}.csv", ["query_id", "premise_id", "relevance"], qrels)

    for system in ["bm25", "bm25_fielddrop", "hybrid", "dense"]:
        rows = simulate_run(system, corpus, queries, gold_map, qrels)
        write_csv(RAW / f"run_{system}_{scale}.csv", ["query_id", "premise_id"], rows)
        print(f"  {scale}: run_{system}_{scale}.csv  ({len(rows)} dòng)")

    print(f"  {scale}: corpus {len(corpus)}, queries {len(queries)}, qrels {len(qrels)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clean", action="store_true", help="Xóa mọi file mock do script này tạo")
    args = ap.parse_args()
    if args.clean:
        removed = 0
        for p in RAW.glob("*_s[123].csv") if RAW.exists() else []:
            p.unlink()
            removed += 1
        print(f"Đã xóa {removed} file mock scale.")
        return

    print("Sinh mock data theo data_contract_v1 ...")
    for n_prem, n_q, scale in [(1_000, 20, "s1"), (5_000, 20, "s2"), (10_000, 20, "s3")]:
        build_scale(n_prem, n_q, scale)

    # ── validate contract cho S1 làm ví dụ ──
    print("\nValidate contract S1:")
    for artifact, path in [("corpus", RAW / "corpus_s1.csv"),
                           ("queries", RAW / "queries_s1.csv"),
                           ("qrels", RAW / "qrels_s1.csv")]:
        rep = validate_csv(path, artifact)
        print(f"  {rep.summary()}")

    print("\nOK. TV6 giờ chạy được toàn pipeline không cần ai:" )
    print("  python scripts/run_all_evaluations.py")


if __name__ == "__main__":
    main()
