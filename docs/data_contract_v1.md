# DATA CONTRACT v1.0 — Nhóm 3 × Nhóm 4
# Lean Premise Retrieval: Sparse/Hybrid (N3) × Dense/ANN (N4)

> Trạng thái: **ACTIVE — N3 công bố đơn phương (2026-10-15) sau khi N4 không phản hồi.**
> Theo mục §7: N4 trễ không chặn N3. N4 tham gia sau chỉ cần làm theo spec này — mọi
> artifact đã sẵn: corpus + queries + qrels + protocol + run file mẫu trong `results/real/`.
> Benchmark chốt: **LeanDojo Benchmark 4, Zenodo DOI 10.5281/zenodo.12740403, license CC-BY-2.0,
> mathlib4 commit `29dcec074de168ac2bf835a77ef68bbe069194c5`, LeanDojo v2.0.0.**
> Bump theo semver: đổi BREAKING → major; thêm trường tùy chọn → minor; sửa mô tả → patch.
> Quy tắc hòa giải mâu thuẫn: (1) nhìn thấy được spec trước hôm chấm split > tiện triển khai; (2) muộn nhất tuần 9 vẫn phải so sánh được; (3) lệch schema ở khâu ETL, không sửa contract sau khi N4 đã encode vector.
> **Nguồn dữ liệu chọn (đã tải và build xong):** [LeanDojo Benchmark 4 — Zenodo DOI 10.5281/zenodo.12740403](https://zenodo.org/records/12740403) — 68 MB tar.gz, license CC-BY-2.0, không cần đăng nhập. Chứa 118.517 theorem (random split: 118.517 train / 2.000 val / 2.000 test) + corpus.jsonl với 180.907 declarations. HuggingFace bị gate nên không dùng.

---

## 1. Phạm vi và nguồn

| Mục | Giá trị |
|---|---|
| Nguồn chính | LeanDojo Benchmark 4 — snapshot **Lean toolchain v4.9.0-rc1, mathlib4 commit `294ec7f`** |
| Corpus (premise pool) | Toàn bộ theorem trong benchmark (~102.576 declarations, cả train/val/test như một kho) |
| Query set | 1.000 statement **chỉ từ split test** của benchmark, loại bỏ query nằm trong corpus như một theorem theo đúng tên `full_name` |
| Cấm | Không chỉnh sửa nội dung field; không thêm split mới ngoài 3 mức quy mô §6; mỗi artifact phải có `data_version` |
| Ranh giới trách nhiệm | **N3 sở hữu contract này + corpus + split; N4 sở hữu embedding + index ANN; cả hai cùng sở hữu query set (đồng ký)** |

> Rationale nguồn: chọn LeanDojo Benchmark 4 vì (a) download 1 lệnh, có card trên HF, (b) premise của mỗi theorem có sẵn từ trace → sinh qrels không phải gán nhãn thủ công từ đầu, (c) 4 file-train hỗ trợ mock pipeline khi chưa tải xong.

## 2. Đơn vị dữ liệu

Một **premise** = một declaration Lean 4 (theorem/lemma/def) trong mathlib4 tại commit ghim. Một **query** = statement cần tìm premise. Không có khái niệm "bài toán tự nhiên" trong pipeline retrieval — chỉ có statement Lean.

## 3. Lược đồ (schema) — 6 field bắt buộc

Mọi artifact CSV/Parquet **phải** có đủ 6 field dưới đây (thứ tự cột tùy, tên cột cố định, phân biệt chữ hoa/thường):

| # | Field | Kiểu | Bắt buộc | Mô tả | Ràng buộc |
|---|---|---|---|---|---|
| 1 | `id` | string | ✅ | Định danh duy nhất | Corpus: nguyên văn `full_name` của declaration (vd. `Nat.add_comm`). Query: `Q0001..Q1000`. Rỗng → ETL **fail** |
| 2 | `statement` | string | ✅ | Phát biểu dạng Lean 4 (nguyên văn, không chuẩn hóa) | Không rỗng sau khi strip; giữ nguyên Unicode (ℕ, ∀, →) |
| 3 | `statement_natural` | string | ✅ (có thể rỗng) | Câu tiếng Anh tự nhiên mô tả cùng nội dung; rỗng nếu không có | Không tự dịch; chỉ lấy từ nguồn |
| 4 | `namespace` | string | ✅ (có thể rỗng) | Namespace đầy đủ (vd. `Analysis.Calculus.Derivative`); rỗng = declaration cấp root trong Lean (vd. `AList`) — v1.1 | |
| 5 | `file_path` | string | ✅ | Đường dẫn file gốc trong mathlib4 (vd. `Mathlib/Analysis/Calculus/Deriv/Add.lean`) | Dùng để tính 2 đặc trưng phụ thuộc §5.4 |
| 6 | `line_start` | int | ✅ | Dòng bắt đầu của declaration trong file | ≥ 1 |

Field tùy chọn (nếu có, không được xóa): `premises` (list id premise được dùng trong chứng minh — chỉ có ở query set), `commit` (hash Lean/mathlib).

> **Ví dụ dòng corpus:** `Nat.add_zero, theorem Nat.add_zero : ∀ (n : ℕ), n + 0 = n, Adding zero to the natural number n gives n, Nat, Mathlib/Data/Nat/Basic.lean, 142`

## 4. Định dạng và version

- **Định dạng:** Parquet (chính, kèm checksum), CSV/JSONL (chỉ cho sample < 1 MB).
- **Quy tắc v nhỏ:** thêm field tùy chọn = bump minor (v1.1); đổi kiểu/xóa field/sửa ràng buộc = bump major (v2.0) — N3 phải thông báo trước 1 tuần trên issue board chung.
- **`data_version`** của mọi run thí nghiệm ghi theo mẫu: `leandojo-benchmark-4@294ec7f+split-v1.0`.

## 5. Định nghĩa split (cố định, không được tái chia)

### 5.1. Ba mức quy mô (bắt buộc ≥ 3 mức — yêu cầu môn học)

| Mức | Số corpus | Số query | Nguồn rút | Checksum của |
|---|---|---|---|---|
| **S1** | 10.000 | 200 | Corpus: 10K đầu sau khi sort theo `id`; Query: 200 test đầu | `corpus_s1.parquet`, `queries_s1.parquet` |
| **S2** | 50.000 | 500 | Corpus: 50K đầu sau khi sort; Query: 500 test đầu | `corpus_s2.parquet`, `queries_s2.parquet` |
| **S3** | toàn bộ ~102K | 1.000 | Toàn bộ corpus; toàn bộ query set | `corpus_full.parquet`, `queries_full.parquet` |

Query S1 ⊂ S2 ⊂ S3 (số lượng, đúng theo thứ tự id tăng dần) — để chạy scale tăng trưởng thật sự.

### 5.2. Qrels (ground truth)

| Nhãn | Ý nghĩa | Nguồn |
|---|---|---|
| **2** | Premise được **dùng trực tiếp** trong chứng minh chuẩn của query (có trong trace LeanDojo) | Tự động từ field `premises` của benchmark — không gán tay |
| **1** | Premise **liên quan gián tiếp**: cùng namespace hoặc cùng file_path với premise nhãn 2 | Bán tự động, kiểm tra tay 10% ngẫu nhiên |
| **0** | Không liên quan | Mặc định |

Cách sinh: pool = top-50 của **cả** hệ N3 và hệ N4 gộp lại, cộng với premise nhãn 2 gốc (pooling TREC-style). Sau khi gộp pool, mọi premise ngoài pool coi như 0.

### 5.3. Query split cho tinh chỉnh

| Tập | Số query | Dùng |
|---|---|---|
| Dev | 200 đầu của query set S2 | Tinh chỉnh field weights, tham số ANN (nprobe/efSearch), reranker |
| Test | 800 còn lại | **Chạy đúng 1 lần** khi báo cáo cuối. Không tinh chỉnh trên tập này |

Cả N3 và N4 phải dùng cùng phân chia Dev/Test. Mỗi bên lưu tệp manifest riêng ghi `split-v1.0-<date>` + checksum 4 tệp (corpus S1/S2/S3 + queries).

### 5.4. Quy tắc eligible premise (thống nhất với N4, 2026-10-18)

1. **Không dùng theorem truy vấn làm premise**: theorem truy vấn KHÔNG được phép xuất hiện trong kết quả truy hồi của chính nó. Vì query nằm trong corpus, hệ phải lọc self trước khi cắt top_k (đã cài trong `src/retrieval/systems.py`).
2. **Pool frozen**: premise pool = toàn bộ corpus.jsonl trừ chính theorem truy vấn, cố định trước mọi run — `pool_id: shared-frozen-pool`.
3. **Premise giữa các theorem test với nhau hợp lệ**: một theorem test KHÁC được dùng làm premise của query vẫn tính là gold (56 nhãn-2 thuộc trường hợp này — kiểm chứng từ trace, giữ nguyên).

### 5.5. Gói chia sẻ schema N4 (kết quả thống nhất, 2026-10-18)

N3 xuất `results/n4_shared/` đúng schema N4 yêu cầu:
- `corpus.jsonl` — `{id, name, statement, namespace, source_commit}` (180.907 dòng; `name` = full_name — LeanDojo không tách name riêng khỏi namespace, ghi chú tại đây)
- `queries.jsonl` — `{id, statement, relevant_ids, split: "test", pool_id: "shared-frozen-pool"}` (898 dòng; `relevant_ids` = nhãn 2, mean 4.7/query)
- `checksums.txt` — SHA-256 của 2 file trên để N4 xác nhận cùng snapshot

## 6. Protocol đánh giá chung (trích từ `evaluation_protocol.md` v0.1 của N3, đã được N3 cam kết)

- **Primary metrics:** `Recall@10` (chất lượng) + `P95 latency` (hiệu năng). Lý do chọn: phục vụ prover cần recall cao trong ngân sách độ trễ thấp.
- **Secondary metrics:** `Recall@1/5/50`, `MRR`, `nDCG@10`, `QPS`, `index_build_time`, `index_size`, `peak_RAM`.
- **Quy ước Recall:** tính trên nhãn **2** (chính thức); nhãn ≥ 1 báo cáo riêng khi cần so sánh. Macro-average trên toàn query set.
- **Load test:** 1 / 10 / 50 truy vấn đồng thời (cả hai nhóm dùng cùng mức để so sánh P95/QPS).
- **Lặp:** runtime biến động → chạy **≥ 3 lần**, báo **median + min/max**. Latency đo trên ≥ 100 truy vấn đơn lẻ.

## 7. Giao dịch giữa N3 và N4

| Từ | Giao cho | Artifact | Định dạng | Deadline |
|---|---|---|---|---|
| N3 → N4 | Corpus + query set + qrels | `corpus_{s1,s2,full}.parquet`, `queries_{s1,s2,full}.parquet`, `qrels_v1.parquet`, `split_manifest.json` | Parquet + JSON | **Tuần 3** |
| N3 → N4 | Protocol đánh giá (mục §6) | File này | md | Tuần 1 |
| N4 → N3 | Kết quả dense/ANN (run file) | `run_dense_{s1,s2,full}.csv` (cột `query_id, premise_id`) | CSV | **Tuần 9** |
| N4 → N3 | Cấu hình ANN đã dùng (để ghi vào so sánh) | `n4_config.json` | JSON | Tuần 9 |
| N3 → N4 | Kết quả sparse/hybrid (để N4 đối chiếu) | `run_sparse_*.csv`, `run_hybrid_*.csv` | CSV | Tuần 9 |

> Quy tắc nội bộ: **nếu N4 trễ** hơn tuần 3, N3 vẫn phải chạy đủ pipeline với corpus mock tự sinh (xem `scripts/make_mock_end_to_end.py`) và không chặn tiến độ của mình. N4 trễ ở tuần 9 → N3 công bố kết quả N3 + ghi chú "dense results pending" trong comparison table, không bị trừ điểm của N3.

## 8. Changelog

- **v1.2 (2026-10-18)** — Thống nhất 6 mục với N4: thêm §5.4 quy tắc eligible premise (không dùng theorem truy vấn làm premise + pool frozen), §5.5 gói chia sẻ schema N4 (corpus.jsonl + queries.jsonl + checksums); sửa schema §3 thêm `source_commit`; eligible rule đã cài trong `src/retrieval/systems.py` (lọc self trước top_k).
- **v1.1 (2026-10-15)** — namespace cho phép rỗng (declaration cấp root của Lean, 128/180.907 trường hợp thực tế); cập nhật nguồn sang Zenodo + số liệu thật.
- **v1.0 (tuần 1)** — bản đầu: 6 field bắt buộc, 3 mức scale, qrels 3 nhãn, protocol đánh giá, lịch giao N3↔N4.

## 9. Lệnh tải LeanDojo Benchmark 4 (cho TV1 — đã chạy xong)

```bash
# Đã tải và build (results/real/ có đầy đủ):
python scripts/build_real_corpus.py   # đọc data_raw/leandojo_benchmark_4/ → corpus/queries/qrels 3 scale

# Tải lại nếu cần (Zenodo, không cần đăng nhập):
python -c "
import urllib.request
url = 'https://zenodo.org/api/records/12740403/files/leandojo_benchmark_4.tar.gz/content'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
open('data_raw/leandojo_benchmark_4.tar.gz', 'wb').write(urllib.request.urlopen(req, timeout=590).read())
"
```

Số liệu đã xác nhận: 180.907 declarations; 898 test queries có premise GT (TB 5.4/query);
12.966 qrels (4.165 nhãn 2 + 8.801 nhãn 1). mathlib4 commit `29dcec074de168ac2bf835a77ef68bbe069194c5`.

## 10. Lịch sử nguồn đã cân nhắc

| Nguồn | Chọn? | Lý do |
|---|---|---|
| **LeanDojo Benchmark 4 (HuggingFace)** | ✅ Có | Một lệnh tải, ~102K theorems, premise có sẵn, card đầy đủ |
| LeanDojo Benchmark 4 (JSON 4.2 GB từ leandojo.org) | ⚠️ Fallback | Cần fetch về local + extract; dùng khi HF không tải được |
| mathlib4 repo (clone full) | ❌ | Cần Lean toolchain để extract; quá nặng cho tuần 2 |
| LeanStacks / Mathlib API search | ❌ | Chỉ là giao diện tìm kiếm, không có ground truth premise |

---

*Người soạn (N3): ______________ (TV6 – Evaluation) | Người đồng ký (N4): ______________ | Ngày: ____/____/2026*
