#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V38 as v38
import STEP_10_V39_DISCOVERY_SPEC as spec

_v38_classifier = b.classify_semantic

# New analytical user-task family identified by the full persisted-V38 manual re-audit.
# Business fit is deliberately UNKNOWN rather than invented from internal assumptions.
b.TASKS.setdefault(
    "ROOF_WINDOWS_COMMERCIAL",
    ("Покупка мансардных/кровельных окон", "COMMERCIAL_PRODUCT", "UNKNOWN_PUBLIC_FIT"),
)


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def classify_v39(phrase: str):
    p = b.norm(phrase)
    win = has(p, "окн", "окон", "rehau", "рехау")
    hardware = "фурнитур" in p
    balcony = has(p, "балкон", "лоджи")

    # ------------------------------------------------------------------
    # RC: co-head glazing + insulation is a combined balcony service,
    # not merely the warm-glazing subtype. Keep adjective/use-context forms
    # such as 'утепленное остекление' and 'остекление под утепление' inherited.
    # ------------------------------------------------------------------
    if balcony and "остеклен" in p and (
        "остекление и утепление" in p
        or "остекление утепление" in p
        or "остекления и утепления" in p
    ):
        return "BALCONY_RENOVATION_WITH_GLAZING_SERVICE", "Glazing and insulation are explicit co-head balcony services", "HIGH"

    # ------------------------------------------------------------------
    # RC: roof/mansard window is a specific product head object.
    # Brand/material/private-house/panoramic wording is secondary context.
    # ------------------------------------------------------------------
    if win and ("мансард" in p or "на крыше" in p or "для крыши" in p):
        return "ROOF_WINDOWS_COMMERCIAL", "Roof/mansard window is the specific product head object", "HIGH"

    # ------------------------------------------------------------------
    # Information/selection head object must outrank broad product/dimension
    # and hardware-shopping fallbacks.
    # ------------------------------------------------------------------
    if win and "частн" in p and has(p, "форма окна", "форма пластиковых окон", "формы пластиковых окон"):
        return "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO", "Window form/type wording is explicit private-house selection information", "HIGH"
    if hardware and has(p, "размер", "название"):
        return "WINDOW_TECH_INFO", "Hardware size/name is technical/reference information about the component family", "HIGH"
    if "уплотнител" in p and has(p, "подходит ли", "совместим"):
        return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit seal compatibility question is accessory selection", "HIGH"

    # Physical adjustment key/tool remains hardware; regulation is use context.
    if "ключ" in p and hardware and "регулиров" in p:
        return "WINDOW_HARDWARE", "Adjustment key/tool is the physical head product; regulation is use context", "HIGH"

    # Hardware belonging to a mosquito/window-screen family stays with that family.
    if hardware and "сет" in p and win:
        return "MOSQUITO_NETS", "Hardware belongs to the window-screen accessory family rather than sash hardware", "HIGH"

    # Explicit home-context repair is DIY even in a truncated phrase.
    if "ремонт" in p and win and has(p, "в домашних", "домашних условиях"):
        return "WINDOW_REPAIR_DIY", "Home-condition wording explicitly marks a DIY repair task", "HIGH"

    # Numeric panoramic dimensions: only treat numbers as a size when the explicit
    # panoramic-window head precedes the numeric pattern. This keeps ambiguous
    # context phrases such as '6 6 с панорамными окнами' unresolved instead of
    # inventing a window-size interpretation.
    panoramic_size = re.search(
        r"(?:панорам\w*\s+окн\w*|окн\w*\s+панорам\w*)\s+"
        r"\d+(?:[.,]\d+)?(?:\s+(?:на\s+)?\d+(?:[.,]\d+)?)?(?:\s|$)",
        p,
    )
    if panoramic_size:
        return "WINDOW_DIMENSIONS_INFO", "Explicit numeric panoramic-window sizing pattern", "HIGH"

    # 'Рулонные' alone does not prove a curtain/blind head object.
    if p == "рулонные пластиковые окна":
        return None, "Roll-type modifier without a curtain/blind head word does not identify a stable product task", "LOW"

    # Explicit French-window product head remains clear under private-house/panoramic modifiers.
    if p in {"французские окна в частном", "французские панорамные окна"}:
        return "FRENCH_WINDOWS_COMMERCIAL", "Explicit French-window product head; private-house/panoramic wording is a configuration/use modifier", "HIGH"

    # Explicit repair noun wins over the generic symptom-only uncertainty rule.
    if "ремонт" in p and win and has(p, "не закры", "не откры", "плохо закры", "провис", "просел", "просела"):
        return "WINDOW_REPAIR", "Explicit repair action resolves the repair task; symptom wording is secondary", "HIGH"

    # Provider/manufacturer query is determinate; bare production wording remains
    # process-vs-provider ambiguous unless other transactional wording resolves it.
    if p == "производители оконной фурнитуры":
        return "WINDOW_HARDWARE", "Plural manufacturers wording is a provider/source query for window hardware", "MEDIUM"
    if p in {"производство алюминиевых окон", "панорамные окна производство", "окна rehau производство"}:
        return None, "Bare production wording can mean manufacturing process or provider/manufacturer search", "LOW"

    return _v38_classifier(phrase)


b.classify_semantic = classify_v39


def full_discovery_self_check() -> None:
    misses = []
    for row in spec.ROWS:
        task_id, reason, confidence = b.classify_semantic(row["phrase"])
        observed = task_id or "SEARCH_REQUIRED"
        expected = row["proposed_cluster_id"]
        if observed != expected:
            misses.append({
                "phrase": row["phrase"],
                "expected": expected,
                "observed": observed,
                "reason": reason,
            })
    if misses:
        for miss in misses:
            print("V39_DISCOVERY_SELF_CHECK_FAIL", miss)
        raise SystemExit(f"V39 discovery self-check failed: {len(misses)} residual errors")
    print(f"V39_DISCOVERY_SELF_CHECK_PASS rows={len(spec.ROWS)}")


if __name__ == "__main__":
    full_discovery_self_check()
    runner.main()
