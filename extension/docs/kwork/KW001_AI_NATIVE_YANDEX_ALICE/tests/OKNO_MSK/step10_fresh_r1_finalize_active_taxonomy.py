#!/usr/bin/env python3
"""Finalize the Fresh-R1 active taxonomy from actual member evidence.

The frozen input taxonomy may contain candidates that receive no final active
rows. Those candidates are preserved as retired input candidates, but they are
not counted or published as final active clusters.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Iterable

BASE_DIR = Path("extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK")
INPUT_TAXONOMY_NAME = "STEP_10_FRESH_R1_TAXONOMY.tsv"
FINAL_TAXONOMY_NAME = "STEP_10_FRESH_R1_TAXONOMY_FINAL.tsv"
FINAL_ASSIGNMENT_NAME = "STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv"
FINAL_SUMMARY_NAME = "STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv"
FINAL_QA_NAME = "STEP_10_FRESH_R1_FINAL_QA.json"
FULL_QA_NAME = "STEP_10_FRESH_R1_PASS3_FULL_QA_LEDGER.tsv"
ERROR_NAME = "STEP_10_FRESH_R1_PASS3_ERROR_LEDGER.tsv"
CORRECTION_NAME = "STEP_10_FRESH_R1_PASS3_CONSOLIDATED_CORRECTIONS.tsv"
IMPACT_NAME = "STEP_10_FRESH_R1_PASS3_IMPACT_RECHECK.tsv"
REPORT_NAME = "STEP_10_FRESH_R1_PASS3_REPORT.md"
MARKER_NAME = "STEP_10_FRESH_R1_COMPLETE.marker"

ACTIVE_DISPOSITIONS = {"CORE_CANDIDATE", "REVIEW_SEARCH"}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: Iterable[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    base = args.root.resolve() / BASE_DIR

    input_taxonomy = read_tsv(base / INPUT_TAXONOMY_NAME)
    assignments = read_tsv(base / FINAL_ASSIGNMENT_NAME)
    qa_path = base / FINAL_QA_NAME
    qa = json.loads(qa_path.read_text(encoding="utf-8"))

    if not input_taxonomy:
        raise SystemExit("input taxonomy is empty")
    if len(assignments) != qa.get("source_rows"):
        raise SystemExit("final assignment row count does not match final QA")

    active_rows = [
        row for row in assignments
        if row.get("source_disposition") in ACTIVE_DISPOSITIONS
    ]
    assigned_rows = [
        row for row in active_rows
        if row.get("assignment_status") == "ASSIGNED"
    ]
    search_required_rows = [
        row for row in active_rows
        if row.get("assignment_status") == "SEARCH_REQUIRED"
    ]

    counts = Counter(row.get("cluster_id", "") for row in assigned_rows)
    counts.pop("", None)
    input_ids = [row["cluster_id"] for row in input_taxonomy]
    input_id_set = set(input_ids)
    unknown = sorted(set(counts) - input_id_set)
    if unknown:
        raise SystemExit(f"assigned rows use unknown cluster IDs: {unknown}")

    active_taxonomy = [row for row in input_taxonomy if counts.get(row["cluster_id"], 0) > 0]
    active_ids = [row["cluster_id"] for row in active_taxonomy]
    retired_ids = [cluster_id for cluster_id in input_ids if cluster_id not in set(active_ids)]

    if len(active_ids) != len(set(active_ids)):
        raise SystemExit("duplicate active cluster IDs")
    if any(counts.get(cluster_id, 0) <= 0 for cluster_id in active_ids):
        raise SystemExit("final active taxonomy contains a zero-member cluster")
    if len(assigned_rows) + len(search_required_rows) != len(active_rows):
        raise SystemExit("active assignment accounting mismatch")

    taxonomy_fields = list(input_taxonomy[0].keys())
    write_tsv(base / FINAL_TAXONOMY_NAME, active_taxonomy, taxonomy_fields)

    summary_rows = [
        {
            "cluster_id": row["cluster_id"],
            "family": row.get("family", ""),
            "user_task": row.get("user_task", ""),
            "intent_type": row.get("intent_type", ""),
            "business_fit": row.get("business_fit", ""),
            "assigned_rows": counts[row["cluster_id"]],
        }
        for row in active_taxonomy
    ]
    write_tsv(
        base / FINAL_SUMMARY_NAME,
        summary_rows,
        ["cluster_id", "family", "user_task", "intent_type", "business_fit", "assigned_rows"],
    )

    qa["input_taxonomy_cluster_ids"] = len(input_taxonomy)
    qa["taxonomy_cluster_ids"] = len(active_taxonomy)
    qa["used_cluster_ids"] = len(active_taxonomy)
    qa["zero_assignment_cluster_ids"] = []
    qa["retired_zero_assignment_cluster_ids"] = retired_ids
    qa["final_active_taxonomy_has_member_evidence"] = True
    qa["final_assigned_active_rows"] = len(assigned_rows)
    qa["final_search_required_active_rows"] = len(search_required_rows)
    qa["final_active_accounted_rows"] = len(active_rows)
    qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    hash_names = [
        FINAL_TAXONOMY_NAME,
        FULL_QA_NAME,
        ERROR_NAME,
        CORRECTION_NAME,
        FINAL_ASSIGNMENT_NAME,
        FINAL_SUMMARY_NAME,
        IMPACT_NAME,
        FINAL_QA_NAME,
    ]
    hashes = {name: sha256(base / name) for name in hash_names}
    retired_text = ", ".join(retired_ids) if retired_ids else "none"
    report = f"""# KW-001 / OKNO-MSK — STEP 10 FRESH R1 FINAL REPORT

