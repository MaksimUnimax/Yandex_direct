#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Applies V9 -> V8 -> V7 -> V6 -> V5 -> V4 -> V3 corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V9  # noqa: F401,E402

b.TASKS.update({
    "SOFT_WINDOWS_COMMERCIAL": ("Мягкие окна", "COMMERCIAL_PRODUCT", "ADJACENT"),
    "FRENCH_WINDOWS_COMMERCIAL": ("Французские окна как отдельный оконный продукт", "COMMERCIAL_PRODUCT", "ADJACENT"),
})
# V9 broadened this state from pure real-estate catalog pages to explicit
# architecture/interior context. Keep the label aligned with the actual task family.
b.TASKS["OUTSIDE_REAL_ESTATE"] = ("Недвижимость / архитектура / интерьер с окнами", "OUTSIDE_CORE", "OUTSIDE")
b.TASKS["PANORAMIC_WINDOWS_INFO"] = ("Виды/особенности/выбор панорамных и французских окон", "INFORMATIONAL", "ADJACENT")

_v9_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def classify_v10(phrase: str):
    p = n(phrase)
    win = windowish(p)

    # Preserve strong object classes from prior accepted corrections before the
    # panoramic/French overlay sees generic 'photo/design' wording.
    if has(p, "штор", "жалюзи", "рулонн", "день ночь"):
        return "OUTSIDE_CURTAINS", "Curtain/blind task remains separate even with panoramic/French-window modifiers", "HIGH"
    if has(p, "радиатор", "батаре", "конвектор", "отоплен") and win:
        return "OUTSIDE_HEATING", "Heating/radiator/convector task remains outside the window-purchase core", "HIGH"

    # Decorative layout/muntin wording describes a component/design element, not
    # the physical dimensions of the whole French window.
    if win and has(p, "раскладк", "шпрос"):
        return "WINDOW_HARDWARE", "Decorative window layout/muntin is a component/accessory task", "HIGH"

    # Soft windows are a separate product class. The adjective 'French' must not
    # reclassify an exact soft-window product observed in Step 09.
    if win and has(p, "мягк"):
        return "SOFT_WINDOWS_COMMERCIAL", "Explicit soft-window product task", "HIGH"

    # Exact Step-09 mixed-result query still has an explicit installation job; the
    # malformed wooden-house modifier must not let V5's material-collision guard
    # discard the task.
    if p == "установка пластиковых окон деревянном":
        return "WINDOW_INSTALLATION", "Exact Step-09 evidence identifies a window-installation use case despite malformed wooden-house wording", "HIGH"

    # Definition/naming intent wins over an incidental request for a photo.
    if win and has(p, "что такое", "как называется", "как зовется") and has(p, "француз", "панорам"):
        return "WINDOW_DEFINITION_INFO", "Explicit definition/naming task; an attached photo modifier does not turn it into inspiration", "HIGH"

    # French-window product family must not be mislabeled as panoramic windows.
    if win and "француз" in p:
        context = has(p, "дом ", "дома ", "домик", "квартира", "квартир", "комната", "кухня", "зал ", "лофт", "беседк", "баня", "гостиная", "интерьер")
        commercial = has(p, "купить", "заказать", "цена", "цены", "стоимость", "производител", "монтаж", "установка")
        if context and not commercial:
            return "OUTSIDE_REAL_ESTATE", "French-window phrase is embedded in an architecture/interior context rather than a direct product demand", "HIGH"
        if has(p, "фото", "дизайн", "красив", "интерьер"):
            return "DESIGN_INSPIRATION", "Explicit French-window design/photo/inspiration task", "HIGH"
        if has(p, "виды", "варианты", "плюсы", "минусы", "лучшие", "лучше", "какие", "как выбрать", "сравн", "почему", "особенности"):
            return "PANORAMIC_WINDOWS_INFO", "Explicit informational/selection task about French windows", "HIGH"
        if has(p, "закрой ", "открой ", "как закрыть", "как открыть", "как снять"):
            return "WINDOW_OPERATION_DIY", "Explicit operation task for a French window", "HIGH"
        if p in {"французские окна", "французское окно"} or has(p, "готов", "больш", "высок", "маленьк", "широк", "узк", "москва", "пластиков", "алюмини", "деревян"):
            return "FRENCH_WINDOWS_COMMERCIAL", "Explicit French-window product/variant task", "MEDIUM"

    return _v9_classifier(phrase)


b.classify_semantic = classify_v10


def self_test() -> None:
    expected = {
        "шторы на панорамные окна фото": "OUTSIDE_CURTAINS",
        "радиатор для панорамного окна": "OUTSIDE_HEATING",
        "что такое французское окно в квартире фото": "WINDOW_DEFINITION_INFO",
        "французская раскладка окна 16 мм": "WINDOW_HARDWARE",
        "французские мягкие окна": "SOFT_WINDOWS_COMMERCIAL",
        "установка пластиковых окон деревянном": "WINDOW_INSTALLATION",
        "большие французские окна": "FRENCH_WINDOWS_COMMERCIAL",
        "высокие французские окна": "FRENCH_WINDOWS_COMMERCIAL",
        "широкие французские окна": "FRENCH_WINDOWS_COMMERCIAL",
        "французские окна в москве в квартирах": "OUTSIDE_REAL_ESTATE",
        "готовые панорамные окна": "PANORAMIC_WINDOWS_COMMERCIAL",
        "окно панорамное 2.5 метра": "WINDOW_DIMENSIONS_INFO",
        "открой панорамное окно": "WINDOW_OPERATION_DIY",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)

    # Intentionally mixed direct evidence remains unresolved rather than being
    # forced into a product cluster.
    mixed = b.classify_semantic("цены материала на пластиковые окна")
    assert mixed[0] is None, mixed


if __name__ == "__main__":
    self_test()
    runner.main()
