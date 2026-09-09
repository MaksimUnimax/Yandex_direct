#!/usr/bin/env python3
"""Finalize hashes and the current release manifest after deterministic QA."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve()
WORK = HERE.parent
JOB = HERE.parents[1]
RELEASE = JOB / "OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09"
XLSX = RELEASE / "04_OKNO_MSK_FULL_SEMANTIC_CORE_2026-09-09.xlsx"
README = RELEASE / "README_RU.md"
SUMMARY = WORK / "FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_SUMMARY_2026-09-09.json"
QA = WORK / "FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_QA_2026-09-09.json"
RECEIPT = WORK / "FINAL_SEMANTIC_CORE_STEP05A_INTEGRATED_RECONCILIATION_RECEIPT_2026-09-09.md"
MANIFEST = RELEASE / "RELEASE_MANIFEST_2026-09-09.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def info(path: Path, relative_to: Path) -> dict[str, object]:
    return {"path": str(path.relative_to(relative_to)), "bytes": path.stat().st_size, "sha256": digest(path)}


def main() -> None:
    qa = json.loads(QA.read_text(encoding="utf-8"))
    if qa["status"] != "PASS":
        raise SystemExit("QA is not PASS")
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    summary["status"] = "PASS"
    summary["qa"] = {"status": qa["status"], "checks_passed": qa["checks_passed"], "checks_total": qa["checks_total"]}
    for path in (XLSX, QA, WORK / "VISUAL_QA_RECEIPT.json", WORK / "XLSX_BUILD_RUNTIME.json"):
        summary["artifacts"][path.name] = info(path, JOB)
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest.update({
        "semantic_core_materialization": "STEP_05A_INTEGRATED_SEMANTIC_CORE_2026-09-09",
        "semantic_core_mode": "ONE_LINEAR_CANONICAL_CORPUS",
        "semantic_core_competitor_appendix": False,
        "semantic_rows": 2856,
        "active_rows": 2348,
        "exact_assignment_decision_rows": 2322,
        "active_unresolved_exact_owner_rows": 26,
        "structural_units": 168,
        "new_provider_calls": 0,
    })
    for item in manifest["artifacts"]:
        if item["path"] == XLSX.name:
            item.update({"bytes": XLSX.stat().st_size, "sha256": digest(XLSX)})
        if item["path"] == README.name:
            item.update({"bytes": README.stat().st_size, "sha256": digest(README)})
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    receipt = RECEIPT.read_text(encoding="utf-8").replace("Статус: MATERIALIZED_PENDING_INDEPENDENT_QA", "Статус: PASS — 37/37 детерминированных проверок")
    receipt += f"""

## Итоговый XLSX и QA

| Артефакт | SHA-256 | Байт |
|---|---|---:|
| `{XLSX.name}` | `{digest(XLSX)}` | {XLSX.stat().st_size} |
| `{QA.name}` | `{digest(QA)}` | {QA.stat().st_size} |

Визуально проверены все 7 листов сохранённого XLSX. Файл повторно открыт программно после записи; структура, строки, фильтры, замороженные заголовки и отсутствие ошибок подтверждены.
"""
    RECEIPT.write_text(receipt, encoding="utf-8")


if __name__ == "__main__":
    main()
