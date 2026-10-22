# Nhóm 3 — Lean Premise Retrieval (Sparse/Hybrid)

Hệ truy hồi premise (định lý/bổ đề) trong mathlib4 bằng từ khóa, ký hiệu và đặc trưng
cấu trúc — INT4418 Dữ liệu lớn, PTIT.

**Đã chạy trên dữ liệu thật:** LeanDojo Benchmark 4 (Zenodo DOI 10.5281/zenodo.12740403,
license CC-BY-2.0, mathlib4 commit `29dcec07`) — 180.907 declarations, 898 test queries
có premise ground truth, 3 mức scale 10K/50K/181K.

## Setup máy mới (nhà)

Gói này KHÔNG chứa dataset (~930 MB) — chạy 1 lệnh, script tự tải:

```bash
python download_data.py     # hoặc: bash download_data.sh (nếu dùng Git Bash)
```

Tải 68 MB từ Zenodo + giải nén + build corpus 181K declarations (~10 phút tùy mạng).
Script có: verify SHA-256 sau tải, chạy lại được (bước xong bị bỏ qua), hướng dẫn chi
tiết khi lỗi (mạng chặn, antivirus giữ file...).

**Chẩn đoán máy (chạy bất cứ lúc nào):**

```bash
python check_setup.py
```

Báo ✓/⚠/✗ từng hạng mục kèm cách sửa cụ thể nếu thiếu.

## Kết quả chính (số thật, tái lập được)

| Scale | BM25 thuần Recall@10 | **Hybrid Recall@10** | Hybrid P95 (ms) |
|---|---|---|---|
| 10K | 0.1368 | **0.1371** | 158.9 |
| 50K | 0.1611 | **0.1698** | 777.6 |
| **181K (full)** | 0.2129 | **0.2450 (+15%)** | **1662.5 (−23% vs BM25)** |

Hybrid đạt cả Recall cao hơn **và** P95 thấp hơn BM25 thuần ở full corpus → trả lời RQ2.
Ablation: structural reranking đóng góp −0.032 Recall@10 nếu bỏ (ở 181K); bỏ ký hiệu Lean:
−0.038. Load test 1/10/50 client: QPS ~5, P95 phình 25× → GIL là nút thắt (finding thật).

## Chạy nhanh

```bash
# 0. Unit test metrics (15/15 PASS)
python tests/test_metrics.py

# 1. Demo truy hồi (không cần build lại — dùng results/real có sẵn)
python scripts/search_cli.py "Every finite integral domain is a field" --top 5
python scripts/search_cli.py "continuous function compact" --system hybrid --show-statement

# 2. Tái lập toàn bộ thí nghiệm (dữ liệu thật đã tải ở data_raw/)
python scripts/build_real_corpus.py     # build corpus/queries/qrels 3 scale + manifest
python scripts/run_real_retrieval.py    # 4 hệ × 3 scale → run files + metrics + latency
python scripts/run_load_test.py         # load test 1/10/50 concurrent
python scripts/fill_gaps.py             # Parquet + data dictionary + index size/manifest + repeats
python scripts/run_ablation.py          # ablation → bảng + hình
python scripts/run_failure_analysis.py  # 30 failure cases + taxonomy
python scripts/run_comparison_n4.py     # comparison với Nhóm 4 (tự nhận run thật khi có)
python scripts/make_real_figures.py     # biểu đồ sinh từ raw

# (Phòng hờ khi chưa có dữ liệu thật — mock end-to-end)
python scripts/make_mock_end_to_end.py && python scripts/run_all_evaluations.py
```

## Cấu trúc

