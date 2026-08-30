#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V17 as v17

_v17_classifier = b.classify_semantic


def classify_v18(phrase: str):
    p = v17.v16.v15.n(phrase)

    # Explicit whole-window / balcony-block replacement or conversion is an action/service
    # and must outrank the French-window product/configuration guard introduced in V17.
    # Keep component replacement (handle/seal/glazing-unit/etc.) outside this rule by
    # requiring the whole window or balcony block to be the explicit replacement object.
    whole_replacement = v17.v16.v15.has(
        p,
        "замена окна", "замена окон", "замена пластиковых окон", "замена панорамных окон", "замена французских окон",
        "заменить окно", "заменить окна", "поменять окно", "поменять окна",
        "замена балконного блока", "заменить балконный блок", "поменять балконный блок",
    )
    if whole_replacement and "ремонт" in p:
        return None, "Phrase explicitly mixes repair and whole-window replacement; keep the boundary visible", "LOW"
    if whole_replacement:
        return "WINDOW_REPLACEMENT_SERVICE", "Explicit whole-window/balcony-block replacement or conversion action outranks French/product configuration context", "HIGH"

    return _v17_classifier(phrase)


b.classify_semantic = classify_v18


def self_test() -> None:
    # Re-run the complete inherited V15/V16/V17 corpus against the final V18 classifier.
    v17.self_test()

    replacement = b.classify_semantic("замена балконного блока на французское окно")
    assert replacement[0] == "WINDOW_REPLACEMENT_SERVICE", replacement

    mixed_repair_replacement = b.classify_semantic("ремонт и замена пластиковых окон")
    assert mixed_repair_replacement[0] is None, mixed_repair_replacement

    french = b.classify_semantic("французские окна в москве в квартирах")
    assert french[0] == "FRENCH_WINDOWS_COMMERCIAL", french

    french_balcony = b.classify_semantic("французское окно на балкон в квартире")
    assert french_balcony[0] == "FRENCH_WINDOWS_COMMERCIAL", french_balcony

    porch = b.classify_semantic("крыльцо для частного дома окна")
    assert porch[0] == "PORCH_GLAZING", porch

    pvc_house = b.classify_semantic("окна пвх для частного дома")
    assert pvc_house[0] == "PVC_WINDOWS_COMMERCIAL", pvc_house

    pvc_dimensions = b.classify_semantic("размеры окон пвх для частного дома")
    assert pvc_dimensions[0] == "WINDOW_DIMENSIONS_INFO", pvc_dimensions


if __name__ == "__main__":
    self_test()
    runner.main()
