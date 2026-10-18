# Đánh giá báo cáo lần 2

**Ngày đánh giá:** 18/10/2026. **Bản được xem:** `report.pdf` cập nhật lúc 23:40 ngày 18/10/2026, 33 trang PDF, nội dung Chương 1–8 vẫn là 20 trang.

**Nguồn:** [báo cáo hiện tại](D:/bigdata/nhom3-lean-retrieval/report/report.pdf), [nhận xét lần trước](D:/bigdata/nhom3-lean-retrieval/report/danh_gia_report.md), mã nguồn và kết quả trong dự án. Đã đọc bản PDF mới, xem ảnh render của cả 33 trang, đối chiếu các bảng robustness, manifest, holdout và phép đo tải mới. Không chạy lại toàn bộ retrieval/Spark hoặc toàn bộ test suite; có chạy kiểm tra dữ liệu holdout và ví dụ tái hiện lỗi thống kê.

**Dấu nhận diện bản PDF:** SHA-256 `a5a68158c018743670cb93ada641f8f75d856e94b23a80871f53892513dbdd02`.

**Quy ước:** Số trang trong nội dung là số in trên báo cáo; số “PDF” tính từ trang bìa. Các đường dẫn tương đối tính từ `D:/bigdata/nhom3-lean-retrieval/`.

## 1. Nhận định sau khi sửa

**Bản này tiến bộ rõ rệt về độ tin cậy và lập luận nghiên cứu.** Các sửa đổi không chỉ đổi câu chữ mà đã bổ sung đối chứng, phân tích dữ liệu và kết quả bất lợi cần thiết. Phần tốt nhất hiện nay là câu chuyện về V5: tăng recall tổng thể, nhưng lợi ích vượt việc tăng số ứng viên chưa rõ trên holdout và có đánh đổi lớn với premise chưa thấy. Đây là kết quả nghiên cứu có giá trị hơn một kết luận “V5 tốt nhất” đơn giản.

Mức tham khảo của chất lượng bản thảo hiện tại là **khoảng 8,5–9/10**, so với khoảng 8/10 ở lần trước. Điểm này chưa phải chấm nghiệm thu: còn phần việc thủ công, phối hợp Nhóm 4 và một lỗi thống kê cần xử lý. **Chưa nên nộp nguyên trạng**, nhưng không cần mở thêm một vòng phát triển thuật toán lớn.

Ba ưu tiên còn lại là:

1. Sửa cách tính/diễn giải p-value, đặc biệt lỗi p hai phía đã tái hiện được.
2. Hoàn tất kiểm tra thủ công, gán nhãn và phân công; bổ sung so sánh Nhóm 4 theo yêu cầu học phần.
3. Làm chính xác hơn diễn giải đối chứng V4-K240, holdout và kết quả tải có timeout.

## 2. Những nhận xét cũ đã được xử lý tốt

