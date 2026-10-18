# Codec posting khi tắt cache (sinh bởi scripts/bench_codec.py)

| Codec | Postings (MB) | Giải mã toàn bộ (s) | Triệu posting/s | P50 truy vấn (ms) | P95 truy vấn (ms) |
|---|---|---|---|---|---|
| raw32 | 12.8 | 0.15 | 11.19 | 12.7 | 23.6 |
| vb | 4.1 | 2.92 | 0.58 | 16.9 | 30.1 |
| gamma | 2.6 | 1.74 | 0.96 | 137.7 | 249.1 |

Median của 3 lần. Cache posting đã giải mã bị tắt (cache_terms = 0) để thấy chi phí giải mã thật.
