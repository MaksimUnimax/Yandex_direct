#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Applies V5 -> V4 -> V3 corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V5  # noqa: F401,E402

b.TASKS.update({
    "GLAZING_DIY_INFO": ("Самостоятельное остекление", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_FINISHING_DIY": ("Самостоятельный монтаж откосов/отливов/подоконников", "INFORMATIONAL", "ADJACENT"),
})

_v5_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def doorish(p: str) -> bool:
    return "двер" in p and has(p, "пластик", "пвх")


def classify_v6(phrase: str):
    p = n(phrase)
    diy = has(p, "своими руками", "самостоятель", "пошаг", "как установить", "как монтировать")

    # Accessory/product object wins over the verb 'установка'. The task is blinds,
    # not professional installation of the window itself.
    if has(p, "штор", "жалюзи", "рулонн", "день ночь"):
        return "OUTSIDE_CURTAINS", "Curtain/blind task; installation wording modifies the accessory, not the window", "HIGH"
    if has(p, "сетк", "москит", "антикошка") and (windowish(p) or doorish(p)):
        if has(p, "как выбрать", "выбрать"):
            return "WINDOW_ACCESSORY_SELECTION_INFO", "Selection of mosquito/protection accessory", "HIGH"
        return "MOSQUITO_NETS", "Mosquito/protection accessory task for a window or plastic door", "HIGH"

    # Explicit DIY installation must be resolved before V4's professional-installation
    # rule and before the old broad 'своими руками' fallback.
    if diy and has(p, "установ", "монтаж") and windowish(p):
        if has(p, "откос", "отлив", "подокон"):
            return "WINDOW_FINISHING_DIY", "DIY installation of slopes/ebb/windowsill, not installation of the window itself", "HIGH"
        return "WINDOW_INSTALLATION_DIY", "Explicit DIY/procedural window installation task", "HIGH"

    # DIY glazing is distinct from repair and from a commercial glazing service.
    if diy and "остеклен" in p:
        return "GLAZING_DIY_INFO", "Explicit DIY glazing task", "HIGH"

    # Bare door DIY without an action is ambiguous; do not infer repair.
    if doorish(p) and has(p, "своими руками", "самостоятель") and not has(p, "ремонт", "регулир", "установ", "монтаж", "сделать", "изготов", "замен"):
        return None, "Plastic-door DIY wording lacks the action needed to identify the task", "LOW"

    # Bare window 'самостоятельно' without action is also insufficient.
    if windowish(p) and has(p, "самостоятель") and not has(p, "ремонт", "регулир", "установ", "монтаж", "сделать", "изготов", "замен", "остеклен"):
        return None, "Window + independently/by-yourself wording lacks an explicit action", "LOW"

    # Visual appearance is not selection. Supply-state wording is too different to
    # infer an appearance/selection cluster safely.
    if has(p, "как выглядит", "как выглядят") and windowish(p):
        if "поставк" in p:
            return None, "Supply-state query with 'как выглядят' is not a window-selection task", "LOW"
        return "DESIGN_INSPIRATION", "Explicit visual-appearance/inspiration task", "HIGH"

    # Convert/make an existing window is a fabrication/modification task.
    if has(p, "как из", "переделать", "переделка") and windowish(p):
        return "WINDOW_FABRICATION_DIY", "Explicit DIY conversion/modification of a window", "HIGH"

    # 'какой ремонт' is repair-oriented but does not identify service vs DIY vs type.
    if windowish(p) and has(p, "какой ремонт", "какая регулировка"):
        return None, "Repair-oriented question is too vague to distinguish service, information or repair type", "LOW"

    # Seal/rubber replacement is maintenance/service; accept Russian forms such as
    # 'резинок', which do not contain the exact stem 'резинк'.
    if windowish(p) and has(p, "резин", "уплотн") and has(p, "замена", "заменить", "поменять"):
        return "WINDOW_REPAIR", "Explicit seal/rubber replacement maintenance task", "HIGH"

    # Cleaning verbs without 'как/чем' are still care/cleaning, not repair service.
    if windowish(p) and has(p, "очистить", "отмыть", "помыть"):
        return "WINDOW_CARE_INFO", "Explicit window cleaning/care action", "HIGH"

    # Repair of a component is a repair task; component nouns must not swallow it.
    if windowish(p) and "ремонт" in p and has(p, "петл", "фурнитур", "ручк", "замк", "механизм"):
        if has(p, "своими руками", "самостоятель", "как ", "видео", "инструк"):
            return "WINDOW_REPAIR_DIY", "Explicit DIY repair of a window component", "HIGH"
        return "WINDOW_REPAIR", "Explicit repair of a window component", "HIGH"

    return _v5_classifier(phrase)


b.classify_semantic = classify_v6

if __name__ == "__main__":
    runner.main()
