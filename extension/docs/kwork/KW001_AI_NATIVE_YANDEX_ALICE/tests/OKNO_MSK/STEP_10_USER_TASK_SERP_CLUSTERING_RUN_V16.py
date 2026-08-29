#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V15 as v15

_v15_classifier = b.classify_semantic


def classify_v16(phrase: str):
    result = _v15_classifier(phrase)
    p = v15.n(phrase)

    # V8 (used as the specific-task probe inside V15) predates explicit handling of
    # the Russian abbreviation 'ПВХ'. Only repair the final generic private-house
    # fallback; all more-specific V15 tasks remain untouched.
    if (
        result[0] == "PRIVATE_HOUSE_WINDOWS_COMMERCIAL"
        and v15.is_private_house(p)
        and v15.windowish(p)
        and "пвх" in p
    ):
        return "PVC_WINDOWS_COMMERCIAL", "Explicit PVC-window material defines the product task; private-house wording remains a use-case modifier", "HIGH"

    return result


b.classify_semantic = classify_v16


def self_test() -> None:
    # Re-run the full V15 regression corpus against the wrapped classifier.
    v15.self_test()
    expected = {
        "окна пвх для частного дома": "PVC_WINDOWS_COMMERCIAL",
        "окна пвх для частного дома цена": "PVC_WINDOWS_COMMERCIAL",
        "как выбрать окна пвх для частного дома": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "размеры окон пвх для частного дома": "WINDOW_DIMENSIONS_INFO",
        "установка окон пвх в частном доме": "WINDOW_INSTALLATION",
        "ремонт окон пвх в частном доме": "WINDOW_REPAIR",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


if __name__ == "__main__":
    self_test()
    runner.main()
