#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
ASSIGN = BASE / "STEP_10_CLUSTER_ASSIGNMENTS.tsv"
OUT = BASE / "STEP_10_SEMANTIC_COLLISION_AUDIT.tsv"
OUT_JSON = BASE / "STEP_10_SEMANTIC_COLLISION_AUDIT.json"


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


INFO = ("как ", "почему", "отзыв", "инструк", "своими руками", "что такое", "как называется", "сравн", "лучше", "разница", "чем отлич")
REPAIR = ("ремонт", "регулир", "провис", "почин", "замена резин", "замена уплот")
ACCESSORY = ("фурнитур", "сетк", "москит", "антикошка", "штор", "жалюзи", "штапик", "ручк", "уплотн", "радиатор", "батаре", "конвектор", "герметик", "шпрос")
DIY = ("своими руками", "самостоятель", "пошаг", "как установить", "как сделать", "как снять", "как открыть", "как вставить")
GEO = ("москва", "митино", "одинцово", "одинцове", "район", "московск")


def audit(r: dict[str, str]) -> list[tuple[str, str]]:
    cid = r["cluster_id"]
    p = n(r["phrase"])
    out = []
    if not cid:
        return out

    product_clusters = {
        "PVC_WINDOWS_COMMERCIAL", "PVC_WINDOWS_GEO", "PVC_WINDOWS_MANUFACTURER",
        "ALUMINIUM_WINDOWS_COMMERCIAL", "REHAU_WINDOWS_COMMERCIAL", "REHAU_PRODUCT_SUBTYPE",
        "PROVEDAL_WINDOWS_COMMERCIAL", "WOOD_WINDOWS_COMMERCIAL", "PANORAMIC_WINDOWS_COMMERCIAL",
        "PVC_DOORS_COMMERCIAL",
    }
    if cid in product_clusters:
        if anym(p, REPAIR): out.append(("PRODUCT_WITH_REPAIR_MARKER", "commercial product cluster contains repair/adjustment wording"))
        if anym(p, ACCESSORY): out.append(("PRODUCT_WITH_ACCESSORY_MARKER", "commercial product cluster contains accessory/component wording"))
        if anym(p, INFO): out.append(("PRODUCT_WITH_INFORMATIONAL_MARKER", "commercial product cluster contains strong informational wording"))
        if anym(p, DIY): out.append(("PRODUCT_WITH_DIY_MARKER", "commercial product cluster contains DIY/procedural wording"))

    if cid == "PVC_WINDOWS_GEO":
        if not anym(p, GEO): out.append(("GEO_CLUSTER_WITHOUT_GEO", "geo cluster member has no explicit geo marker"))
        if not ("пластиков" in p and ("окн" in p or "окон" in p)):
            out.append(("GEO_CLUSTER_NOT_GENERIC_PVC_WINDOW", "geo cluster member is not a generic PVC-window phrase"))

    if cid == "PVC_WINDOWS_COMMERCIAL" and not ("пластиков" in p and ("окн" in p or "окон" in p)):
        out.append(("PVC_PRODUCT_TOKEN_MISMATCH", "PVC-window commercial cluster lacks PVC-window wording"))
    if cid == "ALUMINIUM_WINDOWS_COMMERCIAL" and not ("алюмини" in p and ("окн" in p or "окон" in p)):
        out.append(("ALUMINIUM_PRODUCT_TOKEN_MISMATCH", "aluminium-window cluster lacks aluminium-window wording"))
    if cid == "REHAU_WINDOWS_COMMERCIAL" and not ("rehau" in p or "рехау" in p):
        out.append(("REHAU_PRODUCT_TOKEN_MISMATCH", "Rehau cluster lacks Rehau wording"))
    if cid == "WOOD_WINDOWS_COMMERCIAL" and not anym(p, ("деревян", "дерево алюмини", "дерево-алюмини", "деревоалюмини")):
        out.append(("WOOD_PRODUCT_TOKEN_MISMATCH", "wood/timber-aluminium cluster lacks material wording"))
    if cid == "PANORAMIC_WINDOWS_COMMERCIAL":
        if "панорам" not in p: out.append(("PANORAMIC_TOKEN_MISMATCH", "panoramic cluster lacks panoramic wording"))
        strong = anym(p, ("купить", "заказать", "цена", "цены", "стоимость", "производител", "элитн", "пластиков", "алюмини", "деревян", "размер", "профил"))
        if p not in {"панорамные окна", "панорамное окно"} and not strong:
            out.append(("PANORAMIC_WITHOUT_PURCHASE_SIGNAL", "panoramic cluster lacks a clear product/purchase signal"))

    service_clusters = {"WINDOW_INSTALLATION", "WINDOW_REPAIR", "WINDOW_DEMOLITION", "PVC_DOOR_REPAIR_SERVICE"}
    if cid in service_clusters and anym(p, DIY):
        out.append(("SERVICE_WITH_DIY_MARKER", "commercial service cluster contains strong DIY/procedural wording"))
    if cid == "WINDOW_INSTALLATION" and not anym(p, ("установ", "монтаж")):
        out.append(("INSTALLATION_TOKEN_MISMATCH", "installation cluster lacks installation/mounting wording"))
    if cid == "WINDOW_REPAIR" and not anym(p, ("ремонт", "регулир", "провис", "почин", "замена", "мастер")):
        out.append(("REPAIR_TOKEN_MISMATCH", "repair cluster lacks repair/maintenance wording"))

    exact_requirements = {
        "WINDOW_SELECTION_INFO": ("выбрать", "выбираем", "выбор"),
        "WINDOW_REPAIR_DIY": ("ремонт", "регулир", "провис", "почин"),
        "PVC_DOOR_REPAIR_DIY": ("ремонт", "регулир", "провис", "почин"),
        "PVC_DOOR_REPAIR_SERVICE": ("ремонт", "регулир", "провис", "почин"),
        "WINDOW_FABRICATION_DIY": ("сделать", "изготов"),
        "WINDOW_DIMENSIONS_INFO": ("размер", "ширина", "высота", "габарит"),
        "WINDOW_OPERATION_DIY": ("снять", "вставить", "открыть", "закрыть", "разобрать", "заменить", "поменять"),
        "WINDOW_CARE_INFO": ("отмыть", "очистить", "мыть", "помыть", "очистка"),
        "WINDOW_HARDWARE": ("фурнитур", "штапик", "ручк", "микролифт", "ограничител", "анкер", "гребен", "уплотн", "профил", "fapim", "комплект", "резинк", "шпрос"),
        "MOSQUITO_NETS": ("сетк", "москит", "антикошка"),
        "OUTSIDE_CURTAINS": ("штор", "жалюзи", "рулон", "день ночь"),
        "OUTSIDE_HEATING": ("радиатор", "батаре", "конвектор", "отоплен"),
        "OUTSIDE_REAL_ESTATE": ("дом", "барнхаус", "дача", "апартамент", "гостиная", "баня", "бассейн", "лес", "проект"),
    }
    if cid in exact_requirements and not anym(p, exact_requirements[cid]):
        out.append(("TASK_TOKEN_MISMATCH", f"{cid} lacks its defining task marker"))

    if cid == "WINDOW_SELECTION_INFO" and anym(p, ("сделать", "изготов", "снять", "вставить", "открыть", "регулир", "ремонт")):
        out.append(("SELECTION_WITH_OTHER_ACTION", "selection cluster contains a different explicit action"))
    if cid == "WINDOW_REPAIR" and anym(p, ("отмыть", "очистить", "жидкий пластик", "средство для ремонта")):
        out.append(("REPAIR_SERVICE_WITH_CARE_OR_MATERIAL", "repair service contains care/material wording"))
    if cid == "WINDOW_INSTALLATION" and anym(p, ("сетк", "москит", "штор", "жалюзи", "фурнитур", "подоконник своими руками")):
        out.append(("INSTALLATION_WITH_OTHER_OBJECT", "window-installation cluster appears to target an accessory/other object"))

    return out


def main():
    with ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    flagged = []
    counts = Counter()
    for r in rows:
        if r["input_disposition"] not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit(r):
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
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)
    summary = {
        "status": "AUDIT_GENERATED__MANUAL_REVIEW_REQUIRED",
        "active_rows_scanned": sum(r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "meaning": "Heuristic adversarial audit only; flags must be manually reviewed and cannot self-accept or self-reject Step 10.",
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
