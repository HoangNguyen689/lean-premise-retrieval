#!/usr/bin/env bash
# ============================================================================
# download_data.sh — WRAPPER MỎNG gọi download_data.py (logic chính ở đó)
# ============================================================================
# Nếu máy không có bash (CMD/PowerShell trên Windows), chạy trực tiếp:
#
#     python download_data.py
#
# File này chỉ dành cho ai quen dùng Git Bash / Linux / macOS.
# ============================================================================
cd "$(dirname "$0")"

# Tìm Python chạy được thật (tránh stub giả Microsoft Store trên Windows)
PY=""
for cand in python3 python py; do
    if command -v "$cand" >/dev/null 2>&1; then
        if "$cand" -c "print(1)" >/dev/null 2>&1; then
            PY="$cand"
            break
        fi
    fi
done
if [ -z "$PY" ]; then
    echo "✗ Không tìm thấy Python chạy được."
    echo "  Windows: cài từ python.org (tick 'Add to PATH'), hoặc chạy:"
    echo "    py download_data.py"
    exit 1
fi

echo "→ Chạy: $PY download_data.py"
exec "$PY" download_data.py
