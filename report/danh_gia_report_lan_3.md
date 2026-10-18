# Đánh giá báo cáo lần 3

**Ngày đánh giá:** 19/10/2026. **Bản PDF được xem:** cập nhật lúc 00:15:59 ngày 19/10/2026, 34 trang PDF; Chương 1–8 vẫn chiếm 20 trang.

**Nguồn chính:** [report.pdf](D:/bigdata/nhom3-lean-retrieval/report/report.pdf), [đánh giá lần 2](D:/bigdata/nhom3-lean-retrieval/report/danh_gia_report_lan_2.md), mã thống kê, các bảng kết quả và manifest hiện tại.

**SHA-256 của PDF:** `6cbdc7b85b94c17a665d18cdc847869f6725e70bb0b932a493a59421d7225bce`.

Đã đọc báo cáo mới, xem ảnh render của cả 34 trang, chạy kiểm thử metric/thống kê và kiểm tra chọn lọc từ kết quả thô. Không chạy lại toàn bộ retrieval, Spark hoặc cài môi trường từ đầu. Đường dẫn tương đối dưới đây tính từ `D:/bigdata/nhom3-lean-retrieval/`; số trang in trên báo cáo được phân biệt với số trang PDF.

## 1. Nhận định hiện tại

**Phần phương pháp và kết luận đã vững hơn đáng kể. Lỗi thống kê lớn của lần trước đã được xử lý đúng hướng và vượt qua các kiểm tra đã chạy.** Bản này không còn cần một vòng phát triển thuật toán mới; nên chuyển trọng tâm sang hoàn tất nghiệm thu và biên tập cuối.

Về chất lượng nội dung khoa học của bản thảo, mức tham khảo hiện tại là **khoảng 9/10**. Đây không phải điểm nghiệm thu chính thức: báo cáo vẫn còn chỗ chờ xác nhận, công việc thủ công chưa thực hiện và so sánh Nhóm 4 chưa hoàn tất.

**Không tiếp tục tính lỗi p-value cũ là vấn đề còn tồn tại.** Trong phạm vi kiểm tra lần này, chưa phát hiện lỗi nghiêm trọng mới của cách tính kiểm định. Những điểm còn cần sửa được phân biệt dưới đây thành việc nghiệm thu, tính tái lập và biên tập.

## 2. Các góp ý lần hai đã được xử lý

| Góp ý trước | Bản hiện tại | Nhận xét |
|---|---|---|
| Hai hệ thống giống nhau nhưng p hai phía bằng 0 | Tách CI bootstrap khỏi p của kiểm định hoán vị; hệ thống giống nhau cho p = 1. | **Đã sửa, đã chạy kiểm tra.** |
| Chưa có H0 rõ ràng | Mục 5.5 nêu hoán đổi nhãn hai hệ thống trong toàn bộ query của từng theorem; Mục 7.5 nêu giả định. | **Đã làm rõ.** |
| p Monte Carlo có thể bằng 0 | Dùng `(1 + số lần cực trị)/(1 + số phép hoán vị)`; bảng ghi độ phân giải. | **Đã sửa.** |
| Kết luận “mọi bước đều có ý nghĩa” quá mạnh | Bảng 6.2 và phần trả lời RQ1 đã thừa nhận bước tokenizer chưa có ý nghĩa sau hiệu chỉnh. | **Đã sửa theo kết quả mới.** |
| V4-K240 không bằng chính xác ngân sách V5 | Ghi xấp xỉ trên random/holdout, nhiều hơn V5 trên novel. | **Đã sửa.** |
| Chưa tách nguồn ứng viên khỏi hai đặc trưng usage | Mục 6.2 gọi đúng là tác dụng gộp; không còn diễn giải như tác động nhân quả độc lập. | **Đã sửa.** |
| Holdout dễ bị hiểu như benchmark bên ngoài | Nêu rõ là phần train B giữ riêng, cùng snapshot, có thiên lệch độ dài proof và đã được sử dụng. | **Đã sửa.** |
| Thiếu nhật ký dùng test/holdout | Có `docs/process_log.md`, đồng thời thừa nhận nhật ký không chứng minh lịch sử chưa từng xem dữ liệu. | **Đã bổ sung hợp lý.** |
| Timeout bị che bởi QPS trung vị | Bảng 6.5 có QPS min–max, số lỗi; giải thích latency chỉ tính request thành công. | **Đã sửa tốt.** |
| Abstract không rõ số unseen thuộc tập nào | Ghi rõ mức giảm 0,444 → 0,359 thuộc test novel_premises. | **Đã sửa.** |
| Phạm vi các đối chứng bị ghi sai | Mục 7.5 phân biệt đúng đối chứng nào chỉ có random, đối chứng nào có cả novel/holdout. | **Đã sửa.** |
| Dựng lại báo cáo và cập nhật run bị lẫn | Phụ lục B tách hai mục đích, có thêm `report_records.json` và SHA-256 nguồn bảng. | **Bảng đã được cải thiện; hình còn điểm cần hoàn thiện ở Mục 5.** |
| Khai báo công cụ phản biện chưa đủ | Phụ lục A đã bổ sung vai trò của Codex và phân biệt với Claude Code. | **Đã bổ sung; phần xác nhận cuối vẫn chờ nhóm chốt.** |

