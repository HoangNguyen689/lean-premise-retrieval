# THÀNH VIÊN 3: BM25 BASELINE (PHẦN BẮT BUỘC TỐI THIỂU)

## 1. Việc bắt buộc của TV3

Theo đề bài, TV3 phải có một **baseline TF-IDF hoặc BM25 mặc định trên statement đã tách từ**, không dùng embedding và không dùng dependency. Baseline phải dùng **cùng dữ liệu, cùng split, cùng máy** với phương pháp chính. Kết quả cần có Recall@k, MRR và raw ranking, chạy ở **3 kích thước index**.

Nhóm đã viết sẵn phần này: hệ `bm25` trong `src/retrieval/systems.py`. Vì vậy việc tối thiểu của bạn là:

| # | Việc | Thời gian |
|---|---|---|
| 1 | Học 5 kiến thức nền (mục 2) | 3–4 giờ |
| 2 | Đọc hiểu 4 file (mục 3) | 2 giờ |
| 3 | Chạy lại baseline để có số đúng (mục 4) | 1 giờ (máy tự chạy) |
| 4 | Viết khoảng nửa trang báo cáo cho phần baseline (mục 5) | 1 giờ |
| 5 | Ôn 8 câu hỏi bảo vệ (mục 6) | 1 giờ |

TF-IDF, tinh chỉnh k1/b hay so sánh với OpenSearch **không bắt buộc**: đề chỉ yêu cầu "TF-IDF *hoặc* BM25".

---

## 2. Kiến thức tối thiểu cần học

### 2.1. Bài toán premise retrieval
- **Premise** là một định lý hoặc bổ đề đã có sẵn trong mathlib, ví dụ `Nat.add_comm`.
- **Query** là statement của định lý cần chứng minh.
- Hệ phải trả về danh sách premise xếp theo mức độ liên quan. **Premise đúng** là các premise thực sự được dùng trong chứng minh gốc, lấy từ trace của LeanDojo; trong file `qrels` chúng có nhãn = 2.
- Quy tắc quan trọng: **không được trả về chính định lý đang truy vấn**. Nếu không lọc, nó luôn đứng hạng 1 vì giống query 100%.

### 2.2. Tách từ (tokenize)
Máy không hiểu câu, nên câu phải được cắt thành các "từ" (token). Hàm `tokenize` của nhóm:
```
"theorem Nat.add_comm : ∀ (n m : ℕ), n + m = m + n"
→ theorem, nat, add, comm, :, ∀, (, n, m, :, ℕ, ), ,, n, m, m, n
```
Tên định lý được tách theo dấu `.` và `_`, chữ được chuyển thành chữ thường, và các ký hiệu `∀ ℕ ( : ,` được giữ lại. Riêng `+` và `=` bị mất: đây là một hạn chế nên biết.

### 2.3. Inverted index (chỉ mục đảo)
Inverted index là một bảng tra **từ → danh sách tài liệu chứa từ đó**, ví dụ `comm → {A: 1 lần, C: 1 lần}`. Khi có query, hệ chỉ xét các tài liệu chứa từ của query thay vì đọc cả 181 nghìn tài liệu. Đây là lý do cần index khi dữ liệu lớn.

### 2.4. Công thức BM25 (phải giải thích được)

$$\text{score}(D,Q)=\sum_{t\in Q}\text{IDF}(t)\cdot\frac{tf\,(k_1+1)}{tf+k_1\left(1-b+b\,\frac{|D|}{avgdl}\right)}\qquad \text{IDF}(t)=\ln\left(1+\frac{N-df+0.5}{df+0.5}\right)$$

| Ký hiệu | Nghĩa | Ý tưởng |
|---|---|---|
| tf | số lần từ t xuất hiện trong tài liệu D | xuất hiện nhiều thì liên quan hơn |
| df | số tài liệu chứa t | từ hiếm có giá trị phân biệt cao hơn (IDF lớn) |
| N, avgdl | số tài liệu, độ dài trung bình | |
| \|D\| | độ dài tài liệu D (số token) | |
| **k1 = 1.5** | độ bão hòa | từ lặp 10 lần **không** đáng gấp 10 lần lặp 1 lần |
| **b = 0.75** | chuẩn hóa độ dài | tài liệu dài tự nhiên chứa nhiều từ hơn nên bị phạt bớt |

