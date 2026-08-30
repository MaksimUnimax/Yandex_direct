#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V21 as v21

_v21_classifier = b.classify_semantic
base = v21.base


def classify_v22(phrase: str):
    p = base.n(phrase)

    # Specific material-selection information must outrank the generic material
    # product rule introduced in V20.
    if "остеклен" in p and "толщина" in p and "поликарбонат" in p:
        return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit material-thickness/selection task for a glazing material", "HIGH"

    return _v21_classifier(phrase)


b.classify_semantic = classify_v22


def self_test() -> None:
    # Run the complete inherited V19/V20/V21 regression corpus against V22.
    v21.self_test()
    got = b.classify_semantic("толщина монолитного поликарбоната для остекления веранды")
    assert got[0] == "WINDOW_ACCESSORY_SELECTION_INFO", got


if __name__ == "__main__":
    self_test()
    runner.main()