## 3. Bằng chứng kiểm tra phần thống kê

### 3.1. Các kiểm tra đã thực sự chạy

| Kiểm tra | Kết quả |
|---|---|
| `python -m pytest tests/test_metrics.py -q` | **12 passed**, gồm các test hệ thống giống nhau, ties, đối xứng, ví dụ tính tay, Monte Carlo so với vét cạn và trọng số cụm. |
| Đối chiếu với cài đặt tham chiếu độc lập dùng `itertools.product` | **40/40 trường hợp khớp**, với cụm có 1, 2, 3, 4 query, cả query-macro và theorem-macro. |
| Ví dụ đã phát hiện lỗi ở lần trước: `a=b=[0,0]` | Hàm mới trả **delta = 0, p = 1**. |
| Tính lại B0t → V1, test random, Recall@10 | p = **0,05269473**, khớp CSV; p Holm cũng bằng giá trị này. |
| Tính lại V4 → V5, test novel, Recall@10 | p chưa hiệu chỉnh = **0,07419258**; p Holm = **0,09399060**, khớp CSV và cách làm tròn trong báo cáo. |
| Kiểm tra SHA-256 trong `report/latex/tables/SOURCES.md` | **399 mục khớp, không có tệp thiếu hoặc lệch hash** tại thời điểm đánh giá. |

Không diễn giải 12 test đã chạy ở đây thành xác nhận toàn bộ 58 test được báo cáo. Cũng không diễn giải 399 hash khớp thành chứng minh tất cả phương pháp đều đúng; kiểm tra đó xác nhận tính nhất quán của các tệp đầu vào được liệt kê.

### 3.2. Cách trình bày kết luận mới là phù hợp

- Trên random, B0t → V1 có chênh lệch Recall@10 dương nhưng p Holm khoảng 0,0527; việc không tuyên bố có ý nghĩa ở mức 0,05 là đúng với kiểm định đã chọn.
- Trên novel, V4 → V5 có p Holm khoảng 0,094; không nên dùng mức tăng điểm ước lượng để tuyên bố V5 cải thiện có ý nghĩa.
- CI bootstrap và p hoán vị dùng hai quy trình khác nhau, nên có thể xuất hiện CI sát 0 hoặc không chứa 0 nhưng p sau hiệu chỉnh lớn hơn 0,05. Điều này không tự động là lỗi tính toán.
- Các cận gần 0 được in thêm chữ số giúp người đọc thấy đúng dấu; đây là sửa đổi tốt.

Nguồn đã đối chiếu: `src/n3/eval/metrics.py`, `tests/test_metrics.py`, `scripts/robustness.py`, `scripts/ablation_significance.py`, `results/figures/robustness/significance_cluster.csv`, cùng tệp per-query mà manifest tham chiếu.

## 4. Việc còn ảnh hưởng nghiệm thu — chưa được giải quyết bằng sửa câu chữ

| Việc cần hoàn thành | Vị trí trong bản hiện tại | Yêu cầu thực tế |
|---|---|---|
| Kiểm tra thủ công 20 query | Mục 3.4, trang 4, PDF 10. | Thành viên đối chiếu, ghi tên/ngày và kết quả kiểm tra. |
| Hai người gán nhãn 30 failure cases | Mục 7.3, trang 18, PDF 24. | Lưu nhãn độc lập, quy tắc gán và kết quả đối chiếu; báo mẫu số của tỉ lệ đồng thuận. |
| So sánh thật với Nhóm 4 | Mục 6.1, trang 11, PDF 17. | Chốt benchmark chung và nhận/chạy kết quả thật theo yêu cầu học phần. |
| Chốt người chính/dự phòng | Phụ lục A.2, trang 23, PDF 29. | Thay các ô “A hoặc B” bằng tên được nhóm thống nhất; gắn minh chứng đóng góp. |
| Xác nhận khai báo AI | Phụ lục A.1, trang 23, PDF 29. | Kiểm tra đúng lịch sử sử dụng thực tế, rồi bỏ chú thích chờ xác nhận. Nếu dùng cả phản biện lần ba thì cập nhật phạm vi tương ứng. |
| Có revision lấy về được | Mục 7.5 và Phụ lục B. | Chốt commit/release của bản nộp; giữ nguyên provenance của run cũ, không sửa hồi tố thành commit mới. |

Bản hiện tại đã ghi trung thực rằng các việc này chưa hoàn tất. Điểm cần cải thiện bây giờ là thực hiện, không phải viết thêm một đoạn limitation. Nếu nộp bản cuối ngay, các ô màu đỏ và kết quả phối hợp còn thiếu vẫn là điểm trừ dễ nhận thấy.