| Vấn đề lần trước | Thay đổi trong bản mới | Đánh giá |
|---|---|---|
| Số theorem sau lọc chưa đúng | Bảng 3.1 tách theorem gốc, có tactic, có chú thích và còn query; giải thích 882/1.196 theorem test. | **Đã xử lý tốt.** |
| Novelty bị thay đổi sau lọc | Nêu 103 theorem không còn gold unseen và 2.506/9.735 cặp nhãn unseen. | **Đã xử lý tốt.** |
| V5 đổi dấu khi lấy trung bình theo theorem | Bảng 6.3 trình bày cả hai cách lấy trung bình và phân nhóm theo độ dài proof. | **Đã xử lý tốt.** |
| Chưa biết V5 có tìm premise mới tốt hơn không | Bảng 6.4 tách seen/unseen, nêu rõ R@10 unseen giảm 0,444 → 0,359. | **Đã xử lý tốt.** |
| V5 phát triển từ lỗi test | Mục 5.3 công khai quá trình; bổ sung holdout từ train B chưa dùng trong mẫu huấn luyện reranker. | **Tiến bộ lớn; cần giữ đúng phạm vi holdout.** |
| Chỉ so V5 với V4 top-100 | Thêm V4-K240 trên cả hai test và holdout. | **Đối chứng hữu ích; chưa cô lập hết từng thành phần.** |
| So số công bố LeanDojo như cùng benchmark | Chuyển Bảng C.4 thành bối cảnh, ghi đúng bảng nguồn, bỏ phần trăm thu hẹp khoảng cách. | **Đã xử lý tốt.** |
| Khẳng định V5 không tăng P95 | Đo ba cấu hình trong cùng phiên, xoay thứ tự, công khai P95 tăng và timeout. | **Đã sửa đúng hướng.** |
| Namespace/PageRank bị kết luận quá mức | Thêm V2-nons, popularity-only và PageRank-only; giảm mức khẳng định. | **Đã xử lý tốt.** |
| Lucene vừa đổi analyzer vừa đổi tham số | Thêm analyzer tiếng Anh với cùng k1/b, đo độ trùng top-10 và thời gian theo cùng quy tắc. | **Đã xử lý tốt.** |
| Độ phủ pool bị đồng nhất với trần R@10 | Bảng 7.5 có Oracle@10 và phần mất do xếp hạng; không còn nói nút thắt chuyển hoàn toàn. | **Đã xử lý tốt.** |
| Không rõ prior tĩnh hay lịch sử có trước | Hình 4.1 và Mục 4.6 phân biệt popularity/PageRank tĩnh với usage theo vị trí/import. | **Đã xử lý tốt.** |
| Corpus nhân bản/local bị diễn giải rộng | Đặt giới hạn ngay trong abstract, bảng và kết luận. | **Đã xử lý tốt.** |
| Số biến thể/lần đo/làm tròn sai | Có 8 biến thể, 24 đánh giá chính, 108 lần đo tải và bảng phụ sinh từ dữ liệu. | **Phần lớn đã xử lý.** |
| Tái lập chưa đầy đủ | Có lockfile, dependency, manifest ghim run, script sinh bảng và tùy chọn build PDF. | **Cải thiện rõ; chưa xác nhận chạy từ checkout sạch.** |
| Mô tả kiểm tra thủ công như đã hoàn thành | Bản mới nói rõ việc nào chưa thực hiện. | **Đã sửa tính trung thực của mô tả; công việc vẫn còn.** |

Những vấn đề đã xử lý trong bảng này không nên tiếp tục được tính là lỗi của bản hiện tại.

## 3. P1 — Lỗi p-value cần sửa trước khi chốt kết luận thống kê

**Vị trí báo cáo:** Mục 5.5, Bảng 6.2, Bảng 7.1 và các câu dùng “có ý nghĩa”. **Mã nguồn:** [metrics.py, dòng 75](D:/bigdata/nhom3-lean-retrieval/src/n3/eval/metrics.py:75).

Bootstrap theo cụm theorem và tách query/theorem estimand là cải tiến đúng. Tuy nhiên, phần p hai phía hiện tính:

```python
p1 = (boots <= 0).mean()
p_two_sided = min(1.0, 2 * min(p1, 1 - p1))
```

Đã chạy ví dụ sau trên chính hàm của dự án:

```python
from n3.eval.metrics import paired_cluster_bootstrap

r = paired_cluster_bootstrap(
    [0.0, 0.0], [0.0, 0.0], ['A', 'B'], n_boot=10000
)
print(r)
# delta = 0.0; CI = [0.0, 0.0]
# p_value = 1.0; p_two_sided = 0.0
```

Hai hệ thống giống hệt nhau nhưng nhận p hai phía bằng 0. Nguyên nhân là `1 - P(boots <= 0)` bằng `P(boots > 0)`, không phải `P(boots >= 0)`; khối xác suất tại 0 bị xử lý lệch. Với ví dụ `a=[1,1]`, `b=[0,1]`, hàm cũng cho p hai phía bằng 0 dù phân phối bootstrap có xác suất đáng kể bằng 0.

