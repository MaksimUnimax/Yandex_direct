#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V22 as v22

_v22_classifier = b.classify_semantic
base = v22.base

b.TASKS.update({
    "OUTSIDE_CURTAINS_INSTALLATION": ("Установка штор/жалюзи на окна", "OUTSIDE_CORE_SERVICE", "OUTSIDE"),
    "MOSQUITO_NET_INSTALLATION_SERVICE": ("Установка москитных/защитных сеток на окна", "COMMERCIAL_SERVICE", "ADJACENT"),
})


def has(p: str, *parts: str) -> bool:
    return base.has(p, *parts)


def classify_v23(phrase: str):
    p = base.n(phrase)
    win = base.windowish(p)
    door = "двер" in p and has(p, "пластик", "пвх")
    install = has(p, "установ", "монтаж")
    diy = has(p, "своими руками", "самостоятель", "самому")

    # 'No glazing' negates the service itself. For a veranda the existing
    # OPEN_BALCONY_FINISHING task would invent a balcony-specific meaning, so keep
    # the phrase unresolved rather than forcing either service family.
    if "веранд" in p and "без остеклен" in p:
        return None, "Explicit veranda-without-glazing wording negates the glazing service; exact alternative task remains ambiguous", "LOW"

    # Door components are head products/components, not whole-door demand.
    if door and (
        re.search(r"^(?:детск\w*\s+|многозапорн\w*\s+)?зам(?:ок|ки|ка|ков)\b", p)
        or re.search(r"^(?:механизм|редуктор\w*|ригель\w*|ролик\w*|петл\w*|ручк\w*)\b", p)
        or re.search(r"\b(?:зам(?:ок|ки|ка|ков)|механизм|редуктор\w*|ригель\w*|ролик\w*|петл\w*|ручк\w*)\s+(?:для|на)\s+.*\bдвер", p)
    ) and not has(p, "ремонт", "замена", "заменить", "поменять", "установ", "монтаж"):
        return "WINDOW_HARDWARE", "Plastic-door component is the head object, not the complete door", "HIGH"

    # Explicit replacement of a component is a maintenance/service task. This
    # closes the 'поменять стеклопакет' gap without reintroducing the old whole-
    # window replacement substring bug.
    if (win or door) and has(p, "замена", "заменить", "поменять") and has(
        p, "фурнитур", "ручк", "уплотн", "стеклопак", "петл", "механизм", "замок", "редуктор", "ролик"
    ):
        return "WINDOW_REPAIR", "Explicit replacement of a window/door component is maintenance rather than whole-product replacement", "HIGH"

    # Accessory/finishing installation must be resolved before generic
    # action-headed window installation.
    if install and has(p, "жалюзи", "штор", "рулонн"):
        return "OUTSIDE_CURTAINS_INSTALLATION", "Installation targets blinds/curtains rather than the window itself", "HIGH"
    if install and has(p, "москит", "антикош", "сетка на", "сетки на", "сетку на"):
        return "MOSQUITO_NET_INSTALLATION_SERVICE", "Installation targets a mosquito/protection net rather than the window itself", "HIGH"
    if install and has(p, "оконной фурнитур", "оконную фурнитур", "фурнитуры на", "фурнитуру на"):
        return "WINDOW_REPAIR", "Installation targets window hardware/components rather than the window itself", "HIGH"
    if install and has(p, "откос", "отлив"):
        if diy:
            return "WINDOW_FINISHING_DIY", "DIY installation targets slopes/ebb finishing rather than the window itself", "HIGH"
        return "WINDOW_FINISHING_SERVICE", "Professional installation targets slopes/ebb finishing rather than the window itself", "HIGH"
    if install and "подокон" in p:
        if diy:
            return "WINDOW_FINISHING_DIY", "DIY installation targets the windowsill rather than the window itself", "HIGH"
        return "WINDOW_FINISHING_SERVICE", "Professional installation targets the windowsill rather than the window itself", "HIGH"

    # Explicit self-installation is procedural/DIY even when it starts with the
    # action word 'установка'.
    if win and install and diy:
        return "WINDOW_INSTALLATION_DIY", "Explicit self-installation wording outranks professional installation service routing", "HIGH"

    return _v22_classifier(phrase)


b.classify_semantic = classify_v23


def self_test() -> None:
    v22.self_test()
    expected = {
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
        "установка подоконника на пластиковые окна своими руками": "WINDOW_FINISHING_DIY",
        "установка жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_INSTALLATION",
        "установка рулонных штор на пластиковые окна": "OUTSIDE_CURTAINS_INSTALLATION",
        "установка москитной сетки на пластиковое окно": "MOSQUITO_NET_INSTALLATION_SERVICE",
        "установка сетки антикошка на пластиковые окна": "MOSQUITO_NET_INSTALLATION_SERVICE",
        "установка оконной фурнитуры": "WINDOW_REPAIR",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)

    got = b.classify_semantic("веранда без остекления")
    assert got[0] is None, got


if __name__ == "__main__":
    self_test()
    runner.main()
