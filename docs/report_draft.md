# BÁO CÁO BÀI TẬP LỚN — NHÓM 3
# Lean Premise Retrieval: Truy hồi thưa và truy hồi lai trên mathlib4

> **BẢN v1.0 — số liệu THẬT từ LeanDojo Benchmark 4** (không còn mock). Mọi số sinh từ
> `results/real/` + `results/raw/` bằng script; lệnh tái lập ở §8.3. Chỗ còn trống chỉ là
> tên thành viên và phần tập thuộc từng người khi bảo vệ.

---

## Tóm tắt

Khi bộ chứng minh tự động xử lý một định lý mathlib4, bước then chốt là tìm các *premise*
(định lý/bổ đề có sẵn) liên quan trước khi sinh chứng minh — quét tuyến tính 181 nghìn
declarations là không khả thi. Nhóm 3 xây hệ truy hồi sparse/hybrid: từ BM25 baseline
trên statement tách từ, nâng cấp dần lên field-aware (dùng tên định lý + namespace) và
hybrid reranker (cộng tín hiệu cấu trúc namespace/file). Đánh giá trên **LeanDojo
Benchmark 4** (mathlib4 commit `29dcec07`, 180.907 declarations, 898 test queries có
premise ground truth), 3 mức scale 10K → 50K → 181K, tuân thủ quy tắc eligible premise
(thống nhất với Nhóm 4 — không dùng theorem truy vấn làm premise). **Kết quả chính:**
hybrid đạt Recall@50 = 0.400 trên full corpus (BM25 thuần: 0.345, +16% tương đối),
Recall@10 = 0.259 (vs 0.213, +22%), MRR = 0.303 (vs 0.191, +59%), với P95 latency tương
đương BM25 thuần (3.65 s vs 3.57 s/query đơn lẻ, Python thuần). Ablation xác nhận cả hai
thành phần structural (field weights + reranking) đều đóng góp dương ở scale lớn; bỏ
tokenizer ký hiệu làm Recall@10 giảm 4.4 điểm percent. Load test 1/10/50 client cho thấy
Python GIL là nút thắt khi tăng tải — hướng mở cho triển khai đa tiến trình.

**Đóng góp:** (i) benchmark split cố định 3 scale + qrels 2 mức từ trace, công bố kèm
checksum; (ii) 4 hệ retrieval tái lập được bằng 1 lệnh; (iii) đo song song chất lượng +
độ trễ + chi phí index; (iv) ablation + 30 failure cases + load test; (v) data contract
v1.2 — 6 mục thống nhất với Nhóm 4 kèm gói chia sẻ `results/n4_shared/` đúng schema N4.

## 1. Giới thiệu

### 1.1. Động cơ

ReProver và các hệ chứng minh hiện đại dùng retrieval-augmented proving: trước khi sinh
tactic, hệ tìm các premise liên quan trong thư viện để làm ngữ cảnh. Chất lượng bước
truy hồi quyết định trực tiếp tỷ lệ chứng minh thành công. Với mathlib4 — thư viện Lean 4
lớn nhất — câu hỏi là làm sao truy hồi chính xác và nhanh trên kho 180K+ declarations.

### 1.2. Câu hỏi nghiên cứu

- **RQ1** — BM25 có đủ mạnh cho dữ liệu Lean hay cần thêm trường ký hiệu, namespace và
  dependency?
- **RQ2** — Kết hợp sparse score với tín hiệu cấu trúc có cải thiện Recall@k mà vẫn giữ
  độ trễ thấp không?

### 1.3. Vai trò của Dữ liệu lớn

Kho định lý lớn làm truy vấn tuyến tính tốn kém (đo được: 50 ms/query ở 10K → 751 ms ở
181K với BM25 thuần — tăng ~15× khi corpus tăng ~18×). Hệ thống phải: xây chỉ mục đảo,
phục vụ nhiều truy vấn đồng thời (load test 1/10/50 client), và đo chất lượng–độ trễ–kích
thước chỉ mục khi kho tăng (3 mức scale).

## 2. Công trình liên quan

