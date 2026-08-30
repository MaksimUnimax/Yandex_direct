#!/usr/bin/env python3
from __future__ import annotations

import ast
import csv
import json
import re
from pathlib import Path

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V38 as v38  # installs V38 classifier
import STEP_10_V38_DISCOVERY_SPEC as spec

BASE = Path(__file__).resolve().parent
OUT = BASE / "STEP_10_V38_FULL_REGRESSION_AUDIT.tsv"
OUT_JSON = BASE / "STEP_10_V38_FULL_REGRESSION_AUDIT.json"


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
    # Only [0] task-id assertions are relevant.
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
    """Extract literal phrase->task dictionaries used by historical self-tests."""
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
            # Avoid unrelated prose dictionaries: task IDs are uppercase analytical IDs.
            if val != "SEARCH_REQUIRED" and not re.fullmatch(r"[A-Z0-9_]+", val):
                ok = False; break
            pairs.append((k.value, val))
        if ok and pairs:
            found.extend(pairs)
    return found


def collect_historical_expectations():
    # Latest historical expectation wins. This turns many versioned fail-fast tests
    # into one corpus and avoids whack-a-mole reruns.
    latest: dict[str, dict[str, str | int]] = {}
    files = sorted(BASE.glob("STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V*.py"), key=version_of)
    for path in files:
        ver = version_of(path)
        if ver >= 38:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and "self_test" in n.name]:
            for phrase, expected in literal_expectation_dicts(fn):
                latest[phrase] = {"expected": expected, "source_version": ver, "source_file": path.name}
            for node in ast.walk(fn):
                if isinstance(node, ast.Assert):
                    parsed = classify_literal_assert(node)
                    if parsed:
                        phrase, expected = parsed
                        latest[phrase] = {"expected": expected, "source_version": ver, "source_file": path.name}
    return latest


def main() -> None:
    historical = collect_historical_expectations()

    # The frozen full-manual discovery is the explicit, documented supersession set.
    # No other historical expectation is silently changed.
    for row in spec.ROWS:
        historical[row["phrase"]] = {
            "expected": row["proposed_cluster_id"],
            "source_version": 38,
            "source_file": "STEP_10_V38_DISCOVERY_SPEC.py",
        }

    failures = []
    for phrase in sorted(historical, key=b.norm):
        meta = historical[phrase]
        task_id, reason, confidence = b.classify_semantic(phrase)
        observed = task_id or "SEARCH_REQUIRED"
        expected = str(meta["expected"])
        if observed != expected:
            failures.append({
                "phrase": phrase,
                "expected": expected,
                "observed": observed,
                "source_version": str(meta["source_version"]),
                "source_file": str(meta["source_file"]),
                "observed_reason": reason,
            })

    fields = ["phrase", "expected", "observed", "source_version", "source_file", "observed_reason"]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(failures)

    summary = {
        "status": "PASS" if not failures else "FAIL__FULL_REGRESSION_MISMATCHES",
        "historical_latest_expectations": len(historical),
        "v38_discovery_supersessions": len(spec.ROWS),
        "failure_count": len(failures),
        "meaning": "All discoverable historical literal self-test expectations are evaluated in one pass; the audit reports every mismatch before failing. V38's 85 frozen manual-discovery rows are the only explicit supersessions.",
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for row in failures:
        print("V38_REGRESSION_FAIL", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(f"V38 full regression audit failed with {len(failures)} mismatches")


if __name__ == "__main__":
    main()
