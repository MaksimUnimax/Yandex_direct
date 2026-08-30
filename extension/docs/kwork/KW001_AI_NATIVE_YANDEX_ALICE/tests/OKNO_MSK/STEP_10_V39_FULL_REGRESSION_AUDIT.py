#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import json
import subprocess
from pathlib import Path

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V39 as v39  # installs V39 classifier
import STEP_10_V39_DISCOVERY_SPEC as spec

BASE = Path(__file__).resolve().parent
ASSIGN = BASE / "STEP_10_CLUSTER_ASSIGNMENTS.tsv"
OUT = BASE / "STEP_10_V39_FULL_REGRESSION_AUDIT.tsv"
OUT_JSON = BASE / "STEP_10_V39_FULL_REGRESSION_AUDIT.json"
V38_BASELINE_COMMIT = "d33a203a8eb4293f53198db02b28ec6257840034"
REPO_REL_ASSIGN = "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_CLUSTER_ASSIGNMENTS.tsv"

SEMANTIC_FIELDS = (
    "cluster_id",
    "cluster_evidence_state",
    "user_task",
    "intent_orientation",
    "public_business_fit",
    "additional_search_required",
)


def read_tsv_text(text: str):
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


def frozen_v38_rows():
    proc = subprocess.run(
        ["git", "show", f"{V38_BASELINE_COMMIT}:{REPO_REL_ASSIGN}"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    return read_tsv_text(proc.stdout)


def current_v39_rows():
    with ASSIGN.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def effective_cluster(row):
    return row.get("cluster_id", "") or ("SEARCH_REQUIRED" if row.get("cluster_evidence_state") == "SEARCH_REQUIRED" else "")


def main() -> None:
    baseline = frozen_v38_rows()
    current = current_v39_rows()
    assert len(baseline) == 2840, len(baseline)
    assert len(current) == 2840, len(current)
    bmap = {r["phrase"]: r for r in baseline}
    cmap = {r["phrase"]: r for r in current}
    assert set(bmap) == set(cmap)

    frozen = spec.EXPECTED_BY_PHRASE
    failures = []
    approved_changes = []

    for phrase in sorted(bmap, key=b.norm):
        before = bmap[phrase]
        after = cmap[phrase]
        diffs = {
            field: (before.get(field, ""), after.get(field, ""))
            for field in SEMANTIC_FIELDS
            if before.get(field, "") != after.get(field, "")
        }
        if not diffs:
            continue

        if phrase in frozen:
            expected_cluster = frozen[phrase]["proposed_cluster_id"]
            expected_state = frozen[phrase]["proposed_evidence_state"]
            observed_cluster = effective_cluster(after)
            observed_state = after.get("cluster_evidence_state", "")
            if observed_cluster == expected_cluster and observed_state == expected_state:
                approved_changes.append({
                    "phrase": phrase,
                    "expected": expected_cluster,
                    "observed": observed_cluster,
                    "changed_fields": ";".join(sorted(diffs)),
                })
                continue

        failures.append({
            "comparison_kind": "UNPLANNED_V38_TO_V39_CHANGE" if phrase not in frozen else "FROZEN_V39_TARGET_MISMATCH",
            "phrase": phrase,
            "expected": frozen.get(phrase, {}).get("proposed_cluster_id", effective_cluster(before)),
            "observed": effective_cluster(after),
            "expected_state": frozen.get(phrase, {}).get("proposed_evidence_state", before.get("cluster_evidence_state", "")),
            "observed_state": after.get("cluster_evidence_state", ""),
            "source_file": V38_BASELINE_COMMIT,
            "observed_reason": after.get("assignment_reason", ""),
            "changed_fields": ";".join(sorted(diffs)),
        })

    # Every frozen manual-QA correction must actually produce a semantic change.
    approved_phrases = {r["phrase"] for r in approved_changes}
    for phrase, target in frozen.items():
        if phrase in approved_phrases:
            continue
        after = cmap[phrase]
        expected_cluster = target["proposed_cluster_id"]
        expected_state = target["proposed_evidence_state"]
        if effective_cluster(after) != expected_cluster or after.get("cluster_evidence_state", "") != expected_state:
            # Already represented above when there was a diff; add only if missing.
            if not any(r["phrase"] == phrase for r in failures):
                failures.append({
                    "comparison_kind": "FROZEN_V39_TARGET_NOT_REALIZED",
                    "phrase": phrase,
                    "expected": expected_cluster,
                    "observed": effective_cluster(after),
                    "expected_state": expected_state,
                    "observed_state": after.get("cluster_evidence_state", ""),
                    "source_file": V38_BASELINE_COMMIT,
                    "observed_reason": after.get("assignment_reason", ""),
                    "changed_fields": "",
                })
        else:
            # Target equals current but baseline did not differ in semantic fields;
            # this would mean the ledger did not represent a real V38 error.
            failures.append({
                "comparison_kind": "FROZEN_LEDGER_ROW_WITHOUT_V38_TO_V39_CHANGE",
                "phrase": phrase,
                "expected": expected_cluster,
                "observed": effective_cluster(after),
                "expected_state": expected_state,
                "observed_state": after.get("cluster_evidence_state", ""),
                "source_file": V38_BASELINE_COMMIT,
                "observed_reason": after.get("assignment_reason", ""),
                "changed_fields": "",
            })

    fields = ["comparison_kind", "phrase", "expected", "observed", "expected_state", "observed_state", "source_file", "observed_reason", "changed_fields"]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(failures)

    summary = {
        "status": "PASS" if not failures else "FAIL__FULL_REGRESSION_MISMATCHES",
        "v38_baseline_commit": V38_BASELINE_COMMIT,
        "rows_compared": len(baseline),
        "v39_frozen_manual_errors": len(spec.ROWS),
        "approved_v39_changed_rows": len(approved_changes),
        "unplanned_or_unrealized_rows": len(failures),
        "failure_count": len(failures),
        "meaning": "Regression authority is the exact persisted V38 assignment set across all 2,840 rows. V39 may change semantic assignment/state only for the 22 frozen full-manual-re-audit phrases, and every frozen row must reach its exact target cluster and evidence state.",
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for row in failures:
        print("V39_REGRESSION_FAIL", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(f"V39 full regression audit failed with {len(failures)} rows")


if __name__ == "__main__":
    main()
