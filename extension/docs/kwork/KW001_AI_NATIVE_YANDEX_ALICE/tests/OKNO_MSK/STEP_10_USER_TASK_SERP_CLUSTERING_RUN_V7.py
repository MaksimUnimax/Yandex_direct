#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Applies V6 -> V5 -> V4 -> V3 corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V6  # noqa: F401,E402

b.TASKS.update({
    "WINDOW_REPLACEMENT_SERVICE": ("Замена окна/окон целиком", "COMMERCIAL_SERVICE", "FIT"),
    "PVC_DOOR_REPLACEMENT_SERVICE": ("Замена пластиковых дверей", "COMMERCIAL_SERVICE", "ADJACENT"),
    "WINDOW_FINISHING_SERVICE": ("Монтаж/замена откосов и отливов", "COMMERCIAL_SERVICE", "ADJACENT"),
    "WINDOW_FINISHING_INFO": ("Откосы/отливы после установки окна", "INFORMATIONAL", "ADJACENT"),
})
# Hardware cluster also covers compatible PVC-door hardware/components.
b.TASKS["WINDOW_HARDWARE"] = ("Фурнитура и комплектующие для окон/ПВХ-дверей", "ECOMMERCE_ACCESSORY", "ADJACENT")

_v6_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def doorish(p: str) -> bool:
    return "двер" in p and has(p, "пластик", "пвх")


def classify_v7(phrase: str):
    p = n(phrase)

    # Supply-state wording: 'как сейчас выглядят поставки...' is not visual selection.
    if "поставк" in p and "выгляд" in p and has(p, "rehau", "рехау", "окн", "окон"):
        return None, "Supply-state query is not a window-selection task and needs separate evidence", "LOW"

    # Hardware/accessory overlays such as aluminium/PVC covers belong to components.
    if has(p, "накладк") and (windowish(p) or doorish(p)):
        return "WINDOW_HARDWARE", "Explicit overlay/cover component for window or PVC door", "HIGH"

    # Slopes/ebb are finishing around the window, not installation of the window itself.
    if has(p, "откос", "отлив") and windowish(p):
        if has(p, "своими руками", "самостоятель", "пошаг", "как установить", "как сделать"):
            return "WINDOW_FINISHING_DIY", "DIY slopes/ebb finishing task", "HIGH"
        if has(p, "установ", "монтаж", "замена", "заменить", "поменять", "цена", "стоимость"):
            return "WINDOW_FINISHING_SERVICE", "Commercial slopes/ebb installation or replacement task", "HIGH"
        return "WINDOW_FINISHING_INFO", "Slopes/ebb context around installed windows without a clear service action", "MEDIUM"

    # Component replacement/repair before whole-window replacement.
    if windowish(p) and has(p, "ручк", "уплотн", "резин", "проклад", "стеклопак", "петл", "фурнитур") and has(p, "замена", "заменить", "поменять"):
        return "WINDOW_REPAIR", "Replacement of a window component is maintenance/repair, not whole-window purchase", "HIGH"
    if "подокон" in p and has(p, "замена", "заменить", "поменять"):
        return "WINDOWSILL_REPAIR", "Explicit windowsill replacement/repair task", "HIGH"

    # Full plastic-door replacement is a separate service task.
    if doorish(p) and has(p, "замена", "заменить", "поменять"):
        return "PVC_DOOR_REPLACEMENT_SERVICE", "Explicit replacement of a plastic door", "HIGH"

    # Full-window replacement: distinguish from replacement of components above.
    replacement = has(p, "замена окна", "замена окон", "замена пластиковых окон", "замена алюминиевых окон", "замена окон rehau", "заменить окно", "заменить окна", "заменить пластиковые окна", "заменить алюминиевые окна", "поменять окно", "поменять окна")
    if replacement and windowish(p):
        # Weird 'replace balcony with plastic windows' does not identify a normal whole-window replacement task.
        if "замена балкона" in p:
            return None, "Phrase about replacing a balcony with plastic windows is materially ambiguous", "LOW"
        return "WINDOW_REPLACEMENT_SERVICE", "Explicit replacement of a whole window/window set", "HIGH"

    return _v6_classifier(phrase)


b.classify_semantic = classify_v7

if __name__ == "__main__":
    runner.main()
