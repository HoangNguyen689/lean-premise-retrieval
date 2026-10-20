# PHÂN VAI NHÓM 3 — Bản tạm (chốt muộn nhất cuối tuần 1)

> Bạn (chủ file này) = **TV6 — Evaluation/Error Analysis** (đã có sản phẩm sẵn).
> 5 vai còn lại phân tạm theo nguyên tắc: (1) ai đã thể hiện kỹ năng phù hợp thì nhận vai đó;
> (2) TV6 không phụ thuộc ai — mọi vai vắng mặt, TV6 tự mock dữ liệu thay (`make_mock_end_to_end.py`);
> (3) **mỗi vai phải có người dự phòng** chạy lại + giải thích được khi bảo vệ.
> Cách dùng: đổi `TVx [TẠM]` thành tên thật khi nhóm họp; nếu ai đó không nhận, đổi chỗ trống
> cột "Người dự phòng" lên làm chính.

## 1. Bảng phân vai

| Vai | Người chính | Người dự phòng | Trạng thái |
|-----|-------------|----------------|------------|
| TV1 — Data/Extraction | `TV1 [TẠM — đề xuất: bạn mạnh Python/data]` | **TV6** (mock corpus sẵn: `make_mock_end_to_end.py`) | ⏳ chờ chốt |
| TV2 — Indexing | `TV2 [TẠM]` | TV3 (cùng làm việc trên index khi cài BM25) | ⏳ chờ chốt |
| TV3 — BM25 Baseline | `TV3 [TẠM]` | TV4 (hai vai dùng chung rank_bm25/tokenizer) | ⏳ chờ chốt |
| TV4 — Structural Features | `TV4 [TẠM]` | TV3 (đều sửa tokenizer/field weights) | ⏳ chờ chốt |
| TV5 — Serving/Performance | `TV5 [TẠM]` | TV6 (chạy được load test nhỏ qua eval scripts) | ⏳ chờ chốt |
| TV6 — Evaluation/Error Analysis | **BẠN** | TV3 (chỉ cần biết đọc run CSV + gọi `metrics.py`) | ✅ chốt |

## 2. Vì sao dự phòng được thiết kế như vậy

- **TV6 dự phòng TV1**: TV1 là vai phụ thuộc cao nhất (đàm phán N4 + tải dữ liệu). TV6 giữ sẵn
  corpus mock theo đúng data contract → cả nhóm không bao giờ bị chặn.
- **TV3 ↔ TV4 dự phòng lẫn nhau**: cả hai cùng đụng tokenizer/BM25/index — người nào vắng,
  người kia vẫn build được biến thể.
- **TV3 dự phòng TV6**: script đánh giá đã là "một lệnh" (`run_all_evaluations.py`); chỉ cần
  đọc 2 cột CSV là tính được metric — dễ bám nhất cho người mới.
- **TV6 dự phòng TV5**: latency measure của TV5 (tuần 3+) nằm trong eval pipeline; TV6 chạy
  được, nhưng khi bảo vệ phải để TV5 chính là người giải thích cách đo P50/P95.

## 3. Hợp đồng trách nhiệm từng vai (điều mọi người phải ký)

1. Người chính chịu trách nhiệm minh chứng đúng hạn tuần của mình (theo ma trận ở
   `Nhom3_Lean_Retrieval_TongHop.md` mục 15).
2. Người dự phòng phải **chạy lại được** sản phẩm của người chính ít nhất 1 lần trước tuần 7
   (đồng thời là buổi tập giải thích cho bảo vệ).
3. Mọi run thí nghiệm từ tuần 7 phải ghi đủ **10 trường Phụ lục B** — dùng sẵn
   `src/evaluation/run_logger.py` (import 3 dòng là xong, không tự ghi tay).
4. Khi bảo vệ: mọi người trả lời được toàn pipeline (dùng slide kiến trúc + demo end-to-end).
5. AI hỗ trợ phải khai báo trong `docs/ai_use_statement.md` — nhóm kiểm chứng code/kết luận.

## 4. Kịch bản phòng hờ "người khác chậm" (đã cài sẵn, TV6 không phải lo)

