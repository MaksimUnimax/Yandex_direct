#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V16 as v16

_v16_classifier = b.classify_semantic


def classify_v17(phrase: str):
    p = v16.v15.n(phrase)

    # Exact Step-09 SP09-011 evidence has priority only for this exact phrase.
    # The SERP observed a porch-glazing COMMERCIAL_SERVICE task. This rule must not
    # transfer that evidence to lexical neighbours or generic private-house phrases.
    if p == "крыльцо для частного дома окна":
        return "PORCH_GLAZING", "Exact Step-09 SP09-011 evidence identifies porch glazing as a commercial service; evidence is exact-query only and is not transferred", "HIGH"

    # Final precedence guard for window-headed French-window product/configuration
    # phrases. Old V10 treated any apartment-context token as real-estate context,
    # even in queries such as 'французские окна в москве в квартирах'. Keep only
    # genuinely dwelling-headed constructions ('квартира с французскими окнами')
    # outside the product task.
    french_window_headed = bool(
        re.search(r"\bфранцуз\w*\s+окн\w*\b", p)
        or re.search(r"\bокн\w*\s+француз\w*\b", p)
    )
    french_product_signal = v16.v15.has(
        p,
        "купить", "заказать", "цена", "цены", "стоимость", "сколько стоит", "сколько стоят",
        "производ", "москва", "подмосков", "на балкон", "балконный блок", "ароч", "стеклопак",
        "пластиков", "пвх", "алюмини", "деревян", "готов", "больш", "высок", "маленьк", "широк", "узк",
    )
    if (
        french_window_headed
        and french_product_signal
        and not v16.v15.architecture_subject_with_windows(p)
    ):
        return "FRENCH_WINDOWS_COMMERCIAL", "Window-headed French-window product/configuration demand has priority over incidental apartment/house context", "HIGH"

    return _v16_classifier(phrase)


b.classify_semantic = classify_v17


def self_test() -> None:
    # Re-run the full V15 + V16 regression corpus against the final wrapped classifier.
    v16.self_test()

    porch = b.classify_semantic("крыльцо для частного дома окна")
    assert porch[0] == "PORCH_GLAZING", porch

    french = b.classify_semantic("французские окна в москве в квартирах")
    assert french[0] == "FRENCH_WINDOWS_COMMERCIAL", french
    french_balcony = b.classify_semantic("французское окно на балкон в квартире")
    assert french_balcony[0] == "FRENCH_WINDOWS_COMMERCIAL", french_balcony

    # Direct mixed evidence stays unresolved rather than being force-clustered.
    mixed = b.classify_semantic("цены материала на пластиковые окна")
    assert mixed[0] is None, mixed


if __name__ == "__main__":
    self_test()
    runner.main()
