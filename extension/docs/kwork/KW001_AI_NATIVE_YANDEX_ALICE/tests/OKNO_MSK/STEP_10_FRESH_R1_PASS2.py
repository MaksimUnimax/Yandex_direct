#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv"
TAXONOMY = ROOT / "STEP_10_FRESH_R1_TAXONOMY.tsv"
DIRECT = ROOT / "STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv"
OUT_ASSIGN = ROOT / "STEP_10_FRESH_R1_ASSIGNMENT.tsv"
OUT_SUMMARY = ROOT / "STEP_10_FRESH_R1_CLUSTER_SUMMARY.tsv"
OUT_QA = ROOT / "STEP_10_FRESH_R1_ASSIGNMENT_QA.json"

ACTIVE_DISPOSITIONS = {"CORE_CANDIDATE", "REVIEW_SEARCH"}
DEFERRED_DISPOSITION = "REVIEW_DEFERRED"
EXCLUDED_DISPOSITION = "EXCLUDED_PRESERVED"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower().replace("ё", "е")).strip()


def has(p: str, s: str) -> bool:
    return re.search(p, s, re.I) is not None


def modifiers(q: str) -> str:
    mods = []
    patterns = [
        ("geo", r"\b(москв\w*|спб|петербург\w*|район\w*|округ\w*|област\w*|метро|город\w*)\b"),
        ("price", r"\b(цен\w*|стоим\w*|сколько стоит|дешев\w*|недорог\w*|прайс\w*)\b"),
        ("finance", r"\b(рассроч\w*|кредит\w*|ипотек\w*)\b"),
        ("seller_source", r"\b(производител\w*|завод\w*|фабрик\w*|от производителя|официальн\w*)\b"),
        ("house_series", r"\b(хрущев\w*|сталин\w*|брежнев\w*|п[- ]?44\w*|корабл\w*|серии? дома|дом серии)\b"),
        ("rehau", r"\b(rehau|рехау)\b"),
        ("brand_other", r"\b(kbe|кбе|veka|века|brusbox|брусбокс|provedal|проведал|fapim)\b"),
        ("wood", r"\b(деревянн\w*|дерев\w*|брус\w*)\b"),
        ("aluminium", r"\b(алюмини\w*)\b"),
        ("pvc", r"\b(пвх|пластиков\w*)\b"),
        ("frameless", r"\b(безрамн\w*)\b"),
        ("panoramic", r"\b(панорамн\w*)\b"),
        ("french", r"\b(французск\w*)\b"),
        ("warm", r"\b(тепл\w*|теплое остекление|теплый балкон)\b"),
        ("cold", r"\b(холодн\w*)\b"),
    ]
    for name, pat in patterns:
        if has(pat, q):
            mods.append(name)
    return ";".join(mods)


def info_signal(q: str) -> bool:
    return has(r"\b(как|какие|какой|какая|что такое|что лучше|почему|зачем|можно ли|стоит ли|выбрать|выбор|сравн\w*|отлич\w*|разниц\w*|отзыв\w*|размер\w*|габарит\w*|ширин\w*|высот\w*|устройств\w*|конструкц\w*|характерист\w*|инструкц\w*|схем\w*|видео|фото|виды|тип\w*)\b", q)


def diy_signal(q: str) -> bool:
    return has(r"\b(своими руками|самостоятельн\w*|самому|самой|как сделать|как установить|как поставить|как заменить|как отремонтировать|инструкц\w*|видео)\b", q)


def commercial_signal(q: str) -> bool:
    return has(r"\b(купить|заказать|цена|цены|стоимость|недорого|дешево|под ключ|производитель|от производителя|продажа|магазин|каталог|сколько стоит)\b", q)


