#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V28 as v28


ACTIVE = {"CORE_CANDIDATE", "REVIEW_SEARCH"}
ASSIGNED = {"SEMANTIC_SUPPORTED_NO_DIRECT_SERP", "SERP_SUPPORTED"}


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def reviewed_false_positive(code: str, r: dict[str, str]) -> bool:
    p = n(r.get("phrase", ""))
    cid = r.get("cluster_id", "")

    # Full manual QA explicitly established 'виды ... окон' as a type/selection
    # information task. The inherited lexical audit only recognizes imperative
    # selection wording and therefore raises a false TASK_TOKEN_MISMATCH.
    if code == "TASK_TOKEN_MISMATCH" and cid == "WINDOW_SELECTION_INFO":
        if "вид" in p and has(p, "окн", "окон"):
            return True

    # V28/V32 explicitly reviewed these as component-headed product queries.
    # Suppress inherited marker-vocabulary misses only when the classifier already
    # assigned the reviewed hardware class and an explicit component marker exists.
    component_marker = has(p, "добор", "пластин", "панел", "профил", "рото", "roto", "узл")
    if cid == "WINDOW_HARDWARE" and component_marker and code in {"TASK_TOKEN_MISMATCH", "V15_HARDWARE_TOKEN_MISMATCH"}:
        return True

    # 'поставить окна' is an explicit installation action in ordinary Russian;
    # the inherited audit only looks for установ/монтаж stems.
    if code == "INSTALLATION_TOKEN_MISMATCH" and cid == "WINDOW_INSTALLATION" and "поставить" in p:
        return True

    # V33 adds a dedicated outside-core hardware task for blinds/curtains. V28's
    # curtain-family gate predates this task, so its family mismatch is obsolete
    # only for explicit blind/curtain hardware wording.
    if cid == "OUTSIDE_CURTAINS_HARDWARE":
        curtain = has(p, "жалюз", "штор", "занавес", "день ночь")
        hardware = has(p, "фурнитур", "комплектующ", "крепеж", "креплен", "механизм", "кронштейн")
        if curtain and hardware and code in {"V28_CURTAIN_TASK_MISMATCH", "TASK_TOKEN_MISMATCH"}:
            return True

    return False


def audit_v33(r: dict[str, str]) -> list[tuple[str, str]]:
    raw = list(v28.audit_v28(r))
    out = [(code, reason) for code, reason in raw if not reviewed_false_positive(code, r)]

    if r.get("cluster_evidence_state") not in ASSIGNED:
        return out

    p = n(r.get("phrase", ""))
    cid = r.get("cluster_id", "")

    curtain = has(p, "жалюз", "штор", "занавес", "день ночь")
    hardware = has(p, "фурнитур", "комплектующ", "крепеж", "креплен", "механизм", "кронштейн")
    if curtain and hardware and cid != "OUTSIDE_CURTAINS_HARDWARE":
        out.append(("V33_CURTAIN_HARDWARE_MISMATCH", "Blind/curtain hardware must stay distinct from both the blind product and window hardware"))

    return out


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged: list[dict[str, str]] = []
    counts = Counter()
    for r in rows:
        if r.get("input_disposition") not in ACTIVE:
            continue
        for code, reason in audit_v33(r):
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
        w.writeheader()
        w.writerows(flagged)

    summary = {
        "status": "PASS" if not flagged else "FAIL__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V33",
        "active_rows_scanned": sum(r.get("input_disposition") in ACTIVE for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "adjudication_basis": "Full V27/V32 manual QA: window-type 'виды' is valid selection information; reviewed component markers are valid WINDOW_HARDWARE evidence; 'поставить' is an installation verb; blind/curtain hardware is a new distinct outside-core product task.",
        "meaning": "V33 filters only manually adjudicated inherited lexical false positives and adds a hard gate for blind/curtain hardware. Zero flags remains necessary but not sufficient for final manual semantic acceptance.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if flagged:
        for row in flagged:
            print("V33_COLLISION_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if flagged:
        raise SystemExit("V33 semantic collision hard gate failed")


if __name__ == "__main__":
    main()
