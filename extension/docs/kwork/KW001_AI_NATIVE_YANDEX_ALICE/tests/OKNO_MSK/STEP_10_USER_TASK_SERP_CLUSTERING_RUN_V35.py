#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V34 as v34

_v34_classifier = b.classify_semantic


def classify_v35(phrase: str):
    p = b.norm(phrase)
    rehau = ("rehau" in p or "рехау" in p) and ("окн" in p or "окон" in p or "rehau" in p or "рехау" in p)

    # Brand-specific selection must outrank the generic PVC-window selection
    # fallback introduced in V34.
    if rehau and ("лучшие пластиковые окна rehau" in p or "окна rehau цвета" in p):
        return "REHAU_SELECTION_INFO", "Explicit Rehau quality/colour selection task outranks generic PVC-window selection", "HIGH"

    return _v34_classifier(phrase)


b.classify_semantic = classify_v35


def self_test() -> None:
    v34.self_test()
    assert b.classify_semantic("лучшие пластиковые окна rehau")[0] == "REHAU_SELECTION_INFO"
    assert b.classify_semantic("окна rehau цвета")[0] == "REHAU_SELECTION_INFO"


if __name__ == "__main__":
    self_test()
    runner.main()
