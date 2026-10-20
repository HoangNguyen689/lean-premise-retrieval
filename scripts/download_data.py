"""Tải LeanDojo Benchmark 4 từ Zenodo, kiểm tra md5, giải nén và ghi manifest.

Dùng:  python scripts/download_data.py [--record 12740403] [--out data/raw]
Dữ liệu lớn không đưa vào Git; chỉ manifest (data/raw/MANIFEST.json) là bằng chứng phiên bản.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import tarfile
import urllib.request
from pathlib import Path

ZENODO_API = "https://zenodo.org/api/records/{record}"
DEFAULT_RECORD = "12740403"  # LeanDojo Benchmark 4 v10 (2024-07-14), CC BY 2.0, tác giả Kaiyu Yang


def md5sum(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", default=DEFAULT_RECORD)
    ap.add_argument("--out", default="data/raw")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(ZENODO_API.format(record=args.record), timeout=60) as r:
        meta = json.load(r)
    (f,) = [x for x in meta["files"] if x["key"].endswith((".tar.gz", ".tgz"))]
    expected_md5 = f["checksum"].split(":", 1)[1]
    tarball = out / f["key"]

    if not tarball.exists() or md5sum(tarball) != expected_md5:
        print(f"Đang tải {f['key']} ({f['size'] / 1e6:.1f} MB) ...")
        urllib.request.urlretrieve(f["links"]["self"], tarball)
    actual_md5 = md5sum(tarball)
    if actual_md5 != expected_md5:
        raise SystemExit(f"Sai md5: {actual_md5} != {expected_md5}")
    print("md5 khớp:", actual_md5)

    extract_dir = out / f"leandojo_benchmark_4_v{meta['metadata'].get('version', 'x').lstrip('v')}"
    if not extract_dir.exists():
        with tarfile.open(tarball) as tf:
            tf.extractall(extract_dir, filter="data")  # filter='data' chặn đường dẫn nguy hiểm
    files = [
        {"path": str(p.relative_to(extract_dir)).replace("\\", "/"), "bytes": p.stat().st_size, "md5": md5sum(p)}
        for p in sorted(extract_dir.rglob("*")) if p.is_file()
    ]

    manifest = {
        "dataset": meta["metadata"]["title"],
        "version": meta["metadata"].get("version"),
        "publication_date": meta["metadata"].get("publication_date"),
        "creators": [c.get("name") for c in meta["metadata"].get("creators", [])],
        "license": (meta["metadata"].get("license") or {}).get("id"),
        "zenodo_record": args.record,
        "doi": meta.get("doi"),
        "source_url": f["links"]["self"],
        "archive": {"file": f["key"], "bytes": f["size"], "md5": expected_md5},
        "downloaded_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "extract_dir": str(extract_dir).replace("\\", "/"),
        "files": files,
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã giải nén {len(files)} tệp vào {extract_dir}; manifest: {out / 'MANIFEST.json'}")


if __name__ == "__main__":
    main()
