#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_FRESH_R1_PASS3_AUDIT as base

ORIGINAL_CLASSIFY = base.audit_classify
base.RULE_VERSION = "PASS3_R1_INDEPENDENT_SEMANTIC_AUDIT_V2"

# Morphology and boundary repairs discovered by reading the complete 2,332-row
# Pass-3 pack. In particular: do not read the commercial phrase "под ключ" as
# a hardware key, and do not read the city form "в Клину" as installation wedges.
base.HARDWARE = (
    r"(?:фурнитур\w*|руч\w*|петл\w*|петель\w*|замок\w*|замк\w*|защелк\w*|задвиж\w*|"
    r"фиксатор\w*|блокиратор\w*|ограничител\w*|микролифт\w*|ножниц\w*|цапф\w*|редуктор\w*|"
    r"ролик\w*|гребенк\w*|ригел\w*|направляющ\w*|штапик\w*|кремон\w*|(?<!под )ключ\w*|"
    r"анкерн\w*\s+пластин\w*|пластин\w*\s+анкерн\w*|монтажн\w*\s+пластин\w*|"
    r"пластин\w*\s+монтажн\w*|саморез\w*|створк\w*|механизм\w*|комплектующ\w*|"
    r"детал\w*|элемент\w*|узл\w*)"
)
base.ACCESSORY = (
    r"(?:аксессуар\w*|уплотн\w*|резин\w*|проклад\w*|стеклопакет\w*|подоконник\w*|"
    r"наличник\w*|нащельник\w*|наклад\w*|отлив\w*|заглушк\w*|герметик\w*|клинь\w*|"
    r"пен\w*|кле\w*|космофен\w*|ремкомплект\w*|запчаст\w*|краск\w*|решетк\w*|"
    r"огражден\w*|ставн\w*|навес\w*|добор\w*|шпрос\w*|панел\w*)"
)


def A(cluster_id: str, confidence: str, rule: str, reason: str) -> base.AuditDecision:
    return base.assigned(cluster_id, confidence, rule, reason)