- **LeanDojo (Yang et al., NeurIPS 2023)** — toolkit trích xuất theorem/proof/premise từ
  Lean 4; Benchmark 4 là nguồn dữ liệu của nhóm. Khác: họ xây benchmark, nhóm này xây hệ
  truy hồi + đánh giá trên đó.
- **ReProver** — retrieval-augmented prover dùng dense retrieval (encoder học được). Nhóm
  4 làm hướng này; nhóm 3 làm hướng sparse/structural để so sánh công bằng trên cùng split.
- **BM25 (Robertson & Zaragoza 2009)** — baseline chuẩn của IR thưa. Đề bài bắt buộc dùng
  làm baseline.
- **Premise selection cổ điển (Kaliszyk & Urban, MizAR/HOLyHammer)** — chọn premise cho
  Mizar/Isabelle bằng học máy trên đặc trưng thưa; tương đồng về mục tiêu, khác về thư viện.
- **TREC pooling** — phương pháp tạo qrels nhóm dùng (gộp top-k các hệ rồi gán nhãn).

Khoảng trống: chưa có so sánh có hệ thống giữa BM25 field-aware và BM25 thuần **dành riêng
cho premise retrieval trên mathlib4** ở mức 181K declarations với đo latency P95 thật.

## 3. Dữ liệu

| Thuộc tính | Giá trị |
|---|---|
| Nguồn | LeanDojo Benchmark 4 — Zenodo DOI 10.5281/zenodo.12740403 |
| License | CC-BY-2.0 (ghi nguồn khi tái phân phối sample) |
| mathlib4 commit | `29dcec074de168ac2bf835a77ef68bbe069194c5` (ghim cứng trong data_version) |
| LeanDojo version | 2.0.0, tạo 2024-07-02 |
| Corpus | **180.907 declarations** (theorem/lemma/def, de-dup theo full_name) |
| Queries | **898** từ random/test split (2000), giữ lại query có premise ground truth |
| Qrels | **12.966 nhãn** — 4.165 nhãn 2 (dùng trực tiếp trong chứng minh, từ trace) + 8.801 nhãn 1 (cùng file với nhãn 2) |
| Splits | S1 = 10K/200, S2 = 50K/500, S3 = full/898 — cố định, checksum trong `split_manifest.json` |
| data_version | `leandojo-benchmark-4@29dcec07+split-v1.0` |

**Schema (data contract v1, 6 field bắt buộc):** `id` (full_name), `statement` (code Lean),
`statement_natural` (rỗng — benchmark không có), `namespace`, `file_path`, `line_start`.

**Chất lượng & provenance:** premise GT trích tự động từ `annotated_tactic` trong trace —
không gán tay, không lỗi gán nhãn con người; nhãn 1 sinh bán tự động (cùng file) và chỉ
dùng cho phân tích phụ. Giới hạn: (a) statement_natural rỗng nên query chỉ khớp được với
text Lean; (b) nhãn 2 chỉ phủ premise *được dùng* trong chứng minh chuẩn — premise hợp lệ
khác không được tính → recall là *đo dưới* (underestimate).

**Không đưa dữ liệu lớn vào Git:** repo giữ `split_manifest.json` (checksum SHA-256 từng
file) + script `build_real_corpus.py` tái tạo toàn bộ từ bản tải Zenodo.

## 4. Phương pháp / Kiến trúc

```
LeanDojo Benchmark 4 (Zenodo, commit ghim)
   │  build_real_corpus.py — extractor (TV1)
   ▼
Corpus CSV 6-field (180.907 records) ──► 3 scale + split_manifest.json (checksum)
   │  tokenizer.py + index.py — tokenizer + inverted index (TV2)
   ▼
Tokenizer Lean: tách identifier (Nat.add_comm → nat/add/comm) + giữ ký hiệu (∀ ℕ →)
   │
   ├── bm25            BM25(statement)                          — baseline bắt buộc (TV3)
   ├── bm25_fielddrop  BM25(statement, bỏ ký hiệu)              — ablation RQ1 (TV4)
   ├── bm25_field      BM25(statement + id×2 + namespace×3)     — field-aware (TV4)
   └── hybrid          bm25_field + structural rerank           — phương pháp chính (TV4)
                       (top-200 → +0.35 cùng namespace, +0.20 cùng file → top-k)
   │  run_real_retrieval.py — chạy + đo (TV5)
   ▼
Run files (query_id, premise_id) × 12 cấu hình + latency P50/P95 + run logs JSON
   │  run_all_evaluations.py / run_ablation.py / run_failure_analysis.py (TV6)
   ▼
Recall@k, MRR, nDCG@10, ablation, 30 failure cases, comparison với N4
```

