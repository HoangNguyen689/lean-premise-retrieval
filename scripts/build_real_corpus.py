"""Build corpus + queries + qrels THẬT từ LeanDojo Benchmark 4 (Zenodo v12740403).

TV1 (Data/Extraction) — chạy 1 lần sau khi tải data_raw/leandojo_benchmark_4/.

Đầu ra (theo docs/data_contract_v1.md, ghi vào results/real/):
  corpus_full.parquet/.csv   — ~181K declarations (6-field contract)
  queries_full.parquet/.csv  — ~898 test queries có premise ground truth
  qrels_full.csv             — nhãn 2 = premise dùng trực tiếp trong chứng minh (từ trace)
  split_manifest.json        — checksum + số lượng + data_version

Ba mức scale S1/S2/S3: corpus sort theo id, queries sort theo full_name —
S1 ⊂ S2 ⊂ S3 đúng theo contract §5.1.

Chạy:  python scripts/build_real_corpus.py
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

# Windows console (CMD) thường dùng cp1252/cp437 — không chứa chữ tiếng Việt.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
BENCH = ROOT / "data_raw" / "leandojo_benchmark_4"
OUT = ROOT / "results" / "real"
sys.path.insert(0, str(ROOT / "src" / "evaluation"))

DATA_VERSION = "leandojo-benchmark-4@29dcec07+split-v1.0"
MATHLIB_COMMIT = "29dcec074de168ac2bf835a77ef68bbe069194c5"

SCALES = {"s1": (10_000, 200), "s2": (50_000, 500), "s3": (None, None)}  # None = full


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_path(p: str) -> str:
    """'.lake/packages/mathlib/Mathlib/Analysis/...' → 'Mathlib/Analysis/...'."""
    marker = "Mathlib/"
    i = p.find(marker)
    return p[i:] if i >= 0 else p


def extract_premises(t: dict) -> set[str]:
    """Premise ground truth = full_name xuất hiện trong annotated_tactic của trace."""
    prems = set()
    for tt in t.get("traced_tactics") or []:
        at = tt.get("annotated_tactic") or []
        if isinstance(at, list) and len(at) >= 2 and isinstance(at[1], list):
            for prem in at[1]:
                fn = prem.get("full_name")
                if fn:
                    prems.add(fn)
    return prems


def main() -> int:
    if not BENCH.exists():
        print(f"Thiếu {BENCH}. Tải theo docs/data_contract_v1.md §9 (Zenodo).")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)

    # ── 1. Corpus: mọi declaration từ corpus.jsonl ──
    corpus = []
    ns_counter: Counter = Counter()
    with open(BENCH / "corpus.jsonl", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            fp = clean_path(rec["path"])
            for p in rec["premises"]:
                code = p.get("code", "")
                # namespace = phần trước tên cuối của full_name
                fn = p["full_name"]
                ns = fn.rsplit(".", 1)[0] if "." in fn else ""
                corpus.append({
                    "id": fn,
                    "statement": code,
                    "statement_natural": "",  # benchmark không có bản tự nhiên — contract cho phép rỗng
                    "namespace": ns,
                    "file_path": fp,
                    "line_start": p["start"][0],
                })
    # de-dup theo id (declaration trùng tên giữa các file)
    seen = set()
    dedup = []
    for r in corpus:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        dedup.append(r)
    corpus = dedup
    print(f"Corpus: {len(corpus)} declarations (de-dup từ corpus.jsonl)")

    # ── 2. Queries: test split, chỉ lấy query có premise GT ──
    test = json.load(open(BENCH / "random" / "test.json"))
    queries, qrels = [], []
    for t in test:
        prems = extract_premises(t)
        if not prems:
            continue
        qid = "Q" + t["full_name"]  # id = Q + full_name (duy nhất, dễ truy vết)
        queries.append({
            "id": qid,
            "statement": t["full_name"],  # fallback; sẽ được thay bằng statement thật bên dưới
            "statement_natural": "",
            "namespace": (t["full_name"].rsplit(".", 1)[0] if "." in t["full_name"] else ""),
            "file_path": clean_path(t["file_path"]),
            "line_start": t["start"][0],
        })
        qrels.append((qid, t))  # giữ tạm để lấy statement sau
    print(f"Queries: {len(queries)} (test split, có premise GT)")

    # ── 3. Statement query: đọc từ corpus code (theorem text) nếu có, else full_name ──
    # LeanDojo test.json không chứa statement text; dùng full_name + file_path làm field,
    # statement thật lấy từ corpus theo full_name nếu tìm thấy.
    corpus_by_id = {r["id"]: r for r in corpus}
    for q in queries:
        src = corpus_by_id.get(q["id"][1:])
        if src:
            q["statement"] = src["statement"]
            q["namespace"] = src["namespace"]

    # qrels: nhãn 2 = premise GT từ trace; chỉ giữ premise có trong corpus
    qrels_rows = []
    for qid, t in qrels:
        for pid in sorted(extract_premises(t)):
            if pid in corpus_by_id:
                qrels_rows.append([qid, pid, 2])
    n_q2 = len(qrels_rows)
    # nhãn 1: premise cùng file_path với 1 premise nhãn 2 (liên quan gián tiếp, bán tự động)
    file_of = {r["id"]: r["file_path"] for r in corpus}
    for qid, t in qrels:
        gold_files = {file_of[pid] for pid, _, rel in [(p, 0, 2) for p, _, _ in []]}  # placeholder
    # (tính lại đúng)
    qrels_rows = []
    for qid, t in qrels:
        golds = sorted(p for p in extract_premises(t) if p in corpus_by_id)
        gold_files = {file_of[p] for p in golds}
        partials = set()
        for pid, fp in file_of.items():
            if pid not in set(golds) and fp in gold_files:
                partials.add(pid)
        # giới hạn partial ≤ 10 để qrels không phình
        for pid in sorted(partials)[:10]:
            qrels_rows.append([qid, pid, 1])
        for pid in golds:
            qrels_rows.append([qid, pid, 2])
    print(f"Qrels: {len(qrels_rows)} nhãn (2 = {n_q2 if (n_q2 := sum(1 for r in qrels_rows if r[2]==2)) else 0}, 1 = {sum(1 for r in qrels_rows if r[2]==1)})")

    # ── 4. Ghi full + 3 scale ──
    corpus.sort(key=lambda r: r["id"])
    queries.sort(key=lambda r: r["id"])

    def write_csv(path: Path, rows: list[dict]) -> None:
        import csv
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["id", "statement", "statement_natural",
                                              "namespace", "file_path", "line_start"])
            w.writeheader()
            w.writerows(rows)

    write_csv(OUT / "corpus_full.csv", corpus)
    write_csv(OUT / "queries_full.csv", queries)
    import csv as _csv
    with open(OUT / "qrels_full.csv", "w", encoding="utf-8", newline="") as f:
        w = _csv.writer(f)
        w.writerow(["query_id", "premise_id", "relevance"])
        w.writerows(qrels_rows)

    manifest = {
        "data_version": DATA_VERSION,
        "mathlib_commit": MATHLIB_COMMIT,
        "source": "Zenodo DOI 10.5281/zenodo.12740403 (LeanDojo Benchmark 4)",
        "license": "CC-BY-2.0",
        "splits": {},
    }
    for scale, (n_corpus, n_query) in SCALES.items():
        c = corpus if n_corpus is None else corpus[:n_corpus]
        qs = queries if n_query is None else queries[:n_query]
        # qrels của scale: chỉ query thuộc scale; gold premise phải nằm trong corpus của scale
        cids = {r["id"] for r in c}
        qids = {q["id"] for q in qs}
        qrels_scale = [row for row in qrels_rows
                       if row[0] in qids and (row[2] == 0 or row[1] in cids)]
        write_csv(OUT / f"corpus_{scale}.csv", c)
        write_csv(OUT / f"queries_{scale}.csv", qs)
        with open(OUT / f"qrels_{scale}.csv", "w", encoding="utf-8", newline="") as f:
            w = _csv.writer(f)
            w.writerow(["query_id", "premise_id", "relevance"])
            w.writerows(qrels_scale)
        manifest["splits"][scale] = {
            "corpus": len(c), "queries": len(qs), "qrels": len(qrels_scale),
        }
        print(f"  {scale}: corpus {len(c)}, queries {len(qs)}, qrels {len(qrels_scale)}")

    # ── 5. Manifest + checksum ──
    for p in sorted(OUT.glob("*.csv")):
        manifest.setdefault("checksums", {})[p.name] = sha256(p)
    (OUT / "split_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest: {OUT / 'split_manifest.json'}")
    print(f"DATA_VERSION={DATA_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
