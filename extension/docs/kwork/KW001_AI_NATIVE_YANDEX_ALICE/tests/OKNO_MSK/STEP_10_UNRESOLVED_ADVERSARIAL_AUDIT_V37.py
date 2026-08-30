#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT as old
import STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT_V15 as v15


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


# These two phrases were inspected in the full V33 manual-QA pass and deliberately
# left SEARCH_REQUIRED in V34. They are not semantically determinate enough for a
# stable Step-10 cluster without additional boundary evidence.
REVIEWED_MIXED_BOUNDARIES = {
    "окна сок панорамное раздвижное остекление": {
        "audit_code": "UNRESOLVED_CLEAR_SPECIFIC_WINDOW_PRODUCT",
        "assignment_reason": "Brand/abbreviation plus panoramic sliding-glazing wording is not safe product-versus-service evidence",
    },
    "установка окон и остекление балконов": {
        "audit_code": "UNRESOLVED_CLEAR_OBJECT_GLAZING",
        "assignment_reason": "Phrase combines two material services and should not be forced into one task without boundary evidence",
    },
}


def main() -> None:
    # Rebuild the inherited unresolved audit deterministically, then adjudicate
    # only exact phrase+code pairs whose current assignment still matches the
    # manually reviewed SEARCH_REQUIRED state and reason.
    v15.main()
    inherited = json.loads(old.OUT_JSON.read_text(encoding="utf-8"))

    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        assignments = {n(r.get("phrase", "")): r for r in csv.DictReader(f, delimiter="\t")}

    with old.OUT.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    residual = []
    adjudicated_no_glazing = []
    adjudicated_mixed = []

    for row in rows:
        p = n(row.get("phrase", ""))
        code = row.get("audit_code", "")

        # Preserve V27's existing manual adjudication: explicit negation of a
        # glazing service is not a false unresolved merely because 'остекление'
        # appears lexically.
        if code == "UNRESOLVED_CLEAR_OBJECT_GLAZING" and "без остеклен" in p:
            adjudicated_no_glazing.append(row)
            continue

        reviewed = REVIEWED_MIXED_BOUNDARIES.get(p)
        assignment = assignments.get(p, {})
        if reviewed and code == reviewed["audit_code"]:
            current_state_ok = assignment.get("cluster_evidence_state") == "SEARCH_REQUIRED"
            current_role_ok = assignment.get("cluster_role") == "UNRESOLVED"
            current_reason_ok = assignment.get("assignment_reason") == reviewed["assignment_reason"]
            current_search_flag_ok = assignment.get("additional_search_required") == "true"
            if current_state_ok and current_role_ok and current_reason_ok and current_search_flag_ok:
                adjudicated_mixed.append({
                    **row,
                    "assignment_reason": assignment.get("assignment_reason", ""),
                })
                continue

        residual.append(row)

    with old.OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(residual)

    counts = Counter(r.get("audit_code", "") for r in residual)
    summary = dict(inherited)
    summary.update({
        "status": "PASS" if not residual else "FAIL__LIKELY_FALSE_UNRESOLVED_REMAIN",
        "audit_version": "V37",
        "flagged_rows": len({r.get("phrase", "") for r in residual}),
        "flagged_records": len(residual),
        "audit_counts": dict(sorted((k, v) for k, v in counts.items() if k)),
        "manually_adjudicated_no_glazing_rows": len(adjudicated_no_glazing),
        "manually_adjudicated_no_glazing_examples": [r.get("phrase", "") for r in adjudicated_no_glazing[:10]],
        "manually_adjudicated_mixed_boundary_rows": len(adjudicated_mixed),
        "manually_adjudicated_mixed_boundary_examples": [
            {
                "phrase": r.get("phrase", ""),
                "audit_code": r.get("audit_code", ""),
                "assignment_reason": r.get("assignment_reason", ""),
            }
            for r in adjudicated_mixed
        ],
        "adjudication_rule": "Only exact reviewed phrase+audit-code pairs are suppressed, and only while the generated row remains UNRESOLVED/SEARCH_REQUIRED with the exact manually approved assignment_reason and additional_search_required=true. Any semantic/state/reason drift or any new inherited unresolved flag remains blocking.",
        "meaning": "V37 preserves the unresolved hard gate while recognizing two manually verified mixed boundaries that genuinely require additional Search evidence rather than forced semantic clustering. Zero residual flags is necessary but not sufficient for final manual semantic acceptance.",
    })
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if residual:
        for row in residual:
            print("V37_UNRESOLVED_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if residual:
        raise SystemExit("V37 unresolved hard gate failed")


if __name__ == "__main__":
    main()