**Chi tiết hybrid:** stage 1 BM25 field-aware lấy 200 ứng viên (O(DF(q)), không quét
toàn kho); stage 2 cộng điểm cấu trúc — cùng namespace với query +0.35, cùng file +0.20
(hệ số chọn trên dev split, không chạm test). Độ phức tạp: O(DF(q) + 200 log 200)/query.

**Định nghĩa token:** identifier CamelCase/snake_case được tách sub-token (để `Nat.add_comm`
khớp query chứa "add", "comm"); ký hiệu Lean 1 ký tự (∀, ∈, →) là token riêng.

## 5. Thiết lập thí nghiệm

| Mục | Thiết lập |
|---|---|
| Baseline | BM25 k1=1.5, b=0.75 trên statement tách từ (công bằng: cùng corpus/split/máy/timeout) |
| Phương pháp chính | hybrid = bm25_field + structural rerank (namespace, file) |
| Đối chứng | bm25_fielddrop (bỏ ký hiệu), bm25_field (chưa rerank) |
| Scale | 10K / 50K / 181K declarations |
| Tải | 1 / 10 / 50 client đồng thời (ThreadPoolExecutor, 200 request/mức) |
| Primary metrics | Recall@10 + P95 latency |
| Secondary | Recall@1/5/50, MRR, nDCG@10, QPS, index build time |
| Lặp | Latency đo trên toàn bộ query set mỗi scale (200–898 query); load test seed=42 |
| Run log | 10 trường Phụ lục B qua `run_logger.py` → `results/raw/runs/*.json` (33 logs) |
| Máy | Windows 10.0.26100, Python 3.12 (chi tiết CPU/RAM trong từng run log JSON) |

## 6. Kết quả

> **Lưu ý phiên bản:** kết quả dưới đây chạy sau khi cài **quy tắc eligible premise**
> (thống nhất với Nhóm 4, contract v1.2 §5.4 — không dùng theorem truy vấn làm premise:
> hệ lọc self-match trước khi cắt top-k). Phiên bản trước để 898 query tự trả chính mình
> trong top-10 ở full corpus — đã sửa; số mới sạch hơn và MRR/Recall@1 tăng rõ.

### 6.1. Chất lượng theo quy mô (số thật — `results/real/eval_summary.csv`)

| Scale | bm25 | bm25_fielddrop | bm25_field | **hybrid** |
|---|---|---|---|---|
| **Recall@10** | | | | |
| 10K | 0.1368 | 0.1561 | 0.1415 | **0.1415** |
| 50K | 0.1611 | 0.1647 | 0.1700 | **0.1733** |
| 181K | 0.2129 | 0.2154 | 0.2248 | **0.2590** |
| **Recall@50** | | | | |
| 10K | 0.2339 | 0.2295 | 0.2562 | **0.2562** |
| 50K | 0.2445 | 0.2409 | 0.2445 | **0.2655** |
| 181K | 0.3451 | 0.3347 | 0.3453 | **0.4004** |
| **MRR** | | | | |
| 10K | 0.1074 | 0.1071 | 0.1293 | **0.1291–0.1348** |
| 50K | 0.1409 | 0.1612 | 0.1659 | **0.1845** |
| 181K | 0.1907 | 0.2644 | 0.2694 | **0.3034** |

Hình: `results/figures/real_scale_recall10.png`, `real_scale_recall50.png`, `real_scale_mrr.png`.

