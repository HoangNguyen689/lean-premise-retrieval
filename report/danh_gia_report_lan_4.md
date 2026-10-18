# Đánh giá báo cáo lần 4

**Ngày đánh giá:** 19/10/2026. **Bản được xem:** `report.pdf`, cập nhật lúc 00:43:34 ngày 19/10/2026, 34 trang PDF; phần Chương 1–8 dài 20 trang.

**Nguồn:** [báo cáo hiện tại](D:/bigdata/nhom3-lean-retrieval/report/report.pdf), [nhận xét lần 3](D:/bigdata/nhom3-lean-retrieval/report/danh_gia_report_lan_3.md), mã LaTeX và các tệp nguồn bảng/hình trong repository.

**SHA-256 của PDF:** `bef59a2c143404c7b7f901e650637b5ff6738415255443f881b0a5d2e97fcad9`.

Đã đọc bản mới và xem ảnh render của toàn bộ 34 trang, đối chiếu các góp ý về layout, văn phong, thuật ngữ và tính tái lập. Đã chạy `scripts/verify_report_inputs.py`: **795 mục đầu vào trong hai manifest được kiểm tra, không có mục thiếu hoặc lệch hash**. Đây là số mục được script kiểm tra, không khẳng định có 795 tệp duy nhất. Lần này không chạy lại toàn bộ thí nghiệm hay bộ kiểm thử thống kê đã chạy ở lần 3.

Trong nhận xét dưới đây, “trang PDF” tính từ trang bìa; “trang in” là số trang hiển thị trên báo cáo.

## 1. Nhận định chung

**Bản sửa này đã xử lý tốt phần lớn góp ý về bố cục và cách dùng thuật ngữ. Layout tổng thể hiện hợp lý; không cần tổ chức lại các chương hoặc đổi phong cách trình bày.** Mạch đọc từ bài toán, phương pháp, thực nghiệm tới thảo luận và giới hạn đã rõ hơn. Hình/bảng chính cũng nằm gần phần nội dung liên quan hơn trước.

Văn phong đã tự nhiên hơn. Việc giữ các thuật ngữ như *premise retrieval*, *tokenizer*, *reranker*, *candidate*, *holdout*, *seen/unseen* là phù hợp với chủ đề. Các khái niệm phổ biến như “đặc trưng”, “độ trễ”, “chỉ mục” vẫn dùng tiếng Việt được. **Không nên tiếp tục thay hàng loạt thuật ngữ chỉ để tăng mức Việt hóa hoặc mức dùng tiếng Anh.** Bản hiện tại cần sửa một số câu cụ thể, không cần viết lại toàn bộ.

Về nội dung khoa học, cách trình bày vẫn giữ được những giới hạn quan trọng: test đã ảnh hưởng tới thiết kế, holdout là xác nhận nội bộ, V5 có đánh đổi trên unseen premise và kết quả dưới tải còn chưa ổn định. Chưa thấy lý do từ bản sửa này để yêu cầu thêm một vòng phát triển thuật toán. Công việc còn lại là biên tập cuối và hoàn tất các phần nghiệm thu mà báo cáo đang ghi rõ là chưa xong.

## 2. Các góp ý lần 3 đã được xử lý

| Vấn đề trước | Bản hiện tại | Đánh giá |
|---|---|---|
| Hình kiến trúc ngắt phần giải thích worker | Hình 6.2 đã được giữ trước Mục 6.5. | Mạch đọc tốt hơn, không còn lỗi chen hình như trước. |
| Bảng 7.2 trôi sang phần thảo luận kế tiếp | Bảng nằm trong Mục 7.1, trước Mục 7.2. | Đã sửa đúng vị trí. |
| Ngắt trang làm tách cụm mở đầu “Trên novel” | Đoạn hiện bắt đầu gọn ở trang sau. | Đã cải thiện. |
| Caption dài và dày thông tin | Caption ngắn hơn, phần giải thích được đưa xuống ghi chú hoặc nội dung. | Dễ quét và dễ đối chiếu hơn. |
| Danh mục hình kéo dài thêm một trang ít nội dung | Danh mục hình và bảng đã gộp trên trang PDF 5. | Hợp lý với số hình/bảng của báo cáo này. |
| Tài liệu tham khảo có trang cuối rất ít mục | Toàn bộ 23 tài liệu nằm trên một trang riêng. | Gọn hơn; cỡ chữ vẫn đọc được. |
| Phụ lục bảng bị chia nhóm chưa rõ | Phụ lục C chia theo dữ liệu/môi trường, retrieval/serving/build và thiết kế. | Dễ tra cứu hơn. |
| Thuật ngữ bị dịch gượng hoặc chưa nhất quán | Có định nghĩa lần đầu; dùng premise retrieval, sparse/dense, tokenizer, gold, seen/unseen rõ hơn. | Đã đi đúng hướng. |
| Hình chưa được đóng băng nguồn như bảng | Có manifest hình, đọc bản ghi đã chọn và kiểm tra hash trước khi dựng lại. | Điểm thiếu chính của lần 3 đã được xử lý. |
| Còn cách gọi p-value gây nhầm với bootstrap | Phần mô tả đã phân biệt CI bootstrap và kiểm định hoán vị. | Giữ được sự nhất quán với phương pháp đã sửa. |

