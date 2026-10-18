# Đánh giá báo cáo và gợi ý cải thiện

**Báo cáo:** Truy hồi premise cho Lean 4 bằng chỉ mục thưa và tín hiệu cấu trúc ở quy mô thư viện mathlib4, Nhóm 3, INT4418.

**Ngày đánh giá:** 18/10/2026.

**Nguồn chính:** [report.pdf](D:/bigdata/nhom3-lean-retrieval/report/report.pdf), 30 trang PDF. Đã đọc toàn văn và kiểm tra bố cục bằng ảnh render của cả 30 trang. Đối chiếu thêm [hướng dẫn bài tập lớn](D:/bigdata/HuongDan_Bai_Tap_Lon_BigData_INT4418.pdf), mã nguồn liên quan, bảng kết quả và dữ liệu Parquet hiện có trong dự án. Không dùng `report.md`/`report.docx` làm bản báo cáo chuẩn vì README xác định đó là bản nháp cũ.

**Phạm vi:** Đây là đánh giá tài liệu kèm kiểm tra chọn lọc bằng dữ liệu và mã nguồn, không phải xác nhận đã chạy lại toàn bộ benchmark, kiểm thử hay thí nghiệm Spark. Các phép đếm và phép tổng hợp bổ sung dưới đây được tính trực tiếp từ dữ liệu đã lưu; không chạy lại truy hồi và không sửa báo cáo gốc.

**Quy ước vị trí:** “trang 11” là số in trong báo cáo; “PDF 17” là trang thứ 17 của tệp, tính cả bìa và mục lục. Đường dẫn mã nguồn/kết quả trong nội dung tính từ `D:/bigdata/nhom3-lean-retrieval/`.

## 1. Nhận định tổng thể

**Báo cáo có nền tảng kỹ thuật và thực nghiệm tốt, bám sát đề tài, nhưng chưa nên coi là bản sẵn sàng nộp.** Điểm mạnh nhất là chuỗi lập luận từ baseline đến tối ưu hệ thống: không chỉ đưa ra biến thể tốt nhất, mà còn đo baseline đã tinh tham số, phân rã độ trễ, ablation, lỗi truy cập theorem, giới hạn CPU và trường hợp Spark chậm hơn xử lý tuần tự.

Điểm cần cải thiện lớn nhất là **độ chính xác của phạm vi kết luận**. Một số nhận định mạnh hơn bằng chứng hiện có; số theorem sau lọc chưa được báo cáo đúng; lợi ích V5 trên `novel_premises` phụ thuộc cách lấy trung bình; và những việc cần con người hoàn tất vẫn còn để chờ điền.

Nếu chỉ đánh giá chất lượng bản thảo và bằng chứng đã xem, mức tham khảo là **khoảng 8/10**. Đây không phải điểm chấm chính thức: chưa kiểm chứng demo, toàn bộ khả năng tái lập và phần bảo vệ cá nhân. Ưu tiên hiện tại nên là sửa các vấn đề về dữ liệu, kết luận và nghiệm thu trước khi thêm thuật toán.

## 2. Những điểm làm tốt nên giữ lại

| Khía cạnh | Nhận xét | Minh chứng trong báo cáo |
|---|---|---|
| Bài toán và câu hỏi nghiên cứu | RQ1, RQ2 rõ; chọn Recall@10 và P95 ở 10 client làm hai chỉ số chính giúp tránh kể quá nhiều metric rời rạc. | Chương 1, trang 1, PDF 7. |
| Provenance dữ liệu | Có snapshot, checksum, giấy phép, schema, dead-letter; thừa nhận premise sinh tự động không có trong corpus. | Chương 3, trang 3–4, PDF 9–10. |
| Kiến trúc | Phân biệt đường xây chỉ mục và đường phục vụ; mô tả tokenizer, BM25F, accessibility và reranker đủ cụ thể. | Chương 4, trang 5–7, PDF 11–13. |
| Baseline | Có B0 bắt buộc và B0t được tinh tham số; tránh chỉ so phương pháp nâng cao với một baseline yếu. | Mục 5.2–5.3 và Bảng 6.1. |
| Kiểm soát nhãn train | Chia train A/B để tính thống kê và huấn luyện; tính riêng thống kê cho hai split. Đây là lựa chọn đáng ghi nhận. | Mục 3.4, 4.6; `scripts/build_dependency_stats.py`. |
| Khía cạnh Dữ liệu lớn | Có 4 kích thước index, 3 mức tải, nhiều worker, shuffle, bộ nhớ, codec và 2 engine Spark. | Mục 5.4, 6.3–6.5, 7.2. |
| Báo cáo kết quả bất lợi | Nêu Spark RDD chậm, salting không có lợi ở quy mô thử nghiệm, thêm worker không tăng QPS và namespace chưa có tác dụng đo được trong reranker. | Mục 6.4–6.5, 7.1–7.2. |
| Phân tích lỗi | Tìm được lỗi tự truy hồi theorem, sửa bộ lọc và đo lại; xác định giới hạn tập ứng viên. | Mục 7.3–7.4. |
| Trình bày | Bố cục chương, công thức, bảng và số trang nhất quán; qua ảnh render không thấy lỗi tràn lề/chồng chữ rõ rệt. | Toàn bộ PDF. |

## 3. Đối chiếu yêu cầu học phần

Hướng dẫn INT4418, trang 9–11, yêu cầu Nhóm 3 dùng benchmark chung với Nhóm 4, có baseline BM25, ít nhất ba kích thước index, đo chất lượng và độ trễ, phân tích lỗi và index có thể tái tạo.

