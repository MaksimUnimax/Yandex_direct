#!/usr/bin/env python3
from __future__ import annotations

import ast
import csv
import io
import json
import re
import subprocess
from pathlib import Path

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V38 as v38  # installs V38 classifier
import STEP_10_V38_DISCOVERY_SPEC as spec

BASE = Path(__file__).resolve().parent
ASSIGN = BASE / "STEP_10_CLUSTER_ASSIGNMENTS.tsv"
OUT = BASE / "STEP_10_V38_FULL_REGRESSION_AUDIT.tsv"
OUT_JSON = BASE / "STEP_10_V38_FULL_REGRESSION_AUDIT.json"
V37_BASELINE_COMMIT = "530112a4766dadf8299970895ddc84b82b3651dc"
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


def frozen_v37_rows():
    proc = subprocess.run(
        ["git", "show", f"{V37_BASELINE_COMMIT}:{REPO_REL_ASSIGN}"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    return read_tsv_text(proc.stdout)


def current_v38_rows():
    with ASSIGN.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def version_of(path: Path) -> int:
    m = re.search(r"_V(\d+)\.py$", path.name)
    return int(m.group(1)) if m else 0


def classify_literal_assert(node: ast.Assert):
    test = node.test
    if not isinstance(test, ast.Compare) or len(test.ops) != 1 or len(test.comparators) != 1:
        return None
    left = test.left
    if not isinstance(left, ast.Subscript):
        return None
    call = left.value
    if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Attribute):
        return None
    if call.func.attr != "classify_semantic" or not call.args or not isinstance(call.args[0], ast.Constant) or not isinstance(call.args[0].value, str):
        return None
    sl = left.slice
    idx = sl.value if isinstance(sl, ast.Constant) else None
    if idx != 0:
        return None
    phrase = call.args[0].value
    rhs = test.comparators[0]
    op = test.ops[0]
    if isinstance(op, ast.Eq) and isinstance(rhs, ast.Constant) and isinstance(rhs.value, str):
        return phrase, rhs.value
    if isinstance(op, ast.Is) and isinstance(rhs, ast.Constant) and rhs.value is None:
        return phrase, "SEARCH_REQUIRED"
    return None


def literal_expectation_dicts(fn: ast.AST):
    found = []
    for node in ast.walk(fn):
        if not isinstance(node, ast.Dict):
            continue
        pairs = []
        ok = True
        for k, v in zip(node.keys, node.values):
            if not isinstance(k, ast.Constant) or not isinstance(k.value, str):
                ok = False; break
            if isinstance(v, ast.Constant) and (isinstance(v.value, str) or v.value is None):
                val = "SEARCH_REQUIRED" if v.value is None else v.value
            else:
                ok = False; break
            if val != "SEARCH_REQUIRED" and not re.fullmatch(r"[A-Z0-9_]+", val):
                ok = False; break
            pairs.append((k.value, val))
        if ok and pairs:
            found.extend(pairs)
    return found


def collect_historical_expectations():
    latest = {}
    files = sorted(BASE.glob("STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V*.py"), key=version_of)
    for path in files:
        ver = version_of(path)
        if ver >= 38:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and "self_test" in n.name]:
            for phrase, expected in literal_expectation_dicts(fn):
                latest[phrase] = {"expected": expected, "source_version": ver, "source_file": path.name}
            for node in ast.walk(fn):
                if isinstance(node, ast.Assert):
                    parsed = classify_literal_assert(node)
                    if parsed:
                        phrase, expected = parsed
                        latest[phrase] = {"expected": expected, "source_version": ver, "source_file": path.name}
    return latest


def effective_cluster(row):
    return row.get("cluster_id", "") or ("SEARCH_REQUIRED" if row.get("cluster_evidence_state") == "SEARCH_REQUIRED" else "")


