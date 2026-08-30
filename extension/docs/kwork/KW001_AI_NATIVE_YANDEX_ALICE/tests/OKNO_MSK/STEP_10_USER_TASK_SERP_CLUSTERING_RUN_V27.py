#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V19 as v19
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V26 as v26

_current_classifier = b.classify_semantic


def classify_v27(phrase: str):
    return _current_classifier(phrase)


b.classify_semantic = classify_v27


def _assert_expected(expected: dict[str, str]) -> None:
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


def _assert_unresolved(phrases: set[str]) -> None:
    for phrase in phrases:
        got = b.classify_semantic(phrase)
        assert got[0] is None, (phrase, got)


def self_test() -> None:
    # V19 is the last historical regression suite that is fully compatible with
    # the current taxonomy. Run its complete inherited corpus against V27.
    v19.self_test()

    # V20 still-valid corrections. One historical V20 unresolved expectation —
    # 'ремонт балкона с остеклением' — was intentionally superseded in V26 and is
    # therefore tested later with its current expected task instead of rewritten
    # in history.
    _assert_expected({
        "заглушки для алюминиевых окон": "WINDOW_HARDWARE",
        "замки для алюминиевых окон": "WINDOW_HARDWARE",
        "клапана на алюминиевые окна": "WINDOW_HARDWARE",
        "направляющие для алюминиевых окон": "WINDOW_HARDWARE",
        "редуктор для алюминиевой окон": "WINDOW_HARDWARE",
        "ролики для алюминиевых окон": "WINDOW_HARDWARE",
        "механизм пластикового окна": "WINDOW_HARDWARE",
        "подоконник для пластиковых окон": "WINDOW_ACCESSORIES",
        "стеклопакеты для пластиковых окон": "WINDOW_HARDWARE",
        "теплый подставочный профиль для окон rehau": "WINDOW_HARDWARE",
        "установка пластиковой двери": "PVC_DOOR_INSTALLATION_SERVICE",
        "установка готовых пластиковых окон": "WINDOW_INSTALLATION",
        "изготовление и установка пластиковых окон": "WINDOW_INSTALLATION",
        "стоимость замены окна на пластиковые цена": "WINDOW_REPLACEMENT_SERVICE",
        "замена оконной фурнитуры": "WINDOW_REPAIR",
        "не открывается пластиковое окно": "WINDOW_REPAIR_DIY",
        "не закрывается пластиковая дверь": "PVC_DOOR_REPAIR_DIY",
        "открывание алюминиевых окон": "WINDOW_OPERATION_DIY",
        "проветривание алюминиевые окна": "WINDOW_OPERATION_DIY",
        "какое окно алюминиевое": "WINDOW_SELECTION_INFO",
        "какие окна rehau": "REHAU_SELECTION_INFO",
        "рейтинг алюминиевых окон": "WINDOW_REVIEWS_INFO",
        "панорамные окна для частного дома размеры": "WINDOW_DIMENSIONS_INFO",
        "стандартные размеры панорамных окон для частного дома": "WINDOW_DIMENSIONS_INFO",
        "панорамные окна в частном доме фото": "DESIGN_INSPIRATION",
        "французские окна на балкон фото": "DESIGN_INSPIRATION",
        "какое остекление балкона лучше выбрать": "GLAZING_SELECTION_INFO",
        "остекление балконов самому": "GLAZING_DIY_INFO",
        "разрешение на остекление балкона": "GLAZING_PERMISSION_INFO",
        "балкон без остекления": "OPEN_BALCONY_FINISHING",
        "демонтаж остекления балкона": "WINDOW_DEMOLITION",
        "профиль для остекления балконов": "WINDOW_HARDWARE",
        "поликарбонат для остекления веранды": "WINDOW_ACCESSORIES",
        "толщина монолитного поликарбоната для остекления веранды": "WINDOW_ACCESSORY_SELECTION_INFO",
        "кондиционер на балконе с остеклением": "OUTSIDE_HVAC",
        "запчасти для ремонта пластиковых окон": "WINDOW_HARDWARE",
        "клей для ремонта пластиковых окон": "WINDOW_ACCESSORIES",
        "ремонт пластиковых окон самому": "WINDOW_REPAIR_DIY",
        "ремонт откосов пластиковых окон": "WINDOW_FINISHING_SERVICE",
        "ремонт подоконников пластиковых окон": "WINDOWSILL_REPAIR",
        "французские занавески на окна": "OUTSIDE_CURTAINS",
        "французские вертикальные задвижки для окон": "WINDOW_HARDWARE",
        "французские окна название": "WINDOW_DEFINITION_INFO",
        "французское окно оформление": "DESIGN_INSPIRATION",
        "устанавливаем французские окна": "WINDOW_INSTALLATION",
        "французские окна вместо балконного блока": "WINDOW_REPLACEMENT_SERVICE",
    })
    _assert_unresolved({
        "пластиковые окна монтаж ремонт",
        "пластиковые окна после ремонта",
        "покраска алюминиевых окон",
        "сборка алюминиевых окон",
    })

    # V21–V22 specificity regressions.
    _assert_expected({
        "чем отмыть пластиковые окна после ремонта": "WINDOW_CARE_INFO",
        "чем очистить пластиковые окна после ремонта": "WINDOW_CARE_INFO",
        "очистить пластиковые окна ремонта": "WINDOW_CARE_INFO",
        "толщина монолитного поликарбоната для остекления веранды": "WINDOW_ACCESSORY_SELECTION_INFO",
    })

    # V23 action-head/component corrections, with V24's intentional taxonomy
    # split for windowsill and window-hardware installation represented below.
    _assert_expected({
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
    })

    # V24 dedicated installation-service boundaries.
    _assert_expected({
        "установка деревянного подоконника на пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна цена": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконников под пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка оконной фурнитуры": "WINDOW_HARDWARE_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна своими руками": "WINDOW_FINISHING_DIY",
    })
    _assert_unresolved({"подоконник после установки пластикового окна"})

    # V26 current balcony renovation/glazing-repair boundaries and the explicit
    # no-glazing semantic negation that remains intentionally unresolved.
    _assert_expected({
        "ремонт балкона с остеклением": "BALCONY_RENOVATION_WITH_GLAZING_SERVICE",
        "ремонт остекление балконов москва": "BALCONY_GLAZING_REPAIR_SERVICE",
        "ремонт остекление балкона французские окна": "BALCONY_GLAZING_REPAIR_SERVICE",
    })
    _assert_unresolved({"веранда без остекления"})


if __name__ == "__main__":
    self_test()
    runner.main()
