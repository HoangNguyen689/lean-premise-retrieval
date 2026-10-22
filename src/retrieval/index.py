"""Pure-Python BM25 inverted index."""
from __future__ import annotations

import math
from collections import Counter

from tokenizer import tokenize  # type: ignore[import]


class BM25Index:
    """Inverted index + BM25 scoring over one or more weighted fields."""

    def __init__(self, docs: list[dict], field_weights: dict[str, float] | None = None,
                 k1: float = 1.5, b: float = 0.75):
        """docs: [{id, statement, namespace, file_path, ...}]."""
        self.k1, self.b = k1, b
        self.field_weights = field_weights or {"statement": 1.0}
        self.doc_ids = [d["id"] for d in docs]
        self.doc_len = []
        self.tf: list[Counter] = []
        for d in docs:
            tokens: list[str] = []
            for fname, w in self.field_weights.items():
                text = d.get(fname, "") or ""
                toks = tokenize(text, keep_symbols=True)
                # field weight: repeat tokens according to weight
                tokens.extend(toks * max(1, int(round(w))))
            self.tf.append(Counter(tokens))
            self.doc_len.append(len(tokens))
        self.N = len(docs)
        self.avgdl = sum(self.doc_len) / max(1, self.N)
        self.df: Counter = Counter()
        for c in self.tf:
            self.df.update(c.keys())
        # inverted index: token -> {doc_idx: tf}
        self.inv: dict[str, dict[int, int]] = {}
        for i, c in enumerate(self.tf):
            for tok, n in c.items():
                self.inv.setdefault(tok, {})[i] = n

    def idf(self, tok: str) -> float:
        n = self.df.get(tok, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def search(self, query_tokens: list[str], top_k: int = 50) -> list[tuple[str, float]]:
        scores: dict[int, float] = {}
        for tok in query_tokens:
            postings = self.inv.get(tok)
            if not postings:
                continue
            idf = self.idf(tok)
            for i, tf in postings.items():
                denom = tf + self.k1 * (1 - self.b + self.b * self.doc_len[i] / self.avgdl)
                scores[i] = scores.get(i, 0.0) + idf * tf * (self.k1 + 1) / denom
        ranked = sorted(scores.items(), key=lambda t: (-t[1], t[0]))[:top_k]
        return [(self.doc_ids[i], s) for i, s in ranked]
