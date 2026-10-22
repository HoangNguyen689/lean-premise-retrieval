# CONTRIBUTIONS.md — Nhóm 3, Lean Premise Retrieval

> Điền tên thật khi nhóm họp chốt (`docs/phan_vai_tam.md`). Mỗi thành viên phải có vai
> chính + dự phòng; khi bảo vệ mọi người phải hiểu toàn bộ pipeline.

| Thành viên | Vai chính | Vai dự phòng | Phần đã có sẵn trong repo | Phần tự làm thêm | Minh chứng bảo vệ | Ký |
|---|---|---|---|---|---|---|
| *(điền tên)* — TV1 | Data/Extraction | TV6 | `scripts/build_real_corpus.py` — đã build corpus 180.907 declarations + 3 scale + manifest checksum từ Zenodo | Kiểm tra lại checksum; viết data card chi tiết; cập nhật khi mathlib commit mới | Trình bày schema 6-field, provenance trace → qrels | |
| *(điền tên)* — TV2 | Indexing | TV3 | `src/retrieval/rankers.py::BM25Index` — inverted index + df/idf | Benchmark index build time từng scale; thử compress index | Giải thích inverted index, avgdl, BM25 params | |
| *(điền tên)* — TV3 | BM25 Baseline | TV4 | `RetrievalSystem("bm25"/"bm25_fielddrop")` — baseline đã chạy 3 scale | Tinh chỉnh k1/b trên dev split; thử OpenSearch so sánh | Giải thích công thức BM25, tại sao k1=1.5 b=0.75 | |
| *(điền tên)* — TV4 | Structural Features | TV3 | `RetrievalSystem("bm25_field"/"hybrid")` — field weights + reranker | Tuning hệ số 0.35/0.20 trên dev; thử dependency features | Giải thích stage 1/2 của hybrid | |
| *(điền tên)* — TV5 | Serving/Performance | TV6 | `scripts/run_load_test.py`, `scripts/search_cli.py` — load test 1/10/50 + CLI | Ghi kết quả load test vào báo cáo; thử multiprocessing hoá | Giải thích GIL bottleneck, QPS/P95 | |
| *(tên bạn)* — TV6 | Evaluation/Error Analysis | TV3 | `src/evaluation/*` + `scripts/run_*.py` — toàn bộ eval pipeline, ablation, 30 failure cases, comparison, run logger, report draft | Verify số bằng tay 1 query; chuẩn bị slide bảo vệ | Giải thích Recall/MRR/nDCG, pooling, threats to validity | |

## Lịch sử issue/PR chính (điền khi có repo Git)

| Issue/PR | Người | Mô tả | Trạng thái |
|---|---|---|---|
| #1 | TV6 | Data contract v1 + evaluation protocol | DONE (contract ACTIVE) |
| #2 | TV6 | Mock end-to-end pipeline (phòng hờ) | DONE — chuyển sang real |
| #3 | TV1 | Tải LeanDojo Benchmark 4 từ Zenodo + build corpus | DONE (TV6 làm hộ) |
| #4 | TV2/3/4 | 4 hệ retrieval + tokenizer Lean | DONE (TV6 làm hộ, chờ tuning) |
| #5 | TV5 | Load test + CLI | DONE (TV6 làm hộ) |
| #6 | TV6 | Ablation + failure + report v1 | DONE |
