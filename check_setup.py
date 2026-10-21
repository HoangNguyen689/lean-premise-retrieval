#!/usr/bin/env python3
"""Smoke-test script: verify the local environment is ready to run Lean Premise Retrieval.

Checks:
  - Python version and SSL support
  - Required project files
  - Python dependencies (pyarrow, pandas, matplotlib)
  - Dataset download/build status
  - Unit tests and search CLI smoke test
"""
from __future__ import annotations

import csv
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


def run_with_retry(cmd: list[str], *, delay: float = 2.0) -> subprocess.CompletedProcess[str]:
    """Run a command; on first failure wait and retry once."""
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    if r.returncode != 0:
        time.sleep(delay)
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    return r


def print_tail(proc: subprocess.CompletedProcess[str], prefix: str = "      | ") -> None:
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-8:]
    for line in tail:
        print(f"{prefix}{line}")


def main() -> int:
    print("=" * 60)
    print(" Environment Check - Lean Premise Retrieval")
    print("=" * 60)

    # ── 1. Python ──
    print("\n[1] Python")
    v = sys.version_info
    report(OK if v >= (3, 8) else FAIL,
           f"Python {v.major}.{v.minor}.{v.micro} ({sys.executable})",
           "install Python 3.8+ from python.org")
    try:
        import ssl  # noqa: F401
        report(OK, "ssl module available (HTTPS downloads work)")
    except ImportError:
        report(FAIL, "ssl module missing",
               "reinstall Python with SSL support from python.org")

    # ── 2. Project files ──
    print("\n[2] Required project files")
    required = {
        "download_data.py": "data download script",
        "scripts/build_real_corpus.py": "corpus builder",
        "scripts/fill_gaps.py": "Parquet + index manifest",
        "scripts/run_real_retrieval.py": "retrieval runner (4 systems × 3 scales)",
        "scripts/run_load_test.py": "load test",
        "scripts/search_cli.py": "search CLI demo",
        "src/evaluation/metrics.py": "evaluation metrics",
        "src/retrieval/systems.py": "retrieval systems",
        "tests/test_metrics.py": "unit tests",
        "results/real/qrels_s3.csv": "ground-truth qrels",
        "docs/report_draft.md": "report draft",
    }
    for rel, desc in required.items():
        status = OK if (ROOT / rel).exists() else FAIL
        report(status, f"{rel} — {desc}",
               "missing file — re-download the project archive")

    print("\n[2b] Generated artifacts (optional until you run retrieval)")
    generated = {
        "results/real/eval_summary.csv": "evaluation summary",
        "results/real/run_hybrid_s3.csv": "hybrid run file",
    }
    for rel, desc in generated.items():
        status = OK if (ROOT / rel).exists() else WARN
        report(status, f"{rel} — {desc}",
               "run: python scripts/run_real_retrieval.py")

    # ── 3. Python libraries ──
    print("\n[3] Python libraries")
    for mod in ["pyarrow", "pandas", "matplotlib"]:
        try:
            m = importlib.import_module(mod)
            report(OK, f"{mod} {getattr(m, '__version__', '?')}")
        except ImportError:
            if mod == "matplotlib":
                report(FAIL, f"{mod} (plotting)", "pip install matplotlib")
            else:
                report(WARN, f"{mod} (Parquet support; CSV still works)",
                       "pip install pyarrow pandas")

    # ── 4. Data ──
    print("\n[4] Data (LeanDojo Benchmark 4)")
    tarball = ROOT / "data_raw" / "leandojo_benchmark_4.tar.gz"
    extracted = ROOT / "data_raw" / "leandojo_benchmark_4"
    corpus_s3 = ROOT / "results" / "real" / "corpus_s3.csv"
    if corpus_s3.exists():
        with open(corpus_s3, encoding="utf-8") as f:
            n_records = sum(1 for _ in csv.DictReader(f))
        report(OK, f"corpus built: results/real/corpus_s3.csv ({n_records:,} declarations)")
    elif extracted.exists() and (extracted / "corpus.jsonl").exists():
        report(WARN, "extracted but corpus not built yet",
               "run: python download_data.py")
    elif tarball.exists():
        report(WARN, "tarball downloaded but not extracted",
               "run: python download_data.py")
    else:
        report(WARN, "no dataset found (normal right after cloning)",
               "run: python download_data.py (~10 min, downloads from Zenodo)")

    # ── 5. Smoke tests ──
    print("\n[5] Smoke tests")
    metrics_test = run_with_retry([sys.executable, str(ROOT / "tests" / "test_metrics.py")])
    if metrics_test.returncode == 0:
        report(OK, "unit tests metrics passed")
    else:
        report(FAIL, "unit tests metrics failed after retry")
        print_tail(metrics_test)
        problems.append("unit tests metrics failed — see details above")

    if corpus_s3.exists():
        query = "Every finite integral domain is a field"
        cli_test = run_with_retry([
            sys.executable, str(ROOT / "scripts" / "search_cli.py"),
            query, "--top", "3",
        ])
        if cli_test.returncode == 0:
            report(OK, "search CLI works (corpus is operational)")
        else:
            report(FAIL, "search CLI failed after retry")
            print_tail(cli_test)
            problems.append("search CLI failed — see details above")
    else:
        report(WARN, "search CLI not tested (no corpus yet)",
               "run download_data.py, then re-run this check")

    # ── Summary ──
    print("\n" + "=" * 60)
    if not problems:
        print(" ✓ Environment ready — try the demo:")
        print('    python scripts/search_cli.py "Every finite integral domain is a field" --top 5')
    else:
        print(f" {len(problems)} issue(s) to fix:")
        for p in problems:
            print(f"   • {p}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
