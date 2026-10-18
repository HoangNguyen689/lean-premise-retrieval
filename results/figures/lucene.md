# BM25 của Lucene (Anserini 2.3.0) so với BM25 tự cài đặt (sinh bởi scripts/lucene_baseline.py)

Tập random_test_all, 2641 truy vấn, top 100, trường statement. Thời gian tìm kiếm một luồng, trung bình mỗi truy vấn ở trạng thái ổn định (Lucene: từ mốc 100 truy vấn đến mốc cuối trong log của Anserini; trong ngoặc là wall time chia số truy vấn, gồm khởi động JVM và mở index).

| Hệ thống | R@1 | R@10 | R@50 | MRR | ms/truy vấn | Chỉ mục (MB) | Trùng top-10 với B0 | Top-10 trùng nguyên tập | Top-1 trùng |
|---|---|---|---|---|---|---|---|---|---|
| lucene-default (k1 = 0.9, b = 0.4) | 0.017 | 0.076 | 0.139 | 0.051 | 2.34 (6.65) | 6.8 | 0.544 | 0.025 | 0.530 |
| lucene-english-b0params (k1 = 1.2, b = 0.75) | 0.017 | 0.089 | 0.155 | 0.058 | 2.26 (3.57) | 6.8 | 0.594 | 0.078 | 0.610 |
| lucene-b0tokens (k1 = 1.2, b = 0.75) | 0.018 | 0.100 | 0.176 | 0.066 | 2.39 (3.68) | 6.7 | 0.989 | 0.896 | 0.983 |
| B0 của nhóm (k1 = 1.2, b = 0.75) | 0.018 | 0.100 | 0.176 | 0.065 | 13.22 (13.27) | 4.1 (postings) | 1 | 1 | 1 |
