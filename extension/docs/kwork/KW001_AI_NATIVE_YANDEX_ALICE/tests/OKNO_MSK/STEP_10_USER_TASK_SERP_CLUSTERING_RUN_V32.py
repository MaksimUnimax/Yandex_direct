#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V31 as v31

_v31_classifier = b.classify_semantic


def classify_v32(phrase: str):
    p = b.norm(phrase)

    # Same V31 morphology root cause: genitive/adjectival 'окон' must count as
    # window context. RAL is a colour/configuration marker, not sufficient
    # evidence for ordinary whole-window commercial demand.
    if "ral" in p and "алюмини" in p and v31.windowish_v31(p):
        return None, "RAL colour wording is a configuration/appearance task, not safe whole-window purchase evidence", "LOW"

    return _v31_classifier(phrase)


b.classify_semantic = classify_v32


def self_test() -> None:
    v31.self_test()
    got = b.classify_semantic("ral алюминиевых окон")
    assert got[0] is None, got


if __name__ == "__main__":
    self_test()
    runner.main()