def classify(q0: str) -> tuple[str | None, str, str]:
    q = norm(q0)

    if has(r"\b(штор\w*|жалюз\w*|занавес\w*|карниз\w*)\b", q):
        return "OUTSIDE_CURTAINS_BLINDS", "HIGH", "curtain/blind job is outside core window/glazing task"
    if has(r"\b(б/у|бу окна|бу двер|подержан\w*|авито|с рук)\b", q):
        return "OUTSIDE_USED_MARKET", "HIGH", "used/second-hand market intent"
    if has(r"\bмежкомнатн\w*\b", q) and has(r"\bдвер\w*\b", q):
        return "OUTSIDE_INTERIOR_DOORS", "HIGH", "interior-door job outside target PVC exterior/balcony-door scope"
    if has(r"\b(радиатор\w*|батаре\w*|конвектор\w*|отоплен\w*|кондиционер\w*|вентиляц\w*|теплый пол|теплого пола)\b", q):
        return "OUTSIDE_HEATING_HVAC", "HIGH", "heating/HVAC result outside window/glazing task"
    if has(r"\b(недвижимост\w*|квартир\w+ с панорамн|дом\w+ с панорамн|проект дома|проекты домов|архитектур\w*|фасад\w*|интерьер\w*)\b", q) and not commercial_signal(q) and not has(r"\b(установ\w*|монтаж\w*|остекл\w*|ремонт\w*)\b", q):
        return "OUTSIDE_REAL_ESTATE_ARCHITECTURE", "MEDIUM", "architecture/real-estate result dominates"

    if has(r"\b(официальн\w*|официальный сайт|сайт производителя|сайт rehau|сайт рехау)\b", q) and has(r"\b(rehau|рехау|kbe|кбе|veka|века|brusbox|брусбокс|производител\w*)\b", q):
        return "NAVIGATION_BRAND_SITE", "HIGH", "official/branded destination intent"

    if has(r"\b(москит\w*|от комаров|сетка на окно|сетки на окна)\b", q):
        if has(r"\b(ремонт\w*|почин\w*|восстанов\w*)\b", q):
            return "MOSQUITO_NET_REPAIR_SERVICE", "HIGH", "mosquito-net repair action"
        if has(r"\b(установ\w*|монтаж\w*|поставить)\b", q) and not diy_signal(q):
            return "MOSQUITO_NET_INSTALLATION_SERVICE", "HIGH", "mosquito-net installation action"
        if has(r"\b(выбрать|выбор|какая|какие|виды|тип\w*|лучше)\b", q):
            return "MOSQUITO_NET_SELECTION_INFO", "HIGH", "mosquito-net selection information"
        return "MOSQUITO_NET_SHOPPING", "HIGH", "mosquito-net product/shopping job"

    hardware = has(r"\b(фурнитур\w*|оконн\w+ ручк\w*|ручк\w+ для окон|петл\w+ для окон|оконн\w+ петл\w*|замк\w+ для окон|оконн\w+ замк\w*)\b", q)
    accessory = has(r"\b(аксессуар\w*|уплотнител\w*|стеклопакет\w*|подоконник\w*)\b", q)
    if has(r"\bподоконник\w*\b", q) and has(r"\b(ремонт\w*|восстанов\w*|реставрац\w*|почин\w*)\b", q):
        return "WINDOWSILL_REPAIR_SERVICE", "HIGH", "windowsill-specific repair result"
    if (hardware or accessory) and has(r"\b(ремонт\w*|почин\w*|регулиров\w*|замен\w*)\b", q):
        if diy_signal(q):
            return "WINDOW_REPAIR_DIY_INFO", "HIGH", "DIY component/window repair"
        return "WINDOW_REPAIR_SERVICE", "HIGH", "component-focused professional repair"
    if has(r"\bподоконник\w*\b", q) and has(r"\b(установ\w*|монтаж\w*)\b", q):
        if diy_signal(q):
            return "WINDOW_FINISHING_DIY_INFO", "HIGH", "DIY windowsill/finishing installation"
        return "WINDOW_FINISHING_SERVICE", "HIGH", "professional windowsill/finishing installation"
    if hardware:
        if info_signal(q) and not commercial_signal(q):
            return "WINDOW_HARDWARE_INFO", "HIGH", "window-hardware information/selection"
        return "WINDOW_HARDWARE_SHOPPING", "HIGH", "window-hardware shopping"
    if accessory:
        if has(r"\b(выбрать|выбор|какие|какой|виды|тип\w*|лучше)\b", q) and not commercial_signal(q):
            return "WINDOW_ACCESSORY_SELECTION_INFO", "HIGH", "window-accessory selection information"
        if info_signal(q) and not commercial_signal(q):
            return "WINDOW_PRODUCT_TECH_INFO", "MEDIUM", "component/accessory technical information"
        return "WINDOW_ACCESSORIES_SHOPPING", "MEDIUM", "general window accessory/product shopping"

    if has(r"\bмягк\w+ окн\w*\b", q):
        if info_signal(q) and not commercial_signal(q):
            return "WINDOW_PRODUCT_TECH_INFO", "MEDIUM", "soft-window informational question"
        return "SOFT_WINDOWS_COMMERCIAL", "HIGH", "distinct soft-window product"

    balcony = has(r"\b(балкон\w*|лоджи\w*)\b", q)
    glazing = has(r"\b(остекл\w*|застекл\w*)\b", q)
    if balcony:
        if has(r"\b(демонтаж\w*|снять остекление|разобрать остекление)\b", q):
            return "WINDOW_DEMOLITION_SERVICE", "HIGH", "balcony glazing demolition action"
        if has(r"\b(ремонт балкон\w*|отделк\w+ балкон\w*|балкон\w+ отделк\w*)\b", q) and glazing:
            return "BALCONY_RENOVATION_WITH_GLAZING", "HIGH", "bundled balcony renovation and glazing"
        if not glazing and has(r"\b(без остекления|открыт\w+ балкон\w*)\b", q) and has(r"\b(отделк\w*|ремонт\w*|обустрой\w*|дизайн\w*)\b", q):
            return "OPEN_BALCONY_FINISHING", "HIGH", "open-balcony finishing separated from glazing"
        if glazing or has(r"\b(балкон\w+ под ключ|застеклить балкон|окна на балкон|окна для лоджии)\b", q):
            if info_signal(q) and not commercial_signal(q) and not has(r"\b(под ключ|заказать|цена|стоимость)\b", q):
                if has(r"\b(разрешен\w*|разрешение|согласован\w*|закон\w*|можно ли остекл)\b", q):
                    return "GLAZING_PERMISSION_INFO", "HIGH", "permission/legal glazing question"
                return "BALCONY_GLAZING_INFO", "MEDIUM", "balcony-glazing informational job"
            if has(r"\b(с выносом|вынос\w*)\b", q):
                return "BALCONY_GLAZING_EXTENSION_SERVICE", "HIGH", "balcony extension/outset construction scope"
            if has(r"\b(с крышей|крыша|кровл\w*)\b", q):
                return "BALCONY_GLAZING_ROOF_SERVICE", "HIGH", "balcony roof construction scope"
            if has(r"\b(тепл\w*|теплое остекление|теплый балкон)\b", q):
                return "BALCONY_GLAZING_WARM", "HIGH", "warm-glazing result"
            if has(r"\b(холодн\w*)\b", q):
                return "BALCONY_GLAZING_COLD", "HIGH", "cold-glazing result"
            return "BALCONY_GLAZING_GENERAL", "HIGH", "general balcony/loggia glazing service"

    structure = has(r"\b(веранд\w*|террас\w*|беседк\w*|крыльц\w*)\b", q)
    if structure and glazing:
        if has(r"\b(разрешен\w*|разрешение|согласован\w*|закон\w*)\b", q):
            return "GLAZING_PERMISSION_INFO", "HIGH", "permission/legal glazing question"
        if diy_signal(q):
            return "GLAZING_DIY_INFO", "HIGH", "DIY outdoor-structure glazing"
        if info_signal(q) and not commercial_signal(q):
            return "GLAZING_SELECTION_INFO", "MEDIUM", "outdoor-structure glazing information/selection"
        return "OUTDOOR_STRUCTURE_GLAZING", "HIGH", "glazing service for outdoor structure"

    pvc_door = has(r"\bдвер\w*\b", q) and has(r"\b(пластиков\w*|пвх|rehau|рехау)\b", q)
    if pvc_door:
        if has(r"\b(ремонт\w*|регулиров\w*|почин\w*)\b", q):
            if diy_signal(q):
                return "PVC_DOOR_INFO", "MEDIUM", "PVC-door DIY/repair information"
            return "PVC_DOOR_REPAIR_SERVICE", "HIGH", "professional PVC-door repair"
        if has(r"\b(замена двер\w*|заменить двер\w*|поменять двер\w*)\b", q):
            return "PVC_DOOR_REPLACEMENT_SERVICE", "HIGH", "PVC-door replacement"
        if has(r"\b(установ\w*|монтаж\w*)\b", q) and not has(r"\bбез установки\b", q):
            if diy_signal(q):
                return "PVC_DOOR_INFO", "MEDIUM", "PVC-door installation information"
            return "PVC_DOOR_INSTALLATION_SERVICE", "HIGH", "professional PVC-door installation"
        if info_signal(q) and not commercial_signal(q):
            return "PVC_DOOR_INFO", "HIGH", "PVC-door informational job"
        return "PVC_DOORS_COMMERCIAL", "HIGH", "PVC-door commercial product job"

    if has(r"\b(демонтаж\w*|демонтировать|снять окно|разобрать окно)\b", q):
        return "WINDOW_DEMOLITION_SERVICE", "HIGH", "window demolition/dismantling action"
    if has(r"\b(замена окон|замена окна|заменить окно|поменять окно|замена пластиковых окон|заменить пластиковые окна)\b", q):
        return "WINDOW_REPLACEMENT_SERVICE", "HIGH", "window replacement lifecycle action"
    if has(r"\b(ремонт\w*|почин\w*|регулиров\w*)\b", q) and has(r"\b(окн\w*|стеклопакет\w*|рама\w*)\b", q):
        if diy_signal(q):
            return "WINDOW_REPAIR_DIY_INFO", "HIGH", "DIY window repair"
        return "WINDOW_REPAIR_SERVICE", "HIGH", "professional window repair"
    if has(r"\b(откос\w*|отделк\w+ окон\w*|отделка окна|обналич\w*)\b", q):
        if diy_signal(q):
            return "WINDOW_FINISHING_DIY_INFO", "HIGH", "DIY window finishing"
        if commercial_signal(q) or has(r"\b(монтаж\w*|установ\w*|сделать)\b", q):
            return "WINDOW_FINISHING_SERVICE", "MEDIUM", "professional window finishing"
    if has(r"\b(замер\w*|измерить проем|измерить окно|как замерить|как измерить)\b", q):
        return "WINDOW_MEASUREMENT_INFO", "HIGH", "window measurement task"
    if has(r"\b(установ\w*|монтаж\w*|вставить окно|поставить окно)\b", q) and has(r"\bокн\w*\b", q) and not has(r"\bбез установки\b", q):
        if diy_signal(q) or (info_signal(q) and not commercial_signal(q)):
            return "WINDOW_INSTALLATION_DIY_INFO", "HIGH", "DIY/informational window installation"
        return "WINDOW_INSTALLATION_SERVICE", "HIGH", "professional window installation"

    if has(r"\b(мыть\w*|помыть|чистить|очистить|уход\w*|смаз\w*)\b", q) and has(r"\bокн\w*\b", q):
        return "WINDOW_CARE_INFO", "HIGH", "window care/maintenance information"
    if has(r"\b(отзыв\w*|мнение\w*)\b", q) and has(r"\b(окн\w*|rehau|рехау|профил\w*)\b", q):
        return "WINDOW_REVIEWS_INFO", "HIGH", "reviews/experience information"
    if has(r"\b(сравн\w*|или|vs|против|отлич\w*|разниц\w*)\b", q) and has(r"\b(окн\w*|rehau|рехау|kbe|кбе|veka|века|профил\w*)\b", q):
        return "WINDOW_COMPARISON_INFO", "MEDIUM", "product/brand comparison information"
    if has(r"\b(выбрать|выбор|какие окна|какое окно|какой профиль|что лучше)\b", q):
        return "WINDOW_SELECTION_INFO", "HIGH", "window/product selection information"
    if has(r"\b(размер\w*|габарит\w*|ширин\w*|высот\w*|стандартн\w+ окн\w*)\b", q) and has(r"\b(окн\w*|rehau|рехау|балкон\w*|двер\w*)\b", q):
        return "WINDOW_DIMENSIONS_INFO", "HIGH", "window/product dimensions information"
    if has(r"\b(частн\w+ дом|загородн\w+ дом|коттедж\w*)\b", q) and info_signal(q) and not commercial_signal(q):
        return "PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "MEDIUM", "private-house planning/requirements information"
    if has(r"\b(разрешен\w*|разрешение|согласован\w*|закон\w*)\b", q) and glazing:
        return "GLAZING_PERMISSION_INFO", "HIGH", "permission/legal glazing information"
    if glazing and diy_signal(q):
        return "GLAZING_DIY_INFO", "HIGH", "DIY glazing information"
    if glazing and has(r"\b(выбрать|выбор|какое остекление|какие виды|виды остекления|лучше)\b", q):
        return "GLAZING_SELECTION_INFO", "HIGH", "glazing selection information"
    if has(r"\b(фото|фотографии|картинк\w*|дизайн\w*|идеи|пример\w*)\b", q) and has(r"\b(окн\w*|остекл\w*|балкон\w*|веранд\w*|террас\w*)\b", q):
        return "GLAZING_DESIGN_INSPIRATION", "MEDIUM", "design/photo inspiration job"
    if diy_signal(q) and has(r"\bокн\w*\b", q):
        return "WINDOW_INSTALLATION_DIY_INFO", "LOW", "generic window DIY information; conservative assignment"
    if info_signal(q) and has(r"\b(окн\w*|профил\w*|стеклопакет\w*|rehau|рехау)\b", q):
        return "WINDOW_PRODUCT_TECH_INFO", "MEDIUM", "window/product technical or definition information"

    if has(r"\b(мансардн\w+ окн\w*|окн\w+ (на|для) крыш\w*|кровельн\w+ окн\w*)\b", q):
        return "ROOF_WINDOWS_COMMERCIAL", "HIGH", "roof/mansard window product"
    if has(r"\b(французск\w+ окн\w*)\b", q):
        return "FRENCH_WINDOWS_COMMERCIAL", "HIGH", "French-window product/form job"
    if has(r"\bпанорамн\w+ окн\w*\b", q):
        return "PANORAMIC_WINDOWS_COMMERCIAL", "HIGH", "panoramic-window product/form job"
    if has(r"\b(деревоалюмини\w*|деревянно[- ]алюмини\w*|дерево[- ]алюмини\w*)\b", q):
        return "TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL", "HIGH", "timber-aluminium hybrid product"
    if has(r"\bдеревянн\w+ окн\w*\b", q):
        return "WOOD_WINDOWS_COMMERCIAL", "HIGH", "wooden-window product"
    if has(r"\bалюмини\w+ окн\w*\b", q):
        return "ALUMINIUM_WINDOWS_COMMERCIAL", "HIGH", "aluminium-window product"
    if has(r"\b(rehau|рехау)\b", q) and has(r"\b(окн\w*|профил\w*|систем\w*)\b", q):
        return "REHAU_WINDOWS_COMMERCIAL", "HIGH", "Rehau branded product-family commercial job"
    if has(r"\bокн\w*\b", q) and has(r"\bдвер\w*\b", q) and not info_signal(q):
        return "WINDOWS_DOORS_COMBINED_COMMERCIAL", "MEDIUM", "combined window-and-door commercial job"
    if has(r"\b(пластиков\w+ окн\w*|окн\w+ пвх|пвх окн\w*)\b", q):
        return "PVC_WINDOWS_COMMERCIAL", "HIGH", "PVC-window commercial product job"

    if glazing:
        if commercial_signal(q):
            return "GENERAL_GLAZING_SERVICE", "MEDIUM", "generic commercial glazing service"
        return None, "LOW", "glazing phrase lacks enough task evidence for frozen assignment"
    if has(r"\bокн\w*\b", q):
        if commercial_signal(q):
            return "WINDOWS_COMMERCIAL_GENERAL", "MEDIUM", "generic commercial window job"
        return "WINDOWS_COMMERCIAL_GENERAL", "LOW", "generic window phrase without explicit action"

    return None, "LOW", "no stable frozen-task match"


