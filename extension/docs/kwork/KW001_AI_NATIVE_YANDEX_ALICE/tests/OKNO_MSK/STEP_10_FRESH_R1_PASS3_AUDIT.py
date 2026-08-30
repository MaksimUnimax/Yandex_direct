#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSIGNMENT = ROOT / "STEP_10_FRESH_R1_ASSIGNMENT.tsv"
REVIEW_PACK = ROOT / "STEP_10_FRESH_R1_PASS3_REVIEW_PACK.tsv"
TAXONOMY = ROOT / "STEP_10_FRESH_R1_TAXONOMY.tsv"
DIRECT = ROOT / "STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv"
OUT_REVIEW = ROOT / "STEP_10_FRESH_R1_PASS3_FULL_REVIEW.tsv"
OUT_ERRORS = ROOT / "STEP_10_FRESH_R1_PASS3_ERROR_LEDGER.tsv"
OUT_TRANSITIONS = ROOT / "STEP_10_FRESH_R1_PASS3_ERROR_TRANSITIONS.tsv"
OUT_QA = ROOT / "STEP_10_FRESH_R1_PASS3_QA.json"

ACTIVE_DISPOSITIONS = {"CORE_CANDIDATE", "REVIEW_SEARCH"}
RULE_VERSION = "PASS3_R1_INDEPENDENT_SEMANTIC_AUDIT_V1"

WINDOW = r"(?:окн\w*|окон\w*)"
DOOR = r"двер\w*"
PVC = r"(?:пластиков\w*|пвх|металлопластиков\w*)"
ALUMINIUM = r"алюмини\w*"
WOOD = r"(?:деревянн\w*|дерев\w*|брус\w*)"
REHAU = r"(?:rehau|рехау)"
PANORAMIC = r"панорамн\w*"
FRENCH = r"французск\w*"
BALCONY = r"(?:балкон\w*|лоджи\w*)"
STRUCTURE = r"(?:веранд\w*|террас\w*|беседк\w*|крыльц\w*)"
GLAZING = r"(?:остекл\w*|застекл\w*)"

HARDWARE = (
    r"(?:фурнитур\w*|ручк\w*|петл\w*|замок\w*|замк\w*|защелк\w*|фиксатор\w*|"
    r"блокиратор\w*|ограничител\w*|микролифт\w*|ножниц\w*|цапф\w*|редуктор\w*|"
    r"ролик\w*|гребенк\w*|ригел\w*|направляющ\w*|штапик\w*|кремон\w*|ключ\w*|"
    r"анкерн\w*\s+пластин\w*|монтажн\w*\s+пластин\w*|саморез\w*|створк\w*|"
    r"механизм\w*|комплектующ\w*|детал\w*|элемент\w*|узл\w*)"
)
ACCESSORY = (
    r"(?:аксессуар\w*|уплотнител\w*|резинк\w*|прокладк\w*|стеклопакет\w*|"
    r"подоконник\w*|наличник\w*|нащельник\w*|отлив\w*|заглушк\w*|герметик\w*|"
    r"клин\w*|пен\w*|кле\w*|космофен\w*|ремкомплект\w*|запчаст\w*|краск\w*|"
    r"решетк\w*|ставн\w*|панел\w*)"
)


@dataclass(frozen=True)
class AuditDecision:
    status: str
    cluster_id: str
    confidence: str
    rule: str
    reason: str
    decisive: bool = True


def norm(value: str) -> str:
    value = value.lower().replace("ё", "е").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", value).strip()


def has(q: str, pattern: str) -> bool:
    return re.search(pattern, q, re.I) is not None


def assigned(cluster_id: str, confidence: str, rule: str, reason: str) -> AuditDecision:
    return AuditDecision("ASSIGNED", cluster_id, confidence, rule, reason, True)


def search_required(rule: str, reason: str, decisive: bool = True) -> AuditDecision:
    return AuditDecision("SEARCH_REQUIRED", "", "LOW", rule, reason, decisive)