def main() -> None:
    baseline = frozen_v37_rows()
    current = current_v38_rows()
    assert len(baseline) == 2840, len(baseline)
    assert len(current) == 2840, len(current)
    bmap = {r["phrase"]: r for r in baseline}
    cmap = {r["phrase"]: r for r in current}
    assert set(bmap) == set(cmap)

    frozen = spec.EXPECTED_BY_PHRASE
    failures = []
    approved_changes = []

    # Strong regression contract: for all 2,840 rows, V38 may change semantic
    # assignment/state only for a phrase explicitly frozen in the 85-row discovery
    # ledger. This catches broad-rule side effects beyond the reviewed error set.
    for phrase in sorted(bmap, key=b.norm):
        before = bmap[phrase]
        after = cmap[phrase]
        diffs = {field: (before.get(field, ""), after.get(field, "")) for field in SEMANTIC_FIELDS if before.get(field, "") != after.get(field, "")}
        if not diffs:
            continue
        if phrase in frozen:
            expected = frozen[phrase]["proposed_cluster_id"]
            observed = effective_cluster(after)
            if observed == expected:
                approved_changes.append({"phrase": phrase, "expected": expected, "observed": observed, "changed_fields": ";".join(sorted(diffs))})
                continue
        failures.append({
            "comparison_kind": "UNPLANNED_V37_TO_V38_CHANGE",
            "phrase": phrase,
            "expected": frozen.get(phrase, {}).get("proposed_cluster_id", effective_cluster(before)),
            "observed": effective_cluster(after),
            "source_version": "V37_BASELINE",
            "source_file": V37_BASELINE_COMMIT,
            "observed_reason": after.get("assignment_reason", ""),
            "changed_fields": ";".join(sorted(diffs)),
        })

    # Historical self-tests remain useful diagnostics, but V37 persisted output is
    # the authoritative regression baseline. If an old literal test disagrees with
    # V37 before V38, it is stale history rather than a new V38 regression.
    historical = collect_historical_expectations()
    stale_historical = []
    historical_new_conflicts = []
    for phrase, meta in historical.items():
        if phrase not in bmap or phrase in frozen:
            continue
        historical_expected = str(meta["expected"])
        v37_expected = effective_cluster(bmap[phrase])
        v38_observed = effective_cluster(cmap[phrase])
        if historical_expected != v37_expected:
            stale_historical.append({
                "phrase": phrase,
                "historical_expected": historical_expected,
                "v37_baseline": v37_expected,
                "source_version": str(meta["source_version"]),
                "source_file": str(meta["source_file"]),
            })
        elif v38_observed != historical_expected:
            historical_new_conflicts.append(phrase)

    # Any historical expectation that agreed with V37 but now differs from V38
    # should already be caught by the full 2,840-row baseline diff.
    assert not historical_new_conflicts or failures

    fields = ["comparison_kind", "phrase", "expected", "observed", "source_version", "source_file", "observed_reason", "changed_fields"]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(failures)

    summary = {
        "status": "PASS" if not failures else "FAIL__FULL_REGRESSION_MISMATCHES",
        "v37_baseline_commit": V37_BASELINE_COMMIT,
        "rows_compared": len(baseline),
        "v38_discovery_supersessions": len(spec.ROWS),
        "approved_v38_changed_rows": len(approved_changes),
        "unplanned_v38_changed_rows": len(failures),
        "historical_literal_expectations_scanned": len(historical),
        "stale_historical_expectations_vs_v37": len(stale_historical),
        "stale_historical_examples": stale_historical[:20],
        "failure_count": len(failures),
        "meaning": "Regression authority is the full persisted V37 assignment set across all 2,840 rows. V38 may alter only the 85 frozen manual-discovery phrases. Historical literal tests are diagnostics; expectations already contradicted by persisted V37 are reported as stale rather than forcing semantic rollback.",
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for row in failures:
        print("V38_REGRESSION_FAIL", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(f"V38 full regression audit failed with {len(failures)} unplanned changed rows")


if __name__ == "__main__":
    main()
