#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V19 as v19


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


def rx(p: str, pattern: str) -> bool:
    return bool(re.search(pattern, p))


PRODUCT_CLUSTERS = {
    "ALUMINIUM_WINDOWS_COMMERCIAL",
    "PVC_WINDOWS_COMMERCIAL",
    "PVC_WINDOWS_GEO",
    "PVC_WINDOWS_MANUFACTURER",
    "REHAU_WINDOWS_COMMERCIAL",
    "REHAU_PRODUCT_SUBTYPE",
    "PANORAMIC_WINDOWS_COMMERCIAL",
    "FRENCH_WINDOWS_COMMERCIAL",
    "PVC_DOORS_COMMERCIAL",
    "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
    "WOOD_WINDOWS_COMMERCIAL",
}

GLAZING_SERVICE_CLUSTERS = {
    "BALCONY_GLAZING",
    "BALCONY_GLAZING_WARM",
    "BALCONY_GLAZING_COLD",
    "BALCONY_GLAZING_ROOF",
    "BALCONY_GLAZING_EXTENSION",
    "BALCONY_GLAZING_HOUSE_SERIES",
    "BALCONY_GLAZING_WOOD",
    "VERANDA_GLAZING",
    "TERRACE_GLAZING",
    "GAZEBO_GLAZING",
    "PORCH_GLAZING",
    "FRAMELESS_GLAZING",
    "OUTDOOR_GLAZING_MULTI_OBJECT",
}


def component_head(p: str) -> bool:
    return (
        rx(p, r"^(?:детск\w*\s+)?зам(?:ок|ки|ка|ков)\b")
        or rx(p, r"^(?:многозапорн\w*\s+)?зам(?:ок|ки|ка|ков)\b")
        or rx(p, r"^(?:механизм|створк\w*|редуктор\w*|ригель\w*|ролик\w*|клапан\w*|заглушк\w*|направляющ\w*|стеклопакет\w*)\b")
        or rx(p, r"\b(?:профил\w*|рам\w*|стеклопакет\w*|ролик\w*|клапан\w*|заглушк\w*|направляющ\w*)\s+(?:для|на)\s+.*\bокн")
        or "подставочный профиль для окон" in p
    )


