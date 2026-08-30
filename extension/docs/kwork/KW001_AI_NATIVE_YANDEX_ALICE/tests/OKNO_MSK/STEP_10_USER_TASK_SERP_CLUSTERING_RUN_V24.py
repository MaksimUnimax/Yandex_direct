#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V23 as v23

_v23_classifier = b.classify_semantic
base = v23.base

b.TASKS.update({
    "WINDOWSILL_INSTALLATION_SERVICE": ("Установка/монтаж подоконников", "COMMERCIAL_SERVICE", "ADJACENT"),
    "WINDOW_HARDWARE_INSTALLATION_SERVICE": ("Установка/монтаж оконной фурнитуры", "COMMERCIAL_SERVICE", "ADJACENT"),
})


def classify_v24(phrase: str):
    p = base.n(phrase)
    install = base.has(p, "установ", "монтаж")
    diy = base.has(p, "своими руками", "самостоятель", "самому")

    # A bare/contextual 'windowsill after window installation' phrase does not
    # itself prove demand for a windowsill-installation service.
    if "подокон" in p and "после установ" in p and not re.search(r"\b(?:установка|монтаж)\w*\s+(?:деревянн\w*\s+)?подокон", p):
        return None, "Windowsill is mentioned only in post-window-installation context; exact user task remains ambiguous", "LOW"

    # Dedicated windowsill installation service. DIY remains procedural.
    if "подокон" in p and install:
        if diy:
            return "WINDOW_FINISHING_DIY", "Explicit DIY windowsill installation is a procedural finishing task", "HIGH"
        return "WINDOWSILL_INSTALLATION_SERVICE", "Explicit professional windowsill installation task", "HIGH"

    # Installing window hardware is its own component-service task, not generic
    # whole-window repair/regulation.
    if install and base.has(p, "оконной фурнитур", "оконную фурнитур", "оконная фурнитур", "фурнитуры на", "фурнитуру на"):
        return "WINDOW_HARDWARE_INSTALLATION_SERVICE", "Explicit installation of window hardware/components", "HIGH"

    return _v23_classifier(phrase)


b.classify_semantic = classify_v24


def self_test() -> None:
    v23.self_test()
    expected = {
        "установка деревянного подоконника на пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна цена": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконников под пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка оконной фурнитуры": "WINDOW_HARDWARE_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна своими руками": "WINDOW_FINISHING_DIY",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)

    got = b.classify_semantic("подоконник после установки пластикового окна")
    assert got[0] is None, got


if __name__ == "__main__":
    self_test()
    runner.main()
