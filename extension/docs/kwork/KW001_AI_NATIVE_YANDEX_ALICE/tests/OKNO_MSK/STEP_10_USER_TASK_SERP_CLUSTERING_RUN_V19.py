#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V18 as v18

_v18_classifier = b.classify_semantic
base = v18.v17.v16.v15


def classify_v19(phrase: str):
    p = base.n(phrase)
    win = base.windowish(p)
    private_house = base.is_private_house(p)
    panoramic = "панорам" in p and win
    french = "француз" in p and (win or "балконный блок" in p or "французский балкон" in p)

    # Care/cleaning is an informational maintenance task, not a repair service merely
    # because the phrase also contains the word 'ремонт' as context ('после ремонта').
    if win and base.has(p, "отмыть", "очистить", "очистка", "помыть", "мыть окна", "чем очистить", "чем отмыть"):
        return "WINDOW_CARE_INFO", "Explicit cleaning/care action outranks incidental repair wording", "HIGH"

    # Mosquito/protection accessories outrank numeric dimensions of the accessory.
    if base.has(p, "москит", "антикошка", "сетка на", "сетку на", "сетка для", "сетку для") and base.has(p, "окн", "окон", "двер"):
        return "MOSQUITO_NETS", "Mosquito/protection accessory is the head object; its dimensions are only a product modifier", "HIGH"

    # Repair compounds/materials are accessory/material demand, not a request for a repair service.
    if win and base.has(p, "жидкий пластик", "средство для ремонта"):
        return "WINDOW_ACCESSORIES", "Explicit repair compound/material is the head product rather than a repair-service request", "HIGH"

    # Ready-made window product listings remain commercial products even when an AxB
    # size is present. Brand/model specificity wins before the dimension-info rule.
    if win and "готов" in p:
        if base.has(p, "rehau", "рехау"):
            if base.has(p, "blitz", "блиц", "thermo", "термо", "grazio", "грацио", "delight", "делайт", "intelio", "интелио", "geneo", "генео"):
                return "REHAU_PRODUCT_SUBTYPE", "Ready-made Rehau window with an explicit system/model remains a product-subtype demand; dimensions are configuration", "HIGH"
            return "REHAU_WINDOWS_COMMERCIAL", "Ready-made Rehau window remains a commercial product; dimensions are configuration", "HIGH"
        if base.has(p, "пластиков", "пвх"):
            return "PVC_WINDOWS_COMMERCIAL", "Ready-made PVC window remains a commercial product; dimensions are configuration", "HIGH"
        if "алюмини" in p:
            return "ALUMINIUM_WINDOWS_COMMERCIAL", "Ready-made aluminium window remains a commercial product; dimensions are configuration", "HIGH"
        if "деревян" in p:
            return "WOOD_WINDOWS_COMMERCIAL", "Ready-made wooden window remains a commercial product; dimensions are configuration", "HIGH"

    # Object-specific glazing is a service task and must outrank panoramic/French,
    # material, and private-house overlays. Reuse V15's already-tested object routing.
    glazing_result = base.object_glazing_task(p)
    if glazing_result is not None:
        return glazing_result

    # Specific panoramic/French window family beats generic private-house fallback.
    # Explicit informational wording remains informational for that specific family.
    specific_info = base.has(p, "виды", "варианты", "формы", "плюсы", "минусы", "как выбрать", "какие", "особенности", "сравн")
    if panoramic and private_house:
        if specific_info:
            return "PANORAMIC_WINDOWS_INFO", "Specific panoramic-window informational task outranks generic private-house fallback", "HIGH"
        return "PANORAMIC_WINDOWS_COMMERCIAL", "Specific panoramic-window product/use-case outranks generic private-house fallback", "HIGH"
    if french and private_house:
        if specific_info:
            return "PANORAMIC_WINDOWS_INFO", "Specific French-window informational task stays with the specific-window information family", "HIGH"
        return "FRENCH_WINDOWS_COMMERCIAL", "Specific French-window product/use-case outranks generic private-house fallback", "HIGH"

    # Generic private-house shapes/types are selection/information, not purchase intent.
    if win and private_house and base.has(p, "формы", "форма окон", "виды", "варианты", "выбираем", "выбрать") and not base.has(
        p, "купить", "заказать", "цена", "цены", "стоимость"
    ):
        return "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO", "Explicit forms/types/selection wording makes this a private-house selection task", "HIGH"

    # French-window product/configuration phrases should not remain SEARCH_REQUIRED when
    # the window is the head object and a clear configuration/use-case marker is present.
    french_config = base.has(
        p,
        "в пол", "на лоджи", "на террас", "на балкон", "раздвиж", "с двер", "балконный блок",
        "москв", "подмосков", "купить", "заказать", "цена", "цены", "стоимость", "производ",
        "стеклопак", "ароч", "пластиков", "пвх", "алюмини", "деревян", "готов", "больш", "высок", "широк", "узк",
    )
    explicit_action = base.has(p, "замена", "заменить", "поменять", "ремонт", "регулир", "установ", "монтаж")
    if french and french_config and not explicit_action and not specific_info and not base.architecture_subject_with_windows(p):
        return "FRENCH_WINDOWS_COMMERCIAL", "Clear French-window product/configuration/use-case demand; no stronger action or dwelling-headed context is present", "HIGH"

    return _v18_classifier(phrase)


