#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V14 as v14audit


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


def architecture_subject_with_windows(p: str) -> bool:
    return bool(re.search(
        r"\b(?:дом\w*|квартир\w*|кв|комнат\w*|спальн\w*|кухн\w*|зал|лофт\w*|бан\w*|"
        r"апартамент\w*|пристройк\w*|беседк\w*|гостин\w*|одноэтажн\w*|проект\w*)\b"
        r".{0,45}\bс\b.{0,35}(?:панорам|француз)", p
    ))


def audit_v15(r: dict[str, str]) -> list[tuple[str, str]]:
    cid = r["cluster_id"]
    p = n(r["phrase"])
    flags = list(v14audit.audit_v14(r))
    if not cid:
        return flags

    windowish = anym(p, ("окн", "окон", "стеклопак", "остеклен", "застекл"))
    glazing = anym(p, ("остеклен", "застекл"))
    object_glazing = glazing and anym(p, ("балкон", "лоджи", "веранд", "террас", "бесед", "крыльц"))
    private_house = anym(p, ("частного дома", "частных домов", "частный дом", "частные дома", "частном доме", "загородного дома", "загородный дом", "для дома"))
    commercial = anym(p, ("купить", "заказать", "цена", "цены", "стоимость", "сколько стоит", "сколько стоят"))

    # Manual-QA non-repeat: naming a HOUSE cannot sit in a window-definition cluster.
    if cid == "WINDOW_DEFINITION_INFO" and "дом" in p and anym(p, ("панорам", "француз")) and anym(p, ("как называется", "как называются", "что за дом", "тип дома", "вид дома")):
        flags.append(("WINDOW_DEFINITION_SWALLOWED_HOUSE_NAMING", "window-definition cluster swallowed an architecture/house naming task"))

    # Generic private-house product is a last-resort task, never an override for a
    # more specific object, window type, door object, dimensions, or selection task.
    if cid == "PRIVATE_HOUSE_WINDOWS_COMMERCIAL":
        if object_glazing:
            flags.append(("PRIVATE_HOUSE_SWALLOWED_OBJECT_GLAZING", "generic private-house product cluster swallowed an object-specific glazing service"))
        if "входн" in p and "двер" in p:
            flags.append(("PRIVATE_HOUSE_SWALLOWED_ENTRY_DOOR", "generic private-house window cluster swallowed an entrance-door product"))
        if anym(p, ("панорам", "француз")):
            flags.append(("PRIVATE_HOUSE_SWALLOWED_SPECIFIC_WINDOW_TYPE", "generic private-house cluster swallowed a panoramic/French-window task"))
        if anym(p, ("размер", "ширина", "высота", "габарит")):
            flags.append(("PRIVATE_HOUSE_SWALLOWED_DIMENSION_TASK_V15", "generic private-house product cluster swallowed a dimensions task"))
        if anym(p, ("вариант", "виды", "образц", "как выбрать", "выбрать", "выбираем")) and not commercial:
            flags.append(("PRIVATE_HOUSE_SWALLOWED_SELECTION_TASK_V15", "generic private-house product cluster swallowed an explicit selection/types task"))

    if cid == "WOOD_WINDOWS_COMMERCIAL" and glazing and anym(p, ("веранд", "террас", "бесед", "крыльц", "балкон", "лоджи")):
        flags.append(("WOOD_PRODUCT_SWALLOWED_OBJECT_GLAZING", "wood-window product cluster swallowed an object-specific glazing service"))

    if cid == "SOFT_WINDOWS_COMMERCIAL" and anym(p, ("замок", "фурнитур", "ручк", "петл", "створк", "решетк", "раскладк", "шпрос")):
        flags.append(("SOFT_PRODUCT_SWALLOWED_COMPONENT", "soft-window product cluster swallowed a component/hardware task"))

    if cid == "PVC_WINDOWS_COMMERCIAL" and anym(p, ("виды", "варианты")) and not commercial:
        flags.append(("PVC_PRODUCT_SWALLOWED_TYPES_INFO", "PVC product cluster swallowed an explicit types/variants information task"))

    if cid == "PVC_DOORS_COMMERCIAL" and anym(p, ("окн", "окон")) and commercial and not anym(p, ("установ", "монтаж", "ремонт", "регулир")):
        flags.append(("PVC_DOOR_SWALLOWED_WINDOW_DOOR_PURCHASE", "door-only cluster swallowed an explicit combined windows+doors purchase task"))

    if cid == "OUTSIDE_REAL_ESTATE" and anym(p, ("француз", "панорам")):
        # A window-headed product/configuration phrase should not become real estate
        # merely because it contains 'в квартире'. Strong dwelling-subject forms are okay.
        window_headed = bool(re.search(r"\b(?:француз\w*|панорам\w*)\s+окн\w*\b", p)) or bool(re.search(r"\bокн\w*\s+(?:француз\w*|панорам\w*)\b", p))
        if window_headed and not architecture_subject_with_windows(p) and anym(p, ("на балкон", "москва", "цена", "стоимость", "ароч", "стеклопак")):
            flags.append(("REAL_ESTATE_SWALLOWED_WINDOW_HEADED_PRODUCT", "outside-real-estate cluster swallowed a window-headed product/configuration phrase"))

    # Product families must not swallow repair or object-glazing semantics.
    if cid in {"PANORAMIC_WINDOWS_COMMERCIAL", "FRENCH_WINDOWS_COMMERCIAL"}:
        if anym(p, ("ремонт", "регулир", "почин", "провис")):
            flags.append(("SPECIFIC_PRODUCT_SWALLOWED_REPAIR", "specific window-product cluster contains an explicit repair action"))
        if object_glazing:
            flags.append(("SPECIFIC_PRODUCT_SWALLOWED_OBJECT_GLAZING", "specific window-product cluster swallowed an object-specific glazing service"))

    if cid == "WINDOW_HARDWARE" and not windowish and not anym(p, ("фурнитур", "замок", "ручк", "петл", "створк", "решетк", "раскладк", "шпрос")):
        flags.append(("V15_HARDWARE_TOKEN_MISMATCH", "hardware cluster lacks a defining window/component marker"))

    return flags


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    for r in rows:
        if r["input_disposition"] not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit_v15(r):
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
        "audit_version": "V15",
        "active_rows_scanned": sum(r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "meaning": "V15 task-aware adversarial audit. Zero flags is necessary but not sufficient; manual semantic QA remains mandatory.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