## 5. P2 — Quy trình “dựng lại đúng bản đã phát hành” còn chưa ghim nguồn của hình

**Vị trí:** Phụ lục B.1, trang 24, PDF 30; `report/latex/build.sh`; [make_figures.py, dòng 62](D:/bigdata/nhom3-lean-retrieval/scripts/make_figures.py:62).

Phần bảng hiện đọc run đã ghim từ `report_manifest.json` và `report_records.json`. Tuy nhiên, `build.sh` còn gọi `scripts/make_figures.py --report`, trong khi hàm `load(kind)` của script hình vẫn đọc toàn bộ `results/raw/<kind>/*.json`, không đọc danh sách đã ghim.

Vì vậy, nếu bổ sung một raw run phù hợp với bộ lọc của hình sau khi phát hành, chạy lại lệnh build có thể làm hình thay đổi trong khi bảng vẫn dùng run cũ. **Chưa có bằng chứng rằng hình trong PDF hiện tại đang sai**; đây là điểm chưa bảo đảm của cam kết dựng lại bản phát hành.

Đề xuất nhỏ, không cần chạy lại thí nghiệm:

1. Khi dùng `--report`, cho script hình đọc cùng manifest run như script bảng, bao gồm các nguồn chất lượng mà hình dùng.
2. Hoặc giữ nguyên các PDF hình đã phát hành và tách lệnh “chỉ biên dịch LaTeX” khỏi lệnh “sinh lại hình/bảng”.
3. Nếu muốn phát hiện đầu vào thay đổi, so hash với manifest kỳ vọng trước khi dựng; việc tính lại hash rồi ghi đè `SOURCES.md` chỉ ghi nhận trạng thái mới, chưa phải cơ chế từ chối dữ liệu lệch bản phát hành.

399 hash hiện khớp cho thấy provenance của đầu vào bảng đang nhất quán. Không cần phủ nhận phần cải thiện đó; chỉ cần hoàn thiện nốt đường sinh hình.

## 6. P3 — Hai chỗ còn sót thuật ngữ thống kê cũ

| Vị trí | Nội dung còn sót | Sửa đề xuất |
|---|---|---|
| Chương 1, đóng góp thứ tư, trang 1, PDF 7 | “kiểm định bootstrap theo cụm theorem có hiệu chỉnh Holm”. | “Khoảng tin cậy bootstrap theo cụm theorem và kiểm định hoán vị theo cụm có hiệu chỉnh Holm”. |
| Caption Bảng 7.1, trang 16, PDF 22 | Vẫn ghi “khoảng tin cậy và p hai phía từ bootstrap…” rồi tiếp tục ghi p từ hoán vị. | Chỉ ghi: “Khoảng tin cậy từ bootstrap theo cụm theorem; p hai phía từ kiểm định hoán vị ghép cặp theo cụm theorem, hiệu chỉnh Holm…”. |

Caption Bảng 7.1 được sinh trong `scripts/make_report_tables.py`, khoảng dòng 507–509. Nên sửa nguồn sinh caption thay vì sửa tay tệp bảng `.tex`.

Đây là lỗi mô tả còn sót, không phải dấu hiệu thuật toán vẫn đang dùng p bootstrap. Mã và CSV được kiểm tra đã dùng p hoán vị.

## 7. Trình bày và phạm vi kết luận

### 7.1. Kết luận riêng về layout

**Khung bố cục hợp lý; cách dàn trang còn cần chỉnh trước khi coi là bản cuối.** Tám chương đi đúng mạch bài toán → liên quan → dữ liệu → phương pháp → thiết lập → kết quả → phân tích → kết luận. Dạng A4 một cột, phân cấp tiêu đề, đánh số bảng/hình và tách phụ lục phù hợp với báo cáo học phần. Chưa có lý do để đổi toàn bộ sang bố cục bài báo hai cột nếu lớp không có mẫu yêu cầu.

Qua ảnh render không thấy lỗi tràn lề/chồng chữ rõ rệt. Phần thân 20 trang phân bổ khá cân đối: Giới thiệu 1, Liên quan 1, Dữ liệu 2, Phương pháp 3, Thiết lập 2, Kết quả 6, Phân tích 4, Kết luận 1 trang. **Nên giữ khung này và chỉnh vị trí bảng/hình, điểm ngắt đoạn, caption và khoảng trắng.** Điểm nội dung khoảng 9/10 ở Mục 1 không có nghĩa layout đã hoàn thiện tương ứng.

Phần bổ sung này được kiểm tra trên cùng PDF có hash ghi ở đầu file; đã xem lại các trang liên quan ở ảnh render lớn hơn và đọc cấu hình LaTeX. Đây là đề xuất chỉnh layout, chưa phải kết quả sau khi sửa và biên dịch lại PDF.

