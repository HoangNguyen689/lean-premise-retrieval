"""Kiểm tra đầu vào của bảng và hình còn khớp với bản báo cáo đã phát hành.

Đọc SHA-256 ghi trong report/latex/tables/SOURCES.md và report/latex/figures/SOURCES.md (do make_report_tables.py và
make_figures.py --report ghi lại lúc sinh bản phát hành), tính lại SHA-256 của từng tệp và báo mọi tệp thiếu hoặc lệch.
report/latex/build.sh gọi script này trước khi sinh lại bảng và hình; nếu có lệch, build dừng thay vì âm thầm tạo bảng
khác bản đã phát hành. Muốn chủ ý cập nhật báo cáo bằng dữ liệu mới thì dùng build.sh --update.

SHA-256 được ghi trên tệp lúc sinh: tệp ghi trên Windows có xuống dòng CRLF, tệp ghi trong Docker Linux có LF, còn Git
lưu LF và đổi xuống dòng khi checkout theo core.autocrlf. Vì vậy một tệp được coi là khớp nếu chính nó, hoặc cùng nội
dung đổi hết sang LF hay CRLF, có SHA-256 đã ghi. Tệp nhị phân (Parquet, PNG) Git không đổi nên vẫn khớp ở dạng gốc.

Dùng:  python scripts/verify_report_inputs.py
Thoát: 0 nếu mọi tệp khớp, 1 nếu có tệp thiếu hoặc lệch.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = [ROOT / "report" / "latex" / "tables" / "SOURCES.md", ROOT / "report" / "latex" / "figures" / "SOURCES.md"]
ROW = re.compile(r"^\| `([^`]+)` \| `([0-9a-f]{64})` \|$")


def digests(data: bytes) -> set[str]:
    """SHA-256 của tệp ở dạng gốc, dạng xuống dòng LF và dạng CRLF."""
    lf = data.replace(b"\r\n", b"\n")
    return {hashlib.sha256(form).hexdigest() for form in (data, lf, lf.replace(b"\n", b"\r\n"))}


def main() -> int:
    checked, bad = 0, []
    for m in MANIFESTS:
        if not m.exists():
            bad.append(f"thiếu {m.relative_to(ROOT).as_posix()}")
            continue
        for line in m.read_text(encoding="utf-8").splitlines():
            r = ROW.match(line)
            if not r:
                continue
            path, expected = ROOT / r.group(1), r.group(2)
            checked += 1
            if not path.exists():
                bad.append(f"thiếu {r.group(1)}")
            elif expected not in digests(path.read_bytes()):
                bad.append(f"lệch  {r.group(1)}")
    for b in bad:
        print(b)
    print(f"{checked} tệp đầu vào được kiểm tra, {len(bad)} tệp thiếu hoặc lệch")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
