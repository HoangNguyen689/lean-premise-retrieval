# Benchmark chung N3/N4 (sinh bởi scripts/eval_shared.py, run `shared-20261020-112058-e591`)

Gói `leandojo-benchmark-4@29dcec07+split-v1.0`, pool `shared-frozen-pool`: 180907 premise, 898 truy vấn mức theorem (random/test), SHA-256 khớp bản ghim. 16 truy vấn không có premise đúng nào trong corpus nên không chấm; còn 882 truy vấn. 158 truy vấn có statement còn chứa chứng minh; lát `signature` bỏ chúng, còn 727 truy vấn.

Quy tắc eligible: loại chính theorem truy vấn trước khi cắt top-k, như nhau cho mọi hệ thống. V4 và V5 lọc thêm premise truy cập được (dùng file và dòng của theorem); B0 và V2 chỉ dùng statement. Benchmark này khác benchmark mức tactic của báo cáo, nên không so số trực tiếp với bảng trong báo cáo.

## Lát `all`

| Hệ thống | n | R@1 | R@5 | R@10 | R@50 | MRR | nDCG@10 | P50 ms | P95 ms |
|---|---|---|---|---|---|---|---|---|---|
| B0 | 882 | 0.069 | 0.159 | 0.215 | 0.323 | 0.256 | 0.172 | 12.5 | 19.2 |
| V2 | 882 | 0.098 | 0.242 | 0.313 | 0.460 | 0.349 | 0.260 | 21.4 | 33.5 |
| V4 | 882 | 0.138 | 0.333 | 0.418 | 0.561 | 0.484 | 0.358 | 26.5 | 40.9 |
| V5 | 882 | 0.135 | 0.337 | 0.432 | 0.636 | 0.488 | 0.368 | 23.8 | 35.8 |

## Lát `signature`

| Hệ thống | n | R@1 | R@5 | R@10 | R@50 | MRR | nDCG@10 | P50 ms | P95 ms |
|---|---|---|---|---|---|---|---|---|---|
| B0 | 727 | 0.052 | 0.135 | 0.190 | 0.297 | 0.221 | 0.145 | 12.8 | 19.3 |
| V2 | 727 | 0.065 | 0.179 | 0.240 | 0.374 | 0.265 | 0.183 | 21.7 | 32.3 |
| V4 | 727 | 0.109 | 0.269 | 0.347 | 0.491 | 0.412 | 0.284 | 26.8 | 38.8 |
| V5 | 727 | 0.102 | 0.276 | 0.369 | 0.578 | 0.414 | 0.297 | 24.1 | 33.9 |

## So sánh R@10

Hoán vị ghép cặp hai phía, 10.000 phép hoán vị; Holm trong từng lát; KTC 95% bằng paired bootstrap.

| Lát | A | B | B − A | KTC 95% | p | p Holm |
|---|---|---|---|---|---|---|
| all | B0 | V2 | +0.098 | [0.079; 0.117] | 0.0001 | 0.0003 |
| all | V2 | V4 | +0.105 | [0.086; 0.124] | 0.0001 | 0.0003 |
| all | V4 | V5 | +0.014 | [-0.002; 0.030] | 0.0812 | 0.0812 |
| signature | B0 | V2 | +0.050 | [0.032; 0.068] | 0.0001 | 0.0003 |
| signature | V2 | V4 | +0.108 | [0.087; 0.128] | 0.0001 | 0.0003 |
| signature | V4 | V5 | +0.022 | [0.004; 0.039] | 0.0172 | 0.0172 |

Chưa có run file của Nhóm 4. Khi nhận được: `python scripts/eval_shared.py --external N4-dense=<run_dense>.csv`.
