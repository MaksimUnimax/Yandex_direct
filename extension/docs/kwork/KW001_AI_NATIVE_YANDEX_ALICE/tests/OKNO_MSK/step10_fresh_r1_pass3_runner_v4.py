#!/usr/bin/env python3
"""Final Pass3 runner extending the last intact v2 base.

The previously referenced lowercase ``step10_fresh_r1_pass3_runner_v3.py`` was
never committed. V4 therefore extends the last real, reviewable base (V2)
directly.

The wrapper contains one consolidated, task-first precedence layer. Its rules
express reusable semantic contrasts (negation, expected result, whole object vs
component, buy vs hire vs DIY, transaction vs information) rather than exact
phrase patches.
"""

from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
v2_path = HERE / "step10_fresh_r1_pass3_runner_v2.py"
source = v2_path.read_text(encoding="utf-8")
terminal = "module.classify = classify_with_guards\nraise SystemExit(module.main())"
replacement = "module.classify = classify_with_guards"
if terminal not in source:
    raise SystemExit("unexpected v2 runner shape")
namespace = {"__file__": str(v2_path), "__name__": "step10_pass3_v2_library"}
exec(compile(source.replace(terminal, replacement), str(v2_path), "exec"), namespace)

module = namespace["module"]
direct_exact_decision = namespace["direct_exact_decision"]
base_classify = module.classify
base_invariants = module.invariant_violations


