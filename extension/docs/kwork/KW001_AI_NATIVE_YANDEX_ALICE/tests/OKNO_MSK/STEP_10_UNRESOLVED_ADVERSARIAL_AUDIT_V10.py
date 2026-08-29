#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT as old


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    unresolved = 0
    intentionally_mixed_direct = []

    for r in rows:
        if r["cluster_evidence_state"] != "SEARCH_REQUIRED":
            continue
        unresolved += 1

        # Exact direct SERP may legitimately remain unresolved only when the direct
        # evidence itself is explicitly mixed/ambiguous. Keep that visible as a
        # reviewed note rather than mislabel it as a likely missing semantic class.
        direct_is_explicitly_mixed = bool(
            r["step09_probe_id"]
            and (r["dominant_result_type"].startswith("MIXED_") or "AMBIGUOUS" in r["step09_handoff"])
            and any(x in r["assignment_reason"].casefold() for x in ("mixed", "ambiguous", "неоднознач", "boundary"))
        )
        if direct_is_explicitly_mixed:
            intentionally_mixed_direct.append({
                "phrase": r["phrase"],
                "probe_id": r["step09_probe_id"],
                "dominant_result_type": r["dominant_result_type"],
                "step09_handoff": r["step09_handoff"],
            })

        for code, reason in old.audit_unresolved(r):
            if code == "DIRECT_SERP_LEFT_UNRESOLVED" and direct_is_explicitly_mixed:
                continue
            counts[code] += 1
            flagged.append({
                "audit_code": code,
                "phrase": r["phrase"],
                "step09_probe_id": r["step09_probe_id"],
                "observed_serp_job": r["observed_serp_job"],
                "dominant_result_type": r["dominant_result_type"],
                "reason": reason,
            })

    fields = ["audit_code", "phrase", "step09_probe_id", "observed_serp_job", "dominant_result_type", "reason"]
    with old.OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)

    summary = {
        "status": "AUDIT_GENERATED__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V10",
        "search_required_rows_scanned": unresolved,
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "audit_counts": dict(sorted(counts.items())),
        "intentionally_mixed_direct_rows": len(intentionally_mixed_direct),
        "intentionally_mixed_direct_examples": intentionally_mixed_direct,
        "meaning": "Likely false SEARCH_REQUIRED states are flagged; direct rows remain unresolved without a flag only when the direct Step-09 evidence is itself explicitly mixed/ambiguous.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
