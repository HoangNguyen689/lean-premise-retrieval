"""Bổ sung các minh chứng còn thiếu so với đề bài (kiểm tra 2026-10-15):

1. **Parquet + data dictionary** (tuần 2): chuyển corpus/queries/qrels CSV → Parquet
   + sinh docs/data_dictionary.md tự động.
2. **Index size + index manifest** (tuần 6, mục 9): đo index size MB mỗi hệ/scale,
   ghi index_manifest.json + index_size.csv.
3. **Error analysis theo ký hiệu/độ dài** (tuần 8): bổ sung slice symbol_heavy /
   statement length cho failure cases (ghép vào taxonomy).
4. **Lặp 3 lần runtime** (mục 8): chạy lại hybrid S3 3 lần, ghi median + min/max
   → results/real/runtime_repeats.csv.

Chạy:  python scripts/fill_gaps.py
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
import time
from pathlib import Path

# Windows console (CMD) thường dùng cp1252/cp437 — không chứa chữ tiếng Việt.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
REAL = ROOT / "results" / "real"
RAW = ROOT / "results" / "raw"
sys.path.insert(0, str(ROOT / "src" / "retrieval"))

SCALES = ["s1", "s2", "s3"]
SYMBOLS = set("∀∃∈∉⊆⊂⊃⊇∪∩⋃⋂↦→←↔×∘¬∧∨≡≈≤≥<>=+−*/^λΠΣℕℤℚℝ𝔹")


def sha256(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def task_parquet() -> None:
    try:
        import pandas as pd
    except ImportError:
        print("⚠ Bỏ qua Parquet (thiếu pandas/pyarrow) — CSV vẫn dùng được đầy đủ.")
        print("  Cài thêm nếu muốn Parquet:  pip install pyarrow pandas")
        return
    for scale in SCALES + ["full"]:
        for kind in ["corpus", "queries", "qrels"]:
            src = REAL / f"{kind}_{scale}.csv"
            if src.exists():
                df = pd.read_csv(src, dtype=str, keep_default_na=False,
                                 na_filter=False)
                df.to_parquet(src.with_suffix(".parquet"), index=False)
    print("✓ Parquet: corpus/queries/qrels × 4 (s1/s2/s3/full) —", len(list(REAL.glob('*.parquet'))), "files")


def task_data_dictionary() -> None:
    lines = [
        "# DATA DICTIONARY — Nhóm 3 (LeanDojo Benchmark 4, data_version `leandojo-benchmark-4@29dcec07+split-v1.0`)",
        "",
        "Áp dụng cho `results/real/{corpus,queries,qrels}_{scale}.parquet|.csv` (S1=10K/200, S2=50K/500, S3=full 180.907/898).",
        "",
        "## corpus / queries — 6 field contract v1.1",
        "",
        "| Field | Kiểu | Ý nghĩa | Rỗng hợp lệ? | Ví dụ |",
        "|---|---|---|---|---|",
        "| `id` | string | Định danh duy nhất: full_name của declaration (corpus); `Q<full_name>` (query) | Không | `Nat.add_comm` / `QCategoryTheory.Equivalence.invFunIdAssoc_hom_app` |",
        "| `statement` | string | Code Lean 4 nguyên văn của declaration (đối với query: code nếu tìm thấy trong corpus, else full_name) | Không | `theorem Nat.add_comm : ∀ (n m : ℕ), n + m = m + n := ...` |",
        "| `statement_natural` | string | Phát biểu tiếng Anh tự nhiên | Có (benchmark không cung cấp) | *(rỗng)* |",
        "| `namespace` | string | Namespace Lean: phần full_name trước dấu chấm cuối | Có (= declaration cấp root, vd. `AList`) | `Nat` |",
        "| `file_path` | string | Đường dẫn file trong mathlib4 (đã chuẩn hóa về `Mathlib/...`) | Không | `Mathlib/Data/Nat/Basic.lean` |",
        "| `line_start` | int | Dòng bắt đầu declaration trong file | Không (≥1) | `142` |",
        "",
        "## qrels — ground truth truy hồi",
        "",
        "| Field | Kiểu | Ý nghĩa |",
        "|---|---|---|",
        "| `query_id` | string | Khớp `queries.id` |",
        "| `premise_id` | string | Khớp `corpus.id` |",
        "| `relevance` | int | **2** = premise dùng trực tiếp trong chứng minh chuẩn (trích tự động từ `annotated_tactic` của LeanDojo trace); **1** = liên quan gián tiếp (cùng `file_path` với một premise nhãn 2, tối đa 10/query — chỉ dùng phân tích, không dùng primary metric); **0** = không liên quan (mặc định, không ghi file) |",
        "",
        "## Splits",
        "",
        "| Scale | Corpus | Queries | Ghi chú |",
        "|---|---|---|---|",
        "| S1 | 10.000 | 200 | sort theo `id`, 10K/200 đầu |",
        "| S2 | 50.000 | 500 | S1 ⊂ S2 |",
        "| S3 (full) | 180.907 | 898 | chỉ query có ≥1 premise GT |",
        "",
        "Checksum từng file: `split_manifest.json`. Nguồn: Zenodo DOI 10.5281/zenodo.12740403, license CC-BY-2.0.",
    ]
    out = ROOT / "docs" / "data_dictionary.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("✓ docs/data_dictionary.md")


def task_index_size() -> None:
    """Đo index size thật (inverted index RAM serialize + bytes corpus) mỗi hệ/scale."""
    from systems import RetrievalSystem
    rows, manifest = [], {}
    for scale in SCALES:
        corpus = list(csv.DictReader(open(REAL / f"corpus_{scale}.csv", encoding="utf-8")))
        for name in ["bm25", "bm25_field", "hybrid"]:
            t0 = time.time()
            system = RetrievalSystem(name, corpus)
            build_s = time.time() - t0
            # đo kích thước index: pickle toàn bộ cấu trúc inv + df
            import pickle
            blob = pickle.dumps({"inv": system.index.inv, "df": system.index.df,
                                 "doc_len": system.index.doc_len})
            size_mb = len(blob) / 1e6
            rows.append([scale, name, f"{size_mb:.1f}", f"{build_s:.2f}"])
            manifest[f"{name}:{scale}"] = {
                "index_size_mb": round(size_mb, 1), "build_s": round(build_s, 2),
                "n_docs": len(corpus),
                "tokenizer": "lean-camelcase+symbols" if name != "bm25_fielddrop" else "lean-no-symbols",
                "field_weights": {"bm25": {"statement": 1.0},
                                  "bm25_field": {"statement": 1.0, "id": 2.0, "namespace": 3.0},
                                  "hybrid": {"statement": 1.0, "id": 2.0, "namespace": 3.0}}[name],
                "k1": 1.5, "b": 0.75,
            }
            print(f"  {scale}/{name}: index {size_mb:.1f} MB, build {build_s:.2f}s")

    with open(REAL / "index_size.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scale", "system", "index_size_mb", "build_s"])
        w.writerows(rows)
    (REAL / "index_manifest.json").write_text(
        json.dumps({"data_version": "leandojo-benchmark-4@29dcec07+split-v1.0",
                    "indexes": manifest}, indent=2), encoding="utf-8")
    print("✓ results/real/index_size.csv + index_manifest.json")


def task_error_slices() -> None:
    """Bổ sung slice theo ký hiệu + độ dài vào failure taxonomy (tuần 8)."""
    queries = {q["id"]: q for q in csv.DictReader(open(REAL / "queries_s3.csv", encoding="utf-8"))}
    cases_path = RAW / "failure_cases.csv"
    if not cases_path.exists():
        print(f"⚠ {cases_path.name} not found — skipping error slices. "
              "Run failure analysis first: python scripts/run_failure_analysis.py")
        return
    cases = list(csv.DictReader(open(cases_path, encoding="utf-8")))

    slice_counts = {"symbol_heavy_statement": 0, "long_statement_gt200": 0,
                    "short_statement_lt40": 0}
    for c in cases:
        q = queries.get(c["query_id"], {})
        stmt = q.get("statement", "") or ""
        n_sym = sum(1 for ch in stmt if ch in SYMBOLS)
        if n_sym >= 5:
            slice_counts["symbol_heavy_statement"] += 1
        if len(stmt) > 200:
            slice_counts["long_statement_gt200"] += 1
        if len(stmt) < 40:
            slice_counts["short_statement_lt40"] += 1

    # merge vào taxonomy file
    with open(RAW / "failure_taxonomy.csv", "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        for k, v in slice_counts.items():
            w.writerow([k, v, "slice"])

    # Ghi file slice riêng cho báo cáo
    with open(RAW / "failure_slices.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["slice", "definition", "n_cases"])
        w.writerow(["symbol_heavy_statement", "≥5 ký hiệu Lean trong statement query", slice_counts["symbol_heavy_statement"]])
        w.writerow(["long_statement_gt200", ">200 ký tự", slice_counts["long_statement_gt200"]])
        w.writerow(["short_statement_lt40", "<40 ký tự", slice_counts["short_statement_lt40"]])
    print(f"✓ error slices theo ký hiệu/độ dài: {slice_counts}")


def task_runtime_repeats() -> None:
    """Mục 8: runtime biến động chạy ≥3 lần — đo hybrid S3 3 lần."""
    from systems import RetrievalSystem
    corpus = list(csv.DictReader(open(REAL / "corpus_s3.csv", encoding="utf-8")))
    queries = list(csv.DictReader(open(REAL / "queries_s3.csv", encoding="utf-8")))
    rows = []
    for run in range(1, 4):
        t0 = time.time()
        system = RetrievalSystem("hybrid", corpus)
        build_s = time.time() - t0
        t1 = time.perf_counter()
        for q in queries[:100]:  # 100 query đủ để đo biến động, tránh quá lâu
            system.search(q, top_k=50)
        search_s = time.perf_counter() - t1
        rows.append([run, f"{build_s:.2f}", f"{search_s / 100 * 1000:.1f}"])
        print(f"  repeat {run}: build {build_s:.2f}s, search {search_s / 100 * 1000:.1f} ms/query")
    builds = [float(r[1]) for r in rows]
    searches = [float(r[2]) for r in rows]
    with open(REAL / "runtime_repeats.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["repeat", "index_build_s", "search_ms_per_query_100q"])
        w.writerows(rows)
        w.writerow(["median", f"{statistics.median(builds):.2f}", f"{statistics.median(searches):.1f}"])
        w.writerow(["min", f"{min(builds):.2f}", f"{min(searches):.1f}"])
        w.writerow(["max", f"{max(builds):.2f}", f"{max(searches):.1f}"])
    print(f"✓ runtime_repeats.csv — median search {statistics.median(searches)} ms/query (3 repeats)")


if __name__ == "__main__":
    task_parquet()
    task_data_dictionary()
    task_index_size()
    task_error_slices()
    task_runtime_repeats()
    print("\nXong toàn bộ 4 bổ sung.")
