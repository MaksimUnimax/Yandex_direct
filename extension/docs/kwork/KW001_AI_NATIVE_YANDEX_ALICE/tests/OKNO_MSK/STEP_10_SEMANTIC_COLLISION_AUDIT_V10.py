#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


def audit_v10(r: dict[str, str]) -> list[tuple[str, str]]:
    cid = r["cluster_id"]
    p = n(r["phrase"])
    flags = []

    # Reuse the established audit, but suppress only false positives made obsolete
    # by explicit V9/V10 task definitions. This does not suppress arbitrary flags.
    for code, reason in old.audit(r):
        if code == "TASK_TOKEN_MISMATCH" and cid == "OUTSIDE_REAL_ESTATE" and anym(
            p, ("дом", "барнхаус", "дача", "апартамент", "гостиная", "баня", "бассейн", "лес", "проект", "интерьер", "квартир", "комнат", "кухн", "зал ", "лофт", "бесед", "бытов", "барбекю", "веранд", "террас")
        ):
            continue
        if code == "TASK_TOKEN_MISMATCH" and cid == "WINDOW_OPERATION_DIY" and anym(
            p, ("снять", "вставить", "открыть", "закрыть", "разобрать", "заменить", "поменять", "открой", "закрой")
        ):
            continue
        if code == "TASK_TOKEN_MISMATCH" and cid == "WINDOW_DIMENSIONS_INFO" and (
            anym(p, ("размер", "ширина", "высота", "габарит", "метр", " мм")) or re.search(r"\b\d+(?:[.,]\d+)?\s*м\b", p)
        ):
            continue
        if code == "PANORAMIC_WITHOUT_PURCHASE_SIGNAL" and cid == "PANORAMIC_WINDOWS_COMMERCIAL" and anym(
            p, ("готов", "больш", "высок", "маленьк", "широк", "узк")
        ):
            continue
        flags.append((code, reason))

    # V10 task-specific structural checks.
    if cid == "FRENCH_WINDOWS_COMMERCIAL":
        if "француз" not in p or not ("окн" in p or "окон" in p):
            flags.append(("FRENCH_PRODUCT_TOKEN_MISMATCH", "French-window product cluster lacks French-window wording"))
    if cid == "SOFT_WINDOWS_COMMERCIAL":
        if "мягк" not in p or not ("окн" in p or "окон" in p):
            flags.append(("SOFT_WINDOW_TOKEN_MISMATCH", "soft-window cluster lacks soft-window wording"))
    if cid == "PVC_DOOR_DIMENSIONS_INFO" and not anym(p, ("ширина", "высота", "размер", "габарит")):
        flags.append(("PVC_DOOR_DIMENSION_TOKEN_MISMATCH", "PVC-door dimension cluster lacks a dimension marker"))
    if cid == "PVC_DOOR_OPERATION_INFO" and not anym(p, ("откры", "закры", "снять", "встав", "разоб")):
        flags.append(("PVC_DOOR_OPERATION_TOKEN_MISMATCH", "PVC-door operation cluster lacks an operation marker"))
    if cid == "PVC_DOOR_DEFINITION_INFO" and not anym(p, ("как называется", "что такое", "как зовется")):
        flags.append(("PVC_DOOR_DEFINITION_TOKEN_MISMATCH", "PVC-door definition cluster lacks a definition marker"))
    if cid == "PRIVATE_HOUSE_WINDOWS_COMMERCIAL" and not anym(p, ("частного дома", "частный дом", "в частном доме", "для дома")):
        flags.append(("PRIVATE_HOUSE_PRODUCT_CONTEXT_MISMATCH", "private-house product cluster lacks private-house context"))
    if cid == "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO" and not anym(p, ("вариант", "вид", "какие окна", "какое окно", "лучш", "образц", "выбрать", "выбор")):
        flags.append(("PRIVATE_HOUSE_SELECTION_TOKEN_MISMATCH", "private-house selection cluster lacks a selection/types marker"))
    if cid == "BALCONY_GLAZING_WOOD" and not ("остеклен" in p and anym(p, ("балкон", "лоджи")) and "деревян" in p):
        flags.append(("WOOD_BALCONY_GLAZING_TOKEN_MISMATCH", "wood-frame balcony glazing cluster lacks its service/material markers"))
    if cid == "WINDOW_DEMOLITION" and "демонтаж" not in p:
        flags.append(("DEMOLITION_TOKEN_MISMATCH", "demolition cluster lacks demolition wording"))

    return flags


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    flagged = []
    counts = Counter()
    for r in rows:
        if r["input_disposition"] not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit_v10(r):
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
        "audit_version": "V10",
        "active_rows_scanned": sum(r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "meaning": "Heuristic adversarial audit with V10 task-aware controls; flags still require manual review and cannot self-accept Step 10.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