**Đây là lỗi cài đặt đã xác nhận.** Chưa có bằng chứng rằng tất cả p-value ở bảng thực tế bị thay đổi bởi lỗi này; không được suy từ ví dụ trên thành kết luận mọi metric hay CI đều sai. Điểm ước lượng R@10, MRR và phần CI không sử dụng công thức p hai phía này.

Ngoài lỗi ties, Mục 5.5 tự ghi rằng giá trị p hiện tại là xác suất đuôi bootstrap, không phải p của kiểm định dưới giả thuyết không, nhưng sau đó vẫn hiệu chỉnh Holm và dùng để tuyên bố có ý nghĩa ở mức 0,05. Cần biện minh phương pháp kiểm định và tính hiệu chuẩn, hoặc đổi sang một phép kiểm định có giả thuyết không rõ ràng. Ghi chú minh bạch là tốt nhưng chưa giải quyết mâu thuẫn phương pháp này.

**Cách hoàn thiện đề xuất:**

- Giữ paired cluster bootstrap để tính CI.
- Tính p bằng paired randomization ở cấp theorem: trong mỗi lần, hoán đổi nhãn hai hệ thống cho toàn bộ query của một theorem, rồi tính lại đúng query-macro hoặc theorem-macro. Phải nêu giả định exchangeability của phép hoán đổi, không hoán đổi từng query độc lập.
- Tính xác suất đuôi so với thống kê quan sát trong phân phối dưới H0; xử lý trường hợp bằng nhau và hiệu chỉnh Monte Carlo. Sau đó mới hiệu chỉnh Holm trên họ đã chốt.
- Bổ sung kiểm tra hai hệ thống giống nhau, đảo chiều a/b của p hai phía, trường hợp có nhiều ties, và đối chiếu với một ví dụ hoán vị vét cạn nhỏ. Chỉ sửa `(boots <= 0)` thành một công thức khác chưa đủ để xác lập một phép kiểm định đúng.
- Sinh lại Bảng 6.2, Bảng 7.1 và các câu phụ thuộc p; chưa cần chạy lại retrieval vì đã có metric từng query.

Tài liệu SciPy phân biệt p-value với tỉ lệ cực trị của phân phối dưới H0 và mô tả hoán đổi mẫu ghép cặp; tài liệu statsmodels mô tả Holm là hiệu chỉnh các p-value đầu vào. [SciPy permutation_test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.permutation_test.html), [statsmodels multipletests](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html).

**Lưu ý khi đọc bảng:** p một phía dưới 0,05 nhưng CI hai phía 95% chứa 0 không tự nó là mâu thuẫn. Vấn đề ở đây là định nghĩa/cài đặt p và cách dùng nó, không phải quy tắc “mọi CI chứa 0 thì mọi kiểm định đều không có ý nghĩa”.

## 4. P1 — Các phần nghiệm thu vẫn chưa hoàn thành

| Việc còn thiếu | Vị trí hiện tại | Cách hoàn tất |
|---|---|---|
| Đối chiếu thủ công và ký 20 query | Mục 3.4, trang 4, PDF 10. | Thành viên kiểm tra thực sự, ghi tên/ngày và các trường hợp bất thường. |
| Hai người gán nhãn 30 failure cases | Mục 7.3, trang 18, PDF 24. | Lưu hai bộ nhãn độc lập, quy tắc gán và kết quả thống nhất; báo mẫu số khi tính đồng thuận. |
| So sánh Nhóm 4 trên cùng benchmark | Mục 6.1, trang 11, PDF 17. | Chốt contract và chạy kết quả thật; nếu chưa có, ghi trạng thái chưa hoàn tất như hiện tại. |
| Người chính/dự phòng ở một số vai trò | Phụ lục A.2, trang 22, PDF 28. | Chốt tên cụ thể và minh chứng đóng góp. |
| Revision tái tạo được | Mục 7.5, trang 19, PDF 25. | Chốt commit/release; giữ nguyên provenance của run cũ và ghi revision đầy đủ cho run mới. |

