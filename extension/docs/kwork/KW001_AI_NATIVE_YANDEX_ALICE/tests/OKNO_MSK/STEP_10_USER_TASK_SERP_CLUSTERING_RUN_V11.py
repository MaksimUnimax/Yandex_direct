#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V9 as v9mod
# Applies V10 -> V9 -> V8 -> ... corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V10  # noqa: F401,E402

_v10_classifier = b.classify_semantic
# V9 captured the full V8 classifier before introducing the broad private-house
# overlay. Use it as a precedence probe for specific material/action tasks.
_pre_private_classifier = v9mod._v8_classifier


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def classify_v11(phrase: str):
    p = n(phrase)
    win = windowish(p)

    # A naming question about the HOUSE is an architecture/real-estate task. This
    # is distinct from 'что такое французское окно', where the object being defined
    # is the window itself.
    if win and has(p, "панорам", "француз") and has(p, "как называется дом", "что за дом", "тип дома", "вид дома"):
        return "OUTSIDE_REAL_ESTATE", "Naming/classifying a house with panoramic/French windows is an architecture/real-estate task", "HIGH"

    # Keep V10's dedicated panoramic/French semantics ahead of the generic
    # private-house fallback.
    if win and has(p, "панорам", "француз"):
        return _v10_classifier(phrase)

    private_house = win and has(p, "частного дома", "частный дом", "в частном доме", "для дома")
    if private_house:
        # First ask the validated pre-private classifier whether the phrase already
        # has a more specific task: installation, repair, replacement, dimensions,
        # reviews, material family (PVC/aluminium/wood/Rehau), hardware, etc.
        specific = _pre_private_classifier(phrase)
        if specific[0] is not None:
            return specific

        # Only genuinely generic private-house phrases reach this fallback.
        if has(p, "требован", "норматив", "норма ", "вентиляц", "какое должно", "какой должен", "площадь остекления"):
            return "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO", "Explicit requirements/special-condition information task for a private-house window", "HIGH"
        if has(p, "варианты", "виды", "какие окна", "какое окно", "образцы", "выбор"):
            return "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO", "Explicit private-house window selection/types task", "HIGH"
        return "PRIVATE_HOUSE_WINDOWS_COMMERCIAL", "Generic window product/use-case demand for a private house after specific material/action tasks were excluded", "MEDIUM"

    return _v10_classifier(phrase)


b.classify_semantic = classify_v11


def self_test() -> None:
    expected = {
        "как называется дом с панорамными окнами": "OUTSIDE_REAL_ESTATE",
        "что такое французское окно в квартире фото": "WINDOW_DEFINITION_INFO",
        "деревянные окна для частного дома": "WOOD_WINDOWS_COMMERCIAL",
        "алюминиевые окна для частного дома": "ALUMINIUM_WINDOWS_COMMERCIAL",
        "пластиковые окна для частного дома": "PVC_WINDOWS_COMMERCIAL",
        "окна rehau для частного дома": "REHAU_WINDOWS_COMMERCIAL",
        "установка пластиковых окон в частном доме": "WINDOW_INSTALLATION",
        "ремонт пластиковых окон в частном доме": "WINDOW_REPAIR",
        "размеры пластиковых окон для частного дома": "WINDOW_DIMENSIONS_INFO",
        "окна для частного дома отзывы": "WINDOW_REVIEWS_INFO",
        "окно для котельной в частном доме": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "окно для газовой котельной частного дома требования": "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO",
        "окна для частного дома": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "виды окон для частного дома": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


if __name__ == "__main__":
    self_test()
    runner.main()
