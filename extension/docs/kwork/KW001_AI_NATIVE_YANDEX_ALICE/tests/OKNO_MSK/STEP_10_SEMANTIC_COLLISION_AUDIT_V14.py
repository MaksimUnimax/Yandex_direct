#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V11 as v11audit


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


def audit_v14(r: dict[str, str]) -> list[tuple[str, str]]:
    cid = r["cluster_id"]
    p = n(r["phrase"])
    flags = []

    for code, reason in v11audit.audit_v11(r):
        # V11's base lexical check knows only 'пластиков', not the equivalent
        # explicit Russian abbreviation 'ПВХ'. Suppress that false positive only
        # when both PVC and window tokens are actually present.
        if code == "PVC_PRODUCT_TOKEN_MISMATCH" and cid == "PVC_WINDOWS_COMMERCIAL" and "пвх" in p and anym(p, ("окн", "окон")):
            continue
        flags.append((code, reason))

    # Non-repeat control for the V13 precedence bug: an explicit informational
    # dimension task must never stay inside the PVC product cluster when there is no
    # buying/price/installation signal.
    if cid == "PVC_WINDOWS_COMMERCIAL" and anym(p, ("размер", "ширина", "высота", "габарит")) and not anym(
        p, ("купить", "заказать", "цена", "цены", "стоимость", "установ", "монтаж")
    ):
        flags.append(("PVC_PRODUCT_SWALLOWED_DIMENSION_TASK", "PVC product cluster swallowed an explicit size/dimension information task"))

    if cid == "PVC_WINDOWS_COMMERCIAL" and anym(p, ("установ", "монтаж", "ремонт", "регулир")) and "частн" in p and "пвх" in p:
        flags.append(("PVC_PRODUCT_SWALLOWED_PRIVATE_HOUSE_ACTION", "PVC product cluster swallowed a more specific private-house installation/repair task"))

    return flags


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    flagged = []
    counts = Counter()
    for r in rows:
        if r["input_disposition"] not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit_v14(r):
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
        "audit_version": "V14",
        "active_rows_scanned": sum(r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "meaning": "V14 task-aware adversarial audit. Zero flags is necessary but not sufficient; manual semantic QA remains mandatory.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
