# Error analysis (sinh bởi scripts/error_analysis.py)

Run V4: `eval-V4-20261017-194917-88cd`, B0: `eval-B0-20261017-185614-87d3`, tập random_test_all (n = 2641).
Cặp (truy vấn, premise đúng) V4 không đưa vào top-10: 4369 / 5483.

## Phân loại tự động (một cặp có thể thuộc nhiều nhóm)

| Nhóm | Số cặp | Tỉ lệ |
|---|---|---|
| ngoai_top100 | 3613 | 82.7% |
| nhieu_premise_dung | 2430 | 55.6% |
| premise_tong_quat | 1352 | 30.9% |
| khong_trung_tu_vung | 1080 | 24.7% |
| dinh_nghia_instance | 706 | 16.2% |
| truy_van_dai | 442 | 10.1% |
| khac | 336 | 7.7% |

Tỉ lệ nằm ngoài top-100 (giới hạn của stage 1, reranker không cứu được): 82.7%.


## Lát cắt theo chủ đề (thư mục mathlib) (chỉ nhóm ≥ 30 truy vấn)

| Nhóm | n | R@10 B0 | R@10 V4 | Δ |
|---|---|---|---|---|
| Mathlib/Analysis | 360 | 0.067 | 0.224 | +0.157 |
| Mathlib/Algebra | 323 | 0.097 | 0.258 | +0.161 |
| Mathlib/Data | 263 | 0.207 | 0.330 | +0.123 |
| Mathlib/MeasureTheory | 258 | 0.066 | 0.198 | +0.133 |
| Mathlib/Topology | 211 | 0.075 | 0.196 | +0.121 |
| Mathlib/RingTheory | 170 | 0.068 | 0.198 | +0.130 |
| Mathlib/LinearAlgebra | 148 | 0.083 | 0.284 | +0.201 |
| Mathlib/CategoryTheory | 127 | 0.160 | 0.312 | +0.152 |
| Mathlib/Geometry | 111 | 0.090 | 0.229 | +0.138 |
| Mathlib/Order | 108 | 0.065 | 0.206 | +0.140 |
| Mathlib/Computability | 100 | 0.002 | 0.114 | +0.112 |
| Mathlib/NumberTheory | 87 | 0.129 | 0.188 | +0.059 |
| Mathlib/Probability | 79 | 0.092 | 0.219 | +0.126 |
| Mathlib/FieldTheory | 60 | 0.043 | 0.206 | +0.163 |
| Mathlib/SetTheory | 56 | 0.173 | 0.331 | +0.158 |
| Mathlib/Combinatorics | 46 | 0.119 | 0.168 | +0.049 |
| .lake | 44 | 0.140 | 0.275 | +0.135 |
| Mathlib/GroupTheory | 38 | 0.272 | 0.397 | +0.125 |

## Lát cắt theo độ dài truy vấn (số token Lean) (chỉ nhóm ≥ 30 truy vấn)

| Nhóm | n | R@10 B0 | R@10 V4 | Δ |
|---|---|---|---|---|
| 41–80 | 826 | 0.113 | 0.256 | +0.143 |
| 81–160 | 708 | 0.061 | 0.180 | +0.118 |
| 21–40 | 501 | 0.142 | 0.315 | +0.173 |
| >160 | 407 | 0.039 | 0.169 | +0.130 |
| ≤20 | 199 | 0.206 | 0.378 | +0.172 |

## Lát cắt theo mật độ ký hiệu toán trong truy vấn (chỉ nhóm ≥ 30 truy vấn)

| Nhóm | n | R@10 B0 | R@10 V4 | Δ |
|---|---|---|---|---|
| 0,20–0,35 | 1156 | 0.087 | 0.211 | +0.124 |
| ≤0,20 | 1030 | 0.109 | 0.279 | +0.170 |
| 0,35–0,50 | 374 | 0.106 | 0.234 | +0.128 |
| >0,50 | 81 | 0.157 | 0.266 | +0.109 |

## Lát cắt theo số premise đúng (chỉ nhóm ≥ 30 truy vấn)

| Nhóm | n | R@10 B0 | R@10 V4 | Δ |
|---|---|---|---|---|
| 1 | 1377 | 0.123 | 0.281 | +0.158 |
| 2 | 624 | 0.095 | 0.240 | +0.144 |
| 3–4 | 434 | 0.063 | 0.183 | +0.119 |
| ≥5 | 206 | 0.045 | 0.120 | +0.075 |
