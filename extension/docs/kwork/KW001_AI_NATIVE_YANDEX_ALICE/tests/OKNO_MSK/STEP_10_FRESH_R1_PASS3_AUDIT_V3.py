#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_FRESH_R1_PASS3_AUDIT_V2 as v2

base = v2.base
V2_CLASSIFY = v2.v2_classify
base.RULE_VERSION = "PASS3_R1_INDEPENDENT_SEMANTIC_AUDIT_V3"


def A(cluster_id: str, confidence: str, rule: str, reason: str) -> base.AuditDecision:
    return base.assigned(cluster_id, confidence, rule, reason)


def S(rule: str, reason: str) -> base.AuditDecision:
    return base.search_required(rule, reason, True)


def commercial_product_cluster(q: str) -> str:
    if base.has(q, rf"\b{base.REHAU}\b"):
        return "REHAU_WINDOWS_COMMERCIAL"
    if base.has(q, rf"\b{base.PANORAMIC}\b"):
        return "PANORAMIC_WINDOWS_COMMERCIAL"
    if base.has(q, rf"\b{base.FRENCH}\b"):
        return "FRENCH_WINDOWS_COMMERCIAL"
    if base.has(q, rf"\b{base.ALUMINIUM}\b"):
        return "ALUMINIUM_WINDOWS_COMMERCIAL"
    if base.has(q, rf"\b{base.PVC}\b"):
        return "PVC_WINDOWS_COMMERCIAL"
    return "WINDOWS_COMMERCIAL_GENERAL"