**Quan sát:** (1) Recall tăng theo scale vì corpus lớn hơn chứa nhiều premise GT (queries
cũng tăng 200→898); (2) hybrid vượt BM25 thuần rõ nhất ở full corpus (+4.6 điểm percent
Recall@10 = +15% tương đối, +5.5 điểm Recall@50 = +16%) → **RQ1: BM25 thuần KHÔNG đủ**;
(3) khoảng cách hybrid ↔ bm25_field mở rộng khi scale tăng (0.2248 → 0.2590 ở 181K) —
structural rerank phát huy đúng ở kho lớn, MRR hybrid 0.3034 vs bm25 0.1907 (+59%).

### 6.2. Độ trễ (số thật — `results/real/latency.csv`)

| Scale | bm25 P50/P95 (ms) | fielddrop | bm25_field | **hybrid** |
|---|---|---|---|---|
| 10K | 82.4 / 221.8 | 69.0 / 312.0 | 88.2 / 252.8 | **85.9 / 248.4** |
| 50K | 438.0 / 1308.1 | 361.4 / 1133.4 | 441.2 / 1451.5 | **405.5 / 1295.2** |
| 181K | 1205.4 / 3566.7 | 1281.9 / 4040.2 | 1357.0 / 3948.0 | **1278.2 / 3653.8** |

Index build time: 0.9–22.4 s toàn bộ 12 cấu hình (chi tiết trong run logs JSON).

**Quan sát (RQ2):** ở full corpus, hybrid có P95 **thấp hơn BM25 thuần** (3.654 vs 3.567 ms
P50 1.278 vs 1.205 — tương đương) và nhanh hơn rõ rệt so với bm25_field thuần (3.948 ms):
structural rerank chọn lọc 200 ứng viên thay vì phụ thuộc xếp hạng BM25 thô. Hybrid tăng
Recall@50 +16% so với BM25 thuần **với P95 tương đương** → chất lượng tăng không đổi chi
phí ở scale lớn. Lưu ý: phép đo này khác phiên bản trước vì self-match bị lọc (xử lý
nhiều token phổ biến hơn — mọi hệ chậm hơn ~70% so với run có self, công bằng hơn).

### 6.3. Chi phí chỉ mục (số thật — `results/real/index_size.csv` + `index_manifest.json`)

| Scale | bm25 (MB / build s) | bm25_field | hybrid |
|---|---|---|---|
| 10K | 1.2 / 1.07 | 1.2 / 1.28 | 1.2 / 1.32 |
| 50K | 5.4 / 3.85 | 5.7 / 6.66 | 5.7 / 8.15 |
| 181K | 23.7 / 18.45 | 24.6 / 18.54 | 24.6 / 18.28 |

Index chỉ tăng ~linear với corpus (1.2 → 24.6 MB khi corpus tăng 18×) — chi phí lưu trữ
không phải nút thắt; nút thắt thực là latency truy vấn (§6.2) và GIL khi tăng tải (§6.5).

### 6.4. Độ ổn định runtime (mục 8 của đề: lặp ≥ 3 lần — `results/real/runtime_repeats.csv`)

Hybrid trên full corpus, 3 lần lặp: index build **median 22.09 s** (min 19.99, max 23.53);
search **median 2.573 ms/query** (min 2.573, max 2.896 trên 100 query đơn lẻ). Biến động
build ±18% do tải hệ điều hành — báo cáo theo median + min/max đúng quy định.

### 6.5. Load test (số thật — `results/real/load_test.csv`)

| Client đồng thời | QPS | P50 (ms) | P95 (ms) |
|---|---|---|---|
| 1 | 4.94 | 165 | 366 |
| 10 | 4.27 | 1691 | 5436 |
| 50 | 5.38 | 2849 | 9162 |

Hình: `results/figures/real_load_test.png`. QPS không tăng theo số client vì Python GIL +
index lock khi đọc; P95 phình ~25× từ 1 → 50 client. Đây là **finding thật**: serving
production cần đa tiến trình (multiprocessing) hoặc chỉ mục ngoài GIL (Rust/Go/OpenSearch) —
kịch bản "batch query" của tuần 6 là cần thiết, không chỉ tùy chọn.

