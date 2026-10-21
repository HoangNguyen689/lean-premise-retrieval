"""Data contract loader + validator cho Nhóm 3.

TV1 (Data/Extraction) dùng hàm `validate_contract` để kiểm tra corpus/query
trước khi giao cho TV2/TV3. TV6 dùng để kiểm tra qrels trước khi chấm điểm.

Contract: docs/data_contract_v1.md — 6 field bắt buộc.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_FIELDS = ["id", "statement", "statement_natural", "namespace", "file_path", "line_start"]
OPTIONAL_FIELDS = ["premises", "commit"]


@dataclass
class ValidationError:
    """Một vi phạm contract."""

    file: str
    row: int  # 0 = lỗi mức tệp (header), ≥1 = lỗi dòng
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.file} dòng {self.row} [{self.field}]: {self.message}"


@dataclass
class ContractReport:
    """Kết quả kiểm tra contract cho một tệp."""

    path: str
    n_rows: int
    errors: list[ValidationError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def summary(self) -> str:
        status = "PASS" if self.ok else f"FAIL ({len(self.errors)} lỗi)"
        return f"{self.path}: {self.n_rows} dòng — {status}"


def validate_csv(path: str | Path, artifact: str = "corpus") -> ContractReport:
    """Kiểm tra một tệp CSV theo contract v1.

    artifact: 'corpus' | 'queries' | 'qrels' — quy định field bắt buộc.
    """
    path = Path(path)
    report = ContractReport(path=str(path), n_rows=0)
    if not path.exists():
        report.errors.append(ValidationError(str(path), 0, "*", "Tệp không tồn tại"))
        return report

    required = list(REQUIRED_FIELDS)
    if artifact == "qrels":
        required = ["query_id", "premise_id", "relevance"]
    elif artifact == "run":
        required = ["query_id", "premise_id"]

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        missing = [c for c in required if c not in header]
        if missing:
            report.errors.append(
                ValidationError(str(path), 0, "header", f"Thiếu cột bắt buộc: {missing}")
            )
            return report
        for i, row in enumerate(reader, start=2):
            report.n_rows += 1
            for col in required:
                if col in ("statement_natural", "namespace"):
                    continue  # được phép rỗng (namespace rỗng = declaration cấp root trong Lean)
                val = (row.get(col) or "").strip()
                if not val:
                    report.errors.append(
                        ValidationError(str(path), i, col, "Giá trị rỗng")
                    )
                elif col == "line_start":
                    try:
                        if int(val) < 1:
                            raise ValueError
                    except ValueError:
                        report.errors.append(
                            ValidationError(str(path), i, col, f"line_start không hợp lệ: {val!r}")
                        )
    return report


def validate_all(data_dir: str | Path, scale: str = "s1") -> list[ContractReport]:
    """Kiểm tra bộ artifact của một mức scale: corpus, queries, qrels."""
    d = Path(data_dir)
    return [
        validate_csv(d / f"corpus_{scale}.csv", "corpus"),
        validate_csv(d / f"queries_{scale}.csv", "queries"),
        validate_csv(d / f"qrels_{scale}.csv", "qrels"),
    ]