| Hạng mục theo rubric | Đánh giá hiện tại | Việc cần bổ sung |
|---|---|---|
| Câu hỏi và vai trò Big Data, 10% | Tốt. | Thận trọng với câu “không khả thi” nếu chưa có phép đo quét toàn kho. |
| Dữ liệu và provenance, 15% | Khá tốt nhưng có lỗi thống kê quan trọng. | Phân biệt theorem gốc và theorem còn truy vấn hợp lệ; kiểm tra tính novel sau lọc. |
| Kiến trúc và triển khai, 20% | Mô tả tốt, có minh chứng mã nguồn và kết quả. | Làm rõ đồ thị, phạm vi thông tin được phép dùng và luồng V5. |
| Baseline, 10% | Tốt. | Thêm đối chứng accessibility tương đương khi giải thích đóng góp; sửa diễn giải Lucene. |
| Scalability, 20% | Mạnh so với yêu cầu tối thiểu. | Thống nhất số cấu hình/lần chạy; giữ giới hạn một máy và corpus nhân bản ngay cạnh kết luận. |
| Đánh giá và phân tích, 10% | Nhiều nội dung tốt nhưng còn kết luận quá mạnh. | Bootstrap theo theorem; đánh giá unseen-only; hoàn tất nhãn thủ công. |
| Bàn giao và tái lập, 10% | Có nền tảng nhưng chưa xác nhận đầy đủ. | Khóa môi trường, chốt revision, kiểm tra từ checkout sạch, sinh bảng tự động. |
| Trình bày/đóng góp, 5% | PDF chỉn chu, phần trách nhiệm còn dang dở. | Điền tên chính/dự phòng, xác nhận kiểm tra và minh chứng đóng góp. |

**Chưa hoàn tất yêu cầu phối hợp:** Mục 6.6 vẫn chờ kết quả và xác nhận đặc tả của Nhóm 4. Bảng tham khảo từ bài LeanDojo không thay thế được phép so sánh trên cùng benchmark của hai nhóm.

**Lưu ý độ dài:** Hướng dẫn có hai mốc không thống nhất: trang 2 ghi báo cáo 8–12 trang, còn Phụ lục C trang 27 ghi 12–20 trang. Bản hiện tại có 30 trang PDF, trong đó nội dung Chương 1–8 chiếm 20 trang. Nên chốt cách tính trang theo yêu cầu nộp của lớp; không thể kết luận vi phạm chỉ bằng tổng số trang PDF.

## 4. Những vấn đề ưu tiên sửa

Mức **P1**: ảnh hưởng độ tin cậy hoặc điều kiện nghiệm thu; **P2**: cần cải thiện để bảo vệ kết luận; **P3**: biên tập và trình bày.

### 4.1. P1 — Bảng 3.3 chưa phản ánh số theorem sau lọc

**Vị trí:** Mục 3.4, Bảng 3.3, trang 4, PDF 10.

Caption ghi số theorem và truy vấn “sau lọc”, nhưng hàng theorem vẫn là số theorem gốc của benchmark. Đếm trực tiếp `queries.parquet`, lấy theorem theo cặp `(file_path, theorem_full_name)`, cho kết quả:

| Split | Tập | Theorem gốc theo báo cáo | Theorem còn ít nhất một truy vấn hợp lệ | Truy vấn hợp lệ |
|---|---|---:|---:|---:|
| random | train | 118.517 | 52.663 | 152.330 |
| random | val | 2.000 | 880 | 2.536 |
| random | test | 2.000 | 882 | 2.641 |
| novel_premises | train | 118.517 | 52.047 | 149.459 |
| novel_premises | val | 2.000 | 1.182 | 3.907 |
| novel_premises | test | 2.000 | 1.196 | 4.141 |

Đặc biệt, tập test thực sự được chấm chỉ đại diện **44,1%** theorem gốc ở `random` và **59,8%** ở `novel_premises`. Điều này không tự động làm benchmark sai, vì một số tactic không có premise được chú thích hoặc không còn nhãn trong corpus, nhưng phạm vi đánh giá phải được nói rõ.

**Đề xuất:** Tách hai hàng “theorem gốc” và “theorem có truy vấn được đánh giá”. Thêm sơ đồ số lượng qua từng bước: theorem gốc → tactic có premise → nhãn tìm thấy trong corpus → query còn nhãn. Báo cáo tỉ lệ giữ lại riêng theo train/val/test và hai split; tránh chỉ đưa tổng lượt bị loại gộp chung.

### 4.2. P1 — `novel_premises` sau lọc không còn bảo toàn hoàn toàn ý nghĩa ban đầu

**Vị trí:** Mục 3.3–3.4, 6.1 và 7.5.

Đối chiếu premise đúng trong `qrels.parquet` của test với **toàn bộ train cùng split**, không chỉ train A, thu được:

- 1.196 theorem test còn truy vấn hợp lệ.
- 1.093 theorem còn ít nhất một premise đúng chưa xuất hiện trong nhãn train.
- **103 theorem còn lại không có premise đúng unseen trong các truy vấn được giữ**, khoảng 8,6% số theorem được chấm.
- Có 9.735 cặp `(query, gold premise)` ở test, trong đó 2.506 cặp là unseen, khoảng 25,7%, tương ứng 1.933 premise unseen khác nhau.