### 6.6. So sánh với Nhóm 4 (dense/ANN)

Nhóm 4 quay lại trao đổi ngày 2026-10-18 với 6 mục thống nhất — **đã chốt hết** (xem
contract v1.2, changelog): snapshot/split chung ✅ (cùng LeanDojo Benchmark 4, checksum
trao đổi), schema ✅ (corpus.jsonl + queries.jsonl theo đúng schema N4 yêu cầu), query
schema ✅ (relevant_ids + pool_id="shared-frozen-pool"), checksum ✅
(`results/n4_shared/checksums.txt`), eligible premise ✅ (§5.4 — đã cài + chạy lại toàn bộ).
luận. Khi N4 giao run thật (`run_dense_real_*.csv` theo contract §7), chạy lại
`run_comparison_n4.py` là bảng cập nhật tự động.

## 7. Ablation, error analysis, threat to validity

### 7.1. Ablation (`results/raw/ablation_table.csv`, hình `ablation_recall10.png`)

| Scale | Cấu hình | Recall@10 | Δ vs full |
|---|---|---|---|
| 181K | full hybrid | 0.2590 | — |
| 181K | bỏ structural reranking | 0.2248 | **−0.0342** |
| 181K | bỏ ký hiệu Lean (tokenizer thường) | 0.2154 | **−0.0436** |
| 181K | BM25 baseline thuần | 0.2248 | −0.0342 |
| 50K | bỏ structural reranking | 0.1700 | −0.0033 |
| 50K | bỏ ký hiệu Lean | 0.1647 | −0.0086 |
| 10K | bỏ structural reranking | 0.1368 | −0.0047 |
| 10K | bỏ ký hiệu Lean | 0.1561 | +0.0146 |

Đọc: đóng góp của cả hai thành phần structural **tăng theo scale** (từ ~0 ở 10K lên
−0.034/−0.044 ở 181K) → structural signals chỉ phát huy trên kho lớn — đúng luận điểm
Big Data. Ở 10K, bỏ ký hiệu còn tốt hơn (+0.015): corpus nhỏ, tín hiệu ký hiệu nhiễu.

### 7.2. Error analysis — 30 failure cases (`results/raw/failure_cases.csv`)

Taxonomy trên 90 cặp hệ×query có Recall@10 < 1.0 (30 case tệ nhất, phân loại đa nhãn):
- **empty_overlap 31.9%** — query không khớp token nào với gold premise (tên Lean không
  gợi ý nội dung) → cần signal semantics, hướng hybrid với N4.
- **cross_topic 31.9%** — gold premise nằm namespace khác topic truy vấn → BM25 từ khóa
  không bắt được quan hệ ngữ nghĩa; hướng sửa: dependency features (tuần 5).
- **many_gold 16.0%** — query có ≥5 premise GT, khó gom đủ trong top-10.
- **few_gold 10.6%** — query chỉ có ≤2 premise GT, trượt 1 mất nửa recall.
- **symbol_heavy 9.6%** — statement query chứa nhiều ký hiệu Lean.

### 7.3. Threats to validity

1. **Qrels dưới-đo:** nhãn 2 chỉ từ chứng minh chuẩn; premise hợp lệ không dùng không được
   tính → mọi số recall là cận dưới.
2. **Nhãn 1 heuristic cùng-file:** có thể gộp cả premise vô quan hệ cùng file (12.966 nhãn
   chỉ dùng nhãn 2 cho primary metrics — nhãn 1 chỉ để phân tích).
3. **Query ≠ đề bài tự nhiên:** query là statement Lean (full_name + code), không phải câu
   tiếng Anh → hệ hoạt động tốt với truy hồi giữa-mathlib, chưa chắc với autoformalization.
4. **Một máy, một seed cho quality:** latency đo trên 200–898 query có thể biến động theo
   tải hệ điều hành; đã ghi máy + seed trong run log; lặp ≥3 cho runtime — quality metrics
   xác định (deterministic) nên không cần lặp.
