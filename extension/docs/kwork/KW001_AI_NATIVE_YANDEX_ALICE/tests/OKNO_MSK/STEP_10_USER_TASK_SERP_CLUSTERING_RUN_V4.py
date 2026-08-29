#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Import applies V3's validated class-level corrections to b.classify_semantic.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V3  # noqa: F401,E402

b.TASKS.update({
    "WINDOW_REPAIR_DIY": ("Самостоятельная регулировка/ремонт окон", "INFORMATIONAL_SERVICE", "ADJACENT"),
    "WINDOW_DIMENSIONS_INFO": ("Размеры/габариты окон", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_CARE_INFO": ("Уход и очистка окон", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_REPAIR_MATERIALS": ("Материалы/средства для ремонта окон", "ECOMMERCE_ACCESSORY", "ADJACENT"),
})

_v3_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def doorish(p: str) -> bool:
    return "двер" in p and has(p, "пластик", "пвх")


def classify_v4(phrase: str):
    p = n(phrase)

    # A house/project task remains real-estate/inspiration even when phrased as a
    # definition question; do not let generic 'как называется' steal it.
    if "панорам" in p and has(
        p,
        "как называется дом", "дом с панорам", "дома с панорам", "барнхаус с панорам",
        "дача с панорам", "апартамент", "гостиная с панорам", "баня с панорам",
        "бассейн с панорам", "панорамные окна лес", "проект дома",
    ):
        return "OUTSIDE_REAL_ESTATE", "Explicit house/real-estate/inspiration task with panoramic-window context", "HIGH"

    # Window care/cleaning is not a repair-service lead simply because the phrase
    # says 'после ремонта'.
    if windowish(p) and has(p, "чем отмыть", "как отмыть", "чем очистить", "как очистить", "мыть окна", "помыть окна", "очистка окон"):
        return "WINDOW_CARE_INFO", "Explicit cleaning/care task; 'после ремонта' does not make it window-repair service", "HIGH"

    # Repair consumables/materials are a product/accessory task, not service repair.
    if windowish(p) and has(p, "жидкий пластик", "ремонтный комплект", "ремкомплект", "средство для ремонта"):
        return "WINDOW_REPAIR_MATERIALS", "Explicit repair material/consumable task", "HIGH"

    # Accessories must be resolved before geography. Moscow modifies the accessory
    # request; it does not turn it into a generic window-purchase task.
    if windowish(p) and has(p, "сетк", "москит", "антикошка"):
        if has(p, "как выбрать", "выбрать"):
            return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit selection of mosquito/protection accessory", "HIGH"
        return "MOSQUITO_NETS", "Explicit mosquito/protection accessory task; geography is only a modifier", "HIGH"

    if windowish(p) and has(p, "шпрос", "резинк", "уплотнител", "фурнитур", "штапик", "ручк", "микролифт", "ограничител", "анкер", "гребенк"):
        # Replacement/repair wording is service/maintenance rather than buying the whole window.
        if has(p, "замена ", "заменить", "поменять") and has(p, "резинк", "уплотнител"):
            return "WINDOW_REPAIR", "Explicit seal/rubber replacement maintenance task; geography is only a modifier", "HIGH"
        if has(p, "как выбрать", "выбрать"):
            return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit hardware/accessory selection task", "HIGH"
        if has(p, "отзыв"):
            return "WINDOW_REVIEWS_INFO", "Explicit hardware/accessory review task", "HIGH"
        if has(p, "лучше", "сравн", " или ", "отлич"):
            return "WINDOW_COMPARISON_INFO", "Explicit hardware/accessory comparison task", "HIGH"
        return "WINDOW_HARDWARE", "Explicit window component/hardware task; geography is only a modifier", "HIGH"

    # Aluminium/PVC profile wording can describe the profile/component itself.
    if windowish(p) and "профил" in p and has(p, "алюмини") and not has(p, "какой профиль", "выбрать профиль"):
        return "WINDOW_HARDWARE", "Explicit aluminium window-profile/component task", "MEDIUM"

    # DIY/diagnostic repair before the generic selection rule. The previous method
    # incorrectly put 'как отрегулировать пластиковое окно' into 'Как выбрать окна'.
    diy_repair = has(
        p,
        "как отрегулировать", "как регулировать", "отрегулировать", "своими руками",
        "видео ремонта", "ремонт своими руками", "самостоятельно отрегулировать",
    )
    if diy_repair and (windowish(p) or doorish(p)):
        if doorish(p) and not windowish(p):
            return "PVC_DOOR_REPAIR_DIY", "Explicit DIY/diagnostic plastic-door adjustment/repair task", "HIGH"
        return "WINDOW_REPAIR_DIY", "Explicit DIY/diagnostic window adjustment/repair task", "HIGH"

    # Mixed windows+doors repair with no DIY cue is a service repair task, not a
    # door-only informational cluster.
    if has(p, "ремонт", "регулиров") and windowish(p) and "двер" in p and not diy_repair:
        return "WINDOW_REPAIR", "Explicit commercial/mixed repair-regulation task for windows and doors", "MEDIUM"

    # General window dimensions are informational unless explicit buying/service
    # language makes a different task clear.
    if windowish(p) and has(p, "ширина", "высота", "размер", "габарит"):
        if not has(p, "купить", "заказать", "цена", "цены", "стоимость", "установ", "монтаж"):
            return "WINDOW_DIMENSIONS_INFO", "Explicit dimensions/size information task", "HIGH"

    # Measurement + installation remains its own informational boundary (directly
    # confirmed for one Step-09 query).
    if windowish(p) and has(p, "замер", "размер") and has(p, "установ", "монтаж"):
        return "WINDOW_MEASUREMENT_INFO", "Measurement/dimension task connected with installation", "HIGH"

    # Professional installation before generic geo/product classification.
    if windowish(p) and has(p, "установ", "монтаж") and not has(p, "как установить", "своими руками", "пошаг", "инструкция", "видео"):
        return "WINDOW_INSTALLATION", "Explicit professional installation task; geography is only a modifier", "HIGH"

    # Street/address-like expressions are navigational/entity evidence even without
    # the literal word 'адрес'.
    address_like = bool(re.search(r"\b(ул\.?|улиц|проезд|проспект|шоссе|переулок)\b", p)) or bool(re.search(r"\bд\.?\s*\d+\b", p))
    if address_like and has(p, "rehau", "рехау") and windowish(p):
        return "REHAU_NAVIGATION", "Address/street modifier indicates entity/navigation task for Rehau", "MEDIUM"
    if address_like and windowish(p):
        return "WINDOW_SERVICE_NAVIGATION", "Address/street modifier indicates local/entity navigation task", "MEDIUM"

    return _v3_classifier(phrase)


b.classify_semantic = classify_v4

if __name__ == "__main__":
    runner.main()
