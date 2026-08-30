#!/usr/bin/env python3
from __future__ import annotations

import re

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V27 as v27

_v27_classifier = b.classify_semantic

b.TASKS.update({
    "OUTSIDE_CURTAINS_SELECTION_INFO": ("Выбор штор/жалюзи для окон", "INFORMATIONAL", "OUTSIDE"),
    "OUTSIDE_CURTAINS_REPAIR_SERVICE": ("Ремонт штор/жалюзи на окнах", "COMMERCIAL_SERVICE", "OUTSIDE"),
    "MOSQUITO_NET_SELECTION_INFO": ("Выбор москитной/защитной сетки", "INFORMATIONAL", "ADJACENT"),
    "MOSQUITO_NET_REPAIR_SERVICE": ("Ремонт/замена москитной или защитной сетки", "COMMERCIAL_SERVICE", "ADJACENT"),
    "WINDOW_REPLACEMENT_DIY": ("Самостоятельная замена окна", "INFORMATIONAL", "ADJACENT"),
    "BALCONY_GLAZING_REPLACEMENT_SERVICE": ("Замена существующего балконного остекления", "COMMERCIAL_SERVICE", "FIT"),
    "WINDOWSILL_REPAIR_DIY": ("Самостоятельный ремонт подоконника", "INFORMATIONAL", "ADJACENT"),
    "WINDOW_INSTALLATION_INFO": ("Информация и требования по установке окон", "INFORMATIONAL", "ADJACENT"),
})


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def classify_v28(phrase: str):
    p = b.norm(phrase)
    win = "окн" in p or "rehau" in p or "рехау" in p
    pvc_window = "пластиков" in p and "окн" in p
    pvc_door = "пластиков" in p and "двер" in p
    balcony = has(p, "балкон", "лоджи")
    glazing = has(p, "остеклен", "застекл")
    install = has(p, "установ", "монтаж", "поставить")
    repair = has(p, "ремонт", "регулир", "почин", "не закрывается", "не открывается")
    replace = has(p, "замена", "заменить", "поменять")
    diy = has(p, "своими руками", "самостоятель", "самому")
    curtains = has(p, "жалюз", "штор", "занавес")
    mosquito = has(p, "москит", "антикош", "противомоскит", "сетка на", "сетки на", "сетку на", "сетка для", "сетки для", "сетку для")
    selection = has(p, "как выбрать", "какие выбрать", "какую выбрать", "какой выбрать", "лучше выбрать")

    # Extended navigation markers uncovered by full manual review.
    if has(p, "rehau", "рехау") and has(p, "официаль", "сайт", "дилер", "офис", "партнер", "rehau ru"):
        return "REHAU_NAVIGATION", "Explicit Rehau site/dealer/office/partner navigation task", "HIGH"
    if has(p, "адрес", "телефон", "номер ремонта", "номер телефона") and has(p, "ремонт", "установ", "монтаж", "остеклен", "пластиковые окна"):
        return "WINDOW_SERVICE_NAVIGATION", "Explicit contact/address navigation for a window service", "HIGH"

    # Curtains/blinds are outside the window core; explicit action/selection must
    # outrank both French-window and generic hardware rules.
    if curtains:
        if repair:
            return "OUTSIDE_CURTAINS_REPAIR_SERVICE", "Curtain/blind repair is the head task; window wording is context", "HIGH"
        if install:
            return "OUTSIDE_CURTAINS_INSTALLATION", "Installation targets curtains/blinds rather than the window", "HIGH"
        if selection or has(p, "как выбрать размер"):
            return "OUTSIDE_CURTAINS_SELECTION_INFO", "Explicit curtain/blind selection task", "HIGH"
        return "OUTSIDE_CURTAINS", "Curtain/blind is the head product; window wording is context", "HIGH"

    # Mosquito/protection net: distinguish product, selection, installation and
    # repair/replacement. Mixed window-repair + net-installation remains unresolved.
    if mosquito:
        if repair and install and not has(p, "ремонт москит", "ремонт сетк"):
            return None, "Phrase mixes window repair with mosquito-net installation; keep the service boundary visible", "LOW"
        if repair or replace:
            return "MOSQUITO_NET_REPAIR_SERVICE", "Explicit repair/replacement of a mosquito/protection net", "HIGH"
        if selection:
            return "MOSQUITO_NET_SELECTION_INFO", "Explicit mosquito/protection-net selection task", "HIGH"
        if install:
            return "MOSQUITO_NET_INSTALLATION_SERVICE", "Explicit installation of a mosquito/protection net", "HIGH"

    # DIY repair must outrank broad DIY-installation fallbacks.
    if pvc_door and diy and repair:
        return "PVC_DOOR_REPAIR_DIY", "Explicit DIY plastic-door repair/regulation task", "HIGH"
    if "подокон" in p and diy and repair:
        return "WINDOWSILL_REPAIR_DIY", "Explicit DIY windowsill repair task", "HIGH"

    # Whole-window and glazing replacement boundaries.
    if balcony and glazing and replace:
        return "BALCONY_GLAZING_REPLACEMENT_SERVICE", "Explicit replacement of existing balcony/loggia glazing", "HIGH"
    if win and replace and install and not has(p, "фурнитур", "створк", "сетк", "стеклопак", "подокон", "откос", "отлив"):
        return None, "Phrase mixes whole-window replacement and installation; exact service task is not safe to force", "LOW"
    if win and replace and (diy or re.search(r"^как\s+(?:поменять|заменить)", p)) and not has(p, "фурнитур", "створк", "сетк", "стеклопак", "подокон", "откос", "отлив"):
        return "WINDOW_REPLACEMENT_DIY", "Explicit procedural/self-service whole-window replacement task", "HIGH"

    # 'How to insert a window' is installation procedure, not ordinary operation.
    if win and "как вставить" in p:
        return "WINDOW_INSTALLATION_DIY", "Explicit procedural window insertion/installation task", "HIGH"

    # Negated installation must not create an installation service.
    if "без установки" in p and pvc_window:
        if has(p, "rehau", "рехау"):
            return "REHAU_WINDOWS_COMMERCIAL", "Explicit window product purchase with installation negated", "HIGH"
        return "PVC_WINDOWS_COMMERCIAL", "Explicit PVC-window product purchase with installation negated", "HIGH"

    # Product + installation bundles are installation-service tasks when the
    # installation is explicitly part of the offer/action.
    if pvc_door and has(p, "с установк", "установка", "монтаж"):
        return "PVC_DOOR_INSTALLATION_SERVICE", "Plastic-door product explicitly bundled with installation", "HIGH"
    if pvc_window and "поставить" in p and not has(p, "рассроч", "кредит", "халва"):
        return "WINDOW_INSTALLATION", "Action-headed request to install PVC windows", "HIGH"

    # Strong dimension head beats a trailing photo marker. Installation +
    # dimensions is a measurement/pre-installation information task; this also
    # reconciles the exact direct Step-09 measurement SERP probe.
    if win and has(p, "размер", "ширин", "высот", "габарит") and "фото" in p:
        return "WINDOW_DIMENSIONS_INFO", "Dimensions are the head task; photo is only a representation modifier", "HIGH"
    if win and has(p, "установ", "монтаж") and has(p, "размер", "размером", "размерами", "замер") and not diy:
        return "WINDOW_MEASUREMENT_INFO", "Measurement/dimension task connected with installation", "HIGH"

    # Explicit accessory/profile head objects must not become whole windows/doors.
    if has(p, "добор для пластиковых окон", "монтажная пластина для пластиковых окон", "панель для пластиковой двери", "профиль для пластиковых окон", "профиль пластиковой двери", "профиль пластиковых окон rehau", "узлы алюминиевых окон"):
        if selection:
            return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit component/profile selection task", "HIGH"
        return "WINDOW_HARDWARE", "Explicit window/door component is the head object", "HIGH"
    if "установка створки" in p and "окн" in p:
        return "WINDOW_HARDWARE_INSTALLATION_SERVICE", "Installation targets a window sash/component rather than the whole window", "HIGH"
    if "установка пластиковых панелей окон" in p:
        return None, "Panel-installation wording is not safely equivalent to whole-window installation", "LOW"

    # Aluminium/profile and hardware-brand boundaries missed by the broad product
    # fallback. Window-headed 'made of aluminium profile' remains a window product;
    # bare glazing-by-profile and mixed hardware-brand configurations stay cautious.
    if "рото для алюминиевых окон" in p:
        return "WINDOW_HARDWARE", "Roto is explicit hardware for aluminium windows", "HIGH"
    if has(p, "окно алюминиевое roto", "пластиковые двери roto", "окно rehau roto"):
        return None, "Whole product plus hardware-brand wording is a mixed product/component configuration", "LOW"
    if "ral" in p and "алюмини" in p and "окн" in p:
        return None, "RAL colour wording is a configuration/appearance task, not safe whole-window purchase evidence", "LOW"
    if has(p, "окна из алюминиевого профиля", "алютех окна из алюминиевого профиля", "балконные окна алюминиевый профиль", "цены окна алюминиевые профили"):
        return "ALUMINIUM_WINDOWS_COMMERCIAL", "Window-headed aluminium-profile product task", "HIGH"
    if "остекление окон алюминиевым профилем" in p:
        return None, "Generic glazing-by-profile wording does not safely distinguish service from product/configuration", "LOW"

    # Brand-comparison/definition and vague-fragment corrections.
    if has(p, "окна melke и rehau", "брусбокс это rehau"):
        return "WINDOW_COMPARISON_INFO", "Explicit cross-brand/brand-relationship information task", "HIGH"
    if "суть пластиковых окон" in p:
        return "WINDOW_DEFINITION_INFO", "Explicit definition/explanation task for PVC windows", "HIGH"
    if has(p, "почему пластиковых окнах", "ремонт пластиковых окон лучше"):
        return None, "Vague/incomplete informational wording is not safe to force into a comparison or repair service", "LOW"
    if has(p, "окно пластиковое закрыто", "открытое пластиковое окно", "пластиковое окно внутри", "пластиковое окно снаружи"):
        return None, "State/context fragment lacks a sufficiently explicit material user task", "LOW"
    if p == "пластиковые окна улица":
        return None, "Bare street/context fragment is not enough to infer purchase or navigation", "LOW"
    if p == "самому пластиковые окна":
        return None, "Bare DIY modifier lacks the action needed to identify the user task", "LOW"

    # Hardware information/selection should not stay in ecommerce merely because
    # a hardware token is present.
    hardware_context = has(p, "фурнитур", "ручк", "уплотн", "петл", "замок", "механизм", "профил") and has(p, "окн", "двер")
    if hardware_context and has(p, "как называется", "как устроена", "конструкция", "устройство", "основные функции", "что входит"):
        return "WINDOW_TECH_INFO", "Explicit technical/definition information task about window hardware", "HIGH"
    if hardware_context and has(p, "как выбрать", "какая бывает", "виды", "типы", "лучшая", "лучший"):
        return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit selection/types task about window hardware/components", "HIGH"
    if "как выбрать подоконник" in p:
        return "WINDOW_ACCESSORY_SELECTION_INFO", "Explicit windowsill selection task", "HIGH"

    # Product-family 'types' are selection information, not technical construction.
    if has(p, "виды алюминиевых окон", "виды пластиковых окон"):
        return "WINDOW_SELECTION_INFO", "Explicit window-type selection/information task", "HIGH"
    if has(p, "окна rehau виды", "виды окон rehau"):
        return "REHAU_SELECTION_INFO", "Explicit Rehau system/type selection task", "HIGH"

    # Installation/glazing phrases whose wording is informational or contextual.
    if p == "алюминиевое остекление веранды раздвижными конструкциями":
        return "VERANDA_GLAZING", "Veranda glazing is the head service; sliding construction is a configuration modifier", "HIGH"
    if win and has(p, "зазор при установке", "правильная установка"):
        return "WINDOW_INSTALLATION_INFO", "Explicit installation requirements/guidance task", "HIGH"
    if p == "после установки пластиковых окон":
        return None, "Post-installation context fragment lacks a concrete user task", "LOW"

    return _v27_classifier(phrase)