**Ví dụ tính tay** (bạn nên tự làm lại trên giấy). Kho có 3 tài liệu: A = `add comm add` (3 token), B = `add zero` (2 token), C = `mul comm one two` (4 token). Query là `comm`.
- N = 3, df(comm) = 2, nên IDF = ln(1 + 1.5/2.5) = ln 1.6 ≈ **0.470**
- avgdl = (3 + 2 + 4) / 3 = 3
- A: tf = 1, |D| = 3, nên 1 × 2.5 / (1 + 1.5 × (0.25 + 0.75 × 3/3)) = 2.5 / 2.5 = 1, và điểm = **0.470**
- C: tf = 1, |D| = 4, nên 2.5 / (1 + 1.5 × (0.25 + 0.75 × 4/3)) = 2.5 / 2.875 = 0.870, và điểm = **0.409**
- B không chứa `comm` nên không có điểm. Thứ hạng: **A > C**, vì A ngắn hơn (tác dụng của b).

**So với TF-IDF:** TF-IDF không có bão hòa TF (k1) và không điều chỉnh được mức chuẩn hóa độ dài (b). Đó là lý do BM25 thường tốt hơn.

### 2.5. Chỉ số đánh giá
- **Recall@k** = (số premise đúng nằm trong top-k) / (tổng số premise đúng). Ví dụ: có 4 premise đúng, top-10 chứa 1 thì Recall@10 = 0.25. Đây là chỉ số chính, vì bộ chứng minh chỉ cần premise đúng *có mặt* trong top-k.
- **MRR** = trung bình của 1/(hạng của premise đúng *đầu tiên*). Premise đúng đầu tiên ở hạng 2 thì RR = 0.5; không tìm thấy thì RR = 0.
- **P50/P95 latency**: 50% và 95% số query có thời gian chạy nhỏ hơn giá trị này. Dùng P95 thay vì trung bình để thấy các trường hợp chậm nhất.

**Tài liệu đọc (chỉ cần chừng này):** sách Manning, *Introduction to Information Retrieval* (miễn phí online), chương 1 (inverted index), chương 6.2 (TF-IDF), chương 8.1–8.4 (Recall, MRR) và mục 11.4.3 (BM25).

---

## 3. File cần đọc (theo thứ tự, chỉ những phần ghi rõ)

1. **`docs/data_contract_v1.md`**: §3 (6 cột dữ liệu), §5.1 (3 scale 10K/50K/181K), §5.2 (nhãn 2 là premise đúng), §5.4 (không trả về chính query).
2. **`src/retrieval/systems.py`** (phần của bạn):
   - dòng 40–61: hàm `tokenize` (mục 2.2)
   - dòng 66–95: xây inverted index, df, avgdl (mục 2.3)
   - dòng 97–99: công thức IDF
   - dòng 101–112: hàm `search`, công thức BM25 ở dòng 109–110 (mục 2.4)
   - dòng 151–154: hệ `bm25`, lọc chính query (`pid != self_name`)
3. **`src/evaluation/metrics.py`**: `recall_at_k` (dòng 34) và `reciprocal_rank` (dòng 46) (mục 2.5).
4. **`scripts/run_real_retrieval.py`**: dòng 60–100. Script này chạy baseline ở 3 scale, đo thời gian từng query và ghi kết quả.

Có thể **bỏ qua**: mọi thứ liên quan đến `bm25_field`/`hybrid` (TV4), load test (TV5), và các file mock.

---

## 4. Việc phải chạy

Mở Command Prompt trong thư mục dự án:

```bat
pip install pandas pyarrow matplotlib
python download_data.py
python tests\test_metrics.py
python scripts\run_real_retrieval.py
python scripts\tv3_kiem_tra_tay.py
```

| Lệnh | Tác dụng | Kiểm tra |
|---|---|---|
| `download_data.py` | Tải dữ liệu LeanDojo (68 MB) và tạo corpus cho 3 scale | có `results\real\corpus_s3.csv` |
| `test_metrics.py` | Kiểm tra hàm tính chỉ số | in ra `15 PASS, 0 FAIL` |
| `run_real_retrieval.py` | **Chạy lại baseline** ở 3 scale (khoảng 30–60 phút) | sinh `results\real\eval_summary.csv`, `latency.csv`, `run_bm25_s1/s2/s3.csv` |
| `tv3_kiem_tra_tay.py` | Kiểm chứng tay 1 query (script duy nhất mình thêm vào) | hiện dòng `✓ KHỚP` |

**Vì sao bắt buộc chạy lại:** các file `run_bm25_*.csv` có sẵn trong gói là bản cũ. Ở đó cả 898/898 query đều trả về chính nó ở hạng 1, tức là vi phạm quy tắc ở mục 2.1. Số trong README cũng lấy từ bản cũ này. Sau khi chạy lại, mở `run_bm25_s1.csv` và kiểm tra rằng dòng đầu tiên không còn có `query_id` (bỏ chữ Q ở đầu) trùng với `premise_id`.

