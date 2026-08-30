#!/usr/bin/env python3
"""Hardened runner for the full fresh-R1 Pass3 QA.

The wrapper fixes module registration for dataclasses, normalizes the Russian
standalone genitive plural ``окон`` for object recognition, applies direct
Step-09 evidence only to the exact query row, and binds the Pass3 implementation
to the canonical singular Pass2 assignment artifact.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("step10_pass3_full_impl", HERE / "step10_fresh_r1_pass3_full.py")
if SPEC is None or SPEC.loader is None:
    raise SystemExit("cannot load Pass3 implementation")
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)

# Pass2 canonically writes STEP_10_FRESH_R1_ASSIGNMENT.tsv (singular).
# Keep the full Pass3 implementation bound to that existing artifact instead
# of requiring a duplicate or a phantom plural filename.
module.ASSIGNMENT_NAME = "STEP_10_FRESH_R1_ASSIGNMENT.tsv"

original_classify = module.classify


def direct_exact_decision(direct_observed_job: str):
    d = module.norm(direct_observed_job)
    if not d:
        return None
    if "open balcony" in d:
        return module.decision("OPEN_BALCONY_FINISHING", "DX01_OPEN_BALCONY", "exact Step-09 evidence: open-balcony finishing is separate from glazing")
    if "demolition" in d or "dismantl" in d:
        return module.decision("WINDOW_DEMOLITION_SERVICE", "DX02_DEMOLITION", "exact Step-09 evidence: demolition/dismantling service")
    if "hardware" in d:
        return module.decision("WINDOW_HARDWARE_SHOPPING", "DX03_HARDWARE", "exact Step-09 evidence: window-hardware/component shopping")
    if "accessory shopping" in d or "accessories" in d:
        return module.decision("WINDOW_ACCESSORIES_SHOPPING", "DX04_ACCESSORY", "exact Step-09 evidence: window-accessory shopping")
    if "timber aluminium" in d or "wood aluminium" in d:
        return module.decision("TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL", "DX05_HYBRID", "exact Step-09 evidence: timber-aluminium window product")
    if "wooden window" in d or "wood window" in d:
        return module.decision("WOOD_WINDOWS_COMMERCIAL", "DX06_WOOD", "exact Step-09 evidence: wooden-window product")
    if "soft window" in d:
        return module.decision("SOFT_WINDOWS_COMMERCIAL", "DX07_SOFT", "exact Step-09 evidence: soft-window product")
    if "french window" in d:
        return module.decision("FRENCH_WINDOWS_COMMERCIAL", "DX08_FRENCH", "exact Step-09 evidence: French-window product/form job")
    if "panoramic window" in d:
        return module.decision("PANORAMIC_WINDOWS_COMMERCIAL", "DX09_PANORAMIC", "exact Step-09 evidence: panoramic-window product/form job")
    if "aluminium window" in d or "aluminum window" in d:
        return module.decision("ALUMINIUM_WINDOWS_COMMERCIAL", "DX10_ALUMINIUM", "exact Step-09 evidence: aluminium-window product")
    if "pvc door" in d:
        return module.decision("PVC_DOORS_COMMERCIAL", "DX11_PVC_DOOR", "exact Step-09 evidence: PVC-door product")
    if "warm balcony" in d or "warm glazing" in d:
        return module.decision("BALCONY_GLAZING_WARM", "DX12_WARM_BALCONY", "exact Step-09 evidence: warm balcony glazing")
    if "cold balcony" in d or "cold glazing" in d:
        return module.decision("BALCONY_GLAZING_COLD", "DX13_COLD_BALCONY", "exact Step-09 evidence: cold balcony glazing")
    if "roof" in d and "balcony" in d:
        return module.decision("BALCONY_GLAZING_ROOF_SERVICE", "DX14_BALCONY_ROOF", "exact Step-09 evidence: balcony glazing with roof scope")
    if ("extension" in d or "outset" in d) and "balcony" in d:
        return module.decision("BALCONY_GLAZING_EXTENSION_SERVICE", "DX15_BALCONY_EXTENSION", "exact Step-09 evidence: balcony glazing with extension/outset")
    if "frameless veranda" in d or "veranda glazing" in d or "terrace glazing" in d:
        return module.decision("OUTDOOR_STRUCTURE_GLAZING", "DX16_OUTDOOR_GLAZING", "exact Step-09 evidence: outdoor-structure glazing service")
    return None


def classify_with_guards(phrase: str, source_reason: str, direct_observed_job: str = ""):
    exact = direct_exact_decision(direct_observed_job)
    if exact is not None:
        return exact
    normalized = module.norm(phrase)
    if normalized in {"окон п 44 т", "ral алюминиевых окон", "без алюминиевой окна", "алюминиевый м окно"}:
        return module.unresolved("U003_OPAQUE_FRAGMENT", "opaque lexical fragment requires ordinary search or upstream clarification")
    guarded_phrase = re.sub(r"(?<![а-яa-z])окон(?![а-яa-z])", "окно", phrase.lower().replace("ё", "е"))
    return original_classify(guarded_phrase, source_reason, direct_observed_job)


module.classify = classify_with_guards
raise SystemExit(module.main())
