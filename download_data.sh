#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

PY=""
for p in python3 python py; do
    if command -v "$p" >/dev/null 2>&1; then
        if "$p" -c "print(1)" >/dev/null 2>&1; then
            PY="$p"
            break
        fi
    fi
done
if [ -z "$PY" ]; then
    echo "Python not found."
    exit 1
fi

echo "→ Run: $PY download_data.py"
exec "$PY" download_data.py