def h(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def whole_product_cluster(text: str) -> str:
    """Resolve the acquired whole product without treating modifiers as tasks."""
    window = h(text, r"\bокн(?:о|а|е|у|ом|ами|ах)?\b|\bокон\b|оконн")
    door = h(text, r"двер")
    pvc = h(text, r"пластиков|\bпвх\b")
    if window and door:
        return "WINDOWS_DOORS_COMBINED_COMMERCIAL"
    if door and pvc:
        return "PVC_DOORS_COMMERCIAL"
    if h(text, r"деревянн?о? алюмин|дерево алюмин|алюмин.*дерев"):
        return "TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL"
    if h(text, r"мягк(?:ие|ое|их)? окн|гибк(?:ие|ое|их)? окн"):
        return "SOFT_WINDOWS_COMMERCIAL"
    if h(text, r"мансардн.*окн|окн.*(?:крыш|кровл)"):
        return "ROOF_WINDOWS_COMMERCIAL"
    if h(text, r"\b(?:rehau|рехау)\b"):
        return "REHAU_WINDOWS_COMMERCIAL"
    if h(text, r"алюмин"):
        return "ALUMINIUM_WINDOWS_COMMERCIAL"
    if h(text, r"деревян|дерево"):
        return "WOOD_WINDOWS_COMMERCIAL"
    if h(text, r"панорам"):
        return "PANORAMIC_WINDOWS_COMMERCIAL"
    if h(text, r"французск"):
        return "FRENCH_WINDOWS_COMMERCIAL"
    if pvc and window:
        return "PVC_WINDOWS_COMMERCIAL"
    return "WINDOWS_COMMERCIAL_GENERAL"


def classify_v4(phrase: str, source_reason: str, direct_observed_job: str = ""):
    t = module.norm(phrase)

    # Exact row evidence has precedence and is never transferred to neighbours.
    exact = direct_exact_decision(direct_observed_job)
    if exact is not None:
        return exact

    # Outside-topic boundaries must remain outside even when the query asks for reviews.
    if h(t, r"штор|жалюз|плиссе|занавес|ставн"):
        return module.decision("OUTSIDE_CURTAINS_BLINDS", "O401_CURTAINS", "curtain/blind result is outside the window/glazing task")
    if h(t, r"конвектор|радиатор|батаре|отоплен|теплый пол|кондиционер"):
        return module.decision("OUTSIDE_HEATING_HVAC", "O402_HEATING", "heating/HVAC result is outside the window/glazing task")

    window = h(t, r"\bокн(?:о|а|е|у|ом|ами|ах)?\b|\bокон\b|оконн|стеклопакет")
    door = h(t, r"двер")
    pvc_door = door and h(t, r"пластиков|\bпвх\b")
    balcony = h(t, r"балкон|лоджи")
    outdoor = h(t, r"веранд|террас|бесед|крыльц")
    glazing = h(t, r"остеклен|застекл|стеклить|стекление")
    purchase = h(t, r"купить|заказ|цен|стоим|магазин|каталог|производител|производств|изготов|завод|рассроч|кредит|недорог|дешев|продаж|готов|под ключ")
    diy = h(t, r"своими руками|самостоятель|самому|пошаг|инструкц|как (?:сделать|установить|снять|заменить|поменять|смонтировать)")
    install = h(t, r"установк|установить|монтаж|смонтир")
    replace = h(t, r"замен|поменя")
    repair = h(t, r"ремонт|почин|регулиров|замен|поменя")
    review = h(t, r"отзыв|рейтинг|репутац")
    permission = h(t, r"разрешен|можно ли|перепланиров|согласован|требован|норматив|\bгост\b|закон")
    selection = h(t, r"вариант|виды|типы|выбор|выбрать|какой|какие|что лучше|сравн|отлич")
    visual = h(t, r"\bфото\b|дизайн|интерьер|иде[яи]|пример|стиль|оформлен|проект")
    video = h(t, r"\bвидео\b")
    finishing = h(t, r"подоконник|откос|отлив|наличник|нащельник")
    finishing_action = h(t, r"отделк|обшив|облицов|оштукатур|штукатур|заделк.*проем|оформлен.*откос")
    hardware_or_component = h(t, r"фурнитур|ручк|петл|уплотн|замок|защелк|микролифт|ограничител|блокиратор|цапф|ножниц|редуктор|ролик|штапик|гребенк|механизм|ригель|кремон|стеклопакет|створк|стекло (?:на|для)|направляющ|соединител|оконн.*узл|узлы .*окон")
    accessory = h(t, r"аксессуар|дополнени[ея] для .*окн|комплектующ")
    spare_parts = h(t, r"запчаст|комплектующ|ремкомплект|детал[ьи] для")
    install_consumable = h(t, r"монтажн.*пен|\bпена\b|клинья|саморез|анкерн.*пластин|монтажн.*пластин")
    without_installation = h(t, r"без (?:установк|монтаж)|без работ по установ|не треб.*(?:установк|монтаж)")
    provider_subject = h(t, r"компан|фирм|мастер|подрядчик|установщик|исполнител|сервис")
    interior_door = door and h(t, r"внутренн|межкомнат|в комнат|в ванн|в туалет|дверь купе|гармошк") and not h(t, r"балкон|входн|уличн|наружн|террас|в дом|частн")
    foreign_enclosure = door and h(t, r"корпус|шкаф|витрин|контейнер|бокс|кейс|щит|станок|оборудован|аквариум|террариум|печь") and not (window or balcony or glazing)

    # Known opaque candidates discovered in the full pass remain fail-closed.
    if t in {
        "оконные блоки фурнитурой",
        "остекление балкона работу",
        "пластиковые окна комарова",
        "пластиковые окна домашние окна",
    }:
        return module.unresolved("U401_FULL_PASS_OPAQUE_CANDIDATE", "full-pass QA found no stable expected result without ordinary search")

    # Explicit semantic scope overrides broad product attraction.
    if foreign_enclosure:
        return module.decision("OUTSIDE_OTHER", "O403_FOREIGN_ENCLOSURE", "door is a component of an unrelated enclosure rather than the target product")
    if interior_door:
        return module.decision("OUTSIDE_INTERIOR_DOORS", "O404_INTERIOR_DOOR", "interior-door result is outside the target exterior/balcony-door scope")

    # Permission, legality and replanning are information results, not product purchases.
    if permission and (window or door or glazing or balcony or outdoor):
        return module.decision("GLAZING_PERMISSION_INFO", "I405_PERMISSION_RESULT", "permission, legal or replanning information is the terminal result")

    # A negated included service cannot become the requested service.
    if without_installation and (window or pvc_door) and not (glazing or balcony or outdoor):
        return module.decision(whole_product_cluster(t), "P401_PRODUCT_WITHOUT_SERVICE", "whole-product acquisition explicitly excludes installation service")

    # Reviews, ratings and reputation are information tasks even when a service word is present.
    if review:
        if hardware_or_component:
            return module.decision("WINDOW_HARDWARE_INFO", "I406_COMPONENT_REVIEWS", "reviews or reputation about a component are an information result")
        if balcony or glazing or outdoor:
            return module.decision("BALCONY_GLAZING_INFO" if balcony else "GLAZING_SELECTION_INFO", "I407_GLAZING_REVIEWS", "reviews or reputation about glazing are a selection-information result")
        if window or door or provider_subject:
            return module.decision("WINDOW_REVIEWS_INFO", "I408_PROVIDER_OR_PRODUCT_REVIEWS", "reviews, ratings or provider reputation are the terminal result")

    # Hardware brands/types and component selection are information, not shopping, without a transaction signal.
    if hardware_or_component and not purchase and h(t, r"бренд|марки|производител|виды|типы|какая|какие|какой|выбор|сравн|отзыв|рейтинг"):
        return module.decision("WINDOW_HARDWARE_INFO", "H406_COMPONENT_SELECTION_INFO", "component brands, types, reviews or selection are an information result")

    # Parent product words are context when the requested object is an accessory or spare part.
    if accessory:
        if selection and not purchase:
            return module.decision("WINDOW_ACCESSORY_SELECTION_INFO", "A402_ACCESSORY_SELECTION", "selection of an accessory/add-on")
        return module.decision("WINDOW_ACCESSORIES_SHOPPING", "A403_ACCESSORY_SHOPPING", "the requested object is an accessory/add-on, not the parent product")
    if spare_parts and h(t, r"для ремонт|для установ|для монтаж|на ремонт|купить|цен|магазин|заказ"):
        return module.decision("WINDOW_HARDWARE_SHOPPING", "A404_SPARE_PARTS_FOR_ACTION", "spare parts or components for a later action are products, not the hired action")

    # Consumables/tools for a later install are products, not the installation service itself.
    if install_consumable and h(t, r"для установ|для монтаж|пена установ|клинья установ|пластин"):
        return module.decision("WINDOW_HARDWARE_SHOPPING", "A401_INSTALL_CONSUMABLE", "installation consumable/tool shopping")

    # DIY creation/replacement of the whole object is how-to information, never a hired replacement service.
    if diy and (window or pvc_door) and not (hardware_or_component or finishing or accessory or glazing):
        if h(t, r"сделать|установ|монтаж|вставить|замен|поменя|снять"):
            return module.decision("WINDOW_INSTALLATION_DIY_INFO", "I409_WHOLE_OBJECT_DIY", "how to create, replace or install the whole object is a DIY information result")

    # A bare video request without an action seeks product information, not DIY repair.
    if video and (window or pvc_door) and not h(t, r"как|ремонт|почин|замен|поменя|установ|монтаж|снять|регулиров|отделк|остеклен|застекл"):
        return module.decision("WINDOW_PRODUCT_TECH_INFO", "I410_BARE_PRODUCT_VIDEO", "a product video without an action is technical/product information")

    # Whole-system replacement and repair take precedence over generic new glazing.
    if replace and glazing and not diy:
        return module.decision("WINDOW_REPLACEMENT_SERVICE", "S401_GLAZING_REPLACEMENT", "replacement of an existing glazing system is a replacement lifecycle result")
    if repair and balcony and glazing and not diy:
        return module.decision("BALCONY_RENOVATION_WITH_GLAZING", "S402_BALCONY_GLAZING_REPAIR", "repair/renovation of balcony glazing differs from ordering generic new glazing")

    # Selection wording is decision support; visual wording is inspiration.
    if (glazing or balcony or outdoor) and selection and not visual and not purchase:
        return module.decision("BALCONY_GLAZING_INFO" if balcony else "GLAZING_SELECTION_INFO", "G403_GLAZING_SELECTION", "variants, types or comparison seek glazing decision support")

    # A finishing action is a post-product lifecycle task, not whole-product shopping.
    if finishing_action and (window or pvc_door) and not h(t, r"материал|панел|комплект|купить|магазин|каталог"):
        if diy:
            return module.decision("WINDOW_FINISHING_DIY_INFO", "F409_FINISHING_ACTION_DIY", "DIY finishing/how-to result")
        return module.decision("WINDOW_FINISHING_SERVICE", "F410_FINISHING_ACTION_SERVICE", "professional finishing is the requested terminal result")

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
    finishing_action = h(t, r"отделк|обшив|облицов|оштукатур|штукатур")
    install = h(t, r"установк|установить|монтаж|смонтир")
    component = h(t, r"фурнитур|ручк|петл|уплотн|замок|ограничител|стеклопакет|створк|стекло (?:на|для)|направляющ|соединител")
    accessory = h(t, r"аксессуар|запчаст|комплектующ|ремкомплект")
    consumable = h(t, r"монтажн.*пен|\bпена\b|клинья|саморез|анкерн.*пластин|монтажн.*пластин")
    without_installation = h(t, r"без (?:установк|монтаж)|не треб.*(?:установк|монтаж)")
    review = h(t, r"отзыв|рейтинг|репутац")
    permission = h(t, r"разрешен|можно ли|перепланиров|согласован|требован|норматив|\bгост\b|закон")
    diy_whole = h(t, r"своими руками|самостоятель|самому|пошаг|инструкц|как (?:сделать|установить|снять|заменить|поменять|смонтировать)") and not component
    interior_door = h(t, r"внутренн|межкомнат|в комнат|в ванн|в туалет|дверь купе|гармошк")
    bare_video = h(t, r"\bвидео\b") and not h(t, r"как|ремонт|почин|замен|поменя|установ|монтаж|снять|регулиров|отделк|остеклен|застекл")

    if finishing and cluster in {"PVC_WINDOWS_COMMERCIAL", "REHAU_WINDOWS_COMMERCIAL", "ALUMINIUM_WINDOWS_COMMERCIAL", "WINDOWS_COMMERCIAL_GENERAL", "PVC_DOORS_COMMERCIAL"}:
        violations.append("FINISHING_COMPONENT_MUST_NOT_BE_BASE_PRODUCT")
    if component and install and not consumable and cluster in {"WINDOW_HARDWARE_SHOPPING", "WINDOW_ACCESSORIES_SHOPPING", "PVC_WINDOWS_COMMERCIAL", "REHAU_WINDOWS_COMMERCIAL", "PVC_DOORS_COMMERCIAL"}:
        violations.append("COMPONENT_INSTALL_MUST_NOT_BE_PRODUCT_SHOPPING")
    if consumable and h(t, r"для установ|для монтаж|пена установ|клинья установ|пластин") and cluster in {"WINDOW_INSTALLATION_SERVICE", "WINDOW_REPAIR_SERVICE"}:
        violations.append("INSTALL_CONSUMABLE_MUST_NOT_BE_HIRED_SERVICE")
    if h(t, r"зазор при установ|после установки|правильн.*установ") and cluster == "WINDOW_INSTALLATION_SERVICE":
        violations.append("INSTALLATION_TECH_CONTEXT_MUST_NOT_BE_SERVICE")
    if without_installation and cluster in {"WINDOW_INSTALLATION_SERVICE", "PVC_DOOR_INSTALLATION_SERVICE"}:
        violations.append("NEGATED_INSTALLATION_MUST_NOT_BE_SERVICE")
    if review and cluster in {"WINDOW_INSTALLATION_SERVICE", "WINDOW_REPAIR_SERVICE", "BALCONY_GLAZING_GENERAL", "OUTDOOR_STRUCTURE_GLAZING", "PVC_WINDOWS_COMMERCIAL", "PVC_DOORS_COMMERCIAL"}:
        violations.append("REVIEWS_MUST_NOT_BE_TRANSACTIONAL_RESULT")
    if accessory and cluster in {"PVC_WINDOWS_COMMERCIAL", "PVC_DOORS_COMMERCIAL", "WINDOWS_COMMERCIAL_GENERAL", "WINDOW_INSTALLATION_SERVICE", "WINDOW_REPAIR_SERVICE"}:
        violations.append("ACCESSORY_OR_SPARE_PART_MUST_NOT_BE_PARENT_PRODUCT_OR_SERVICE")
    if permission and cluster in {"PVC_WINDOWS_COMMERCIAL", "REHAU_WINDOWS_COMMERCIAL", "FRENCH_WINDOWS_COMMERCIAL", "PANORAMIC_WINDOWS_COMMERCIAL", "BALCONY_GLAZING_GENERAL", "OUTDOOR_STRUCTURE_GLAZING", "GENERAL_GLAZING_SERVICE"}:
        violations.append("PERMISSION_RESULT_MUST_NOT_BE_TRANSACTIONAL")
    if finishing_action and cluster in {"PVC_WINDOWS_COMMERCIAL", "REHAU_WINDOWS_COMMERCIAL", "ALUMINIUM_WINDOWS_COMMERCIAL", "WINDOWS_COMMERCIAL_GENERAL"}:
        violations.append("FINISHING_ACTION_MUST_NOT_BE_WHOLE_PRODUCT")
    if diy_whole and cluster in {"WINDOW_REPLACEMENT_SERVICE", "WINDOW_INSTALLATION_SERVICE", "PVC_DOOR_REPLACEMENT_SERVICE", "PVC_DOOR_INSTALLATION_SERVICE", "WINDOW_REPAIR_SERVICE"}:
        violations.append("WHOLE_OBJECT_DIY_MUST_NOT_BE_HIRED_SERVICE")
    if interior_door and cluster in {"PVC_DOORS_COMMERCIAL", "PVC_DOOR_INSTALLATION_SERVICE", "PVC_DOOR_REPAIR_SERVICE"}:
        violations.append("INTERIOR_DOOR_MUST_NOT_BE_TARGET_PVC_DOOR_TASK")
    if bare_video and cluster == "WINDOW_REPAIR_DIY_INFO":
        violations.append("BARE_PRODUCT_VIDEO_MUST_NOT_BE_REPAIR_DIY")
    return sorted(set(violations))


module.classify = classify_v4
module.invariant_violations = invariants_v4
raise SystemExit(module.main())
