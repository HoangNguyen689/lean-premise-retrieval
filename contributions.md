# Contributions — Nhóm 3

Cập nhật mỗi tuần. Mỗi dòng ghi việc đã làm kèm bằng chứng (commit, PR, issue, file kết quả).
Phân vai lấy từ "Nhóm 3 - Big Data - 2026.docx"; hai vai trò còn trống cần nhóm chốt. Việc cần chạy lại và giải thích
của từng vai trò: `docs/role_guides.md`.

| Vai trò | Người chính | Dự phòng | Phần mã / tài liệu phụ trách | Phần bảo vệ |
|---|---|---|---|---|
| Data/extraction | Nguyễn Đức Hoàng (B25CHHT096) | Nguyễn Ngọc Minh | `scripts/download_data.py`, `src/n3/extract/`, `scripts/make_subsets.py`, `scripts/make_sample.py`, `docs/data_card.md`, `docs/license_note.md` | Nguồn, giấy phép, data contract, dead-letter, vì sao 115K premise đúng bị loại |
| Indexing | Trần Duy Khánh (B25CHHT100) | (người phụ trách Serving) | `src/n3/index/` (build_seq, build_spark, codec), `scripts/run_scale.py --part build` | MapReduce build, partition/skew/salting, nén d-gap/VB/gamma, overhead Spark trên Windows |
| BM25 baseline | Nguyễn Mạnh Cường (B25CHHT082) | (người phụ trách Structural) | `src/n3/analysis/tokenizer.py`, `src/n3/retrieval/search.py`, `scripts/tune_bm25.py`, configs B0/B0t/V1/V2 | Công thức BM25/BM25F, tokenizer Lean, tinh tham số chỉ trên val |
| Structural features | **chưa chốt** (Vũ Trung Kiên B25CHHT101 hoặc Trần Đình Dũng B25CHHT089) | Nguyễn Mạnh Cường | `src/n3/retrieval/features.py`, `rerank.py`, `scripts/build_dependency_stats.py`, `scripts/train_reranker.py` | Đặc trưng cấu trúc, PageRank, bộ lọc truy cập được, chống rò rỉ train A/B |
| Serving/performance | **chưa chốt** (Vũ Trung Kiên hoặc Trần Đình Dũng) | Trần Duy Khánh | `src/n3/serving/`, `src/n3/eval/loadtest.py`, `scripts/run_scale.py --part serve`, môi trường `.venv`/`.venv-spark` | API, warm-up, GIL và nhiều worker, P95 dưới tải |
| Evaluation/error analysis | Nguyễn Ngọc Minh (B25CHHT106) | Nguyễn Đức Hoàng | `src/n3/eval/metrics.py`, `run_eval.py`, `scripts/summarize_quality.py`, `scripts/ablation.py`, `scripts/error_analysis.py`, `scripts/make_figures.py`, `docs/benchmark_spec.md` | Metric, bootstrap, ablation, 30 failure case, so sánh với Nhóm 4 |

## Nhật ký

| Tuần | Ngày | Ai | Việc | Bằng chứng |
|---|---|---|---|---|
| 1–9 | 2026-10-17 | (AI hỗ trợ, xem docs/ai_use_statement.md) | Dựng repo, pipeline B0–V4, Spark build, API, thí nghiệm quy mô (build 78 lần chạy, tải 36 lần), ablation, error analysis, bản nháp báo cáo | toàn bộ repo; results/raw; results/figures; report/ |
| 8 | 2026-10-17 | (AI hỗ trợ) | Phát hiện và sửa lỗi bộ lọc để lọt chính theorem (42% truy vấn test); thêm test hồi quy; chạy lại V2a/V4 | tests/test_accessible.py; docs/benchmark_spec.md |
| 1, 2, 5 | 2026-10-18 | (AI hỗ trợ) | Bổ sung sản phẩm còn thiếu: 20 truy vấn kiểm tra, data dictionary, ablation plan, latency profile theo bước; KTC bootstrap cho ablation; sửa lỗi làm tròn hai lần trong ablation.py (sai lệch ≤ 0,001); hướng dẫn theo vai trò | docs/check_queries.md; docs/data_dictionary.md; docs/ablation_plan.md; results/figures/latency_profile.md; results/figures/ablation_significance.md; docs/role_guides.md |
| 7 | 2026-10-18 | (AI hỗ trợ) | Viết lại job Spark (engine Arrow: executor đọc Parquet, gộp posting theo partition, shuffle trong JVM); thí nghiệm build2 trên Windows và Linux (Docker), 194 lần chạy, chỉ mục trùng từng byte; Spark nhanh hơn tuần tự tới 3,84 lần ở 3,6 triệu bản ghi | src/n3/index/build_spark_arrow.py; tests/test_spark_arrow_logic.py; docker/; results/figures/scale_tables.md |
| 5, 6, 8 | 2026-10-18 | (AI hỗ trợ) | V5: ứng viên bổ sung theo lịch sử sử dụng (chỉ theorem có trước), chọn trên validation; test random R@10 0,243 → 0,281. Baseline Lucene: cùng kết quả với B0, nhanh hơn khoảng 5 lần. Thí nghiệm 4/8/12 worker và kiểm tra CPU: dịch vụ bị giới hạn bởi CPU. Báo cáo rút về 20 trang phần thân | configs/v5_rerank_expand.yaml; scripts/tune_v5.py; scripts/lucene_baseline.py; scripts/serve_cpu_check.py; tests/test_usage_causal.py |
| | | | | |
