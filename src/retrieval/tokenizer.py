"""Lean 4 statement tokenizer for sparse retrieval."""
from __future__ import annotations

import re

# Common Lean/Mathlib symbols found in statements
LEAN_SYMBOLS = set("∀∃∈∉⊆⊂⊃⊇∪∩⋃⋂↦→←↔×∘¬∧∨≡≈≤≥<>=+−*/^λΠΣℕℤℚℝ𝔹⟨⟩")

_TOKEN_RE = re.compile(
    r"""
    [A-Za-z_][A-Za-z0-9_'.!?]*        # identifier: Nat.add_comm, List.foldl
    | [ℕℤℚℝ𝔹]                          # number types
    | [∀∃∈∉⊆⊂⊃⊇∪∩⋃⋂↦→←↔×∘¬∧∨≡≈≤≥]      # logic/algebra single-char operators
    | \d+                              # numbers
    | [(){}\[\]:|,]                    # Lean punctuation
    """,
    re.VERBOSE,
)


def tokenize(text: str, keep_symbols: bool = True) -> list[str]:
    """Tokenize a Lean 4 statement.

    keep_symbols=True  -> keep Lean symbols (used by bm25_field, hybrid)
    keep_symbols=False -> drop symbols (used by bm25_fielddrop ablation)
    """
    if not keep_symbols:
        text = "".join(ch if ch not in LEAN_SYMBOLS else " " for ch in text)
    # split CamelCase / snake_case identifiers: Nat.add_comm -> nat, add, comm
    tokens = []
    for raw in _TOKEN_RE.findall(text):
        low = raw.lower()
        for part in re.split(r"[._]+", low):
            if not part:
                continue
            if len(part) > 4 and re.fullmatch(r"[a-z]+", part):
                # CamelCase split: prefold -> pre, fold
                for sub in re.findall(r"[a-z]+|[0-9]+", part):
                    tokens.append(sub)
            else:
                tokens.append(part)
    return tokens
