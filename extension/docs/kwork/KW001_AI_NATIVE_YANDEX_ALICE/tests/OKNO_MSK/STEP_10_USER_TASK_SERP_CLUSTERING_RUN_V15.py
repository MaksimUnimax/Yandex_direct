#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V9 as v9mod
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V14  # noqa: F401,E402

_v14_classifier = b.classify_semantic
_pre_private_classifier = v9mod._v8_classifier

b.TASKS.update({
    "OUTSIDE_ENTRY_DOORS": ("Входные двери с окном как отдельный товар", "OUTSIDE_CORE", "OUTSIDE"),
    "WINDOW_DOOR_COMMERCIAL": ("Покупка окон и балконных/ПВХ-дверей", "COMMERCIAL_PRODUCT", "FIT"),
    "HOUSE_SERIES_WINDOWS_COMMERCIAL": ("Окна/балконные блоки по серии дома", "COMMERCIAL_PRODUCT", "FIT"),
    "OUTDOOR_GLAZING_MULTI_OBJECT": ("Остекление веранд/террас/беседок: смешанный объект", "COMMERCIAL_SERVICE", "FIT"),
})


def n(text: str) -> str:
    return " ".join((text or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "стеклопак", "остеклен", "застекл")


def is_private_house(p: str) -> bool:
    return has(
        p,
        "частного дома", "частных домов", "частный дом", "частные дома", "частном доме",
        "загородного дома", "загородный дом", "загородных домов", "для дома",
    )


def is_house_series(p: str) -> bool:
    return bool(re.search(r"\bп\s*[- ]?\s*\d{1,3}\s*[а-я]?\b", p))


def architecture_subject_with_windows(p: str) -> bool:
    # The dwelling/project is the head object: 'квартира с панорамными окнами',
    # 'проекты домов с панорамными окнами', etc. This deliberately does not match
    # window-headed phrases such as 'французское окно на балкон в квартире'.
    return bool(re.search(
        r"\b(?:дом\w*|квартир\w*|кв|комнат\w*|спальн\w*|кухн\w*|зал|лофт\w*|бан\w*|"
        r"апартамент\w*|пристройк\w*|беседк\w*|гостин\w*|одноэтажн\w*|проект\w*)\b"
        r".{0,45}\bс\b.{0,35}(?:панорам|француз)",
        p,
    ))


def object_glazing_task(p: str):
    glazing = has(p, "остеклен", "застекл")
    if not glazing:
        return None

    # Content/procedure/selection intent beats the service object.
    if has(p, "что такое", "как называется", "как называются"):
        return None
    if has(p, "фото", "дизайн", "красив", "интерьер"):
        return "DESIGN_INSPIRATION", "Explicit photo/design intent around an object-specific glazing task", "HIGH"
    if has(p, "своими руками", "самостоятель", "как сделать", "как застеклить", "как остеклить", "пошаг"):
        return "GLAZING_DIY_INFO", "Explicit DIY/procedural glazing task", "HIGH"
    if has(p, "плюсы", "минусы", "сравн", "что лучше", "какое лучше", "виды", "варианты", "как выбрать", "выбрать остекление"):
        return "GLAZING_SELECTION_INFO", "Explicit comparison/selection task for glazing variants", "HIGH"
    if has(p, "конструкция", "устройство", "схема"):
        return "WINDOW_TECH_INFO", "Explicit technical/construction information task for glazing", "HIGH"

    if has(p, "безрам", "бескаркас"):
        return "FRAMELESS_GLAZING", "Explicit frameless glazing service", "HIGH"

    groups = []
    if has(p, "балкон", "лоджи"):
        groups.append("BALCONY")
    if "веранд" in p:
        groups.append("VERANDA")
    if "террас" in p:
        groups.append("TERRACE")
    if "бесед" in p:
        groups.append("GAZEBO")
    if "крыльц" in p:
        groups.append("PORCH")

    groups = list(dict.fromkeys(groups))
    if len(groups) > 1:
        return "OUTDOOR_GLAZING_MULTI_OBJECT", "Explicit glazing service spans multiple outdoor object types; keep one mixed-object service task instead of forcing one object", "HIGH"
    if not groups:
        return None

    group = groups[0]
    if group == "BALCONY":
        if has(p, "деревян", "деревянными рам", "деревянных рам"):
            return "BALCONY_GLAZING_WOOD", "Balcony/loggia glazing with wooden-frame material remains a glazing service", "HIGH"
        if "тепл" in p:
            return "BALCONY_GLAZING_WARM", "Explicit warm balcony/loggia glazing subtype", "HIGH"
        if "холод" in p:
            return "BALCONY_GLAZING_COLD", "Explicit cold balcony/loggia glazing subtype", "HIGH"
        if has(p, "с крыш", "крышей"):
            return "BALCONY_GLAZING_ROOF", "Explicit roof balcony/loggia glazing subtype", "HIGH"
        if "вынос" in p:
            return "BALCONY_GLAZING_EXTENSION", "Explicit balcony/loggia glazing with extension", "HIGH"
        if is_house_series(p):
            return "BALCONY_GLAZING_HOUSE_SERIES", "Explicit balcony/loggia glazing for a house-series modifier", "HIGH"
        return "BALCONY_GLAZING", "Explicit balcony/loggia glazing service; panoramic/material/private-house wording is only a modifier", "HIGH"
    if group == "VERANDA":
        return "VERANDA_GLAZING", "Explicit veranda glazing service; panoramic/material/private-house wording is only a modifier", "HIGH"
    if group == "TERRACE":
        return "TERRACE_GLAZING", "Explicit terrace glazing service; panoramic/material/private-house wording is only a modifier", "HIGH"
    if group == "GAZEBO":
        return "GAZEBO_GLAZING", "Explicit gazebo glazing service", "HIGH"
    if group == "PORCH":
        return "PORCH_GLAZING", "Explicit porch glazing service", "HIGH"
    return None


def classify_v15(phrase: str):
    p = n(phrase)
    win = windowish(p)
    panoramic = "панорам" in p and win
    french = "француз" in p and (win or "балконный блок" in p)
    soft = "мягк" in p and win
    private_house = is_private_house(p)

    # Strong object classes must survive every panoramic/French/private-house overlay.
    if has(p, "штор", "жалюзи", "рулонн", "день ночь"):
        return "OUTSIDE_CURTAINS", "Curtain/blind task remains separate from the window product", "HIGH"
    if has(p, "радиатор", "батаре", "конвектор", "отоплен") and win:
        return "OUTSIDE_HEATING", "Heating/radiator/convector task remains outside the window-purchase core", "HIGH"

    # A component/accessory of a soft/panoramic/French window is not the whole-window product.
    if (soft or panoramic or french) and has(p, "замок", "фурнитур", "ручк", "петл", "створк", "решетк", "раскладк", "шпрос"):
        return "WINDOW_HARDWARE", "Explicit window component/hardware task beats the whole-window product family", "HIGH"
    if (panoramic or french) and has(p, "ставн", "огражден", "подоконник"):
        return "WINDOW_ACCESSORIES", "Explicit accessory/adjacent component task beats the whole-window product family", "HIGH"

    # Soft windows are a dedicated product only after component intent was excluded.
    if soft:
        return "SOFT_WINDOWS_COMMERCIAL", "Explicit soft-window product task", "HIGH"

    # Non-PVC entrance doors with a window are a door product, not a window-purchase task.
    if "входн" in p and "двер" in p and not has(p, "пластик", "пвх"):
        return "OUTSIDE_ENTRY_DOORS", "Explicit entrance-door product with a window; the door is the head object", "HIGH"

    # Mixed windows+doors purchase demand must not be reduced to the door-only cluster.
    commercial = has(p, "купить", "заказать", "цена", "цены", "стоимость", "сколько стоит", "сколько стоят")
    if has(p, "окн", "окон") and "двер" in p and commercial and not has(p, "установ", "монтаж", "ремонт", "регулир"):
        return "WINDOW_DOOR_COMMERCIAL", "Explicit combined purchase/price task for windows and doors", "HIGH"

    # Whole-window replacement/conversion is a service. Preserve the existing mixed
    # repair+replacement boundary instead of forcing one service family.
    whole_replacement = has(
        p,
        "замена окна", "замена окон", "замена пластиковых окон", "замена панорамных окон", "замена французских окон",
        "заменить окно", "заменить окна", "поменять окно", "поменять окна", "замена балконного блока",
    )
    if win and "ремонт" in p and whole_replacement:
        return None, "Phrase explicitly mixes repair and whole-window replacement; keep the boundary visible", "LOW"
    if whole_replacement and (win or french):
        return "WINDOW_REPLACEMENT_SERVICE", "Explicit whole-window/balcony-block replacement or conversion service", "HIGH"

    # Repair/adjustment beats panoramic/French product overlays.
    if win and has(p, "ремонт", "регулир", "провис", "почин", "сломал"):
        if has(p, "своими руками", "самостоятель", "как ", "видео", "инструк"):
            return "WINDOW_REPAIR_DIY", "Explicit DIY/diagnostic window repair task", "HIGH"
        return "WINDOW_REPAIR", "Explicit window repair/adjustment service task", "HIGH"

    # Object-specific glazing beats material/product/private-house semantics.
    glazing_result = object_glazing_task(p)
    if glazing_result is not None:
        return glazing_result

    # A naming question about the dwelling/project is not a definition of the window.
    if (panoramic or french) and "дом" in p and has(p, "как называется", "как называются", "что за дом", "тип дома", "вид дома"):
        return "OUTSIDE_REAL_ESTATE", "Naming/classifying a house with panoramic/French windows is an architecture/real-estate task", "HIGH"

    # Window definition/naming itself, including plural wording.
    if (panoramic or french) and has(p, "что такое", "как называется", "как называются", "как зовется"):
        return "WINDOW_DEFINITION_INFO", "Explicit definition/naming task for the window type", "HIGH"

    # Design/photo intent before architecture/product routing.
    if (panoramic or french) and has(p, "фото", "дизайн", "дизайны", "красив", "интерьер", "стиль", "имитац"):
        return "DESIGN_INSPIRATION", "Explicit design/photo/inspiration task around panoramic/French windows", "HIGH"

    # Strong dwelling/project-headed context remains outside the window-purchase core.
    if (panoramic or french) and architecture_subject_with_windows(p):
        return "OUTSIDE_REAL_ESTATE", "The dwelling/project is the head object; panoramic/French windows are an architecture/interior attribute", "HIGH"

    # Explicit dimensions beat product/material/use-case routing. Numeric dimensions
    # are accepted only with strong format cues, avoiding fragments such as '6 6 с ...'.
    dim_words = has(p, "размер", "ширина", "высота", "габарит")
    dim_pattern = bool(re.search(r"\b\d+(?:[.,]\d+)?\s*(?:на|x|х)\s*\d+(?:[.,]\d+)?\b", p))
    pan_decimal = bool(re.search(r"(?:панорам\w*\s+окн\w*|окн\w*\s+панорам\w*)\s+\d+[.,]\d+\b", p))
    if win and (dim_words or dim_pattern or pan_decimal) and not has(p, "купить", "заказать", "цена", "цены", "стоимость", "установ", "монтаж"):
        return "WINDOW_DIMENSIONS_INFO", "Explicit window size/dimension information task", "HIGH"

    # Informational 'types/variants' must not fall into a generic material-product cluster.
    if panoramic or french:
        if has(p, "виды", "варианты", "плюсы", "минусы", "лучшие", "лучше", "какие", "как выбрать", "сравн", "почему", "особенности"):
            return "PANORAMIC_WINDOWS_INFO", "Explicit informational/selection task about panoramic/French windows", "HIGH"

    # Clear French-window product/configuration demand. Apartment/balcony wording is
    # a use-case modifier unless the dwelling itself is syntactically the head object.
    if french:
        french_product = has(
            p,
            "купить", "заказать", "цена", "цены", "стоимость", "сколько стоит", "сколько стоят",
            "производ", "москва", "подмосков", "на балкон", "балконный блок", "ароч", "стеклопак",
            "пластиков", "пвх", "алюмини", "деревян", "готов", "больш", "высок", "маленьк", "широк", "узк",
        )
        if p in {"французские окна", "французское окно"} or french_product:
            return "FRENCH_WINDOWS_COMMERCIAL", "Explicit French-window product/configuration demand", "HIGH"

    # Clear panoramic-window commercial/product signals.
    if panoramic:
        panoramic_product = has(
            p,
            "купить", "заказать", "цена", "цены", "стоимость", "сколько стоит", "сколько стоят",
            "производ", "под ключ", "москва", "подмосков", "раздвиж", "открывающ", "треугольн", "стеклянн",
            "стеклопак", "в пол", "с двер", "на крыш", "на террас", "на балкон", "на лоджи", "для загородного дома",
            "готов", "больш", "высок", "маленьк", "широк", "узк", "элитн", "пластиков", "алюмини", "деревян",
        )
        if p in {"панорамные окна", "панорамное окно"} or panoramic_product:
            return "PANORAMIC_WINDOWS_COMMERCIAL", "Explicit panoramic-window product/purchase/configuration task", "HIGH"

    # House-series window demand is a distinct product/use-case task. Balcony-glazing
    # series phrases were already handled by object_glazing_task above.
    if win and is_house_series(p):
        return "HOUSE_SERIES_WINDOWS_COMMERCIAL", "Explicit window/blocks demand for a named house series", "HIGH"

    # Private-house fallback is last among material/action/type rules.
    if private_house:
        if has(p, "rehau", "рехау") and has(p, "профил", "систем") and has(p, "выбрать", "выбор", "какой"):
            return "REHAU_SELECTION_INFO", "Explicit Rehau profile/system selection task in a private-house use case", "HIGH"
        if has(p, "требован", "норматив", "норма ", "вентиляц", "котельн", "газов", "какое должно", "какой должен", "площадь остекления") and not commercial:
            return "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO", "Explicit requirements/special-condition information task for a private-house window", "HIGH"
        if has(p, "вариант", "виды", "какие окна", "какое окно", "лучшие окна", "лучшее окно", "образц", "как выбрать", "выбрать", "выбираем", "выбор"):
            return "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO", "Explicit private-house window selection/types task", "HIGH"

        specific = _pre_private_classifier(phrase)
        if specific[0] is not None:
            return specific
        return "PRIVATE_HOUSE_WINDOWS_COMMERCIAL", "Generic window product/use-case demand for a private house after specific object/material/action tasks were excluded", "MEDIUM"

    # General window types/variants are informational unless a stronger task above applies.
    if win and has(p, "виды", "варианты") and not commercial and not has(p, "установ", "монтаж", "ремонт", "регулир"):
        return "WINDOW_TECH_INFO", "Explicit window types/variants information task", "HIGH"

    return _v14_classifier(phrase)


b.classify_semantic = classify_v15


def self_test() -> None:
    expected = {
        # V14/V13 non-repeat controls.
        "окна пвх для частного дома": "PVC_WINDOWS_COMMERCIAL",
        "размеры окон пвх для частного дома": "WINDOW_DIMENSIONS_INFO",
        "установка окон пвх в частном доме": "WINDOW_INSTALLATION",
        "ремонт окон пвх в частном доме": "WINDOW_REPAIR",
        "крыльцо для частного дома окна": "PORCH_GLAZING",
        "деревянные окна для частного дома": "WOOD_WINDOWS_COMMERCIAL",
        "алюминиевые окна для частного дома": "ALUMINIUM_WINDOWS_COMMERCIAL",
        # Manual-QA failures discovered after V14.
        "дом треугольный как называется с панорамными окнами": "OUTSIDE_REAL_ESTATE",
        "застекление веранды в частном доме панорамное остекление": "VERANDA_GLAZING",
        "деревянное остекление веранды": "VERANDA_GLAZING",
        "остекление веранды в деревянном доме": "VERANDA_GLAZING",
        "панорамное остекление веранды": "VERANDA_GLAZING",
        "панорамное остекление балкона": "BALCONY_GLAZING",
        "виды пластиковых окон": "WINDOW_TECH_INFO",
        "французский замок для мягких окон": "WINDOW_HARDWARE",
        "входные двери с окном для частного дома": "OUTSIDE_ENTRY_DOORS",
        "цены на пластиковые окна балконные двери": "WINDOW_DOOR_COMMERCIAL",
        "французские окна в частном доме цена": "FRENCH_WINDOWS_COMMERCIAL",
        "цена панорамных окон для дома": "PANORAMIC_WINDOWS_COMMERCIAL",
        "французское окно на балкон в квартире": "FRENCH_WINDOWS_COMMERCIAL",
        "французские окна в москве в квартирах": "FRENCH_WINDOWS_COMMERCIAL",
        "сколько стоит панорамное окно": "PANORAMIC_WINDOWS_COMMERCIAL",
        "сколько стоят французские окна": "FRENCH_WINDOWS_COMMERCIAL",
        "ремонт панорамных окон": "WINDOW_REPAIR",
        "раздвижные панорамные окна": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамные окна москва": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамные окна под ключ": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамные окна производство": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамные окна как называются": "WINDOW_DEFINITION_INFO",
        "проекты домов с панорамными окнами": "OUTSIDE_REAL_ESTATE",
        "спальня с панорамными окнами": "OUTSIDE_REAL_ESTATE",
        "пристройка с панорамными окнами": "OUTSIDE_REAL_ESTATE",
        "панорамное окно 3 на 3": "WINDOW_DIMENSIONS_INFO",
        "окно панорамное 2.5": "WINDOW_DIMENSIONS_INFO",
        "створки панорамного окна": "WINDOW_HARDWARE",
        "ставни для французского окна": "WINDOW_ACCESSORIES",
        "подоконник французского окна": "WINDOW_ACCESSORIES",
        "окна французская решетка": "WINDOW_HARDWARE",
        "замена балконного блока на французское окно": "WINDOW_REPLACEMENT_SERVICE",
        "балконный блок французское окно": "FRENCH_WINDOWS_COMMERCIAL",
        "панорамное окно с дверью": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамное окно на крыше": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамное окно в пол": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамные окна для загородного дома": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамное окно открывающееся": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамное треугольное окно": "PANORAMIC_WINDOWS_COMMERCIAL",
        "стеклянные панорамные окна": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамное окно стеклопакет": "PANORAMIC_WINDOWS_COMMERCIAL",
        "ограждение панорамных окон": "WINDOW_ACCESSORIES",
        "панорамные окна на террасу": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамные окна подмосковье": "PANORAMIC_WINDOWS_COMMERCIAL",
        "панорамные окна с дверью в частном": "PANORAMIC_WINDOWS_COMMERCIAL",
        "заказать окна в однушку п 44": "HOUSE_SERIES_WINDOWS_COMMERCIAL",
        "окна серии п 44": "HOUSE_SERIES_WINDOWS_COMMERCIAL",
        "образцы окон для частных домов": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "окон в котельной требования для частных домов": "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO",
        "окна для кухни частном доме": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "окна для крыши частных домов": "PRIVATE_HOUSE_WINDOWS_COMMERCIAL",
        "видно про раздвижное остекление террас веранд беседок": "OUTDOOR_GLAZING_MULTI_OBJECT",
    }
    for phrase, task in expected.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)

    intentionally_ambiguous = {
        "ремонт и замена пластиковых окон",
        "замена балкона на пластиковые окна цена",
        "панорамные окна 2 2",
        "панорамные окна пик",
    }
    for phrase in intentionally_ambiguous:
        got = b.classify_semantic(phrase)
        assert got[0] is None, (phrase, got)


if __name__ == "__main__":
    self_test()
    runner.main()
