#!/usr/bin/env python3
"""Pass3 v5: product bundle 'windows with installation' != install-only service."""

from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
v4_path = HERE / "step10_fresh_r1_pass3_runner_v4.py"
source = v4_path.read_text(encoding="utf-8")
terminal = "module.classify = classify_v4\nmodule.invariant_violations = invariants_v4\nraise SystemExit(module.main())"
replacement = "module.classify = classify_v4\nmodule.invariant_violations = invariants_v4"
if terminal not in source:
    raise SystemExit("unexpected v4 runner shape")
namespace = {"__file__": str(v4_path), "__name__": "step10_pass3_v4_library"}
exec(compile(source.replace(terminal, replacement), str(v4_path), "exec"), namespace)

module = namespace["module"]
base_classify = module.classify
base_invariants = module.invariant_violations


def h(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def product_bundle_cluster(t: str) -> str:
    window = h(t, r"\bокн(?:о|а|е|у|ом|ами|ах)?\b|\bокон\b|оконн")
    door = h(t, r"двер")
    pvc = h(t, r"пластиков|\bпвх\b")
    if window and door:
        return "WINDOWS_DOORS_COMBINED_COMMERCIAL"
    if door and pvc:
        return "PVC_DOORS_COMMERCIAL"
    if h(t, r"деревянн?о? алюмин|дерево алюмин|алюмин.*дерев"):
        return "TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL"
    if h(t, r"мягк(?:ие|ое|их)? окн|гибк(?:ие|ое|их)? окн"):
        return "SOFT_WINDOWS_COMMERCIAL"
    if h(t, r"мансардн.*окн|окн.*(?:крыш|кровл)"):
        return "ROOF_WINDOWS_COMMERCIAL"
    if h(t, r"\b(?:rehau|рехау)\b"):
        return "REHAU_WINDOWS_COMMERCIAL"
    if h(t, r"алюмин"):
        return "ALUMINIUM_WINDOWS_COMMERCIAL"
    if h(t, r"деревян|дерево"):
        return "WOOD_WINDOWS_COMMERCIAL"
    if h(t, r"панорам"):
        return "PANORAMIC_WINDOWS_COMMERCIAL"
    if h(t, r"французск"):
        return "FRENCH_WINDOWS_COMMERCIAL"
    if pvc and window:
        return "PVC_WINDOWS_COMMERCIAL"
    return "WINDOWS_COMMERCIAL_GENERAL"


def classify_v5(phrase: str, source_reason: str, direct_observed_job: str = ""):
    t = module.norm(phrase)
    with_installation = h(t, r"\bс установк|включая установк|вместе с установк")
    service_primary = h(t, r"^(?:установка|монтаж|установить|смонтировать|заказ и установка|изготовление и установка|производство и установка)\b")
    disqualifier = h(t, r"остеклен|застекл|ремонт|замен|демонтаж|своими руками|самостоятель|инструкц|\bвидео\b|отзыв|рейтинг|москит|антикош|сетк|фурнитур|ручк|петл|уплотн|замок|жалюз|штор|подоконник|откос|отлив")
    product_object = h(t, r"\bокн(?:о|а|е|у|ом|ами|ах)?\b|\bокон\b|оконн|двер")
    if with_installation and product_object and not service_primary and not disqualifier:
        cluster = product_bundle_cluster(t)
        return module.decision(cluster, "P501_PRODUCT_WITH_INSTALLATION", "window/door product bundle with installation included")
    return base_classify(phrase, source_reason, direct_observed_job)


def invariants_v5(phrase: str, status: str, cluster: str):
    violations = list(base_invariants(phrase, status, cluster))
    if status != "ASSIGNED":
        return violations
    t = module.norm(phrase)
    with_installation = h(t, r"\bс установк|включая установк|вместе с установк")
    service_primary = h(t, r"^(?:установка|монтаж|установить|смонтировать|заказ и установка|изготовление и установка|производство и установка)\b")
    disqualifier = h(t, r"остеклен|застекл|ремонт|замен|демонтаж|своими руками|самостоятель|инструкц|\bвидео\b|отзыв|рейтинг|москит|антикош|сетк|фурнитур|ручк|петл|уплотн|замок|жалюз|штор|подоконник|откос|отлив")
    if with_installation and not service_primary and not disqualifier and cluster in {"WINDOW_INSTALLATION_SERVICE", "PVC_DOOR_INSTALLATION_SERVICE"}:
        violations.append("PRODUCT_WITH_INSTALLATION_MUST_NOT_BE_INSTALL_ONLY_SERVICE")
    return sorted(set(violations))


module.classify = classify_v5
module.invariant_violations = invariants_v5
raise SystemExit(module.main())