Bản mới đã mô tả trung thực tình trạng chưa thực hiện. Đây là tiến bộ, nhưng chưa thay thế việc hoàn tất yêu cầu. Những việc cần con người làm không nên được “sửa” bằng cách xóa đoạn màu đỏ rồi giữ nguyên nội dung như thể đã hoàn thành.

## 5. P2 — Đối chứng V4-K240 tốt hơn trước nhưng chưa phải cô lập nguồn ứng viên

**Vị trí:** Mục 5.1, 6.2; Bảng 6.3 và 7.5; PDF 14, 17, 24.

Có hai giới hạn cần ghi chính xác:

1. **Ngân sách chỉ xấp xỉ bằng nhau.** V4-K240 có 240 ứng viên/query; V5 trung bình 238,5 ở random, 236,3 ở holdout nhưng chỉ 208,4 ở novel. Vì vậy gọi “cùng ngân sách” trên novel là chưa chính xác; nên dùng “đối chứng top-240, xấp xỉ pool V5 trên random/holdout”. Ngân sách ứng viên cũng chưa đồng nghĩa chi phí tính toán bằng nhau.
2. **Đổi cả pool và đặc trưng.** V4-K240 dùng 13 đặc trưng, V5 dùng 15, thêm `file_usage` và `dir_usage`. Chênh lệch V5 − V4-K240 là tác động tổng hợp của nguồn ứng viên và hai đặc trưng usage sau huấn luyện lại, không phải tác dụng riêng của nguồn ứng viên.

Do đó câu “lợi ích riêng của các nguồn ứng viên …” ở cuối trang 11 nên đổi thành:

> Phần lợi ích của V5 vượt đối chứng top-240, bao gồm thay đổi nguồn ứng viên và đặc trưng usage, chưa được xác lập trên holdout.

Tương tự, “khoảng một nửa mức tăng đến từ nhiều ứng viên hơn” nên viết là **phân rã mô tả**: V4→V4-K240 tăng khoảng 0,011; V4-K240→V5 tăng khoảng 0,011. Hai phép chuyển không tạo thành một phép tách tác động nhân quả độc lập vì pool, đặc trưng và quá trình huấn luyện tương tác.

Nếu chỉ sửa báo cáo, đổi cách diễn đạt là đủ. Nếu muốn kết luận riêng từng thành phần, thêm V4 + hai đặc trưng usage nhưng giữ pool cũ, và pool V5 với cùng bộ 13 đặc trưng; chọn trên validation, xác nhận trên holdout mới. Không cần chạy thêm chỉ để đáp ứng một câu kết luận có thể viết thận trọng hơn.

## 6. P2 — Holdout mới hợp lý cho xác nhận nội bộ, cần giữ đúng phạm vi

Đã kiểm tra trực tiếp `random_holdoutB.npy`, bảng query và cách tái tạo mẫu 6.000 query huấn luyện:

| Kiểm tra | Kết quả |
|---|---:|
| Query holdout | 2.500 |
| Theorem holdout | 1.138 |
| Query thuộc train random nửa B | 2.500/2.500 |
| Trùng theorem với mẫu huấn luyện reranker, đối chiếu cặp file/tên | 0 |
| Trùng theorem với validation/test random | 0 |
| Proof state trùng chuỗi chính xác với validation/test random | 0 |
| Query ID của V4, V4-K240 và V5 trong các run holdout | Cùng tập holdout |

R@10 tính lại từ các tệp per-query đã ghim lần lượt là **0,31015; 0,32120; 0,33235**, khớp Bảng 6.3. Chưa phát hiện chồng lấn theorem trong các phép kiểm tra trên. Các kiểm tra tập dữ liệu không thể tự xác nhận lịch sử “chưa từng được xem”; phần đó vẫn cần nhật ký quy trình.

Holdout này là **phần dữ liệu train B còn lại, được dành riêng cho xác nhận nội bộ**, cùng snapshot và phân phối thư viện. Nó không phải benchmark bên ngoài hoặc split novel mới. Việc loại mọi theorem có ít nhất một query được lấy vào train còn khiến proof nhiều query có xác suất bị loại cao hơn; holdout có khoảng 2,20 query/theorem, so với 2,99 ở test random được chấm.