### 7.2. Những vấn đề layout cụ thể và cách sửa

| Ưu tiên | Vị trí | Quan sát trên bản hiện tại | Cách chỉnh |
|---|---|---|---|
| Cao | Trang 16–17, PDF 22–23 | Bảng 7.2 thuộc phân tích thành phần ở Mục 7.1 nhưng trôi tới đầu trang sau, khi văn bản đã chuyển sang Mục 7.2 về xây chỉ mục. Ngay dưới bảng lại tiếp tục câu đang nói về salting. | Giữ Bảng 7.2 trong cụm nội dung 7.1; đặt một ranh giới float trước khi bắt đầu 7.2. Nếu bảng không đủ chỗ, cho bảng và phần giải thích sang trang tiếp theo rồi mới mở 7.2. |
| Cao | Trang 13–14, PDF 19–20 | Hình 6.2 thuộc Mục 6.4 về kích thước kho, nhưng xuất hiện sau khi Mục 6.5 đã bắt đầu và chen giữa đoạn “Thêm worker có giúp không?”. | Đưa Hình 6.2 về sau đoạn giới thiệu của 6.4 và giữ nó trước 6.5. Tránh để hình về kích thước index cắt ngang phân tích về worker. |
| Cao | Trang 11–12, PDF 17–18 | Đoạn phân tích holdout kết thúc trang bằng từ “Trên”, trang sau mới bắt đầu “novel_premises…”. | Tách phân tích random/holdout và novel thành hai đoạn; mở đoạn mới từ “Trên novel_premises”. Giữ vài dòng đầu đoạn cùng nhau khi ngắt trang. |
| Vừa | Trang 12–13, PDF 18–19 | Sau Hình 6.1, phần mở đầu phép đo V4/V5 nằm ở cuối trang; câu tiếp tục sang trang sau rồi mới đến Bảng 6.5. | Kết thúc đoạn phân tích B0/V2/V4 trước; để đoạn giới thiệu phép đo V5 cùng Bảng 6.5 và ít nhất một đoạn diễn giải. Nếu cần, chuyển cả cụm sang trang sau. |
| Vừa | Trang 13–14, PDF 19–20 | Nhãn đậm “Thêm worker có giúp không?” chỉ có một phần ngắn ở cuối trang, còn nội dung chính bị đẩy qua hình. | Sau khi sửa vị trí Hình 6.2, giữ nhãn đậm cùng khoảng 3–4 dòng giải thích; tránh mở một luận điểm mới ở hai dòng cuối trang. |
| Vừa | Bảng 6.2, 6.3, 7.1; PDF 16–17, 22 | Caption dài nhiều dòng, mang cả định nghĩa kiểm định, cỡ mẫu và quy tắc đọc. Một số trang có hai bảng thống kê lớn nên khá dày. | Rút caption thành tên phép so sánh + đối tượng; đưa giải thích chung về CI/p về Mục 5.5, đặt ghi chú riêng dưới bảng khi cần. Giữ cỡ chữ bảng đọc được. |
| Vừa | Trang 22, PDF 28 | Trang tài liệu tham khảo thứ hai chỉ còn ba mục, phần lớn trang để trắng. | Thử giảm khoảng cách giữa các mục hoặc dùng cỡ chữ bibliography khoảng 10 pt; nếu vẫn cần hai trang thì phân bố hợp lý. Không bắt buộc ép 23 tài liệu vào một trang. |
| Thấp | Trang 27–28, PDF 33–34 | Các bảng phụ lục được dàn gần giữa trang hoặc giãn khoảng cách lớn, khiến nhịp trang không đều. | Nhóm phụ lục theo dữ liệu/môi trường, truy hồi, xây chỉ mục; ưu tiên căn đầu trang và khoảng cách giữa bảng ổn định. Có thể thêm tiêu đề nhóm ngắn để tạo mạch đọc. |
| Thấp, tùy mẫu lớp | PDF 5 | Danh sách hình chỉ có ba mục nhưng chiếm một trang riêng. | Nếu quy định cho phép và đủ chỗ, thử đặt danh sách hình và danh sách bảng trên cùng một trang; nếu mẫu yêu cầu tách thì giữ nguyên. |

Các khoảng trắng ở cuối một chương ngắn không tự nó là lỗi. Vấn đề đáng sửa nhất là bảng/hình đi sang luận điểm khác hoặc cắt ngang câu, chứ không phải mọi trang đều phải đầy kín.

### 7.3. Giữ gì ở thân bài, đưa gì về phụ lục?

Các bảng chứng minh kết luận chính nên tiếp tục ở thân bài:

- **Bảng 6.1:** kết quả tổng thể của baseline và các biến thể.
- **Bảng 6.3–6.4:** holdout, cách lấy trung bình và seen/unseen; đây là cơ sở của kết luận V4/V5.
- **Bảng 6.5:** chất lượng phục vụ và lỗi dưới tải.
- **Bảng 7.1 và 7.5:** ablation và phân rã giới hạn ứng viên/xếp hạng.

