#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V20 as v20

_v20_classifier = b.classify_semantic
base = v20.base


def classify_v21(phrase: str):
    p = base.n(phrase)
    win = base.windowish(p)

    # V20 introduced an intentionally conservative contextual-repair boundary.
    # Preserve V19's accepted stronger signal: explicit cleaning/care wording wins
    # even when 'ремонт' appears only as context ('после ремонта').
    if win and base.has(p, "отмыть", "очистить", "очистка", "помыть", "мыть окна", "чем очистить", "чем отмыть"):
        return "WINDOW_CARE_INFO", "Explicit cleaning/care action outranks incidental repair wording", "HIGH"

    return _v20_classifier(phrase)


b.classify_semantic = classify_v21


def self_test() -> None:
    # Re-run V19 + V20 regression suites against the final V21 classifier.
    v20.self_test()
    expected = {
        "чем отмыть пластиковые окна после ремонта": "WINDOW_CARE_INFO",
        "чем очистить пластиковые окна после ремонта": "WINDOW_CARE_INFO",
        "очистить пластиковые окна ремонта": "WINDOW_CARE_INFO",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


if __name__ == "__main__":
    self_test()
    runner.main()
