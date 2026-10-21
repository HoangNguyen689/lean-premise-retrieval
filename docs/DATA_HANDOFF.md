# Data/extraction: N3 ↔ N4 frozen benchmark

## Scope
The source of truth is the **attached** `n4_shared.zip`, not an independently rebuilt split. Existing group code for indexing, BM25, hybrid and serving is untouched. The original group ZIP is the baseline. This module validates the shared data instead of rewriting it.

## Frozen provenance

- Source: LeanDojo Benchmark 4, mathlib4 commit `29dcec074de168ac2bf835a77ef68bbe069194c5`
- Data version: `leandojo-benchmark-4@29dcec07+split-v1.0`
- Pool: `shared-frozen-pool`
- Corpus: 180,907 documents; SHA-256 `c9157bd1381ca4147aa931f14b9985ac9bfe5cbfe892a982a24a133ff4221efd`
- Queries: 898; SHA-256 `c2b764fafe981755ae7ca2614912498f0559317ea5427bcb7a7150cb45166004`

## Exact N4 interface

`corpus.jsonl` fields: `id`, `name` (= full_name = id), `statement`, `namespace`, `source_commit`.

`queries.jsonl` fields: `id` (`Q` + theorem full_name), `statement`, `relevant_ids`, `split` (`test`), `pool_id` (`shared-frozen-pool`).

`relevant_ids` are only directly-used proof-trace premises (not same-file weak labels). The frozen N4 file has **16 queries with empty `relevant_ids`**; do not silently exclude these queries or rewrite the file, as this changes the SHA-256 and shared benchmark. Specify metric handling explicitly. Self theorem is *ineligible* for retrieval. Remove self before top-K truncation. **Other test theorems remain eligible**, including 56 reported label-2 cases. Never change source bytes if checksums must remain frozen.

## Run

Copy `n4_shared.zip` to `data_raw/n4_shared.zip` (ignored by Git) and run:

```bash
python scripts/verify_n4_shared.py data_raw/n4_shared.zip
python -m unittest discover -s tests -p 'test_*.py' -v
```

This produces `results/data_quality/shared_validation.json` and checks full raw SHA-256, schema, type, uniqueness, foreign keys, self eligibility and pinned snapshot. For compliance with the course instructions, do **not** push the 66 MB JSONL data or ZIP to Git; store it separately and version the manifest and verification program.

## N4 handoff

N4 receives the unmodified shared bundle and returns `run_dense_*.csv` with columns `query_id,premise_id`. This data component does not evaluate dense runs, fix other members' results or claim legacy CSV metrics are accurate. It only freezes and validates the official benchmark interface.
