# Latency profile theo giai đoạn (sinh bởi scripts/profile_latency.py)

Một luồng, index toàn bộ (180.957 premise), 500 truy vấn `scale_random_test_500`. Đơn vị: ms. Lượt *lạnh*: cache posting rỗng lúc bắt đầu; lượt *nóng*: chạy lại cùng truy vấn với cache đã đầy. Tổng của trung vị từng bước không bằng trung vị của tổng. Cache LRU giữ 4.096 posting đã giải mã nên đầy sau vài truy vấn đầu; vì vậy hai lượt gần như bằng nhau và phần còn lại là chi phí cộng điểm trên posting dài.

## Lượt lạnh: trung vị (P95) theo bước

| Biến thể | tokenize | bm25_score | accessible_mask | filter_topk | features | rerank_sort | Tổng | Tỉ lệ BM25 trong tổng (trung bình) |
|---|---|---|---|---|---|---|---|---|
| B0 | 0.03 (0.08) | 12.73 (23.75) | 0.00 (0.00) | 0.68 (1.09) | — | — | 13.39 (24.94) | 95% |
| V2 | 0.17 (0.54) | 19.66 (36.01) | 0.00 (0.00) | 0.78 (1.11) | — | — | 20.64 (37.13) | 96% |
| V4 | 0.17 (0.50) | 18.25 (31.76) | 1.13 (1.82) | 0.86 (1.31) | 2.25 (5.55) | 0.07 (0.11) | 23.00 (37.99) | 79% |

## Lượt nóng: trung vị (P95) theo bước

| Biến thể | tokenize | bm25_score | accessible_mask | filter_topk | features | rerank_sort | Tổng | Tỉ lệ BM25 trong tổng (trung bình) |
|---|---|---|---|---|---|---|---|---|
| B0 | 0.03 (0.08) | 12.41 (23.54) | 0.00 (0.00) | 0.67 (1.09) | — | — | 13.14 (24.72) | 95% |
| V2 | 0.18 (0.56) | 19.71 (36.10) | 0.00 (0.00) | 0.76 (1.14) | — | — | 20.66 (37.59) | 96% |
| V4 | 0.17 (0.53) | 18.26 (32.24) | 0.85 (1.24) | 0.87 (1.42) | 0.54 (0.96) | 0.06 (0.10) | 20.89 (35.69) | 88% |

## Ý nghĩa các bước

- `tokenize`: tách từ proof state (tokenizer mặc định hoặc Lean).
- `bm25_score`: giải nén posting của mọi term trong truy vấn và cộng điểm BM25/BM25F.
- `accessible_mask`: tính tập premise truy cập được qua bao đóng import (có cache theo file).
- `filter_topk`: áp mặt nạ và chọn top-K bằng argpartition.
- `features`: tính 13 đặc trưng cấu trúc cho 100 ứng viên.
- `rerank_sort`: chuẩn hóa, nhân trọng số hồi quy logistic và sắp xếp lại.

Kiểm tra đúng đắn (50 truy vấn đầu, so với `searcher.search`): B0: trùng, V2: trùng, V4: trùng.