Những bảng môi trường, nguồn dữ liệu chi tiết, lưới tinh tham số, codec và worker đầy đủ đã đưa xuống phụ lục là hợp lý. Bảng kiểm định chi tiết 6.2 có thể chuyển xuống phụ lục nếu cần làm trang kết quả thoáng hơn, với điều kiện phần thân giữ lại effect size/CI và kết luận chính; đây là lựa chọn biên tập, không phải bắt buộc.

Phần “Bối cảnh và so sánh với nhóm khác” đang chen giữa kết quả RQ1 và độ bền V5 ở trang 11. Khi có kết quả thật của Nhóm 4, nên cân nhắc tạo một tiểu mục so sánh riêng trong Chương 6 để luồng đọc thành: kết quả chính → độ bền/seen-unseen → chi phí/quy mô → so sánh ngoài. Chưa có dữ liệu Nhóm 4 thì không cần mở thêm một mục lớn chỉ để chứa thông báo đang chờ.

### 7.4. Chữ, hình và caption

Font thân bài khoảng 11 pt, phần lớn bảng khoảng 10 pt là phù hợp; nên giữ cỡ này. Hình ghép hai ô có nhãn nhỏ hơn, nên kiểm tra bản in hoặc xem ở 100%. Với Hình 6.1–6.3, tăng cỡ nhãn ngay trong script vẽ và bớt nhãn lặp giúp dễ đọc hơn so với chỉ tăng kích thước chữ toàn báo cáo.

Hình 4.1 có nhiều thông tin nhưng vẫn đọc được. Có thể tăng chữ của hai hộp usage/prior ở nhánh phải bằng cách rút gọn câu trong hộp; chi tiết ràng buộc để ở Mục 4.6. Giữ chú thích rõ 239 là tổng pool trung bình.

Ví dụ rút caption Bảng 6.3:

> Recall@10 của V4, V4-K240 và V5 trên hai test split và holdout, theo query-macro và theorem-macro.

Ghi chú dưới bảng có thể nêu “KTC 95% từ bootstrap theo cụm theorem; holdout gồm 2.500 query của 1.138 theorem; ngân sách ứng viên xem Mục 5.1”. Như vậy caption dễ quét, còn định nghĩa vẫn có chỗ tra cứu. Không chỉ cắt các điều kiện cần thiết mà không chuyển chúng sang vị trí khác.

### 7.5. Cách triển khai trong LaTeX

Nguồn chính cần chỉnh là `report/latex/main.tex`; caption và bố cục bảng tự sinh cần chỉnh ở `scripts/make_report_tables.py`; chữ và nhãn hình chỉnh trong `scripts/make_figures.py`.

Có thể thử hai công cụ sau tại các điểm cụ thể:

```latex
% Trong preamble
\usepackage{placeins}
\usepackage{needspace}

% Sau khi kết thúc nội dung và bảng của 7.1
\input{tables/controls}
\FloatBarrier
\section{Ablation của đường xây chỉ mục}

% Giữ một nhãn mở luận điểm cùng vài dòng nội dung
\Needspace{5\baselineskip}
\paragraph{Thêm worker có giúp không?}
```