b.classify_semantic = classify_v19


def self_test() -> None:
    v18.self_test()

    expected = {
        "готовое пластиковое окно двухстворчатое 1000x1200 rehau": "REHAU_WINDOWS_COMMERCIAL",
        "готовые окна rehau blitz 1200x1000": "REHAU_PRODUCT_SUBTYPE",
        "москитная сетка на пластиковые окна rehau 133х45": "MOSQUITO_NETS",
        "жидкий пластик для ремонта пластиковых окон": "WINDOW_ACCESSORIES",
        "средство для ремонта пластиковых окон": "WINDOW_ACCESSORIES",
        "очистить пластиковые окна ремонта": "WINDOW_CARE_INFO",
        "чем отмыть пластиковые окна после ремонта": "WINDOW_CARE_INFO",
        "чем очистить пластиковые окна после ремонта": "WINDOW_CARE_INFO",
        "застекление веранды в частном доме панорамное остекление": "VERANDA_GLAZING",
        "деревянное остекление веранды": "VERANDA_GLAZING",
        "остекление веранды в деревянном доме": "VERANDA_GLAZING",
        "панорамные окна в частном доме": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамные окна для частного дома": "PANORAMIC_WINDOWS_COMMERCIAL",
        "французские окна в частном доме": "FRENCH_WINDOWS_COMMERCIAL",
        "формы окон для частных домов": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "окна для крыши частных домов": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "панорамное окно на крыше": "PANORAMIC_WINDOWS_COMMERCIAL",
        "французские окна в пол": "FRENCH_WINDOWS_COMMERCIAL",
        "французские окна на лоджию": "FRENCH_WINDOWS_COMMERCIAL",
        "французские окна на террасе": "FRENCH_WINDOWS_COMMERCIAL",
        "французский балкон окно в пол": "FRENCH_WINDOWS_COMMERCIAL",
        "французское окно раздвижное": "FRENCH_WINDOWS_COMMERCIAL",
        "французское окно с дверью": "FRENCH_WINDOWS_COMMERCIAL",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)

    # Preserve already-fixed higher-priority boundaries.
    assert b.classify_semantic("замена балконного блока на французское окно")[0] == "WINDOW_REPLACEMENT_SERVICE"
    assert b.classify_semantic("ремонт и замена пластиковых окон")[0] is None
    assert b.classify_semantic("квартира с французскими окнами")[0] == "OUTSIDE_REAL_ESTATE"
    assert b.classify_semantic("крыльцо для частного дома окна")[0] == "PORCH_GLAZING"
    assert b.classify_semantic("размеры окон пвх для частного дома")[0] == "WINDOW_DIMENSIONS_INFO"


if __name__ == "__main__":
    self_test()
    runner.main()