| Sự cố | TV6 đã chuẩn bị gì |
|---|---|
| TV1 chưa tải được LeanDojo (tuần 2) | `make_mock_end_to_end.py` sinh corpus/query/qrels đúng 6-field contract cho cả 3 scale → TV2-TV6 làm tiếp bình thường |
| TV3 chưa xong BM25 baseline (tuần 3) | `run_bm25_*.csv` mock có sẵn → eval pipeline chạy đủ; khi TV3 xong, chỉ cần chép run thật vào thay mock |
| TV4 chưa xong hybrid (tuần 5) | `run_hybrid_*.csv` mock + ablation script sẵn → bảng ablation chạy được |
| Nhóm 4 chưa đồng ký contract | `data_contract_v1.md` đánh dấu DRAFT + mục §7 ghi rõ "N4 trễ không chặn N3" |
| Nhóm 4 chưa giao run (tuần 9) | `run_comparison_n4.py` tự dùng mock và ghi chú rõ trong bảng; khi N4 giao, chép `run_dense_*.csv` thật vào `results/raw/` và chạy lại |

> ⚠️ Quy tắc đạo đức: file mock chỉ để **không bị chặn**, tuyệt đối không nộp số mock như số
> thật. Mọi bảng trong báo cáo phải ghi rõ nguồn dữ liệu (mock hay thật) — mock chỉ tồn tại
> cho đến khi run thật có mặt.

## 5. MA TRẬN CHIA VIỆC CHI TIẾT THEO TUẦN (người × tuần) — cho buổi họp nhóm

> Migrat từ `Nhom3_Lean_Retrieval_TongHop.md` (đã xóa). Ký hiệu ★ = người chính chịu
> trách nhiệm chính cho việc đó trong tuần. Mỗi thành viên xem đúng dòng của mình.

### TV1 — Data/Extraction
| Tuần | Nhiệm vụ chính | Minh chứng |
|------|----------------|-----------|
| T1 | Định nghĩa schema truy vấn/premise; đàm phán data contract với Nhóm 4 | Benchmark spec (đồng ký với TV6) |
| T2 | Trích xuất snapshot nhỏ, các trường Lean → Parquet | Parquet sample + data dictionary |
| T3 | Cung cấp corpus đã sạch cho BM25; checksum/manifest | Corpus manifest |
| T4 | Bổ sung trường ký hiệu/namespace vào schema | Schema v0.2 + tests |
| T5 | Trích dependency graph cho đặc trưng cấu trúc | Dependency dump |
| T6 | Chuẩn bị data cho load test; data card v1.0 | Data card |
| T7 | Chuẩn bị 3 bộ corpus 10K/50K/full | 3 corpus manifest |
| T8 | Kiểm tra dữ liệu của các failure cases | Data audit cho 30 cases |
| T9 | Cập nhật data card; hỗ trợ tái lập | Data card final |
| T10 | Hỗ trợ demo; trả lời phần data khi bảo vệ | Q&A prep |

### TV2 — Indexing
| Tuần | Nhiệm vụ chính | Minh chứng |
|------|----------------|-----------|
| T1 | Đề xuất định dạng index; khảo sát OpenSearch vs Lucene vs rank_bm25 | So sánh công cụ (1 trang) |
| T2 | Xây inverted index trên sample | Index sample |
| T3 | Index cho baseline end-to-end | Index build script |
| T4 | Index nhiều field (statement, name, namespace) | Multi-field index |
| T5 | Index cho hybrid: lưu sparse scores + structural signals | Index v0.1 |
| T6 | Index manifest: checksum, version, build config | Index manifest |
| T7 | Build index 10K/50K/full; đo build time + size | Bảng build time/size |
| T8 | Index tái tạo được từ scripts | Repro test |
| T9 | Index final cho comparison | Final index |
| T10 | Hỗ trợ demo | Q&A prep |

