#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V30 as v30

_v30_classifier = b.classify_semantic


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish_v31(p: str) -> bool:
    # Keep both stem orders: Russian inflection has окна/окно (окн) and
    # окон/оконный/оконная (окон); neither substring subsumes the other.
    return has(p, "окн", "окон", "rehau", "рехау")


def classify_v31(phrase: str):
    p = b.norm(phrase)
    win = windowish_v31(p)
    diy = has(p, "своими руками", "самостоятель", "самому")

    # Re-apply V28 rules whose local 'окн' shorthand missed genitive/adjectival
    # forms such as 'окон' and 'оконная'.
    if win and has(p, "размер", "ширин", "высот", "габарит") and "фото" in p:
        return "WINDOW_DIMENSIONS_INFO", "Dimensions are the head task; photo is only a representation modifier", "HIGH"
    if win and has(p, "установ", "монтаж") and has(p, "размер", "размером", "размерами", "замер") and not diy:
        return "WINDOW_MEASUREMENT_INFO", "Measurement/dimension task connected with installation", "HIGH"
    if win and has(p, "зазор при установке", "правильная установка"):
        return "WINDOW_INSTALLATION_INFO", "Explicit installation requirements/guidance task", "HIGH"

    hardware_context = has(p, "фурнитур", "ручк", "уплотн", "петл", "замок", "механизм", "профил") and win
    if hardware_context and has(p, "как называется", "как устроена", "конструкция", "устройство", "основные функции", "что входит"):
        return "WINDOW_TECH_INFO", "Explicit technical/definition information task about window hardware", "HIGH"
    if hardware_context and has(p, "как выбрать", "какая бывает", "виды", "типы", "лучшая", "лучший"):
        return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit selection/types task about window hardware/components", "HIGH"

    return _v30_classifier(phrase)


b.classify_semantic = classify_v31


def self_test() -> None:
    # V30 calls the complete current V29 corpus; running it against V31 proves
    # both prior corrections and the morphology repair together.
    v30.self_test()
    expected = {
        "размеры окон для частного дома фото": "WINDOW_DIMENSIONS_INFO",
        "установка пластиковых окон размером": "WINDOW_MEASUREMENT_INFO",
        "зазор при установке пластиковых окон": "WINDOW_INSTALLATION_INFO",
        "правильная установка пластиковых окон": "WINDOW_INSTALLATION_INFO",
        "оконная фурнитура виды": "WINDOW_ACCESSORY_SELECTION_INFO",
        "как называется оконная фурнитура": "WINDOW_TECH_INFO",
        "как устроена оконная фурнитура": "WINDOW_TECH_INFO",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


if __name__ == "__main__":
    self_test()
    runner.main()
