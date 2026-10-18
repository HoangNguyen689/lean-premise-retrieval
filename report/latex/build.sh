#!/usr/bin/env bash
# Sinh lại bảng (scripts/make_report_tables.py) và hình cho báo cáo rồi biên dịch main.tex; chép PDF ra report/report.pdf.
# Dùng Tectonic nếu có (biến TECTONIC hoặc trong PATH), không thì dùng xelatex.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$(cd ../.. && pwd)
PY=$ROOT/.venv/Scripts/python; [ -x "$PY" ] || PY=$ROOT/.venv/bin/python
export PYTHONIOENCODING=utf-8
(cd "$ROOT" && "$PY" scripts/make_report_tables.py && "$PY" scripts/running_example.py > /dev/null \
  && "$PY" scripts/make_figures.py --report)

TECTONIC=${TECTONIC:-$(command -v tectonic || true)}
if [ -n "$TECTONIC" ]; then
  "$TECTONIC" -X compile main.tex
else
  xelatex -interaction=nonstopmode main.tex > /dev/null
  xelatex -interaction=nonstopmode main.tex > /dev/null
fi
cp main.pdf ../report.pdf
echo "Xong: report/report.pdf"
