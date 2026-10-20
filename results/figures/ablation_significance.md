# Ablation kèm kiểm định (sinh bởi scripts/ablation_significance.py)

random_test_all, n = 2641. Δ = biến thể trừ V4 đầy đủ; KTC 95% từ paired bootstrap theo cụm theorem, p hai phía từ kiểm định hoán vị ghép cặp theo cụm theorem (10.000 phép hoán vị, seed 42, p = (1 + số lần cực trị) / 10.001); p Holm hiệu chỉnh trên 9 phép so sánh của từng metric. Mỗi biến thể huấn luyện lại reranker trên cùng 6.000 truy vấn train nửa B.

| Biến thể | Thay đổi | R@10 | ΔR@10 [KTC 95%] | p (Holm) | MRR | ΔMRR [KTC 95%] | p (Holm) | Kết luận theo R@10 |
|---|---|---|---|---|---|---|---|---|
| abl_full | V4 đầy đủ (tham chiếu) | 0.2425 |  |  | 0.1956 |  |  |  |
| abl_no_bm25 | bỏ bm25_rel, bm25_rr | 0.2062 | -0.0364 [-0.0472, -0.0258] | 0.0001 (0.0009) | 0.1491 | -0.0465 [-0.0587, -0.0350] | 0.0001 (0.0009) | kém hơn có ý nghĩa |
| abl_no_namespace | bỏ ns_in_query, ns_thm | 0.2422 | -0.0003 [-0.0037, +0.0030] | 0.8568 (1.0000) | 0.1954 | -0.0002 [-0.0023, +0.0021] | 0.8770 (0.8770) | không phân biệt được sau hiệu chỉnh |
| abl_no_location | bỏ same_file, dir_overlap | 0.2427 | +0.0002 [-0.0070, +0.0077] | 0.9605 (1.0000) | 0.1859 | -0.0097 [-0.0156, -0.0044] | 0.0002 (0.0010) | không phân biệt được sau hiệu chỉnh |
| abl_no_symbols | bỏ sym_jaccard | 0.2336 | -0.0090 [-0.0169, -0.0013] | 0.0268 (0.1320) | 0.1873 | -0.0083 [-0.0131, -0.0037] | 0.0001 (0.0009) | không phân biệt được sau hiệu chỉnh |
| abl_no_kind | bỏ 4 đặc trưng kind_* | 0.2416 | -0.0010 [-0.0065, +0.0046] | 0.7348 (1.0000) | 0.1871 | -0.0085 [-0.0138, -0.0040] | 0.0002 (0.0010) | không phân biệt được sau hiệu chỉnh |
| abl_no_dependency | bỏ popularity, pagerank | 0.2241 | -0.0184 [-0.0295, -0.0075] | 0.0011 (0.0077) | 0.1802 | -0.0154 [-0.0225, -0.0084] | 0.0001 (0.0009) | kém hơn có ý nghĩa |
| abl_no_filter | tắt bộ lọc truy cập được | 0.1914 | -0.0511 [-0.0608, -0.0422] | 0.0001 (0.0009) | 0.1296 | -0.0660 [-0.0758, -0.0567] | 0.0001 (0.0009) | kém hơn có ý nghĩa |
| abl_k50 | K = 50 ứng viên | 0.2340 | -0.0085 [-0.0161, -0.0011] | 0.0264 (0.1320) | 0.1890 | -0.0066 [-0.0105, -0.0028] | 0.0011 (0.0033) | không phân biệt được sau hiệu chỉnh |
| abl_k200 | K = 200 ứng viên | 0.2523 | +0.0097 [+0.0029, +0.0164] | 0.0032 (0.0192) | 0.2015 | +0.0059 [+0.0019, +0.0099] | 0.0030 (0.0060) | tốt hơn có ý nghĩa |
