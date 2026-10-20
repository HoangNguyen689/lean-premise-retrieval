# Lean Premise Retrieval — Nhóm 3 (PTIT INT4418)

Sparse / structural / hybrid premise retrieval for Lean 4 and mathlib4.

## Hoàng — Data/extraction

The pinned shared N3/N4 benchmark is used **unchanged**:

- Dataset: LeanDojo Benchmark 4, mathlib4 commit `29dcec074de168ac2bf835a77ef68bbe069194c5`
- `data_version`: `leandojo-benchmark-4@29dcec07+split-v1.0`
- Corpus: 180,907 declarations with keys `id,name,statement,namespace,source_commit`
- Queries: 898 test queries with keys `id,statement,relevant_ids,split,pool_id`
- `pool_id`: `shared-frozen-pool`
- Relevant premises: directly used from proof traces
- Eligibility: exclude the query's own theorem *before* taking top-k; do not drop other test theorems

### Verify the shared snapshot

Place the provided `n4_shared.zip` at `data_raw/n4_shared.zip`, then:

```bash
python scripts/verify_n4_shared.py data_raw/n4_shared.zip
python -m unittest discover -s tests -p 'test_*.py' -v
```

Verification checks full SHA-256 hashes, dataset sizes, record schemas, uniqueness, referential integrity and self-match labels. A JSON report is written to `results/data_quality/shared_validation.json`.

See [Hoàng's data handoff](docs/HOANG_DATA_HANDOFF.md) and [pinned checksums](configs/n4_shared_manifest.json).

## Repository import status

The Data/extraction module has been pushed. Remaining group source (retrieval, performance, evaluation and related scripts) is available in the original integration archive and is **not yet fully imported to this GitHub repository**. Large dataset files are intentionally excluded from Git.