def audit_v20(r: dict[str, str]) -> list[tuple[str, str]]:
    cid = r["cluster_id"]
    p = n(r["phrase"])
    out: list[tuple[str, str]] = []

    # Preserve all already-adjudicated V19 hard-gate controls.
    out.extend(v19.audit_v19(r))

    # Broad whole-product clusters must not swallow explicit user actions or
    # head components. These patterns are intentionally conservative: only strong
    # markers discovered in manual QA are hard-gated.
    if cid in PRODUCT_CLUSTERS:
        if anym(p, ("отзыв", "рейтинг", "форум")):
            out.append(("V20_PRODUCT_SWALLOWED_REPUTATION_TASK", "whole-product cluster swallowed explicit reviews/ranking/forum intent"))
        if anym(p, ("фото", "дизайн", "интерьер")) or rx(p, r"\bпример(?:ы)?\b"):
            out.append(("V20_PRODUCT_SWALLOWED_VISUAL_TASK", "whole-product cluster swallowed explicit photo/design/example intent"))
        if anym(p, ("размер", "ширина", "высота", "габарит")) and not anym(p, ("купить", "заказать", "цена", "цены", "стоимость", "установ", "монтаж")):
            out.append(("V20_PRODUCT_SWALLOWED_DIMENSION_TASK", "whole-product cluster swallowed an explicit dimension-information task"))
        if rx(p, r"^\s*(?:установка|монтаж)\b") or "изготовление и установка" in p or "установка готовых" in p:
            out.append(("V20_PRODUCT_SWALLOWED_ACTION_HEADED_INSTALL", "whole-product cluster swallowed an action-headed installation service"))
        if anym(p, ("не закрывается", "не открывается", "не закрывает", "не открывает", "открывание", "проветривание")):
            out.append(("V20_PRODUCT_SWALLOWED_OPERATION_OR_SYMPTOM", "whole-product cluster swallowed an operation/malfunction task"))
        if component_head(p):
            out.append(("V20_PRODUCT_SWALLOWED_COMPONENT_HEAD", "whole-product cluster swallowed a component/hardware head object"))
        if anym(p, ("подоконник для пластиковых окон", "цена пластиковых подоконников", "пластиковые решетки на окна", "краска для алюминиевых окон")):
            out.append(("V20_PRODUCT_SWALLOWED_ACCESSORY_HEAD", "whole-product cluster swallowed an explicit accessory/material head object"))
        if anym(p, ("какое окно алюминиевое", "какие окна rehau", "какие окна рехау")) and not anym(p, ("купить", "заказать", "цена", "стоимость")):
            out.append(("V20_PRODUCT_SWALLOWED_SELECTION_TASK", "whole-product cluster swallowed an explicit selection question"))

    # Object-specific glazing service clusters were the main false-green source in
    # V19. Explicit information/DIY/legal/demolition/material-head signals cannot
    # remain in the generic service family.
    if cid in GLAZING_SERVICE_CLUSTERS:
        if anym(p, ("отзыв", "рейтинг", "форум")):
            out.append(("V20_GLAZING_SWALLOWED_REPUTATION_TASK", "glazing service cluster swallowed reviews/ranking/forum intent"))
        if anym(p, ("фото", "дизайн")) or rx(p, r"\bпример(?:ы)?\b"):
            out.append(("V20_GLAZING_SWALLOWED_VISUAL_TASK", "glazing service cluster swallowed photo/design/example intent"))
        if anym(p, ("какое остекление", "какое лучше", "какое выбрать", "выбрать остекление", "материалы")):
            out.append(("V20_GLAZING_SWALLOWED_SELECTION_TASK", "glazing service cluster swallowed explicit selection/material-choice intent"))
        if anym(p, ("самому", "своими руками", "самостоятель", "как остеклить", "как застеклить", "пошаг", "видео")):
            out.append(("V20_GLAZING_SWALLOWED_DIY_TASK", "glazing service cluster swallowed explicit DIY/procedural intent"))
        if anym(p, ("разрешение", "разрешен", "можно ли", "нужно ли")):
            out.append(("V20_GLAZING_SWALLOWED_PERMISSION_TASK", "glazing service cluster swallowed legal/permission intent"))
        if "без остеклен" in p:
            out.append(("V20_GLAZING_SWALLOWED_NO_GLAZING_TASK", "glazing service cluster swallowed an explicit no-glazing/open-balcony task"))
        if "демонтаж" in p:
            out.append(("V20_GLAZING_SWALLOWED_DEMOLITION", "glazing service cluster swallowed explicit demolition/removal action"))
        if "ремонт" in p:
            out.append(("V20_GLAZING_SWALLOWED_REPAIR_MIX", "glazing service cluster swallowed a mixed repair/glazing task"))
        if rx(p, r"\b(?:профил\w*|рам\w*)\s+для\s+остеклен") or rx(p, r"\b(?:монолитн\w*\s+)?поликарбонат\w*\s+для\s+остеклен"):
            out.append(("V20_GLAZING_SWALLOWED_MATERIAL_HEAD", "glazing service cluster swallowed a material/component head object"))
        if "кондиционер" in p:
            out.append(("V20_GLAZING_SWALLOWED_HVAC", "glazing service cluster swallowed an air-conditioning task"))

    if cid == "WINDOW_REPLACEMENT_SERVICE" and anym(p, ("оконной фурнитур", "замена фурнитуры", "заменить фурнитуру")):
        out.append(("V20_REPLACEMENT_SWALLOWED_HARDWARE_REPLACEMENT", "whole-window replacement cluster swallowed replacement of window hardware"))

    if cid == "WINDOW_REPAIR":
        if anym(p, ("запчасти для ремонта", "ремкомплект", "набор для ремонта", "клей для ремонта", "космофен для ремонта")):
            out.append(("V20_REPAIR_SWALLOWED_REPAIR_PRODUCT", "repair-service cluster swallowed repair parts/material product demand"))
        if anym(p, ("самому", "своими руками", "домашних условиях", "руками")):
            out.append(("V20_REPAIR_SWALLOWED_DIY", "repair-service cluster swallowed explicit self-repair/DIY intent"))
        if anym(p, ("отзыв", "рейтинг", "форум")):
            out.append(("V20_REPAIR_SWALLOWED_REPUTATION", "repair-service cluster swallowed reviews/ranking/forum intent"))
        if anym(p, ("ремонт откос", "ремонт отлив", "ремонт подокон")):
            out.append(("V20_REPAIR_SWALLOWED_FINISHING", "generic repair cluster swallowed finishing/windowsill repair"))
        if anym(p, ("пластиковые окна после ремонта", "пластиковые окна без ремонта", "окна пластиковые какой ремонт")):
            out.append(("V20_REPAIR_SWALLOWED_CONTEXTUAL_REPAIR_WORD", "repair-service cluster swallowed contextual/ambiguous repair wording"))

    if cid == "PVC_DOORS_COMMERCIAL":
        if rx(p, r"^\s*(?:установка|монтаж)\b"):
            out.append(("V20_DOOR_PRODUCT_SWALLOWED_INSTALL_SERVICE", "plastic-door product cluster swallowed action-headed installation"))
        if anym(p, ("не закрывается", "не открывается", "открывание", "как открыть", "как закрыть", "снять дверь")):
            out.append(("V20_DOOR_PRODUCT_SWALLOWED_OPERATION_REPAIR", "plastic-door product cluster swallowed operation/malfunction intent"))

    if cid == "WINDOW_INSTALLATION":
        if anym(p, ("отзыв", "рейтинг", "форум")):
            out.append(("V20_INSTALL_SWALLOWED_REPUTATION", "installation-service cluster swallowed reviews/ranking/forum intent"))
        if anym(p, ("фото", "видео", "инструк", "пошаг")):
            out.append(("V20_INSTALL_SWALLOWED_PROCEDURE", "installation-service cluster swallowed explicit procedural/visual intent"))
        if "ремонт" in p:
            out.append(("V20_INSTALL_SWALLOWED_REPAIR_MIX", "installation-service cluster swallowed mixed installation+repair intent"))

    return out


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    for r in rows:
        if r["input_disposition"] not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit_v20(r):
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
        "status": "PASS" if not flagged else "FAIL__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V20",
        "active_rows_scanned": sum(r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "meaning": "V20 broad-cluster adversarial hard gate derived from manual-QA failures. Zero flags is necessary but still not sufficient for final manual semantic acceptance.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if flagged:
        for row in flagged:
            print("V20_COLLISION_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if flagged:
        raise SystemExit("V20 collision hard gate failed")


if __name__ == "__main__":
    main()
