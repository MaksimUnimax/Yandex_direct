#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V36 as v36
import STEP_10_V38_DISCOVERY_SPEC as spec

ACTIVE = {"CORE_CANDIDATE", "REVIEW_SEARCH"}

# These codes are lexical-vocabulary checks from inherited audits. They may be
# suppressed only for an exact phrase whose V38 target was manually frozen in the
# 85-row discovery ledger and only while the generated cluster equals that target.
# Any other code, phrase or target remains blocking.
V38_ADJUDICATED_INHERITED_CODES = {
    "TASK_TOKEN_MISMATCH",
    "PANORAMIC_WITHOUT_PURCHASE_SIGNAL",
    "REPAIR_TOKEN_MISMATCH",
}


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


FROZEN_TARGET = {
    n(row["phrase"]): row["proposed_cluster_id"]
    for row in spec.ROWS
    if row["proposed_cluster_id"] != "SEARCH_REQUIRED"
}


def reviewed_v38_false_positive(code: str, r: dict[str, str]) -> bool:
    expected = FROZEN_TARGET.get(n(r.get("phrase", "")))
    if not expected or r.get("cluster_id", "") != expected:
        return False
    return code in V38_ADJUDICATED_INHERITED_CODES


def audit_v38(r: dict[str, str]):
    raw = list(v36.audit_v36(r))
    return [(code, reason) for code, reason in raw if not reviewed_v38_false_positive(code, r)]


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    suppressed = []
    for r in rows:
        if r.get("input_disposition") not in ACTIVE:
            continue
        raw = list(v36.audit_v36(r))
        for code, reason in raw:
            if reviewed_v38_false_positive(code, r):
                suppressed.append({"phrase": r.get("phrase", ""), "cluster_id": r.get("cluster_id", ""), "collision_code": code})
                continue
            counts[code] += 1
            flagged.append({
                "collision_code": code,
                "phrase": r.get("phrase", ""),
                "cluster_id": r.get("cluster_id", ""),
                "user_task": r.get("user_task", ""),
                "evidence_state": r.get("cluster_evidence_state", ""),
                "step09_probe_id": r.get("step09_probe_id", ""),
                "reason": reason,
            })

    fields = ["collision_code", "phrase", "cluster_id", "user_task", "evidence_state", "step09_probe_id", "reason"]
    with old.OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)

    summary = {
        "status": "PASS" if not flagged else "FAIL__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V38",
        "active_rows_scanned": sum(r.get("input_disposition") in ACTIVE for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "v38_frozen_discovery_rows": len(spec.ROWS),
        "suppressed_exact_inherited_records": len(suppressed),
        "suppressed_exact_inherited_examples": suppressed[:30],
        "adjudication_rule": "Suppression requires exact frozen phrase + exact manually approved V38 target + one of three inherited lexical codes. Any new code, phrase or changed target remains a hard failure.",
        "meaning": "Inherited lexical audit vocabulary is retained as an adversarial signal, but it cannot veto exact full-manual-discovery corrections merely because its token dictionary predates those reviewed tasks. Zero residual flags remains necessary but not sufficient for final semantic acceptance.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for row in flagged:
        print("V38_COLLISION_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if flagged:
        raise SystemExit(f"V38 semantic collision gate failed with {len(flagged)} residual records")


if __name__ == "__main__":
    main()