Như vậy, Recall@10 tổng thể của split này vẫn bao gồm nhiều nhãn đã thấy. Không nên dùng riêng mức tăng từ 0,269 lên 0,280 để kết luận V5 truy hồi tốt hơn các premise mới. Các nguồn dựa trên lịch sử sử dụng có thể cải thiện phần seen trong cùng proof.

**Đề xuất:** Giữ kết quả benchmark tổng thể để so sánh, đồng thời bổ sung `Recall@10_unseen`, `Recall@50_unseen`, kết quả seen-only và số query/theorem có nhãn unseen. Với query không có nhãn unseen, loại khỏi trung bình unseen và ghi rõ mẫu số. Tách mất thuộc tính novel do lọc nhãn khỏi hiện tượng split vốn chỉ bảo đảm novel ở cấp proof, không phải ở từng tactic.

### 4.3. P1 — Kết luận lợi ích V5 trên novel phụ thuộc đơn vị lấy trung bình

**Vị trí:** Mục 5.5–5.6, Bảng 6.1–6.2.

Lấy trung bình theo query là lựa chọn hợp lệ nếu mục tiêu là chất lượng cho một bước tactic. Tuy nhiên, query trong cùng theorem có quan hệ với nhau. Dữ liệu thực tế có theorem chứa tới **46 query** ở `random` và **53 query** ở `novel_premises`; tương ứng 433 và 660 theorem có nhiều query.

Từ các tệp `perquery.parquet` mà bảng kết quả đang tham chiếu, lấy trung bình R@10 trong từng theorem, rồi lấy trung bình đều giữa các theorem, cho kết quả mô tả bổ sung:

| Split | Hệ thống | Query-macro R@10 trong báo cáo | Theorem-macro R@10 tính bổ sung |
|---|---|---:|---:|
| random | V4 | 0,243 | 0,3586 |
| random | V5 | 0,281 | 0,3931 |
| novel_premises | V4 | 0,269 | 0,3725 |
| novel_premises | V5 | 0,280 | 0,3585 |

**Trên novel, dấu của chênh lệch đổi từ dương sang âm khi mỗi theorem được tính trọng số bằng nhau.** Đây chưa phải kiểm định ý nghĩa thống kê và không phủ nhận metric query-macro; nó cho thấy mức tăng không đồng đều, có thể tập trung vào các proof nhiều bước.

Hàm `paired_bootstrap` trong `src/n3/eval/metrics.py` hiện lấy mẫu query độc lập. Khi nhiều bước thuộc cùng proof, cách này có thể đánh giá thấp độ bất định.

**Đề xuất:** Giữ query-macro làm primary metric nếu đã chốt, thêm theorem-macro làm kiểm tra độ bền và dùng **paired cluster bootstrap theo theorem**: lấy mẫu theorem có hoàn lại, mang theo các query của theorem đó và tính chênh lệch theo cùng estimand đã chọn. Phân tích thêm nhóm theorem ít/nhiều query. Không chỉ đổi tên bootstrap nếu chưa đổi đơn vị lấy mẫu.

### 4.4. P1 — So sánh với công bố ngoài đang dẫn tới suy luận quá mạnh

**Vị trí:** Mục 6.1, Bảng 6.3, trang 12, PDF 18.

Báo cáo đã ghi đúng rằng benchmark khác phiên bản. Tuy nhiên, hai câu sau vẫn vượt quá bằng chứng: dùng độ gần của metric để xác nhận pipeline đúng; và tính phần trăm “thu hẹp khoảng cách” tới ReProver từ các kết quả không cùng điều kiện.