# Query-local Step-09 evidence. These mappings apply only to the exact probed query.
# They are deliberately explicit so no direct SERP conclusion is transferred to an
# unprobed phrase merely because it looks similar.
DIRECT_OVERRIDES_RAW = {
    "аксессуары для пластиковых окон": "WINDOW_ACCESSORIES_SHOPPING",
    "алюминиевые окна fapim": "WINDOW_HARDWARE_SHOPPING",
    "балкон без остекления": "OPEN_BALCONY_FINISHING",
    "безрамное остекление веранды": "OUTDOOR_STRUCTURE_GLAZING",
    "демонтаж остекления балкона": "WINDOW_DEMOLITION_SERVICE",
    "дерево алюминиевые окна": "TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL",
    "деревянные окна для частного дома": "WOOD_WINDOWS_COMMERCIAL",
    "дом с панорамными окнами": "OUTSIDE_REAL_ESTATE_ARCHITECTURE",
    "как выбрать шторы на пластиковые окна": "OUTSIDE_CURTAINS_BLINDS",
    "комплект для окна алюминиевые": "WINDOW_HARDWARE_SHOPPING",
    "крыльцо для частного дома окна": "OUTDOOR_STRUCTURE_GLAZING",
    "окна rehau 70": "REHAU_WINDOWS_COMMERCIAL",
    "окна rehau kbe": "WINDOW_COMPARISON_INFO",
    "окна rehau официальный": "NAVIGATION_BRAND_SITE",
    "окна rehau провисли": "WINDOW_REPAIR_SERVICE",
    "окна пластиковые москитная": "MOSQUITO_NET_SHOPPING",
    "окна стеклопакеты rehau": "REHAU_WINDOWS_COMMERCIAL",
    "оконная фурнитура отзывы": "WINDOW_HARDWARE_INFO",
    "остекление балкона с выносом подоконника": "BALCONY_GLAZING_EXTENSION_SERVICE",
    "остекление балкона с крышей цена": "BALCONY_GLAZING_ROOF_SERVICE",
    "остекление балконов деревянными рамами": "BALCONY_GLAZING_GENERAL",
    "остекление балконов конструкция": "BALCONY_GLAZING_INFO",
    "остекление веранды фото": "GLAZING_DESIGN_INSPIRATION",
    "панорамные деревянные окна": "WOOD_WINDOWS_COMMERCIAL",
    "панорамные окна лес": "OUTSIDE_REAL_ESTATE_ARCHITECTURE",
    "пластиковые двери видео": "PVC_DOOR_INFO",
    "пластиковые двери межкомнатные": "OUTSIDE_INTERIOR_DOORS",
    "пластиковые двери старый": "OUTSIDE_USED_MARKET",
    "пластиковые окна в халва рассрочка": "PVC_WINDOWS_COMMERCIAL",
    "пластиковые окна район": "PVC_WINDOWS_COMMERCIAL",
    "почему алюминиевые окна": "WINDOW_PRODUCT_TECH_INFO",
    "ремонт квартиры пластиковые окна": "WINDOW_REPAIR_SERVICE",
    "ремонт пластиковых окон район": "WINDOW_REPAIR_SERVICE",
    "ремонт пластиковых окон телефон": "WINDOW_REPAIR_SERVICE",
    "ремонт подоконников пластиковых окон": "WINDOWSILL_REPAIR_SERVICE",
    "установка пластиковых окон деревянном": "WINDOW_INSTALLATION_SERVICE",
    "установка пластиковых окон размером": "WINDOW_MEASUREMENT_INFO",
    "французские мягкие окна": "SOFT_WINDOWS_COMMERCIAL",
    "цены материала на пластиковые окна": "PVC_WINDOWS_COMMERCIAL",
    "шторы на пластиковые окна фото цены": "OUTSIDE_CURTAINS_BLINDS",
    "provedal остекление веранды": "OUTDOOR_STRUCTURE_GLAZING",
    "алюминиевые окна provedal": "ALUMINIUM_WINDOWS_COMMERCIAL",
    "алюминиевые окна проведал": "ALUMINIUM_WINDOWS_COMMERCIAL",
    "окна rehau в рассрочку": "REHAU_WINDOWS_COMMERCIAL",
    "окна рехау в рассрочку": "REHAU_WINDOWS_COMMERCIAL",
    "оконная фурнитура rehau": "WINDOW_HARDWARE_SHOPPING",
    "оконная фурнитура рехау": "WINDOW_HARDWARE_SHOPPING",
    "пластиковые окна rehau": "REHAU_WINDOWS_COMMERCIAL",
    "пластиковые окна от производителя rehau": "REHAU_WINDOWS_COMMERCIAL",
    "пластиковые окна рехау": "REHAU_WINDOWS_COMMERCIAL",
    "пластиковые окна рехау от производителя": "REHAU_WINDOWS_COMMERCIAL",
    "пошаговая установка пластиковых окон": "WINDOW_INSTALLATION_DIY_INFO",
    "проведал остекление веранды": "OUTDOOR_STRUCTURE_GLAZING",
    "ремонт пластиковых окон в одинцове": "WINDOW_REPAIR_SERVICE",
    "ремонт пластиковых окон в одинцово": "WINDOW_REPAIR_SERVICE",
    "установка пластиковых окон пошагово": "WINDOW_INSTALLATION_DIY_INFO",
    "rehau thermo окна": "REHAU_WINDOWS_COMMERCIAL",
    "алюминиевые окна москва": "ALUMINIUM_WINDOWS_COMMERCIAL",
    "как выбрать пластиковые окна": "WINDOW_SELECTION_INFO",
    "какой профиль rehau выбрать": "WINDOW_SELECTION_INFO",
    "окна rehau москва": "REHAU_WINDOWS_COMMERCIAL",
    "остекление балкона п 46": "BALCONY_GLAZING_GENERAL",
    "остекление балкона с выносом": "BALCONY_GLAZING_EXTENSION_SERVICE",
    "остекление балкона с крышей": "BALCONY_GLAZING_ROOF_SERVICE",
    "остекление балконов москва": "BALCONY_GLAZING_GENERAL",
    "остекление беседки": "OUTDOOR_STRUCTURE_GLAZING",
    "остекление веранды": "OUTDOOR_STRUCTURE_GLAZING",
    "остекление террасы": "OUTDOOR_STRUCTURE_GLAZING",
    "пластиковые двери москва": "PVC_DOORS_COMMERCIAL",
    "пластиковые окна митино": "PVC_WINDOWS_COMMERCIAL",
    "пластиковые окна москва": "PVC_WINDOWS_COMMERCIAL",
    "пластиковые окна от производителя": "PVC_WINDOWS_COMMERCIAL",
    "теплое остекление балкона": "BALCONY_GLAZING_WARM",
    "установка пластиковых окон москва": "WINDOW_INSTALLATION_SERVICE",
    "холодное остекление балкона": "BALCONY_GLAZING_COLD",
}
DIRECT_OVERRIDES = {norm(k): v for k, v in DIRECT_OVERRIDES_RAW.items()}


