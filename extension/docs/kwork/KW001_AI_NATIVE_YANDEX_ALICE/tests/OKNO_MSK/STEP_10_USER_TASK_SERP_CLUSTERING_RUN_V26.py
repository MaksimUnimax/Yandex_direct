#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V25 as v25

_v25_classifier = b.classify_semantic
base = v25.v24.base

b.TASKS.update({
    "BALCONY_RENOVATION_WITH_GLAZING_SERVICE": ("Ремонт/отделка балкона с остеклением", "COMMERCIAL_SERVICE", "ADJACENT"),
    "BALCONY_GLAZING_REPAIR_SERVICE": ("Ремонт существующего балконного остекления", "COMMERCIAL_SERVICE", "ADJACENT"),
})


def classify_v26(phrase: str):
    p = base.n(phrase)
    balcony = base.has(p, "балкон", "лоджи")
    glazing = base.has(p, "остеклен", "застекл")

    # Explicit negative glazing remains unresolved/non-glazing. Do not let the
    # repair+glazing rules below turn 'без остекления' back into a glazing task.
    if "веранд" in p and "без остеклен" in p:
        return None, "Explicit no-glazing wording negates the glazing service; exact alternative task remains ambiguous", "LOW"

    # Combined balcony-renovation + glazing is a distinct service task when the
    # syntax explicitly states renovation WITH glazing.
    if balcony and "ремонт" in p and "с остеклен" in p:
        return "BALCONY_RENOVATION_WITH_GLAZING_SERVICE", "Explicit combined balcony renovation/repair with glazing service", "HIGH"

    # 'ремонт остекление/остекления балкона' is a repair task whose head object
    # is existing balcony glazing, including French-window subtype wording.
    if balcony and glazing and "ремонт" in p and "без остеклен" not in p:
        return "BALCONY_GLAZING_REPAIR_SERVICE", "Explicit repair of existing balcony glazing; glazing subtype/location is context", "HIGH"

    return _v25_classifier(phrase)


b.classify_semantic = classify_v26


def self_test() -> None:
    v25.self_test()
    expected = {
        "ремонт балкона с остеклением": "BALCONY_RENOVATION_WITH_GLAZING_SERVICE",
        "ремонт остекление балконов москва": "BALCONY_GLAZING_REPAIR_SERVICE",
        "ремонт остекление балкона французские окна": "BALCONY_GLAZING_REPAIR_SERVICE",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)

    got = b.classify_semantic("веранда без остекления")
    assert got[0] is None, got


if __name__ == "__main__":
    self_test()
    runner.main()
