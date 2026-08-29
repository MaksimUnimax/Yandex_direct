#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V10 as v10audit


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


def audit_v11(r: dict[str, str]) -> list[tuple[str, str]]:
    cid = r["cluster_id"]
    p = n(r["phrase"])
    flags = []

    for code, reason in v10audit.audit_v10(r):
        if code == "SOFT_WINDOW_TOKEN_MISMATCH" and "мягк" in p and anym(p, ("окн", "окон", "остеклен")):
            continue
        if code == "TASK_TOKEN_MISMATCH" and cid == "WINDOW_HARDWARE" and "раскладк" in p:
            continue
        flags.append((code, reason))

    # Non-repeat controls for the V9/V10 private-house precedence regression.
    if cid == "PRIVATE_HOUSE_WINDOWS_COMMERCIAL":
        if anym(p, ("пластиков", "пвх", "алюмини", "деревян", "rehau", "рехау", "provedal", "проведал")):
            flags.append(("PRIVATE_HOUSE_SWALLOWED_MATERIAL_TASK", "generic private-house cluster swallowed an explicit window material/brand task"))
        if anym(p, ("установ", "монтаж", "ремонт", "регулир", "замена", "заменить", "поменять", "размер", "ширина", "высота", "отзыв")):
            flags.append(("PRIVATE_HOUSE_SWALLOWED_ACTION_OR_INFO_TASK", "generic private-house cluster swallowed a more specific service/information task"))

    if cid == "WINDOW_DEFINITION_INFO" and anym(p, ("как называется дом", "что за дом", "тип дома", "вид дома")):
        flags.append(("WINDOW_DEFINITION_SWALLOWED_HOUSE_NAMING", "window-definition cluster contains a question whose defined object is the house"))

    if cid == "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO" and not anym(
        p, ("требован", "норматив", "норма ", "вентиляц", "какое должно", "какой должен", "площадь остекления")
    ):
        flags.append(("PRIVATE_HOUSE_REQUIREMENTS_WITHOUT_REQUIREMENT_MARKER", "requirements cluster lacks an explicit requirements/constraint marker"))

    return flags


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    flagged = []
    counts = Counter()
    for r in rows:
        if r["input_disposition"] not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit_v11(r):
            counts[code] += 1
            flagged.append({
                "collision_code": code,
                "phrase": r["phrase"],
                "cluster_id": r["cluster_id"],
                "user_task": r["user_task"],
                "evidence_state": r["cluster_evidence_state"],
                "step09_probe_id": r["step09_probe_id"],
                "reason": reason,
            })

    fields = ["collision_code", "phrase", "cluster_id", "user_task", "evidence_state", "step09_probe_id", "reason"]
    with old.OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)

    summary = {
        "status": "AUDIT_GENERATED__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V11",
        "active_rows_scanned": sum(r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "meaning": "V11 task-aware adversarial audit. Zero flags is necessary but not sufficient; manual semantic QA remains mandatory.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