Nên bổ sung một câu về giới hạn chọn mẫu này và gọi kết quả là “xác nhận trên phần dữ liệu chưa dùng để fit/chọn cấu hình”, tránh diễn đạt như đã kiểm chứng khả năng tổng quát sang thư viện hoặc thời điểm mới. Sau khi đã dùng holdout để quyết định cải tiến tiếp theo, không tiếp tục coi nó là tập xác nhận chưa xem.

## 7. P2 — Bảng tải nên thể hiện rõ lần timeout và metric có điều kiện

**Vị trí:** Mục 6.3, Bảng 6.5, trang 12–13, PDF 18–19.

Đo xen kẽ ba cấu hình là cải thiện đúng. Báo cáo cũng đã công khai một request timeout. Đối chiếu 27 mức đo mang tag `v5cmp2` xác nhận:

| V5, 10 client | Giá trị |
|---|---:|
| QPS thấp nhất trong ba lần | 3,30 |
| QPS trung vị | 127,64 |
| QPS cao nhất | 134,41 |
| Lần có lỗi | `v5cmp2-r2` |
| Thành công/lỗi của lần đó | 399/1 |
| P95 của request thành công trong lần đó | 138,73 ms |

P95 được tính từ request thành công trong `src/n3/eval/loadtest.py`; timeout không có mặt trong mảng latency. QPS lại tính trên wall time gồm cả thời gian chờ timeout. Vì vậy một lần đo có P95 khoảng 139 ms đồng thời QPS 3,3 là có thể xảy ra theo định nghĩa hiện tại.

**Đề xuất:** Caption ghi “latency của request thành công”; bảng thêm số lỗi và QPS min–max hoặc đưa đủ ba lần đo vào phụ lục. Không dùng trung vị để người đọc bỏ qua sự kiện này. Phân biệt thông lượng điển hình khi chạy thành công với độ tin cậy thực nghiệm; chưa đủ bằng chứng để kết luận nguyên nhân timeout là chi phí 240 ứng viên hay lỗi phía nào.

## 8. Những điểm biên tập còn nên chỉnh

| Vị trí | Nhận xét | Sửa đề xuất |
|---|---|---|
| Abstract, PDF 2 | Số unseen 0,444→0,359 nằm sau kết quả holdout, dễ bị hiểu là cũng đo trên holdout. | Thêm “trên test novel_premises” ngay trước con số. |
| Mục 5.2, cuối trang 8 | “Tập kiểm tra chỉ được chạy với cấu hình đã chốt” dễ được hiểu rộng hơn thực tế Mục 5.3. | Ghi rõ “tham số số ứng viên được chọn trên validation; thiết kế V5 đã chịu ảnh hưởng của test”. |
| Mục 7.5, đoạn nhiều so sánh | Ghi các cấu hình đối chứng chỉ chạy random, trong khi V4-K240 và V2-nons có cả novel. | Giới hạn câu đó cho popularity-only, PageRank-only và ablation V4; nêu đối chứng nào có hai split. |
| Bảng 6.1 | V5 được in đậm cả dòng trong khi kết luận chọn V4 làm cấu hình dùng chung. | Chú thích đậm là cao nhất theo metric query-macro trong bảng, hoặc làm nổi cả cấu hình mặc định V4. |
| Hình 4.1, PDF 11 | Đã có V5, nhưng cụm hộp/nhánh phải khá nhỏ. | Tăng chữ ở nhánh usage/prior khi có thể; giữ rõ 239 là tổng pool trung bình, không phải số thêm. |
| Bảng 6.2–6.3, 7.1 | Một số cận được in `−0,000`, khó thấy mức độ gần 0. | Với cận sát 0, dùng thêm chữ số hoặc chú thích; tránh xóa dấu khiến đổi cách hiểu CI. |
| Tái lập ở Phụ lục B | Lệnh `pin_runs.py` chọn lại run mới nhất; không phải chỉ đọc manifest đã ghim. | Tách lệnh “tái tạo đúng bản đã phát hành” khỏi “cập nhật bản báo cáo bằng run mới”. |
| Truy vết bảng | Chất lượng đã ghim run, nhưng một số bảng tải/build vẫn tổng hợp các JSON theo bộ lọc. | Nếu cần tái tạo chính xác bản nộp, ghim luôn danh sách run và checksum của các CSV nguồn, không chỉ bảng chất lượng. |
| Khai báo AI | Phụ lục A chỉ nêu Claude, dù lần sửa này có dùng nhận xét của Codex. | Nếu các nhận xét hoặc phép kiểm tra từ cuộc trao đổi này được đưa vào báo cáo, bổ sung đúng vai trò hỗ trợ phản biện của Codex; không gán toàn bộ mã cho công cụ khác. |