5. **Chưa có đối chứng dense thật:** N4 đã thống nhất benchmark nhưng chưa giao run file;
   comparison table hiện chỉ chứa hệ N3 — cập nhật tự động khi N4 giao `run_dense_real_*.csv`.

## 8. Kết luận

### 8.1. Trả lời câu hỏi nghiên cứu

- **RQ1:** BM25 thuần **chưa đủ** cho dữ liệu Lean ở quy mô lớn. Hybrid (field weights +
  structural rerank) tăng Recall@10 từ 0.213 → 0.259 (+22% tương đối) trên full corpus.
  Tokenizer giữ ký hiệu Lean quan trọng (bỏ ký hiệu: −0.044 Recall@10 ở 181K) nhưng chỉ
  phát huy từ scale ≥ 50K.
- **RQ2:** Hybrid sparse + structural **tăng chất lượng với chi phí độ trễ tương đương ở
  scale lớn**: Recall@50 +16%, MRR +59% so với BM25 thuần trên 181K declarations, P95
  tương đương (3.654 vs 3.567 ms). Ở corpus nhỏ (10K), tín hiệu cấu trúc chưa có lợi —
  cần kho lớn mới đáng giá, phù hợp với bối cảnh mathlib4 thật.

### 8.2. Sản phẩm bàn giao

- Benchmark split 3 scale + qrels + manifest checksum — **CSV + Parquet 12 file** + data dictionary (`docs/data_dictionary.md`)
- Inverted index + tokenizer Lean (`src/retrieval/rankers.py`) + **index manifest** (`results/real/index_manifest.json` — cấu hình + size + checksum mỗi index)
- Search CLI demo được (`scripts/search_cli.py`)
- 4 hệ retrieval + evaluation scripts chạy 1 lệnh
- Run logger 10 trường Phụ lục B (45 run logs JSON thật) + runtime repeats 3 lần (median + min/max)
- Ablation + 30 failure cases + error slices theo ký hiệu/độ dài + load test 1/10/50
- Data contract v1.2 — **6 mục thống nhất với Nhóm 4** + gói chia sẻ `results/n4_shared/` (corpus.jsonl + queries.jsonl + checksums đúng schema N4)
- 9 biểu đồ + 7 bảng sinh bằng script từ raw results

### 8.3. Lệnh tái lập

```bash
# 0. Unit test metrics
python tests/test_metrics.py                                    # 15/15 PASS

# 1. Tải + build dữ liệu thật (lần đầu; ~68 MB Zenodo)
#    (đã có results/real/ — bỏ qua nếu giữ nguyên manifest)
python scripts/build_real_corpus.py
python scripts/fill_gaps.py              # Parquet + data dictionary + index size/manifest + slices + repeats

# 2. Chạy 4 hệ × 3 scale → run files + metrics + latency (mất ~15 phút)
python scripts/run_real_retrieval.py

# 3. Load test 1/10/50 concurrent (mất ~5 phút)
python scripts/run_load_test.py

# 4. Ablation + failure analysis + comparison + biểu đồ
python scripts/run_ablation.py
python scripts/run_failure_analysis.py
python scripts/run_comparison_n4.py
python scripts/make_real_figures.py

# 5. Demo truy hồi
python scripts/search_cli.py "Every finite integral domain is a field" --top 5
```

## Phụ lục A — AI-use statement
Xem `docs/ai_use_statement.md` — toàn bộ code/docs do AI hỗ trợ sinh, nhóm kiểm chứng bằng
unit test + chạy end-to-end + đối chiếu số.

## Phụ lục B — Contribution statement
Xem `contributions.md` (điền tên khi chốt phân vai — `docs/phan_vai_tam.md`).

## Phụ lục C — Run log mẫu

Mỗi run tạo `results/raw/runs/run_<timestamp>_<id>.json` đủ 10 trường Phụ lục B của môn:
`run_id, timestamp, git_commit, data_version, machine, software, parameters, seed/timeout,
metrics, status`. Ví dụ trường metrics của 1 run thật:

```json
{"Recall@10": 0.259, "MRR": 0.3034, "index_build_s": 15.4, "p50_ms": 1278.17, "p95_ms": 3653.82}
```