```
nhom3/
├── docs/
│   ├── data_contract_v1.md       # Data contract N3×N4 — ACTIVE (N3 công bố đơn phương)
│   ├── evaluation_protocol.md    # Protocol đánh giá v0.1
│   ├── decuong_1_trang.md        # Đề cương 1 trang (Phụ lục A)
│   ├── phan_vai_tam.md           # Phân vai tạm + người dự phòng
│   ├── report_draft.md           # BÁO CÁO v1.0 — số thật, đủ 8 mục theo Phụ lục C
│   └── ai_use_statement.md       # Khai báo dùng AI (bắt buộc của môn)
├── src/
│   ├── retrieval/
│   │   ├── tokenizer.py          # Lean statement tokenizer
│   │   ├── index.py              # BM25 inverted index
│   │   └── rankers.py            # bm25 / bm25_field / hybrid retrieval systems
│   └── evaluation/
│       ├── metrics.py            # Recall@k, MRR, nDCG@k
│       ├── contract.py           # Validator 6-field data contract
│       └── run_logger.py         # Run log 10 trường Phụ lục B
├── tests/test_metrics.py         # 15 unit tests — PASS
├── configs/query_set_v0.csv      # 20 truy vấn kiểm tra tuần 1
├── scripts/
│   ├── build_real_corpus.py      # Zenodo → corpus/queries/qrels 3 scale + checksum
│   ├── run_real_retrieval.py     # 4 hệ × 3 scale — chạy + đo + run logs
│   ├── run_load_test.py          # 1/10/50 concurrent → QPS/P50/P95
│   ├── search_cli.py             # CLI demo truy hồi
│   ├── run_ablation.py / run_failure_analysis.py / run_comparison_n4.py
│   ├── make_real_figures.py / make_figures.py
│   ├── make_mock_end_to_end.py / run_all_evaluations.py  # (mock phòng hờ)
│   └── demo_evaluation.py        # demo tuần 1
├── data_raw/leandojo_benchmark_4/  # dữ liệu Zenodo đã giải nén (68 MB, không đưa Git)
├── results/
│   ├── real/                     # corpus/queries/qrels/run × 3 scale + latency + load test
│   │   └── split_manifest.json   # checksum SHA-256 từng file
│   ├── raw/                      # eval_summary + ablation + failure + 33 run logs JSON
│   └── figures/                  # 9 PNG sinh bằng script
└── contributions.md              # vai trò + phần bảo vệ từng thành viên
```

## Data contract với Nhóm 4

`docs/data_contract_v1.md` — **ACTIVE**, Nhóm 3 công bố đơn phương (N4 không phản hồi).
Nhóm 4 tham gia sau chỉ cần: đọc contract → encode corpus `results/real/corpus_*.csv` →
giao `run_dense_real_{scale}.csv` (cột `query_id, premise_id`) → đặt vào `results/real/`
→ chạy `run_comparison_n4.py` là bảng so sánh tự cập nhật trên cùng split.

## Quy tắc bắt buộc của nhóm

1. **Dự phòng:** mỗi vai có người dự phòng chạy lại được trước tuần 7 (`phan_vai_tam.md`).
2. **Run log:** mọi run qua `run_logger.py` — 10 trường Phụ lục B, tự ghi tay là vi phạm.
3. **Mock ≠ thật:** số mock chỉ dùng khi chưa có dữ liệu; bảng trong báo cáo ghi rõ nguồn.
4. **Bảo vệ:** mọi thành viên giải thích được toàn pipeline, không chỉ phần mình.

## Data/extraction (N3 / N4)

The canonical source for the two groups is the frozen `n4_shared.zip`
(`leandojo-benchmark-4@29dcec07+split-v1.0`). **Do not regenerate a different
split** when comparing N3 and N4. To validate the supplied snapshot:

```bash
python scripts/verify_n4_shared.py data_raw/n4_shared.zip
```

> **Note on line endings:** The canonical `n4_shared.zip` uses Windows-style
> line endings (`CRLF`, `\r\n`) for `corpus.jsonl` and `queries.jsonl`.
> If you regenerate the package with `scripts/export_n4_shared.py`, it already
> writes `CRLF`; manually created files must use `CRLF` to match the frozen
> SHA-256 hashes below.
>
> Frozen SHA-256:
> - `corpus.jsonl`:  `c9157bd1381ca4147aa931f14b9985ac9bfe5cbfe892a982a24a133ff4221efd`
> - `queries.jsonl`: `c2b764fafe981755ae7ca2614912498f0559317ea5427bcb7a7150cb45166004`

See [`docs/HOANG_DATA_HANDOFF.md`](docs/HOANG_DATA_HANDOFF.md) for exact
schema, SHA-256 hashes, query eligibility, and handoff rules. Existing scripts
remain available; this validator is non-destructive.
