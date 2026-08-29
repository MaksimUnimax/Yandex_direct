#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Applies V12 -> V11 -> V10 -> ... corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V12  # noqa: F401,E402

_v12_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def classify_v13(phrase: str):
    p = n(phrase)
    win = windowish(p)

    # Explicit whole-window material beats a generic private-house use-case. The
    # house remains a modifier; the task is still a PVC-window product task.
    if win and has(p, "частного дома", "частный дом", "в частном доме", "для дома") and has(p, " пвх", "пвх "):
        return "PVC_WINDOWS_COMMERCIAL", "Explicit PVC-window material defines the product task; private-house wording remains a use-case modifier", "HIGH"

    # Explicit dimensions are an informational task even inside panoramic/private-
    # house wording, unless the phrase clearly asks to buy/order/price or install.
    if win and has(p, "размер", "ширина", "высота", "габарит") and not has(
        p, "купить", "заказать", "цена", "цены", "стоимость", "установ", "монтаж"
    ):
        return "WINDOW_DIMENSIONS_INFO", "Explicit size/dimension information task has priority over generic material/use-case product routing", "HIGH"

    return _v12_classifier(phrase)


b.classify_semantic = classify_v13


def self_test() -> None:
    expected = {
        "окна пвх для частного дома": "PVC_WINDOWS_COMMERCIAL",
        "окна пвх для частного дома цена": "PVC_WINDOWS_COMMERCIAL",
        "стандартные размеры панорамных окон для частного дома": "WINDOW_DIMENSIONS_INFO",
        "размеры пластиковых окон для частного дома": "WINDOW_DIMENSIONS_INFO",
        "ширина пластиковой двери": "PVC_DOOR_DIMENSIONS_INFO",
        "крыльцо для частного дома окна": "PORCH_GLAZING",
        "деревянные окна для частного дома": "WOOD_WINDOWS_COMMERCIAL",
        "алюминиевые окна для частного дома": "ALUMINIUM_WINDOWS_COMMERCIAL",
        "установка пластиковых окон в частном доме": "WINDOW_INSTALLATION",
        "ремонт пластиковых окон в частном доме": "WINDOW_REPAIR",
        "как называется дом с панорамными окнами": "OUTSIDE_REAL_ESTATE",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


if __name__ == "__main__":
    self_test()
    runner.main()
