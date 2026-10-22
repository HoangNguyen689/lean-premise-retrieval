"""Retrieval rankers for Lean Premise Retrieval.

Implements four systems on the real LeanDojo Benchmark 4 corpus:
  1. bm25           - default BM25 over tokenized statement (required baseline)
  2. bm25_fielddrop - BM25 dropping Lean symbols (ablation RQ1: with/without symbols)
  3. bm25_field     - field-aware BM25 (statement + full_name + namespace)
  4. hybrid         - bm25_field + structural reranking (namespace + file proximity)
"""
from __future__ import annotations

from dataclasses import dataclass, field

from index import BM25Index  # type: ignore[import]
from tokenizer import tokenize  # type: ignore[import]


@dataclass
class RetrievalSystem:
    """A concrete retrieval system + query function."""

    name: str
    docs: list[dict]
    index: BM25Index | None = None
    ns_of: dict[str, str] = field(default_factory=dict)
    file_of: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.ns_of = {d["id"]: d["namespace"] for d in self.docs}
        self.file_of = {d["id"]: d["file_path"] for d in self.docs}
        if self.name == "bm25":
            self.index = BM25Index(self.docs, {"statement": 1.0})
        elif self.name == "bm25_fielddrop":
            # symbol-blind: drop Lean symbols when tokenizing statement
            self.index = BM25Index(self.docs, {"statement": 1.0})
            self._drop = True
        elif self.name == "bm25_field":
            self.index = BM25Index(self.docs, {"statement": 1.0, "id": 2.0, "namespace": 3.0})
        elif self.name == "hybrid":
            self.index = BM25Index(self.docs, {"statement": 1.0, "id": 2.0, "namespace": 3.0})

    def search(self, query: dict, top_k: int = 50) -> list[str]:
        """Return a ranked list of premise IDs.

        Eligible-premise rule (data contract v1.2 §5.4, agreed with Group 4):
        the query theorem must not appear in its own results. Because the query
        is part of the corpus, we filter self before cutting top_k; the system
        still returns a full top_k of useful results.
        """
        assert self.index is not None
        self_name = query["id"][1:] if query["id"].startswith("Q") else query["id"]
        if self.name == "bm25":
            hits = self.index.search(tokenize(query["statement"], True), top_k + 8)
            return [pid for pid, _ in hits if pid != self_name][:top_k]
        if self.name == "bm25_fielddrop":
            hits = self.index.search(tokenize(query["statement"], False), top_k + 8)
            return [pid for pid, _ in hits if pid != self_name][:top_k]
        if self.name == "bm25_field":
            text = " ".join([query["statement"], query["id"].replace("Q", ""), query["namespace"]])
            hits = self.index.search(tokenize(text, True), top_k + 8)
            return [pid for pid, _ in hits if pid != self_name][:top_k]
        if self.name == "hybrid":
            # stage 1: field-aware BM25 retrieves top-200 (extra room for self-filter)
            text = " ".join([query["statement"], query["id"].replace("Q", ""), query["namespace"]])
            cand = self.index.search(tokenize(text, True), 200)
            # stage 2: structural rerank - boost namespace match + file proximity
            q_ns = query["namespace"]
            q_file = query.get("file_path", "")
            reranked = []
            for pid, score in cand:
                if pid == self_name:
                    continue  # eligible premise: do not return the query theorem itself
                ns_bonus = 0.35 if self.ns_of.get(pid, "").startswith(q_ns[:30]) else 0.0
                file_bonus = 0.20 if self.file_of.get(pid, "") == q_file else 0.0
                reranked.append((pid, score + ns_bonus + file_bonus))
            reranked.sort(key=lambda t: (-t[1], t[0]))
            return [pid for pid, _ in reranked[:top_k]]
        raise ValueError(self.name)
