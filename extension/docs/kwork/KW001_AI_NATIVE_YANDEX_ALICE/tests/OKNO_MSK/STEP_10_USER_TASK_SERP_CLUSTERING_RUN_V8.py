#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Applies V7 -> V6 -> V5 -> V4 -> V3 corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V7  # noqa: F401,E402

_v7_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def classify_v8(phrase: str):
    p = n(phrase)

    # Final adversarial correction: replacing a component of an existing window is
    # repair/maintenance even when price/PVC wording would otherwise trigger the
    # generic commercial-product classifier.
    component_replacement = (
        windowish(p)
        and has(p, "замена", "заменить", "поменять")
        and has(p, "ручк", "уплотн", "резин", "проклад", "стеклопак", "петл", "фурнитур", "замк", "механизм")
    )
    if component_replacement:
        return "WINDOW_REPAIR", "Replacement of an existing-window component is a repair/maintenance task, not window purchase", "HIGH"

    # 'Замена балкона на пластиковые окна' does not specify a normal whole-window
    # replacement job. It may mean balcony glazing, replacement of an old balcony
    # frame, or malformed wording. Preserve uncertainty instead of forcing it into
    # the generic PVC-window purchase cluster.
    if "замена балкона" in p and windowish(p) and has(p, "пластик", "пвх"):
        return None, "Balcony-to-PVC-window replacement wording is materially ambiguous; direct Search evidence is required", "LOW"

    return _v7_classifier(phrase)


b.classify_semantic = classify_v8


def self_test() -> None:
    handle = b.classify_semantic("замена ручек на пластиковых окнах цена")
    assert handle[0] == "WINDOW_REPAIR", handle

    balcony = b.classify_semantic("замена балкона на пластиковые окна цена")
    assert balcony[0] is None, balcony


if __name__ == "__main__":
    self_test()
    runner.main()
