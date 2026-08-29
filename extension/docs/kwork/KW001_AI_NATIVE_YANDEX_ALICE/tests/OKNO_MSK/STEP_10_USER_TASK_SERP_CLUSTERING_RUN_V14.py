#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V13 as v13  # noqa: F401,E402

_v13_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def classify_v14(phrase: str):
    p = n(phrase)
    win = windowish(p)
    private_house = has(p, "частного дома", "частный дом", "в частном доме", "для дома")
    explicit_pvc = has(p, " пвх", "пвх ")

    # Dimension/information task beats material and private-house product routing.
    if win and has(p, "размер", "ширина", "высота", "габарит") and not has(
        p, "купить", "заказать", "цена", "цены", "стоимость", "установ", "монтаж"
    ):
        return "WINDOW_DIMENSIONS_INFO", "Explicit size/dimension information task has priority over PVC material and private-house product routing", "HIGH"

    # For explicit PVC wording in a private-house phrase, preserve any more specific
    # pre-V13 task (installation, repair, selection, etc.). Only replace the old
    # generic private-house product fallback with the PVC product family.
    if win and private_house and explicit_pvc:
        prior = v13._v12_classifier(phrase)
        if prior[0] is not None and prior[0] != "PRIVATE_HOUSE_WINDOWS_COMMERCIAL":
            return prior
        return "PVC_WINDOWS_COMMERCIAL", "Explicit PVC-window material defines the product task; private-house wording remains a use-case modifier", "HIGH"

    return _v13_classifier(phrase)


b.classify_semantic = classify_v14


def self_test() -> None:
    expected = {
        "окна пвх для частного дома": "PVC_WINDOWS_COMMERCIAL",
        "окна пвх для частного дома цена": "PVC_WINDOWS_COMMERCIAL",
        "размеры окон пвх для частного дома": "WINDOW_DIMENSIONS_INFO",
        "размеры окон пвх стандартные для частного дома": "WINDOW_DIMENSIONS_INFO",
        "стандартные размеры панорамных окон для частного дома": "WINDOW_DIMENSIONS_INFO",
        "установка окон пвх в частном доме": "WINDOW_INSTALLATION",
        "ремонт окон пвх в частном доме": "WINDOW_REPAIR",
        "как выбрать окна пвх для частного дома": "WINDOW_SELECTION_INFO",
        "крыльцо для частного дома окна": "PORCH_GLAZING",
        "деревянные окна для частного дома": "WOOD_WINDOWS_COMMERCIAL",
        "алюминиевые окна для частного дома": "ALUMINIUM_WINDOWS_COMMERCIAL",
        "как называется дом с панорамными окнами": "OUTSIDE_REAL_ESTATE",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


if __name__ == "__main__":
    self_test()
    runner.main()
