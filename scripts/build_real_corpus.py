"""Build real corpus, queries, and qrels from LeanDojo Benchmark 4.

TV1 (Data/Extraction) - run once after extracting data_raw/leandojo_benchmark_4/.

Outputs (written to results/real/):
  corpus_{s1,s2,s3,full}.csv   - declarations
  queries_{s1,s2,s3,full}.csv  - test queries with premise ground truth
  qrels_{s1,s2,s3,full}.csv    - relevance labels (2 = direct premise, 1 = same-file)
  split_manifest.json          - checksums + counts + data_version

Scales S1/S2/S3 are nested subsets sorted by id (corpus) and full_name (queries).
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

# Windows consoles often use cp1252/cp437; force UTF-8 so Unicode symbols print correctly.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]

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
    """Convert '.lake/packages/mathlib/Mathlib/...' to 'Mathlib/...'."""
    marker = "Mathlib/"
    i = p.find(marker)
    return p[i:] if i >= 0 else p


def extract_premises(t: dict) -> set[str]:
    """Ground-truth premises = full_names appearing in the annotated tactic trace."""
    prems = set()
    for tt in t.get("traced_tactics") or []:
        at = tt.get("annotated_tactic") or []
        if isinstance(at, list) and len(at) >= 2 and isinstance(at[1], list):
            for prem in at[1]:
                fn = prem.get("full_name")
                if fn:
                    prems.add(fn)
    return prems


def write_csv(path: Path, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["id", "statement", "statement_natural",
                        "namespace", "file_path", "line_start"],
        )
        w.writeheader()
        w.writerows(rows)


def build_corpus() -> list[dict]:
    print("Building corpus from corpus.jsonl...")
    corpus = []
    with open(BENCH / "corpus.jsonl", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            fp = clean_path(rec["path"])
            for p in rec["premises"]:
                code = p.get("code", "")
                fn = p["full_name"]
                ns = fn.rsplit(".", 1)[0] if "." in fn else ""
                corpus.append({
                    "id": fn,
                    "statement": code,
                    "statement_natural": "",  # benchmark has no natural statement
                    "namespace": ns,
                    "file_path": fp,
                    "line_start": p["start"][0],
                })

    # De-duplicate declarations that appear in multiple files
    seen = set()
    dedup = []
    for r in corpus:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        dedup.append(r)

    print(f"  {len(dedup)} declarations after de-duplication")
    return dedup


def build_queries(corpus_by_id: dict[str, dict]) -> tuple[list[dict], list[tuple[str, dict]]]:
    print("Building queries from random/test.json...")
    test = json.load(open(BENCH / "random" / "test.json"))

    # Cache premise extraction per test theorem
    premise_cache: dict[str, set[str]] = {}

    queries = []
    qrels = []
    for t in test:
        tname = t["full_name"]
        prems = premise_cache.setdefault(tname, extract_premises(t))
        if not prems:
            continue
        qid = "Q" + tname
        ns = tname.rsplit(".", 1)[0] if "." in tname else ""
        queries.append({
            "id": qid,
            "statement": tname,  # fallback; replaced by corpus code below if found
            "statement_natural": "",
            "namespace": ns,
            "file_path": clean_path(t["file_path"]),
            "line_start": t["start"][0],
        })
        qrels.append((qid, t))

    # Replace fallback statement with actual corpus code when available
    for q in queries:
        src = corpus_by_id.get(q["id"][1:])
        if src:
            q["statement"] = src["statement"]
            q["namespace"] = src["namespace"]

    print(f"  {len(queries)} queries with premise ground truth")
    return queries, qrels


def build_qrels(
    qrels: list[tuple[str, dict]],
    corpus_by_id: dict[str, dict],
    file_of: dict[str, str],
    ids_by_file: dict[str, set[str]],
) -> list[list]:
    print("Building qrels (direct + same-file partial premises)...")
    qrels_rows = []
    n_gold_total = 0
    for i, (qid, t) in enumerate(qrels, 1):
        if i % 100 == 0 or i == len(qrels):
            print(f"  processing query {i}/{len(qrels)}")
        golds_set = {p for p in extract_premises(t) if p in corpus_by_id}
        golds = sorted(golds_set)
        n_gold_total += len(golds)
        gold_files = {file_of[p] for p in golds}

        # Partial relevance = declarations in the same file as a direct premise
        partials = set()
        for gf in gold_files:
            for pid in ids_by_file.get(gf, ()):
                if pid not in golds_set:
                    partials.add(pid)

        for pid in sorted(partials)[:10]:
            qrels_rows.append([qid, pid, 1])
        for pid in golds:
            qrels_rows.append([qid, pid, 2])

    n_partial = sum(1 for r in qrels_rows if r[2] == 1)
    print(f"  {len(qrels_rows)} labels ({n_gold_total} direct, {n_partial} partial)")
    return qrels_rows


def main() -> int:
    if not BENCH.exists():
        print(f"Missing {BENCH}. Download data first: python download_data.py")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)

    corpus = build_corpus()
    corpus.sort(key=lambda r: r["id"])
    corpus_by_id = {r["id"]: r for r in corpus}
    file_of = {r["id"]: r["file_path"] for r in corpus}
    ids_by_file: dict[str, set[str]] = defaultdict(set)
    for r in corpus:
        ids_by_file[r["file_path"]].add(r["id"])

    queries, qrels = build_queries(corpus_by_id)
    queries.sort(key=lambda r: r["id"])

    qrels_rows = build_qrels(qrels, corpus_by_id, file_of, ids_by_file)

    write_csv(OUT / "corpus_full.csv", corpus)
    write_csv(OUT / "queries_full.csv", queries)
    with open(OUT / "qrels_full.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
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
        cids = {r["id"] for r in c}
        qids = {q["id"] for q in qs}
        qrels_scale = [row for row in qrels_rows
                       if row[0] in qids and (row[2] == 0 or row[1] in cids)]
        write_csv(OUT / f"corpus_{scale}.csv", c)
        write_csv(OUT / f"queries_{scale}.csv", qs)
        with open(OUT / f"qrels_{scale}.csv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["query_id", "premise_id", "relevance"])
            w.writerows(qrels_scale)
        manifest["splits"][scale] = {
            "corpus": len(c), "queries": len(qs), "qrels": len(qrels_scale),
        }
        print(f"  {scale}: corpus {len(c)}, queries {len(qs)}, qrels {len(qrels_scale)}")

    for p in sorted(OUT.glob("*.csv")):
        manifest.setdefault("checksums", {})[p.name] = sha256(p)
    (OUT / "split_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest: {OUT / 'split_manifest.json'}")
    print(f"DATA_VERSION={DATA_VERSION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