`\FloatBarrier` giúp giữ float trong ranh giới nội dung; `\Needspace` chuyển sang trang mới khi phần còn lại không đủ khoảng đã yêu cầu. Nên đặt barrier chọn lọc trước 6.5 và 7.2 rồi xem lại kết quả; đặt ở mọi tiểu mục hoặc ép mọi bảng bằng `[H]` có thể tạo thêm khoảng trắng. Hai cách này kiểm soát hai vấn đề khác nhau: vị trí float và không gian tối thiểu cho phần văn bản. [Tài liệu placeins trên CTAN](https://ctan.org/tex-archive/macros/latex/contrib/placeins), [tài liệu needspace trên CTAN](https://ctan.org/pkg/needspace).

Không cần thêm `\newpage` hàng loạt. Trước hết sửa điểm ngắt đoạn và ranh giới float, sau đó mới cân chỉnh khoảng cách bảng/caption và các trang phụ lục. Mỗi lần đổi vị trí float có thể ảnh hưởng vài trang sau, nên các số trang trong nhận xét này chỉ áp dụng cho bản PDF đang được đánh giá.

### 7.6. Thứ tự chỉnh và tiêu chí đạt

1. Sửa hai float trôi rõ nhất: Bảng 7.2 và Hình 6.2.
2. Sửa đoạn bị ngắt ở trang 11–12 và gom phần giới thiệu phép đo V5 với Bảng 6.5.
3. Rút caption dài, tăng độ rõ của nhãn hình; giữ cỡ chữ thân bài và bảng.
4. Cân đối bibliography, phụ lục và danh sách hình nếu mẫu lớp cho phép.
5. Biên dịch lại, xem toàn bộ PDF và kiểm tra lại mục lục, danh sách bảng/hình, tham chiếu và các trang phía sau chỗ đã chỉnh.

Layout có thể coi là đạt khi mỗi bảng/hình xuất hiện trong đúng cụm luận điểm, không cắt ngang phần khác; tiêu đề/nhãn mở đoạn có đủ nội dung đi cùng; các bảng thống kê đọc được ở kích thước trang thật; và khoảng trắng giữa các trang phụ lục có chủ đích. Tổng số trang có thể đổi nhẹ sau khi dàn lại, không cần lấy việc giữ đúng 34 trang làm mục tiêu.

### 7.7. Phạm vi kết luận cần giữ khi đổi layout

Thông điệp khoa học hiện đã phù hợp:

> V4 là lựa chọn cân bằng giữa chất lượng retrieval và độ trễ. V5 cải thiện candidate recall và Recall@10 tổng thể trong một số điều kiện. Tuy nhiên, trên holdout, chưa có đủ bằng chứng cho thấy V5 tốt hơn V4-K240; V5 cũng làm giảm recall trên unseen premise và tăng chi phí khi tải cao. Với phần xây index, kết quả cho thấy cách tổ chức Spark job ảnh hưởng lớn đến hiệu năng song song trên một máy. Các thử nghiệm mở rộng dùng corpus nhân bản như đã mô tả.

Nên giữ nguyên tinh thần này khi làm slide và demo. Không cần tìm cách đổi ngưỡng hoặc chọn metric khác để đưa các p-value gần 0,05 trở lại thành kết quả có ý nghĩa.

## 8. Bổ sung về văn phong và cách dùng thuật ngữ

### 8.1. Nhận xét chung

**Cần thêm một lượt biên tập ngôn ngữ.** Bản hiện tại đúng về chuyên môn hơn trước, nhưng một số câu vẫn mang dấu vết dịch sát thuật ngữ hoặc viết theo cấu trúc tiếng Anh. Các cụm như “truy hồi dày đặc”, “chấm lại 100 ứng viên”, “premise chưa thấy”, “phần dữ liệu huấn luyện giữ riêng làm holdout” hoặc “phần lợi ích chưa được xác lập” khiến câu nặng và đôi khi kém chính xác về nghĩa.

Đề xuất là **viết câu bằng tiếng Việt tự nhiên, giữ những thuật ngữ tiếng Anh quen thuộc trong lĩnh vực và giải thích ngắn khi xuất hiện lần đầu**. Không cần dịch mọi thuật ngữ; cũng không cần thay mọi từ tiếng Việt bằng tiếng Anh. Đây là định hướng biên tập theo yêu cầu của người viết, không phải nhận định rằng mọi thuật ngữ dịch hiện tại đều sai.

### 8.2. Quy ước thuật ngữ nên thống nhất

| Nhóm | Cách dùng đề xuất | Ghi chú |
|---|---|---|
| Bài toán | `premise retrieval`, `sparse retrieval`, `dense retrieval`, `hybrid retrieval` | Ưu tiên các tên này thay cho việc lặp lại “truy hồi thưa/dày đặc/lai”. Giải thích ngắn sự khác nhau ở lần đầu. |
| Đối tượng Lean | `premise`, `proof state`, `tactic`, `namespace` | Lần đầu có thể viết “proof state (trạng thái chứng minh)”. Khi nói chung về toán học vẫn dùng “định lý”, “bổ đề”; tên khai báo/code giữ nguyên. |
| Bước xử lý | `tokenizer`, `token`, `reranker`, `rerank` | Ví dụ “tokenizer cho Lean”, “rerank 100 candidate”. Không cần dịch thành “bộ tách từ” ở mọi chỗ vì tokenizer còn xử lý tên và ký hiệu. |
| Tập ứng viên | `candidate pool`, `candidate recall` | Định nghĩa candidate recall bằng công thức ở phần metric; có thể giải thích là tỉ lệ gold premise có trong pool. Sau đó dùng một tên nhất quán. |
| Dữ liệu | `corpus`, `dataset`, `split`, `train`, `validation`, `test`, `holdout` | Phân biệt corpus chứa premise với tập query và các split. Ví dụ “holdout lấy từ phần train B chưa dùng để fit reranker”. |
| Nhãn đánh giá | `gold premise`, `seen premise`, `unseen premise` | Gold là premise được benchmark gán nhãn; unseen là chưa xuất hiện trong nhãn train cùng split, không phải chưa có trong corpus. |
| Thực nghiệm | `baseline`, `benchmark`, `ablation`, `run`, `run record`, `seed`, `checkpoint` | Giải thích nếu cần, sau đó giữ thuật ngữ. “Tinh chỉnh tham số” hoặc “tuning” đều được; tránh dùng luân phiên nhiều tên không cần thiết. |
| Index và Spark | “chỉ mục đảo (inverted index)”; `posting list`, `shuffle`, `partition`, `worker`, `cache` | “Chỉ mục đảo” là cách gọi rõ và thông dụng, không cần đổi toàn bộ thành tiếng Anh. Phân biệt worker, process và thread; không gom cả ba thành “luồng”. |
| Chất lượng và chi phí | `Recall@k`, `MRR`, `nDCG@10`, `P95`, `QPS`; “độ trễ”, “thông lượng” | Tên metric giữ nguyên. “Độ trễ” và “thông lượng” tự nhiên trong câu tiếng Việt; nếu bảng dùng latency/throughput thì thống nhất cách ghi. |
| Mô hình và thống kê | “đặc trưng”, “hồi quy logistic”, “khoảng tin cậy”, “kiểm định hoán vị”, `bootstrap`, `p-value`, `Holm` | Các cách gọi tiếng Việt này đã rõ. Lần đầu có thể kèm tên đầy đủ `paired cluster permutation test`; tránh kéo tên dịch dài vào mọi câu. |
| Tên đặc trưng | `popularity`, `PageRank`, `file_usage`, `dir_usage` | Dùng đúng tên khi nói về feature cụ thể; giải thích popularity được tính bằng số theorem train A dùng premise. |
| Cách lấy trung bình | `query-macro`, `theorem-macro` | Định nghĩa lần đầu: mỗi query có trọng số bằng nhau / mỗi theorem có trọng số bằng nhau. Dùng nhãn này trong bảng để gọn và dễ đối chiếu. |

Các mục trên là quy ước gợi ý cho báo cáo này. Không thay chuỗi trong code, tên cột, query ID hay tên split `novel_premises` để phục vụ việc dịch thuật. Tránh tìm-thay tự động toàn văn vì cùng một từ có thể mang nghĩa khác nhau ở mô tả toán học và phần triển khai.

### 8.3. Những cụm cụ thể nên viết lại

| Cách viết hiện tại | Cách viết tự nhiên hơn | Vì sao |
|---|---|---|
| “chỉ dùng chỉ mục thưa và tín hiệu cấu trúc có chi phí thấp” | “kết hợp BM25F với các đặc trưng cấu trúc có chi phí tính toán thấp” | Nêu trực tiếp thành phần thực tế; tránh cụm “chỉ mục thưa” khó hình dung. |
| “một mô hình hồi quy logistic chấm lại 100 ứng viên” | “dùng hồi quy logistic để rerank 100 candidate” | Giữ đúng tên bước xử lý, câu ngắn hơn. |
| “bộ truy hồi dày đặc” | “dense retriever” | Tên quen thuộc, dễ liên hệ với ReProver và tài liệu tham khảo. |
| “premise truy cập được” | “accessible premise”, giải thích lần đầu là premise có thể dùng tại vị trí chứng minh hiện tại | “Truy cập” dễ bị hiểu thành quyền truy cập dữ liệu; ở đây liên quan import và thứ tự khai báo. |
| “recall trên premise chưa thấy” | “recall trên unseen premise” | Nhắc rõ unseen được xác định so với nhãn train, tránh hiểu rằng premise vắng khỏi corpus. |
| “phần dữ liệu huấn luyện giữ riêng làm holdout” | “holdout lấy từ phần train B chưa dùng để huấn luyện reranker” | Giữ thông tin về nguồn và cách loại mẫu, bớt vòng vo. |
| “phần V5 vượt đối chứng top 240 chưa được xác lập” | “trên holdout, chưa có đủ bằng chứng cho thấy V5 tốt hơn V4-K240” | Nêu chủ thể và phạm vi trực tiếp; giữ mức độ thận trọng thống kê. |
| “kết quả sau quan sát” | “kết quả sau khi thiết kế V5 dựa trên phân tích lỗi của test” | Giải thích đúng vấn đề thay cho một nhãn dịch ngắn nhưng khó hiểu. |
| “độ trễ đuôi thấp” | “giữ P95 latency ở mức thấp” hoặc “giữ độ trễ P95 ở mức thấp” | Gắn ngay với metric thực sự được dùng. |
| “phần mất do tạo ứng viên / phần mất do xếp hạng” | “recall mất ở bước tạo candidate / ranking gap” | Định nghĩa công thức một lần; tên cột sau đó có thể ngắn hơn. |
| “họ so sánh chính” | “nhóm phép so sánh chính” | Tự nhiên hơn trong phần mô tả; có thể kèm `family of hypotheses` lần đầu nếu cần. |
| “Nguy cơ đối với tính đúng đắn của kết luận” | “Hạn chế và threats to validity” | Ngắn, quen thuộc với báo cáo nghiên cứu; nội dung vẫn cần phân tích các yếu tố ảnh hưởng đến kết luận. |

Với tiêu đề báo cáo, có thể cân nhắc **“Premise retrieval cho Lean 4 bằng BM25F và đặc trưng cấu trúc trên mathlib4”**. Tiêu đề này nêu trực tiếp bài toán và phương pháp, bớt nặng hơn cụm “bằng chỉ mục thưa và tín hiệu cấu trúc ở quy mô thư viện”. Tên đề tài chính thức của học phần, nếu đã được chốt, vẫn cần được nhận diện rõ.

### 8.4. Ví dụ viết lại một đoạn

Đoạn mở đầu mô tả phương pháp có thể viết:

> Nhóm xây dựng hệ thống premise retrieval cho Lean 4 trên corpus mathlib4. Hệ thống dùng BM25F với ba trường name, namespace và statement, kết hợp tokenizer cho Lean để tạo candidate pool. Với V4, bộ lọc chỉ giữ các accessible premise, sau đó reranker dùng hồi quy logistic để xếp hạng lại top 100 candidate dựa trên các đặc trưng cấu trúc, popularity và PageRank. V5 bổ sung candidate từ lịch sử sử dụng trong train A và thêm hai đặc trưng file_usage, dir_usage. Hệ thống được đánh giá bằng Recall@10 và P95 latency; kết quả seen/unseen và holdout được phân tích riêng để làm rõ giới hạn của V5.

Đoạn trên là mẫu văn phong, không thay thế phần định nghĩa chi tiết: accessible premise, seen/unseen, ràng buộc lịch sử usage và train A/B vẫn phải được giải thích đúng ở các mục tương ứng. Không dùng câu văn gọn để làm mất điều kiện thí nghiệm hoặc nâng mức kết luận.

### 8.5. Quy tắc biên tập cho toàn báo cáo

1. **Giải thích ở lần đầu, dùng nhất quán về sau.** Không lặp bản dịch song ngữ ở mọi trang.
2. **Một câu nên có một ý chính.** Tách mô tả phương pháp, số liệu và hạn chế thành các câu riêng khi câu quá dài.
3. **Ưu tiên chủ thể và động từ rõ.** Viết “V5 tăng Recall@10…” hoặc “nhóm đo…” thay cho nhiều tầng danh từ như “phần lợi ích của việc bổ sung…”.
4. **Giữ văn phong học thuật nhưng dễ đọc.** Các từ “chưa được xác lập”, “sau quan sát”, “thực sự” chỉ nên dùng khi chúng diễn đạt rõ hơn; thường có thể thay bằng câu cụ thể về dữ liệu và bằng chứng.
5. **Phân biệt tên đối tượng với lời giải thích.** Ví dụ `popularity` là tên feature, còn “số theorem dùng premise” là định nghĩa; `novel_premises` là tên split, còn unseen premise là nhóm nhãn được xác định lại sau lọc.
6. **Đồng bộ văn bản, caption, bảng, hình và slide.** Nên lập bảng thuật ngữ ngắn trong phần đầu hoặc tài liệu nhóm dùng để biên tập; các thuật ngữ và chữ viết tắt cần được định nghĩa ở lần xuất hiện đầu tiên trong phần nội dung độc lập như abstract.

Áp dụng các nguyên tắc này cả với những mẫu caption và kết luận được gợi ý trong nhận xét lần ba. Những bản dịch từng dùng trong các nhận xét trước là cách giải thích nội dung, không phải yêu cầu phải Việt hóa chúng trong báo cáo cuối.

## 9. Danh sách hoàn thiện tối thiểu

- [ ] Hoàn tất kiểm tra 20 query, hai bộ nhãn cho 30 failure cases, phân công và xác nhận AI-use.
- [ ] Hoàn tất phần benchmark/kết quả Nhóm 4 hoặc thống nhất rõ phạm vi nghiệm thu với giảng viên nếu phụ thuộc này chưa sẵn sàng.
- [ ] Sửa hai chỗ còn gọi p là bootstrap trong Chương 1 và caption Bảng 7.1.
- [ ] Ghim nguồn sinh hình hoặc tách lệnh chỉ biên dịch từ các artifact đã phát hành.
- [ ] Chỉnh Bảng 7.2 và Hình 6.2 về đúng cụm nội dung; rà điểm ngắt đoạn, caption, bibliography và phụ lục theo Mục 7.
- [ ] Biên tập văn phong và thống nhất thuật ngữ theo Mục 8; ưu tiên giữ thuật ngữ chuyên ngành quen thuộc, giải thích ngắn ở lần đầu và kiểm tra lại các điều kiện khoa học sau khi viết gọn.
- [ ] Chốt revision và kiểm tra bản đóng gói từ checkout sạch; dựng/render PDF cuối.

**Kết luận lần ba:** Phần sửa thống kê đã đạt mục tiêu của phản biện lần trước trong các kiểm tra đã thực hiện. Không còn lý do từ các phát hiện hiện tại để mở thêm một vòng thuật toán hoặc benchmark lớn. Công việc tiếp theo nên là hoàn tất minh chứng, sửa mô tả còn sót và đóng gói bản nộp.