def main() -> None:
    with TAXONOMY.open(encoding="utf-8", newline="") as f:
        taxonomy_rows = list(csv.DictReader(f, delimiter="\t"))
    allowed = {r["cluster_id"] for r in taxonomy_rows}
    taxonomy_meta = {r["cluster_id"]: r for r in taxonomy_rows}

    direct_queries = set()
    if DIRECT.exists():
        with DIRECT.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                direct_queries.add(norm(r["query"]))

    rows_out = []
    active_count = 0
    assigned_count = 0
    search_required_count = 0
    preserved_deferred = 0
    preserved_excluded = 0
    unknown_cluster_ids = set()

    with SOURCE.open(encoding="utf-8", newline="") as f:
        src_rows = list(csv.DictReader(f, delimiter="\t"))

    for r in src_rows:
        phrase = r["phrase"]
        disp = r["search_stage_disposition"]
        direct = norm(phrase) in direct_queries
        cluster_id = ""
        assignment_status = ""
        assignment_confidence = ""
        reason = ""
        evidence_mode = "DIRECT_SERP" if direct else "SEMANTIC_ONLY"

        if disp == DEFERRED_DISPOSITION:
            assignment_status = "PRESERVED_DEFERRED"
            evidence_mode = "UPSTREAM_PRESERVED"
            preserved_deferred += 1
        elif disp == EXCLUDED_DISPOSITION:
            assignment_status = "PRESERVED_EXCLUDED"
            evidence_mode = "UPSTREAM_PRESERVED"
            preserved_excluded += 1
        elif disp in ACTIVE_DISPOSITIONS:
            active_count += 1
            cid, conf, why = classify(phrase)
            if cid and cid in allowed and not (disp == "REVIEW_SEARCH" and conf == "LOW" and not direct):
                cluster_id = cid
                assignment_status = "ASSIGNED"
                assignment_confidence = conf
                reason = why
                assigned_count += 1
            else:
                assignment_status = "SEARCH_REQUIRED"
                assignment_confidence = conf
                reason = why
                search_required_count += 1
        else:
            raise RuntimeError(f"unexpected search_stage_disposition={disp!r} for {phrase!r}")

        if cluster_id and cluster_id not in allowed:
            unknown_cluster_ids.add(cluster_id)

        rows_out.append({
            "phrase": phrase,
            "source_disposition": disp,
            "source_corrected_status": r["corrected_status"],
            "source_corrected_reason": r["corrected_reason"],
            "source_semantic_confidence": r["semantic_confidence"],
            "assignment_status": assignment_status,
            "cluster_id": cluster_id,
            "assignment_confidence": assignment_confidence,
            "evidence_mode": evidence_mode,
            "modifiers": modifiers(norm(phrase)),
            "assignment_reason": reason,
        })

    if len(src_rows) != 2840:
        raise RuntimeError(f"expected 2840 source rows, got {len(src_rows)}")
    if active_count != 2332:
        raise RuntimeError(f"expected 2332 active rows, got {active_count}")
    if preserved_deferred != 174:
        raise RuntimeError(f"expected 174 deferred rows, got {preserved_deferred}")
    if preserved_excluded != 334:
        raise RuntimeError(f"expected 334 excluded rows, got {preserved_excluded}")
    if assigned_count + search_required_count != active_count:
        raise RuntimeError("active accounting mismatch")
    if unknown_cluster_ids:
        raise RuntimeError(f"unknown cluster ids: {sorted(unknown_cluster_ids)}")

    fields = [
        "phrase", "source_disposition", "source_corrected_status", "source_corrected_reason",
        "source_semantic_confidence", "assignment_status", "cluster_id", "assignment_confidence",
        "evidence_mode", "modifiers", "assignment_reason",
    ]
    with OUT_ASSIGN.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows_out)

    counts = Counter(r["cluster_id"] for r in rows_out if r["assignment_status"] == "ASSIGNED")
    with OUT_SUMMARY.open("w", encoding="utf-8", newline="") as f:
        fields2 = ["cluster_id", "family", "user_task", "intent_type", "business_fit", "assigned_rows"]
        w = csv.DictWriter(f, fieldnames=fields2, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for cid in sorted(allowed):
            m = taxonomy_meta[cid]
            w.writerow({
                "cluster_id": cid,
                "family": m["family"],
                "user_task": m["user_task"],
                "intent_type": m["intent_type"],
                "business_fit": m["business_fit"],
                "assigned_rows": counts.get(cid, 0),
            })

    qa = {
        "status": "PASS2_MACHINE_ACCOUNTING_PASS__PASS3_INDEPENDENT_SEMANTIC_QA_REQUIRED",
        "source_rows": len(src_rows),
        "active_rows": active_count,
        "assigned_active_rows": assigned_count,
        "search_required_active_rows": search_required_count,
        "preserved_deferred_rows": preserved_deferred,
        "preserved_excluded_rows": preserved_excluded,
        "active_accounted_rows": assigned_count + search_required_count,
        "taxonomy_cluster_ids": len(allowed),
        "used_cluster_ids": len(counts),
        "zero_assignment_cluster_ids": sorted(cid for cid in allowed if counts.get(cid, 0) == 0),
        "unknown_cluster_ids": sorted(unknown_cluster_ids),
        "direct_serp_rows_in_full_ledger": sum(1 for r in rows_out if r["evidence_mode"] == "DIRECT_SERP"),
        "old_step10_input_used": False,
        "blind84_input_used": False,
        "target_cluster_count_used": False,
        "pass2_created_new_cluster": False,
        "pass3_independent_semantic_qa_required": True,
        "pass3_complete": False,
    }
    OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False))


if __name__ == "__main__":
    main()
