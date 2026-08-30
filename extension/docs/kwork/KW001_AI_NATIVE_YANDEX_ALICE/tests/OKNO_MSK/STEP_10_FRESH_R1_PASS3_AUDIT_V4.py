#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_FRESH_R1_PASS3_AUDIT_V3 as v3

base = v3.base
V3_CLASSIFY = v3.v3_classify
base.RULE_VERSION = "PASS3_R1_INDEPENDENT_SEMANTIC_AUDIT_V4"


def A(cluster_id: str, confidence: str, rule: str, reason: str) -> base.AuditDecision:
    return base.assigned(cluster_id, confidence, rule, reason)


def S(rule: str, reason: str) -> base.AuditDecision:
    return base.search_required(rule, reason, True)


EXACT_ASSIGNED_RAW: dict[str, tuple[str, str, str]] = {
    # Mixed-object and lifecycle corrections found in the V3 all-cluster sample pass.
    "ремонт пластиковых окон и дверей": ("WINDOW_REPAIR_SERVICE", "COMBINED_REPAIR_SERVICE", "repair service for windows and doors; no combined repair cluster exists"),
    "ремонт регулировка пластиковых окон и дверей": ("WINDOW_REPAIR_SERVICE", "COMBINED_REPAIR_SERVICE", "repair/adjustment service for windows and doors"),
    "ремонт штульповых пластиковых окон дверей": ("WINDOW_REPAIR_SERVICE", "COMBINED_REPAIR_SERVICE", "repair of shtulp window/door constructions"),
    "цены на ремонт пластиковых окон": ("WINDOW_REPAIR_SERVICE", "REPAIR_PRICE_SERVICE", "price request for professional window repair"),
    "цены на монтаж пластиковых окон": ("WINDOW_INSTALLATION_SERVICE", "INSTALLATION_PRICE_SERVICE", "price request for professional window installation"),
    "цены на установку пластиковых окон москва": ("WINDOW_INSTALLATION_SERVICE", "INSTALLATION_PRICE_SERVICE", "price request for professional window installation"),
    "цены на пластиковые окна отзывы": ("WINDOW_REVIEWS_INFO", "MIXED_PRICE_REVIEW_INFO", "review/experience result dominates the accompanying price modifier"),
    "цены на пластиковые окна балконные двери": ("WINDOWS_DOORS_COMBINED_COMMERCIAL", "COMBINED_PRODUCT_PRICE", "combined window-and-balcony-door product price"),
    "цены окна алюминиевые профили": ("WINDOW_HARDWARE_SHOPPING", "ALUMINIUM_PROFILE_PRICE", "aluminium window-profile component price"),
    "поменять подоконник на пластиковом окне цена": ("WINDOWSILL_REPAIR_SERVICE", "WINDOWSILL_REPLACEMENT_SERVICE", "professional windowsill replacement price"),
    "замена откосов на пластиковых окнах цена": ("WINDOW_FINISHING_SERVICE", "SLOPE_REPLACEMENT_SERVICE", "professional slope replacement/finishing price"),
    "монтажная пластина для пластиковых окон rehau grazio": ("WINDOW_HARDWARE_SHOPPING", "MOUNTING_PLATE_COMPONENT", "mounting plate is a hardware component, not an installation action"),
    "аксессуары для пластиковых окон и дверей": ("WINDOW_ACCESSORIES_SHOPPING", "COMBINED_ACCESSORY_SHOPPING", "accessories for both windows and doors"),
    "оконная и дверная фурнитура": ("WINDOW_HARDWARE_SHOPPING", "COMBINED_HARDWARE_SHOPPING", "window-and-door hardware shopping"),
    "фурнитура оконной двери": ("WINDOW_HARDWARE_SHOPPING", "COMBINED_HARDWARE_SHOPPING", "door/window hardware component"),
    "балконный блок французское окно": ("FRENCH_WINDOWS_COMMERCIAL", "FRENCH_BALCONY_BLOCK_PRODUCT", "French-window form is the product object"),
    "дом панорамное окно дверь окно": ("OUTSIDE_REAL_ESTATE_ARCHITECTURE", "BUILDING_FORM_FRAGMENT", "building/form phrase rather than a stable window-and-door purchase"),
    "утепленное остекление балконов": ("BALCONY_GLAZING_WARM", "WARM_GLAZING_SYNONYM", "insulated glazing denotes the warm glazing result"),
    "остекление балкона под утепление": ("BALCONY_GLAZING_WARM", "WARM_GLAZING_PREPARATION", "glazing intended for insulation has a warm-result requirement"),
    "выбираем окна для частного дома": ("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "PRIVATE_HOUSE_SELECTION_MORPHOLOGY", "window choice/planning for a private house"),
    "как выбрать пластиковые окна для частного": ("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "PRIVATE_HOUSE_SELECTION_TRUNCATED", "truncated but clear private-house window selection task"),
    "окна в пол для частного дома": ("PANORAMIC_WINDOWS_COMMERCIAL", "FLOOR_TO_CEILING_WINDOW_PRODUCT", "floor-to-ceiling window is the panoramic product/form job"),
    "площадь окна для газовой котельной частного дома": ("WINDOW_DIMENSIONS_INFO", "PRIVATE_HOUSE_DIMENSIONS", "requested result is window area/sizing"),
    "корпус пластиковый прозрачная дверь": ("OUTSIDE_OTHER", "OUTSIDE_ENCLOSURE_PRODUCT", "plastic enclosure/cabinet with transparent door, not a PVC building door"),
    "щит пластиковый прозрачная дверь": ("OUTSIDE_OTHER", "OUTSIDE_ENCLOSURE_PRODUCT", "plastic electrical panel/enclosure with transparent door"),
    "пластиковые окна ремонт установка москитной сетки": ("MOSQUITO_NET_INSTALLATION_SERVICE", "MIXED_REPAIR_NET_INSTALL", "explicit mosquito-net installation is the actionable accessory service"),
    "тбм маркет мытищи оконная фурнитура": ("WINDOW_HARDWARE_SHOPPING", "HARDWARE_STORE_NAV_SHOPPING", "named hardware retailer/store query"),
    "как называется оконная фурнитура": ("WINDOW_HARDWARE_INFO", "HARDWARE_DEFINITION_INFO", "window-hardware terminology information"),
    "название оконной фурнитуры": ("WINDOW_HARDWARE_INFO", "HARDWARE_DEFINITION_INFO", "window-hardware terminology information"),
    "как называется пластиковая дверь": ("PVC_DOOR_INFO", "PVC_DOOR_DEFINITION_INFO", "PVC-door terminology/information"),
    "закроем пластиковые окна": ("WINDOW_PRODUCT_TECH_INFO", "WINDOW_OPERATION_REQUEST", "window closing/operation task rather than a purchase"),
    "открой панорамное окно": ("WINDOW_PRODUCT_TECH_INFO", "WINDOW_OPERATION_REQUEST", "window opening/operation task"),
    "закрой панорамное окно": ("WINDOW_PRODUCT_TECH_INFO", "WINDOW_OPERATION_REQUEST", "window closing/operation task"),
    "открытое пластиковое окно": ("WINDOW_PRODUCT_TECH_INFO", "WINDOW_STATE_INFO_V4", "window state/operation information"),
    "открытое панорамное окно": ("WINDOW_PRODUCT_TECH_INFO", "WINDOW_STATE_INFO_V4", "window state/operation information"),
}
EXACT_ASSIGNED = {base.norm(k): v for k, v in EXACT_ASSIGNED_RAW.items()}

EXACT_SEARCH_RAW = {
    "алюминиевый м окно",
    "пластиковая задняя дверь",
}
EXACT_SEARCH = {base.norm(x) for x in EXACT_SEARCH_RAW}


def product_cluster(q: str, source_reason: str) -> str:
    if "REHAU_WINDOW_INTENT" in source_reason or base.has(q, rf"\b{base.REHAU}\b"):
        return "REHAU_WINDOWS_COMMERCIAL"
    if "ALUMINIUM_WINDOW_INTENT" in source_reason or base.has(q, rf"\b{base.ALUMINIUM}\b"):
        return "ALUMINIUM_WINDOWS_COMMERCIAL"
    if "PVC_WINDOW_INTENT" in source_reason or base.has(q, rf"\b{base.PVC}\b"):
        return "PVC_WINDOWS_COMMERCIAL"
    if base.has(q, rf"\b{base.PANORAMIC}\b") or base.has(q, r"\b(?:в пол|до пола|от пола до потолка)\b"):
        return "PANORAMIC_WINDOWS_COMMERCIAL"
    if base.has(q, rf"\b{base.FRENCH}\b"):
        return "FRENCH_WINDOWS_COMMERCIAL"
    return "WINDOWS_COMMERCIAL_GENERAL"


def v4_classify(phrase: str, source_reason: str) -> base.AuditDecision:
    q = base.norm(phrase)

    # Exact Step-09 decisions remain immutable and query-local.
    if q in base.DIRECT_OVERRIDES:
        return V3_CLASSIFY(phrase, source_reason)
    if q in EXACT_ASSIGNED:
        cluster_id, rule, reason = EXACT_ASSIGNED[q]
        return A(cluster_id, "HIGH", rule, reason)
    if q in EXACT_SEARCH:
        return S("FULL_ROW_EDGE_SEARCH_REQUIRED", "full-row review found an unresolved object/context boundary")

    is_window = base.has(q, rf"\b{base.WINDOW}\b")
    is_door = base.has(q, rf"\b{base.DOOR}\b")
    is_pvc = base.has(q, rf"\b{base.PVC}\b")
    is_rehau = base.has(q, rf"\b{base.REHAU}\b")
    is_aluminium = base.has(q, rf"\b{base.ALUMINIUM}\b")
    is_french = base.has(q, rf"\b{base.FRENCH}\b")
    is_panoramic = base.has(q, rf"\b{base.PANORAMIC}\b") or base.has(q, r"\b(?:в пол|до пола|от пола до потолка)\b")
    is_balcony = base.has(q, rf"\b{base.BALCONY}\b")
    is_structure = base.has(q, rf"\b{base.STRUCTURE}\b")
    is_glazing = base.has(q, rf"\b{base.GLAZING}\b")
    is_hardware = base.has(q, rf"\b{base.HARDWARE}\b") or base.has(q, r"\b(?:креплен\w*|соединител\w*)\b")
    is_accessory = base.has(q, rf"\b{base.ACCESSORY}\b")

    repair = base.has(q, r"\b(?:ремонт\w*|почин\w*|регулир\w*|не закрыва\w*|не открыва\w*|провис\w*|просел\w*|просела\w*|течет|текут)\b")
    replace = base.has(q, r"\b(?:замена|заменить|поменять|сменить)\b")
    install = base.has(q, r"\b(?:установк\w*|установить|монтаж\w*|монтировать|вставить|поставить)\b") and not base.has(q, r"\bбез установки\b")
    diy = base.has(q, r"\b(?:своими руками|самостоятельн\w*|самому|пошагов\w*|инструкц\w*|как\b|видео)\b")
    review = base.has(q, r"\bотзыв\w*\b")
    price = base.has(q, r"\b(?:цен\w*|стоим\w*|сколько стоит|рассчитать|калькулятор\w*)\b")
    buy = base.has(q, r"\b(?:купить|заказать|продаж\w*|магазин\w*|маркет\b|каталог\w*|под ключ|рассроч\w*|кредит\w*)\b")
    dimensions = base.has(q, r"\b(?:размер\w*|габарит\w*|ширин\w*|высот\w*|площад\w*|толщин\w*)\b")
    selection = base.has(q, r"\b(?:как выбрать|выбирать|выбираем|выбрать|выбор\w*|какие лучше|какой лучше|какая лучше|что лучше|лучшие|рейтинг\w*)\b")
    comparison = base.has(q, r"\b(?:сравн\w*|отлич\w*|разниц\w*|чем отличается|\bvs\b|против)\b") or (base.has(q, r"\bили\b") and (is_window or is_rehau or is_hardware))
    finishing_component = base.has(q, r"\b(?:подоконник\w*|откос\w*|отлив\w*|наличник\w*|нащельник\w*)\b")
    mosquito = base.has(q, r"\b(?:москит\w*|антикошк\w*|антипыл\w*|противомоскит\w*)\b") or (base.has(q, r"\bсетк\w*\b") and (is_window or is_door))

    # Outside categories must win over incidental window words.
    if base.has(q, r"\b(?:штор\w*|жалюз\w*|занавес\w*|карниз\w*|плиссе)\b"):
        return A("OUTSIDE_CURTAINS_BLINDS", "HIGH", "OUTSIDE_CURTAINS_V4", "curtain/blind task is outside the window/glazing business job")
    if base.has(q, r"\b(?:радиатор\w*|батаре\w*|конвектор\w*|отоплен\w*|кондиционер\w*|тепл\w*\s+пол)\b"):
        return A("OUTSIDE_HEATING_HVAC", "HIGH", "OUTSIDE_HEATING_V4", "heating/HVAC equipment is the requested result")

    # Terminology/selection/comparison for hardware and accessories must be resolved
    # before generic window information rules.
    if is_hardware and base.has(q, r"\b(?:как называется|назван\w*|что такое|что входит|шаблон\w*|виды|тип\w*|устройств\w*|конструкц\w*)\b"):
        return A("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_DEFINITION_INFO_V4", "window-hardware terminology/structure information")
    if is_hardware and comparison:
        return A("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_COMPARISON_INFO", "comparison of window-hardware brands/components")
    if is_hardware and selection:
        return A("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_SELECTION_INFO_V4", "window-hardware selection/ranking information")
    if is_accessory and selection:
        return A("WINDOW_ACCESSORY_SELECTION_INFO", "HIGH", "ACCESSORY_SELECTION_INFO_V4", "window-accessory selection information")
    if is_hardware and base.has(q, r"\b(?:магазин\w*|маркет\b|купить|каталог\w*|цен\w*)\b"):
        return A("WINDOW_HARDWARE_SHOPPING", "HIGH", "HARDWARE_SHOPPING_SIGNAL", "hardware shopping/store/price result")

    # Reviews are an information result even when price or installation is also a modifier.
    if review:
        if is_hardware:
            return A("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_REVIEWS_V4", "reviews concern window hardware")
        if is_door:
            return A("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_REVIEWS_V4", "reviews concern PVC doors")
        if is_balcony and is_glazing:
            return A("BALCONY_GLAZING_INFO", "HIGH", "BALCONY_GLAZING_REVIEWS_V4", "reviews concern balcony glazing")
        if is_structure and is_glazing:
            return A("GLAZING_SELECTION_INFO", "MEDIUM", "OUTDOOR_GLAZING_REVIEWS_V4", "reviews concern an outdoor glazing system/service")
        return A("WINDOW_REVIEWS_INFO", "HIGH", "WINDOW_REVIEWS_V4", "review/experience content is requested")

    # Component lifecycle actions precede component-price shopping.
    if finishing_component and (repair or replace):
        if diy:
            return A("WINDOW_FINISHING_DIY_INFO", "HIGH", "FINISHING_COMPONENT_REPAIR_DIY", "DIY repair/replacement of a window finishing component")
        if base.has(q, r"\bподоконник\w*\b"):
            return A("WINDOWSILL_REPAIR_SERVICE", "HIGH", "WINDOWSILL_REPAIR_REPLACEMENT_V4", "professional windowsill repair/replacement")
        return A("WINDOW_FINISHING_SERVICE", "HIGH", "FINISHING_COMPONENT_REPAIR_SERVICE", "professional repair/replacement of slopes/surround components")
    if finishing_component and install:
        if diy:
            return A("WINDOW_FINISHING_DIY_INFO", "HIGH", "FINISHING_COMPONENT_INSTALL_DIY_V4", "DIY installation of a window finishing component")
        return A("WINDOW_FINISHING_SERVICE", "HIGH", "FINISHING_COMPONENT_INSTALL_SERVICE_V4", "professional installation of a window finishing component")

    # Mounting/anchor plates are components; adjective morphology is not an install action.
    if base.has(q, r"\b(?:монтажн\w*|анкерн\w*)\s+пластин\w*\b"):
        return A("WINDOW_HARDWARE_SHOPPING", "HIGH", "MOUNTING_PLATE_COMPONENT_V4", "mounting/anchor plate component")

    # Mosquito-net action priority: install beats an unrelated window-repair token.
    if mosquito:
        if install:
            return A("MOSQUITO_NET_INSTALLATION_SERVICE", "HIGH", "MOSQUITO_INSTALL_V4", "professional mosquito-net installation")
        if repair or replace:
            return A("MOSQUITO_NET_REPAIR_SERVICE", "HIGH", "MOSQUITO_REPAIR_V4", "mosquito-net repair/replacement")
        if selection:
            return A("MOSQUITO_NET_SELECTION_INFO", "HIGH", "MOSQUITO_SELECTION_V4", "mosquito-net selection information")
        return A("MOSQUITO_NET_SHOPPING", "HIGH", "MOSQUITO_SHOPPING_V4", "mosquito-net product shopping")

    # Service actions and their prices take priority over generic product-price rules.
    if repair:
        if is_door and not is_window:
            if diy:
                return A("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_REPAIR_DIY_V4", "DIY PVC-door repair/adjustment information")
            return A("PVC_DOOR_REPAIR_SERVICE", "HIGH", "PVC_DOOR_REPAIR_SERVICE_V4", "professional PVC-door repair/adjustment")
        if diy:
            return A("WINDOW_REPAIR_DIY_INFO", "HIGH", "WINDOW_REPAIR_DIY_V4", "DIY window diagnosis/repair")
        return A("WINDOW_REPAIR_SERVICE", "HIGH", "WINDOW_REPAIR_SERVICE_V4", "professional window repair/adjustment")
    if install:
        if is_glazing and is_balcony:
            # Explicit glazing remains the object-specific glazing service; a phrase
            # saying "installation of a balcony window" is handled below as window installation.
            if base.has(q, rf"\b{base.GLAZING}\b"):
                return V3_CLASSIFY(phrase, source_reason)
        if is_glazing and is_structure:
            return V3_CLASSIFY(phrase, source_reason)
        if is_door and not is_window:
            return A("PVC_DOOR_INSTALLATION_SERVICE", "HIGH", "PVC_DOOR_INSTALLATION_SERVICE_V4", "professional PVC-door installation")
        if is_window or is_pvc or is_rehau or is_aluminium:
            if diy:
                return A("WINDOW_INSTALLATION_DIY_INFO", "HIGH", "WINDOW_INSTALLATION_DIY_V4", "DIY window installation procedure")
            return A("WINDOW_INSTALLATION_SERVICE", "HIGH", "WINDOW_INSTALLATION_SERVICE_V4", "professional window installation")

    # Whole-object replacement after component replacement has been resolved.
    if replace:
        if is_door and not is_window:
            return A("PVC_DOOR_REPLACEMENT_SERVICE", "HIGH", "PVC_DOOR_REPLACEMENT_V4", "whole PVC-door replacement")
        if is_window or is_pvc or is_rehau or is_aluminium:
            return A("WINDOW_REPLACEMENT_SERVICE", "HIGH", "WINDOW_REPLACEMENT_V4", "whole-window replacement")

    # Combined products are created only when the requested object is the window/door
    # bundle itself—not accessories, hardware, repair or installation.
    if is_window and is_door:
        if is_hardware:
            return A("WINDOW_HARDWARE_SHOPPING", "HIGH", "COMBINED_HARDWARE_SHOPPING_V4", "hardware for window/door constructions")
        if is_accessory:
            return A("WINDOW_ACCESSORIES_SHOPPING", "HIGH", "COMBINED_ACCESSORY_SHOPPING_V4", "accessories for window/door constructions")
        return A("WINDOWS_DOORS_COMBINED_COMMERCIAL", "HIGH", "COMBINED_PRODUCT_COMMERCIAL_V4", "combined window-and-door product result")

    # Bare balcony-window product phrases are not silently converted to glazing
    # services. The frozen upstream semantic reason is used only as row-local evidence.
    if is_balcony and is_window and not is_glazing:
        if "POSITIVE_CORE_REHAU_WINDOW_INTENT" in source_reason or is_rehau:
            return A("REHAU_WINDOWS_COMMERCIAL", "HIGH", "BALCONY_WINDOW_PRODUCT_REHAU", "Rehau balcony-window product")
        if "POSITIVE_CORE_ALUMINIUM_WINDOW_INTENT" in source_reason or is_aluminium:
            return A("ALUMINIUM_WINDOWS_COMMERCIAL", "HIGH", "BALCONY_WINDOW_PRODUCT_ALUMINIUM", "aluminium balcony/loggia window product")
        if "POSITIVE_CORE_PVC_WINDOW_INTENT" in source_reason or is_pvc:
            return A("PVC_WINDOWS_COMMERCIAL", "HIGH", "BALCONY_WINDOW_PRODUCT_PVC", "PVC balcony/loggia window product")
        if "POSITIVE_CORE_HOUSE_SERIES_WINDOW_INTENT" in source_reason:
            return A("BALCONY_GLAZING_GENERAL", "MEDIUM", "HOUSE_SERIES_BALCONY_CONTEXT", "house-series balcony window context represents the glazing job")
        if price or buy:
            return A(product_cluster(q, source_reason), "MEDIUM", "BALCONY_WINDOW_PRODUCT_COMMERCIAL", "commercial balcony/loggia window product wording")

    # Dimensions are a factual result and must precede private-house planning.
    if dimensions and (is_window or is_door or is_rehau or is_aluminium or is_panoramic or is_french):
        if is_door and not is_window:
            return A("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_DIMENSIONS_V4", "PVC-door dimensions information")
        return A("WINDOW_DIMENSIONS_INFO", "HIGH", "WINDOW_DIMENSIONS_V4", "window/product dimensions and sizing information")

    # Floor-to-ceiling wording is a panoramic product/form signal unless the row asks dimensions.
    if is_panoramic and is_window and not is_glazing:
        return A("PANORAMIC_WINDOWS_COMMERCIAL", "HIGH", "PANORAMIC_FORM_PRODUCT_V4", "panoramic/floor-to-ceiling window product/form job")

    # Warm vs bundled balcony work: adjective/result wording is warm glazing; explicit
    # conjunction with finishing/insulation is a renovation bundle.
    if is_balcony and is_glazing:
        if base.has(q, r"\b(?:остекл\w*\s+(?:и\s+)?утеплен\w*|остекл\w*\s+(?:и\s+)?отделк\w*|остекл\w*\s+обшивк\w*|ремонт\w*\s+балкон\w*\s+с\s+остекл\w*)\b"):
            return A("BALCONY_RENOVATION_WITH_GLAZING", "HIGH", "BALCONY_RENOVATION_BUNDLE_V4", "glazing explicitly bundled with insulation/finishing/renovation")
        if base.has(q, r"\b(?:тепл\w*|утепленн\w*|под утеплен\w*)\b"):
            return A("BALCONY_GLAZING_WARM", "HIGH", "BALCONY_WARM_GLAZING_V4", "warm/insulated glazing result")

    # Private-house selection morphology missed by earlier literal patterns.
    if selection and base.has(q, r"\b(?:частн\w*|частного)\b") and (is_window or is_rehau or is_pvc or is_aluminium):
        return A("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "HIGH", "PRIVATE_HOUSE_SELECTION_V4", "window choice/planning for a private house")

    # Generic hardware shop navigation should remain shopping, not brand-name information.
    if is_hardware and (buy or price):
        return A("WINDOW_HARDWARE_SHOPPING", "HIGH", "HARDWARE_SHOPPING_V4", "window-hardware shopping result")

    return V3_CLASSIFY(phrase, source_reason)


base.audit_classify = v4_classify


REGRESSIONS: dict[str, tuple[str, str]] = {
    "ремонт пластиковых окон и дверей": ("ASSIGNED", "WINDOW_REPAIR_SERVICE"),
    "цены на ремонт пластиковых окон": ("ASSIGNED", "WINDOW_REPAIR_SERVICE"),
    "цены на монтаж пластиковых окон": ("ASSIGNED", "WINDOW_INSTALLATION_SERVICE"),
    "цены на пластиковые окна отзывы": ("ASSIGNED", "WINDOW_REVIEWS_INFO"),
    "цены на пластиковые окна балконные двери": ("ASSIGNED", "WINDOWS_DOORS_COMBINED_COMMERCIAL"),
    "цены окна алюминиевые профили": ("ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
    "поменять подоконник на пластиковом окне цена": ("ASSIGNED", "WINDOWSILL_REPAIR_SERVICE"),
    "замена откосов на пластиковых окнах цена": ("ASSIGNED", "WINDOW_FINISHING_SERVICE"),
    "монтажная пластина для пластиковых окон rehau grazio": ("ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
    "аксессуары для пластиковых окон и дверей": ("ASSIGNED", "WINDOW_ACCESSORIES_SHOPPING"),
    "оконная и дверная фурнитура": ("ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
    "балконный блок французское окно": ("ASSIGNED", "FRENCH_WINDOWS_COMMERCIAL"),
    "утепленное остекление балконов": ("ASSIGNED", "BALCONY_GLAZING_WARM"),
    "остекление балкона под утепление": ("ASSIGNED", "BALCONY_GLAZING_WARM"),
    "выбираем окна для частного дома": ("ASSIGNED", "PRIVATE_HOUSE_WINDOW_PLANNING_INFO"),
    "окна в пол для частного дома": ("ASSIGNED", "PANORAMIC_WINDOWS_COMMERCIAL"),
    "площадь окна для газовой котельной частного дома": ("ASSIGNED", "WINDOW_DIMENSIONS_INFO"),
    "корпус пластиковый прозрачная дверь": ("ASSIGNED", "OUTSIDE_OTHER"),
    "щит пластиковый прозрачная дверь": ("ASSIGNED", "OUTSIDE_OTHER"),
    "пластиковые окна ремонт установка москитной сетки": ("ASSIGNED", "MOSQUITO_NET_INSTALLATION_SERVICE"),
    "тбм маркет мытищи оконная фурнитура": ("ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
    "как называется оконная фурнитура": ("ASSIGNED", "WINDOW_HARDWARE_INFO"),
    "как называется пластиковая дверь": ("ASSIGNED", "PVC_DOOR_INFO"),
    "accado или vorne фурнитура оконная лучше": ("ASSIGNED", "WINDOW_HARDWARE_INFO"),
    "какая оконная фурнитура лучше рото или зигения": ("ASSIGNED", "WINDOW_HARDWARE_INFO"),
    "балконное окно rehau": ("ASSIGNED", "REHAU_WINDOWS_COMMERCIAL"),
    "балконные окна алюминиевый профиль": ("ASSIGNED", "ALUMINIUM_WINDOWS_COMMERCIAL"),
    "балконные окна пластиковые цены": ("ASSIGNED", "PVC_WINDOWS_COMMERCIAL"),
    "пластиковые окна на лоджию цена с установкой": ("ASSIGNED", "WINDOW_INSTALLATION_SERVICE"),
    "установка пластикового балконного окна цены": ("ASSIGNED", "WINDOW_INSTALLATION_SERVICE"),
    "окна стандартные размеры пластиковые для частного дома": ("ASSIGNED", "WINDOW_DIMENSIONS_INFO"),
    "размер окна для газовой котельной частного дома": ("ASSIGNED", "WINDOW_DIMENSIONS_INFO"),
    "остекление и утепление балкона": ("ASSIGNED", "BALCONY_RENOVATION_WITH_GLAZING"),
    "как выбрать профиль для пластиковых окон правильно": ("ASSIGNED", "WINDOW_HARDWARE_INFO"),
    "установка подоконника на пластиковые окна": ("ASSIGNED", "WINDOW_FINISHING_SERVICE"),
    "установка подоконника на пластиковые окна своими руками": ("ASSIGNED", "WINDOW_FINISHING_DIY_INFO"),
}


def run_regressions() -> None:
    for phrase, expected in REGRESSIONS.items():
        decision = v4_classify(phrase, "REGRESSION")
        actual = (decision.status, decision.cluster_id)
        if actual != expected:
            raise RuntimeError(f"V4 regression failed: {phrase!r}: expected={expected} actual={actual}")
    print(f"PASS3_AUDIT_V4_REGRESSIONS=PASS_{len(REGRESSIONS)}")


if __name__ == "__main__":
    run_regressions()
    base.main()
