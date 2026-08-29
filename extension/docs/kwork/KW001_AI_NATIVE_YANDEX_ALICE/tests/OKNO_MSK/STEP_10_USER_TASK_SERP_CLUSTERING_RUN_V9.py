#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Applies V8 -> V7 -> V6 -> V5 -> V4 -> V3 corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V8  # noqa: F401,E402

b.TASKS.update({
    "PVC_DOOR_DIMENSIONS_INFO": ("Размеры/габариты пластиковых дверей", "INFORMATIONAL", "ADJACENT"),
    "PVC_DOOR_OPERATION_INFO": ("Как открыть/снять/эксплуатировать пластиковую дверь", "INFORMATIONAL", "ADJACENT"),
    "PVC_DOOR_DEFINITION_INFO": ("Что это / как называется пластиковая дверь", "INFORMATIONAL", "ADJACENT"),
    "PVC_DOOR_SELECTION_INFO": ("Как выбрать пластиковую дверь", "INFORMATIONAL", "ADJACENT"),
    "PVC_DOOR_INSTALLATION_DIY": ("Самостоятельная/пошаговая установка пластиковой двери", "INFORMATIONAL", "ADJACENT"),
    "PRIVATE_HOUSE_WINDOWS_COMMERCIAL": ("Окна для частного дома: покупка/цена", "COMMERCIAL_PRODUCT", "FIT"),
    "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO": ("Выбор окон для частного дома", "INFORMATIONAL", "ADJACENT"),
    "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO": ("Требования и специальные условия к окнам частного дома", "INFORMATIONAL", "ADJACENT"),
    "PANORAMIC_WINDOWS_INFO": ("Виды/особенности/выбор панорамных окон", "INFORMATIONAL", "ADJACENT"),
    "GLAZING_SELECTION_INFO": ("Выбор и сравнение вариантов остекления", "INFORMATIONAL_COMPARISON", "ADJACENT"),
    "BALCONY_GLAZING_WOOD": ("Остекление балкона деревянными рамами", "COMMERCIAL_SERVICE", "ADJACENT"),
    "WINDOW_DOOR_REPAIR_SERVICE": ("Ремонт/регулировка окон и пластиковых дверей", "COMMERCIAL_SERVICE", "ADJACENT"),
    "PORCH_GLAZING": ("Остекление крыльца", "COMMERCIAL_SERVICE", "ADJACENT"),
})

_v8_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def doorish(p: str) -> bool:
    return "двер" in p and has(p, "пластик", "пвх")


