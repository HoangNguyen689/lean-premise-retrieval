"""Ghim các lần chạy đánh giá dùng cho bản báo cáo vào một manifest cố định.

Bảng của báo cáo đọc run_id từ manifest này thay vì "lần chạy mới nhất", nên một lần chạy phát sinh sau đó không làm bảng
thay đổi ngoài ý muốn. Chỉ chạy lại script này khi chủ ý cập nhật bản báo cáo.

Dùng:  python scripts/pin_runs.py
Ra:    results/figures/report_manifest.json  {"<hệ thống>|<tập đánh giá>": {run_id, per_query_file, run_file, metrics...}}
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEMS = ["B0", "B0t", "V1", "V2", "V2a", "V3", "V4", "V5", "V4-K240", "V2-nons", "V4-poponly", "V4-pronly"]
EVALS = ["random_val_all", "random_test_all", "novel_premises_test_all", "random_holdoutB"]


def main() -> None:
    latest: dict[str, dict] = {}
    for f in (ROOT / "results" / "raw" / "eval").glob("*.json"):
        r = json.loads(f.read_text(encoding="utf-8"))
        prm = r["parameters"]
        name, ev = prm["config"]["name"], prm["eval_set"]
        if name not in SYSTEMS or ev not in EVALS or prm.get("subset", "full") != "full":
            continue
        key = f"{name}|{ev}"
        if key not in latest or r["timestamp"] > latest[key]["timestamp"]:
            latest[key] = {"run_id": r["run_id"], "timestamp": r["timestamp"], "tag": prm.get("tag"),
                           "per_query_file": r.get("per_query_file"), "run_file": r.get("run_file"),
                           "code_hash": r.get("code_hash"),
                           "metrics": {k: r["metrics"][k] for k in ("R@1", "R@5", "R@10", "R@50", "MRR", "nDCG@10",
                                                                    "latency_ms_p95", "n_queries")}}
    out = ROOT / "results" / "figures" / "report_manifest.json"
    out.write_text(json.dumps(dict(sorted(latest.items())), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(latest)} lần chạy được ghim vào {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
