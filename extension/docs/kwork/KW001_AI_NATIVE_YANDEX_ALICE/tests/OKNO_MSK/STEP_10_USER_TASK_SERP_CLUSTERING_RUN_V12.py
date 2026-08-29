#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Applies V11 -> V10 -> V9 -> V8 -> ... corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V11  # noqa: F401,E402

_v11_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def classify_v12(phrase: str):
    p = n(phrase)

    # Exact Step-09 evidence has priority over the generic private-house fallback.
    # SP09-011 observed a COMMERCIAL_SERVICE porch-glazing SERP for this exact
    # phrase, so the evidence must stay attached only to this phrase and must not be
    # rewritten as a generic private-house window-product task.
    if p == "крыльцо для частного дома окна":
        return "PORCH_GLAZING", "Exact Step-09 SP09-011 evidence identifies porch glazing as a commercial service; no evidence transfer to other private-house phrases", "HIGH"

    return _v11_classifier(phrase)


b.classify_semantic = classify_v12


def self_test() -> None:
    porch = b.classify_semantic("крыльцо для частного дома окна")
    assert porch[0] == "PORCH_GLAZING", porch

    # Preserve V11 precedence corrections while fixing only the exact Step-09
    # porch-glazing anchor.
    regressions = {
        "как называется дом с панорамными окнами": "OUTSIDE_REAL_ESTATE",
        "деревянные окна для частного дома": "WOOD_WINDOWS_COMMERCIAL",
        "алюминиевые окна для частного дома": "ALUMINIUM_WINDOWS_COMMERCIAL",
        "пластиковые окна для частного дома": "PVC_WINDOWS_COMMERCIAL",
        "окна rehau для частного дома": "REHAU_WINDOWS_COMMERCIAL",
        "установка пластиковых окон в частном доме": "WINDOW_INSTALLATION",
        "ремонт пластиковых окон в частном доме": "WINDOW_REPAIR",
        "окна для частного дома": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "виды окон для частного дома": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "цены материала на пластиковые окна": None,
    }
    for phrase, task in regressions.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


if __name__ == "__main__":
    self_test()
    runner.main()