Về bố cục, bản mới gom bảng phụ vào Phụ lục C và giữ thân bài 20 trang là hợp lý. Qua ảnh render không thấy tràn lề/chồng chữ rõ rệt; bảng thống kê vẫn khá dày. Không cần tiếp tục ép nhỏ chữ để giảm tổng 33 trang, nhất là khi chưa chốt cách tính giới hạn trang của lớp.

## 9. Thông điệp nghiên cứu nên dùng khi bảo vệ

**V4 là cấu hình cân bằng; V5 là một đánh đổi có điều kiện.** V4 cải thiện mạnh so với baseline và vẫn tốt hơn V5 trên premise chưa thấy. V5 mở rộng độ phủ ứng viên và tăng recall tổng thể trên random/holdout, nhưng phần vượt đối chứng top-240 chưa rõ trên holdout, giảm chất lượng unseen và tăng chi phí tải.

Kết quả hệ thống quan trọng khác là **cách tổ chức Spark job quyết định điểm hòa vốn**: engine RDD không thắng bản tuần tự ở các kích thước đã thử; Arrow và gộp trước shuffle mang lại lợi ích trên dữ liệu đủ lớn. Giới hạn một máy và corpus nhân bản đã được nêu đúng, nên đây là một kết luận thực nghiệm có phạm vi rõ.

Không nên trở lại cách trình bày “V5 tốt nhất trên mọi mặt”, “namespace chắc chắn cần thiết”, hoặc “3,84 lần chứng minh khả năng mở rộng của cụm”. Bản mới đã có đủ bằng chứng để kể một câu chuyện chính xác và có giá trị mà không cần các khẳng định đó.

## 10. Danh sách hoàn thiện ngắn nhất trước khi nộp

- [ ] Sửa lỗi ties của p hai phía và chốt phép kiểm định p-value; tính lại p/Holm từ per-query đã lưu.
- [ ] Cập nhật các câu “có ý nghĩa” sau khi tính lại; giữ riêng CI bootstrap và p của kiểm định đã chọn.
- [ ] Đổi “lợi ích riêng của nguồn ứng viên” thành lợi ích tổng hợp của V5 so với đối chứng top-240; ghi ngân sách chỉ xấp xỉ.
- [ ] Nêu phạm vi holdout train-B và chỉ rõ số unseen trong abstract đo trên test novel.
- [ ] Bổ sung số lỗi, QPS min–max và định nghĩa latency thành công cho Bảng 6.5.
- [ ] Hoàn tất 20 query kiểm tra, hai bộ nhãn cho 30 failure cases, phân vai và phối hợp Nhóm 4.
- [ ] Chốt revision, ghim nguồn dữ liệu của bản báo cáo, chạy kiểm tra từ checkout sạch và render PDF cuối.

**Khuyến nghị hiện tại:** Dừng thêm thuật toán. Tập trung sửa phần thống kê, hoàn tất những việc cần thành viên thực hiện và đóng gói provenance. Khi các mục đó hoàn thành, bản báo cáo đã có nền tảng tốt để bảo vệ.
