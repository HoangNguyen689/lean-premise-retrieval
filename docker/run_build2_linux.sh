#!/usr/bin/env bash
# Chạy phần build2 của scripts/run_scale.py trong container Linux.
# Mã và dữ liệu được chép vào ổ của container (/work) vì đọc ghi qua thư mục chia sẻ với Windows chậm hơn nhiều
# và sẽ làm sai số đo. Run record và log được chép ngược về repo khi chạy xong.
# Tham số truyền thẳng cho run_scale.py, ví dụ: --reps 3 --sizes full,x5,x20 --indexes lean --masters 4,8
set -euo pipefail
SRC=/repo
W=/work
mkdir -p "$W/data/processed/subsets" "$W/data/processed/synthetic" "$W/data/raw" "$W/results/raw/build"
cp -r "$SRC/src" "$SRC/scripts" "$SRC/pyproject.toml" "$W/"
cp "$SRC/data/raw/MANIFEST.json" "$W/data/raw/"
cp "$SRC/data/processed/premises.parquet" "$W/data/processed/"
cp "$SRC"/data/processed/subsets/*.npy "$W/data/processed/subsets/"
cp "$SRC"/data/processed/synthetic/premises_x*.parquet "$W/data/processed/synthetic/"
cd "$W"
export PYTHONPATH="$W/src" N3_PY=python N3_PY_SPARK=python PYTHONIOENCODING=utf-8
python scripts/run_scale.py --part build2 "$@"
cp results/raw/build/*.json "$SRC/results/raw/build/"
mkdir -p "$SRC/results/logs/scale"
cp results/logs/scale/* "$SRC/results/logs/scale/" 2>/dev/null || true
echo "Xong: đã chép run record về $SRC/results/raw/build"
