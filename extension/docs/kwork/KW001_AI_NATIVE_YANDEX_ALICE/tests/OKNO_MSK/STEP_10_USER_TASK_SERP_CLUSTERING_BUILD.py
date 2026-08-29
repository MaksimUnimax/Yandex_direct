#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / "STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv"
DECISIONS = BASE / "STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv"
COMPARISONS = BASE / "STEP_09_SERP_COMPARISONS.tsv"
OUT_ASSIGN = BASE / "STEP_10_CLUSTER_ASSIGNMENTS.tsv"
OUT_SUMMARY = BASE / "STEP_10_CLUSTER_SUMMARY.tsv"
OUT_BOUNDARY = BASE / "STEP_10_BOUNDARY_REVIEW.tsv"
OUT_QA = BASE / "STEP_10_QA.json"
OUT_SAMPLE = BASE / "STEP_10_SEMANTIC_QA_SAMPLE.tsv"

EXPECTED = {
    "total": 2840,
    "CORE_CANDIDATE": 1388,
    "REVIEW_SEARCH": 944,
    "REVIEW_DEFERRED": 174,
    "EXCLUDED_PRESERVED": 334,
    "active": 2332,
    "direct_probes": 75,
    "duplicate_comparisons": 8,
}

# Job-specific user-task taxonomy. These labels are analytical working states only;
# they do not assign an existing URL or structural action.
TASKS = {
    "PVC_WINDOWS_COMMERCIAL": ("Покупка пластиковых окон", "COMMERCIAL_PRODUCT", "FIT"),
    "PVC_WINDOWS_GEO": ("Покупка пластиковых окон с гео-модификатором", "COMMERCIAL_PRODUCT", "FIT"),
    "PVC_WINDOWS_MANUFACTURER": ("Пластиковые окна от производителя", "COMMERCIAL_PRODUCT", "FIT"),
    "REHAU_WINDOWS_COMMERCIAL": ("Покупка окон Rehau", "COMMERCIAL_PRODUCT", "FIT"),
    "REHAU_PRODUCT_SUBTYPE": ("Выбор конкретной системы/модели Rehau", "COMMERCIAL_PRODUCT", "FIT"),
    "ALUMINIUM_WINDOWS_COMMERCIAL": ("Покупка алюминиевых окон", "COMMERCIAL_PRODUCT", "FIT"),
    "PROVEDAL_WINDOWS_COMMERCIAL": ("Окна/системы Provedal", "COMMERCIAL_PRODUCT", "FIT"),
    "WOOD_WINDOWS_COMMERCIAL": ("Покупка деревянных или дерево-алюминиевых окон", "COMMERCIAL_PRODUCT", "ADJACENT"),
    "PANORAMIC_WINDOWS_COMMERCIAL": ("Покупка панорамных окон", "COMMERCIAL_PRODUCT", "FIT"),
    "PVC_DOORS_COMMERCIAL": ("Покупка пластиковых дверей", "COMMERCIAL_PRODUCT", "FIT"),
    "WINDOW_FINANCE": ("Покупка окон в рассрочку/кредит", "COMMERCIAL_PRODUCT_FINANCE", "FIT"),
    "BALCONY_GLAZING": ("Остекление балкона/лоджии", "COMMERCIAL_SERVICE", "FIT"),
    "BALCONY_GLAZING_WARM": ("Тёплое остекление балкона/лоджии", "COMMERCIAL_SERVICE", "FIT"),
    "BALCONY_GLAZING_COLD": ("Холодное остекление балкона/лоджии", "COMMERCIAL_SERVICE", "FIT"),
    "BALCONY_GLAZING_ROOF": ("Остекление балкона с крышей", "COMMERCIAL_SERVICE", "FIT"),
    "BALCONY_GLAZING_EXTENSION": ("Остекление балкона с выносом", "COMMERCIAL_SERVICE", "FIT"),
    "BALCONY_GLAZING_HOUSE_SERIES": ("Остекление балкона по серии дома", "COMMERCIAL_SERVICE", "FIT"),
    "VERANDA_GLAZING": ("Остекление веранды", "COMMERCIAL_SERVICE", "FIT"),
    "TERRACE_GLAZING": ("Остекление террасы", "COMMERCIAL_SERVICE", "FIT"),
    "GAZEBO_GLAZING": ("Остекление беседки", "COMMERCIAL_SERVICE", "FIT"),
    "FRAMELESS_GLAZING": ("Безрамное остекление", "COMMERCIAL_SERVICE", "FIT"),
    "WINDOW_INSTALLATION": ("Профессиональная установка/монтаж окон", "COMMERCIAL_SERVICE", "FIT"),
    "WINDOW_REPAIR": ("Ремонт и регулировка окон", "COMMERCIAL_SERVICE", "ADJACENT"),
    "WINDOWSILL_REPAIR": ("Ремонт подоконников", "COMMERCIAL_SERVICE", "ADJACENT"),
    "WINDOW_ACCESSORIES": ("Аксессуары для окон", "ECOMMERCE_ACCESSORY", "ADJACENT"),
    "WINDOW_HARDWARE": ("Оконная фурнитура и комплектующие", "ECOMMERCE_ACCESSORY", "ADJACENT"),
    "MOSQUITO_NETS": ("Москитные сетки и защита на окна", "ECOMMERCE_ACCESSORY", "ADJACENT"),
    "WINDOW_SELECTION_INFO": ("Как выбрать окна", "INFORMATIONAL", "ADJACENT"),
    "REHAU_SELECTION_INFO": ("Как выбрать профиль/систему Rehau", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_INSTALLATION_DIY": ("Самостоятельная/пошаговая установка окон", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_TECH_INFO": ("Устройство, конструкция и техническая информация об окнах", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_COMPARISON_INFO": ("Сравнение окон/профилей/систем", "INFORMATIONAL_COMPARISON", "ADJACENT"),
    "WINDOW_REVIEWS_INFO": ("Отзывы об окнах/фурнитуре", "INFORMATIONAL", "ADJACENT"),
    "DESIGN_INSPIRATION": ("Фото/идеи/дизайн окон и остекления", "INFORMATIONAL_INSPIRATION", "ADJACENT"),
    "REHAU_NAVIGATION": ("Навигационный поиск официального Rehau", "NAVIGATIONAL", "ADJACENT"),
    "WINDOW_SERVICE_NAVIGATION": ("Навигационный поиск оконной услуги/контактов", "NAVIGATIONAL", "ADJACENT"),
    "OUTSIDE_CURTAINS": ("Шторы/жалюзи как отдельный товар", "OUTSIDE_CORE", "OUTSIDE"),
    "OUTSIDE_REAL_ESTATE": ("Недвижимость/проекты домов с окнами", "OUTSIDE_CORE", "OUTSIDE"),
    "OUTSIDE_USED_MARKET": ("Б/у товар или вторичный рынок", "OUTSIDE_CORE", "OUTSIDE"),
    "OUTSIDE_INTERIOR_DOORS": ("Межкомнатные двери как отдельный товар", "OUTSIDE_CORE", "OUTSIDE"),
    "OPEN_BALCONY_FINISHING": ("Балкон без остекления / отделка открытого балкона", "MIXED_SERVICE_INFORMATION", "ADJACENT"),
}

INFO_MARKERS = (
    "как ", "как выбрать", "почему", "какой ", "какую ", "что такое", "инструкция",
    "своими руками", "пошаг", "видео", "конструкция", "устройство", "схема", "отзывы",
    "плюсы", "минусы", "разница", "сравн", "лучше", "фото",
)
NAV_MARKERS = ("официальный сайт", "официальный", "адрес", "телефон", "контакты")
GEO_MARKERS = ("москва", "митино", "одинцово", "одинцове", "район", "московск")


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def norm(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has_any(text: str, markers: tuple[str, ...] | list[str]) -> bool:
    return any(m in text for m in markers)


def classify_semantic(phrase: str) -> tuple[str | None, str, str]:
    """Return task_id, reason, confidence from explicit task semantics only.

    This is deliberately conservative. Unknown/materially ambiguous phrases remain unresolved.
    It does not use corrected_reason, source_id, provenance, frequency or lexical similarity
    to another phrase as cluster authority.
    """
    p = norm(phrase)
    info = has_any(p, INFO_MARKERS)
    nav = has_any(p, NAV_MARKERS)
    geo = has_any(p, GEO_MARKERS)

    # Strong outside-core meanings first.
    if any(x in p for x in ("штор", "жалюзи")):
        return "OUTSIDE_CURTAINS", "Explicit curtain/blind shopping or selection task", "HIGH"
    if any(x in p for x in ("авито", "б у", "б/у", "старый", "бу дверь", "бу окна")):
        return "OUTSIDE_USED_MARKET", "Explicit used/marketplace task", "HIGH"
    if "межкомнат" in p and "двер" in p:
        return "OUTSIDE_INTERIOR_DOORS", "Explicit interior-door product task", "HIGH"
    if ("панорам" in p and any(x in p for x in ("дом ", "дома", "барнхаус", "дача", "апартамент", "лес", "гостиная", "баня", "бассейн", "интерьер"))):
        return "OUTSIDE_REAL_ESTATE", "Panoramic-window wording is embedded in house/real-estate/inspiration task", "HIGH"

    # Explicit informational/navigation task overrides generic commercial subject.
    if nav and ("rehau" in p or "рехау" in p):
        return "REHAU_NAVIGATION", "Explicit official/entity navigation modifier", "HIGH"
    if nav and any(x in p for x in ("окн", "остеклен", "ремонт", "установ")):
        return "WINDOW_SERVICE_NAVIGATION", "Explicit address/phone/entity-navigation modifier", "MEDIUM"

    if info:
        if any(x in p for x in ("установ", "монтаж")) and any(x in p for x in ("своими руками", "пошаг", "видео", "инструкция", "как ")):
            return "WINDOW_INSTALLATION_DIY", "Explicit procedural/DIY installation intent", "HIGH"
        if ("rehau" in p or "рехау" in p) and any(x in p for x in ("выбрать", "какой", "сравн", "лучше")):
            if any(x in p for x in ("сравн", "лучше", "или ")):
                return "WINDOW_COMPARISON_INFO", "Explicit comparison task involving Rehau", "HIGH"
            return "REHAU_SELECTION_INFO", "Explicit Rehau selection question", "HIGH"
        if any(x in p for x in ("отзывы", "отзыв")):
            return "WINDOW_REVIEWS_INFO", "Explicit reviews task", "HIGH"
        if any(x in p for x in ("конструкция", "устройство", "схема", "инструкция", "режим")):
            return "WINDOW_TECH_INFO", "Explicit technical-information task", "HIGH"
        if any(x in p for x in ("сравн", "лучше", "или ", "почему")):
            return "WINDOW_COMPARISON_INFO", "Explicit comparison/explanation task", "HIGH"
        if "фото" in p:
            return "DESIGN_INSPIRATION", "Explicit photo/inspiration intent", "MEDIUM"
        if any(x in p for x in ("выбрать", "как ", "какой ", "какую ")) and "окн" in p:
            return "WINDOW_SELECTION_INFO", "Explicit window-selection question", "HIGH"
        # Informational marker exists but exact task family is not safe.
        return None, "Informational marker present but material task boundary remains ambiguous", "LOW"

    # Finance is a distinct user goal, not evidence of a separate URL.
    if any(x in p for x in ("рассроч", "кредит", "халва")) and ("окн" in p or "rehau" in p or "рехау" in p):
        return "WINDOW_FINANCE", "Explicit finance modifier on window purchase", "HIGH"

    # Repairs before generic product/installation.
    if any(x in p for x in ("ремонт", "провис", "регулир", "почин", "сломал", "замена уплот", "заменить уплот")) and "подокон" in p:
        return "WINDOWSILL_REPAIR", "Explicit windowsill repair task", "HIGH"
    if any(x in p for x in ("ремонт", "провис", "регулир", "почин", "сломал", "замена уплот", "заменить уплот")) and any(x in p for x in ("окн", "rehau", "рехау", "стеклопак")):
        return "WINDOW_REPAIR", "Explicit window repair/diagnostic task", "HIGH"

    # Accessories/components before generic product.
    if any(x in p for x in ("москит", "антикошка", "сетка на ок", "сетка для ок")):
        return "MOSQUITO_NETS", "Explicit mosquito/protection accessory task", "HIGH"
    if any(x in p for x in ("фурнитур", "ручк", "микролифт", "ограничител", "анкерн", "гребенк", "комплект для окна", "профиль для окна")):
        return "WINDOW_HARDWARE", "Explicit window hardware/component task", "HIGH"
    if any(x in p for x in ("аксессуар", "герметик для пластиковых окон", "блокиратор окон")):
        return "WINDOW_ACCESSORIES", "Explicit window accessory task", "HIGH"

    # Balcony/glazing service subdivisions.
    if "без остеклен" in p and "балкон" in p:
        return "OPEN_BALCONY_FINISHING", "Explicit no-glazing balcony task", "HIGH"
    if "остеклен" in p and any(x in p for x in ("балкон", "лоджи")):
        if "демонтаж" in p:
            return "WINDOW_REPAIR", "Explicit glazing-demolition adjacent service", "MEDIUM"
        if "тепл" in p:
            return "BALCONY_GLAZING_WARM", "Explicit warm-glazing subtype", "HIGH"
        if "холод" in p:
            return "BALCONY_GLAZING_COLD", "Explicit cold-glazing subtype", "HIGH"
        if "с крыш" in p or "крышей" in p:
            return "BALCONY_GLAZING_ROOF", "Explicit roof-glazing subtype", "HIGH"
        if "с вынос" in p or "вынос" in p:
            return "BALCONY_GLAZING_EXTENSION", "Explicit extension-glazing subtype", "HIGH"
        if re.search(r"\bп\s*[- ]?\d+", p):
            return "BALCONY_GLAZING_HOUSE_SERIES", "Explicit house-series glazing modifier", "HIGH"
        return "BALCONY_GLAZING", "Explicit balcony/loggia glazing service", "HIGH"

    if "остеклен" in p and "веранд" in p:
        if "безрам" in p or "бескаркас" in p:
            return "FRAMELESS_GLAZING", "Explicit frameless veranda glazing", "HIGH"
        return "VERANDA_GLAZING", "Explicit veranda glazing service", "HIGH"
    if "остеклен" in p and "террас" in p:
        if "безрам" in p or "бескаркас" in p:
            return "FRAMELESS_GLAZING", "Explicit frameless terrace glazing", "HIGH"
        return "TERRACE_GLAZING", "Explicit terrace glazing service", "HIGH"
    if "остеклен" in p and ("бесед" in p or "крыльц" in p):
        return "GAZEBO_GLAZING", "Explicit gazebo/porch glazing service", "HIGH"
    if "безрам" in p and "остеклен" in p:
        return "FRAMELESS_GLAZING", "Explicit frameless glazing service", "HIGH"

    # Professional installation.
    if any(x in p for x in ("установка", "монтаж", "установить")) and "окн" in p:
        return "WINDOW_INSTALLATION", "Explicit professional window installation task", "HIGH"

    # Doors.
    if "двер" in p and any(x in p for x in ("пластик", "пвх")):
        return "PVC_DOORS_COMMERCIAL", "Explicit PVC/plastic door product task", "HIGH"

    # Material/product families.
    if "provedal" in p or "проведал" in p:
        if "остеклен" in p:
            # Object-specific service already handled above when explicit; keep remaining Provedal glazing together provisionally.
            return "PROVEDAL_WINDOWS_COMMERCIAL", "Explicit Provedal system/product intent", "MEDIUM"
        return "PROVEDAL_WINDOWS_COMMERCIAL", "Explicit Provedal product/system intent", "HIGH"
    if "алюмини" in p and "окн" in p:
        return "ALUMINIUM_WINDOWS_COMMERCIAL", "Explicit aluminium-window product task", "HIGH"
    if ("деревян" in p or "дерево алюмини" in p) and "окн" in p:
        return "WOOD_WINDOWS_COMMERCIAL", "Explicit wood/timber-aluminium window product task", "HIGH"
    if "панорам" in p and "окн" in p:
        return "PANORAMIC_WINDOWS_COMMERCIAL", "Explicit panoramic-window product task without outside-core house context", "MEDIUM"

    # Brand before generic PVC.
    if "rehau" in p or "рехау" in p:
        if re.search(r"\b(thermo|grazio|sib|intelio|delight|brillant|geneo|70|80|60)\b", p):
            return "REHAU_PRODUCT_SUBTYPE", "Explicit Rehau product/system subtype", "HIGH"
        if "от производител" in p:
            return "REHAU_WINDOWS_COMMERCIAL", "Rehau product with manufacturer modifier", "HIGH"
        if "окн" in p or "стеклопак" in p:
            return "REHAU_WINDOWS_COMMERCIAL", "Explicit Rehau window product task", "HIGH"

    if "от производител" in p and "окн" in p:
        return "PVC_WINDOWS_MANUFACTURER", "Explicit manufacturer modifier on window purchase", "HIGH"
    if "пластиков" in p and "окн" in p:
        if geo:
            return "PVC_WINDOWS_GEO", "Explicit PVC-window purchase with geographic modifier", "HIGH"
        return "PVC_WINDOWS_COMMERCIAL", "Explicit PVC-window product task", "HIGH"

    # Generic 'окна' without enough material/action context is not safe to force.
    return None, "No sufficiently explicit user-task decomposition under conservative Step-10 rules", "LOW"


def task_fields(task_id: str | None) -> tuple[str, str, str]:
    if not task_id:
        return "", "UNKNOWN_OR_MIXED", "UNKNOWN_PUBLIC_FIT"
    label, intent, fit = TASKS[task_id]
    return label, intent, fit


def material_modifiers(phrase: str) -> str:
    p = norm(phrase)
    mods = []
    for key, markers in [
        ("GEO", GEO_MARKERS),
        ("FINANCE", ("рассроч", "кредит", "халва")),
        ("PRICE", ("цена", "цены", "стоимость")),
        ("DIY", ("своими руками", "пошаг", "инструкция", "видео")),
        ("PHOTO", ("фото",)),
        ("REVIEW", ("отзывы", "отзыв")),
        ("OFFICIAL", ("официаль",)),
        ("WARM", ("тепл",)),
        ("COLD", ("холод",)),
        ("ROOF", ("крышей", "с крыш")),
        ("EXTENSION", ("вынос",)),
        ("REHAU", ("rehau", "рехау")),
        ("PROVEDAL", ("provedal", "проведал")),
    ]:
        if has_any(p, markers):
            mods.append(key)
    return "|".join(mods)


def main() -> None:
    rows = read_tsv(INPUT)
    decisions = read_tsv(DECISIONS)
    comparisons = read_tsv(COMPARISONS)

    assert len(rows) == EXPECTED["total"], len(rows)
    assert len({r["phrase"].casefold() for r in rows}) == EXPECTED["total"]
    disposition_counts = Counter(r["search_stage_disposition"] for r in rows)
    for key in ("CORE_CANDIDATE", "REVIEW_SEARCH", "REVIEW_DEFERRED", "EXCLUDED_PRESERVED"):
        assert disposition_counts[key] == EXPECTED[key], (key, disposition_counts[key])
    assert disposition_counts["CORE_CANDIDATE"] + disposition_counts["REVIEW_SEARCH"] == EXPECTED["active"]

    assert len(decisions) == EXPECTED["direct_probes"], len(decisions)
    direct_by_phrase = {norm(r["query"]): r for r in decisions}
    assert len(direct_by_phrase) == EXPECTED["direct_probes"]
    assert len(comparisons) == EXPECTED["duplicate_comparisons"]

    # Every Step-09 direct query must correspond to one Step-08 phrase key.
    input_by_phrase = {norm(r["phrase"]): r for r in rows}
    missing_direct = sorted(q for q in direct_by_phrase if q not in input_by_phrase)
    assert not missing_direct, missing_direct

    # DUP-0004 exact strings receive a mandatory boundary override.
    dup4_phrases = {
        norm("пластиковые окна от производителя rehau"),
        norm("пластиковые окна рехау от производителя"),
    }

    out_rows = []
    boundary_rows = []
    cluster_members: dict[str, list[dict[str, str]]] = defaultdict(list)
    direct_consumed = 0
    review_unprobed_with_direct_claim = 0

    for src in rows:
        phrase = src["phrase"]
        pnorm = norm(phrase)
        disposition = src["search_stage_disposition"]
        direct = direct_by_phrase.get(pnorm)
        if direct:
            direct_consumed += 1

        base = {
            "phrase": phrase,
            "input_disposition": disposition,
            "corrected_status": src["corrected_status"],
            "corrected_reason": src["corrected_reason"],
            "user_task": "",
            "intent_orientation": "",
            "material_modifiers": material_modifiers(phrase),
            "public_business_fit": "",
            "step09_probe_id": direct["probe_id"] if direct else "",
            "step09_evidence_scope": direct["evidence_scope"] if direct else "NO_DIRECT_STEP09_SERP",
            "observed_serp_job": direct["observed_serp_job"] if direct else "",
            "dominant_result_type": direct["dominant_result_type"] if direct else "",
            "step09_handoff": direct["step10_handoff"] if direct else "",
            "cluster_id": "",
            "cluster_role": "",
            "cluster_evidence_state": "",
            "assignment_reason": "",
            "confidence": "",
            "additional_search_required": "false",
        }

        if disposition == "REVIEW_DEFERRED":
            base.update({
                "user_task": "Deferred upstream evidence state",
                "intent_orientation": "DEFERRED",
                "public_business_fit": "UNKNOWN_PUBLIC_FIT",
                "cluster_role": "DEFERRED_PRESERVED",
                "cluster_evidence_state": "DEFERRED_PRESERVED",
                "assignment_reason": "Step-08 REVIEW_DEFERRED preserved; Step 10 not authorized to force-cluster it",
                "confidence": "N/A",
            })
            out_rows.append(base)
            continue
        if disposition == "EXCLUDED_PRESERVED":
            base.update({
                "user_task": "Excluded upstream state preserved",
                "intent_orientation": "EXCLUDED",
                "public_business_fit": "OUTSIDE_OR_EXCLUDED_UPSTREAM",
                "cluster_role": "EXCLUDED_PRESERVED",
                "cluster_evidence_state": "EXCLUDED_PRESERVED",
                "assignment_reason": "Accepted Step-07/08 exclusion preserved; not reintroduced by clustering",
                "confidence": "N/A",
            })
            out_rows.append(base)
            continue

        # Active rows only below.
        task_id, semantic_reason, semantic_conf = classify_semantic(phrase)

        # Direct evidence can contradict an otherwise plausible semantic grouping.
        direct_outside = bool(direct and (
            direct["step10_handoff"].startswith("OUTSIDE_")
            or direct["dominant_result_type"] in {"REAL_ESTATE_PROJECT_CATALOG", "REAL_ESTATE_TRAVEL_INSPIRATION", "SECOND_HAND_MARKETPLACE"}
        ))
        direct_info = bool(direct and any(x in direct["dominant_result_type"] for x in ("INFORMATION", "REVIEWS", "VIDEO", "NAVIGATIONAL")))
        semantic_commercial = bool(task_id and TASKS[task_id][1].startswith("COMMERCIAL"))
        direct_contradiction = direct_outside and task_id and TASKS[task_id][2] != "OUTSIDE"
        if direct_info and semantic_commercial and direct and direct["step10_handoff"].startswith("INFORMATIONAL_"):
            direct_contradiction = True

        if pnorm in dup4_phrases:
            label, intent, fit = task_fields(task_id)
            base.update({
                "user_task": label or "Rehau manufacturer-query boundary",
                "intent_orientation": intent,
                "public_business_fit": fit,
                "cluster_id": "",
                "cluster_role": "BOUNDARY_REVIEW",
                "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW",
                "assignment_reason": "Mandatory DUP-0004 override: Step-09 exact URL overlap 1/10; no auto-merge",
                "confidence": "HIGH",
                "additional_search_required": "true",
            })
            boundary_rows.append({
                "record_type": "PHRASE_BOUNDARY",
                "phrase": phrase,
                "related_id": "DUP-0004",
                "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW",
                "reason": base["assignment_reason"],
                "direct_evidence": f"probe={base['step09_probe_id']}|serp_job={base['observed_serp_job']}",
            })
            out_rows.append(base)
            continue

        if direct_contradiction:
            label, intent, fit = task_fields(task_id)
            base.update({
                "user_task": label or direct["observed_serp_job"],
                "intent_orientation": intent,
                "public_business_fit": fit,
                "cluster_role": "BOUNDARY_REVIEW",
                "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW",
                "assignment_reason": f"Direct Step-09 SERP contradicts semantic grouping hypothesis: {direct['step10_handoff']}",
                "confidence": "MEDIUM",
                "additional_search_required": "true",
            })
            boundary_rows.append({
                "record_type": "PHRASE_BOUNDARY",
                "phrase": phrase,
                "related_id": direct["probe_id"],
                "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW",
                "reason": base["assignment_reason"],
                "direct_evidence": f"serp_job={direct['observed_serp_job']}|result_type={direct['dominant_result_type']}",
            })
            out_rows.append(base)
            continue

        if not task_id:
            base.update({
                "user_task": "Unresolved material user task",
                "intent_orientation": "UNKNOWN_OR_MIXED",
                "public_business_fit": "UNKNOWN_PUBLIC_FIT",
                "cluster_role": "UNRESOLVED",
                "cluster_evidence_state": "SEARCH_REQUIRED",
                "assignment_reason": semantic_reason,
                "confidence": "LOW",
                "additional_search_required": "true",
            })
            boundary_rows.append({
                "record_type": "SEARCH_REQUIRED",
                "phrase": phrase,
                "related_id": direct["probe_id"] if direct else "",
                "cluster_evidence_state": "SEARCH_REQUIRED",
                "reason": semantic_reason,
                "direct_evidence": f"serp_job={direct['observed_serp_job']}" if direct else "NO_DIRECT_STEP09_SERP",
            })
            out_rows.append(base)
            continue

        label, intent, fit = task_fields(task_id)
        evidence_state = "SERP_SUPPORTED" if direct else "SEMANTIC_SUPPORTED_NO_DIRECT_SERP"
        role = "DIRECT_SERP_MEMBER" if direct else "SEMANTIC_MEMBER_NO_DIRECT_SERP"
        reason = semantic_reason
        if direct:
            reason += f"; direct Step-09 evidence: {direct['observed_serp_job']} / {direct['dominant_result_type']}"
        base.update({
            "user_task": label,
            "intent_orientation": intent,
            "public_business_fit": fit,
            "cluster_id": task_id,
            "cluster_role": role,
            "cluster_evidence_state": evidence_state,
            "assignment_reason": reason,
            "confidence": direct["confidence"] if direct else semantic_conf,
            "additional_search_required": "false",
        })
        cluster_members[task_id].append(base)
        out_rows.append(base)

    assert len(out_rows) == EXPECTED["total"]
    assert direct_consumed == EXPECTED["direct_probes"], direct_consumed

    # Explicitly consume all eight duplicate comparisons as evidence records.
    dup4_seen = False
    for comp in comparisons:
        cid = comp["comparison_id"]
        gid = comp["group_id"]
        if gid == "DUP-0004":
            dup4_seen = True
            assert comp["exact_url_overlap"] == "1", comp
            assert "DO_NOT_AUTO_MERGE" in comp["step10_handoff"], comp
        boundary_rows.append({
            "record_type": "DUPLICATE_COMPARISON_AUDIT",
            "phrase": f"{comp['query_a']} <> {comp['query_b']}",
            "related_id": f"{cid}|{gid}",
            "cluster_evidence_state": "MIXED_OR_BOUNDARY_REVIEW" if gid == "DUP-0004" else "SERP_SUPPORTED_CANDIDATE_PAIR",
            "reason": comp["step09_conclusion"] + " / " + comp["step10_handoff"],
            "direct_evidence": f"exact_url_overlap={comp['exact_url_overlap']}/{comp['top_n_a']}",
        })
    assert dup4_seen

    fields = [
        "phrase", "input_disposition", "corrected_status", "corrected_reason", "user_task",
        "intent_orientation", "material_modifiers", "public_business_fit", "step09_probe_id",
        "step09_evidence_scope", "observed_serp_job", "dominant_result_type", "step09_handoff",
        "cluster_id", "cluster_role", "cluster_evidence_state", "assignment_reason", "confidence",
        "additional_search_required",
    ]
    with OUT_ASSIGN.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(out_rows)

    # Cluster summary. Primary query uses accepted Wordstat max_result_count only to choose an anchor
    # *inside* an already assigned cluster; it never creates the cluster.
    src_by_phrase = {r["phrase"]: r for r in rows}
    summary_rows = []
    for task_id in sorted(cluster_members):
        members = cluster_members[task_id]
        label, intent, fit = TASKS[task_id]
        primary = max(
            members,
            key=lambda r: (int(src_by_phrase[r["phrase"]].get("max_result_count") or 0), -len(r["phrase"]), r["phrase"]),
        )["phrase"]
        direct_count = sum(bool(r["step09_probe_id"]) for r in members)
        semantic_count = len(members) - direct_count
        state = "SERP_SUPPORTED" if direct_count else "SEMANTIC_SUPPORTED_NO_DIRECT_SERP"
        summary_rows.append({
            "cluster_id": task_id,
            "cluster_label": label,
            "user_task": label,
            "intent_orientation": intent,
            "public_business_fit": fit,
            "primary_query": primary,
            "member_count": str(len(members)),
            "direct_serp_member_count": str(direct_count),
            "semantic_only_member_count": str(semantic_count),
            "cluster_evidence_state": state,
            "boundary_notes": "Working Step-10 task cluster only; no URL ownership or structural action",
        })
    summary_fields = list(summary_rows[0].keys()) if summary_rows else []
    with OUT_SUMMARY.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=summary_fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(summary_rows)

    boundary_fields = ["record_type", "phrase", "related_id", "cluster_evidence_state", "reason", "direct_evidence"]
    with OUT_BOUNDARY.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=boundary_fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(boundary_rows)

    # Deterministic QA sample: first 3 + last 2 alphabetically per cluster, plus every direct member and every boundary.
    sample_rows = []
    for task_id in sorted(cluster_members):
        members = sorted(cluster_members[task_id], key=lambda r: norm(r["phrase"]))
        chosen = []
        for r in members[:3] + members[-2:] + [x for x in members if x["step09_probe_id"]]:
            if r["phrase"] not in {x["phrase"] for x in chosen}:
                chosen.append(r)
        for r in chosen:
            sample_rows.append({
                "sample_type": "CLUSTER_MEMBER",
                "cluster_id": task_id,
                "phrase": r["phrase"],
                "user_task": r["user_task"],
                "intent_orientation": r["intent_orientation"],
                "evidence_state": r["cluster_evidence_state"],
                "step09_probe_id": r["step09_probe_id"],
                "reason": r["assignment_reason"],
            })
    # Add all mixed/direct boundary rows and a bounded deterministic sample of unresolved rows.
    unresolved = [r for r in out_rows if r["cluster_evidence_state"] == "SEARCH_REQUIRED"]
    for r in sorted(unresolved, key=lambda x: norm(x["phrase"]))[:100]:
        sample_rows.append({
            "sample_type": "SEARCH_REQUIRED_SAMPLE",
            "cluster_id": "",
            "phrase": r["phrase"],
            "user_task": r["user_task"],
            "intent_orientation": r["intent_orientation"],
            "evidence_state": r["cluster_evidence_state"],
            "step09_probe_id": r["step09_probe_id"],
            "reason": r["assignment_reason"],
        })
    sample_fields = ["sample_type", "cluster_id", "phrase", "user_task", "intent_orientation", "evidence_state", "step09_probe_id", "reason"]
    with OUT_SAMPLE.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=sample_fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(sample_rows)

    states = Counter(r["cluster_evidence_state"] for r in out_rows)
    active_rows = [r for r in out_rows if r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"}]
    assert len(active_rows) == EXPECTED["active"]
    assert all(r["cluster_evidence_state"] in {"SERP_SUPPORTED", "SEMANTIC_SUPPORTED_NO_DIRECT_SERP", "MIXED_OR_BOUNDARY_REVIEW", "SEARCH_REQUIRED"} for r in active_rows)
    assert states["DEFERRED_PRESERVED"] == EXPECTED["REVIEW_DEFERRED"]
    assert states["EXCLUDED_PRESERVED"] == EXPECTED["EXCLUDED_PRESERVED"]
    assert sum(states.values()) == EXPECTED["total"]

    # No unprobed phrase may claim direct Step-09 evidence.
    for r in out_rows:
        if not r["step09_probe_id"]:
            if r["step09_evidence_scope"] != "NO_DIRECT_STEP09_SERP" and r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
                review_unprobed_with_direct_claim += 1
    assert review_unprobed_with_direct_claim == 0

    # DUP-0004 must remain unclustered/boundary review for both members.
    dup4_assign = [r for r in out_rows if norm(r["phrase"]) in dup4_phrases]
    assert len(dup4_assign) == 2
    assert all(r["cluster_id"] == "" and r["cluster_evidence_state"] == "MIXED_OR_BOUNDARY_REVIEW" for r in dup4_assign)

    # Step 10 may not assign downstream fields at all.
    forbidden_fields = {"target_url", "page_ownership", "structural_action", "cannibalization", "merge_action", "new_page"}
    assert not (forbidden_fields & set(fields))

    qa = {
        "status": "MACHINE_QA_PASS__MANUAL_SEMANTIC_QA_REQUIRED",
        "total_phrase_keys": len(out_rows),
        "active_search_stage_rows": len(active_rows),
        "input_disposition_counts": dict(sorted(disposition_counts.items())),
        "cluster_count": len(summary_rows),
        "cluster_evidence_state_counts": dict(sorted(states.items())),
        "direct_step09_probes_expected": EXPECTED["direct_probes"],
        "direct_step09_probes_consumed": direct_consumed,
        "duplicate_comparisons_expected": EXPECTED["duplicate_comparisons"],
        "duplicate_comparisons_consumed": len(comparisons),
        "dup0004_auto_merged": False,
        "unprobed_rows_claiming_direct_serp": review_unprobed_with_direct_claim,
        "silent_drops": EXPECTED["total"] - len(out_rows),
        "review_deferred_preserved": states["DEFERRED_PRESERVED"],
        "excluded_preserved": states["EXCLUDED_PRESERVED"],
        "search_required_rows": states["SEARCH_REQUIRED"],
        "mixed_boundary_rows": states["MIXED_OR_BOUNDARY_REVIEW"],
        "semantic_supported_no_direct_serp_rows": states["SEMANTIC_SUPPORTED_NO_DIRECT_SERP"],
        "serp_supported_rows": states["SERP_SUPPORTED"],
        "manual_semantic_qa_required": True,
        "manual_semantic_qa_pass": False,
        "page_ownership_decisions": 0,
        "structural_action_decisions": 0,
        "cannibalization_decisions": 0,
        "provider_requests": 0,
        "provider_cost_rub": 0,
    }
    OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