def v2_classify(phrase: str, source_reason: str) -> base.AuditDecision:
    q = base.norm(phrase)

    # Preserve exact query-local Step-09 evidence as the highest authority.
    if q in base.DIRECT_OVERRIDES:
        return ORIGINAL_CLASSIFY(phrase, source_reason)

    # Resolve the four V1 non-decisive rows from the completed full-row read.
    exact_resolutions = {
        "алюминиевые окна остекление": ("ALUMINIUM_WINDOWS_COMMERCIAL", "aluminium-window product phrase"),
        "остекление панорамное окно": ("PANORAMIC_WINDOWS_COMMERCIAL", "panoramic-window product/form phrase"),
        "остекление раздвижными алюминиевыми окнами": ("GENERAL_GLAZING_SERVICE", "generic glazing service using aluminium sliding windows"),
        "остекление французское окно": ("FRENCH_WINDOWS_COMMERCIAL", "French-window product/form phrase"),
    }
    if q in exact_resolutions:
        cid, reason = exact_resolutions[q]
        return A(cid, "MEDIUM", "FULL_ROW_EXACT_RESOLUTION", reason)

    is_window = base.has(q, rf"\b{base.WINDOW}\b")
    is_door = base.has(q, rf"\b{base.DOOR}\b")
    is_pvc = base.has(q, rf"\b{base.PVC}\b")
    is_aluminium = base.has(q, rf"\b{base.ALUMINIUM}\b")
    is_rehau = base.has(q, rf"\b{base.REHAU}\b")
    is_panoramic = base.has(q, rf"\b{base.PANORAMIC}\b")
    is_french = base.has(q, rf"\b{base.FRENCH}\b")
    is_balcony = base.has(q, rf"\b{base.BALCONY}\b")
    is_glazing = base.has(q, rf"\b{base.GLAZING}\b")
    is_hardware = base.has(q, rf"\b{base.HARDWARE}\b")
    is_accessory = base.has(q, rf"\b{base.ACCESSORY}\b")

    # A positive request to glaze an open balcony is not the negated task
    # "open balcony without glazing".
    if is_glazing and is_balcony and base.has(q, r"\bоткрыт\w*\s+балкон\w*\b") and not base.has(q, r"\bбез остекления\b"):
        return A("BALCONY_GLAZING_GENERAL", "HIGH", "POSITIVE_OPEN_BALCONY_GLAZING", "explicit glazing of an open balcony")

    # Repairing balcony windows remains window repair; it is not a new glazing order.
    repair_word = base.has(q, r"\b(?:ремонт\w*|почин\w*|регулир\w*|не закрыва\w*|не открыва\w*|провис\w*|просел\w*|просела\w*|течет|текут)\b")
    repair_diy = base.has(q, r"\b(?:своими руками|самостоятельн\w*|самому|пошагов\w*|инструкц\w*|видео|как\b)\b")
    if repair_word and is_window and is_balcony and not base.has(q, r"\bремонт\w*\s+(?:балкон\w*|остекл\w*)\b"):
        if repair_diy:
            return A("WINDOW_REPAIR_DIY_INFO", "HIGH", "BALCONY_WINDOW_REPAIR_DIY", "DIY repair of windows located on a balcony/loggia")
        return A("WINDOW_REPAIR_SERVICE", "HIGH", "BALCONY_WINDOW_REPAIR", "professional repair of balcony/loggia windows")

    # Whole balcony-block replacement is a replacement lifecycle job. A bare
    # "balcony block + French window" remains the French-window product/form job.
    if base.has(q, r"\b(?:замена|заменить|поменять)\b.*\bбалконн\w*\s+блок\w*\b") and is_window:
        return A("WINDOW_REPLACEMENT_SERVICE", "HIGH", "BALCONY_BLOCK_REPLACEMENT", "replacement of a balcony block with another window form")
    if base.has(q, r"\bбалконн\w*\s+блок\w*\b") and is_french and is_window:
        return A("FRENCH_WINDOWS_COMMERCIAL", "HIGH", "FRENCH_BALCONY_BLOCK_PRODUCT", "French-window form is the requested product")

    # "Windows made from an aluminium profile" is a window product. Only an
    # independently requested profile/component belongs to hardware shopping.
    if is_window and is_aluminium and (
        base.has(q, r"\bокн\w*\s+из\s+алюминиев\w*\s+профил\w*\b")
        or base.has(q, r"\bалютех\b.*\bокн\w*\b")
        or base.has(q, r"\bалюминиев\w*\s+профил\w*\s+окн\w*\b")
    ):
        return A("ALUMINIUM_WINDOWS_COMMERCIAL", "HIGH", "ALUMINIUM_PROFILE_WINDOW_PRODUCT", "aluminium-profile window product, not a standalone profile")
    if q == "профиль пластиковых окон rehau":
        return A("REHAU_WINDOWS_COMMERCIAL", "MEDIUM", "REHAU_PROFILE_PRODUCT_FAMILY", "Rehau profile-family product phrase")

    # Product-only videos/instructions are technical content, not automatically
    # installation DIY. Glazing videos remain glazing DIY and repair videos remain
    # repair DIY through the base classifier.
    procedural_install = base.has(q, r"\b(?:установ\w*|монтаж\w*|вставить|поставить|снять|заменить|поменять|сделать)\b")
    if base.has(q, r"\b(?:видео|инструкц\w*)\b") and (is_window or is_rehau or is_aluminium or is_pvc) and not is_glazing and not repair_word and not procedural_install:
        if is_door:
            return A("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_MEDIA_INFO", "PVC-door procedural/technical media")
        return A("WINDOW_PRODUCT_TECH_INFO", "HIGH", "WINDOW_PRODUCT_MEDIA_INFO", "product instructions/video without an installation or repair action")

    # Installation-context questions are informational even without the word "как".
    if base.has(q, r"\b(?:зазор\w*\s+при\s+установк\w*|после\s+установк\w*|правильн\w*\s+установк\w*)\b") and is_window:
        return A("WINDOW_INSTALLATION_DIY_INFO", "HIGH", "INSTALLATION_TECH_INFO", "installation method/quality information")

    # More complete Russian selection morphology than the V1 literal phrases.
    selection_question = (
        base.has(q, r"^(?:какие|какой|какая|какое)\b")
        or base.has(q, r"\b(?:какие|какой|какая|какое)\b.*\bлучше\b")
        or base.has(q, r"\b(?:какие бывают|какая бывает|какой бывает|какое бывает)\b")
    )
    if selection_question:
        if base.has(q, r"\b(?:размер\w*|ширин\w*|высот\w*|площад\w*)\b"):
            if is_door:
                return A("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_DIMENSION_QUESTION", "PVC-door sizing question")
            return A("WINDOW_DIMENSIONS_INFO", "HIGH", "WINDOW_DIMENSION_QUESTION", "window sizing question")
        if is_hardware or base.has(q, r"\bпрофил\w*\b"):
            if base.has(q, r"\bчастн\w*\s+дом\w*\b"):
                return A("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "HIGH", "PRIVATE_HOUSE_PROFILE_SELECTION", "profile choice for a private house")
            return A("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_SELECTION_QUESTION", "hardware/profile selection information")
        if is_door:
            return A("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_SELECTION_QUESTION", "PVC-door selection information")
        if is_window or is_rehau or is_aluminium or is_panoramic or is_french:
            if base.has(q, r"\bчастн\w*\s+дом\w*\b"):
                return A("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "HIGH", "PRIVATE_HOUSE_SELECTION", "window choice for a private house")
            return A("WINDOW_SELECTION_INFO", "HIGH", "WINDOW_SELECTION_QUESTION", "window/product selection question")

    # Private-house forms/types/requirements are planning, not a generic product
    # cluster. Explicit dimensions retain the dimensions result.
    private_house = base.has(q, r"\b(?:частн\w*\s+дом\w*|загородн\w*\s+дом\w*|коттедж\w*)\b")
    private_info = base.has(q, r"\b(?:вариант\w*|виды|форма\w*|требован\w*|норм\w*|стандарт\w*|выбрать|выбор\w*)\b")
    if private_house and private_info and not base.has(q, r"\b(?:цен\w*|стоим\w*|купить|заказать)\b"):
        if base.has(q, r"\b(?:размер\w*|ширин\w*|высот\w*|площад\w*)\b"):
            return A("WINDOW_DIMENSIONS_INFO", "HIGH", "PRIVATE_HOUSE_DIMENSIONS", "private-house window dimensions")
        if base.has(q, r"\b(?:фото|дизайн\w*|образц\w*|пример(?:ы|ов)?)\b"):
            return A("GLAZING_DESIGN_INSPIRATION", "HIGH", "PRIVATE_HOUSE_INSPIRATION", "private-house window examples/photos")
        return A("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "HIGH", "PRIVATE_HOUSE_PLANNING_V2", "private-house window planning/requirements")

    # House-series wording is a context modifier, not technical information by itself.
    if is_window and base.has(q, r"\b(?:п\s*44\w*|п\s*3\w*)\b") and not base.has(q, r"\b(?:размер\w*|ширин\w*|высот\w*|установ\w*|остекл\w*)\b"):
        if is_pvc:
            return A("PVC_WINDOWS_COMMERCIAL", "HIGH", "HOUSE_SERIES_PVC_PRODUCT", "house series retained as product context modifier")
        return A("WINDOWS_COMMERCIAL_GENERAL", "HIGH", "HOUSE_SERIES_WINDOW_PRODUCT", "house series retained as product context modifier")

    # Strong form/style phrases remain their product/form tasks before generic tech.
    if is_window and is_french and base.has(q, r"\b(?:раскладк\w*|стил\w*|блок\w*)\b"):
        return A("FRENCH_WINDOWS_COMMERCIAL", "HIGH", "FRENCH_FORM_STYLE_PRODUCT", "French form/style is the primary product distinction")

    # RAL/colors/appearance are technical/property information, not a purchase merely
    # because a material word is present.
    if is_window and is_aluminium and base.has(q, r"\b(?:ral|как выгляд\w*|цвет\w*)\b"):
        return A("WINDOW_PRODUCT_TECH_INFO", "HIGH", "ALUMINIUM_PROPERTY_INFO", "aluminium-window appearance/property information")
    if is_window and is_pvc and base.has(q, r"\bцвет\w*\b"):
        return A("WINDOW_PRODUCT_TECH_INFO", "HIGH", "PVC_WINDOW_PROPERTY_INFO", "PVC-window color/property information")

    # Better/ratings are selection unless the actual phrase is "best prices".
    if base.has(q, r"\bлучшие\s+цены\b"):
        if is_rehau:
            return A("REHAU_WINDOWS_COMMERCIAL", "HIGH", "BEST_PRICE_COMMERCIAL", "commercial price phrase")
        if is_pvc and is_window:
            return A("PVC_WINDOWS_COMMERCIAL", "HIGH", "BEST_PRICE_COMMERCIAL", "commercial price phrase")
    if base.has(q, r"\b(?:лучшие|рейтинг\w*)\b") and (is_window or is_rehau or is_aluminium or is_panoramic or is_french) and not base.has(q, r"\b(?:компани\w*|фирм\w*|ремонт\w*|установк\w*|остекл\w*)\b"):
        return A("WINDOW_SELECTION_INFO", "HIGH", "WINDOW_RANKING_SELECTION", "product ranking/selection result")

    # Door photos are information/browsing, not a bare door purchase.
    if is_door and base.has(q, r"\b(?:фото|дизайн\w*|виды|вариант\w*)\b"):
        return A("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_VISUAL_INFO", "PVC-door visual/type information")

    # Combined windows+doors installation keeps the door-installation task because
    # the frozen taxonomy has no combined installation cluster.
    if is_window and is_door and base.has(q, r"\b(?:установ\w*|монтаж\w*)\b"):
        return A("PVC_DOOR_INSTALLATION_SERVICE", "MEDIUM", "COMBINED_WINDOW_DOOR_INSTALL", "combined installation represented by the closest frozen door-installation task")

    # Finishing/insulation of windows is a finishing service even without an extra
    # buy/install verb.
    if is_window and not is_balcony and base.has(q, r"\b(?:отделк\w*|утеплен\w*|утеплить|покраск\w*)\b"):
        return A("WINDOW_FINISHING_SERVICE", "HIGH", "WINDOW_FINISHING_V2", "professional window finishing/insulation/painting result")

    # Cleaning after construction/repair is care, not another repair service.
    if is_window and base.has(q, r"\b(?:отмыть|очистить|мыть|мойк\w*)\b") and not base.has(q, r"\b(?:ремонтировать|починить)\b"):
        return A("WINDOW_CARE_INFO", "HIGH", "WINDOW_CARE_CLEANING", "window cleaning/care information")

    # Generic "как ... сделать/снять/заменить" word orders are procedural even when
    # the verb is separated from "как" by several words.
    if is_window and base.has(q, r"\bкак\b.*\b(?:сделать|установить|вставить|поставить|снять|заменить|поменять)\b"):
        return A("WINDOW_INSTALLATION_DIY_INFO", "HIGH", "WINDOW_PROCEDURAL_WORD_ORDER", "DIY window installation/replacement procedure")

    # Bare assembly/drilling concerns technology/procedure, not a product purchase.
    if is_window and base.has(q, r"\b(?:сборк\w*|сверлен\w*)\b"):
        return A("WINDOW_PRODUCT_TECH_INFO", "HIGH", "WINDOW_CONSTRUCTION_TECH", "window assembly/drilling information")

    # "Что входит" and templates are hardware information.
    if is_hardware and base.has(q, r"\b(?:что входит|шаблон\w*)\b"):
        return A("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_CONTENT_INFO", "hardware composition/template information")

    # Additional repair morphology omitted by V1 (регулируем/регулировать).
    if base.has(q, r"\bрегулир\w*\b"):
        if is_door:
            return A("PVC_DOOR_REPAIR_SERVICE", "HIGH", "PVC_DOOR_REGULATION", "PVC-door adjustment service")
        if is_window or is_rehau or is_aluminium:
            return A("WINDOW_REPAIR_SERVICE", "HIGH", "WINDOW_REGULATION", "window adjustment service")

    return ORIGINAL_CLASSIFY(phrase, source_reason)


base.audit_classify = v2_classify

if __name__ == "__main__":
    base.main()
