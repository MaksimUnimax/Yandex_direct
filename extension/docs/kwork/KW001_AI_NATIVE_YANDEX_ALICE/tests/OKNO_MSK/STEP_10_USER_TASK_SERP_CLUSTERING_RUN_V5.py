#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
# Import applies all V4 corrections.
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V4  # noqa: F401,E402

b.TASKS.update({
    "WINDOW_FABRICATION_DIY": ("Самостоятельное изготовление/переделка окна", "INFORMATIONAL", "ADJACENT"),
    "PVC_DOOR_REPAIR_SERVICE": ("Регулировка/ремонт пластиковых дверей как услуга", "COMMERCIAL_SERVICE", "ADJACENT"),
})
# Finance can include product purchase and associated window work; keep one user-goal
# family at Step 10 without deciding page ownership.
b.TASKS["WINDOW_FINANCE"] = ("Окна/оконные работы в рассрочку или кредит", "COMMERCIAL_FINANCE", "FIT")

_v4_classifier = b.classify_semantic


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен")


def doorish(p: str) -> bool:
    return "двер" in p and has(p, "пластик", "пвх")


def classify_v5(phrase: str):
    p = n(phrase)

    # Any naming question about a HOUSE with panoramic windows is a house/architecture
    # task, independent of word order.
    if "панорам" in p and "дом" in p and has(p, "как называется", "что за дом", "тип дома", "вид дома"):
        return "OUTSIDE_REAL_ESTATE", "Naming/classifying a house with panoramic windows is an architecture/real-estate task", "HIGH"

    # Mixed window-material wording is not safe to collapse unless it is the clear
    # 'PVC windows in a wooden house' use case already handled by V4.
    if windowish(p) and "пластиков" in p and "деревянн" in p and not has(p, "в деревянном доме", "деревянный дом", "деревянного дома"):
        return None, "Mixed plastic/wood window wording does not prove one material/product task", "LOW"

    # Explicit manufacture/make-it-yourself wording is not a buying-selection query.
    if windowish(p) and has(p, "как сделать", "как изготовить", "изготовить своими руками", "сделать своими руками"):
        return "WINDOW_FABRICATION_DIY", "Explicit DIY window fabrication/modification task", "HIGH"

    # Bare 'windows + своими руками' is ambiguous: it could mean manufacture,
    # installation, repair, finishing, etc. Do not force it into repair.
    if windowish(p) and "своими руками" in p and not has(
        p,
        "ремонт", "регулир", "установ", "монтаж", "сделать", "изготов", "замен", "утепл", "остеклен",
    ):
        return None, "Bare 'windows + своими руками' lacks the action needed to identify the user task", "LOW"

    # DIY window repair requires a repair/adjustment action; 'своими руками' alone
    # is no longer sufficient.
    if windowish(p) and has(p, "ремонт", "регулир", "провис", "почин") and has(
        p,
        "как ", "своими руками", "самостоятель", "видео", "инструкция",
    ):
        return "WINDOW_REPAIR_DIY", "Explicit DIY/diagnostic window repair or adjustment task", "HIGH"

    # Door repair: separate informational DIY from a bare service demand.
    if doorish(p) and has(p, "ремонт", "регулир", "провис", "почин"):
        if has(p, "как ", "своими руками", "самостоятель", "видео", "инструкция"):
            return "PVC_DOOR_REPAIR_DIY", "Explicit DIY/diagnostic plastic-door repair/adjustment task", "HIGH"
        return "PVC_DOOR_REPAIR_SERVICE", "Bare plastic-door repair/adjustment wording is a service task, not automatically DIY", "MEDIUM"

    return _v4_classifier(phrase)


b.classify_semantic = classify_v5

if __name__ == "__main__":
    runner.main()