Đối chiếu bản gốc xác nhận số BM25 nằm ở Table 1 cho Lean 3, còn số ReProver Lean 4 nằm ở Table B, Appendix D; phần Lean 4 sử dụng snapshot khác v10. Nên ghi rõ bảng nguồn và phiên bản cho từng dòng. [Nguồn: bài LeanDojo, bản arXiv v2](https://arxiv.org/pdf/2306.15626).

**Đề xuất:** Giữ bảng như bối cảnh tham khảo, bỏ diễn giải phần trăm thu hẹp khoảng cách và “bằng chứng độc lập cho tính đúng”. Xác nhận pipeline bằng kiểm thử công thức, qrels và thứ hạng trên cùng dữ liệu. Muốn so chất lượng với ReProver, cần chạy checkpoint phù hợp trên cùng snapshot, tập query, qrels, candidate universe và bộ lọc truy cập được.

### 4.5. P1 — “V5 không làm tăng P95” chưa được chứng minh

**Vị trí:** Tóm tắt, Mục 6.2 và kết luận; PDF 2, 19, 26.

Đợt đo V4/V5 cùng server cho P95 ở 10 client là **116,1 và 117,6 ms**, tức V5 tăng khoảng **1,3%** ở trung vị ba lần. Khoảng min–max lần lượt là 104,8–136,8 và 103,4–124,7 ms. Số này hỗ trợ nhận định “chênh lệch nhỏ trong phép đo”, chưa đủ để khẳng định không tăng hoặc tương đương về thống kê.

Ở 50 client, QPS giảm từ 131 xuống 108, khoảng **17,6%**, và P95 tăng từ 623,1 lên 727,0 ms, khoảng **16,7%**. Đánh đổi này nên hiện diện ngay trong tóm tắt kết quả V5.

**Đề xuất:** Đổi câu thành “P95 ở 10 client gần nhau trong ba lần đo; ở tải 50 client, V5 có chi phí rõ hơn”. Thêm bảng V4/V5 vào thân báo cáo. Nếu muốn khẳng định không thua kém, đặt trước biên chấp nhận được và thu thập đủ các lần đo xen kẽ để ước lượng khoảng tin cậy của chênh lệch. Không suy ra tính tương đương từ khoảng min–max chồng lấn.

### 4.6. P1 — Các phần cần người thực hiện chưa hoàn tất

**Vị trí:** Mục 3.5, 6.6, 7.3 và Phụ lục A.2; PDF 10, 22, 24, 28.

Các chỗ chờ điền còn hiển thị rõ trong PDF:

- Người kiểm tra 20 truy vấn ký xác nhận trong `docs/check_queries.md`.
- Bảng đối chiếu Nhóm 4 và xác nhận benchmark.
- Nhãn thủ công, tỉ lệ đồng thuận của hai người đánh giá 30 failure cases.
- Người chính cho đặc trưng/phục vụ và người dự phòng ở Bảng A.1.

Câu “hai thành viên gán nhãn độc lập rồi đối chiếu” đang được viết như việc đã hoàn thành trong khi kết quả còn chờ điền. Cần xác nhận trạng thái thực tế, không chỉ xóa chữ đỏ.

**Đề xuất:** Hoàn tất bằng người thật, lưu nhãn và bằng chứng, sau đó cập nhật câu mô tả. Với 30 mẫu, báo số mẫu và tỉ lệ đồng thuận thô; chỉ thêm Cohen's kappa khi quy tắc gán nhãn phù hợp. Nếu chưa có kết quả Nhóm 4, ghi rõ phạm vi chưa hoàn tất thay vì thay bằng số mô phỏng hoặc công bố ngoài.

## 5. Những cải thiện về phương pháp và diễn giải

### 5.1. P2 — Tách kiểm thử lỗi dữ liệu khỏi việc chọn phương pháp theo test

Mục 4.6 nói V5 được phát triển từ phân tích lỗi V4, còn Mục 7.3 trình bày lỗi trên test. Mục 7.4 cũng phát hiện lỗi accessibility trên test và chạy lại.

Sửa lỗi tự truy hồi theorem là cần thiết, nên giữ phần mô tả minh bạch này. Tuy nhiên, **nếu kiến trúc V5 được chọn sau khi quan sát lỗi test**, tập test đã tham gia vòng phát triển; tinh riêng số ứng viên trên validation không xóa được sự thích nghi đó.

Nên bổ sung nhật ký: tập nào dùng khám phá lỗi, thời điểm chốt giả thuyết và thời điểm chốt cấu hình. Nếu đã dùng test để thiết kế V5, công bố kết quả hiện tại là phân tích sau quan sát và xác nhận trên holdout mới. Đây là nguy cơ cần làm rõ, chưa phải kết luận rằng mọi kết quả bị rò rỉ nhãn.

### 5.2. P2 — Kết luận về namespace và dependency cần khớp ablation

Mục 6.1 và Chương 8 kết luận các trường/tín hiệu đều đóng góp có ý nghĩa. Trong khi đó, Mục 5.3 cho biết cấu hình BM25F tốt nhất theo primary metric đặt trọng số namespace bằng 0; Bảng 7.1 cho thấy bỏ namespace trong reranker chưa tạo khác biệt đo được. Namespace trong BM25F và trong reranker là hai can thiệp khác nhau, không thể dùng kết quả của cái này để khẳng định cái kia.

V3 → V4 đồng thời thêm accessibility và popularity/PageRank; chênh lệch của bước này không phải tác động riêng của PageRank. Ablation hiện tại mới tách cặp popularity/PageRank khỏi phần còn lại, chưa tách từng thành phần.

**Đề xuất:** Viết kết luận theo bằng chứng: BM25F nhiều trường và cấu trúc nói chung có lợi; accessibility có tác động mạnh; chưa xác định lợi ích độc lập của namespace; popularity và PageRank đang được đánh giá theo nhóm. Nếu chạy thêm, ưu tiên `name+statement` so với thêm namespace, và popularity-only so với PageRank-only trên cùng pool/cách huấn luyện.

Việc chọn V2 hơi thấp hơn điểm Recall@10 tốt nhất trên validation đã được công khai, nhưng cần quy tắc chọn cấu hình xác định trước. Các chỉ số phụ tốt hơn và mong muốn dùng đủ trường chưa đủ để tuyên bố namespace cần thiết.

### 5.3. P2 — Đối chứng Lucene không trùng hoàn toàn và chưa cô lập tokenizer

**Vị trí:** Mục 6.4, Bảng 6.5, trang 14, PDF 20.

Bảng ghi MRR Lucene = 0,066, B0 = 0,065; vì vậy câu “Recall@10, Recall@50 và MRR trùng đến chữ số thập phân thứ ba” không đúng với chính bảng. Mã `scripts/lucene_baseline.py` cũng lưu ý Lucene nén độ dài tài liệu và có thể lệch nhẹ điểm/thứ hạng.

Ngoài ra, Lucene mặc định dùng `k1=0,9; b=0,4`, còn cấu hình token B0 dùng `k1=1,2; b=0,75`. Chênh lệch Recall@10 giữa hai cấu hình chưa thể quy toàn bộ cho stopword/stemming vì đổi cả analyzer và tham số BM25.

**Đề xuất:** Dùng “các metric rất gần nhau” và thêm số query/top-k trùng nhau, sai khác điểm trên mẫu kiểm tra, quy tắc hòa điểm. Muốn đo tác động analyzer, giữ nguyên k1/b. Lợi thế tốc độ khoảng 5 lần hiện là trung bình một luồng ở cấu hình B0, không phải bằng chứng trực tiếp cho tốc độ BM25F hoặc P95 API sau khi tích hợp Lucene.

### 5.4. P2 — Độ phủ ứng viên chưa đủ để kết luận nút thắt đã chuyển hoàn toàn

**Vị trí:** Mục 7.3, trang 18–19, PDF 24–25.

V5 có pool recall 65,0% và R@10 28,1% cho thấy còn dư địa xếp hạng, nhưng vẫn thiếu khoảng 35% nhãn trong pool. Hơn nữa, pool recall không giới hạn k, còn R@10 bị giới hạn 10 kết quả; với query nhiều gold, ngay cả oracle cũng không đưa toàn bộ gold vào top 10.

Nên tính trần thực tế:

```text
OracleRecall@10(q) = min(10, |G_q ∩ C_q|) / |G_q|
Candidate loss(q)  = 1 - |G_q ∩ C_q| / |G_q|
Ranking gap(q)     = OracleRecall@10(q) - Recall@10(q)
```

Trong đó `G_q` là gold và `C_q` là pool ứng viên. Lấy trung bình theo cùng đơn vị như metric chính, đồng thời báo hạn chế do top-10. Tách kết quả theo nguồn ứng viên, seen/unseen và số gold. Trước khi có bảng này, nên viết “reranker trở thành một hướng cải thiện quan trọng” thay cho “nút thắt đã chuyển” như kết luận dứt khoát.

### 5.5. P2 — Làm rõ phạm vi “chỉ dùng thông tin có trước”

V5 giới hạn lịch sử cùng tệp/thư mục theo vị trí và import, là lựa chọn hợp lý. Nhưng `scripts/build_dependency_stats.py` tính popularity và PageRank từ toàn bộ train A; các thống kê toàn cục này không được xây lại theo mốc của từng query. Lọc một premise truy cập được khác với bảo đảm mọi bằng chứng dùng để chấm premise đó đều có trước.

Trong benchmark train/test tĩnh, cách làm này có thể chấp nhận được. Tuy nhiên, câu “chỉ dùng các định lý đã có trước” ở tóm tắt dễ khiến người đọc hiểu toàn bộ pipeline mô phỏng thời gian thực.

**Đề xuất:** Phân biệt rõ “không dùng nhãn val/test”, “premise trả về truy cập được”, và “thống kê tuân thủ thời gian”. Nếu giữ mô tả mô phỏng viết theorem mới, cần kiểm tra cả nguồn popularity/PageRank hoặc nêu đó là prior học từ snapshot train tĩnh.

### 5.6. P2 — Kiểm định và nhiều phép so sánh cần nhất quán

Báo cáo đã thảo luận Bonferroni cho ablation, đây là điểm tốt. Tuy nhiên, chuỗi cải tiến cũng có nhiều cặp và hai metric. Một số p-value yếu hơn ở novel, nên “mọi bước có ý nghĩa” cần ghi rõ mức, phía kiểm định, họ giả thuyết và có hiệu chỉnh hay chưa.

Hàm hiện tại lấy tỉ lệ bootstrap có delta không dương làm `p_value`. Nên mô tả đúng là xác suất đuôi bootstrap theo cách cài đặt, tránh coi việc viện dẫn sách bootstrap là đủ xác nhận mọi tính chất của kiểm định. Có thể bổ sung paired permutation test theo theorem hoặc phương pháp bootstrap dưới giả thuyết không, sau khi xác định đơn vị lấy mẫu.

**Đề xuất thực tế:** Ưu tiên effect size và CI; chốt một họ so sánh chính, áp dụng Holm hoặc một hiệu chỉnh đã chọn; tách metric phụ thành phân tích khám phá. Không in `p=0`: ghi độ phân giải Monte Carlo, hoặc giới hạn báo cáo phù hợp với 10.000 mẫu.

### 5.7. P2 — Giới hạn scalability đã nêu tốt, cần đặt sát phát biểu chính

Các mức 905K và 3,6 triệu được tạo bằng nhân bản corpus nên không mô phỏng đầy đủ tăng trưởng vocabulary, namespace và đa dạng nội dung. Spark chạy `local[n]` trên một máy chứng minh lợi ích song song cục bộ, chưa chứng minh mở rộng trên cụm.

Nên viết ngay trong tóm tắt/bảng chính: “tăng tốc 3,84 lần trên corpus nhân bản 20 lần, Spark local[8], Linux”. Giữ kết quả ở corpus thật 181K làm mốc thực tiễn và phân biệt với stress test.

Thí nghiệm 10K→181K chứa sẵn mọi gold của 500 query là một thiết kế kiểm soát distractor hợp lý; không phải mô hình ingestion tự nhiên. Cần gọi đúng mục tiêu của phép đo, vì thay corpus cũng đổi IDF và độ dài trung bình, không chỉ tăng số phần tử cạnh tranh.

### 5.8. P2 — Phân tích độ phức tạp cần khớp mã triển khai

Mục 4.4 mô tả chi phí theo tổng posting được đọc rồi nói không tỉ lệ với số tài liệu. Posting phổ biến vẫn có thể dài tuyến tính theo N. Ngoài ra, `score_terms` trong `src/n3/retrieval/search.py` dùng `np.unique` để gộp doc-id ở nhiều bước, nên chỉ đếm số posting chưa phản ánh đầy đủ chi phí sắp xếp/gộp. Mặt nạ accessibility còn đi qua mảng premise toàn corpus.

**Đề xuất:** Viết “chi phí phụ thuộc lượng posting chạm tới và thao tác gộp; thường tránh chấm mọi tài liệu riêng lẻ, nhưng trường hợp xấu vẫn tăng theo N”. Phân biệt mô hình lý tưởng dùng accumulator với cài đặt NumPy hiện tại. Giữ nhận định WAND/MaxScore là hướng tối ưu, chưa khẳng định mức tăng tốc cho hệ thống nhiều trường khi chưa đo.

## 6. Các lỗi nhất quán và tái lập cần chỉnh

| Vị trí | Vấn đề đã đối chiếu | Cách sửa |
|---|---|---|
| Mục 5.2, Bảng 5.2 | Văn bản ghi 7 biến thể nhưng liệt kê 8: B0, B0t, V1, V2, V2a, V3, V4, V5. | Cập nhật mô tả và số phép đánh giá tương ứng. |
| Bảng 5.4, dòng chất lượng | Ghi 7 biến thể, 21 lần trong khi pipeline hiện đánh giá 8 biến thể trên 3 tập. | Nếu đầy đủ theo pipeline hiện tại là 24 lần; phân biệt số mới thêm và số đã chạy thực tế bằng run manifest. |
| Mục 5.4 và Bảng 5.4, dòng tải | 3 hệ thống × 4 index × 3 tải = 36 cấu hình; lặp 3 lần thành 108 lần đo tải, mỗi lần 400 request. Tổng 43.200 đúng với 108×400, không phải 36×400. | Tách “cấu hình”, “lặp”, “lần chạy chương trình” và “request”. Nếu một lần gọi đo nhiều tải, ghi rõ cách đếm. |
| Bảng 5.3, caption | V4 validation ghi 0,274, nhưng bảng kết quả lưu hiện tại là 0,2734556, làm tròn ba chữ số thành 0,273. | Truy về đúng run dùng làm đối chứng và thống nhất làm tròn. |
| Bảng 5.3, hàng popular=50 | Ghi R@10 0,293, CSV là 0,2924524, làm tròn thành 0,292. | Sinh bảng từ CSV, không sửa số thủ công trong LaTeX. |
| Mục 6.3 | Một số số P95 như V4 full “96 ms” khác cách làm tròn 95,5 thành “95 ms” ở phần khác. | Chọn một độ chính xác và một quy tắc; ghi tên đợt đo vì V4 có cả mốc 95,5; 105; 116,1 ms. |
| Tóm tắt và Bảng 3.2 | 315.014 là tổng lượt query của hai split, không có nghĩa là 315.014 proof state khác nhau. | Ghi “lượt truy vấn cộng hai split” hoặc bổ sung số trạng thái/query duy nhất theo định nghĩa chuẩn hóa. |
| Kết luận “mọi bảng sinh bằng script” | `main.tex` chứa trực tiếp nhiều số của bảng 5.3, 6.1...; đã có sai khác với CSV. | Sinh các tệp `.tex` bảng bằng script rồi `\input`; giữ mapping bảng→run_id. |
| Phụ lục B, môi trường | Có version trong run record nhưng `pyproject.toml` chưa khai báo đầy đủ dependency; README cài nhiều gói không khóa version. | Thêm lockfile hoặc requirements khóa phiên bản cho môi trường chính/Spark và hướng dẫn Java/Anserini. |
| `scripts/reproduce.sh --with-tuning` | Chưa gọi grid BM25 mở rộng và `tune_v5.py`, dù báo cáo có dùng các bước chọn này. | Phân biệt tái đánh giá cấu hình đã chốt và tái tạo toàn bộ quá trình lựa chọn; bổ sung stage còn thiếu nếu cam kết tái lập toàn bộ. |
| Đầu ra `reproduce.sh` | Sinh hình PDF và DOCX, chưa gọi build LaTeX chính thức; README nói DOCX là nháp cũ. | Đưa `report/latex/build.sh` vào quy trình phát hành PDF hoặc ghi rõ bước riêng. |
| `git_commit=uncommitted` | Có code hash nhưng chưa chỉ tới revision checkout được. | Chốt commit/release, lưu source snapshot/hash và môi trường của từng đợt; không sửa hồi tố commit vào run cũ như thể đã chạy ở commit đó. |

Ngoài ra, nên thêm cột `run_id` hoặc một manifest cho từng bảng/hình. Script tổng hợp đang chọn lần chạy mới nhất; một run phát sinh sau này có thể làm bảng thay đổi dù tác giả chưa chủ ý cập nhật bản nộp.

## 7. Gợi ý cải thiện cách trình bày

### 7.1. Rút gọn tóm tắt, đưa V5 và giới hạn lên cùng một mạch

Tóm tắt hiện dày số liệu và trộn nhiều đợt thí nghiệm. Có thể gói trong khoảng 200–250 từ nếu không có mẫu riêng: bài toán → dữ liệu → phương pháp → kết quả chính → giới hạn. Chọn một kết quả chất lượng và một phép so chi phí được đo cùng điều kiện, tránh để người đọc ghép P95 V4 của đợt trước với V5 của đợt sau.

Mẫu diễn đạt có thể dùng sau khi chốt số liệu:

> Trên các truy vấn test hợp lệ của split random, hệ thống BM25F kết hợp tín hiệu cấu trúc đạt Recall@10 là 0,243 so với 0,100 của baseline BM25. Mở rộng ứng viên bằng lịch sử sử dụng của train nâng chỉ số này lên 0,281. Trong đợt đo V4/V5 cùng server ở 10 client, P95 lần lượt là 116,1 và 117,6 ms; tại 50 client, V5 giảm thông lượng từ 131 xuống 108 QPS. Kết quả được đo trên một máy; phép thử corpus lớn sử dụng dữ liệu nhân bản. Lợi ích đối với premise chưa thấy và chất lượng ở cấp theorem cần được phân tích riêng.

### 7.2. Cập nhật Hình 4.1 cho biến thể cuối cùng

Hình hiện giải thích V4: top-100 và 13 đặc trưng, trong khi đóng góp mới là V5. Thêm nhánh ứng viên từ tệp/thư mục/popularity, bước hợp nhất và loại trùng, chấm điểm 15 đặc trưng, rồi top-k. Chú thích rõ 100 BM25F + tối đa 250 bổ sung; số pool thực tế trung bình khoảng 239 trên test random.

### 7.3. Đưa V5 vào bảng đánh đổi chính

Hình 6.1 chỉ có B0/V2/V4, khiến kết quả cuối cùng không hiện diện trên đồ thị chính. Nếu thêm V5, phải đo lại các hệ thống trong cùng đợt và ghi rõ cùng tập query, trạng thái cache và tải. Nếu không đo lại, trình bày bảng V4/V5 riêng để không tạo so sánh chéo phiên.

Các hình ghép hai cột như 6.1–6.3 có nhãn khá nhỏ khi xem nguyên trang. Tăng cỡ chữ và giảm nhãn lặp; legend và nhãn trực tiếp đang cùng lặp tên B0/V2/V4. Chỉ giữ một cách nhận diện chính, đồng thời dùng kiểu nét/marker để đọc được khi in xám.

### 7.4. Dùng ví dụ xuyên suốt và một số bảng ngắn hơn

Một ví dụ proof state → token → ứng viên BM25F → sau lọc → sau rerank giúp người đọc hiểu tác dụng thật của từng bước. Nên chọn query validation hoặc ví dụ minh họa được ghi rõ, không lựa một trường hợp test đẹp để làm bằng chứng định lượng.

Phụ lục B có nhiều lệnh dài và trang cuối phần lớn để trống. Có thể chuyển lệnh dài thành code block có xuống dòng, rút run record xuống những trường cần giải thích và dẫn tới tệp JSON đầy đủ. Không nên thu nhỏ chữ chỉ để ép số trang.

## 8. Thí nghiệm bổ sung theo giá trị nhận được

| Thứ tự | Việc đề xuất | Lý do | Chi phí tương đối |
|---:|---|---|---|
| 1 | Tính theorem-macro, seen/unseen, cluster CI từ kết quả đã lưu. | Trực tiếp kiểm tra độ bền của kết luận V5; nhiều phần không cần chạy retriever lại. | Thấp. |
| 2 | Tạo data-flow trước/sau lọc và kiểm tra novelty. | Sửa phạm vi benchmark và mẫu số đánh giá. | Thấp. |
| 3 | Hoàn tất phân loại 30 failure cases bằng hai người. | Đáp ứng đầu ra đề bài và kiểm chứng diễn giải lỗi. | Cần thời gian thành viên. |
| 4 | V4 top-100, V4 top-200/250 và V5; cùng ngân sách ứng viên và cùng phiên đo tải. | Xác định lợi ích của nguồn cấu trúc so với chỉ mở rộng top-K BM25F. | Trung bình. |
| 5 | Oracle@10/50 và phân rã candidate loss/ranking gap. | Chọn đúng hướng cải thiện tiếp theo. | Thấp đến trung bình. |
| 6 | Nhóm 3, Nhóm 4 và RRF trên benchmark đã thống nhất. | Hoàn tất phần phối hợp của đề; kiểm tra nguồn kết quả có bổ sung nhau không. | Phụ thuộc dữ liệu Nhóm 4. |
| 7 | Ablation popularity-only/PageRank-only và name+statement/+namespace. | Cô lập thành phần có lợi trước khi tăng độ phức tạp. | Trung bình. |
| 8 | Tích hợp thử với Lean prover trên tập nhỏ, cùng budget tìm kiếm. | Kiểm tra chất lượng retrieval có chuyển thành proof success hay không. | Cao hơn; mở rộng, không bắt buộc nếu chưa tích hợp. |
| 9 | Lucene BM25F hoặc tối ưu posting, rồi mới thử cụm nhiều máy. | Giảm CPU phục vụ và đánh giá scalability thực tế. | Cao; phù hợp giai đoạn nghiên cứu tiếp theo. |

Với thời gian hạn chế, ba mục đầu và các chỉnh sửa P1 đem lại giá trị hơn việc thêm ngay một reranker phi tuyến. Không nên thay phương pháp rồi tiếp tục chọn theo cùng tập test đã xem nhiều lần.

## 9. Kế hoạch chỉnh sửa và tiêu chí hoàn thành

### Đợt 1 — Sửa tính chính xác, chưa cần chạy lại toàn bộ

- [ ] Sửa Bảng 3.3, thêm theorem gốc/theorem còn query và luồng lọc dữ liệu.
- [ ] Công bố 103 theorem không còn gold unseen và mẫu số unseen-only.
- [ ] Bổ sung theorem-macro và mô tả độ nhạy của V5 trên novel.
- [ ] Giảm mức khẳng định ở so sánh ReProver, P95, namespace và nút thắt reranker.
- [ ] Sửa MRR Lucene, số biến thể, cách đếm lượt chạy và các số làm tròn sai.
- [ ] Kiểm tra từng câu “đã thực hiện” với trạng thái kiểm tra/gán nhãn thực tế.

### Đợt 2 — Củng cố bằng chứng và đáp ứng nghiệm thu

- [ ] Tính CI theo theorem, chốt họ giả thuyết và cách hiệu chỉnh.
- [ ] Thêm seen/unseen, oracle và so sánh cùng ngân sách ứng viên.
- [ ] Hoàn tất nhãn thủ công, xác nhận 20 query và phân công chính/dự phòng.
- [ ] Chốt benchmark và bảng đối chiếu Nhóm 4; chỉ đưa RRF vào kết quả khi đã chạy thật.
- [ ] Xác nhận chất lượng trên holdout mới nếu V5 được thiết kế từ lỗi test.

### Đợt 3 — Đóng gói bản nộp

- [ ] Sinh bảng từ raw results, gắn run manifest cố định cho bản báo cáo.
- [ ] Khóa môi trường, chốt revision và chạy kiểm tra từ checkout sạch.
- [ ] Cập nhật Hình 4.1, bảng chi phí V5, abstract và kết luận theo cùng bộ số liệu.
- [ ] Biên dịch lại PDF; rà nội dung chờ điền, bảng/hình, lệnh tái lập và giới hạn số trang đã được lớp xác nhận.

## 10. Nguồn kiểm tra và cách tái kiểm tra các nhận xét

### 10.1. Nguồn trong dự án

| Nhận xét | Nguồn đã kiểm tra |
|---|---|
| Số query/theorem sau lọc, gold seen/unseen | `data/processed/queries.parquet`, `data/processed/qrels.parquet`. |
| Theorem-macro V4/V5 | `results/figures/quality_random_test_all.csv`, `quality_novel_premises_test_all.csv`, các tệp `perquery.parquet` theo `run_id` trong đó; nối `query_id` với bảng query. |
| Bảng validation và số làm tròn | `results/figures/quality_random_val_all.csv`, `results/raw/tuning/V5__extra__random_val_all.csv`. |
| P95/QPS cùng server | Phần V4/V5 trong `results/figures/scale_tables.md`. |
| Chênh lệch Lucene | `results/figures/lucene.md`, `scripts/lucene_baseline.py`. |
| Bootstrap và cách tổng hợp | `src/n3/eval/metrics.py`, `scripts/summarize_quality.py`, `src/n3/eval/run_eval.py`. |
| Đặc trưng và thống kê sử dụng | `src/n3/retrieval/features.py`, `rerank.py`, `scripts/build_dependency_stats.py`, `train_reranker.py`, `tune_v5.py`. |
| Quá trình tái lập và biên dịch | `README.md`, `pyproject.toml`, `scripts/reproduce.sh`, `report/latex/build.sh`, `report/latex/main.tex`. |

Các số bổ sung là kiểm tra mô tả trên snapshot hiện tại, không phải kết quả kiểm định mới. Để tái kiểm tra, dùng quy tắc sau:

```python
# Chạy từ gốc dự án với môi trường có pandas và pyarrow.
import pandas as pd
import pyarrow.parquet as pq

q = pq.read_table('data/processed/queries.parquet').to_pandas()
r = pq.read_table('data/processed/qrels.parquet').to_pandas()
keys = ['file_path', 'theorem_full_name']

# Số theorem có query hợp lệ.
for strategy in ['random', 'novel_premises']:
    for split in ['train', 'val', 'test']:
        x = q[(q.split_strategy == strategy) & (q.split == split)]
        print(strategy, split, len(x), len(x.drop_duplicates(keys)))

# Novelty được tính so với toàn bộ train của cùng split.
n = q[q.split_strategy == 'novel_premises']
seen = set(r[r.query_id.isin(n[n.split == 'train'].query_id)].premise_id)
test = n[n.split == 'test']
gold = r[r.query_id.isin(test.query_id)].merge(test[['query_id'] + keys], on='query_id')
gold['unseen'] = ~gold.premise_id.isin(seen)
novel = gold.groupby(keys).unseen.any()
print('theorem có/không còn gold unseen:', novel.sum(), (~novel).sum())

# Theorem-macro theo các run đang được bảng chất lượng tham chiếu.
for strategy in ['random', 'novel_premises']:
    runs = pd.read_csv(f'results/figures/quality_{strategy}_test_all.csv').set_index('name')
    for system in ['V4', 'V5']:
        run_id = runs.loc[system, 'run_id']
        m = pq.read_table(f'results/raw/eval/{run_id}.perquery.parquet').to_pandas()
        m = m.merge(q[['query_id'] + keys], on='query_id', validate='one_to_one')
        print(strategy, system, m.groupby(keys)['R@10'].mean().mean())
```

### 10.2. Nguồn ngoài đã đối chiếu

[LeanDojo: Theorem Proving with Retrieval-Augmented Language Models, arXiv v2](https://arxiv.org/pdf/2306.15626): dùng để xác minh nguồn các dòng công bố trong Bảng 6.3, gồm Table 1 và Table B của Appendix D. Không dùng số liệu từ website tổng hợp để chấm mức vượt trội của hệ thống.

**Tiêu chí quan trọng cho bản tiếp theo:** Người đọc phải phân biệt được kết quả nào đã đo, kết quả nào chỉ tham khảo, dữ liệu nào thực sự được chấm và kết luận nào còn là giả thuyết. Với phần kỹ thuật hiện có, làm rõ bốn điểm này sẽ tăng độ thuyết phục đáng kể.
