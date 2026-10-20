# Evaluation Protocol — Nhóm 3 Lean Premise Retrieval

> Phiên bản: v0.1 (tuần 1) | Người chịu trách nhiệm: TV6 — Evaluation/Error Analysis
>
> Tài liệu này cần được **Nhóm 4 đồng ý** vì hai nhóm dùng chung split và benchmark.

---

## 1. Bài toán đánh giá

**Đầu vào:** một truy vấn (statement định lý cần chứng minh, dạng tự nhiên/LaTeX/Lean).

**Đầu ra của hệ thống:** danh sách `k` premise (định lý/bổ đề trong mathlib4) xếp hạng theo độ liên quan giảm dần.

**Đánh giá:** so sánh danh sách trả về với ground truth (qrels) để tính chất lượng; đo thời gian phản hồi để tính độ trễ.

## 2. Định nghĩa tập dữ liệu đánh giá

### 2.1. Split truy vấn — premise

| Tập | Vai trò | Ghi chú |
|-----|---------|---------|
| **Corpus (premise pool)** | Toàn bộ định lý/bổ đề có thể được truy hồi | Từ mathlib4 declarations, có version + commit |
| **Query set** | Truy vấn dùng để đánh giá | Tách **riêng**, không trùng statement với corpus quá 90% ký tự |
| **Dev set** | Tinh chỉnh tham số (field weights, reranker) | Tách từ query set, **không được dùng để báo cáo kết quả cuối** |
| **Test set** | Báo cáo kết quả cuối cùng | Chạy đúng 1 lần lúc báo cáo, không tinh chỉnh trên tập này |

> **Nguyên tắc:** mọi split cố định theo file manifest có checksum; version hóa dạng `split-v1.0-<commit>`. Nhóm 3 và Nhóm 4 dùng **cùng một split**.

### 2.2. Qrels (ground truth)

Với mỗi truy vấn, danh sách premise liên quan được gán nhãn theo 3 mức:

| Nhãn | Ý nghĩa | Nguồn |
|------|---------|-------|
| **2 — Relevant trực tiếp** | Premise xuất hiện trong chứng minh tham chiếu (từ LeanDojo trace) | Tự động từ benchmark |
| **1 — Relevant gián tiếp** | Premise cùng namespace/dependency với các premise trực tiếp | Bán tự động, kiểm tra tay |
| **0 — Không liên quan** | Mọi premise còn lại | Mặc định |

> Vì gán nhãn đầy đủ toàn bộ corpus là bất khả thi (hàng trăm nghìn premise), ta dùng **pooling**: gộp top-50 của mọi hệ thống tham gia đánh giá (BM25, hybrid, và của Nhóm 4) thành pool, gán nhãn thủ công phần pool đó. Cách này là chuẩn thực hành trong IR (từ TREC).

## 3. Định nghĩa chỉ số

### 3.1. Recall@k (PRIMARY METRIC 1)

Tỷ lệ premise liên quan (nhãn ≥ 1... hoặc chỉ nhãn 2 — xem §3.4) xuất hiện trong top-k kết quả:

```
Recall@k(q) = |{premise liên quan} ∩ {top-k trả về}| / |{premise liên quan của q}|
```

Báo cáo: **macro-average trên toàn bộ query set**. Tính tại k = 1, 5, 10, 50.

### 3.2. MRR — Mean Reciprocal Rank (PRIMARY METRIC 2)

Nghịch đảo hạng của kết quả liên quan **đầu tiên**:

```
RR(q) = 1 / rank của kết quả liên quan đầu tiên
MRR = mean(RR) trên toàn query set
```

> Nếu không có kết quả liên quan nào trong top-k, RR(q) = 0.

### 3.3. nDCG@k

Chỉ số thứ hai để phân biệt kết quả liên quan mạnh/yếu (nhãn 2 vs 1):

```
DCG@k = Σ(i=1..k) (2^rel_i − 1) / log2(i + 1)
IDCG@k = DCG@k của thứ hạng lý tưởng
nDCG@k = DCG@k / IDCG@k
```

Báo cáo tại k = 10.

### 3.4. Quy ước khi tính Recall

- Cấu hình chính (báo cáo chính thức): Recall tính trên **nhãn 2** (relevant trực tiếp).
- Cấu hình phụ: Recall trên **nhãn ≥ 1** — báo cáo riêng, để so sánh.
- Mọi bảng kết quả phải ghi rõ dùng quy ước nào.

### 3.5. Chỉ số hiệu năng (TV5 phụ trách đo, TV6 tổng hợp)

| Chỉ số | Cách đo |
|--------|---------|
| P50/P95 latency | Phân bố thời gian phản hồi trên ≥ 100 truy vấn đơn lẻ |
| QPS | Số truy vấn/giây dưới tải đồng thời 1/10/50 |
| Index build time, index size | Ghi tại lúc build, kèm manifest |

## 4. Quy tắc chạy thí nghiệm (khớp yêu cầu môn học)

1. **Cùng điều kiện:** baseline và phương pháp chính dùng cùng dữ liệu, split, phần cứng, timeout.
2. **Lặp:** runtime biến động → chạy ≥ 3 lần, báo **median + min–max**.
3. **Ghi log mỗi run** theo Phụ lục B của hướng dẫn: run_id, timestamp, git_commit, data_version, machine, software, parameters, seed/timeout, metrics, status/log.
4. **Biểu đồ** sinh từ raw results bằng script (`results/figures/` sinh từ `results/raw/`), không vẽ tay.
5. **Không chọn lọc:** báo cáo cả kết quả bất lợi cho phương pháp chính.

## 5. Quy trình tạo query set (20 truy vấn tuần 1)

Nguồn truy vấn: statement từ LeanDojo Benchmark 4 (tách riêng khỏi corpus).

Phân bố 20 truy vấn kiểm tra (đảm bảo đa dạng, không thiên về một chủ đề):

| Nhóm truy vấn | Số lượng | Mục đích |
|----------------|----------|----------|
| Đại số (ring, group, field) | 4 | Chủ đề phổ biến trong mathlib |
| Giải tích (limit, continuity, measure) | 4 | Statement dài, nhiều ký hiệu |
| Số học tự nhiên/số nguyên | 3 | Statement ngắn, dễ kiểm tra tay |
| Cấu trúc thứ tự/tập hợp | 3 | Nhiều ký hiệu logic (∈, ⊆, ⋃) |
| Topology/category | 3 | Namespace sâu, dependency phức tạp |
| Khó/biên (statement rất dài hoặc rất ngắn, ký hiệu hiếm) | 3 | Để error analysis sau này |

Mỗi truy vấn lưu: `query_id`, `statement_raw` (nguyên văn), `statement_clean` (đã chuẩn hóa), `namespace`, `gold_premises` (danh sách premise nhãn 2), `difficulty`.

## 6. Tiêu chí chấp nhận của protocol

- [ ] Nhóm 4 xác nhận cùng split + cùng quy ước Recall
- [ ] Query set v0 (20 truy vấn) có manifest + checksum
- [ ] Script metrics pass unit test (so với kết quả tính tay)
- [ ] Cách tạo qrels (pooling top-50) được cả nhóm thống nhất

## 7. Lịch sử phiên bản

| Phiên bản | Ngày | Thay đổi |
|-----------|------|----------|
| v0.1 | Tuần 1 | Bản đầu — định nghĩa metrics, split, qrels, 20 truy vấn |
