#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V33 as v33

_v33_classifier = b.classify_semantic


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def windowish(p: str) -> bool:
    return has(p, "окн", "окон", "rehau", "рехау")


def classify_v34(phrase: str):
    p = b.norm(phrase)
    win = windowish(p)
    pvc_window = "пластиков" in p and win
    pvc_door = "пластиков" in p and "двер" in p
    aluminium = "алюмини" in p and win
    rehau = has(p, "rehau", "рехау") and win
    curtain = has(p, "жалюз", "штор", "занавес", "день ночь", "плиссе")
    install = has(p, "установ", "монтаж", "поставить")
    repair = has(p, "ремонт", "регулир", "почин", "плохо закрывается", "просела", "провис")
    replace = has(p, "замена", "заменить", "поменять", "вместо")
    price = has(p, "цена", "цены", "стоимость", "сколько стоит")

    # ---- explicit information/selection outranks photo and broad product families ----
    if "что такое французское окно" in p:
        return "WINDOW_DEFINITION_INFO", "Explicit definition task outranks a trailing photo modifier", "HIGH"
    if "виды окон для частного дома" in p or "формы пластиковых окон для частного дома" in p:
        return "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO", "Explicit private-house window types/forms task outranks photo/product fallbacks", "HIGH"
    if curtain and has(p, "как правильно выбрать", "как лучше выбрать"):
        return "OUTSIDE_CURTAINS_SELECTION_INFO", "Explicit blind/curtain selection wording", "HIGH"
    if curtain and "фото" in p and not price:
        return "DESIGN_INSPIRATION", "Photo-only curtain/blind query is an inspiration/visual-reference task, not ordinary shopping", "HIGH"
    if p == "шторы на пластиковые окна без":
        return None, "Truncated negative modifier does not identify a stable curtain task", "LOW"

    # Price/commercial wording outranks photo-only inspiration when both are present.
    if pvc_window and "фото" in p and price:
        return "PVC_WINDOWS_COMMERCIAL", "Window photos plus explicit price intent form a commercial product task", "HIGH"
    if "остеклен" in p and "балкон" in p and "фото" in p and price:
        return "BALCONY_GLAZING", "Balcony-glazing photos plus explicit price intent form a commercial service task", "HIGH"

    # ---- PVC door head-object and intent boundaries ----
    if pvc_door and not install and not repair and not replace and has(p, "пластиковые окна", "окна пластиковые", "двери окна пластиковые"):
        return "WINDOW_DOOR_COMMERCIAL", "Combined window-and-door product task; neither object should swallow the other", "HIGH"
    if pvc_door and has(p, "защелк", "фиксатор"):
        return "WINDOW_HARDWARE", "Plastic-door latch/retainer is a component, not a whole door", "HIGH"
    if has(p, "наличник пластиковый на двери", "стекло для пластиковой двери"):
        return "WINDOW_HARDWARE", "Explicit plastic-door component is the head product", "HIGH"
    if pvc_door and has(p, "плохо закрывается", "просела"):
        return "PVC_DOOR_REPAIR_SERVICE", "Explicit door malfunction is a repair/adjustment task, not door purchase", "HIGH"
    if pvc_door and has(p, "лучшие пластиковые двери", "цвета пластиковых дверей"):
        return "PVC_DOOR_SELECTION_INFO", "Explicit best/colour choice task for plastic doors", "HIGH"
    if pvc_door and has(p, "внутренние пластиковые двери", "дверь в ванную", "дверь в комнату", "дверь в туалет", "дверь гармошка", "дверь купе"):
        return "OUTSIDE_INTERIOR_DOORS", "Interior-room plastic door is outside the window/PVC exterior-door core", "HIGH"
    if p in {"сделать пластиковую дверь", "корпус пластиковый прозрачная дверь", "под дверь пластиковые", "двери деревянные пластиковые", "дверь металлическая пластиковая"}:
        return None, "Phrase does not safely distinguish whole-door purchase from fabrication/material/outside-product intent", "LOW"

    # ---- explicit component/accessory head objects ----
    if pvc_window and has(p, "ключ на пластиковые окна", "крепление для пластиковых окон", "наличники для пластиковых окон", "нащельник для пластиковых окон", "ножницы на окно пластиковое", "пластиковые наличники на окна", "пластиковый наличник на окно", "рама пластикового окна", "стекло на пластиковое окно", "цена замка на пластиковое окно"):
        return "WINDOW_HARDWARE", "Explicit window component is the head product, not a whole PVC window", "HIGH"
    if pvc_window and "от комаров" in p:
        return "MOSQUITO_NETS", "Mosquito protection is the head accessory task", "HIGH"
    if pvc_window and "плиссе" in p:
        return "OUTSIDE_CURTAINS", "Pleated blind/shade is the head outside-core product", "HIGH"
    if rehau and "соединител" in p:
        return "WINDOW_HARDWARE", "Explicit Rehau connector is a component rather than a whole window", "HIGH"
    if aluminium and "алюминиевые рамы для окон" in p:
        return "WINDOW_HARDWARE", "Aluminium window frame is a component/head product distinct from whole-window purchase", "HIGH"

    # ---- broad-product informational leakage ----
    if pvc_window and has(p, "лучшие пластиковые окна", "правильные пластиковые окна", "цвета пластиковых окон") and "лучшие цены" not in p:
        return "WINDOW_SELECTION_INFO", "Explicit best/correct/colour selection task for PVC windows", "HIGH"
    if pvc_window and "стандарты пластиковых окон для частного дома" in p:
        return "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO", "Standards for private-house PVC windows are a requirements task", "HIGH"
    if pvc_window and has(p, "производители пластиковых окон", "пластиковые окна от заводов производителей", "пластиковые окна от производителей без установки", "завод пластиковых окон"):
        return "PVC_WINDOWS_MANUFACTURER", "Explicit manufacturer/provider task for PVC windows", "HIGH"
    if p == "производство пластиковых окон":
        return None, "Bare production wording may mean manufacturing process or manufacturer/provider intent", "LOW"
    if p in {"закроем пластиковые окна", "сверление пластикового окна"}:
        return None, "Action fragment does not identify a stable purchase/service user task", "LOW"

    if aluminium and has(p, "серии алюминиевых окон", "системы алюминиевых окон", "цвета алюминиевых окон", "хорошие алюминиевые окна"):
        return "WINDOW_SELECTION_INFO", "Explicit series/system/colour/quality choice task for aluminium windows", "HIGH"
    if p in {"работа алюминиевые окна", "без алюминиевой окна", "алюминиевые окна остекление", "остекление раздвижными алюминиевыми окнами", "цены окна алюминиевые профили"}:
        return None, "Mixed/fragment aluminium-window wording does not safely identify product versus service/component intent", "LOW"

    if rehau and "лучшие пластиковые окна rehau" in p:
        return "REHAU_SELECTION_INFO", "Explicit quality/selection task for Rehau windows", "HIGH"
    if rehau and "окна rehau цвета" in p:
        return "REHAU_SELECTION_INFO", "Explicit Rehau colour-selection task", "HIGH"
    if p == "мансардное окно rehau":
        return None, "Brand/product-family compatibility is not safe to assume from the phrase alone", "LOW"

    # Whole-window glass-unit selection is still an accessory/component choice.
    if "как выбрать стеклопакет для пластиковых окон" in p:
        return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit glazing-unit selection task, not whole-window selection", "HIGH"
    if "логотипы оконной фурнитуры" in p:
        return "WINDOW_TECH_INFO", "Hardware-logo identification is technical/reference information rather than selection", "HIGH"

    # ---- private-house and panoramic boundaries ----
    if p == "окна в пол для частного дома":
        return "PANORAMIC_WINDOWS_COMMERCIAL", "Floor-to-ceiling windows are a panoramic-window product use case", "HIGH"
    if p == "проем для окна в частном доме" or p == "стандарт окна для частного дома":
        return "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO", "Opening/standard wording is a construction requirement rather than window purchase", "HIGH"
    if p == "современные окна для частного дома":
        return "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO", "Modern-window wording is a private-house style/selection task", "HIGH"
    if p == "панорамные окна в лесу подмосковье":
        return "OUTSIDE_REAL_ESTATE", "Forest/location context matches the direct Step-09 real-estate/inspiration boundary for panoramic windows", "HIGH"
    if p == "крыльцо для частного дома с панорамными окнами":
        return "PORCH_GLAZING", "Porch is the head object; panoramic windows specify its glazing configuration", "HIGH"
    if p == "окна сок панорамное раздвижное остекление":
        return None, "Brand/abbreviation plus panoramic sliding-glazing wording is not safe product-versus-service evidence", "LOW"
    if p in {"угловое панорамное окно", "фасадные панорамные окна"}:
        return "PANORAMIC_WINDOWS_COMMERCIAL", "Explicit panoramic-window subtype/configuration product task", "HIGH"
    if p == "теплый пол панорамные окна":
        return "OUTSIDE_HEATING", "Underfloor heating is the head system; panoramic windows are context", "HIGH"
    if p == "капитальный ремонт замена пластиковых окон":
        return "WINDOW_REPLACEMENT_SERVICE", "Capital-renovation context still contains an explicit whole-window replacement service", "HIGH"
    if p == "французские окна в квартире":
        return "FRENCH_WINDOWS_COMMERCIAL", "Window-headed apartment use case remains the French-window product task", "HIGH"

    # ---- balcony-glazing specializations and information ----
    if "остеклен" in p and "балкон" in p and has(p, "серии", "серия", "дома серии", "балконов серии"):
        return "BALCONY_GLAZING_HOUSE_SERIES", "Explicit house-series balcony-glazing task", "HIGH"
    if "остеклен" in p and "балкон" in p and "лучшие компании" in p:
        return "WINDOW_REVIEWS_INFO", "Best-company wording is provider ranking/review information, not the glazing action itself", "HIGH"
    if p == "остекление балкона правильно":
        return "GLAZING_DIY_INFO", "Proper-glazing wording is procedural information rather than a service order", "HIGH"

    # ---- finishing boundaries ----
    if p == "откосы после установки пластиковых окон":
        return "WINDOW_FINISHING_INFO", "Post-installation slopes wording is informational without a service action", "HIGH"
    if p in {"цена откосов на окно пластиковое", "цена отливов на пластиковые окна"}:
        return None, "Price-only slope/ebb wording does not safely distinguish material/product price from installation service", "LOW"

    # ---- installation / measurement / finance / accessory precedence ----
    if install and has(p, "рассроч", "кредит", "халва") and win:
        return "WINDOW_FINANCE", "Finance is the decision-driving intent; installation is a bundled modifier", "HIGH"
    if p in {"клинья для установки пластиковых окон", "пена установки пластиковых окон"}:
        return "WINDOW_ACCESSORIES", "Installation material is the head product, not installation service", "HIGH"
    if "установка ограничителя" in p and win:
        return "WINDOW_HARDWARE_INSTALLATION_SERVICE", "Installation targets a window limiter/component", "HIGH"
    if "установка сеток на пластиковые окна" in p:
        return "MOSQUITO_NET_INSTALLATION_SERVICE", "Installation targets window nets, not whole windows", "HIGH"
    if "установка остекления балкона" in p or p == "установка балкона цена остекление балкона":
        return "BALCONY_GLAZING", "Balcony glazing is the head service; installation wording is generic", "HIGH"
    if p == "установка окон и остекление балконов":
        return None, "Phrase combines two material services and should not be forced into one task without boundary evidence", "LOW"
    if "установка французского окна вместо балконного блока" in p:
        return "WINDOW_REPLACEMENT_SERVICE", "Replacing a balcony block with a French window is a whole-opening replacement task", "HIGH"
    if pvc_window and "без установки" in p:
        return "PVC_WINDOWS_COMMERCIAL", "Installation is explicitly negated; the remaining task is window purchase", "HIGH"
    if p in {"заказ окон пластиковых с замером и установкой", "замер и установка пластиковых окон москва", "пластиковые окна установка цена с размерами"}:
        return "WINDOW_INSTALLATION", "Explicit commercial order/geo/price bundle makes measurement a service modifier rather than the head information task", "HIGH"
    if p == "установка пластиковых окон фото":
        return "WINDOW_INSTALLATION_INFO", "Installation photos are procedural/reference information without explicit DIY or service-order intent", "HIGH"
    if p == "установка пластиковых окон лучшие":
        return "WINDOW_REVIEWS_INFO", "Best-installation wording is provider/service evaluation information", "HIGH"
    if p == "заделать окна установки пластиковых окон":
        return "WINDOW_FINISHING_SERVICE", "Sealing/finishing around installed windows is the head service action", "MEDIUM"
    if p in {"пластиковые окна наружной установки", "установка пластиковых окон день", "установка пластиковых окон метр", "установленное пластиковое окно"}:
        return None, "State/fragment installation wording is not enough to infer a stable service task", "LOW"

    # Window-net repair must not remain generic window repair.
    if "ремонт оконных сеток" in p or "ремонт москит" in p or "ремонт сетки" in p:
        return "MOSQUITO_NET_REPAIR_SERVICE", "Repair targets a window net rather than the window itself", "HIGH"

    return _v33_classifier(phrase)