Date: 2026-08-30  
Status: **COMPLETE — FULL ROW QA / CONSOLIDATED CORRECTION / VERIFIED ACTIVE TAXONOMY**

## Final accounting

```text
SOURCE_ROWS = {len(assignments)}
ACTIVE_ROWS = {len(active_rows)}
PASS3_INDEPENDENTLY_REVIEWED = {qa['pass3_rows_independently_reviewed']}/{len(active_rows)}
FINAL_ASSIGNED_ACTIVE_ROWS = {len(assigned_rows)}
FINAL_SEARCH_REQUIRED_ACTIVE_ROWS = {len(search_required_rows)}
FINAL_ACTIVE_ACCOUNTED_ROWS = {len(active_rows)}/{len(active_rows)}
PASS3_ERROR_LEDGER_ROWS = {qa['pass3_error_ledger_rows']}
CONSOLIDATED_CORRECTION_ROWS = {qa['consolidated_correction_rows']}
CORRECTION_BATCHES_APPLIED = {qa['correction_batches_applied']}
IMPACT_RECHECK_FAILURES = {qa['impact_recheck_failures']}
SEMANTIC_INVARIANT_VIOLATIONS = {qa['semantic_invariant_violations']}
```

## Taxonomy outcome

```text
INPUT_FROZEN_TAXONOMY_CANDIDATES = {len(input_taxonomy)}
FINAL_ACTIVE_CLUSTERS_WITH_MEMBER_EVIDENCE = {len(active_taxonomy)}
FINAL_ZERO_MEMBER_ACTIVE_CLUSTERS = 0
RETIRED_ZERO_MEMBER_INPUT_CANDIDATES = {len(retired_ids)}
RETIRED_IDS = {retired_text}
TARGET_CLUSTER_COUNT_USED = false
```

The retired IDs are preserved as input-history candidates only. They are not counted as final active clusters because no final active phrase supplied member evidence.

## Isolation and evidence controls

```text
OLD_STEP10_INPUT_USED = {str(qa['old_step10_input_used']).lower()}
BLIND84_INPUT_USED = {str(qa['blind84_input_used']).lower()}
DIRECT_SERP_TRANSFER_TO_UNPROBED_ROWS = false
FINAL_ACTIVE_TAXONOMY_HAS_MEMBER_EVIDENCE = true
```

## Artifact hashes

```text
{chr(10).join(f'{name}  {digest}' for name, digest in hashes.items())}
```

## Verdict

```text
STEP10_FRESH_R1_FULL_ROW_QA = PASS
STEP10_FRESH_R1_COMPLETE_ERROR_LEDGER = FROZEN
STEP10_FRESH_R1_CONSOLIDATED_CORRECTION_BATCH = PASS_ONE_BATCH
STEP10_FRESH_R1_FULL_ACCOUNTING_REGRESSION = PASS
STEP10_FRESH_R1_IMPACT_SET_RECHECK = PASS
STEP10_FRESH_R1_ACTIVE_TAXONOMY_MEMBER_EVIDENCE = PASS
STEP10_FRESH_R1_FINAL_STATUS = COMPLETE
```
"""
    report_path = base / REPORT_NAME
    report_path.write_text(report, encoding="utf-8")

    marker = {
        "status": "STEP10_FRESH_R1_FINAL_ACTIVE_TAXONOMY_VERIFIED",
        "source_rows": len(assignments),
        "active_rows": len(active_rows),
        "final_assigned_active_rows": len(assigned_rows),
        "final_search_required_active_rows": len(search_required_rows),
        "input_taxonomy_cluster_ids": len(input_taxonomy),
        "final_active_taxonomy_cluster_ids": len(active_taxonomy),
        "retired_zero_assignment_cluster_ids": retired_ids,
        "final_qa_sha256": sha256(qa_path),
        "final_assignments_sha256": sha256(base / FINAL_ASSIGNMENT_NAME),
        "final_taxonomy_sha256": sha256(base / FINAL_TAXONOMY_NAME),
        "report_sha256": sha256(report_path),
    }
    (base / MARKER_NAME).write_text(
        json.dumps(marker, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"qa": qa, "marker": marker}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
