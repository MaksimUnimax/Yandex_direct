#!/usr/bin/env python3
"""Runner for the full fresh-R1 Pass3 QA with an independent morphology guard."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("pass3_full", HERE / "step10_fresh_r1_pass3_full.py")
if SPEC is None or SPEC.loader is None:
    raise SystemExit("cannot load Pass3 implementation")
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

original_classify = module.classify


def classify_with_okon_guard(phrase: str, source_reason: str, direct_observed_job: str = ""):
    normalized = module.norm(phrase)
    if normalized == "окон п 44 т":
        return module.unresolved("U003_OPAQUE_FRAGMENT", "opaque lexical fragment requires ordinary search or upstream clarification")
    guarded_phrase = re.sub(r"(?<![а-яa-z])окон(?![а-яa-z])", "окно", phrase.lower().replace("ё", "е"))
    return original_classify(guarded_phrase, source_reason, direct_observed_job)


module.classify = classify_with_okon_guard
raise SystemExit(module.main())
