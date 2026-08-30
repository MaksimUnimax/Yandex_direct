#!/usr/bin/env python3
from __future__ import annotations

"""Frozen full-manual-discovery specification for the V37 Step-10 candidate.

This file is intentionally data-first. It records the complete discovery pass before
any V38 correction is applied. Validation must use the whole set; fail-fast CI is not
an error-discovery method.
"""

ROOT_RATIONALE = {
    "SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST": "A specific head object/action was swallowed by a broader product/service family.",
    "SEMANTICALLY_DETERMINATE_LEFT_UNRESOLVED": "The phrase has a determinate user task from its own semantics but V37 left it SEARCH_REQUIRED.",
    "DIY_SERVICE_INFO_INFERRED_WITHOUT_ENOUGH_EVIDENCE": "V37 inferred a DIY/service/info sub-mode that the phrase itself does not safely prove.",
    "PHOTO_DESIGN_MODIFIER_OUTRANKED_HEAD_OBJECT": "Photo/design wording outranked the actual dwelling/room/architecture head object.",
    "PRIVATE_HOUSE_MODIFIER_SPLIT_EQUIVALENT_SELECTION": "Equivalent private-house selection queries were split by modifier precedence.",
    "DEFINITION_MISROUTED_AS_SELECTION": "A definition/naming query was routed to selection/types information.",
    "COMMERCIAL_GEO_REPAIR_OVERRIDDEN_BY_SYMPTOM_RULE": "Explicit commercial geo repair intent was demoted by a symptom/diagnostic rule.",
}

ROWS: list[dict[str, str]] = []


def add_many(phrases, *, v37_cluster: str, v37_state: str, root: str, target: str) -> None:
    for phrase in phrases:
        ROWS.append({
            "phrase": phrase,
            "v37_cluster_id": v37_cluster,
            "v37_evidence_state": v37_state,
            "root_cause": root,
            "proposed_cluster_id": target,
            "proposed_evidence_state": "SEARCH_REQUIRED" if target == "SEARCH_REQUIRED" else "SEMANTIC_SUPPORTED_NO_DIRECT_SERP",
            "manual_qa_rationale": ROOT_RATIONALE[root],
        })


# Root cause 1: specific head object/action lost — 36 rows.
add_many([
    "остекление и отделка балконов",
    "остекление и отделка балконов в москве",
    "остекление и отделка балконов под ключ",
    "остекление обшивка балконов",
    "остекление отделка балконов цены",
    "отделка балкона под ключ москва с остеклением",
], v37_cluster="BALCONY_GLAZING", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="BALCONY_RENOVATION_WITH_GLAZING_SERVICE")

