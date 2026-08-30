#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V19 as v19

_v19_classifier = b.classify_semantic
base = v19.base

b.TASKS.update({
    "PVC_DOOR_INSTALLATION_SERVICE": ("Профессиональная установка/монтаж пластиковых дверей", "COMMERCIAL_SERVICE", "ADJACENT"),
    "GLAZING_PERMISSION_INFO": ("Разрешения/правила для остекления балкона", "INFORMATIONAL", "ADJACENT"),
    "OUTSIDE_HVAC": ("Кондиционирование рядом с балконом/окнами", "OUTSIDE_CORE", "OUTSIDE"),
})

# V20 is a manual-QA correction layer. It deliberately handles only explicit
# head-object/action signals that V19 broad product/service fallbacks swallowed.
# Ambiguous combinations still return None -> SEARCH_REQUIRED.


def _has(p: str, *parts: str) -> bool:
    return base.has(p, *parts)


def _word(p: str, pattern: str) -> bool:
    return bool(re.search(pattern, p))


def classify_v20(phrase: str):
    p = base.n(phrase)
    win = base.windowish(p)
    glazing = _has(p, "остеклен", "застекл")
    balcony = _has(p, "балкон", "лоджи")
    door = "двер" in p and _has(p, "пластик", "пвх")
    commercial_price = _has(p, "купить", "заказать", "цена", "цены", "стоимость", "сколько стоит", "сколько стоят")

    # 1) Reputation/review intent must not be swallowed by the underlying
    # product, installation, repair or glazing family.
    if (win or glazing) and _has(p, "отзыв", "рейтинг", "форум"):
        return "WINDOW_REVIEWS_INFO", "Explicit reviews/ranking/forum task outranks the underlying product or service family", "HIGH"

    # 2) Visual/procedural intent must outrank V19 panoramic/French/private-house
    # commercial fallbacks. Avoid false match on 'примерные цены'.
    exact_example = bool(re.search(r"\bпример(?:ы)?\b", p))
    if win and _has(p, "установ", "монтаж") and _has(p, "фото", "видео", "инструк", "пошаг"):
        return "WINDOW_INSTALLATION_DIY", "Explicit installation photo/video/instruction task is procedural information, not a service request", "HIGH"
    if (win or glazing) and (_has(p, "фото", "дизайн", "интерьер") or exact_example or "проекты остекления" in p):
        return "DESIGN_INSPIRATION", "Explicit photo/design/example task outranks the underlying product or glazing family", "HIGH"

    # 3) Dimensions remain informational unless explicit buying/price/install
    # language makes the dimensions a product/service configuration.
    if win and _has(p, "размер", "ширина", "высота", "габарит") and not commercial_price and not _has(p, "установ", "монтаж"):
        return "WINDOW_DIMENSIONS_INFO", "Explicit window dimensions task outranks specific material/private-house product routing", "HIGH"

    # 4) Open/no-glazing balcony and legal/permission tasks are not glazing
    # service requests merely because the word 'остекление' appears.
    if balcony and "без остеклен" in p:
        return "OPEN_BALCONY_FINISHING", "Explicit no-glazing/open-balcony task outranks the generic balcony-glazing service family", "HIGH"
    if balcony and glazing and _has(p, "разрешение", "разрешен", "можно ли", "нужно ли"):
        return "GLAZING_PERMISSION_INFO", "Explicit permission/rules question about balcony glazing", "HIGH"
    if balcony and "кондиционер" in p:
        return "OUTSIDE_HVAC", "Air-conditioning is the head task; glazing is only context", "HIGH"

    # 5) Selection and DIY glazing intent before object-specific service routing.
    if glazing and _has(p, "какое остекление", "какое лучше", "какое выбрать", "выбрать остекление", "материалы"):
        return "GLAZING_SELECTION_INFO", "Explicit glazing selection/material-choice task outranks the service family", "HIGH"
    if glazing and _has(p, "самому", "своими руками", "самостоятель", "как остеклить", "как застеклить", "пошаг", "видео"):
        return "GLAZING_DIY_INFO", "Explicit DIY/procedural glazing task outranks the service family", "HIGH"

    # 6) Demolition is an action of its own; repair+glazing combinations are
    # intentionally unresolved rather than forced into generic glazing.
    if glazing and "демонтаж" in p:
        return "WINDOW_DEMOLITION", "Explicit demolition/removal of glazing is not a generic glazing-installation task", "HIGH"
    if glazing and "ремонт" in p and balcony:
        return None, "Phrase explicitly mixes balcony/glazing with repair; keep the action boundary visible", "LOW"

    # 7) Materials/components whose head object is the thing bought/selected for
    # glazing are not the glazing service itself.
    if glazing and _word(p, r"\b(?:профил\w*|рам\w*)\s+для\s+остеклен"):
        return "WINDOW_HARDWARE", "Profile/frame is the head component; glazing is its use context", "HIGH"
    if glazing and _word(p, r"\b(?:монолитн\w*\s+)?поликарбонат\w*\s+для\s+остеклен"):
        return "WINDOW_ACCESSORIES", "Polycarbonate is the head material/product; glazing is its use context", "HIGH"
    if glazing and "толщина" in p and "поликарбонат" in p:
        return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit material-thickness/selection task for a glazing material", "HIGH"

    # 8) Repair kits/materials are product demand even though 'ремонт' occurs as
    # a use-context word. This must run before generic repair routing.
    if win and _has(p, "запчасти для ремонта", "ремкомплект", "набор для ремонта"):
        return "WINDOW_HARDWARE", "Repair kit/parts are the head product rather than a repair-service request", "HIGH"
    if win and _has(p, "клей для ремонта", "космофен для ремонта"):
        return "WINDOW_ACCESSORIES", "Repair compound/material is the head product rather than a repair-service request", "HIGH"

    # 9) Explicit symptom/operation intent is not a product purchase merely because
    # a material or Rehau brand is present.
    symptom = _has(p, "не закрывается", "не открывается", "не закрывает", "не открывает")
    if door and symptom:
        return "PVC_DOOR_REPAIR_DIY", "Explicit plastic-door malfunction/diagnostic task", "HIGH"
    if win and symptom:
        return "WINDOW_REPAIR_DIY", "Explicit window malfunction/diagnostic task", "HIGH"
    if door and _has(p, "открывание", "как открыть", "как закрыть", "снять дверь"):
        return "PVC_DOOR_OPERATION_INFO", "Explicit plastic-door operation task", "HIGH"
    if win and _has(p, "открывание", "проветривание"):
        return "WINDOW_OPERATION_DIY", "Explicit window operation/ventilation task", "HIGH"

    # 10) DIY repair and repair finishing/reputation boundaries before generic
    # repair service routing.
    if win and "ремонт" in p and _has(p, "самому", "своими руками", "домашних условиях", "руками"):
        return "WINDOW_REPAIR_DIY", "Explicit self-repair/home-repair wording is informational/DIY", "HIGH"
    if win and _has(p, "ремонт откос", "ремонт отлив"):
        return "WINDOW_FINISHING_SERVICE", "Explicit slopes/ebb repair belongs to window finishing rather than generic window repair", "HIGH"
    if win and "ремонт подокон" in p:
        return "WINDOWSILL_REPAIR", "Explicit windowsill repair is a dedicated maintenance task", "HIGH"
    if win and _has(p, "пластиковые окна после ремонта", "пластиковые окна без ремонта", "окна пластиковые какой ремонт"):
        return None, "Repair wording is contextual/ambiguous rather than a clear repair-service request", "LOW"

    # 11) Whole-window replacement: use action/object wording, not the V18 naive
    # substring that also matches 'замена оконной фурнитуры'.
    if _has(p, "замена оконной фурнитуры", "заменить оконную фурнитуру", "замена фурнитуры"):
        return "WINDOW_REPAIR", "Replacement of window hardware is component maintenance, not whole-window replacement", "HIGH"
    if win and _word(p, r"\b(?:стоимость|цена|цены)\b.{0,25}\bзамен\w*\b.{0,20}\bокн(?:о|а|а?ми|ов)?\b"):
        return "WINDOW_REPLACEMENT_SERVICE", "Explicit priced whole-window replacement task", "HIGH"
    if win and _word(p, r"\bзамен\w*\b.{0,12}\b(?:окно|окна|окон)\b") and not _has(p, "фурнитур", "ручк", "уплотн", "стеклопак", "петл", "механизм"):
        if "ремонт" in p:
            return None, "Phrase explicitly mixes repair and whole-window replacement; keep the boundary visible", "LOW"
        return "WINDOW_REPLACEMENT_SERVICE", "Explicit whole-window replacement action", "HIGH"

    # 12) Mixed installation+repair stays unresolved. Action-headed installation
    # is a service even if V19 sees a ready-made/material product.
    if win and _has(p, "установ", "монтаж") and "ремонт" in p:
        return None, "Phrase explicitly mixes installation and repair; keep the service boundary visible", "LOW"
    if door and _word(p, r"\b(?:установка|монтаж)\w*\b.{0,45}\bдвер"):
        return "PVC_DOOR_INSTALLATION_SERVICE", "Action-headed plastic-door installation/ монтаж request is a service, not door purchase", "HIGH"
    if win and (_word(p, r"^\s*(?:установка|монтаж)\b") or "изготовление и установка" in p or "установка готовых" in p):
        return "WINDOW_INSTALLATION", "Action-headed window installation request outranks ready-made/material product routing", "HIGH"

    # 13) Strong component/accessory head objects before broad aluminium/PVC/Rehau
    # product families. Do not reroute window-headed Rehau profile/system phrases.
    component_head = (
        _word(p, r"^(?:детск\w*\s+)?замок\b")
        or _word(p, r"^(?:многозапорн\w*\s+)?замок\b")
        or _word(p, r"^(?:механизм|створк\w*|редуктор\w*|ригель\w*|ролик\w*|клапан\w*|заглушк\w*|направляющ\w*|стеклопакет\w*)\b")
        or _word(p, r"\b(?:профил\w*|рам\w*|стеклопакет\w*|ролик\w*|клапан\w*|заглушк\w*|направляющ\w*)\s+(?:для|на)\s+.*\bокн")
        or "подставочный профиль для окон" in p
    )
    if win and component_head and not _has(p, "ремонт", "замена", "заменить", "установ", "монтаж"):
        return "WINDOW_HARDWARE", "Explicit component/hardware head object outranks the whole-window product family", "HIGH"
    if win and _has(p, "подоконник для пластиковых окон", "цена пластиковых подоконников", "пластиковые решетки на окна", "краска для алюминиевых окон") and not _has(p, "ремонт", "замена", "установ"):
        return "WINDOW_ACCESSORIES", "Explicit adjacent accessory/material head object outranks whole-window purchase", "HIGH"

    # 14) Clear selection questions before material/brand commercial fallback.
    if win and not commercial_price and _has(p, "какое окно алюминиевое", "какие окна rehau", "какие окна рехау"):
        if _has(p, "rehau", "рехау"):
            return "REHAU_SELECTION_INFO", "Explicit Rehau selection question outranks brand-product fallback", "HIGH"
        return "WINDOW_SELECTION_INFO", "Explicit window-selection question outranks material-product fallback", "HIGH"

    # 15) A few French-window boundaries are lexically explicit enough to resolve
    # without paid Search; ambiguous room/use-case phrases remain unresolved.
    if "француз" in p and _has(p, "занавес") and win:
        return "OUTSIDE_CURTAINS", "Curtain is the head object; French-window wording is context", "HIGH"
    if "француз" in p and _has(p, "задвижк") and win:
        return "WINDOW_HARDWARE", "Window latch is the head component", "HIGH"
    if "француз" in p and win and _has(p, "что значит", "название", "тип окон"):
        return "WINDOW_DEFINITION_INFO", "Explicit definition/naming task for French windows", "HIGH"
    if "француз" in p and win and _has(p, "оформление", "примеры"):
        return "DESIGN_INSPIRATION", "Explicit design/example task for French windows", "HIGH"
    if "француз" in p and win and _has(p, "устанавливаем", "установка", "монтаж"):
        return "WINDOW_INSTALLATION", "Explicit French-window installation action", "HIGH"
    if "француз" in p and win and _has(p, "вместо балконного блока", "вместо балконного"):
        return "WINDOW_REPLACEMENT_SERVICE", "Explicit conversion/replacement of a balcony block with a French window", "HIGH"
    if "француз" in p and win and _has(p, "коричнев", "черн", "распашн"):
        return "FRENCH_WINDOWS_COMMERCIAL", "Explicit French-window product/configuration modifier", "HIGH"

    # Surface treatment / assembly wording is materially distinct but not safely
    # represented by the existing service taxonomy; preserve it for Search rather
    # than forcing a product cluster.
    if win and _has(p, "покраска алюминиевых окон", "сборка алюминиевых окон"):
        return None, "Surface-treatment/assembly task is distinct from window purchase and needs boundary evidence", "LOW"

    return _v19_classifier(phrase)


