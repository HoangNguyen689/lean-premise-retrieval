# License và privacy note

## Dữ liệu
- **LeanDojo Benchmark 4 v10**: phát hành theo **CC BY 2.0** (theo `licenses/README.md` trong bản tải và trang Zenodo
  record 12740403). Được phép sao chép, chỉnh sửa, phân phối lại với điều kiện ghi công tác giả.
  Ghi công: Kaiyu Yang và cộng sự, *LeanDojo: Theorem Proving with Retrieval-Augmented Language Models*, NeurIPS 2023.
- **Mã Lean gốc** (statement, code) thuộc các repo: mathlib4, lean4, batteries, aesop, ProofWidgets4, quote4,
  import-graph, lean4-cli. Bản tải kèm giấy phép từng repo trong `licenses/` (mathlib4 và lean4: Apache-2.0).
- `data_sample/` chứa 1.000 premise và 200 truy vấn trích từ bộ trên, giữ nguyên nội dung, kèm ghi công này.
- Dữ liệu đầy đủ không đưa vào Git; chỉ có script tải (`scripts/download_data.py`) và manifest có md5.

## Privacy
- Dữ liệu là mã nguồn toán học công khai, không chứa thông tin cá nhân của người học.
- Tên tác giả commit của mathlib không được trích hay lưu.
- Run record lưu cấu hình máy nhưng chỉ lưu băm tên máy (`hostname_hash`), không lưu tên người dùng.
