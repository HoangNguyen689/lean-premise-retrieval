"""Run logger - ghi đủ 10 trường theo Phụ lục B của hướng dẫn môn học.

Mọi thí nghiệm (tuần 7+) phải dùng module này để ghi metadata một lần chạy:
run_id, timestamp, git_commit, data_version, machine, software, parameters,
seed/timeout, metrics, status/log.

Ví dụ:

    from run_logger import RunLogger  # type: ignore[import]
    log = RunLogger(parameters={"index": "bm25", "k": 50}, seed=42)
    try:
        ...chạy thí nghiệm...
        log.finish(metrics={"Recall@10": 0.42}, artifacts=["results/raw/run_bm25.csv"])
    except Exception as e:
        log.fail(error=str(e))
    # → results/raw/runs/run_20261001_103000_ab12.json
"""
from __future__ import annotations

import json
import platform
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path


def _git_commit() -> str:
    """Lấy commit hiện tại; trả về 'no-git' nếu thư mục không phải repo."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except Exception:
        pass
    return "no-git"


def machine_info() -> dict:
    return {
        "cpu": platform.processor() or platform.machine(),
        "cores": __import__("os").cpu_count(),
        "ram_gb": round(__import__("os").sysconf("SC_PAGE_SIZE") * __import__("os").sysconf("SC_PHYS_PAGES") / 2**30, 1)
        if hasattr(__import__("os"), "sysconf")
        else None,
        "gpu": None,  # điền tay nếu dùng GPU
        "os": f"{platform.system()} {platform.release()}",
        "hostname": socket.gethostname(),
    }


class RunLogger:
    """Ghi metadata một lần chạy thí nghiệm theo Phụ lục B."""

    def __init__(self, parameters: dict, seed: int | None = None,
                 timeout_s: float | None = None, data_version: str = "mock-v0",
                 out_dir: str | Path | None = None):
        self.started = time.time()
        self.run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        self.record: dict = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "git_commit": _git_commit(),
            "data_version": data_version,
            "machine": machine_info(),
            "software": {
                "python": sys.version.split()[0],
                # thêm lib quan trọng khi có: spark/lean/faiss/...
            },
            "parameters": parameters,
            "seed": seed,
            "timeout_s": timeout_s,
            "status": "running",
            "metrics": {},
            "artifacts": [],
            "error": None,
        }
        self.out_dir = Path(out_dir) if out_dir else Path("results/raw/runs")
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def set_software(self, **versions: str) -> None:
        """Ghi thêm phiên bản phần mềm, vd. set_software(spark='3.5.1')."""
        self.record["software"].update(versions)

    def finish(self, metrics: dict, artifacts: list[str] | None = None) -> Path:
        self.record["metrics"] = metrics
        self.record["artifacts"] = artifacts or []
        self.record["status"] = "success"
        self.record["wall_time_s"] = round(time.time() - self.started, 3)
        return self._write()

    def fail(self, error: str) -> Path:
        self.record["status"] = "failed"
        self.record["error"] = error
        self.record["wall_time_s"] = round(time.time() - self.started, 3)
        return self._write()

    def _write(self) -> Path:
        path = self.out_dir / f"{self.run_id}.json"
        path.write_text(json.dumps(self.record, indent=2, ensure_ascii=False), encoding="utf-8")
        return path
