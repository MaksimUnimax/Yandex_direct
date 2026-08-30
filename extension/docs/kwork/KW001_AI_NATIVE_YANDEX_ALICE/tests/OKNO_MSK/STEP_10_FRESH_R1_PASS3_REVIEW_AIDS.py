#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FULL = ROOT / "STEP_10_FRESH_R1_PASS3_FULL_REVIEW.tsv"
QA = ROOT / "STEP_10_FRESH_R1_PASS3_QA.json"
OUT_COMPACT = ROOT / "STEP_10_FRESH_R1_PASS3_ERROR_REVIEW_PACK.tsv"
OUT_DIRECT = ROOT / "STEP_10_FRESH_R1_PASS3_DIRECT_CONFLICTS.tsv"
OUT_UNRESOLVED = ROOT / "STEP_10_FRESH_R1_PASS3_UNRESOLVED.tsv"
OUT_SAMPLES = ROOT / "STEP_10_FRESH_R1_PASS3_TRANSITION_SAMPLES.tsv"


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    with FULL.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    qa = json.loads(QA.read_text(encoding="utf-8"))
    if len(rows) != 2332 or qa["pass3_rows_reviewed"] != 2332:
        raise RuntimeError(f"expected 2332 full-review rows, got rows={len(rows)} qa={qa['pass3_rows_reviewed']}")

    compact_fields = [
        "error_seq", "qa_row", "phrase", "pass2_assignment_status", "pass2_cluster_id",
        "audit_expected_status", "audit_cluster_id", "audit_rule", "error_class",
    ]
    compact: list[dict[str, str]] = []
    direct: list[dict[str, str]] = []
    unresolved: list[dict[str, str]] = []
    grouped: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)

    error_seq = 0
    for row in rows:
        if row["error_class"]:
            error_seq += 1
            item = {field: row.get(field, "") for field in compact_fields}
            item["error_seq"] = str(error_seq)
            compact.append(item)
            key = (
                row["pass2_assignment_status"], row["pass2_cluster_id"],
                row["audit_expected_status"], row["audit_cluster_id"], row["error_class"],
            )
            grouped[key].append(row)
            if row["error_class"].startswith("DIRECT_SERP_"):
                direct.append(item)
        if row["review_outcome"] == "PASS2_NOT_CONFIRMED_REQUIRES_ADJUDICATION":
            unresolved.append({field: row.get(field, "") for field in compact_fields if field != "error_seq"})

    sample_fields = [
        "pass2_assignment_status", "pass2_cluster_id", "audit_expected_status", "audit_cluster_id",
        "error_class", "transition_count", "sample_rank", "qa_row", "phrase", "audit_rule",
    ]
    samples: list[dict[str, str]] = []
    for key, members in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        for rank, row in enumerate(members[:5], 1):
            samples.append({
                "pass2_assignment_status": key[0],
                "pass2_cluster_id": key[1],
                "audit_expected_status": key[2],
                "audit_cluster_id": key[3],
                "error_class": key[4],
                "transition_count": str(len(members)),
                "sample_rank": str(rank),
                "qa_row": row["qa_row"],
                "phrase": row["phrase"],
                "audit_rule": row["audit_rule"],
            })

    if len(compact) != qa["pass3_error_rows"]:
        raise RuntimeError(f"error count mismatch: pack={len(compact)} qa={qa['pass3_error_rows']}")
    if len(direct) != qa["direct_assignment_conflicts_found"]:
        raise RuntimeError(f"direct conflict mismatch: pack={len(direct)} qa={qa['direct_assignment_conflicts_found']}")
    if len(unresolved) != qa["pass3_unresolved_adjudication_rows"]:
        raise RuntimeError(f"unresolved mismatch: pack={len(unresolved)} qa={qa['pass3_unresolved_adjudication_rows']}")

    write_tsv(OUT_COMPACT, compact_fields, compact)
    write_tsv(OUT_DIRECT, compact_fields, direct)
    write_tsv(OUT_UNRESOLVED, [f for f in compact_fields if f != "error_seq"], unresolved)
    write_tsv(OUT_SAMPLES, sample_fields, samples)
    print(f"PASS3_ERROR_REVIEW_PACK={len(compact)}")
    print(f"PASS3_DIRECT_CONFLICTS={len(direct)}")
    print(f"PASS3_UNRESOLVED={len(unresolved)}")
    print(f"PASS3_TRANSITION_SAMPLES={len(samples)}")


if __name__ == "__main__":
    main()
