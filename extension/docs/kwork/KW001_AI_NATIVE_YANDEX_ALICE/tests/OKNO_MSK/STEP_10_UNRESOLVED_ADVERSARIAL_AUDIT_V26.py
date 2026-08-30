#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT as old
import STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT_V15 as v15


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def main() -> None:
    # Generate the strongest inherited unresolved audit, then adjudicate only the
    # semantic negation class established in V26: 'без остекления' cannot be
    # treated as a clear positive glazing-service task merely because the object
    # and the token 'остекление' are present.
    v15.main()
    inherited = json.loads(old.OUT_JSON.read_text(encoding="utf-8"))

    with old.OUT.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
        fieldnames = list(f.fieldnames or [])

    residual = []
    adjudicated = []
    for row in rows:
        p = n(row.get("phrase", ""))
        if row.get("audit_code") == "UNRESOLVED_CLEAR_OBJECT_GLAZING" and "без остеклен" in p:
            adjudicated.append(row)
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
        "audit_version": "V26",
        "flagged_rows": len({r.get("phrase", "") for r in residual}),
        "flagged_records": len(residual),
        "audit_counts": dict(sorted((k, v) for k, v in counts.items() if k)),
        "manually_adjudicated_no_glazing_rows": len(adjudicated),
        "manually_adjudicated_no_glazing_examples": [r.get("phrase", "") for r in adjudicated[:10]],
        "meaning": "V26 hard gate treats explicit 'без остекления' as semantic negation of a glazing service. All other inherited likely-false SEARCH_REQUIRED flags remain blocking. Zero residual flags is necessary but not sufficient for final manual semantic acceptance.",
    })
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if residual:
        for row in residual:
            print("V26_UNRESOLVED_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if residual:
        raise SystemExit("V26 unresolved hard gate failed")


if __name__ == "__main__":
    main()