add_many([
    "масло для оконной фурнитуры",
    "масло для смазки оконной фурнитуры",
    "силиконовая смазка для оконной фурнитуры",
    "смазка для оконной фурнитуры",
    "смазка для оконной фурнитуры на пластиковых",
    "смазка для оконной фурнитуры на пластиковых окнах",
], v37_cluster="WINDOW_HARDWARE", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_ACCESSORIES")

add_many([
    "чем смазать оконную фурнитуру",
    "чем смазать оконную фурнитуру для пластиковых окон",
], v37_cluster="WINDOW_HARDWARE", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_CARE_INFO")

add_many([
    "оконная фурнитура гост",
    "оконная фурнитура сертификат",
], v37_cluster="WINDOW_HARDWARE", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_TECH_INFO")

add_many([
    "производители оконной фурнитуры",
    "производство оконной фурнитуры",
], v37_cluster="WINDOW_HARDWARE", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="SEARCH_REQUIRED")

add_many([
    "балконное окно с дверью пластиковое цена установкой",
    "балконный блок пластиковые окна установкой",
    "балконный блок пластиковые окна цена с установкой",
], v37_cluster="WINDOW_INSTALLATION", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_DOOR_INSTALLATION_SERVICE")
add_many([
    "установка пластикового окна с балконной дверью",
    "установка пластиковых окон и дверей",
], v37_cluster="PVC_DOOR_INSTALLATION_SERVICE", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_DOOR_INSTALLATION_SERVICE")

add_many([
    "ремонт пластиковых окон и дверей",
    "ремонт регулировка пластиковых окон и дверей",
    "ремонт штульповых пластиковых окон дверей",
], v37_cluster="WINDOW_REPAIR", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_DOOR_REPAIR_SERVICE")

add_many(["алюминиевые окна и двери"], v37_cluster="ALUMINIUM_WINDOWS_COMMERCIAL", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_DOOR_COMMERCIAL")
add_many(["окна двери rehau"], v37_cluster="REHAU_WINDOWS_COMMERCIAL", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_DOOR_COMMERCIAL")
add_many(["окна двери для частного дома"], v37_cluster="PRIVATE_HOUSE_WINDOWS_COMMERCIAL", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_DOOR_COMMERCIAL")

add_many([
    "отделка пластиковых окон",
    "цена на отделку пластиковых окон",
], v37_cluster="PVC_WINDOWS_COMMERCIAL", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_FINISHING_SERVICE")
add_many(["остекление веранды в рассрочку"], v37_cluster="VERANDA_GLAZING", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_FINANCE")
add_many(["стекло остекления балкона"], v37_cluster="BALCONY_GLAZING", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_HARDWARE")
add_many(["верандные рамы для веранды остекление одинарное цена"], v37_cluster="VERANDA_GLAZING", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_HARDWARE")
add_many(["жидкое стекло остекление веранды"], v37_cluster="VERANDA_GLAZING", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="WINDOW_ACCESSORIES")
add_many(["система остекления веранды"], v37_cluster="VERANDA_GLAZING", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="SPECIFIC_HEAD_OBJECT_OR_ACTION_LOST", target="GLAZING_SELECTION_INFO")

# Root cause 2: semantically determinate rows left unresolved — 25 rows.
TARGETS_FALSE_UNRESOLVED = {
    "ral алюминиевых окон": "WINDOW_SELECTION_INFO",
    "камин панорамные окна": "OUTSIDE_HEATING",
    "окно панорамный блок": "PANORAMIC_WINDOWS_COMMERCIAL",
    "окно французской гостиной": "OUTSIDE_REAL_ESTATE",
    "отделка панорамных окон": "WINDOW_FINISHING_SERVICE",
    "отделка французского окна": "WINDOW_FINISHING_SERVICE",
    "панорамное окно на кухне": "OUTSIDE_REAL_ESTATE",
    "панорамные окна в здании": "OUTSIDE_REAL_ESTATE",
    "панорамные окна в каркасном": "OUTSIDE_REAL_ESTATE",
    "панорамные окна в частном": "PANORAMIC_WINDOWS_COMMERCIAL",
    "панорамные окна для загородного": "PANORAMIC_WINDOWS_COMMERCIAL",
    "панорамные окна и потолок": "OUTSIDE_REAL_ESTATE",
    "панорамные окна на море": "OUTSIDE_REAL_ESTATE",
    "перегородка французское окно": "OUTSIDE_REAL_ESTATE",
    "перепланировка французское окно": "OUTSIDE_REAL_ESTATE",
    "покраска алюминиевых окон": "WINDOW_FINISHING_SERVICE",
    "современные панорамные окна": "PANORAMIC_WINDOWS_INFO",
    "спальня французское окно": "OUTSIDE_REAL_ESTATE",
    "студия с панорамными окнами": "OUTSIDE_REAL_ESTATE",
    "утепление панорамных окон": "WINDOW_REPAIR",
    "французские балконные окна": "FRENCH_WINDOWS_COMMERCIAL",
    "французские окна в хрущевке": "FRENCH_WINDOWS_COMMERCIAL",
    "французские окна на даче": "FRENCH_WINDOWS_COMMERCIAL",
    "французские окна на кухню": "FRENCH_WINDOWS_COMMERCIAL",
    "французские окна современные": "PANORAMIC_WINDOWS_INFO",
}
for phrase, target in TARGETS_FALSE_UNRESOLVED.items():
    add_many([phrase], v37_cluster="", v37_state="SEARCH_REQUIRED", root="SEMANTICALLY_DETERMINATE_LEFT_UNRESOLVED", target=target)

# Root cause 3: unsupported DIY/service/info sub-mode inference — 14 rows.
add_many([
    "не закрывается окно rehau",
    "не закрывается пластиковое окно",
    "не открывается пластиковое окно",
    "окно rehau не открывается на проветривание",
    "пластиковое окно не закрывается ремонт",
], v37_cluster="WINDOW_REPAIR_DIY", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="DIY_SERVICE_INFO_INFERRED_WITHOUT_ENOUGH_EVIDENCE", target="SEARCH_REQUIRED")
add_many([
    "плохо закрывается пластиковая дверь",
    "провис пластиковой двери",
    "провисла пластиковая дверь",
    "просела пластиковая дверь",
], v37_cluster="PVC_DOOR_REPAIR_SERVICE", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="DIY_SERVICE_INFO_INFERRED_WITHOUT_ENOUGH_EVIDENCE", target="SEARCH_REQUIRED")
add_many(["не закрывается пластиковая дверь"], v37_cluster="PVC_DOOR_REPAIR_DIY", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="DIY_SERVICE_INFO_INFERRED_WITHOUT_ENOUGH_EVIDENCE", target="SEARCH_REQUIRED")
add_many(["пластиковая дверь своими руками"], v37_cluster="PVC_DOOR_INSTALLATION_DIY", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="DIY_SERVICE_INFO_INFERRED_WITHOUT_ENOUGH_EVIDENCE", target="SEARCH_REQUIRED")
add_many([
    "остекление балкона видео",
    "остекление веранды видео",
], v37_cluster="GLAZING_DIY_INFO", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="DIY_SERVICE_INFO_INFERRED_WITHOUT_ENOUGH_EVIDENCE", target="SEARCH_REQUIRED")
add_many(["ремонт пластиковых окон видео"], v37_cluster="WINDOW_REPAIR_DIY", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="DIY_SERVICE_INFO_INFERRED_WITHOUT_ENOUGH_EVIDENCE", target="SEARCH_REQUIRED")

# Root cause 4: architecture head object lost to photo/design — 5 rows.
add_many([
    "дизайн кухни с панорамными окнами",
    "дома с панорамными окнами фото",
    "интерьер с панорамными окнами",
    "стиль дома с панорамными окнами",
    "терраса с панорамными окнами фото",
], v37_cluster="DESIGN_INSPIRATION", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="PHOTO_DESIGN_MODIFIER_OUTRANKED_HEAD_OBJECT", target="OUTSIDE_REAL_ESTATE")

# Root cause 5: equivalent private-house selection split by modifier precedence — 3 rows.
add_many([
    "виды пластиковых окон для частного дома",
    "виды пластиковых окон для частного дома фото",
    "как выбрать пластиковые окна для частного",
], v37_cluster="WINDOW_SELECTION_INFO", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="PRIVATE_HOUSE_MODIFIER_SPLIT_EQUIVALENT_SELECTION", target="PRIVATE_HOUSE_WINDOWS_SELECTION_INFO")

# Root cause 6: definition misrouted to selection — 1 row.
add_many(["французские окна это какие"], v37_cluster="PANORAMIC_WINDOWS_INFO", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="DEFINITION_MISROUTED_AS_SELECTION", target="WINDOW_DEFINITION_INFO")

# Root cause 7: commercial geo repair overridden by symptom rule — 1 row.
add_many(["ремонт окна пластикового в москве не закрывается"], v37_cluster="WINDOW_REPAIR_DIY", v37_state="SEMANTIC_SUPPORTED_NO_DIRECT_SERP", root="COMMERCIAL_GEO_REPAIR_OVERRIDDEN_BY_SYMPTOM_RULE", target="WINDOW_REPAIR")

assert len(ROWS) == 85, len(ROWS)
assert len({r["phrase"] for r in ROWS}) == 85

EXPECTED_BY_PHRASE = {r["phrase"]: r for r in ROWS}
SUPERSEDED_PHRASES = set(EXPECTED_BY_PHRASE)
