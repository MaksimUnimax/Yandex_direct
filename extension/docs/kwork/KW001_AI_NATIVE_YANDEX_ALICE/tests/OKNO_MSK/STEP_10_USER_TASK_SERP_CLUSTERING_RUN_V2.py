#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner

_original = b.classify_semantic


def classify_semantic_with_window_inflection(phrase: str):
    result = _original(phrase)
    if result[0] is not None:
        return result
    # The base conservative taxonomy uses the stem `окн` for окно/окна/окнами.
    # Russian genitive/plural forms such as `окон` use `окон-`; normalize only this
    # morphological form and retry the same semantic rules. This is not a new
    # cluster signal and does not create evidence transfer between phrases.
    normalized = re.sub(r"\bокон(?=\b|\s)", "окн", phrase, flags=re.IGNORECASE)
    if normalized != phrase:
        return _original(normalized)
    return result


b.classify_semantic = classify_semantic_with_window_inflection

if __name__ == "__main__":
    runner.main()