Chụp màn hình kết quả `tv3_kiem_tra_tay.py`. Đây là bằng chứng bạn hiểu và kiểm chứng được code.

---

## 5. Báo cáo phần baseline (khoảng nửa trang)

Lấy số từ `results\real\eval_summary.csv` (các dòng `bm25`) và `results\real\latency.csv`:

> **Baseline BM25.** Statement Lean được tách từ bằng `tokenize` (tách tên theo `.`/`_`, giữ ký hiệu Lean). Chỉ mục đảo được xây trên trường `statement`. BM25 dùng tham số mặc định k1 = 1.5, b = 0.75 và IDF dạng ln(1 + (N − df + 0.5)/(df + 0.5)), không dùng embedding và không dùng dependency. Hệ lọc bỏ chính định lý truy vấn trước khi lấy top-k. Baseline chạy trên cùng dữ liệu, cùng split và cùng máy với các biến thể của nhóm.

| Scale | Recall@1 | Recall@5 | **Recall@10** | Recall@50 | MRR | P50 (ms) | **P95 (ms)** | Build index (s) |
|---|---|---|---|---|---|---|---|---|
| 10K | | | | | | | | |
| 50K | | | | | | | | |
| 181K | | | | | | | | |

> **Nhận xét** (điền theo số): Recall@10 ở 181K đạt …, nghĩa là trung bình chỉ khoảng …% premise đúng nằm trong top-10. P95 tăng từ … ms (10K) lên … ms (181K) khi corpus tăng 18 lần. Lý do là các token như `theorem`, `:`, `(` xuất hiện ở hầu hết tài liệu, nên mỗi query vẫn phải duyệt gần hết kho. **Hạn chế:** tokenizer bỏ `+`, `=`; nhiều query không có từ chung với premise đúng nên BM25 không thể tìm ra. Đây là lý do nhóm thử thêm field và structural features (RQ1).

---

## 6. Tám câu hỏi bảo vệ cần trả lời được

1. **BM25 khác TF-IDF ở đâu?** BM25 có bão hòa TF (k1) và chuẩn hóa độ dài điều chỉnh được (b).
2. **k1, b là gì? Vì sao chọn 1.5 và 0.75?** Xem bảng ở mục 2.4. Đây là giá trị mặc định chuẩn (của thư viện `rank_bm25`), đúng yêu cầu "BM25 mặc định" của đề.
3. **IDF có ý nghĩa gì?** Từ càng hiếm thì càng có giá trị. Ví dụ token `:` có trong mọi tài liệu nên IDF ≈ 0, còn tên riêng như `isroot` thì IDF cao.
4. **Inverted index giúp gì?** Chỉ xét các tài liệu chứa từ của query, không phải quét toàn bộ kho. Có thể minh họa bằng ví dụ ở mục 2.3.
5. **Làm sao tránh rò rỉ dữ liệu?** Lọc chính định lý truy vấn khỏi kết quả (dòng 151–154 của `systems.py`). Bản cũ chưa lọc nên bạn đã chạy lại.
6. **Vì sao dùng Recall@10 làm chỉ số chính?** Bộ chứng minh chỉ cần premise đúng có mặt trong ngữ cảnh. Thứ tự chính xác bên trong top-10 ít quan trọng hơn.
7. **Recall@10 khác MRR thế nào?** Recall@10 đo tỷ lệ premise đúng nằm trong top-10. MRR chỉ quan tâm premise đúng đầu tiên xuất hiện ở hạng mấy. Có thể demo bằng `tv3_kiem_tra_tay.py`.
8. **Baseline có công bằng không?** Có: cùng file dữ liệu (có checksum), cùng script và cùng máy với hybrid. Tham số không được chỉnh để phương pháp mới trông tốt hơn.

---

## 7. Nên báo cho TV6 (người viết báo cáo chung)

Chỉ cần gửi 2 điểm liên quan trực tiếp đến baseline của bạn:
1. Run file cũ trong `results/real/` còn trả về chính query, nên đã chạy lại `run_real_retrieval.py`. README và `report_draft.md` cần cập nhật số theo `eval_summary.csv` mới.
2. Trong `report_draft.md`, bảng mục 6.1 trộn số của hai lần chạy (ví dụ MRR của BM25 ở 181K ghi 0.1907, trong khi `eval_summary` là 0.2694). Câu "P95 hybrid thấp hơn BM25" cần kiểm tra lại với `latency.csv`.
