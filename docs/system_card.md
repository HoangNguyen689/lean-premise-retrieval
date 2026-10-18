# System card — Lean premise search (Nhóm 3) v0.1

## Mục đích
Gợi ý top-k premise trong mathlib4 cho một trạng thái chứng minh Lean, dùng làm bước truy hồi trước bộ chứng minh.
Không chứng minh định lý và không bảo đảm premise được gợi ý dùng được: Lean vẫn là bên kiểm chứng cuối cùng.

## Thành phần
| Thành phần | Mô tả | Học từ dữ liệu? |
|---|---|---|
| Tokenizer `default-v1` | chữ thường, `\w+` | không |
| Tokenizer `lean-v1` | tách tên theo `.`, `_`, camelCase; giữ ký hiệu toán; bỏ biến một chữ cái | không (luật viết tay) |
| BM25 / BM25F | k1, b, trọng số field, query_tf | tham số tinh trên random/val |
| Bộ lọc truy cập được | bao đóng import của file + khai báo xong trước theorem trong cùng file | không |
| Popularity, PageRank | từ đồ thị theorem → premise của train nửa A | có (train A) |
| Reranker | logistic regression 11–13 đặc trưng, top-100 ứng viên | có (train nửa B, 6.000 truy vấn) |

Trọng số reranker: `results/models/*.json` (có mean/std chuẩn hóa, hệ số, cấu hình huấn luyện).

## Dữ liệu huấn luyện và đánh giá
LeanDojo Benchmark 4 v10 (mathlib commit `29dcec07`). Huấn luyện/thống kê chỉ trên train; tinh tham số trên val;
báo cáo trên test của `random` và `novel_premises`. Chi tiết: `docs/benchmark_spec.md`, `docs/data_card.md`.

## Hiệu năng
Xem `results/figures/quality.md` (chất lượng, kiểm định bootstrap) và `results/figures/scale_tables.md` (độ trễ, thông lượng,
build). Số liệu đo trên một máy Windows 11, 12 luồng CPU, 32 GB RAM (chi tiết trong từng run record).

## Giới hạn đã biết
- Recall@10 tốt nhất khoảng một phần tư: phần lớn premise đúng vẫn không vào top-10. 82% premise đúng bị bỏ lỡ
  nằm ngoài top-100 của stage 1, nên reranker không cứu được (`results/figures/error_slices.md`).
- Premise phổ biến dùng ở mọi nơi (ví dụ lemma về `≤`, `+`) ít trùng từ vựng với goal, khó tìm bằng từ khóa.
- Popularity thiên vị premise đã được dùng nhiều trong train; với `novel_premises` (premise mới), đặc trưng này bằng 0.
- Bộ lọc truy cập được cần biết file và vị trí theorem; nếu thiếu ngữ cảnh, hệ thống tự tắt bộ lọc (cho phép mọi premise).
- Phục vụ bằng Python: mỗi tiến trình bị GIL giới hạn; thông lượng tăng bằng nhiều worker, không bằng nhiều luồng.
- Spark chạy local mode trên Windows: không dùng được daemon fork của PySpark nên overhead mỗi task lớn
  (xem threats to validity trong báo cáo).

## Sử dụng có trách nhiệm
Gợi ý chỉ là ứng viên; không suy ra tính đúng của chứng minh từ việc một premise được xếp hạng cao.
