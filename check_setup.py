#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_setup.py — Kiểm tra một lệnh: máy này đã sẵn sàng chạy dự án Nhóm 3 chưa.

Chạy ở bất cứ đâu, bất cứ lúc nào (cả TRƯỚC khi tải dữ liệu):

    python check_setup.py

Báo cáo từng hạng mục ✓/⚠/✗ kèm CÁCH SỬA cụ thể nếu thiếu. Lỗi thường gặp:
  - Python giả Microsoft Store → chạy script này bằng `py check_setup.py`
  - Thiếu pyarrow/pandas → pip install pyarrow pandas
  - Chưa tải dataset → python download_data.py
"""
from __future__ import annotations

import importlib
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

OK, WARN, FAIL = "✓", "⚠", "✗"
problems: list[str] = []


def report(status: str, msg: str, fix: str = "") -> None:
    print(f"  {status} {msg}")
    if status == FAIL and msg not in problems:
        problems.append(f"{msg}" + (f" → {fix}" if fix else ""))


def main() -> int:
    print("=" * 60)
    print(" KIỂM TRA MÁY CHẠY DỰ ÁN NHÓM 3 — Lean Premise Retrieval")
    print("=" * 60)

    # ── 1. Python ──
    print("\n[1] Python")
    v = sys.version_info
    report(OK if v >= (3, 8) else FAIL,
           f"Python {v.major}.{v.minor}.{v.micro} ({sys.executable})",
           "cài Python 3.8+ từ python.org")
    try:
        import ssl  # noqa: F401
        report(OK, "module ssl khả dụng (tải HTTPS từ Zenodo được)")
    except ImportError:
        report(FAIL, "không có module ssl", "Python bị build thiếu ssl — cài lại từ python.org")

    # ── 2. File dự án ──
    print("\n[2] File dự án (gói nhom3Send đủ chưa)")
    required = {
        "download_data.py": "script tải dữ liệu",
        "scripts/build_real_corpus.py": "build corpus",
        "scripts/fill_gaps.py": "Parquet + index manifest",
        "scripts/run_real_retrieval.py": "chạy 4 hệ × 3 scale",
        "scripts/run_load_test.py": "load test",
        "scripts/search_cli.py": "CLI demo",
        "src/evaluation/metrics.py": "thang chấm TV6",
        "src/retrieval/systems.py": "máy tìm kiếm",
        "tests/test_metrics.py": "unit tests",
        "results/real/eval_summary.csv": "kết quả đã chạy sẵn",
        "results/real/qrels_s3.csv": "đáp án",
        "results/real/run_hybrid_s3.csv": "run file hybrid",
        "docs/report_draft.md": "báo cáo v1.0",
    }
    for rel, desc in required.items():
        report((ROOT / rel).exists() and OK or FAIL, f"{rel} — {desc}",
               "zip thiếu file — tải lại nhom3Send.zip")

    # ── 3. Thư viện Python ──
    print("\n[3] Thư viện Python")
    for mod in ["pyarrow", "pandas", "matplotlib"]:
        try:
            m = importlib.import_module(mod)
            report(OK, f"{mod} {getattr(m, '__version__', '?')}")
        except ImportError:
            if mod == "matplotlib":
                report(FAIL, f"{mod} (vẽ biểu đồ)", "pip install matplotlib")
            else:
                report(WARN, f"{mod} (chỉ cần cho Parquet; CSV vẫn dùng được)",
                       "pip install pyarrow pandas")

    # ── 4. Dữ liệu ──
    print("\n[4] Dữ liệu thật (LeanDojo Benchmark 4)")
    tarball = ROOT / "data_raw" / "leandojo_benchmark_4.tar.gz"
    extracted = ROOT / "data_raw" / "leandojo_benchmark_4"
    corpus_s3 = ROOT / "results" / "real" / "corpus_s3.csv"
    if corpus_s3.exists():
        import csv as _csv
        with open(corpus_s3, encoding="utf-8") as f:
            n_records = sum(1 for _ in _csv.DictReader(f))  # đếm record, không phải dòng vật lý
        report(OK, f"corpus đã build: results/real/corpus_s3.csv ({n_records:,} declarations)")
    elif extracted.exists() and (extracted / "corpus.jsonl").exists():
        report(WARN, "đã giải nén nhưng CHƯA build corpus",
               "python download_data.py  (sẽ chạy lại bước build)")
    elif tarball.exists():
        report(WARN, "đã tải tarball nhưng chưa giải nén",
               "python download_data.py")
    else:
        report(WARN, "CHƯA có dataset (bình thường nếu vừa giải nén zip)",
               "python download_data.py  (~10 phút, tự tải từ Zenodo)")

    # ── 5. Thử chạy từng chức năng ──
    print("\n[5] Smoke test chức năng")
    r = subprocess.run([sys.executable, str(ROOT / "tests" / "test_metrics.py")],
                       capture_output=True, text=True, cwd=str(ROOT))
    if r.returncode == 0 and "15 PASS, 0 FAIL" in r.stdout:
        report(OK, "unit tests metrics: 15/15 PASS")
    else:
        # thử lại 1 lần (lỗi tạm thời: antivirus/file lock ngay sau khi tải)
        time.sleep(2)
        r = subprocess.run([sys.executable, str(ROOT / "tests" / "test_metrics.py")],
                           capture_output=True, text=True, cwd=str(ROOT))
        if r.returncode == 0 and "15 PASS, 0 FAIL" in r.stdout:
            report(OK, "unit tests metrics: 15/15 PASS (thành công ở lần thử lại 2 — lần 1 lỗi tạm thời)")
        else:
            report(FAIL, "unit tests metrics thất bại 2 lần — lỗi thật, chi tiết:")
            tail = (r.stdout + r.stderr).strip().splitlines()[-8:]
            for line in tail:
                print(f"      | {line}")
            problems.append("unit tests metrics thất bại — xem chi tiết ở trên")

    if corpus_s3.exists():
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "search_cli.py"),
                            "Every finite integral domain is a field", "--top", "3"],
                           capture_output=True, text=True, cwd=str(ROOT))
        if r.returncode == 0:
            report(OK, "search CLI chạy được (corpus hoạt động)")
        else:
            time.sleep(2)
            r = subprocess.run([sys.executable, str(ROOT / "scripts" / "search_cli.py"),
                                "Every finite integral domain is a field", "--top", "3"],
                               capture_output=True, text=True, cwd=str(ROOT))
            if r.returncode == 0:
                report(OK, "search CLI chạy được (thành công ở lần thử lại 2 — lần 1 lỗi tạm thời)")
            else:
                report(FAIL, "search CLI lỗi 2 lần — chi tiết:")
                tail = (r.stdout + r.stderr).strip().splitlines()[-8:]
                for line in tail:
                    print(f"      | {line}")
                problems.append("search CLI lỗi — xem chi tiết ở trên")
    else:
        report(WARN, "search CLI chưa thử được (chưa có corpus)",
               "chạy download_data.py xong rồi chạy lại check này")

    # ── Tổng kết ──
    print("\n" + "=" * 60)
    if not problems:
        print(" ✓ MỌI THỨ SẴN SÀNG — chạy demo:")
        print('    python scripts/search_cli.py "Every finite integral domain is a field" --top 5')
    else:
        print(f" CẦN XỬ LÝ {len(problems)} VIỆC:")
        for p in problems:
            print(f"   • {p}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
