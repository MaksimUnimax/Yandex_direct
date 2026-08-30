#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V22 as v22
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V24 as v24

_v24_classifier = b.classify_semantic


def classify_v25(phrase: str):
    return _v24_classifier(phrase)


b.classify_semantic = classify_v25


def self_test() -> None:
    # V23's historical self-test intentionally locked one pre-V24 taxonomy
    # decision ('установка оконной фурнитуры' -> WINDOW_REPAIR). V24 deliberately
    # superseded that decision with a dedicated installation-service task. Keep
    # history immutable and build the current regression corpus from the last
    # non-conflicting baseline (V22) plus all still-valid V23/V24 expectations.
    v22.self_test()

    expected = {
        # V23 action-head/component fixes that remain canonical.
        "замок для пластиковой двери": "WINDOW_HARDWARE",
        "механизм пластиковой двери": "WINDOW_HARDWARE",
        "многозапорный замок на пластиковые двери": "WINDOW_HARDWARE",
        "поменять стеклопакет на пластиковом окне цена": "WINDOW_REPAIR",
        "монтаж откосов на пластиковые окна цена": "WINDOW_FINISHING_SERVICE",
        "установка откосов на пластиковые окна": "WINDOW_FINISHING_SERVICE",
        "установка откосов на пластиковые окна своими руками": "WINDOW_FINISHING_DIY",
        "установка отливов на пластиковые окна": "WINDOW_FINISHING_SERVICE",
        "установка отлива на пластиковое окно своими руками": "WINDOW_FINISHING_DIY",
        "установка пластиковых окон своими руками": "WINDOW_INSTALLATION_DIY",
        "установка пластиковых окон самостоятельно": "WINDOW_INSTALLATION_DIY",
        "установка жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_INSTALLATION",
        "установка рулонных штор на пластиковые окна": "OUTSIDE_CURTAINS_INSTALLATION",
        "установка москитной сетки на пластиковое окно": "MOSQUITO_NET_INSTALLATION_SERVICE",
        "установка сетки антикошка на пластиковые окна": "MOSQUITO_NET_INSTALLATION_SERVICE",
        # V24 intentional taxonomy split.
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

    unresolved = {
        "веранда без остекления",
        "подоконник после установки пластикового окна",
    }
    for phrase in unresolved:
        got = b.classify_semantic(phrase)
        assert got[0] is None, (phrase, got)


if __name__ == "__main__":
    self_test()
    runner.main()
