#!/usr/bin/env bash
# Dựng báo cáo: report/latex/main.tex -> report/report.pdf. Dùng Tectonic nếu có (biến TECTONIC, trong PATH hoặc
# tools/tectonic/ của kho), không thì dùng xelatex. Biến PYTHON chọn trình thông dịch (mặc định .venv của kho mã).
#
#   bash build.sh                  kiểm tra đầu vào khớp bản đã phát hành (SHA-256 trong tables/ và figures/SOURCES.md),
#                                  sinh lại bảng, ví dụ và hình rồi biên dịch; dừng nếu đầu vào lệch
#   bash build.sh --compile-only   chỉ biên dịch LaTeX từ bảng và hình đã có trong kho
#   bash build.sh --update         chủ ý cập nhật báo cáo bằng đầu vào hiện tại (bỏ bước kiểm tra), ghi lại SOURCES.md
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$(cd ../.. && pwd)
PY=${PYTHON:-$ROOT/.venv/Scripts/python}; [ -x "$PY" ] || PY=$ROOT/.venv/bin/python
export PYTHONIOENCODING=utf-8
MODE=${1:-}

if [ "$MODE" != "--compile-only" ]; then
  if [ "$MODE" != "--update" ]; then
    (cd "$ROOT" && "$PY" scripts/verify_report_inputs.py) || {
      echo "Đầu vào khác bản đã phát hành. Dùng --compile-only để dựng đúng bản phát hành, hoặc --update để cập nhật." >&2
      exit 1
    }
  fi
  (cd "$ROOT" && "$PY" scripts/make_report_tables.py && "$PY" scripts/running_example.py > /dev/null \
    && "$PY" scripts/make_figures.py --report)
fi

TECTONIC=${TECTONIC:-$(command -v tectonic || true)}
[ -n "$TECTONIC" ] || for t in "$ROOT/tools/tectonic/tectonic.exe" "$ROOT/tools/tectonic/tectonic"; do [ -x "$t" ] && TECTONIC=$t && break; done
if [ -n "$TECTONIC" ]; then
  "$TECTONIC" -X compile main.tex
else
  xelatex -interaction=nonstopmode main.tex > /dev/null
  xelatex -interaction=nonstopmode main.tex > /dev/null
fi
cp main.pdf ../report.pdf
echo "Xong: report/report.pdf"
