#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V29 as v29

_v29_classifier = b.classify_semantic


def classify_v30(phrase: str):
    p = b.norm(phrase)

    # Manual-QA regression: 'день-ночь' is a blind/curtain product name even
    # when the literal words жалюзи/шторы are absent. Preserve the action head.
    if "день ночь" in p and ("окн" in p or "двер" in p):
        if any(x in p for x in ("установ", "монтаж")):
            return "OUTSIDE_CURTAINS_INSTALLATION", "Day-night blind is the head object and installation is the explicit action", "HIGH"
        if any(x in p for x in ("ремонт", "почин")):
            return "OUTSIDE_CURTAINS_REPAIR_SERVICE", "Day-night blind is the head object and repair is the explicit action", "HIGH"
        if any(x in p for x in ("как выбрать", "какие выбрать", "какую выбрать")):
            return "OUTSIDE_CURTAINS_SELECTION_INFO", "Explicit selection of day-night blinds", "HIGH"
        return "OUTSIDE_CURTAINS", "Day-night blind is an outside-core curtain/blind product", "HIGH"

    return _v29_classifier(phrase)


b.classify_semantic = classify_v30


def self_test() -> None:
    # Re-run the full current V29 corpus against the corrected V30 classifier.
    v29.self_test()
    got = b.classify_semantic("день ночь на пластиковые окна установка")
    assert got[0] == "OUTSIDE_CURTAINS_INSTALLATION", got


if __name__ == "__main__":
    self_test()
    runner.main()
