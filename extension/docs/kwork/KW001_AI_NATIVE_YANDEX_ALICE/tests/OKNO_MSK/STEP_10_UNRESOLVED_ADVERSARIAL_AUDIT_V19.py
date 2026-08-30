#!/usr/bin/env python3
from __future__ import annotations

import csv
import json

import STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT as old
import STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT_V15 as v15


def main() -> None:
    # Generate the strengthened V15 unresolved audit first; V19 turns every remaining
    # non-intentional flag into a hard workflow failure so a green workflow can no
    # longer coexist with known likely-false SEARCH_REQUIRED rows.
    v15.main()
    summary = json.loads(old.OUT_JSON.read_text(encoding="utf-8"))

    with old.OUT.open("r", encoding="utf-8", newline="") as f:
        flagged = list(csv.DictReader(f, delimiter="\t"))

    v19_summary = dict(summary)
    v19_summary["audit_version"] = "V19"
    v19_summary["status"] = "PASS" if not flagged else "FAIL__LIKELY_FALSE_UNRESOLVED_REMAIN"
    v19_summary["meaning"] = "V19 hard gate over strengthened unresolved audit. Zero likely-false unresolved rows is necessary but still not sufficient for final manual semantic acceptance."
    old.OUT_JSON.write_text(json.dumps(v19_summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if flagged:
        for row in flagged:
            print("V19_UNRESOLVED_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(v19_summary, ensure_ascii=False, indent=2))
    if flagged:
        raise SystemExit("V19 unresolved hard gate failed")


if __name__ == "__main__":
    main()
