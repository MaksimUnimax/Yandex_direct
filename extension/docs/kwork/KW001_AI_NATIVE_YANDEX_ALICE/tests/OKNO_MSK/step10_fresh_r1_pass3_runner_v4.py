#!/usr/bin/env python3
"""Final Pass3 runner, extending v3 with component-install grammar guards."""

from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
v3_path = HERE / "step10_fresh_r1_pass3_runner_v3.py"
source = v3_path.read_text(encoding="utf-8")
terminal = "module.classify = classify_v3\nmodule.invariant_violations = invariants_v3\nraise SystemExit(module.main())"
replacement = "module.classify = classify_v3\nmodule.invariant_violations = invariants_v3"
if terminal not in source:
    raise SystemExit("unexpected v3 runner shape")
namespace = {"__file__": str(v3_path), "__name__": "step10_pass3_v3_library"}
exec(compile(source.replace(terminal, replacement), str(v3_path), "exec"), namespace)

module = namespace["module"]
base_classify = module.classify
base_invariants = module.invariant_violations


def h(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def classify_v4(phrase: str, source_reason: str, direct_observed_job: str = ""):
    t = module.norm(phrase)

    # Outside-topic boundaries must remain outside even when the query asks for reviews.
    if h(t, r"штор|жалюз|плиссе|занавес|ставн"):
        return module.decision("OUTSIDE_CURTAINS_BLINDS", "O401_CURTAINS", "curtain/blind result is outside the window/glazing task")
    if h(t, r"конвектор|радиатор|батаре|отоплен|теплый пол|кондиционер"):
        return module.decision("OUTSIDE_HEATING_HVAC", "O402_HEATING", "heating/HVAC result is outside the window/glazing task")

    window = h(t, r"\bокн(?:о|а|е|у|ом|ами|ах)?\b|\bокон\b|оконн|стеклопакет")
    pvc_door = h(t, r"двер") and h(t, r"пластиков|\bпвх\b")
    balcony = h(t, r"балкон|лоджи")
    outdoor = h(t, r"веранд|террас|бесед|крыльц")
    glazing = h(t, r"остеклен|застекл|стеклить|стекление")
    purchase = h(t, r"купить|заказ|цен|стоим|магазин|каталог|производител|завод|рассроч|кредит|недорог|дешев")
    diy = h(t, r"своими руками|самостоятель|самому|пошаг|инструкц|как (?:сделать|установить|снять|заменить|поменять|смонтировать)")
    install = h(t, r"установк|установить|монтаж|смонтир")
    repair = h(t, r"ремонт|почин|регулиров|замен|поменя")
    finishing = h(t, r"подоконник|откос|отлив|наличник|нащельник")
    hardware_or_component = h(t, r"фурнитур|ручк|петл|уплотн|замок|защелк|микролифт|ограничител|блокиратор|цапф|ножниц|редуктор|ролик|штапик|гребенк|механизм|ригель|кремон|стеклопакет|створк|стекло (?:на|для)|направляющ|соединител|оконн.*узл|узлы .*окон")
    install_consumable = h(t, r"монтажн.*пен|\bпена\b|клинья|саморез|анкерн.*пластин|монтажн.*пластин")

    # Known opaque candidates discovered in the full pass remain fail-closed.
    if t in {
        "оконные блоки фурнитурой",
        "остекление балкона работу",
        "пластиковые окна комарова",
        "пластиковые окна домашние окна",
    }:
        return module.unresolved("U401_FULL_PASS_OPAQUE_CANDIDATE", "full-pass QA found no stable expected result without ordinary search")

    # Consumables/tools for a later install are products, not the installation service itself.
    if install_consumable and h(t, r"для установ|для монтаж|пена установ|клинья установ|пластин"):
        return module.decision("WINDOW_HARDWARE_SHOPPING", "A401_INSTALL_CONSUMABLE", "installation consumable/tool shopping")

    # Bare finishing components are add-on products; lifecycle verbs make them services.
    if finishing:
        if repair:
            if h(t, r"подоконник"):
                if diy:
                    return module.decision("WINDOW_FINISHING_DIY_INFO", "F401_WINDOWSILL_REPAIR_DIY", "DIY windowsill repair/finishing information")
                return module.decision("WINDOWSILL_REPAIR_SERVICE", "F402_WINDOWSILL_REPAIR", "professional windowsill repair/restoration")
            if diy:
                return module.decision("WINDOW_FINISHING_DIY_INFO", "F403_FINISHING_REPAIR_DIY", "DIY window finishing repair information")
            return module.decision("WINDOW_FINISHING_SERVICE", "F404_FINISHING_REPAIR", "professional window finishing repair")
        if install or h(t, r"цен.*работ|работ.*цен"):
            if diy:
                return module.decision("WINDOW_FINISHING_DIY_INFO", "F405_FINISHING_INSTALL_DIY", "DIY window finishing installation information")
            return module.decision("WINDOW_FINISHING_SERVICE", "F406_FINISHING_INSTALL", "professional window finishing installation")
        if h(t, r"как выбрать|какой лучше|виды|материал"):
            return module.decision("WINDOW_ACCESSORY_SELECTION_INFO", "F407_FINISHING_COMPONENT_SELECTION", "selection of a window finishing component")
        return module.decision("WINDOW_ACCESSORIES_SHOPPING", "F408_FINISHING_COMPONENT_SHOPPING", "window finishing component/add-on shopping", "MEDIUM")

    # Installing a structural component is a service; merely buying it remains shopping.
    if hardware_or_component and install and not install_consumable:
        if diy:
            return module.decision("WINDOW_REPAIR_DIY_INFO", "H401_COMPONENT_INSTALL_DIY", "DIY fitting/replacement of a window component")
        return module.decision("WINDOW_REPAIR_SERVICE", "H402_COMPONENT_INSTALL_SERVICE", "professional fitting/replacement of a window component")

    # Glass, guides, connectors and window assemblies are component jobs, not base-window products.
    if h(t, r"стекло (?:на|для) (?:пластиков|окон|двер)|направляющ.*окн|соединител.*окн"):
        if repair:
            return module.decision("WINDOW_REPAIR_SERVICE", "H403_COMPONENT_REPAIR", "professional window-component repair/replacement")
        return module.decision("WINDOW_HARDWARE_SHOPPING", "H404_COMPONENT_SHOPPING", "window structural component shopping")
    if h(t, r"узлы .*окон|оконн.*узл"):
        return module.decision("WINDOW_HARDWARE_INFO", "H405_WINDOW_ASSEMBLY_INFO", "window assembly/component reference information")

    # Technical context around installation is information, not an order for installers.
    if h(t, r"зазор при установ|после установки|правильн.*установ|технолог.*установ") and window:
        return module.decision("WINDOW_INSTALLATION_DIY_INFO", "I401_INSTALLATION_TECH_INFO", "window-installation technical/how-to information")
    if h(t, r"сверлен.*(?:окн|окон)|сборк.*(?:окн|окон)"):
        return module.decision("WINDOW_INSTALLATION_DIY_INFO", "I402_WINDOW_ASSEMBLY_DIY", "window assembly/drilling/installation information", "MEDIUM")

    # Glazing size/material wording without transaction signals is an information result.
    if (glazing or outdoor or balcony) and not purchase and h(t, r"размер|толщин|стекло остеклен|материал"):
        if balcony:
            return module.decision("BALCONY_GLAZING_INFO", "G401_BALCONY_GLAZING_SPEC", "balcony-glazing size/material/specification information")
        return module.decision("GLAZING_SELECTION_INFO", "G402_GLAZING_SPEC", "glazing size/material/specification information")

    # Service-provider superlatives are selection/reputation jobs.
    if h(t, r"лучшие (?:компании|фирмы)|лучшая (?:компания|фирма)"):
        if glazing or balcony or outdoor:
            return module.decision("GLAZING_SELECTION_INFO" if not balcony else "BALCONY_GLAZING_INFO", "I403_SERVICE_PROVIDER_SELECTION", "selection of a glazing provider")
        return module.decision("WINDOW_REVIEWS_INFO", "I404_WINDOW_PROVIDER_SELECTION", "selection/reputation of a window-service provider")

    return base_classify(phrase, source_reason, direct_observed_job)


def invariants_v4(phrase: str, status: str, cluster: str):
    violations = list(base_invariants(phrase, status, cluster))
    if status != "ASSIGNED":
        return violations
    t = module.norm(phrase)
    finishing = h(t, r"подоконник|откос|отлив|наличник|нащельник")
    install = h(t, r"установк|установить|монтаж|смонтир")
    component = h(t, r"фурнитур|ручк|петл|уплотн|замок|ограничител|стеклопакет|створк|стекло (?:на|для)|направляющ|соединител")
    consumable = h(t, r"монтажн.*пен|\bпена\b|клинья|саморез|анкерн.*пластин|монтажн.*пластин")
    if finishing and cluster in {"PVC_WINDOWS_COMMERCIAL", "REHAU_WINDOWS_COMMERCIAL", "ALUMINIUM_WINDOWS_COMMERCIAL", "WINDOWS_COMMERCIAL_GENERAL", "PVC_DOORS_COMMERCIAL"}:
        violations.append("FINISHING_COMPONENT_MUST_NOT_BE_BASE_PRODUCT")
    if component and install and not consumable and cluster in {"WINDOW_HARDWARE_SHOPPING", "WINDOW_ACCESSORIES_SHOPPING", "PVC_WINDOWS_COMMERCIAL", "REHAU_WINDOWS_COMMERCIAL", "PVC_DOORS_COMMERCIAL"}:
        violations.append("COMPONENT_INSTALL_MUST_NOT_BE_PRODUCT_SHOPPING")
    if consumable and h(t, r"для установ|для монтаж|пена установ|клинья установ|пластин") and cluster in {"WINDOW_INSTALLATION_SERVICE", "WINDOW_REPAIR_SERVICE"}:
        violations.append("INSTALL_CONSUMABLE_MUST_NOT_BE_HIRED_SERVICE")
    if h(t, r"зазор при установ|после установки|правильн.*установ") and cluster == "WINDOW_INSTALLATION_SERVICE":
        violations.append("INSTALLATION_TECH_CONTEXT_MUST_NOT_BE_SERVICE")
    return sorted(set(violations))


module.classify = classify_v4
module.invariant_violations = invariants_v4
raise SystemExit(module.main())
