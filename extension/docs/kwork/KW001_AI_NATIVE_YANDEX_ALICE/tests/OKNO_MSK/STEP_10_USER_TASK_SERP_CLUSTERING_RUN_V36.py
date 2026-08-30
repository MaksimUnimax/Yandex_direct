#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V35 as v35

_v35_classifier = b.classify_semantic


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def classify_v36(phrase: str):
    p = b.norm(phrase)
    curtain = has(p, "жалюз", "штор", "занавес", "день ночь", "плиссе")
    price = has(p, "цена", "цены", "стоимость", "сколько стоит")

    # A blind/curtain head object remains the outside-core product even when the
    # phrase also contains PVC-window context plus photo/price modifiers. This
    # must outrank V34's generic PVC-window commercial photo+price rule.
    if curtain and price and "фото" in p:
        return "OUTSIDE_CURTAINS", "Blind/curtain is the head product; photo and price are shopping modifiers and window wording is context", "HIGH"

    return _v35_classifier(phrase)


b.classify_semantic = classify_v36


def self_test() -> None:
    v35.self_test()
    assert b.classify_semantic("жалюзи на пластиковые окна фото цена")[0] == "OUTSIDE_CURTAINS"
    assert b.classify_semantic("жалюзи зебра на пластиковые окна фото цены")[0] == "OUTSIDE_CURTAINS"


if __name__ == "__main__":
    self_test()
    runner.main()