b.classify_semantic = classify_v20


def self_test() -> None:
    v19.self_test()

    expected = {
        "заглушки для алюминиевых окон": "WINDOW_HARDWARE",
        "замки для алюминиевых окон": "WINDOW_HARDWARE",
        "клапана на алюминиевые окна": "WINDOW_HARDWARE",
        "направляющие для алюминиевых окон": "WINDOW_HARDWARE",
        "редуктор для алюминиевой окон": "WINDOW_HARDWARE",
        "ролики для алюминиевых окон": "WINDOW_HARDWARE",
        "механизм пластикового окна": "WINDOW_HARDWARE",
        "подоконник для пластиковых окон": "WINDOW_ACCESSORIES",
        "стеклопакеты для пластиковых окон": "WINDOW_HARDWARE",
        "теплый подставочный профиль для окон rehau": "WINDOW_HARDWARE",
        "установка пластиковой двери": "PVC_DOOR_INSTALLATION_SERVICE",
        "установка готовых пластиковых окон": "WINDOW_INSTALLATION",
        "изготовление и установка пластиковых окон": "WINDOW_INSTALLATION",
        "стоимость замены окна на пластиковые цена": "WINDOW_REPLACEMENT_SERVICE",
        "замена оконной фурнитуры": "WINDOW_REPAIR",
        "не открывается пластиковое окно": "WINDOW_REPAIR_DIY",
        "не закрывается пластиковая дверь": "PVC_DOOR_REPAIR_DIY",
        "открывание алюминиевых окон": "WINDOW_OPERATION_DIY",
        "проветривание алюминиевые окна": "WINDOW_OPERATION_DIY",
        "какое окно алюминиевое": "WINDOW_SELECTION_INFO",
        "какие окна rehau": "REHAU_SELECTION_INFO",
        "рейтинг алюминиевых окон": "WINDOW_REVIEWS_INFO",
        "панорамные окна для частного дома размеры": "WINDOW_DIMENSIONS_INFO",
        "стандартные размеры панорамных окон для частного дома": "WINDOW_DIMENSIONS_INFO",
        "панорамные окна в частном доме фото": "DESIGN_INSPIRATION",
        "французские окна на балкон фото": "DESIGN_INSPIRATION",
        "какое остекление балкона лучше выбрать": "GLAZING_SELECTION_INFO",
        "остекление балконов самому": "GLAZING_DIY_INFO",
        "разрешение на остекление балкона": "GLAZING_PERMISSION_INFO",
        "балкон без остекления": "OPEN_BALCONY_FINISHING",
        "демонтаж остекления балкона": "WINDOW_DEMOLITION",
        "профиль для остекления балконов": "WINDOW_HARDWARE",
        "поликарбонат для остекления веранды": "WINDOW_ACCESSORIES",
        "толщина монолитного поликарбоната для остекления веранды": "WINDOW_ACCESSORY_SELECTION_INFO",
        "кондиционер на балконе с остеклением": "OUTSIDE_HVAC",
        "запчасти для ремонта пластиковых окон": "WINDOW_HARDWARE",
        "клей для ремонта пластиковых окон": "WINDOW_ACCESSORIES",
        "ремонт пластиковых окон самому": "WINDOW_REPAIR_DIY",
        "ремонт откосов пластиковых окон": "WINDOW_FINISHING_SERVICE",
        "ремонт подоконников пластиковых окон": "WINDOWSILL_REPAIR",
        "французские занавески на окна": "OUTSIDE_CURTAINS",
        "французские вертикальные задвижки для окон": "WINDOW_HARDWARE",
        "французские окна название": "WINDOW_DEFINITION_INFO",
        "французское окно оформление": "DESIGN_INSPIRATION",
        "устанавливаем французские окна": "WINDOW_INSTALLATION",
        "французские окна вместо балконного блока": "WINDOW_REPLACEMENT_SERVICE",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)

    unresolved = {
        "ремонт балкона с остеклением",
        "пластиковые окна монтаж ремонт",
        "пластиковые окна после ремонта",
        "покраска алюминиевых окон",
        "сборка алюминиевых окон",
    }
    for phrase in unresolved:
        got = b.classify_semantic(phrase)
        assert got[0] is None, (phrase, got)


if __name__ == "__main__":
    self_test()
    runner.main()