b.classify_semantic = classify_v34


def expect(mapping: dict[str, str]) -> None:
    for phrase, task in mapping.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


def unresolved(phrases: set[str]) -> None:
    for phrase in phrases:
        got = b.classify_semantic(phrase)
        assert got[0] is None, (phrase, got)


def self_test() -> None:
    v33.self_test()
    expect({
        "как правильно выбрать жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_SELECTION_INFO",
        "французские жалюзи на окна фото": "DESIGN_INSPIRATION",
        "шторы на панорамные окна фото": "DESIGN_INSPIRATION",
        "что такое французское окно в квартире фото": "WINDOW_DEFINITION_INFO",
        "виды окон для частного дома фото": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "фото цены на пластиковые окна": "PVC_WINDOWS_COMMERCIAL",
        "пластиковые окна на кухню фото цена": "PVC_WINDOWS_COMMERCIAL",
        "остекление балконов фото цены": "BALCONY_GLAZING",
        "защелка для пластиковой двери": "WINDOW_HARDWARE",
        "стекло для пластиковой двери": "WINDOW_HARDWARE",
        "плохо закрывается пластиковая дверь": "PVC_DOOR_REPAIR_SERVICE",
        "просела пластиковая дверь": "PVC_DOOR_REPAIR_SERVICE",
        "лучшие пластиковые двери": "PVC_DOOR_SELECTION_INFO",
        "цвета пластиковых дверей": "PVC_DOOR_SELECTION_INFO",
        "внутренние пластиковые двери": "OUTSIDE_INTERIOR_DOORS",
        "пластиковая дверь гармошка": "OUTSIDE_INTERIOR_DOORS",
        "пластиковая дверь в ванную": "OUTSIDE_INTERIOR_DOORS",
        "пластиковые окна и двери": "WINDOW_DOOR_COMMERCIAL",
        "пластиковые окна с балконной дверью": "WINDOW_DOOR_COMMERCIAL",
        "ключ на пластиковые окна цена": "WINDOW_HARDWARE",
        "крепление для пластиковых окон": "WINDOW_HARDWARE",
        "наличники для пластиковых окон": "WINDOW_HARDWARE",
        "ножницы на окно пластиковое цена": "WINDOW_HARDWARE",
        "рама пластикового окна": "WINDOW_HARDWARE",
        "стекло на пластиковое окно цена": "WINDOW_HARDWARE",
        "от комаров на окна пластиковые": "MOSQUITO_NETS",
        "плиссе на пластиковые окна": "OUTSIDE_CURTAINS",
        "соединители под 45 градусов для окон rehau": "WINDOW_HARDWARE",
        "алюминиевые рамы для окон": "WINDOW_HARDWARE",
        "лучшие пластиковые окна": "WINDOW_SELECTION_INFO",
        "цвета пластиковых окон": "WINDOW_SELECTION_INFO",
        "стандарты пластиковых окон для частного дома": "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO",
        "производители пластиковых окон": "PVC_WINDOWS_MANUFACTURER",
        "пластиковые окна от заводов производителей": "PVC_WINDOWS_MANUFACTURER",
        "серии алюминиевых окон": "WINDOW_SELECTION_INFO",
        "системы алюминиевых окон": "WINDOW_SELECTION_INFO",
        "цвета алюминиевых окон": "WINDOW_SELECTION_INFO",
        "лучшие пластиковые окна rehau": "REHAU_SELECTION_INFO",
        "окна rehau цвета": "REHAU_SELECTION_INFO",
        "как выбрать стеклопакет для пластиковых окон": "WINDOW_ACCESSORY_SELECTION_INFO",
        "логотипы оконной фурнитуры": "WINDOW_TECH_INFO",
        "окна в пол для частного дома": "PANORAMIC_WINDOWS_COMMERCIAL",
        "проем для окна в частном доме": "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO",
        "стандарт окна для частного дома": "PRIVATE_HOUSE_WINDOW_REQUIREMENTS_INFO",
        "современные окна для частного дома": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "панорамные окна в лесу подмосковье": "OUTSIDE_REAL_ESTATE",
        "крыльцо для частного дома с панорамными окнами": "PORCH_GLAZING",
        "угловое панорамное окно": "PANORAMIC_WINDOWS_COMMERCIAL",
        "фасадные панорамные окна": "PANORAMIC_WINDOWS_COMMERCIAL",
        "теплый пол панорамные окна": "OUTSIDE_HEATING",
        "капитальный ремонт замена пластиковых окон": "WINDOW_REPLACEMENT_SERVICE",
        "французские окна в квартире": "FRENCH_WINDOWS_COMMERCIAL",
        "остекление балконов серии п": "BALCONY_GLAZING_HOUSE_SERIES",
        "лучшие компании по остеклению балконов": "WINDOW_REVIEWS_INFO",
        "остекление балкона правильно": "GLAZING_DIY_INFO",
        "откосы после установки пластиковых окон": "WINDOW_FINISHING_INFO",
        "окна в рассрочку с установкой недорого": "WINDOW_FINANCE",
        "клинья для установки пластиковых окон": "WINDOW_ACCESSORIES",
        "пена установки пластиковых окон": "WINDOW_ACCESSORIES",
        "установка ограничителя на пластиковые окна": "WINDOW_HARDWARE_INSTALLATION_SERVICE",
        "установка сеток на пластиковые окна москва": "MOSQUITO_NET_INSTALLATION_SERVICE",
        "установка остекления балкона": "BALCONY_GLAZING",
        "установка французского окна вместо балконного блока": "WINDOW_REPLACEMENT_SERVICE",
        "цена пластиковых окон без установки": "PVC_WINDOWS_COMMERCIAL",
        "замер и установка пластиковых окон москва": "WINDOW_INSTALLATION",
        "заказ окон пластиковых с замером и установкой": "WINDOW_INSTALLATION",
        "пластиковые окна установка цена с размерами": "WINDOW_INSTALLATION",
        "установка пластиковых окон размером": "WINDOW_MEASUREMENT_INFO",
        "установка пластиковых окон фото": "WINDOW_INSTALLATION_INFO",
        "установка пластиковых окон лучшие": "WINDOW_REVIEWS_INFO",
        "ремонт оконных сеток для пластиковых окон": "MOSQUITO_NET_REPAIR_SERVICE",
    })
    unresolved({
        "шторы на пластиковые окна без",
        "сделать пластиковую дверь",
        "корпус пластиковый прозрачная дверь",
        "под дверь пластиковые",
        "двери деревянные пластиковые",
        "дверь металлическая пластиковая",
        "производство пластиковых окон",
        "закроем пластиковые окна",
        "сверление пластикового окна",
        "работа алюминиевые окна",
        "без алюминиевой окна",
        "алюминиевые окна остекление",
        "остекление раздвижными алюминиевыми окнами",
        "цены окна алюминиевые профили",
        "мансардное окно rehau",
        "окна сок панорамное раздвижное остекление",
        "цена откосов на окно пластиковое",
        "цена отливов на пластиковые окна",
        "установка окон и остекление балконов",
        "пластиковые окна наружной установки",
        "установка пластиковых окон день",
        "установка пластиковых окон метр",
        "установленное пластиковое окно",
    })


if __name__ == "__main__":
    self_test()
    runner.main()
