#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import STEP_10_V39_DISCOVERY_SPEC as spec

BASE = Path(__file__).resolve().parent
ASSIGN = BASE / "STEP_10_CLUSTER_ASSIGNMENTS.tsv"
OUT_JSON = BASE / "STEP_10_V39_DISCOVERY_LEDGER_GATE.json"


def effective_cluster(row: dict[str, str]) -> str:
    return row.get("cluster_id", "") or ("SEARCH_REQUIRED" if row.get("cluster_evidence_state") == "SEARCH_REQUIRED" else "")


def main() -> None:
    with ASSIGN.open("r", encoding="utf-8", newline="") as f:
        assignments = list(csv.DictReader(f, delimiter="\t"))
    amap = {r["phrase"]: r for r in assignments}

    failures = []
    for expected in spec.ROWS:
        phrase = expected["phrase"]
        row = amap.get(phrase)
        if row is None:
            failures.append({"phrase": phrase, "failure": "MISSING_ASSIGNMENT"})
            continue
        observed_cluster = effective_cluster(row)
        observed_state = row.get("cluster_evidence_state", "")
        if observed_cluster != expected["proposed_cluster_id"] or observed_state != expected["proposed_evidence_state"]:
            failures.append({
                "phrase": phrase,
                "failure": "TARGET_MISMATCH",
                "expected_cluster": expected["proposed_cluster_id"],
                "observed_cluster": observed_cluster,
                "expected_state": expected["proposed_evidence_state"],
                "observed_state": observed_state,
                "assignment_reason": row.get("assignment_reason", ""),
            })
        if row.get("step09_probe_id", ""):
            failures.append({
                "phrase": phrase,
                "failure": "UNEXPECTED_DIRECT_SERP_ON_FROZEN_MANUAL_ROW",
                "step09_probe_id": row.get("step09_probe_id", ""),
            })

    root_counts = Counter(r["root_cause"] for r in spec.ROWS)
    summary = {
        "status": "PASS" if not failures else "FAIL__V39_FROZEN_LEDGER_RESIDUALS",
        "v38_full_manual_error_rows": len(spec.ROWS),
        "unique_phrases": len({r['phrase'] for r in spec.ROWS}),
        "root_cause_counts": dict(sorted(root_counts.items())),
        "direct_step09_rows_in_frozen_ledger": sum(bool(r.get("step09_probe_id")) for r in spec.ROWS),
        "v39_resolution_failures": len(failures),
        "failures": failures,
        "meaning": "All 22 errors found by the complete persisted-V38 manual re-audit are checked together. No frozen row may borrow direct Step-09 evidence.",
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for failure in failures:
        print("V39_DISCOVERY_LEDGER_FAIL", json.dumps(failure, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(f"V39 frozen manual ledger gate failed: {len(failures)} residuals")


if __name__ == "__main__":
    main()
