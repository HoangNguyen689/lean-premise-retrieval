# Báo cáo LaTeX

`main.tex` là báo cáo chính thức của Nhóm 3; bản PDF đã biên dịch được chép ra `report/report.pdf`.
Báo cáo dùng lớp `report` của LaTeX: phần đầu đánh số La Mã (tóm tắt, mục lục, danh sách hình vẽ, danh sách bảng),
thân bài gồm 8 chương (20 trang), sau đó là tài liệu tham khảo và ba phụ lục A (khai báo AI, phân công), B (tái lập) và
C (bảng bổ sung). Hình, bảng và công thức đánh số theo chương.

## Nguồn số liệu

- Bảng số liệu trong `tables/*.tex` sinh bằng `python scripts/make_report_tables.py` từ kết quả thô; không sửa tay.
  `tables/SOURCES.md` ghi nguồn của từng bảng và các `run_id` đã ghim.
- Các lần chạy đánh giá dùng cho bản báo cáo được ghim trong `results/figures/report_manifest.json`
  (`python scripts/pin_runs.py`). Chỉ chạy lại script này khi chủ ý cập nhật báo cáo.
- `tables/example.tex` (ví dụ xuyên suốt) sinh bằng `python scripts/running_example.py`.
- Hình trong `figures/` sinh bằng `python scripts/make_figures.py --report`.
- Các phân tích độ bền (`scripts/robustness.py`) và phân rã ứng viên (`scripts/candidate_analysis.py`) phải chạy trước
  khi sinh bảng.

## Biên dịch

Cần XeLaTeX (hoặc Tectonic, dựa trên XeTeX) vì báo cáo dùng `fontspec` với font TeX Gyre Termes và DejaVu Sans Mono.

```bash
bash build.sh                       # sinh lại bảng, ví dụ và hình rồi biên dịch bằng Tectonic hoặc xelatex
```

Hoặc thủ công:

```bash
tectonic -X compile main.tex        # hoặc: xelatex main.tex && xelatex main.tex
```

Trên Overleaf: tải cả thư mục này lên (gồm `tables/` và `figures/`) và chọn trình biên dịch XeLaTeX.

## Các chỗ nhóm phải điền trước khi nộp

Chữ đỏ trong ngoặc vuông (macro `\canchot`) đánh dấu nội dung nhóm còn phải làm hoặc chốt:

- Người nhận vai trò Đặc trưng cấu trúc và Phục vụ (Vũ Trung Kiên hoặc Trần Đình Dũng), cùng người dự phòng tương ứng (Phụ lục A.2).
- Đối chiếu thủ công và ký xác nhận 20 truy vấn kiểm tra (Mục 3.4, `docs/check_queries.md`).
- Bảng so sánh với Nhóm 4 (đoạn "So sánh với Nhóm 4" cuối Mục 6.1).
- Gán nhãn thủ công 30 trường hợp thất bại bởi hai thành viên và tỉ lệ đồng thuận (Mục 7.3).

Khi làm xong, sửa câu mô tả trạng thái tương ứng trong báo cáo (hiện ghi là "chưa được thực hiện") rồi mới xóa macro
`\canchot`. Nhóm cũng cần mở từng tài liệu tham khảo để kiểm tra trích dẫn.