# Query-local and full-row exact resolutions. These are intentionally explicit:
# they prevent broad lexical rules from changing a reviewed edge case.
EXACT_ASSIGNED_RAW: dict[str, tuple[str, str, str]] = {
    "крепление для пластиковых окон": ("WINDOW_HARDWARE_SHOPPING", "HARDWARE_FASTENING", "window fastening/component product"),
    "алюминиевые рамы для окон": ("WINDOW_HARDWARE_SHOPPING", "WINDOW_FRAME_COMPONENT", "aluminium window frames requested as a component"),
    "окно алюминиевое roto": ("WINDOW_HARDWARE_SHOPPING", "HARDWARE_BRAND_EDGE", "Roto denotes window hardware in this component-oriented edge phrase"),
    "лучшие компании по остеклению балконов": ("BALCONY_GLAZING_GENERAL", "BALCONY_PROVIDER_SELECTION", "provider selection remains a balcony-glazing service job"),
    "остекление балконов в москве рейтинг": ("BALCONY_GLAZING_GENERAL", "BALCONY_PROVIDER_SELECTION", "service-provider ranking remains a balcony-glazing service job"),
    "ремонт балконных пластиковых окон": ("WINDOW_REPAIR_SERVICE", "BALCONY_WINDOW_REPAIR_V3", "repair of windows located on a balcony"),
    "окна система rehau": ("REHAU_WINDOWS_COMMERCIAL", "REHAU_SYSTEM_PRODUCT", "bare Rehau system phrase is a product-family job"),
    "соединители под 45 градусов для окон rehau": ("WINDOW_HARDWARE_SHOPPING", "WINDOW_CONNECTOR_COMPONENT", "window connector is a hardware component"),
    "окно французской гостиной": ("GLAZING_DESIGN_INSPIRATION", "FRENCH_ROOM_INSPIRATION", "room/style wording seeks an example or design result"),
    "французский профиль окна": ("WINDOW_HARDWARE_SHOPPING", "FRENCH_PROFILE_COMPONENT", "window profile is a component rather than a French-window product"),
    "окна на балкон сапожок п 44": ("BALCONY_GLAZING_GENERAL", "HOUSE_SERIES_BALCONY_GLAZING", "P-44 balcony-form context modifies the balcony glazing job"),
    "остекление балкона без крыши": ("BALCONY_GLAZING_GENERAL", "NEGATED_ROOF_BALCONY_GLAZING", "explicit absence of a roof must not create the roof-service task"),
    "французские окна в интерьере": ("GLAZING_DESIGN_INSPIRATION", "FRENCH_INTERIOR_INSPIRATION", "interior examples/design are the expected result"),
    "окно для вентиляции в частном доме": ("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "PRIVATE_HOUSE_VENTILATION_PLANNING", "window planning for a private-house ventilation requirement"),
    "окна двери rehau": ("WINDOWS_DOORS_COMBINED_COMMERCIAL", "REHAU_COMBINED_PRODUCTS", "combined window-and-door result dominates the brand modifier"),
    "лучшие пластиковые двери": ("PVC_DOOR_INFO", "PVC_DOOR_SELECTION_V3", "PVC-door selection information"),
    "регулировка пластиковых дверей своими руками": ("PVC_DOOR_INFO", "PVC_DOOR_DIY_ADJUSTMENT", "DIY PVC-door adjustment information"),
    "цена отливов на пластиковые окна": ("WINDOW_ACCESSORIES_SHOPPING", "FLASHING_COMPONENT_PRICE", "component price without an installation action"),
    "установка французского окна вместо балконного блока": ("WINDOW_REPLACEMENT_SERVICE", "FRENCH_BALCONY_BLOCK_REPLACEMENT", "installation instead of a balcony block is a replacement lifecycle job"),
    "французские окна это какие": ("WINDOW_PRODUCT_TECH_INFO", "FRENCH_DEFINITION_INFO", "definition/explanation of French windows"),
    "лучшие окна для частного дома": ("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "PRIVATE_HOUSE_RANKING_SELECTION", "selection/planning for a private house"),
    "ремонт подоконника пластикового окна своими руками": ("WINDOW_FINISHING_DIY_INFO", "WINDOWSILL_DIY_FINISHING", "DIY windowsill repair belongs to finishing DIY"),
    "запчасти оконной фурнитуры": ("WINDOW_HARDWARE_SHOPPING", "HARDWARE_SPARE_PARTS", "spare parts for window hardware remain hardware shopping"),
    "установка отлива на пластиковое окно своими руками": ("WINDOW_FINISHING_DIY_INFO", "FLASHING_INSTALL_DIY", "DIY window flashing installation"),
    "что входит в комплект оконной фурнитуры": ("WINDOW_HARDWARE_INFO", "HARDWARE_CONTENT_INFO_V3", "hardware kit composition information"),
    "шторы на пластиковые окна без сверления": ("OUTSIDE_CURTAINS_BLINDS", "OUTSIDE_CURTAINS_V3", "curtain/blind result remains outside even when drilling is mentioned"),
    "от комаров на окна пластиковые": ("MOSQUITO_NET_SHOPPING", "IMPLICIT_MOSQUITO_NET", "implicit mosquito-protection net product"),
    "варианты остекления веранды в частном доме": ("GLAZING_SELECTION_INFO", "OUTDOOR_GLAZING_SELECTION_V3", "explicit veranda glazing system selection dominates private-house context"),
    "пластиковые навесные двери": ("PVC_DOORS_COMMERCIAL", "HINGED_PVC_DOORS", "навесные describes hinged doors, not a separate awning component"),
    "оконная фурнитура для пластиковых окон рейтинг": ("WINDOW_HARDWARE_INFO", "HARDWARE_RANKING_INFO", "window-hardware ranking/selection information"),
    "рейтинг оконной фурнитуры": ("WINDOW_HARDWARE_INFO", "HARDWARE_RANKING_INFO", "window-hardware ranking/selection information"),
    "уплотнитель для пластиковых окон rehau какой лучше": ("WINDOW_ACCESSORY_SELECTION_INFO", "SEAL_SELECTION_INFO", "seal/accessory selection information"),
    "какой профиль окон лучше veka или rehau": ("WINDOW_COMPARISON_INFO", "PROFILE_BRAND_COMPARISON", "explicit comparison of two window profile brands"),
    "установка подоконника на пластиковые окна своими руками": ("WINDOW_FINISHING_DIY_INFO", "WINDOWSILL_INSTALL_DIY", "DIY windowsill installation"),
    "окна и дверь на балкон пластиковые цена": ("WINDOWS_DOORS_COMBINED_COMMERCIAL", "BALCONY_BLOCK_COMBINED_PRODUCT", "window-and-door product bundle for a balcony"),
    "установка ограничителя на пластиковые окна": ("WINDOW_INSTALLATION_SERVICE", "HARDWARE_INSTALL_SERVICE", "installation action dominates component shopping"),
    "установка створки пластикового окна": ("WINDOW_INSTALLATION_SERVICE", "HARDWARE_INSTALL_SERVICE", "installation action dominates component shopping"),
    "открытое пластиковое окно": ("WINDOW_PRODUCT_TECH_INFO", "WINDOW_STATE_INFO", "window state/operation information"),
    "открытое панорамное окно": ("WINDOW_PRODUCT_TECH_INFO", "WINDOW_STATE_INFO", "window state/operation information"),
}
EXACT_ASSIGNED = {base.norm(k): v for k, v in EXACT_ASSIGNED_RAW.items()}

EXACT_SEARCH_REQUIRED = {
    base.norm(x)
    for x in {
        "пластиковое окно закрыто",
        "пластиковое окно внутри",
        "пластиковое окно снаружи",
        "панорамное окно снаружи",
    }
}


def v3_classify(phrase: str, source_reason: str) -> base.AuditDecision:
    q = base.norm(phrase)

    # Exact Step-09 evidence remains immutable and query-local.
    if q in base.DIRECT_OVERRIDES:
        return V2_CLASSIFY(phrase, source_reason)

    if q in EXACT_ASSIGNED:
        cluster_id, rule, reason = EXACT_ASSIGNED[q]
        return A(cluster_id, "HIGH", rule, reason)
    if q in EXACT_SEARCH_REQUIRED:
        return S("STATE_FRAGMENT_SEARCH_REQUIRED", "standalone state/location fragment does not establish a stable user task")

    is_window = base.has(q, rf"\b{base.WINDOW}\b")
    is_door = base.has(q, rf"\b{base.DOOR}\b")
    is_pvc = base.has(q, rf"\b{base.PVC}\b")
    is_aluminium = base.has(q, rf"\b{base.ALUMINIUM}\b")
    is_rehau = base.has(q, rf"\b{base.REHAU}\b")
    is_panoramic = base.has(q, rf"\b{base.PANORAMIC}\b")
    is_french = base.has(q, rf"\b{base.FRENCH}\b")
    is_balcony = base.has(q, rf"\b{base.BALCONY}\b")
    is_structure = base.has(q, rf"\b{base.STRUCTURE}\b")
    is_glazing = base.has(q, rf"\b{base.GLAZING}\b")
    is_hardware = base.has(q, rf"\b{base.HARDWARE}\b") or base.has(q, r"\b(?:креплен\w*|соединител\w*)\b")
    is_accessory = base.has(q, rf"\b{base.ACCESSORY}\b")

    has_price = base.has(q, r"\b(?:цен\w*|стоим\w*|сколько стоит|рассчитать|калькулятор\w*)\b")
    has_buy = base.has(q, r"\b(?:купить|заказать|продаж\w*|магазин\w*|каталог\w*|под ключ|рассроч\w*|кредит\w*)\b")
    has_install = base.has(q, r"\b(?:установ\w*|монтаж\w*|вставить|поставить)\b") and not base.has(q, r"\bбез установки\b")
    has_repair = base.has(q, r"\b(?:ремонт\w*|почин\w*|регулир\w*|не закрыва\w*|не открыва\w*|провис\w*|просел\w*|просела\w*|течет|текут)\b")
    has_diy = base.has(q, r"\b(?:своими руками|самостоятельн\w*|самому|пошагов\w*|инструкц\w*|как\b|видео)\b")
    has_photo = base.has(q, r"\b(?:фото|дизайн\w*|интерьер\w*|оформлен\w*|образц\w*|пример(?:ы|ов)?)\b")
    private_house = base.has(q, r"\b(?:частн\w*\s+дом\w*|загородн\w*\s+дом\w*|коттедж\w*)\b")

    # Stable outside families must win over incidental words such as drilling.
    if base.has(q, r"\b(?:штор\w*|жалюз\w*|занавес\w*|карниз\w*|плиссе)\b"):
        return A("OUTSIDE_CURTAINS_BLINDS", "HIGH", "OUTSIDE_CURTAINS_V3", "curtain/blind result is outside the core window/glazing task")
    if base.has(q, r"\b(?:радиатор\w*|батаре\w*|конвектор\w*|отоплен\w*|кондиционер\w*|тепл\w*\s+пол)\b"):
        return A("OUTSIDE_HEATING_HVAC", "HIGH", "OUTSIDE_HEATING_V3", "heating/HVAC equipment is the requested result")

    # Explicit comparison has priority over the generic interrogative "какие".
    comparison = base.has(q, r"\b(?:сравн\w*|отлич\w*|разниц\w*|чем отличается|\bvs\b|против)\b") or (
        base.has(q, r"\bили\b") and (is_window or is_rehau or is_aluminium or is_pvc)
    )
    if comparison and (is_window or is_rehau or is_aluminium or is_pvc or is_panoramic or is_french):
        return A("WINDOW_COMPARISON_INFO", "HIGH", "WINDOW_COMPARISON_V3", "explicit product/brand/material comparison")

    # A price question is commercial, not selection merely because it begins with
    # "какие". Component and service objects keep their own task families.
    if base.has(q, r"\bкакие\s+цены\b") or base.has(q, r"^цены?\b"):
        if base.has(q, r"\b(?:москит\w*|антикошк\w*|антипыл\w*|сетк\w*)\b") and (is_window or is_door):
            return A("MOSQUITO_NET_SHOPPING", "HIGH", "MOSQUITO_PRICE", "mosquito-net product price")
        if is_hardware:
            return A("WINDOW_HARDWARE_SHOPPING", "HIGH", "HARDWARE_PRICE", "window-hardware price")
        if is_accessory:
            return A("WINDOW_ACCESSORIES_SHOPPING", "HIGH", "ACCESSORY_PRICE", "window-accessory price")
        if is_balcony and (is_glazing or is_window):
            return A("BALCONY_GLAZING_GENERAL", "HIGH", "BALCONY_GLAZING_PRICE", "balcony-glazing commercial service price")
        if is_structure and is_glazing:
            return A("OUTDOOR_STRUCTURE_GLAZING", "HIGH", "OUTDOOR_GLAZING_PRICE", "outdoor-structure glazing service price")
        if is_door:
            return A("PVC_DOORS_COMMERCIAL", "HIGH", "PVC_DOOR_PRICE", "PVC-door commercial price")
        if is_window or is_rehau or is_aluminium or is_pvc or is_panoramic or is_french:
            return A(commercial_product_cluster(q), "HIGH", "WINDOW_PRICE_COMMERCIAL", "window-product commercial price")

    # Explicit glazing task boundaries beat generic private-house rules.
    if is_structure and is_glazing and base.has(q, r"\b(?:вариант\w*|виды|плюсы и минусы|материал\w*|толщин\w*|конструкц\w*)\b"):
        return A("GLAZING_SELECTION_INFO", "HIGH", "OUTDOOR_GLAZING_SELECTION_V3", "outdoor glazing type/system selection")

    # Reviews/rankings of service providers remain the service task. Product and
    # component rankings remain informational selection tasks.
    provider_words = base.has(q, r"\b(?:компани\w*|фирм\w*|мастер\w*|служб\w*|подрядчик\w*)\b")
    ranking = base.has(q, r"\b(?:лучшие|рейтинг\w*)\b")
    if (provider_words or ranking) and is_balcony and (is_glazing or is_window) and not base.has(q, r"\b(?:виды|варианты|конструкц\w*)\b"):
        return A("BALCONY_GLAZING_GENERAL", "HIGH", "BALCONY_PROVIDER_SELECTION", "service-provider selection is part of the glazing service job")
    if ranking and is_hardware:
        return A("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_RANKING_INFO", "window-hardware ranking/selection")
    if ranking and is_door:
        return A("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_RANKING_INFO", "PVC-door ranking/selection")
    if ranking and private_house:
        return A("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "HIGH", "PRIVATE_HOUSE_RANKING_SELECTION", "window selection/planning for a private house")

    # Accessory/hardware selection must not collapse into generic window selection.
    selection = base.has(q, r"\b(?:как выбрать|выбрать|выбор\w*|какие лучше|какой лучше|какая лучше|что лучше|лучшие|рейтинг\w*)\b")
    if selection and is_hardware:
        return A("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_SELECTION_V3", "window-hardware selection information")
    if selection and is_accessory:
        return A("WINDOW_ACCESSORY_SELECTION_INFO", "HIGH", "ACCESSORY_SELECTION_V3", "window-accessory selection information")

    # Component installation/repair lifecycle actions have priority over shopping.
    finishing_component = base.has(q, r"\b(?:подоконник\w*|отлив\w*|откос\w*|наличник\w*|нащельник\w*)\b")
    if finishing_component and has_install:
        if has_diy:
            return A("WINDOW_FINISHING_DIY_INFO", "HIGH", "FINISHING_COMPONENT_INSTALL_DIY", "DIY installation of a window finishing component")
        return A("WINDOW_FINISHING_SERVICE", "HIGH", "FINISHING_COMPONENT_INSTALL_SERVICE", "professional installation of a window finishing component")
    if is_hardware and has_install:
        return A("WINDOW_INSTALLATION_SERVICE", "MEDIUM", "HARDWARE_INSTALL_SERVICE_V3", "installation action dominates component shopping")
    if base.has(q, r"\b(?:соединител\w*|креплен\w*)\b") and not has_install:
        return A("WINDOW_HARDWARE_SHOPPING", "HIGH", "WINDOW_CONNECTION_COMPONENT", "window fastening/connector component")

    # An adjective meaning hinged doors must not be read as an awning accessory.
    if is_door and base.has(q, r"\bнавесн\w*\s+двер\w*\b"):
        return A("PVC_DOORS_COMMERCIAL", "HIGH", "HINGED_PVC_DOORS", "hinged PVC-door product")

    # Window/door multi-object product bundles dominate material and brand modifiers.
    balcony_block = base.has(q, r"\bбалконн\w*\s+блок\w*\b")
    if (is_window and is_door) or balcony_block:
        if base.has(q, r"\b(?:замена|заменить|поменять|вместо)\b"):
            return A("WINDOW_REPLACEMENT_SERVICE", "HIGH", "COMBINED_BLOCK_REPLACEMENT", "replacement of a window-and-door/balcony block")
        if has_install:
            return A("PVC_DOOR_INSTALLATION_SERVICE", "MEDIUM", "COMBINED_BLOCK_INSTALLATION", "combined window-and-door installation represented by the frozen door-installation task")
        return A("WINDOWS_DOORS_COMBINED_COMMERCIAL", "HIGH", "COMBINED_WINDOW_DOOR_PRODUCT_V3", "combined window-and-door product result")

    # Repair of the window object remains repair even when the location is a balcony.
    if has_repair and is_window and is_balcony and not base.has(q, r"\bремонт\w*\s+балкон\w*\b"):
        if has_diy:
            return A("WINDOW_REPAIR_DIY_INFO", "HIGH", "BALCONY_WINDOW_REPAIR_DIY_V3", "DIY repair of balcony-located windows")
        return A("WINDOW_REPAIR_SERVICE", "HIGH", "BALCONY_WINDOW_REPAIR_V3", "professional repair of balcony-located windows")

    # Private-house room/application phrases without a transaction cue are planning.
    private_application = base.has(q, r"\b(?:котельн\w*|санузл\w*|ванн\w*|вентиляц\w*|кухн\w*)\b")
    if private_house and (private_application or base.has(q, r"\b(?:требован\w*|норм\w*|стандарт\w*|вариант\w*|виды|форма\w*)\b")) and not (has_buy or has_price or has_install):
        if has_photo:
            return A("GLAZING_DESIGN_INSPIRATION", "HIGH", "PRIVATE_HOUSE_INSPIRATION_V3", "private-house window examples/photos")
        return A("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "HIGH", "PRIVATE_HOUSE_APPLICATION_PLANNING", "private-house window planning/requirements")

    # Definition/operation phrases beat product form clusters.
    definition = base.has(q, r"\b(?:что значит|что такое|это какие|как называется|название|суть)\b")
    if definition and (is_window or is_rehau or is_panoramic or is_french or is_aluminium or is_pvc):
        if base.has(q, r"\bдом\w*\b") and (is_panoramic or is_french):
            return A("OUTSIDE_REAL_ESTATE_ARCHITECTURE", "HIGH", "BUILDING_DEFINITION_OUTSIDE", "building/architecture term is the requested result")
        return A("WINDOW_PRODUCT_TECH_INFO", "HIGH", "WINDOW_DEFINITION_INFO_V3", "window/product definition or terminology information")

    # Design/interior/form examples remain inspiration unless a price/buy/service
    # action is explicit.
    if has_photo and not (has_price or has_buy or has_install or has_repair) and (is_window or is_glazing or is_panoramic or is_french):
        return A("GLAZING_DESIGN_INSPIRATION", "HIGH", "WINDOW_DESIGN_INSPIRATION_V3", "window/glazing design or interior examples")

    # Component price without install/repair is shopping, not finishing service.
    if finishing_component and (has_price or has_buy) and not (has_install or has_repair):
        return A("WINDOW_ACCESSORIES_SHOPPING", "HIGH", "FINISHING_COMPONENT_SHOPPING", "window finishing component product/price")

    # Rehau bare product-system wording is commercial; explicit technical cues are
    # still handled by V2.
    if is_rehau and is_window and base.has(q, r"\bсистем\w*\b") and not base.has(q, r"\b(?:что|как|виды|режим\w*|конструкц\w*|цвет\w*)\b"):
        return A("REHAU_WINDOWS_COMMERCIAL", "HIGH", "REHAU_SYSTEM_PRODUCT", "bare Rehau product-system phrase")

    # Installation instead of an existing balcony block is replacement.
    if is_french and is_window and has_install and base.has(q, r"\bвместо\s+балконн\w*\s+блок\w*\b"):
        return A("WINDOW_REPLACEMENT_SERVICE", "HIGH", "FRENCH_BALCONY_BLOCK_REPLACEMENT", "replacement of a balcony block with a French window")

    # Implicit mosquito protection wording.
    if base.has(q, r"\bот комар\w*\b") and (is_window or is_door):
        return A("MOSQUITO_NET_SHOPPING", "HIGH", "IMPLICIT_MOSQUITO_NET", "implicit mosquito-protection net product")

    # A French-profile phrase is component intent, not a French-window form job.
    if is_french and base.has(q, r"\bпрофил\w*\b"):
        if selection or definition:
            return A("WINDOW_HARDWARE_INFO", "HIGH", "FRENCH_PROFILE_INFO", "window-profile information")
        return A("WINDOW_HARDWARE_SHOPPING", "HIGH", "FRENCH_PROFILE_COMPONENT", "window-profile component shopping")

    # Repair spare parts for hardware remain hardware, not generic repair material.
    if base.has(q, r"\bзапчаст\w*\b") and base.has(q, r"\bфурнитур\w*\b"):
        return A("WINDOW_HARDWARE_SHOPPING", "HIGH", "HARDWARE_SPARE_PARTS", "spare parts for window hardware")

    # Explicit "какие цены" was handled above; ordinary selection now follows V2.
    return V2_CLASSIFY(phrase, source_reason)


base.audit_classify = v3_classify


REGRESSION_CASES: dict[str, tuple[str, str]] = {
    "какие цены на пластиковые окна": ("ASSIGNED", "PVC_WINDOWS_COMMERCIAL"),
    "какие окна лучше veka или rehau": ("ASSIGNED", "WINDOW_COMPARISON_INFO"),
    "какие окна пластиковые или алюминиевые": ("ASSIGNED", "WINDOW_COMPARISON_INFO"),
    "крепление для пластиковых окон": ("ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
    "алюминиевые рамы для окон": ("ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
    "лучшие компании по остеклению балконов": ("ASSIGNED", "BALCONY_GLAZING_GENERAL"),
    "ремонт балконных пластиковых окон": ("ASSIGNED", "WINDOW_REPAIR_SERVICE"),
    "соединители под 45 градусов для окон rehau": ("ASSIGNED", "WINDOW_HARDWARE_SHOPPING"),
    "установка подоконника на пластиковые окна": ("ASSIGNED", "WINDOW_FINISHING_SERVICE"),
    "установка подоконника на пластиковые окна своими руками": ("ASSIGNED", "WINDOW_FINISHING_DIY_INFO"),
    "установка ограничителя на пластиковые окна": ("ASSIGNED", "WINDOW_INSTALLATION_SERVICE"),
    "пластиковые навесные двери": ("ASSIGNED", "PVC_DOORS_COMMERCIAL"),
    "французские окна в интерьере": ("ASSIGNED", "GLAZING_DESIGN_INSPIRATION"),
    "французские окна это какие": ("ASSIGNED", "WINDOW_PRODUCT_TECH_INFO"),
    "окна двери rehau": ("ASSIGNED", "WINDOWS_DOORS_COMBINED_COMMERCIAL"),
    "лучшие пластиковые двери": ("ASSIGNED", "PVC_DOOR_INFO"),
    "регулировка пластиковых дверей своими руками": ("ASSIGNED", "PVC_DOOR_INFO"),
    "уплотнитель для пластиковых окон rehau какой лучше": ("ASSIGNED", "WINDOW_ACCESSORY_SELECTION_INFO"),
    "какой профиль окон лучше veka или rehau": ("ASSIGNED", "WINDOW_COMPARISON_INFO"),
    "от комаров на окна пластиковые": ("ASSIGNED", "MOSQUITO_NET_SHOPPING"),
    "варианты остекления веранды в частном доме": ("ASSIGNED", "GLAZING_SELECTION_INFO"),
    "остекление балкона без крыши": ("ASSIGNED", "BALCONY_GLAZING_GENERAL"),
    "окно для вентиляции в частном доме": ("ASSIGNED", "PRIVATE_HOUSE_WINDOW_PLANNING_INFO"),
    "цена отливов на пластиковые окна": ("ASSIGNED", "WINDOW_ACCESSORIES_SHOPPING"),
    "установка французского окна вместо балконного блока": ("ASSIGNED", "WINDOW_REPLACEMENT_SERVICE"),
    "шторы на пластиковые окна без сверления": ("ASSIGNED", "OUTSIDE_CURTAINS_BLINDS"),
}


def run_regressions() -> None:
    for phrase, expected in REGRESSION_CASES.items():
        decision = v3_classify(phrase, "REGRESSION")
        actual = (decision.status, decision.cluster_id)
        if actual != expected:
            raise RuntimeError(f"V3 regression failed: {phrase!r}: expected={expected} actual={actual}")
    print(f"PASS3_AUDIT_V3_REGRESSIONS=PASS_{len(REGRESSION_CASES)}")


if __name__ == "__main__":
    run_regressions()
    base.main()