def classify_v9(phrase: str):
    p = n(phrase)
    win = windowish(p)
    door = doorish(p)

    # Exact direct-SERP anchors whose wording alone is weak, but whose exact Step-09
    # observation supplies a high-confidence job-specific task boundary. Evidence is
    # consumed only for this exact phrase by the runner; it is never transferred.
    if p == "пластиковые двери видео":
        return "PVC_DOOR_INSTALLATION_DIY", "Exact Step-09 evidence identifies a PVC-door installation-video/procedural task", "HIGH"
    if p == "крыльцо для частного дома окна":
        return "PORCH_GLAZING", "Exact Step-09 evidence identifies porch glazing as a commercial service", "HIGH"

    # Mixed whole-window repair + replacement wording contains two material service
    # tasks and must not be forced into replacement only.
    if win and has(p, "ремонт") and has(p, "замена пластиковых окон", "заменить пластиковые окна", "поменять окна", "замена окон"):
        return None, "Phrase explicitly mixes repair and whole-window replacement; keep the boundary visible", "LOW"

    # Mixed windows+doors repair is a combined service task, not a door-only task.
    if win and door and has(p, "ремонт", "регулир", "провис", "почин"):
        return "WINDOW_DOOR_REPAIR_SERVICE", "Explicit combined repair/adjustment service for windows and PVC doors", "HIGH"

    # 'Демонтаж' contains the substring 'монтаж'; resolve it before installation rules.
    if "демонтаж" in p and win:
        return "WINDOW_DEMOLITION", "Explicit demolition/removal of windows or glazing; not installation", "HIGH"

    # Wooden-frame balcony glazing is a service job. Material wording must not turn
    # it into a wooden-window product cluster.
    if "остеклен" in p and has(p, "балкон", "лоджи") and has(p, "деревян", "деревянными рам", "деревянных рам"):
        return "BALCONY_GLAZING_WOOD", "Explicit balcony/loggia glazing service using wooden frames", "HIGH"

    # Slopes/ebb repair is a finishing service unless the wording is explicitly DIY.
    if win and has(p, "откос", "отлив") and has(p, "ремонт", "почин", "восстанов"):
        if has(p, "своими руками", "самостоятель", "как ремонт", "как восстанов", "видео", "инструкция"):
            return "WINDOW_FINISHING_DIY", "DIY repair/restoration of slopes or ebb", "HIGH"
        return "WINDOW_FINISHING_SERVICE", "Commercial repair/restoration task for slopes or ebb", "HIGH"

    # PVC-door information must be resolved before the generic door-product rule.
    if door and has(p, "ширина", "высота", "размер", "габарит") and not has(p, "купить", "заказать", "цена", "стоимость"):
        return "PVC_DOOR_DIMENSIONS_INFO", "Explicit plastic-door dimensions/size information task", "HIGH"
    if door and has(p, "как называется", "что такое", "как зовется"):
        return "PVC_DOOR_DEFINITION_INFO", "Explicit definition/naming question about a plastic door", "HIGH"
    if door and has(p, "как открыть", "как закрыть", "как снять", "как вставить", "как разобрать", "снять с петель", "открыть пластиковую дверь", "закрыть пластиковую дверь"):
        return "PVC_DOOR_OPERATION_INFO", "Explicit plastic-door operation/removal procedure", "HIGH"
    if door and has(p, "как установить", "как монтировать", "пошаг", "своими руками", "видео установки", "инструкция установки"):
        return "PVC_DOOR_INSTALLATION_DIY", "Explicit procedural/DIY plastic-door installation task", "HIGH"
    if door and has(p, "как выбрать", "какую пластиковую дверь", "какая пластиковая дверь", "выбрать пластиковую дверь"):
        return "PVC_DOOR_SELECTION_INFO", "Explicit plastic-door selection task", "HIGH"
    # A malformed/object-collision phrase must not become a confident PVC-door sale.
    if door and has(p, "щит пластиковый", "прозрачный щит", "прозрачная дверь щит") and not has(p, "купить", "заказать", "цена"):
        return None, "Plastic-shield/door wording is materially ambiguous; do not force a door-product task", "LOW"

    # Panoramic/French contextual semantics before generic private-house/product rules.
    panoramic = "панорам" in p and win
    french = "француз" in p and win
    if panoramic or french:
        if has(p, "фото", "дизайн", "дизайны", "красив", "интерьер"):
            return "DESIGN_INSPIRATION", "Explicit design/photo/inspiration task around panoramic/French windows", "HIGH"
        context_nouns = (
            "дом ", "дома ", "домик", "квартира", "комната", "кухня", "зал ", "лофт",
            "беседк", "бытовк", "барбекю", "баня", "гостиная", "апартамент", "веранда",
            "терраса", "бассейн", "лесу", "в лес", "проект дома",
        )
        commercial = has(p, "купить", "заказать", "цена", "цены", "стоимость", "производител", "монтаж", "установка")
        if has(p, *context_nouns) and not commercial:
            return "OUTSIDE_REAL_ESTATE", "Building/interior context is an architecture/real-estate/inspiration task, not a window-purchase claim", "HIGH"
        if has(p, "виды", "варианты", "плюсы", "минусы", "лучшие", "лучше", "какие", "как выбрать", "сравн", "почему", "особенности"):
            return "PANORAMIC_WINDOWS_INFO", "Explicit informational/selection task about panoramic/French windows", "HIGH"
        if has(p, "закрой ", "открой ", "как закрыть", "как открыть", "как снять"):
            return "WINDOW_OPERATION_DIY", "Explicit operation task for a panoramic/French window", "HIGH"
        if re.search(r"\b\d+(?:[.,]\d+)?\s*(?:м|метр)", p):
            return "WINDOW_DIMENSIONS_INFO", "Explicit panoramic-window dimensional specification", "MEDIUM"
        if has(p, "готов", "больш", "высок", "маленьк", "широк", "узк"):
            return "PANORAMIC_WINDOWS_COMMERCIAL", "Explicit panoramic-window product variant/specification", "MEDIUM"

    # Informational comparison/selection of glazing should not stay unresolved merely
    # because the phrase says 'остекление' instead of 'окна'.
    if "остеклен" in p and has(p, "плюсы", "минусы", "сравн", "что лучше", "какое лучше", "виды", "варианты", "как выбрать", "выбрать остекление"):
        return "GLAZING_SELECTION_INFO", "Explicit comparison/selection task for glazing variants", "HIGH"

    # Private-house windows have a clear task family even without a material token.
    # Informational selection/requirements are separated from purchase/price demand.
    private_house = win and has(p, "частного дома", "частный дом", "в частном доме", "для дома")
    if private_house:
        if has(p, "требован", "норм", "вентиляц", "котельн") and not has(p, "купить", "заказать", "цена", "стоимость"):
            return "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO", "Explicit requirements/special-room information task for a private-house window", "HIGH"
        if has(p, "варианты", "виды", "какие окна", "какое окно", "лучшие окна", "лучшее окно", "образцы", "как выбрать", "выбрать"):
            return "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO", "Explicit private-house window selection task", "HIGH"
        return "PRIVATE_HOUSE_WINDOWS_COMMERCIAL", "Explicit window product/use-case demand for a private house", "MEDIUM"

    # Generic window 'types/variants' are informational, not an unresolved purchase.
    if win and has(p, "виды окон", "виды окна", "варианты окон", "варианты окна"):
        return "WINDOW_TECH_INFO", "Explicit window-types/variants information task", "HIGH"

    return _v8_classifier(phrase)