MANUAL_SEARCH_REQUIRED = {
    norm(x)
    for x in {
        "6 6 с панорамными окнами",
        "rehau окна 2",
        "rehau окна анадырский проезд д 47",
        "алюминиевые окна 2",
        "остекление балкона 3",
        "остекление балконов 44",
        "панорамные окна 2 2",
        "пластиковая дверь 2000",
        "окно панорамное 2.5",
        "цена на пластиковое окно 100",
        "цена на пластиковое окно 3",
    }
}


def audit_classify(phrase: str, source_reason: str) -> AuditDecision:
    q = norm(phrase)

    if q in DIRECT_OVERRIDES:
        return assigned(
            DIRECT_OVERRIDES[q],
            "HIGH",
            "DIRECT_SERP_EXACT_OVERRIDE",
            "exact Step-09 query-local evidence; no transfer to other rows",
        )

    if q in MANUAL_SEARCH_REQUIRED:
        return search_required(
            "FULL_ROW_REVIEW_AMBIGUOUS_FRAGMENT",
            "full Pass-3 row review found insufficient standalone task meaning",
            True,
        )

    is_window = has(q, rf"\b{WINDOW}\b")
    is_door = has(q, rf"\b{DOOR}\b")
    is_pvc = has(q, rf"\b{PVC}\b")
    is_aluminium = has(q, rf"\b{ALUMINIUM}\b")
    is_wood = has(q, rf"\b{WOOD}\b")
    is_rehau = has(q, rf"\b{REHAU}\b")
    is_panoramic = has(q, rf"\b{PANORAMIC}\b")
    is_french = has(q, rf"\b{FRENCH}\b")
    is_balcony = has(q, rf"\b{BALCONY}\b")
    is_structure = has(q, rf"\b{STRUCTURE}\b")
    is_glazing = has(q, rf"\b{GLAZING}\b")
    is_hardware = has(q, rf"\b{HARDWARE}\b")
    is_accessory = has(q, rf"\b{ACCESSORY}\b")

    price_or_buy = has(
        q,
        r"\b(?:купить|заказать|продаж\w*|цен\w*|стоим\w*|сколько стоит|недорог\w*|"
        r"дешев\w*|под ключ|рассроч\w*|кредит\w*|магазин\w*|каталог\w*|калькулятор\w*|"
        r"рассчитать|производител\w*|производств\w*|изготовлен\w*|завод\w*|фирм\w*|компани\w*)\b",
    )
    photo = has(q, r"\b(?:фото|фотографи\w*|картинк\w*|дизайн\w*|иде\w*|образц\w*|оформлен\w*)\b") or has(
        q, r"\bпример(?:ы|ов|ами)?\b"
    )
    review = has(q, r"\b(?:отзыв\w*|мнения?\b|опыт\w*)\b")
    comparison = has(q, r"\b(?:сравн\w*|отлич\w*|разниц\w*|\bvs\b|против)\b") or (
        has(q, r"\b(?:или)\b") and (is_window or is_rehau)
    )
    selection = has(
        q,
        r"\b(?:как выбрать|выбрать|выбор\w*|какие лучше|какое лучше|какой лучше|что лучше|"
        r"лучшие|лучшая|рейтинг\w*|вариант\w*)\b",
    )
    dimensions = has(q, r"\b(?:размер\w*|габарит\w*|ширин\w*|высот\w*|площад\w*|толщин\w*)\b")
    diy = has(
        q,
        r"\b(?:своими руками|самостоятельн\w*|самому|самой|пошагов\w*|инструкц\w*|как установить|"
        r"как вставить|как поставить|как заменить|как поменять|как отрегулировать|как регулировать|"
        r"как снять|как сделать|видео)\b",
    )
    install = has(q, r"\b(?:установ\w*|монтаж\w*|вставить|поставить|монтажник\w*|устанавливаем)\b") and not has(
        q, r"\bбез установки\b"
    )
    repair = has(
        q,
        r"\b(?:ремонт\w*|почин\w*|регулиров\w*|не закрыва\w*|не открыва\w*|провис\w*|просел\w*|"
        r"просела\w*|течет|текут|слом\w*|обслуживан\w*|профилактик\w*)\b",
    )
    replace = has(q, r"\b(?:замена|заменить|поменять|сменить)\b")
    finishing = has(q, r"\b(?:откос\w*|отлив\w*|отделк\w*|обшивк\w*|утеплен\w*|утеплить|покраск\w*)\b")

    # Stable outside-business families.
    if has(q, r"\b(?:штор\w*|жалюз\w*|занавес\w*|карниз\w*|плиссе)\b"):
        return assigned("OUTSIDE_CURTAINS_BLINDS", "HIGH", "OUTSIDE_CURTAINS", "curtain/blind task is outside the window/glazing business job")
    if has(q, r"\b(?:радиатор\w*|батаре\w*|конвектор\w*|отоплен\w*|кондиционер\w*|тепл\w*\s+пол)\b"):
        return assigned("OUTSIDE_HEATING_HVAC", "HIGH", "OUTSIDE_HEATING", "heating or HVAC equipment is the requested result")
    if has(q, r"\b(?:б/у|\bбу\b|подержан\w*|авито|с рук)\b"):
        return assigned("OUTSIDE_USED_MARKET", "HIGH", "OUTSIDE_USED", "used-market intent")
    if is_door and has(q, r"\b(?:межкомнатн\w*|в комнат\w*|в ванн\w*|в туалет\w*|гармошк\w*|купе)\b"):
        return assigned("OUTSIDE_INTERIOR_DOORS", "MEDIUM", "OUTSIDE_INTERIOR_DOOR", "interior-door result is outside exterior/balcony PVC-door scope")

    building_first = has(
        q,
        rf"\b(?:дом\w*|домик\w*|квартир\w*|апартамент\w*|студи\w*|комнат\w*|спальн\w*|"
        rf"гостин\w*|зал\w*|кухн\w*|бан\w*|бассейн\w*|барнхаус\w*|бытовк\w*|лофт\w*|"
        rf"пристройк\w*|беседк\w*|террас\w*|веранд\w*|барбекю\w*)\b.*\b(?:{PANORAMIC}|{FRENCH})\b",
    )
    project_context = has(q, rf"\b(?:проект\w*|интерьер\w*)\b.*\b(?:{PANORAMIC}|{FRENCH})\b")
    panorama_place = has(q, rf"\b{PANORAMIC}\b.*\b{WINDOW}\b.*\b(?:лес|море|пик|новострой\w*)\b")
    if (building_first or project_context or panorama_place) and not (is_glazing or install or repair):
        return assigned(
            "OUTSIDE_REAL_ESTATE_ARCHITECTURE",
            "HIGH" if building_first or project_context else "MEDIUM",
            "OUTSIDE_ARCHITECTURE",
            "building/project/inspiration result dominates over a window-product task",
        )

    # Dedicated navigation result.
    if has(q, r"\b(?:официальн\w*|сайт\w*|дилер\w*|партнер\w*)\b") and (
        is_rehau or has(q, r"\b(?:kbe|кбе|veka|века|brusbox|брусбокс|производител\w*)\b")
    ):
        return assigned("NAVIGATION_BRAND_SITE", "HIGH", "BRAND_NAVIGATION", "official/branded destination is requested")

    # Visual/examples content is a distinct result. Price/buy wording keeps a row in
    # its commercial/service task unless Step-09 directly proved a portfolio job.
    if photo and not price_or_buy and not is_door and (is_window or is_glazing or is_balcony or is_structure):
        return assigned("GLAZING_DESIGN_INSPIRATION", "HIGH", "DESIGN_INSPIRATION", "photos/design/examples are the expected result")

    if review:
        if is_hardware:
            return assigned("WINDOW_HARDWARE_INFO", "HIGH", "HARDWARE_REVIEWS", "reviews concern window hardware")
        if is_balcony and (is_glazing or is_window):
            return assigned("BALCONY_GLAZING_INFO", "MEDIUM", "BALCONY_REVIEWS", "reviews concern balcony glazing")
        if is_structure and is_glazing:
            return assigned("GLAZING_SELECTION_INFO", "MEDIUM", "OUTDOOR_GLAZING_REVIEWS", "reviews concern an outdoor-structure glazing system")
        if is_door:
            return assigned("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_REVIEWS", "reviews concern PVC doors")
        return assigned("WINDOW_REVIEWS_INFO", "HIGH", "WINDOW_REVIEWS", "reviews/experience content is requested")

    # Mosquito nets, anti-cat and anti-dust nets are their own task family.
    mosquito = has(q, r"\b(?:москит\w*|антикошк\w*|антипыл\w*|противомоскит\w*)\b") or (
        has(q, r"\bсетк\w*\b") and (is_window or is_door)
    )
    if mosquito:
        if repair or replace:
            return assigned("MOSQUITO_NET_REPAIR_SERVICE", "HIGH", "MOSQUITO_REPAIR", "mosquito-net repair/replacement result")
        if install:
            return assigned("MOSQUITO_NET_INSTALLATION_SERVICE", "HIGH", "MOSQUITO_INSTALL", "mosquito-net installation result")
        if selection or has(q, r"\b(?:как выбрать|виды|тип\w*)\b"):
            return assigned("MOSQUITO_NET_SELECTION_INFO", "HIGH", "MOSQUITO_SELECTION", "mosquito-net decision support")
        return assigned("MOSQUITO_NET_SHOPPING", "HIGH", "MOSQUITO_SHOPPING", "mosquito-net product is requested")

    negated_balcony_glazing = is_balcony and has(q, r"\b(?:без остекления|открыт\w*\s+балкон\w*)\b")
    if negated_balcony_glazing:
        return assigned(
            "OPEN_BALCONY_FINISHING",
            "HIGH",
            "OPEN_BALCONY",
            "open/unglazed balcony task is separated from glazing",
        )
    if is_structure and has(q, r"\bбез остекления\b"):
        return search_required("NEGATED_OUTDOOR_GLAZING", "unglazed outdoor-structure phrase does not establish a positive service task", True)

    # Products used to perform repairs remain shopping tasks, not repair services.
    if has(
        q,
        r"\b(?:ремкомплект\w*|набор\w*\s+для\s+ремонт\w*|средств\w*\s+для\s+ремонт\w*|"
        r"кле\w*\s+для\s+ремонт\w*|космофен\w*|жидк\w*\s+пластик\w*|запчаст\w*)\b",
    ):
        return assigned("WINDOW_ACCESSORIES_SHOPPING", "HIGH", "REPAIR_MATERIAL_SHOPPING", "repair material/kit is the requested product")

    # Balcony and outdoor glazing are resolved before generic component words so a
    # glazing-unit/sill mention inside a glazing service does not steal the task.
    if is_balcony and (is_glazing or has(q, rf"\b(?:{WINDOW})\b.*\b(?:на|для)\b.*\b{BALCONY}\b") or has(q, rf"\b{BALCONY}\b.*\b{WINDOW}\b")):
        if has(q, r"\b(?:разрешен\w*|согласован\w*|закон\w*|нужно ли разрешение)\b"):
            return assigned("GLAZING_PERMISSION_INFO", "HIGH", "GLAZING_PERMISSION", "permission/legal glazing result")
        if diy:
            return assigned("GLAZING_DIY_INFO", "HIGH", "BALCONY_GLAZING_DIY", "DIY balcony-glazing instructions")
        if has(q, r"\b(?:демонтаж\w*|разобрать|снять остекление)\b"):
            return assigned("WINDOW_DEMOLITION_SERVICE", "HIGH", "BALCONY_DEMOLITION", "balcony glazing dismantling")
        if replace and is_glazing:
            return assigned("BALCONY_GLAZING_GENERAL", "HIGH", "BALCONY_REGLAZING", "replacement of balcony glazing")
        if has(q, r"\b(?:вынос\w*|с выносом)\b"):
            return assigned("BALCONY_GLAZING_EXTENSION_SERVICE", "HIGH", "BALCONY_EXTENSION", "extension/outset changes construction scope")
        if has(q, r"\b(?:с крышей|крыш\w*|кровл\w*)\b"):
            return assigned("BALCONY_GLAZING_ROOF_SERVICE", "HIGH", "BALCONY_ROOF", "roof construction changes service scope")
        if (finishing or has(q, r"\b(?:ремонт балкон\w*|утеплен\w*|обшивк\w*)\b")) and is_glazing:
            return assigned("BALCONY_RENOVATION_WITH_GLAZING", "HIGH", "BALCONY_RENOVATION_BUNDLE", "renovation/finishing is bundled with glazing")
        if has(q, r"\bтепл\w*\b"):
            return assigned("BALCONY_GLAZING_WARM", "HIGH", "BALCONY_WARM", "warm glazing result")
        if has(q, r"\bхолодн\w*\b"):
            return assigned("BALCONY_GLAZING_COLD", "HIGH", "BALCONY_COLD", "cold glazing result")
        if photo and not price_or_buy:
            return assigned("GLAZING_DESIGN_INSPIRATION", "HIGH", "BALCONY_INSPIRATION", "balcony glazing photos/examples")
        if review or selection or has(q, r"\b(?:виды|варианты|конструкц\w*|форум\w*|можно ли|правильно|материал\w*)\b"):
            return assigned("BALCONY_GLAZING_INFO", "HIGH", "BALCONY_GLAZING_INFO", "balcony-glazing information/selection result")
        return assigned("BALCONY_GLAZING_GENERAL", "HIGH", "BALCONY_GLAZING_SERVICE", "balcony/loggia glazing service")

    if is_structure and is_glazing:
        if has(q, r"\b(?:разрешен\w*|согласован\w*|закон\w*)\b"):
            return assigned("GLAZING_PERMISSION_INFO", "HIGH", "GLAZING_PERMISSION", "permission/legal glazing result")
        if diy:
            return assigned("GLAZING_DIY_INFO", "HIGH", "OUTDOOR_GLAZING_DIY", "DIY outdoor-structure glazing")
        if photo and not price_or_buy:
            return assigned("GLAZING_DESIGN_INSPIRATION", "HIGH", "OUTDOOR_INSPIRATION", "outdoor-glazing photos/design/examples")
        if selection or has(q, r"\b(?:виды|варианты|плюсы и минусы|материал\w*|толщин\w*|конструкц\w*)\b"):
            return assigned("GLAZING_SELECTION_INFO", "HIGH", "OUTDOOR_GLAZING_SELECTION", "outdoor glazing system/material decision support")
        return assigned("OUTDOOR_STRUCTURE_GLAZING", "HIGH", "OUTDOOR_GLAZING_SERVICE", "glazing service for veranda/terrace/gazebo/porch")

    # DIY/procedural lifecycle tasks.
    if diy:
        if is_door:
            return assigned("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_DIY", "PVC-door procedural information")
        if finishing:
            return assigned("WINDOW_FINISHING_DIY_INFO", "HIGH", "WINDOW_FINISHING_DIY", "DIY window finishing")
        if repair or has(q, r"\b(?:отрегулиров\w*|регулировать|починить)\b"):
            return assigned("WINDOW_REPAIR_DIY_INFO", "HIGH", "WINDOW_REPAIR_DIY", "DIY window diagnosis/repair")
        if is_glazing:
            return assigned("GLAZING_DIY_INFO", "HIGH", "GLAZING_DIY", "DIY glazing work")
        if is_window or is_rehau or is_aluminium or is_pvc or is_french or is_panoramic:
            return assigned("WINDOW_INSTALLATION_DIY_INFO", "MEDIUM", "WINDOW_DIY", "procedural window work without hiring a service")

    # Component replacement/repair is a repair job; whole-object replacement is not.
    component_context = is_hardware or is_accessory or has(q, r"\b(?:стекл\w*|фрамуг\w*)\b")
    if has(q, r"\bподоконник\w*\b") and (repair or replace):
        return assigned("WINDOWSILL_REPAIR_SERVICE", "HIGH", "WINDOWSILL_REPAIR", "windowsill repair/replacement result")
    if finishing and (repair or replace or install or price_or_buy):
        return assigned("WINDOW_FINISHING_SERVICE", "HIGH", "WINDOW_FINISHING_SERVICE", "professional slopes/surround/window finishing")
    if replace and is_door and not component_context:
        return assigned("PVC_DOOR_REPLACEMENT_SERVICE", "HIGH", "PVC_DOOR_REPLACEMENT", "whole PVC-door replacement")
    if replace and is_window and not component_context:
        return assigned("WINDOW_REPLACEMENT_SERVICE", "HIGH", "WINDOW_REPLACEMENT", "whole-window replacement")
    if (repair or (replace and component_context)) and is_door:
        return assigned("PVC_DOOR_REPAIR_SERVICE", "HIGH", "PVC_DOOR_REPAIR", "professional PVC-door repair/component replacement")
    if (repair or (replace and component_context)) and (is_window or is_rehau or is_aluminium or component_context):
        return assigned("WINDOW_REPAIR_SERVICE", "HIGH", "WINDOW_REPAIR", "professional window repair/component replacement")

    # Hardware/accessory tasks precede generic installation/product matching.
    profile_component = has(q, r"\bпрофил\w*\s+для\b") or has(q, r"^профил\w*\b") or has(q, r"\bалюминиев\w*\s+профил\w*\b")
    if is_hardware or profile_component:
        hardware_info = review or selection or comparison or has(
            q,
            r"\b(?:виды|тип\w*|бренд\w*|марк\w*|назван\w*|логотип\w*|гост\b|сертификат\w*|"
            r"функци\w*|устройств\w*|конструкц\w*|как устроен\w*|как называется|чем смазать|размер\w*)\b",
        )
        if hardware_info:
            return assigned("WINDOW_HARDWARE_INFO", "HIGH", "WINDOW_HARDWARE_INFO", "hardware information/selection result")
        return assigned("WINDOW_HARDWARE_SHOPPING", "HIGH", "WINDOW_HARDWARE_SHOPPING", "window hardware/component product")

    if is_accessory or has(q, r"\b(?:стекл\w*\s+для\s+(?:пластиков\w*\s+)?двер\w*|средств\w*\s+для\s+окон)\b"):
        if selection or comparison or has(q, r"\b(?:как выбрать|виды|тип\w*)\b"):
            return assigned("WINDOW_ACCESSORY_SELECTION_INFO", "HIGH", "WINDOW_ACCESSORY_SELECTION", "window accessory decision support")
        return assigned("WINDOW_ACCESSORIES_SHOPPING", "HIGH", "WINDOW_ACCESSORY_SHOPPING", "window accessory/add-on product")

    # Professional installation after accessory-specific actions have been resolved.
    if install:
        if dimensions and has(q, r"\bразмером\b") and not price_or_buy:
            return assigned("WINDOW_MEASUREMENT_INFO", "MEDIUM", "INSTALLATION_MEASUREMENT", "installation phrase is primarily about sizing/measurement")
        if is_door and not is_window:
            return assigned("PVC_DOOR_INSTALLATION_SERVICE", "HIGH", "PVC_DOOR_INSTALLATION", "professional PVC-door installation")
        if is_window or is_rehau or is_aluminium or is_pvc:
            return assigned("WINDOW_INSTALLATION_SERVICE", "HIGH", "WINDOW_INSTALLATION", "professional window installation")

    if has(q, r"\b(?:демонтаж\w*|демонтировать|снять окно|разобрать окно)\b"):
        return assigned("WINDOW_DEMOLITION_SERVICE", "HIGH", "WINDOW_DEMOLITION", "window dismantling/demolition")

    # Generic glazing outside an object-specific family.
    if is_glazing:
        if has(q, r"\b(?:разрешен\w*|согласован\w*|закон\w*)\b"):
            return assigned("GLAZING_PERMISSION_INFO", "HIGH", "GLAZING_PERMISSION", "permission/legal glazing result")
        if selection or has(q, r"\b(?:виды|варианты|материал\w*|конструкц\w*)\b"):
            return assigned("GLAZING_SELECTION_INFO", "HIGH", "GENERAL_GLAZING_SELECTION", "glazing system/type decision support")
        if price_or_buy:
            return assigned("GENERAL_GLAZING_SERVICE", "MEDIUM", "GENERAL_GLAZING_SERVICE", "commercial glazing service without a more specific object")
        return search_required("GENERIC_GLAZING_UNRESOLVED", "generic glazing wording lacks a stable object/action boundary", False)

    # Information tasks are normalized by expected result rather than product word.
    if comparison:
        return assigned("WINDOW_COMPARISON_INFO", "HIGH", "WINDOW_COMPARISON", "relative product/brand evaluation")
    if dimensions and (is_window or is_door or is_rehau or is_panoramic or is_french or is_aluminium or is_pvc):
        if is_door:
            return assigned("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_DIMENSIONS", "PVC-door dimensions information")
        return assigned("WINDOW_DIMENSIONS_INFO", "HIGH", "WINDOW_DIMENSIONS", "window/product sizing information")
    if has(q, r"\b(?:частн\w*\s+дом|загородн\w*\s+дом|коттедж\w*|котельн\w*|санузл\w*|ванн\w*)\b") and (
        selection or has(q, r"\b(?:требован\w*|норм\w*|стандарт\w*|форма\w*|виды|варианты|какие окна|какое окно)\b")
    ):
        return assigned("PRIVATE_HOUSE_WINDOW_PLANNING_INFO", "HIGH", "PRIVATE_HOUSE_PLANNING", "private-house window planning/requirements")
    if selection:
        return assigned("WINDOW_SELECTION_INFO", "HIGH", "WINDOW_SELECTION", "window/product decision support")
    if has(
        q,
        r"\b(?:виды|тип\w*|серии|систем\w*|конструкц\w*|устройств\w*|режим\w*|цвет\w*|стил\w*|"
        r"проветриван\w*|открыван\w*|закрыт\w*|открыт\w*|почему|зачем|суть|что значит|что такое|"
        r"как выглядит|как называ\w*|сверлен\w*|сборк\w*)\b",
    ) and (is_window or is_rehau or is_aluminium or is_pvc or is_panoramic or is_french):
        if is_door:
            return assigned("PVC_DOOR_INFO", "HIGH", "PVC_DOOR_INFO", "PVC-door operation/properties information")
        return assigned("WINDOW_PRODUCT_TECH_INFO", "HIGH", "WINDOW_TECH_INFO", "window technology/definition/operation information")

    # Product/object families. Material/form modifiers do not create extra clusters
    # beyond the frozen taxonomy.
    if has(q, r"\b(?:мягк\w*\s+окн\w*)\b"):
        return assigned("SOFT_WINDOWS_COMMERCIAL", "HIGH", "SOFT_WINDOWS_PRODUCT", "soft-window product")
    if has(q, rf"\b(?:мансардн\w*\s+{WINDOW}|{WINDOW}\s+(?:на|для)\s+крыш\w*|кровельн\w*\s+{WINDOW})\b"):
        return assigned("ROOF_WINDOWS_COMMERCIAL", "HIGH", "ROOF_WINDOWS_PRODUCT", "roof/mansard-window product")
    if is_french and is_window:
        return assigned("FRENCH_WINDOWS_COMMERCIAL", "HIGH", "FRENCH_WINDOWS_PRODUCT", "French-window product/form job")
    if is_panoramic and is_window:
        return assigned("PANORAMIC_WINDOWS_COMMERCIAL", "HIGH", "PANORAMIC_WINDOWS_PRODUCT", "panoramic-window product/form job")
    if has(q, r"\b(?:деревоалюмини\w*|деревянно[- ]алюмини\w*|дерево[- ]алюмини\w*|дерево\s+алюмини\w*)\b") and is_window:
        return assigned("TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL", "HIGH", "TIMBER_ALUMINIUM_PRODUCT", "timber-aluminium hybrid window")
    if is_wood and is_window and not is_pvc:
        return assigned("WOOD_WINDOWS_COMMERCIAL", "HIGH", "WOOD_WINDOWS_PRODUCT", "wooden-window product")
    if is_aluminium and is_window:
        return assigned("ALUMINIUM_WINDOWS_COMMERCIAL", "HIGH", "ALUMINIUM_WINDOWS_PRODUCT", "aluminium-window product")
    if is_rehau and (is_window or has(q, r"\b(?:профил\w*|систем\w*)\b")):
        return assigned("REHAU_WINDOWS_COMMERCIAL", "HIGH", "REHAU_PRODUCT", "Rehau product-family commercial job")
    if is_window and is_door:
        return assigned("WINDOWS_DOORS_COMBINED_COMMERCIAL", "HIGH", "WINDOW_DOOR_COMBINED", "combined window-and-door product result")
    if is_door and is_pvc:
        return assigned("PVC_DOORS_COMMERCIAL", "HIGH", "PVC_DOOR_PRODUCT", "PVC-door product")
    if is_window and is_pvc:
        return assigned("PVC_WINDOWS_COMMERCIAL", "HIGH", "PVC_WINDOWS_PRODUCT", "PVC-window product")
    if is_window:
        return assigned("WINDOWS_COMMERCIAL_GENERAL", "MEDIUM", "GENERIC_WINDOWS_PRODUCT", "generic window product task")

    if source_reason == "AMBIGUOUS_NUMERIC_OR_FRAGMENT_INTENT":
        return search_required("UPSTREAM_AMBIGUOUS_FRAGMENT", "upstream ambiguity remains unresolved by independent review", True)
    return search_required("NO_STABLE_FROZEN_TASK", "independent review found no stable frozen-task match", False)


