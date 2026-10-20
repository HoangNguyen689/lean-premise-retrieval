# DATA DICTIONARY — Nhóm 3 (LeanDojo Benchmark 4, data_version `leandojo-benchmark-4@29dcec07+split-v1.0`)

Áp dụng cho `results/real/{corpus,queries,qrels}_{scale}.parquet|.csv` (S1=10K/200, S2=50K/500, S3=full 180.907/898).

## corpus / queries — 6 field contract v1.1

| Field | Kiểu | Ý nghĩa | Rỗng hợp lệ? | Ví dụ |
|---|---|---|---|---|
| `id` | string | Định danh duy nhất: full_name của declaration (corpus); `Q<full_name>` (query) | Không | `Nat.add_comm` / `QCategoryTheory.Equivalence.invFunIdAssoc_hom_app` |
| `statement` | string | Code Lean 4 nguyên văn của declaration (đối với query: code nếu tìm thấy trong corpus, else full_name) | Không | `theorem Nat.add_comm : ∀ (n m : ℕ), n + m = m + n := ...` |
| `statement_natural` | string | Phát biểu tiếng Anh tự nhiên | Có (benchmark không cung cấp) | *(rỗng)* |
| `namespace` | string | Namespace Lean: phần full_name trước dấu chấm cuối | Có (= declaration cấp root, vd. `AList`) | `Nat` |
| `file_path` | string | Đường dẫn file trong mathlib4 (đã chuẩn hóa về `Mathlib/...`) | Không | `Mathlib/Data/Nat/Basic.lean` |
| `line_start` | int | Dòng bắt đầu declaration trong file | Không (≥1) | `142` |

## qrels — ground truth truy hồi

| Field | Kiểu | Ý nghĩa |
|---|---|---|
| `query_id` | string | Khớp `queries.id` |
| `premise_id` | string | Khớp `corpus.id` |
| `relevance` | int | **2** = premise dùng trực tiếp trong chứng minh chuẩn (trích tự động từ `annotated_tactic` của LeanDojo trace); **1** = liên quan gián tiếp (cùng `file_path` với một premise nhãn 2, tối đa 10/query — chỉ dùng phân tích, không dùng primary metric); **0** = không liên quan (mặc định, không ghi file) |

## Splits

| Scale | Corpus | Queries | Ghi chú |
|---|---|---|---|
| S1 | 10.000 | 200 | sort theo `id`, 10K/200 đầu |
| S2 | 50.000 | 500 | S1 ⊂ S2 |
| S3 (full) | 180.907 | 898 | chỉ query có ≥1 premise GT |

Checksum từng file: `split_manifest.json`. Nguồn: Zenodo DOI 10.5281/zenodo.12740403, license CC-BY-2.0.