#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner

# Additional job-specific task states discovered by independent semantic QA.
# They remain Step-10 user-task labels only: no URL ownership or structural action.
b.TASKS.update({
    "WINDOW_DEMOLITION": ("Демонтаж окон/остекления", "COMMERCIAL_SERVICE", "ADJACENT"),
    "WINDOW_MEASUREMENT_INFO": ("Замер и размеры перед установкой окон", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_OPERATION_DIY": ("Как снять/вставить/открыть/эксплуатировать окно", "INFORMATIONAL", "ADJACENT"),
    "PVC_DOOR_REPAIR_DIY": ("Регулировка/ремонт пластиковой двери", "INFORMATIONAL_SERVICE", "ADJACENT"),
    "WINDOW_DEFINITION_INFO": ("Что это / как называется оконная конструкция", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_ACCESSORY_SELECTION_INFO": ("Как выбрать оконный аксессуар/комплектующее", "INFORMATIONAL", "ADJACENT"),
    "OUTSIDE_HEATING": ("Отопление/радиаторы/конвекторы рядом с окнами", "OUTSIDE_CORE", "OUTSIDE"),
})

_base_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(text: str, *parts: str) -> bool:
    return any(x in text for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def classify_v3(phrase: str):
    p = n(phrase)

    # --- Strong outside-core task classes first. ---
    # Heating is not a window-purchase task even when the phrase contains
    # panoramic/French-window wording.
    if has(p, "радиатор", "батаре", "конвектор", "отоплен") and windowish(p):
        return "OUTSIDE_HEATING", "Explicit heating/radiator/convector task around windows", "HIGH"

    # Curtains/blinds include common 'day-night' phrasing that the previous
    # classifier mistook for window installation because of the word установка.
    if has(p, "штор", "жалюзи", "рулонн", "день ночь"):
        return "OUTSIDE_CURTAINS", "Explicit curtain/blind task, not window installation", "HIGH"

    # Used/marketplace remains a strong outside-core signal.
    if has(p, "авито", "б/у", " б у", "бу дверь", "бу окна"):
        return "OUTSIDE_USED_MARKET", "Explicit marketplace/used-product task", "HIGH"

    # --- Components/hardware before material/product windows. ---
    # FAPIM is directly observed in Step 09 as hardware-brand shopping.
    if "fapim" in p:
        return "WINDOW_HARDWARE", "FAPIM query is hardware/component intent; direct Step-09 evidence confirms hardware-brand shopping", "HIGH"
    if has(
        p,
        "фурнитур", "штапик", "ручк", "микролифт", "ограничител", "анкерн",
        "гребенк", "уплотнител", "петл", "доводчик", "замок для ок", "комплект для окна",
        "комплектующие для ок", "детали для ок", "механизм ок",
    ):
        # Reviews/comparison around hardware remain informational rather than shopping.
        if has(p, "отзыв"):
            return "WINDOW_REVIEWS_INFO", "Explicit reviews task for window hardware/component", "HIGH"
        if has(p, "лучше", "сравн", " или ", "отлич"):
            return "WINDOW_COMPARISON_INFO", "Explicit comparison task for window hardware/component", "HIGH"
        if has(p, "как выбрать", "выбрать"):
            return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit selection task for window hardware/component", "HIGH"
        return "WINDOW_HARDWARE", "Explicit window hardware/component task", "HIGH"

    # Mosquito/protection accessory selection must not become generic window selection.
    if has(p, "москит", "антикошка", "сетка на ок", "сетка для ок"):
        if has(p, "как выбрать", "выбрать"):
            return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit selection task for mosquito/protection accessory", "HIGH"
        return "MOSQUITO_NETS", "Explicit mosquito/protection accessory task", "HIGH"

    # --- Explicit comparison / definition / operation / measurement information. ---
    # Comparison has priority over product-family tokens such as Rehau model names.
    if has(p, "чем отличается", "чем отлич", "отличие", "разница", "сравн", "что лучше", "какой лучше", "какая лучше", " или "):
        if windowish(p) or has(p, "rehau", "рехау", "профил"):
            return "WINDOW_COMPARISON_INFO", "Explicit comparison/difference user task", "HIGH"

    if has(p, "как называется", "что такое", "как зовется", "как называется") and windowish(p):
        return "WINDOW_DEFINITION_INFO", "Explicit definition/naming user task", "HIGH"

    if has(p, "как отрегулировать", "как регулировать", "регулировка") and "двер" in p and has(p, "пластик", "пвх"):
        return "PVC_DOOR_REPAIR_DIY", "Explicit plastic-door adjustment/repair task", "HIGH"

    if has(p, "как снять", "как вставить", "как открыть", "как закрыть", "как разобрать", "как заменить", "как поменять") and windowish(p):
        return "WINDOW_OPERATION_DIY", "Explicit window operation/removal/replacement procedure", "HIGH"

    # Measurements/dimensions tied to installation are informational evidence,
    # matching the direct Step-09 result for 'установка пластиковых окон размером'.
    if has(p, "размер", "замер") and has(p, "установ", "монтаж") and windowish(p):
        return "WINDOW_MEASUREMENT_INFO", "Explicit measurement/dimension task connected with installation", "HIGH"

    # Selection is intentionally narrow: only explicit choose/selection wording.
    if has(p, "как выбрать", "выбрать", "выбираем", "выбор"):
        if has(p, "rehau", "рехау") and has(p, "профил", "систем"):
            return "REHAU_SELECTION_INFO", "Explicit Rehau profile/system selection task", "HIGH"
        if windowish(p):
            return "WINDOW_SELECTION_INFO", "Explicit window-selection task", "HIGH"

    # --- Demolition before installation. ---
    if "демонтаж" in p and windowish(p):
        return "WINDOW_DEMOLITION", "Explicit window/glazing demolition task", "HIGH"

    # --- Strong informational types that must not be swallowed by commercial terms. ---
    if has(p, "отзыв") and windowish(p):
        return "WINDOW_REVIEWS_INFO", "Explicit reviews task", "HIGH"

    # The word 'конструкция' is informational only when the query asks about the
    # construction/types, not when it merely describes a commercial glazing system.
    if has(p, "конструкция", "устройство", "схема", "режим") and windowish(p):
        if has(p, "остеклен") and has(p, "веранд", "террас", "балкон", "лоджи") and not has(p, "конструкция остекления", "конструкция балко", "виды", "какие конструкции"):
            pass
        else:
            return "WINDOW_TECH_INFO", "Explicit technical/construction information task", "HIGH"

    # Explicit DIY installation only when a procedural cue is present.
    if has(p, "пошаг", "своими руками", "как установить", "как монтировать", "видео установки", "видео монтаж") and has(p, "установ", "монтаж") and windowish(p):
        return "WINDOW_INSTALLATION_DIY", "Explicit procedural/DIY installation task", "HIGH"

    # --- Material/product priorities. ---
    # Timber-aluminium is a distinct material product and must beat generic aluminium.
    if has(p, "дерево алюмини", "дерево-алюмини", "деревоалюмини") and windowish(p):
        return "WOOD_WINDOWS_COMMERCIAL", "Explicit timber-aluminium window product", "HIGH"

    # PVC windows installed in a wooden house are still PVC windows, not wooden windows.
    if has(p, "пластиков", "пвх") and windowish(p) and has(p, "деревянном доме", "деревянный дом", "деревянного дома"):
        return "PVC_WINDOWS_COMMERCIAL", "PVC-window product/use case for a wooden house; house material does not change window material", "HIGH"

    if has(p, "деревянн") and windowish(p):
        return "WOOD_WINDOWS_COMMERCIAL", "Explicit wooden-window product task", "HIGH"

    # --- Panoramic-window logic: only clear product/purchase wording is commercial. ---
    if "панорам" in p and windowish(p):
        real_estate_patterns = (
            "дом с панорам", "дома с панорам", "барнхаус с панорам", "дача с панорам",
            "апартамент", "гостиная с панорам", "баня с панорам", "бассейн с панорам",
            "панорамные окна лес", "интерьер с панорам", "проект дома",
        )
        if has(p, *real_estate_patterns):
            return "OUTSIDE_REAL_ESTATE", "Explicit real-estate/house-project/inspiration task", "HIGH"
        commercial_markers = (
            "купить", "заказать", "цена", "цены", "стоимость", "производител", "монтаж",
            "установка", "элитн", "пластиков", "алюмини", "деревянн", "размер", "профиль",
        )
        if p in {"панорамные окна", "панорамное окно"} or has(p, *commercial_markers):
            return "PANORAMIC_WINDOWS_COMMERCIAL", "Explicit panoramic-window product/purchase task", "HIGH"
        # Vague context such as 'барбекю с панорамными окнами' is not safe to call a purchase.
        return None, "Panoramic-window phrase lacks enough evidence to distinguish product purchase from architecture/inspiration/context", "LOW"

    # --- Direct Step-09 known exact boundary classes. ---
    # This exact query was observed as comparison/mixed-commercial, not plain Rehau purchase.
    if p == "окна rehau kbe" or p == "окна рехау kbe":
        return "WINDOW_COMPARISON_INFO", "Direct Step-09 SERP shows Rehau-vs-KBE comparison boundary", "HIGH"

    if p == "установка пластиковых окон размером":
        return "WINDOW_MEASUREMENT_INFO", "Direct Step-09 SERP shows measurement information rather than installation service", "HIGH"

    if p == "цены материала на пластиковые окна":
        return None, "Direct Step-09 evidence is mixed/ambiguous price-material boundary; do not force a cluster", "LOW"

    # Morphology correction for Russian genitive/plural 'окон'. It only normalizes
    # the form before reusing the existing conservative rules; it adds no evidence.
    result = _base_classifier(phrase)
    if result[0] is not None:
        return result
    normalized = re.sub(r"\bокон(?=\b|\s)", "окн", phrase, flags=re.IGNORECASE)
    if normalized != phrase:
        return _base_classifier(normalized)
    return result


b.classify_semantic = classify_v3

if __name__ == "__main__":
    runner.main()