Không nên tiếp tục liệt kê những vấn đề trên như lỗi đang tồn tại. Các nhận xét còn hiệu lực nằm ở những mục sau.

## 3. Layout: còn một lỗi rõ và vài điểm nhỏ

### 3.1. Cần giữ nguyên khối JSON ở Phụ lục B.2

**Vị trí:** trang PDF 28–29, tương ứng trang in 23–24; phần “Ví dụ một bản ghi lần chạy”.

Khối JSON bắt đầu cuối trang 28 rồi chỉ còn hai dòng trên trang 29. Phần lớn trang 29 bị bỏ trống. Đây là lỗi dàn trang dễ thấy nhất còn lại: một ví dụ ngắn bị chia làm hai khung và tạo ra một trang gần như rỗng.

**Cách sửa đề xuất:** giữ cả khối JSON trong một `minipage` để LaTeX chuyển nguyên khối sang trang sau khi không đủ chỗ. Trước tiêu đề hoặc đoạn giới thiệu có thể dùng `\Needspace` với chiều cao đủ cho tiêu đề, phần dẫn và ví dụ. Nếu vẫn thiếu chỗ, rút gọn phần dẫn hoặc giảm nhẹ khoảng cách dọc ở B.1; không cần giảm cỡ chữ của toàn báo cáo.

Ví dụ về nguyên tắc bố trí, cần điều chỉnh chiều cao theo kết quả biên dịch thực tế:

```latex
% Nếu đã nạp gói needspace:
\Needspace{12\baselineskip}
\section{Ví dụ một bản ghi lần chạy}
% Đoạn giới thiệu ngắn.
\noindent\begin{minipage}{\linewidth}
\begin{Verbatim}[fontsize=\footnotesize,frame=single,framesep=2mm]
...
\end{Verbatim}
\end{minipage}
```

Không cần ép riêng hai dòng cuối lên bằng khoảng cách âm. Sau khi sửa phải xem lại cả hai trang để bảo đảm khối ví dụ và khung không bị cắt.

### 3.2. Có thể gom một số đoạn ngắn qua trang

- Cuối Mục 7.1, đoạn kết bị tách giữa trang PDF 21 và 22; trang sau chỉ còn vài dòng trước Mục 7.2. Có thể chuyển nguyên đoạn ngắn sang trang sau nếu cân đối hơn.
- Đoạn nói về gán nhãn thủ công các trường hợp lỗi cũng chạy từ trang PDF 23 sang 24. Nếu chỉnh được bằng `\Needspace` trước cả đoạn thì trang sẽ gọn hơn.

Đây là các điểm hoàn thiện nhỏ. Không nên thêm hàng loạt `\newpage` hoặc đặt mọi hình/bảng thành `[H]`, vì có thể tạo thêm khoảng trắng ở các trang khác. Các trang phụ lục có ít bảng cũng không mặc nhiên là lỗi nếu nhóm nội dung rõ và bảng dễ đọc.

### 3.3. Những phần nên giữ

Giữ bố cục chương hiện tại, danh mục hình/bảng đã gộp, caption ngắn và cách đặt ghi chú dưới bảng. Phần nội dung 20 trang đang đủ chỗ để trình bày phương pháp và giới hạn; không cần cố rút thêm chỉ để giảm tổng số trang PDF.

## 4. Thuật ngữ và văn phong: sửa có chọn lọc

### 4.1. Sửa lỗi “Train train A” trong Hình 4.1

**Vị trí:** trang PDF 10, trang in 5; nút bên phải của sơ đồ kiến trúc. Trong `report/latex/main.tex`, nút `dep` đang chứa “Train train A”.

Có thể đổi thành:

> Thống kê từ train A: popularity, PageRank (tĩnh); số lần dùng theo tệp/thư mục từ các theorem có trước.

Nếu nút quá chật, viết ngắn hơn trong hình và giữ điều kiện chi tiết ở đoạn giải thích phía dưới. Đây là sửa cục bộ, không cần thay mọi lần xuất hiện của “train A”.

### 4.2. Mô tả ReProver cần chính xác hơn

**Vị trí:** Chương 2, trang PDF 7, trang in 2. Câu hiện tại gọi ReProver là “một dense retriever”. ReProver là hệ thống chứng minh kết hợp mô hình ngôn ngữ và retrieval; dense retriever là một thành phần của hệ thống. Phân biệt này được nêu trong [bài LeanDojo gốc của Yang và cộng sự](https://arxiv.org/abs/2306.15626).

Gợi ý sửa:

> Công trình giới thiệu LeanDojo Benchmark với hai split `random` và `novel_premises`, đồng thời đề xuất ReProver, một hệ thống chứng minh kết hợp mô hình sinh tactic với dense retriever. Thành phần retrieval chỉ tìm trong các premise có thể dùng tại vị trí chứng minh.

Hoặc, nếu đoạn chỉ cần bàn về retrieval, dùng trực tiếp “dense retriever của ReProver”. Đây là chỉnh độ chính xác của phần tổng quan, không làm thay đổi kết quả của nhóm.

### 4.3. Định nghĩa accessible premise trong tóm tắt còn hơi hẹp

Tóm tắt hiện giải thích theo “quan hệ import”, trong khi Mục 4.5 còn xét premise cùng tệp và thứ tự khai báo. Nên tránh để định nghĩa ngắn đầu bài khiến người đọc hiểu thiếu trường hợp cùng tệp.

Gợi ý ngắn, tự nhiên:

> Bộ lọc chỉ giữ accessible premise, tức premise có thể dùng tại vị trí chứng minh hiện tại.

Sau đó để Mục 4.5 giải thích điều kiện import và thứ tự khai báo. Không cần nhồi toàn bộ quy tắc vào tóm tắt.

### 4.4. Một vài cách diễn đạt nên làm mềm lại

| Vị trí/cách viết hiện tại | Gợi ý | Lý do |
|---|---|---|
| Mục 5.2: “Tinh tham số và huấn luyện” | “Tinh chỉnh tham số và huấn luyện” | “Tinh chỉnh” tự nhiên và quen thuộc hơn trong văn viết kỹ thuật. |
| Chương 8: “Tinh tham số, trường name…” | “Việc tinh chỉnh tham số, sử dụng trường name…” | Làm rõ các thao tác đang được liệt kê. |
| Chương 2: “đặc trưng cấu trúc rẻ” | “đặc trưng cấu trúc có chi phí tính toán thấp” | Tránh sắc thái khẩu ngữ và nói rõ “rẻ” theo nghĩa nào. |

Các từ *candidate*, *gold premise*, *reranker*, *holdout* không cần dịch thêm. Giữ tên trường `name`, `namespace`, `statement` và tên đặc trưng trong mã khi đang nói đúng các thành phần đó. Với thuật ngữ dùng lần đầu, giải thích ngắn bằng tiếng Việt rồi dùng nhất quán về sau là đủ.

## 5. Nội dung khoa học và tính tái lập

### 5.1. Các kết luận chính vẫn được đặt đúng giới hạn

So với lần 3, bản sửa chủ yếu là biên tập và cơ chế dựng báo cáo. Các kết quả quan trọng vẫn được trình bày thận trọng:

- Không diễn giải mọi bước tăng điểm là đều có ý nghĩa thống kê; bước tokenizer và mức tăng V4 → V5 trên novel vẫn có giới hạn bằng chứng.
- Giữ sự khác biệt giữa query-macro và theorem-macro; mức tăng tổng thể của V5 không được dùng để che mức giảm trên unseen premise.
- Không gọi holdout nội bộ là đánh giá độc lập trên benchmark bên ngoài.
- Thừa nhận thay đổi candidate pool và thêm đặc trưng usage diễn ra cùng nhau, nên chưa tách được tác động riêng của từng yếu tố.
- Phần tải đồng thời vẫn nêu timeout và biến động QPS, không kết luận V5 hoàn toàn ổn định dưới tải.

Nên giữ các giới hạn này kể cả khi rút ngắn bài. Chúng giúp kết luận đáng tin hơn. Lần đánh giá này không có thêm thí nghiệm để nâng mức khẳng định về hiệu quả hoặc khả năng phục vụ của hệ thống.

### 5.2. Nguồn hình và bảng đã được kiểm soát tốt hơn

Đã kiểm tra mã và chạy script xác minh. Bản hiện tại có cả `tables/SOURCES.md` và `figures/SOURCES.md`; chế độ sinh hình cho báo cáo sử dụng các bản ghi đã chọn trong `report_records.json`. Quy trình build mặc định kiểm tra hash trước khi sinh lại bảng/hình, có phân biệt `--compile-only` và cập nhật có chủ ý bằng `--update`.

Kết quả kiểm tra thực tế: **795 mục khớp, 0 mục thiếu hoặc lệch; script kết thúc thành công.** Góp ý còn dang dở về nguồn hình ở lần 3 có thể đóng lại trong phạm vi kiểm tra này.

Kiểm tra hash xác nhận các đầu vào đang khớp với manifest. Nó chưa thay thế việc chạy lại toàn bộ thí nghiệm hoặc chứng minh mọi môi trường đều dựng được báo cáo giống hệt nhau; lần này không thực hiện các kiểm tra rộng đó.

## 6. Những phần nhóm vẫn cần hoàn tất trước khi nộp

| Việc còn mở | Vị trí trong bản PDF | Cách hoàn tất |
|---|---|---|
| Kiểm tra và ký xác nhận 20 query | Trang PDF 9, trang in 4 | Thực hiện đối chiếu, ghi người kiểm tra và kết quả trong tệp được dẫn; sau đó sửa câu “chưa được thực hiện”. |
| So sánh với Nhóm 4 | Trang PDF 16, trang in 11 | Nhận kết quả thật và chốt đặc tả so sánh; nếu chưa có thì giữ trạng thái chưa hoàn tất, không suy diễn thành kết quả. |
| Gán nhãn thủ công 30 trường hợp lỗi | Trang PDF 23–24, trang in 18–19 | Hoàn tất nhãn, quy tắc phân loại và xác nhận; hoặc trình bày rõ đây là công việc chưa thực hiện. |
| Chốt phân công và khai báo công cụ AI | Phụ lục A, trang PDF 27, trang in 22 | Điền người phụ trách chính, xác nhận nội dung thực tế và bỏ các ghi chú chờ chốt sau khi đã xác nhận. |

Phụ lục A hiện nói Codex dùng cho “ba bản phản biện”. Sau lần này đã có thêm file nhận xét lần 4, nên nhóm cần cập nhật phạm vi khai báo cho đúng thực tế nếu sử dụng nhận xét này. Có thể ghi “hỗ trợ phản biện các bản thảo và góp ý biên tập”, kèm phạm vi cụ thể đã dùng. Không tự xác nhận thay thành viên nhóm.

Các bản ghi thí nghiệm có `git_commit = uncommitted` vẫn là giới hạn truy vết lịch sử đã được thừa nhận. Khi chốt bản nộp, nên lưu commit của bản cuối và hướng dẫn dựng lại; không sửa ngược các bản ghi cũ thành commit mới vì sẽ làm sai xuất xứ của lần chạy.

## 7. Thứ tự sửa đề xuất

1. **Hoàn tất các mục cần người thật xác nhận:** query, phân loại lỗi, phân công và phạm vi công cụ AI; xử lý tình trạng so sánh Nhóm 4 theo dữ liệu thực tế.
2. **Sửa khối JSON ở B.2:** giữ nguyên khối trên một trang, xem lại hai trang liền kề sau khi biên dịch.
3. **Sửa các điểm ngôn ngữ cụ thể:** “Train train A”, cách mô tả ReProver, định nghĩa ngắn accessible premise, “tinh chỉnh tham số” và “chi phí tính toán thấp”.
4. **Rà lần cuối PDF sau biên dịch:** kiểm tra ngắt đoạn ở Mục 7.1, các ghi chú chờ chốt, số trang, tham chiếu hình/bảng và phụ lục. Chỉ chỉnh khoảng cách khi có lỗi nhìn thấy.

**Bản hiện tại đã có bố cục phù hợp và cách dùng thuật ngữ tương đối tự nhiên.** Không cần một vòng thay thuật ngữ hoặc dàn trang diện rộng nữa. Sau khi xử lý khối JSON, vài câu nêu trên và các mục xác nhận còn mở, báo cáo sẽ ở trạng thái hoàn thiện hơn để chốt bản nộp.