b.classify_semantic = classify_v28


def _expect(mapping: dict[str, str]) -> None:
    for phrase, task in mapping.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


def _unresolved(phrases: set[str]) -> None:
    for phrase in phrases:
        got = b.classify_semantic(phrase)
        assert got[0] is None, (phrase, got)


def self_test() -> None:
    # Re-run the compatible V27 corpus first. V28 intentionally changes none of
    # those canonical cases.
    v27.self_test()

    _expect({
        "регулировка пластиковых дверей своими руками": "PVC_DOOR_REPAIR_DIY",
        "ремонт жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_REPAIR_SERVICE",
        "ремонт москитной сетки на пластиковые окна": "MOSQUITO_NET_REPAIR_SERVICE",
        "ремонт сетки для пластиковых окон": "MOSQUITO_NET_REPAIR_SERVICE",
        "замена сетки на пластиковых окнах цена": "MOSQUITO_NET_REPAIR_SERVICE",
        "как поменять пластиковое окно": "WINDOW_REPLACEMENT_DIY",
        "день ночь на пластиковые окна установка": "OUTSIDE_CURTAINS_INSTALLATION",
        "профиль для пластиковых окон": "WINDOW_HARDWARE",
        "профиль пластиковой двери": "WINDOW_HARDWARE",
        "профиль пластиковых окон rehau": "WINDOW_HARDWARE",
        "размеры окон для частного дома фото": "WINDOW_DIMENSIONS_INFO",
        "как выбрать жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_SELECTION_INFO",
        "как выбрать шторы на пластиковые окна": "OUTSIDE_CURTAINS_SELECTION_INFO",
        "как выбрать москитную сетку на пластиковое окно": "MOSQUITO_NET_SELECTION_INFO",
        "как выбрать подоконник для пластиковых окон": "WINDOW_ACCESSORY_SELECTION_INFO",
        "замена остекления балкона": "BALCONY_GLAZING_REPLACEMENT_SERVICE",
        "замена холодного остекления балкона": "BALCONY_GLAZING_REPLACEMENT_SERVICE",
        "балконная дверь пластиковая с установкой москва": "PVC_DOOR_INSTALLATION_SERVICE",
        "поставить пластиковые окна на кухне цена": "WINDOW_INSTALLATION",
        "установка пластиковых окон размером": "WINDOW_MEASUREMENT_INFO",
        "купить пластиковые окна без установки цена": "PVC_WINDOWS_COMMERCIAL",
        "как вставить пластиковое окно": "WINDOW_INSTALLATION_DIY",
        "балконы остекление адреса": "WINDOW_SERVICE_NAVIGATION",
        "номер ремонта пластиковых окон": "WINDOW_SERVICE_NAVIGATION",
        "окна rehau дилеры": "REHAU_NAVIGATION",
        "окна rehau сайт": "REHAU_NAVIGATION",
        "офис окна rehau в москве": "REHAU_NAVIGATION",
        "официальные партнеры производителя окон rehau в россии": "REHAU_NAVIGATION",
        "добор для пластиковых окон rehau купить": "WINDOW_HARDWARE",
        "монтажная пластина для пластиковых окон rehau grazio": "WINDOW_HARDWARE",
        "панель для пластиковой двери": "WINDOW_HARDWARE",
        "узлы алюминиевых окон": "WINDOW_HARDWARE",
        "установка створки пластикового окна": "WINDOW_HARDWARE_INSTALLATION_SERVICE",
        "окна melke и rehau": "WINDOW_COMPARISON_INFO",
        "суть пластиковых окон": "WINDOW_DEFINITION_INFO",
        "окна из алюминиевого профиля": "ALUMINIUM_WINDOWS_COMMERCIAL",
        "рото для алюминиевых окон": "WINDOW_HARDWARE",
        "ремонт подоконника пластикового окна своими руками": "WINDOWSILL_REPAIR_DIY",
        "зазор при установке пластиковых окон": "WINDOW_INSTALLATION_INFO",
        "правильная установка пластиковых окон": "WINDOW_INSTALLATION_INFO",
        "виды алюминиевых окон": "WINDOW_SELECTION_INFO",
        "оконная фурнитура виды": "WINDOW_ACCESSORY_SELECTION_INFO",
    })

    _unresolved({
        "пластиковые окна ремонт установка москитной сетки",
        "пластиковые окна замена установка",
        "окно rehau roto",
        "окно алюминиевое roto",
        "пластиковые двери roto",
        "ral алюминиевых окон",
        "остекление окон алюминиевым профилем",
        "установка пластиковых панелей окон",
        "почему пластиковых окнах",
        "ремонт пластиковых окон лучше",
        "окно пластиковое закрыто",
        "открытое пластиковое окно",
        "пластиковое окно внутри",
        "пластиковое окно снаружи",
        "пластиковые окна улица",
        "самому пластиковые окна",
        "после установки пластиковых окон",
    })


if __name__ == "__main__":
    self_test()
    runner.main()