b.classify_semantic = classify_v9


def self_test() -> None:
    expected = {
        "ширина пластиковой двери": "PVC_DOOR_DIMENSIONS_INFO",
        "как открыть пластиковую дверь": "PVC_DOOR_OPERATION_INFO",
        "как называется пластиковая дверь": "PVC_DOOR_DEFINITION_INFO",
        "как установить пластиковую дверь": "PVC_DOOR_INSTALLATION_DIY",
        "пластиковые двери видео": "PVC_DOOR_INSTALLATION_DIY",
        "демонтаж остекления балкона": "WINDOW_DEMOLITION",
        "остекление балконов деревянными рамами": "BALCONY_GLAZING_WOOD",
        "ремонт откосов пластиковых окон": "WINDOW_FINISHING_SERVICE",
        "ремонт регулировка пластиковых окон и дверей": "WINDOW_DOOR_REPAIR_SERVICE",
        "крыльцо для частного дома окна": "PORCH_GLAZING",
        "окна для частного дома купить": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "окна для частного дома цена": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "окна пвх для частного дома": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "какие окна для частного дома": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "лучшие окна для частного дома": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "окно для газовой котельной частного дома требования": "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO",
        "виды панорамных окон": "PANORAMIC_WINDOWS_INFO",
        "дизайн кухни с панорамными окнами": "DESIGN_INSPIRATION",
        "дом в лесу с панорамными окнами": "OUTSIDE_REAL_ESTATE",
        "безрамное остекление веранды плюсы и минусы": "GLAZING_SELECTION_INFO",
        "замена ручек на пластиковых окнах цена": "WINDOW_REPAIR",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)

    mixed = b.classify_semantic("ремонт и замена пластиковых окон")
    assert mixed[0] is None, mixed

    ambiguous = b.classify_semantic("замена балкона на пластиковые окна цена")
    assert ambiguous[0] is None, ambiguous


if __name__ == "__main__":
    self_test()
    runner.main()