def main() -> None:
    with TAXONOMY.open(encoding="utf-8", newline="") as f:
        taxonomy_rows = list(csv.DictReader(f, delimiter="\t"))
    allowed = {r["cluster_id"] for r in taxonomy_rows}
    if len(allowed) != 62:
        raise RuntimeError(f"expected 62 frozen taxonomy ids, got {len(allowed)}")
    unknown_direct = sorted(set(DIRECT_OVERRIDES.values()) - allowed)
    if unknown_direct:
        raise RuntimeError(f"direct overrides use unknown clusters: {unknown_direct}")

    with ASSIGNMENT.open(encoding="utf-8", newline="") as f:
        assignment_rows = list(csv.DictReader(f, delimiter="\t"))
    active_rows = [r for r in assignment_rows if r["source_disposition"] in ACTIVE_DISPOSITIONS]
    if len(assignment_rows) != 2840 or len(active_rows) != 2332:
        raise RuntimeError(f"assignment accounting mismatch: all={len(assignment_rows)} active={len(active_rows)}")

    with REVIEW_PACK.open(encoding="utf-8", newline="") as f:
        pack_rows = list(csv.DictReader(f, delimiter="\t"))
    if len(pack_rows) != 2332:
        raise RuntimeError(f"expected 2332 review-pack rows, got {len(pack_rows)}")
    if [r["phrase"] for r in active_rows] != [r["phrase"] for r in pack_rows]:
        raise RuntimeError("review pack and active assignment phrase order differ")
    if [int(r["qa_row"]) for r in pack_rows] != list(range(1, 2333)):
        raise RuntimeError("qa_row sequence is not 1..2332")

    with DIRECT.open(encoding="utf-8", newline="") as f:
        direct_rows = list(csv.DictReader(f, delimiter="\t"))
    direct_queries = {norm(r["query"]) for r in direct_rows}
    if len(direct_rows) != 75:
        raise RuntimeError(f"expected 75 Step-09 direct decisions, got {len(direct_rows)}")

    full_review = []
    errors = []
    transitions = Counter()
    outcomes = Counter()
    rules = Counter()
    direct_active = 0
    direct_conflicts = 0
    unresolved = 0

    for idx, row in enumerate(active_rows, 1):
        phrase = row["phrase"]
        q = norm(phrase)
        if q in direct_queries:
            direct_active += 1
        decision = audit_classify(phrase, row["source_corrected_reason"])
        if decision.cluster_id and decision.cluster_id not in allowed:
            raise RuntimeError(f"unknown audit cluster {decision.cluster_id!r} for {phrase!r}")
        rules[decision.rule] += 1

        old_status = row["assignment_status"]
        old_cluster = row["cluster_id"]
        error_class = ""
        correction_action = "NONE"

        if decision.status == "ASSIGNED":
            if old_status == "ASSIGNED" and old_cluster == decision.cluster_id:
                outcome = "PASS2_CONFIRMED"
            elif old_status == "SEARCH_REQUIRED":
                outcome = "PASS2_ERROR_SEARCH_REQUIRED_RESOLVED"
                error_class = "SEARCH_REQUIRED_FALSE_NEGATIVE"
                correction_action = "ASSIGN_CLUSTER"
            else:
                outcome = "PASS2_ERROR_WRONG_CLUSTER"
                error_class = "WRONG_CLUSTER"
                correction_action = "REASSIGN_CLUSTER"
        else:
            if old_status == "SEARCH_REQUIRED":
                outcome = "PASS2_SEARCH_REQUIRED_CONFIRMED"
            elif decision.decisive:
                outcome = "PASS2_ERROR_ASSIGNED_SHOULD_SEARCH"
                error_class = "UNSUPPORTED_ASSIGNMENT"
                correction_action = "SET_SEARCH_REQUIRED"
            else:
                outcome = "PASS2_NOT_CONFIRMED_REQUIRES_ADJUDICATION"
                unresolved += 1

        if q in DIRECT_OVERRIDES and outcome not in {"PASS2_CONFIRMED", "PASS2_SEARCH_REQUIRED_CONFIRMED"}:
            direct_conflicts += 1
            if error_class:
                error_class = "DIRECT_SERP_" + error_class

        outcomes[outcome] += 1
        transition_key = (
            old_status,
            old_cluster or "<NONE>",
            decision.status,
            decision.cluster_id or "<NONE>",
            error_class or "<NONE>",
        )
        if error_class:
            transitions[transition_key] += 1

        record = {
            "qa_row": idx,
            "phrase": phrase,
            "source_disposition": row["source_disposition"],
            "source_corrected_reason": row["source_corrected_reason"],
            "pass2_assignment_status": old_status,
            "pass2_cluster_id": old_cluster,
            "pass2_assignment_confidence": row["assignment_confidence"],
            "evidence_mode": row["evidence_mode"],
            "audit_expected_status": decision.status,
            "audit_cluster_id": decision.cluster_id,
            "audit_confidence": decision.confidence,
            "audit_rule": decision.rule,
            "audit_reason": decision.reason,
            "review_outcome": outcome,
            "error_class": error_class,
            "correction_action": correction_action,
        }
        full_review.append(record)
        if error_class:
            errors.append(record)

    review_fields = [
        "qa_row",
        "phrase",
        "source_disposition",
        "source_corrected_reason",
        "pass2_assignment_status",
        "pass2_cluster_id",
        "pass2_assignment_confidence",
        "evidence_mode",
        "audit_expected_status",
        "audit_cluster_id",
        "audit_confidence",
        "audit_rule",
        "audit_reason",
        "review_outcome",
        "error_class",
        "correction_action",
    ]
    with OUT_REVIEW.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=review_fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(full_review)
    with OUT_ERRORS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=review_fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(errors)

    transition_fields = [
        "pass2_assignment_status",
        "pass2_cluster_id",
        "audit_expected_status",
        "audit_cluster_id",
        "error_class",
        "row_count",
    ]
    with OUT_TRANSITIONS.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=transition_fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for key, count in sorted(transitions.items(), key=lambda kv: (-kv[1], kv[0])):
            w.writerow({
                "pass2_assignment_status": key[0],
                "pass2_cluster_id": key[1],
                "audit_expected_status": key[2],
                "audit_cluster_id": key[3],
                "error_class": key[4],
                "row_count": count,
            })

    if len(full_review) != 2332:
        raise RuntimeError("Pass3 full-review accounting mismatch")
    if len(errors) != sum(transitions.values()):
        raise RuntimeError("Pass3 error-ledger transition accounting mismatch")
    if direct_active != 66:
        raise RuntimeError(f"expected 66 active direct-evidence rows, got {direct_active}")

    qa = {
        "status": "PASS3_FULL_REVIEW_GENERATED__ERROR_LEDGER_NOT_FROZEN",
        "rule_version": RULE_VERSION,
        "source_assignment_rows": len(assignment_rows),
        "active_rows": len(active_rows),
        "review_pack_rows": len(pack_rows),
        "pass3_rows_reviewed": len(full_review),
        "pass3_silent_drops": 0,
        "pass3_error_rows": len(errors),
        "pass3_unresolved_adjudication_rows": unresolved,
        "direct_step09_decisions": len(direct_rows),
        "direct_active_rows": direct_active,
        "direct_assignment_conflicts_found": direct_conflicts,
        "taxonomy_cluster_ids": len(allowed),
        "review_outcomes": dict(sorted(outcomes.items())),
        "audit_rule_counts": dict(sorted(rules.items())),
        "unknown_cluster_ids": [],
        "old_step10_input_used": False,
        "blind84_input_used": False,
        "target_cluster_count_used": False,
        "pass2_mutated_by_pass3_audit": False,
        "error_ledger_frozen": False,
        "consolidated_correction_applied": False,
        "pass3_complete": False,
    }
    OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False))


if __name__ == "__main__":
    main()
