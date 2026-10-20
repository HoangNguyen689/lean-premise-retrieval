# -*- coding: utf-8 -*-
"""Retrieval systems THẬT cho Nhóm 3 — TV2 (index) + TV3 (BM25) + TV4 (structural).

4 hệ thống trên corpus thật (LeanDojo Benchmark 4):
  1. bm25           — BM25 mặc định trên statement tách từ (baseline bắt buộc của môn)
  2. bm25_fielddrop — BM25 bỏ ký hiệu Lean (ablation RQ1: "có/không ký hiệu")
  3. bm25_field     — field-aware: BM25 nhiều field (statement + full_name + namespace)
  4. hybrid         — bm25_field + structural reranking (namespace match + file proximity)

Cùng dữ liệu, cùng split, cùng máy — theo QUY TẮC BASELINE của đề.

Dùng rank_bm25 nếu có, không có thì BM25 thuần Python (không phụ thuộc mạng).
"""
from __future__ import annotations

import csv
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

# ── Tokenizer ──────────────────────────────────────────────────────────────

# Ký hiệu Lean/Mathlib thường gặp trong statement
LEAN_SYMBOLS = set("∀∃∈∉⊆⊂⊃⊇∪∩⋃⋂↦→←↔×∘¬∧∨≡≈≤≥<>=+−*/^λΠΣℕℤℚℝ𝔹⟨⟩")

_TOKEN_RE = re.compile(
    r"""
    [A-Za-z_][A-Za-z0-9_'.!?]*        # identifier: Nat.add_comm, List.foldl
    | [ℕℤℚℝ𝔹]                          # number types
    | [∀∃∈∉⊆⊂⊃⊇∪∩⋃⋂↦→←↔×∘¬∧∨≡≈≤≥]      # toán tử logic/đại số 1 ký tự
    | \d+                              # số
    | [(){}\[\]:|,]                    # dấu câu Lean
    """,
    re.VERBOSE,
)


def tokenize(text: str, keep_symbols: bool = True) -> list[str]:
    """Tách statement Lean thành tokens.

    keep_symbols=True  → giữ ký hiệu Lean (dùng cho bm25_field, hybrid)
    keep_symbols=False → bỏ ký hiệu (dùng cho bm25_fielddrop — ablation)
    """
    if not keep_symbols:
        text = "".join(ch if ch not in LEAN_SYMBOLS else " " for ch in text)
    # tách identifier dạng CamelCase/snake_case thành sub-tokens: Nat.add_comm → nat, add, comm
    tokens = []
    for raw in _TOKEN_RE.findall(text):
        low = raw.lower()
        for part in re.split(r"[._]+", low):
            if not part:
                continue
            if len(part) > 4 and re.fullmatch(r"[a-z]+", part):
                # CamelCase split: prefold → pre, fold
                for sub in re.findall(r"[a-z]+|[0-9]+", part):
                    tokens.append(sub)
            else:
                tokens.append(part)
    return tokens


# ── BM25 (thuần Python, không phụ thuộc thư viện ngoài) ────────────────────

class BM25Index:
    """Inverted index + BM25 trên một field (hoặc nhiều field gộp/trọng số)."""

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
                # field weight: nhân số lần xuất hiện
                tokens.extend(toks * max(1, int(round(w))))
            self.tf.append(Counter(tokens))
            self.doc_len.append(len(tokens))
        self.N = len(docs)
        self.avgdl = sum(self.doc_len) / max(1, self.N)
        self.df: Counter = Counter()
        for c in self.tf:
            self.df.update(c.keys())
        # inverted index: token → {doc_idx: tf}
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


# ── 4 hệ thống ─────────────────────────────────────────────────────────────

@dataclass
class RetrievalSystem:
    """Một hệ truy hồi cụ thể + hàm truy vấn."""

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
            # "mù" ký hiệu: tokenize bỏ ký hiệu trên statement (ablation RQ1)
            idx = BM25Index(self.docs, {"statement": 1.0})
            orig = tokenize
            self.index = idx
            self._drop = True
        elif self.name == "bm25_field":
            self.index = BM25Index(self.docs, {"statement": 1.0, "id": 2.0, "namespace": 3.0})
        elif self.name == "hybrid":
            self.index = BM25Index(self.docs, {"statement": 1.0, "id": 2.0, "namespace": 3.0})

    def search(self, query: dict, top_k: int = 50) -> list[str]:
        """Trả về danh sách premise id xếp hạng.

        Quy tắc eligible premise (data contract v1.2 §5.4, thống nhất với Nhóm 4):
        theorem truy vấn KHÔNG được phép xuất hiện trong kết quả (không dùng chính nó
        làm premise). Vì query nằm trong corpus, lọc self trước khi cắt top_k —
        hệ vẫn trả đủ top_k kết quả hiệu dụng.
        """
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
            # stage 1: BM25 field-aware lấy top-200 (lấy dư để lọc self không rỗng top_k)
            text = " ".join([query["statement"], query["id"].replace("Q", ""), query["namespace"]])
            cand = self.index.search(tokenize(text, True), 200)
            # stage 2: structural rerank — cộng điểm namespace match + file proximity
            q_ns = query["namespace"]
            q_file = query.get("file_path", "")
            reranked = []
            for pid, score in cand:
                if pid == self_name:
                    continue  # eligible premise: không trả chính theorem truy vấn
                ns_bonus = 0.35 if self.ns_of.get(pid, "").startswith(q_ns[:30]) else 0.0
                file_bonus = 0.20 if self.file_of.get(pid, "") == q_file else 0.0
                reranked.append((pid, score + ns_bonus + file_bonus))
            reranked.sort(key=lambda t: (-t[1], t[0]))
            return [pid for pid, _ in reranked[:top_k]]
        raise ValueError(self.name)
