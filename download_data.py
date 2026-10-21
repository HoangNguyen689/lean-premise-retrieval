#!/usr/bin/env python3
"""Prepare the LeanDojo Benchmark 4 dataset: download, extract, and build.

This script downloads and also builds corpus/queries/qrels
and generates Parquet/index files. Each step is resumable.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# Windows consoles often use cp1252/cp437; force UTF-8 so Unicode symbols print correctly.
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# ── Constants ──────────────────────────────────────────────────────────────
ZENODO_RECORD = "12740403"
ZENODO_META_URL = f"https://zenodo.org/api/records/{ZENODO_RECORD}"
ZENODO_FILE_URL = (
    f"https://zenodo.org/api/records/{ZENODO_RECORD}"
    f"/files/leandojo_benchmark_4.tar.gz/content"
)
EXPECTED_SHA256 = "19b9a31968229d5bae4b959be9351d92740643d16a58c7f58f6d82795b8a98a4"
EXPECTED_SIZE = 68141936  # bytes
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json",
}

ROOT = Path(__file__).resolve().parent
TARBALL = ROOT / "data_raw" / "leandojo_benchmark_4.tar.gz"
EXTRACTED = ROOT / "data_raw" / "leandojo_benchmark_4"

REQUIRED_AFTER_EXTRACT = [
    "metadata.json",
    "corpus.jsonl",
    "random/test.json",
    "random/train.json",
    "random/val.json",
]


# ── Helpers ─────────────────────────────────────────────────────────────────
def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_unlink(path: Path, attempts: int = 3) -> None:
    """Delete a file, retrying on Windows if antivirus/file lock holds it."""
    for i in range(attempts):
        try:
            path.unlink()
            return
        except PermissionError:
            if i < attempts - 1:
                time.sleep(1.5)
    print(f"  ✗ Could not delete {path.name} (held by another process, often antivirus).")
    print("    → Close any program using this file, wait 10 seconds, and rerun.")
    print(f"    → Or delete it manually: {path}")
    sys.exit(1)


def move_into_place(tmp: Path, target: Path) -> None:
    """Rename .part file to final name; retry on Windows file locks."""
    for _ in range(3):
        try:
            shutil.move(str(tmp), str(target))
            return
        except PermissionError:
            time.sleep(1.5)
    print(f"  ✗ Could not write {target.name} (file is locked). Try rerunning the script.")
    sys.exit(1)


def run_py(script: Path, what: str) -> bool:
    """Run a child script with the current interpreter."""
    print(f"\n→ {what}: python {script.name}")
    r = subprocess.run([sys.executable, str(script)], cwd=str(ROOT))
    if r.returncode != 0:
        print(f"✗ {what} failed (exit {r.returncode}). See errors above.")
        return False
    return True


def print_manual_download_instructions() -> None:
    print("    → Check your internet connection. If the error persists, download manually:")
    print("      1. Open https://zenodo.org/records/12740403 in your browser")
    print("      2. Download leandojo_benchmark_4.tar.gz")
    print(f"      3. Place it in: {TARBALL.parent}  (create the folder if needed)")
    print("      4. Rerun: python download_data.py  (the script will detect the existing file)")


# ── Steps ───────────────────────────────────────────────────────────────────
def step_deps() -> None:
    print("\n[1/4] Checking libraries (pyarrow, pandas)...")
    if importlib.util.find_spec("pyarrow") and importlib.util.find_spec("pandas"):
        print("  ✓ pyarrow + pandas found — Parquet files will be generated.")
    else:
        print("  ⚠ pyarrow/pandas missing — trying pip install...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "pyarrow", "pandas"])
        if r.returncode == 0:
            print("  ✓ Installation complete.")
        else:
            print("  ⚠ Installation failed. CSV files will still be built; only Parquet is skipped.")
            print("    (The assignment requires Parquet — install manually: pip install pyarrow pandas)")


def verify_zenodo_file() -> dict:
    """Confirm the file exists on Zenodo and return metadata."""
    try:
        req = urllib.request.Request(ZENODO_META_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as resp:
            meta = json.load(resp)
        f = meta["files"][0]
        print(f"  Zenodo OK: {f['key']} — {f['size'] / 1e6:.1f} MB (confirmed by server)")
        return meta
    except Exception as e:
        print(f"  ✗ Cannot reach Zenodo: {e}")
        print_manual_download_instructions()
        sys.exit(1)


def download_tarball() -> None:
    """Download the tarball with progress reporting and integrity checks."""
    print("\n[2/4] Downloading LeanDojo Benchmark 4 (68 MB, Zenodo)...")
    if TARBALL.exists():
        actual = sha256_of(TARBALL)
        if actual == EXPECTED_SHA256:
            print("  ✓ Tarball already present and checksum matches — skipping download.")
            return
        if TARBALL.stat().st_size < 1_000_000:
            print(f"  ⚠ Existing tarball too small ({TARBALL.stat().st_size} bytes) — likely an error page, deleting.")
        else:
            print("  ⚠ Existing tarball checksum mismatch (network interrupted?) — deleting and re-downloading.")
        safe_unlink(TARBALL)

    verify_zenodo_file()

    t0 = time.time()
    req = urllib.request.Request(
        ZENODO_FILE_URL,
        headers={"User-Agent": HEADERS["User-Agent"]},
    )
    tmp = TARBALL.with_suffix(".part")
    tmp.parent.mkdir(parents=True, exist_ok=True)

    total = 0
    try:
        with urllib.request.urlopen(req, timeout=590) as resp, open(tmp, "wb") as out:
            next_report = 10 * 1024 * 1024
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
                total += len(chunk)
                if total >= next_report:
                    speed = total / max(1e-6, time.time() - t0) / 1e6
                    print(f"    ... {total / 1e6:5.1f} MB  ({speed:.1f} MB/s)", flush=True)
                    next_report += 10 * 1024 * 1024
    except KeyboardInterrupt:
        tmp.unlink(missing_ok=True)
        print("  ✗ Download cancelled by user — rerun to start from the beginning.")
        sys.exit(1)
    except Exception as e:
        tmp.unlink(missing_ok=True)
        print(f"  ✗ Download failed: {e}")
        print("    Partial .part file removed — rerun to retry.")
        sys.exit(1)

    if total != EXPECTED_SIZE:
        tmp.unlink(missing_ok=True)
        print(f"  ✗ Size mismatch: received {total} ≠ {EXPECTED_SIZE} bytes — download incomplete, removed.")
        print("    Rerun the script to retry.")
        sys.exit(1)

    actual = sha256_of(tmp)
    if actual != EXPECTED_SHA256:
        tmp.unlink(missing_ok=True)
        print("  ✗ SHA-256 mismatch — file corrupted, removed. Rerun the script to retry.")
        sys.exit(1)

    move_into_place(tmp, TARBALL)
    print(f"  ✓ Downloaded {total / 1e6:.1f} MB in {time.time() - t0:.0f}s — SHA-256 matches ✓")


def step_extract() -> None:
    print("\n[3/4] Extracting...")
    if all((EXTRACTED / r).exists() for r in REQUIRED_AFTER_EXTRACT):
        print("  ✓ Already fully extracted — skipping.")
        return
    if not TARBALL.exists():
        print("  ✗ Tarball missing — rerun the script (step 2 will download it).")
        sys.exit(1)
    EXTRACTED.parent.mkdir(parents=True, exist_ok=True)
    import tarfile

    t0 = time.time()
    with tarfile.open(TARBALL, "r:gz") as tf:
        tf.extractall(EXTRACTED.parent)  # noqa: S202 — official Zenodo archive
    missing = [r for r in REQUIRED_AFTER_EXTRACT if not (EXTRACTED / r).exists()]
    if missing:
        print(f"  ✗ Missing after extraction: {missing} — tarball may be corrupt. Delete data_raw/ and rerun.")
        sys.exit(1)
    print(f"  ✓ Extracted in {time.time() - t0:.0f}s → {EXTRACTED.name}/")


def step_build() -> None:
    print("\n[4/4] Building corpus + queries + qrels for 3 scales...")
    if not run_py(ROOT / "scripts" / "build_real_corpus.py", "build real corpus"):
        print("    This step is required — cannot continue.")
        sys.exit(1)
    print("\n→ Adding Parquet + data dictionary + index size + repeats...")
    if not run_py(ROOT / "scripts" / "fill_gaps.py", "fill gaps (Parquet/index/repeats)"):
        print("    ⚠ This step only affects Parquet/index files; core CSV data is complete.")


# ── Entry point ─────────────────────────────────────────────────────────────
def main() -> int:
    print("=" * 60)
    print(" Download LeanDojo Benchmark 4")
    print(f" Working directory: {ROOT}")
    print(f" Python: {sys.version.split()[0]} ({sys.executable})")
    print("=" * 60)

    for required in ["scripts/build_real_corpus.py", "scripts/fill_gaps.py"]:
        if not (ROOT / required).exists():
            print(f"✗ Missing file: {required} — project archive is incomplete.")
            return 1

    step_deps()
    download_tarball()
    step_extract()
    step_build()

    print("\n" + "=" * 60)
    print(" ✓ Done — real data is ready")
    print("=" * 60)
    print(" Verify:   python check_setup.py")
    print(' Demo:     python scripts/search_cli.py "Every finite integral domain is a field" --top 5')
    print(" Test:     python tests/test_metrics.py")
    print(" Full run:")
    print("           python scripts/run_real_retrieval.py")
    print("           python scripts/run_load_test.py")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
