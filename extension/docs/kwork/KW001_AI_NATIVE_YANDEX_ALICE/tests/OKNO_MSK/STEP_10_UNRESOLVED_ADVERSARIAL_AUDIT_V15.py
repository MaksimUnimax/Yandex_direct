#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter

import STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT as old


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


def is_private_house(p: str) -> bool:
    return anym(p, (
        "частного дома", "частных домов", "частный дом", "частные дома", "частном доме",
        "загородного дома", "загородный дом", "загородных домов", "для дома",
    ))


def is_house_series(p: str) -> bool:
    return bool(re.search(r"\bп\s*[- ]?\s*\d{1,3}\s*[а-я]?\b", p))


def architecture_subject_with_windows(p: str) -> bool:
    return bool(re.search(
        r"\b(?:дом\w*|квартир\w*|кв|комнат\w*|спальн\w*|кухн\w*|зал|лофт\w*|бан\w*|"
        r"апартамент\w*|пристройк\w*|беседк\w*|гостин\w*|одноэтажн\w*|проект\w*)\b"
        r".{0,45}\bс\b.{0,35}(?:панорам|француз)", p
    ))


def audit_v15(r: dict[str, str]) -> list[tuple[str, str]]:
    if r["cluster_evidence_state"] != "SEARCH_REQUIRED":
        return []

    p = n(r["phrase"])
    out: list[tuple[str, str]] = []
    windowish = anym(p, ("окн", "окон", "стеклопак", "остеклен", "застекл"))
    panoramic = "панорам" in p and windowish
    french = "француз" in p and (windowish or "балконный блок" in p)
    commercial = anym(p, (
        "купить", "заказать", "цена", "цены", "стоимость", "сколько стоит", "сколько стоят",
        "производ", "под ключ", "москва", "подмосков",
    ))

    # Direct exact SERP should never remain unresolved unless the evidence itself is
    # explicitly mixed/ambiguous; the caller suppresses that known intentional case.
    if r["step09_probe_id"]:
        out.append(("DIRECT_SERP_LEFT_UNRESOLVED", "Exact Step-09 evidence exists; verify that unresolved state is intentionally mixed rather than a missing semantic class"))

    # Clear object-specific glazing service (excluding content/DIY/selection variants).
    if anym(p, ("остеклен", "застекл")) and anym(p, ("балкон", "лоджи", "веранд", "террас", "бесед", "крыльц")):
        if not anym(p, ("видео", "своими руками", "самостоятель", "пошаг", "фото", "дизайн", "виды", "варианты", "плюсы", "минусы", "как выбрать", "конструкция", "схема")):
            out.append(("UNRESOLVED_CLEAR_OBJECT_GLAZING", "Object-specific glazing service has enough semantic evidence to assign a Step-10 task"))

    # Clear private-house tasks, with broader Russian morphology than V10 audit.
    if windowish and is_private_house(p):
        if anym(p, ("требован", "норматив", "норма ", "вентиляц", "котельн", "газов")) and not commercial:
            out.append(("UNRESOLVED_CLEAR_PRIVATE_HOUSE_REQUIREMENTS", "Private-house phrase explicitly asks about requirements/special-room conditions"))
        elif anym(p, ("вариант", "виды", "образц", "как выбрать", "выбрать", "выбираем", "какие окна", "лучшие окна")):
            out.append(("UNRESOLVED_CLEAR_PRIVATE_HOUSE_SELECTION", "Private-house phrase has explicit selection/types wording"))
        elif commercial or anym(p, ("для кухни", "для крыши")):
            out.append(("UNRESOLVED_CLEAR_PRIVATE_HOUSE_PRODUCT", "Private-house phrase has explicit product/price/use-case demand"))

    # P-series house windows are a clear house-series product/use-case task.
    if windowish and is_house_series(p) and not anym(p, ("остеклен", "застекл")):
        out.append(("UNRESOLVED_CLEAR_HOUSE_SERIES_WINDOWS", "Window phrase contains an explicit P-series house modifier"))

    # Panoramic/French repair is an explicit service task.
    if (panoramic or french) and anym(p, ("ремонт", "регулир", "почин", "провис")):
        out.append(("UNRESOLVED_CLEAR_SPECIFIC_WINDOW_REPAIR", "Panoramic/French-window phrase contains an explicit repair/adjustment action"))

    # Strong architecture/project context is outside the window-purchase core.
    if (panoramic or french) and architecture_subject_with_windows(p):
        out.append(("UNRESOLVED_CLEAR_ARCHITECTURE_CONTEXT", "Dwelling/project is the head object with panoramic/French windows as an attribute"))

    # Explicit window definition/naming.
    if (panoramic or french) and anym(p, ("что такое", "как называется", "как называются", "как зовется")):
        out.append(("UNRESOLVED_CLEAR_WINDOW_DEFINITION", "Panoramic/French-window phrase explicitly asks for definition/naming"))

    # Strong dimensions: words or explicit AxB / decimal size format.
    dim_pattern = bool(re.search(r"\b\d+(?:[.,]\d+)?\s*(?:на|x|х)\s*\d+(?:[.,]\d+)?\b", p))
    pan_decimal = bool(re.search(r"(?:панорам\w*\s+окн\w*|окн\w*\s+панорам\w*)\s+\d+[.,]\d+\b", p))
    if windowish and (anym(p, ("размер", "ширина", "высота", "габарит")) or dim_pattern or pan_decimal) and not commercial:
        out.append(("UNRESOLVED_CLEAR_WINDOW_DIMENSIONS", "Window phrase has explicit dimensions/size information wording"))

    # Clear accessories/components around panoramic/French/soft windows.
    if (panoramic or french or ("мягк" in p and windowish)) and anym(p, ("замок", "фурнитур", "ручк", "петл", "створк", "решетк", "раскладк", "шпрос", "ставн", "огражден", "подоконник")):
        out.append(("UNRESOLVED_CLEAR_WINDOW_COMPONENT", "Specific-window phrase explicitly names a component/accessory"))

    # Clear whole-window replacement/conversion.
    if (panoramic or french) and anym(p, ("замена окна", "замена окон", "заменить окно", "заменить окна", "замена балконного блока")):
        out.append(("UNRESOLVED_CLEAR_WINDOW_REPLACEMENT", "Specific-window phrase explicitly asks for whole-window/balcony-block replacement"))

    # Clear panoramic/French product demand and product variants. Deliberately exclude
    # weak context-only wording such as 'панорамные окна в здании'.
    specific_product = anym(p, (
        "купить", "заказать", "цена", "цены", "стоимость", "сколько стоит", "сколько стоят",
        "производ", "под ключ", "москва", "подмосков", "раздвиж", "открывающ", "треугольн", "стеклянн",
        "стеклопак", "в пол", "с двер", "на крыш", "на террас", "на балкон", "на лоджи", "для загородного дома",
        "готов", "больш", "высок", "маленьк", "широк", "узк", "элитн", "ароч", "балконный блок",
    ))
    if (panoramic or french) and specific_product:
        out.append(("UNRESOLVED_CLEAR_SPECIFIC_WINDOW_PRODUCT", "Panoramic/French-window phrase contains explicit commercial/product/configuration wording"))

    # General 'types/variants of windows' is informational if no stronger action exists.
    if windowish and anym(p, ("виды", "варианты")) and not commercial and not anym(p, ("установ", "монтаж", "ремонт", "регулир")):
        out.append(("UNRESOLVED_CLEAR_WINDOW_TYPES_INFO", "Window phrase explicitly asks for types/variants"))

    # Entrance door with a window is clearly a door-headed product.
    if "входн" in p and "двер" in p and windowish and not anym(p, ("пластик", "пвх")):
        out.append(("UNRESOLVED_CLEAR_ENTRY_DOOR", "Entrance door is the head object; window is a modifier"))

    return out


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    unresolved = 0
    intentionally_mixed_direct = []

    for r in rows:
        if r["cluster_evidence_state"] != "SEARCH_REQUIRED":
            continue
        unresolved += 1

        direct_is_explicitly_mixed = bool(
            r["step09_probe_id"]
            and (r["dominant_result_type"].startswith("MIXED_") or "AMBIGUOUS" in r["step09_handoff"])
            and any(x in r["assignment_reason"].casefold() for x in ("mixed", "ambiguous", "неоднознач", "boundary"))
        )
        if direct_is_explicitly_mixed:
            intentionally_mixed_direct.append({
                "phrase": r["phrase"],
                "probe_id": r["step09_probe_id"],
                "dominant_result_type": r["dominant_result_type"],
                "step09_handoff": r["step09_handoff"],
            })

        for code, reason in audit_v15(r):
            if code == "DIRECT_SERP_LEFT_UNRESOLVED" and direct_is_explicitly_mixed:
                continue
            counts[code] += 1
            flagged.append({
                "audit_code": code,
                "phrase": r["phrase"],
                "step09_probe_id": r["step09_probe_id"],
                "observed_serp_job": r["observed_serp_job"],
                "dominant_result_type": r["dominant_result_type"],
                "reason": reason,
            })

    fields = ["audit_code", "phrase", "step09_probe_id", "observed_serp_job", "dominant_result_type", "reason"]
    with old.OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)

    summary = {
        "status": "AUDIT_GENERATED__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V15",
        "search_required_rows_scanned": unresolved,
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "audit_counts": dict(sorted(counts.items())),
        "intentionally_mixed_direct_rows": len(intentionally_mixed_direct),
        "intentionally_mixed_direct_examples": intentionally_mixed_direct,
        "meaning": "V15 unresolved audit flags semantically determinate rows that should not remain SEARCH_REQUIRED. Zero flags is necessary but manual semantic QA remains mandatory.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
