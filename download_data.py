#!/usr/bin/env python3
"""download_data.py — Tải + build dữ liệu LeanDojo Benchmark 4 cho Nhóm 3.

Viết THUẦN PYTHON (không cần Git Bash / bash) để chạy được trên mọi Windows
đã cài Python 3.8+. Chạy:

    python download_data.py

Làm 4 việc, mỗi bước đều có kiểm tra và có thể chạy lại mà không làm lại
những bước đã xong (resumable):
  1. Kiểm tra/cài pyarrow+pandas (chỉ Parquet là cần; thiếu thì cảnh báo,
     CSV vẫn build đủ — không chặn)
  2. Tải tar.gz 68 MB từ Zenodo — VERIFY SHA-256 sau khi tải (tệp hỏng/mạng
     đứt → phát hiện ngay, xóa để lần sau tải lại từ đầu)
  3. Giải nén + verify các file bắt buộc
  4. Build corpus/queries/qrels 3 scale (gọi scripts/build_real_corpus.py)
     + Parquet/index manifest (gọi scripts/fill_gaps.py — thiếu pandas thì
     bỏ qua phần Parquet, không chết)

Sau khi xong, chạy `python check_setup.py` để xác nhận mọi thứ sẵn sàng.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys

# Windows console (CMD) thường dùng cp1252/cp437 — không chứa chữ tiếng Việt.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
# Script con gọi qua pipe cũng phải nói UTF-8 (không nhận cp1252 từ console).
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
import time
import urllib.request
from pathlib import Path

# ── Hằng số ────────────────────────────────────────────────────────────────
ZENODO_RECORD = "12740403"
ZENODO_META_URL = f"https://zenodo.org/api/records/{ZENODO_RECORD}"
ZENODO_FILE_URL = (f"https://zenodo.org/api/records/{ZENODO_RECORD}"
                   f"/files/leandojo_benchmark_4.tar.gz/content")
EXPECTED_SHA256 = "19b9a31968229d5bae4b959be9351d92740643d16a58c7f58f6d82795b8a98a4"
EXPECTED_SIZE = 68141936  # bytes
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
           "Accept": "application/json"}

ROOT = Path(__file__).resolve().parent
TARBALL = ROOT / "data_raw" / "leandojo_benchmark_4.tar.gz"
EXTRACTED = ROOT / "data_raw" / "leandojo_benchmark_4"

REQUIRED_AFTER_EXTRACT = [
    "metadata.json", "corpus.jsonl",
    "random/test.json", "random/train.json", "random/val.json",
]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_py(script: Path, what: str) -> bool:
    """Chạy 1 script con cùng interpreter hiện tại; False = lỗi (đã in ra)."""
    print(f"\n→ {what}: python {script.name}")
    r = subprocess.run([sys.executable, str(script)], cwd=str(ROOT))
    if r.returncode != 0:
        print(f"✗ {what} THẤT BẠI (exit {r.returncode}). Đọc lỗi ở trên.")
        return False
    return True


# ── Bước 1: thư viện ───────────────────────────────────────────────────────
def step_deps() -> None:
    print("\n[1/4] Kiểm tra thư viện (pyarrow, pandas)...")
    try:
        import pyarrow  # noqa: F401
        import pandas  # noqa: F401
        print("  ✓ pyarrow + pandas đã có — Parquet sẽ được sinh.")
    except ImportError:
        print("  ⚠ Thiếu pyarrow/pandas — cài thử bằng pip...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "pyarrow", "pandas"])
        if r.returncode == 0:
            print("  ✓ Đã cài xong.")
        else:
            print("  ⚠ Cài không thành công. CSV vẫn build đủ, chỉ thiếu file Parquet")
            print("    (môn yêu cầu Parquet — nên tự cài: pip install pyarrow pandas)")


def _safe_unlink(path: Path, attempts: int = 3) -> None:
    """Xóa file; trên Windows file có thể bị antivirus/quét giữ → thử lại vài lần."""
    for i in range(attempts):
        try:
            path.unlink()
            return
        except PermissionError:
            if i < attempts - 1:
                time.sleep(1.5)
    print(f"  ✗ Không xóa được {path.name} (bị process khác giữ — thường là antivirus).")
    print("    → Đóng mọi chương trình đang mở file này, đợi 10 giây rồi chạy lại script.")
    print(f"    → Hoặc xóa tay: {path}")
    sys.exit(1)


# ── Bước 2: tải ────────────────────────────────────────────────────────────
def step_download() -> None:
    print("\n[2/4] Tải LeanDojo Benchmark 4 (68 MB, Zenodo)...")
    if TARBALL.exists():
        actual = sha256_of(TARBALL)
        if actual == EXPECTED_SHA256:
            print(f"  ✓ Đã có tarball đúng checksum — BỎ QUA tải.")
            return
        if TARBALL.stat().st_size < 1_000_000:
            print(f"  ⚠ Tarball cũ quá nhỏ ({TARBALL.stat().st_size} bytes) — có thể là trang lỗi HTML, xóa.")
        else:
            print(f"  ⚠ Tarball cũ checksum KHÁC (network đứt giữa chừng?) — xóa, tải lại.")
        _safe_unlink(TARBALL)

    # Xác nhận file tồn tại trên Zenodo trước khi tải (báo lỗi rõ ràng)
    try:
        req = urllib.request.Request(ZENODO_META_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            meta = json.load(resp)
        f = meta["files"][0]
        print(f"  Zenodo OK: {f['key']} — {f['size']/1e6:.1f} MB (server khẳng định)")
    except Exception as e:
        print(f"  ✗ Không truy cập được Zenodo: {e}")
        print("    → Kiểm tra internet. Nếu vẫn lỗi, tải THỦ CÔNG:")
        print("      1. Mở https://zenodo.org/records/12740403 trong trình duyệt")
        print("      2. Tải file leandojo_benchmark_4.tar.gz")
        print(f"      3. Đặt file vào: {TARBALL.parent}  (tạo thư mục nếu chưa có)")
        print("      4. Chạy lại: python download_data.py  (script sẽ tự nhận file có sẵn)")
        sys.exit(1)

    t0 = time.time()
    req = urllib.request.Request(ZENODO_FILE_URL,
                                 headers={"User-Agent": HEADERS["User-Agent"]})
    tmp = TARBALL.with_suffix(".part")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(req, timeout=590) as resp, open(tmp, "wb") as out:
            total = 0
            next_report = 10 * 1024 * 1024
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                total += len(chunk)
                if total >= next_report:
                    speed = total / max(1e-6, time.time() - t0) / 1e6
                    print(f"    ... {total/1e6:5.1f} MB  ({speed:.1f} MB/s)", flush=True)
                    next_report += 10 * 1024 * 1024
    except KeyboardInterrupt:
        tmp.unlink(missing_ok=True)
        print("  ✗ Bạn đã dừng tải — chạy lại script sẽ tải tiếp từ đầu.")
        sys.exit(1)
    except Exception as e:
        tmp.unlink(missing_ok=True)
        print(f"  ✗ Tải thất bại: {e}")
        print("    File .part rác đã xóa — chạy lại để thử tiếp.")
        sys.exit(1)

    if total != EXPECTED_SIZE:
        tmp.unlink(missing_ok=True)
        print(f"  ✗ Kích thước sai: nhận {total} ≠ {EXPECTED_SIZE} bytes — tải đứt, xóa.")
        print("    Chạy lại script.")
        sys.exit(1)
    actual = sha256_of(tmp)
    if actual != EXPECTED_SHA256:
        tmp.unlink(missing_ok=True)
        print("  ✗ SHA-256 KHÔNG khớp bản gốc — file hỏng, xóa. Chạy lại script.")
        sys.exit(1)

    _move_into_place(tmp)
    print(f"  ✓ Tải xong {total/1e6:.1f} MB trong {time.time()-t0:.0f}s — SHA-256 khớp ✓")


def _move_into_place(tmp: Path) -> None:
    """Đổi tên .part → tên cuối; retry vì Windows có thể khóa file mới tải."""
    for i in range(3):
        try:
            shutil.move(str(tmp), str(TARBALL))
            return
        except PermissionError:
            time.sleep(1.5)
    print(f"  ✗ Không ghi được {TARBALL.name} (file bị giữ). Thử chạy lại script.")
    sys.exit(1)


# ── Bước 3: giải nén + verify ──────────────────────────────────────────────
def step_extract() -> None:
    print("\n[3/4] Giải nén...")
    if all((EXTRACTED / r).exists() for r in REQUIRED_AFTER_EXTRACT):
        print("  ✓ Đã giải nén đầy đủ trước đó — BỎ QUA.")
        return
    if not TARBALL.exists():
        print("  ✗ Không có tarball — chạy lại script (bước 2 sẽ tải).")
        sys.exit(1)
    EXTRACTED.parent.mkdir(parents=True, exist_ok=True)
    import tarfile
    t0 = time.time()
    with tarfile.open(TARBALL, "r:gz") as tf:
        tf.extractall(EXTRACTED.parent)  # noqa: S202 — file từ Zenodo chính thức
    missing = [r for r in REQUIRED_AFTER_EXTRACT if not (EXTRACTED / r).exists()]
    if missing:
        print(f"  ✗ Sau giải nén THIẾU: {missing} — tarball có thể hỏng. Xóa data_raw/ và chạy lại.")
        sys.exit(1)
    print(f"  ✓ Giải nén xong trong {time.time()-t0:.0f}s → {EXTRACTED.name}/")


# ── Bước 4: build ──────────────────────────────────────────────────────────
def step_build() -> None:
    print("\n[4/4] Build corpus + queries + qrels 3 scale...")
    ok = run_py(ROOT / "scripts" / "build_real_corpus.py", "build corpus thật")
    if not ok:
        print("    Đây là bước bắt buộc — không tiếp tục được.")
        sys.exit(1)
    print("\n→ Bổ sung Parquet + data dictionary + index size + repeats...")
    ok = run_py(ROOT / "scripts" / "fill_gaps.py", "fill gaps (Parquet/index/repeats)")
    if not ok:
        print("    ⚠ Bước này chỉ thiếu phần Parquet/index — dữ liệu chính vẫn đủ, tiếp tục.")


def main() -> int:
    print("=" * 60)
    print(" NHÓM 3 — TẢI DỮ LIỆU LeanDojo Benchmark 4")
    print(f" Thư mục làm việc: {ROOT}")
    print(f" Python: {sys.version.split()[0]} ({sys.executable})")
    print("=" * 60)

    for required in ["scripts/build_real_corpus.py", "scripts/fill_gaps.py"]:
        if not (ROOT / required).exists():
            print(f"✗ Thiếu file: {required} — gói nhom3Send chưa copy đủ, kiểm tra lại zip.")
            return 1

    step_deps()
    step_download()
    step_extract()
    step_build()

    print("\n" + "=" * 60)
    print(" ✓ HOÀN TẤT — dữ liệu thật đã sẵn sàng")
    print("=" * 60)
    print(" Xác nhận:  python check_setup.py")
    print(" Demo:      python scripts/search_cli.py \"Every finite integral domain is a field\" --top 5")
    print(" Test:      python tests/test_metrics.py")
    print(" Chạy lại toàn bộ thí nghiệm (~20 phút):")
    print("            python scripts/run_real_retrieval.py")
    print("            python scripts/run_load_test.py")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
