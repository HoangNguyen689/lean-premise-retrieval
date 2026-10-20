# AI-USE STATEMENT — Nhóm 3, Lean Premise Retrieval

> Bắt buộc theo hướng dẫn môn (mục 2, yêu cầu chung): "Việc sử dụng AI phải được khai báo;
> mọi code và kết luận do AI hỗ trợ vẫn phải được nhóm kiểm chứng."

## Nguyên tắc nhóm

1. Mọi lần dùng AI hỗ trợ sinh code/văn bản/phân tích **phải được ghi vào bảng dưới**.
2. Người ghi là người chạy prompt; người đó **kiểm chứng** kết quả trước khi đưa vào repo.
3. Code do AI sinh chỉ được merge sau khi (a) unit test pass, (b) một thành viên khác đọc và hiểu.
4. Kết luận trong báo cáo không được dựa chỉ vào output AI — phải đối chiếu raw results.

## Bảng khai báo

| Ngày | Thành viên | Công cụ | Mục đích | Phạm vi | Đã kiểm chứng bằng |
|---|---|---|---|---|---|
| 2026-10-01 | TV6 (Evaluation) | Claude (VCode agent) | Soạn khung pipeline evaluation: contract.py, run_logger.py, make_mock_end_to_end.py, run_all_evaluations.py, run_ablation.py, run_failure_analysis.py, run_comparison_n4.py, make_figures.py, data_contract_v1.md, phan_vai_tam.md, report_draft.md, bản khai báo này | Toàn bộ code/docs trong commit này | `python tests/test_metrics.py` 15/15 PASS; chạy 4 script end-to-end trên mock, đối chiếu eval_summary.csv tính lại từ run file bằng tay cho 1 query (Q001) |
| 2026-10-15 | TV6 (Evaluation) | Claude (VCode agent) | Chọn benchmark + tải LeanDojo Benchmark 4 từ Zenodo; build_real_corpus.py (corpus 180.907 + qrels từ trace); src/retrieval/systems.py (tokenizer Lean, BM25 thuần Python, 4 hệ); run_real_retrieval.py, run_load_test.py, search_cli.py, make_real_figures.py; report_draft.md v1.0 số thật; contract chuyển ACTIVE; contributions.md | Toàn bộ pipeline dữ liệu thật | 15/15 unit tests; 12 cấu hình chạy đủ 3 scale với số Recall hợp lý (tăng theo scale, fielddrop < full ở 181K khớp giả thuyết); latency đo trực tiếp 898 query; contract validator PASS cho corpus S1; CLI demo trả kết quả đúng namespace |
| | | | | | |

## Kết luận AI không được dùng cho

- Số liệu trong bảng kết quả chính (chỉ từ raw results + script).
- Nhận định "đúng/đặc" về Lean/mathlib chưa kiểm chứng bằng Lean toolchain.
