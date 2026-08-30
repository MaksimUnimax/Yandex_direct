#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import STEP_10_V38_DISCOVERY_SPEC as spec

BASE = Path(__file__).resolve().parent
ASSIGN = BASE / "STEP_10_CLUSTER_ASSIGNMENTS.tsv"
OUT = BASE / "STEP_10_V37_FULL_MANUAL_ERROR_LEDGER.tsv"
OUT_JSON = BASE / "STEP_10_V38_DISCOVERY_LEDGER_GATE.json"


def main() -> None:
    with ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    by_phrase = {r["phrase"]: r for r in rows}

    ledger = []
    failures = []
    root_counts = Counter()
    for frozen in spec.ROWS:
        phrase = frozen["phrase"]
        root_counts[frozen["root_cause"]] += 1
        observed = by_phrase.get(phrase)
        if not observed:
            result = "FAIL_MISSING_PHRASE"
            observed_cluster = ""
            observed_state = ""
            observed_reason = ""
        else:
            observed_cluster = observed.get("cluster_id", "") or "SEARCH_REQUIRED"
            observed_state = observed.get("cluster_evidence_state", "")
            observed_reason = observed.get("assignment_reason", "")
            expected_cluster = frozen["proposed_cluster_id"]
            cluster_ok = observed_cluster == expected_cluster
            if expected_cluster == "SEARCH_REQUIRED":
                state_ok = observed_state == "SEARCH_REQUIRED" and observed.get("additional_search_required") == "true"
            else:
                state_ok = observed_state in {"SEMANTIC_SUPPORTED_NO_DIRECT_SERP", "SERP_SUPPORTED"}
            result = "PASS" if cluster_ok and state_ok else "FAIL"

        record = {
            "phrase": phrase,
            "v37_cluster_id": frozen["v37_cluster_id"],
            "v37_evidence_state": frozen["v37_evidence_state"],
            "root_cause": frozen["root_cause"],
            "proposed_cluster_id": frozen["proposed_cluster_id"],
            "proposed_evidence_state": frozen["proposed_evidence_state"],
            "manual_qa_rationale": frozen["manual_qa_rationale"],
            "v38_observed_cluster_id": observed_cluster,
            "v38_observed_evidence_state": observed_state,
            "v38_observed_reason": observed_reason,
            "resolution_result": result,
        }
        ledger.append(record)
        if result != "PASS":
            failures.append(record)

    fields = list(ledger[0].keys())
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(ledger)

    summary = {
        "status": "PASS" if not failures else "FAIL__V38_DISCOVERY_ERRORS_REMAIN",
        "v37_full_manual_error_rows": len(spec.ROWS),
        "unique_phrases": len({r["phrase"] for r in spec.ROWS}),
        "root_cause_counts": dict(sorted(root_counts.items())),
        "direct_step09_rows_in_frozen_ledger": 0,
        "v38_resolution_failures": len(failures),
        "meaning": "This is the frozen full V37 discovery ledger plus V38 observed resolution. All 85 errors are checked in one pass; the gate reports every residual failure before exiting.",
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for row in failures:
        print("V38_DISCOVERY_LEDGER_FAIL", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(f"V38 discovery-ledger gate failed with {len(failures)} residual errors")


if __name__ == "__main__":
    main()