### TV3 — BM25 Baseline
| Tuần | Nhiệm vụ chính | Minh chứng |
|------|----------------|-----------|
| T1 | Đề xuất 20 truy vấn kiểm tra đầu tiên | Query set v0 (đồng ký với TV6) |
| T2 | Chạy thử BM25 trên sample | Kết quả thử nghiệm |
| T3 | **Cài TF-IDF/BM25 baseline; Recall@k + MRR end-to-end** | Raw ranking results |
| T4 | BM25 trên các biến thể tokenizer/field | Bảng so sánh biến thể |
| T5 | Xuất sparse scores cho hybrid reranker | Sparse score API |
| T6 | BM25 tích hợp vào search service | Service endpoint |
| T7 | Chạy baseline ở 3 mức scale + 3 mức tải | Raw baseline results |
| T8 | Phân tích baseline failures | Failure cases (phần BM25) |
| T9 | Bảng so sánh sparse/dense/hybrid | Comparison table |
| T10 | Demo baseline | Q&A prep |

### TV4 — Structural Features
| Tuần | Nhiệm vụ chính | Minh chứng |
|------|----------------|-----------|
| T1 | Nghiên cứu đặc trưng cấu trúc Lean (ký hiệu, namespace) | Đề xuất đặc trưng |
| T2 | Thiết kế tokenizer giữ ký hiệu Lean | Tokenizer spec |
| T3 | Tokenizer cơ bản cho baseline | Tokenizer v0 |
| T4 | **Tokenizer ký hiệu + field weighting + namespace** | Biến thể retrieval + unit tests |
| T5 | **Dependency features + hybrid reranking** | Model v0.1 + ablation plan |
| T6 | Tối ưu reranking trong service | Reranker endpoint |
| T7 | Chạy hybrid ở 3 mức scale | Raw hybrid results |
| T8 | Ablation từng đặc trưng | Bảng ablation |
| T9 | Viết phần phương pháp trong report | Report draft |
| T10 | Demo hybrid | Q&A prep |

### TV5 — Serving/Performance
| Tuần | Nhiệm vụ chính | Minh chứng |
|------|----------------|-----------|
| T1 | Đề xuất interface API/CLI; khảo sát FastAPI | API design draft |
| T2 | CLI truy vấn thử trên sample | CLI v0 |
| T3 | Đo latency BM25 (P50/P95) | Latency profile v0 |
| T4 | Benchmark các biến thể | Latency table |
| T5 | **Latency profile cho hybrid** | Latency profile |
| T6 | **Đóng gói service; cache; batch query** | API/CLI + load test nhỏ |
| T7 | **Load test 1/10/50 truy vấn đồng thời** | QPS/P95 raw data |
| T8 | Profile bottleneck của reranking | Bottleneck report |
| T9 | Service ổn định cho comparison | Service release |
| T10 | Demo trực tiếp | Live demo |

### TV6 — Evaluation/Error Analysis (BẠN)
| Tuần | Nhiệm vụ chính | Minh chứng |
|------|----------------|-----------|
| T1 | Định nghĩa protocol đánh giá; chốt với Nhóm 4 | Evaluation protocol (đồng ký với TV1) |
| T2 | Query set + qrels (đánh giá chuẩn) cho sample | Query set + qrels |
| T3 | Chạy đánh giá baseline: Recall@k, MRR | Metric report v0 |
| T4 | Đánh giá các biến thể | Metric table |
| T5 | Ablation plan; nDCG@k | Ablation plan |
| T6 | Smoke test service metrics | Test report |
| T7 | Tổng hợp raw results; kiểm tra reproducibility | Consolidated raw data |
| T8 | **Error analysis: 30 failure cases theo chủ đề/ký hiệu/độ dài** | Error taxonomy |
| T9 | **Comparison table với Nhóm 4; viết report** | Report 8–12 trang |
| T10 | Chuẩn bị bảo vệ; AI-use statement | Defense slides |

> ⚠️ **Cập nhật thực tế (2026-10-15):** nhiều việc trong ma trận trên đã được làm sẵn/hộ
> (xem `contributions.md` cột "Phần đã có sẵn trong repo") — mỗi thành viên khi nhận vai
> chỉ cần: đọc hiểu phần của mình + chạy lại được + bổ sung phần chưa có (vd. TV4 tuning
> hệ số rerank, TV3 tuning k1/b trên dev split).
