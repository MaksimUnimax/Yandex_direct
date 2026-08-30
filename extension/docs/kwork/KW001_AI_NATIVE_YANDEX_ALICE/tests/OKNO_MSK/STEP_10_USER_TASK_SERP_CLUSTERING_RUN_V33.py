#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V32 as v32

_v32_classifier = b.classify_semantic

b.TASKS.update({
    "OUTSIDE_CURTAINS_HARDWARE": ("Фурнитура и комплектующие для штор/жалюзи", "COMMERCIAL_PRODUCT", "OUTSIDE"),
})


def classify_v33(phrase: str):
    p = b.norm(phrase)
    curtain = any(x in p for x in ("жалюз", "штор", "занавес", "день ночь"))
    hardware = any(x in p for x in ("фурнитур", "комплектующ", "крепеж", "креплен", "механизм", "кронштейн"))

    # Full manual QA found that blind/curtain hardware is neither the blind product
    # itself nor window hardware. The accessory is the head object; window wording
    # merely describes where the blind is used.
    if curtain and hardware:
        return "OUTSIDE_CURTAINS_HARDWARE", "Blind/curtain hardware is the head product and stays outside the window-core taxonomy", "HIGH"

    return _v32_classifier(phrase)


b.classify_semantic = classify_v33


def self_test() -> None:
    v32.self_test()
    expected = {
        "фурнитура для жалюзей оконных": "OUTSIDE_CURTAINS_HARDWARE",
        "оконные жалюзи фурнитура": "OUTSIDE_CURTAINS_HARDWARE",
        "установка жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_INSTALLATION",
        "ремонт жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_REPAIR_SERVICE",
        "как выбрать жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_SELECTION_INFO",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


if __name__ == "__main__":
    self_test()
    runner.main()
