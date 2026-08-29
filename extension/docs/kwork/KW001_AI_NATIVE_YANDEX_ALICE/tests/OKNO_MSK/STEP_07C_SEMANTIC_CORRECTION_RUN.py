#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUILDER = ROOT / "STEP_07C_SEMANTIC_CORRECTION_BUILD.py"

spec = importlib.util.spec_from_file_location("kw001_step07c_builder", BUILDER)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load semantic correction builder")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

_original_positive_for_source = module.positive_for_source

def positive_for_source_with_russian_window_inflection(text: str, source_id: str) -> bool:
    # Historical QA found that forms such as "окон" do not contain the literal substring "окн".
    # Normalize that inflection only for the positive-family test; the phrase itself is never rewritten.
    return _original_positive_for_source(text.replace("окон", "окн"), source_id)

module.positive_for_source = positive_for_source_with_russian_window_inflection
module.main()
