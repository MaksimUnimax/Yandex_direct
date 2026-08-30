#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V28 as v28

_current_classifier = b.classify_semantic


def classify_v29(phrase: str):
    # V29 is a regression-harness revision only. Semantic behavior is V28.
    return _current_classifier(phrase)


b.classify_semantic = classify_v29


def expect(mapping: dict[str, str]) -> None:
    for phrase, task in mapping.items():
        got = b.classify_semantic(phrase)
        assert got[0] == task, (phrase, task, got)


def unresolved(phrases: set[str]) -> None:
    for phrase in phrases:
        got = b.classify_semantic(phrase)
        assert got[0] is None, (phrase, got)


def self_test() -> None:
    # Current compatible regression corpus. Historical suites remain immutable;
    # cases intentionally superseded by manual QA are asserted with their current
    # V28 expectation here instead of rewriting old files.
    expect({
        # Long-lived product / component / repair boundaries.
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
        "замена оконной фурнитуры": "WINDOW_REPAIR",
        "поменять стеклопакет на пластиковом окне цена": "WINDOW_REPAIR",
        "не открывается пластиковое окно": "WINDOW_REPAIR_DIY",
        "не закрывается пластиковая дверь": "PVC_DOOR_REPAIR_DIY",
        "открывание алюминиевых окон": "WINDOW_OPERATION_DIY",
        "проветривание алюминиевые окна": "WINDOW_OPERATION_DIY",
        "чем отмыть пластиковые окна после ремонта": "WINDOW_CARE_INFO",
        "чем очистить пластиковые окна после ремонта": "WINDOW_CARE_INFO",
        "очистить пластиковые окна ремонта": "WINDOW_CARE_INFO",

        # Selection / review / dimensions / design boundaries.
        "какое окно алюминиевое": "WINDOW_SELECTION_INFO",
        "какие окна rehau": "REHAU_SELECTION_INFO",
        "рейтинг алюминиевых окон": "WINDOW_REVIEWS_INFO",
        "панорамные окна для частного дома размеры": "WINDOW_DIMENSIONS_INFO",
        "стандартные размеры панорамных окон для частного дома": "WINDOW_DIMENSIONS_INFO",
        "панорамные окна в частном доме фото": "DESIGN_INSPIRATION",
        "французские окна на балкон фото": "DESIGN_INSPIRATION",
        "формы окон для частных домов": "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO",
        "французские окна в пол": "FRENCH_WINDOWS_COMMERCIAL",
        "французские окна на лоджию": "FRENCH_WINDOWS_COMMERCIAL",
        "французские окна на террасе": "FRENCH_WINDOWS_COMMERCIAL",

        # Glazing / installation / finishing boundaries retained from V20-V27.
        "какое остекление балкона лучше выбрать": "GLAZING_SELECTION_INFO",
        "остекление балконов самому": "GLAZING_DIY_INFO",
        "разрешение на остекление балкона": "GLAZING_PERMISSION_INFO",
        "балкон без остекления": "OPEN_BALCONY_FINISHING",
        "демонтаж остекления балкона": "WINDOW_DEMOLITION",
        "профиль для остекления балконов": "WINDOW_HARDWARE",
        "поликарбонат для остекления веранды": "WINDOW_ACCESSORIES",
        "толщина монолитного поликарбоната для остекления веранды": "WINDOW_ACCESSORY_SELECTION_INFO",
        "кондиционер на балконе с остеклением": "OUTSIDE_HVAC",
        "ремонт пластиковых окон самому": "WINDOW_REPAIR_DIY",
        "ремонт откосов пластиковых окон": "WINDOW_FINISHING_SERVICE",
        "ремонт подоконников пластиковых окон": "WINDOWSILL_REPAIR",
        "установка пластиковой двери": "PVC_DOOR_INSTALLATION_SERVICE",
        "установка готовых пластиковых окон": "WINDOW_INSTALLATION",
        "изготовление и установка пластиковых окон": "WINDOW_INSTALLATION",
        "стоимость замены окна на пластиковые цена": "WINDOW_REPLACEMENT_SERVICE",
        "монтаж откосов на пластиковые окна цена": "WINDOW_FINISHING_SERVICE",
        "установка откосов на пластиковые окна": "WINDOW_FINISHING_SERVICE",
        "установка откосов на пластиковые окна своими руками": "WINDOW_FINISHING_DIY",
        "установка отливов на пластиковые окна": "WINDOW_FINISHING_SERVICE",
        "установка отлива на пластиковое окно своими руками": "WINDOW_FINISHING_DIY",
        "установка пластиковых окон своими руками": "WINDOW_INSTALLATION_DIY",
        "установка пластиковых окон самостоятельно": "WINDOW_INSTALLATION_DIY",
        "установка жалюзи на пластиковые окна": "OUTSIDE_CURTAINS_INSTALLATION",
        "установка рулонных штор на пластиковые окна": "OUTSIDE_CURTAINS_INSTALLATION",
        "установка москитной сетки на пластиковое окно": "MOSQUITO_NET_INSTALLATION_SERVICE",
        "установка сетки антикошка на пластиковые окна": "MOSQUITO_NET_INSTALLATION_SERVICE",
        "установка деревянного подоконника на пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна цена": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка подоконников под пластиковые окна": "WINDOWSILL_INSTALLATION_SERVICE",
        "установка оконной фурнитуры": "WINDOW_HARDWARE_INSTALLATION_SERVICE",
        "установка подоконника на пластиковые окна своими руками": "WINDOW_FINISHING_DIY",
        "ремонт балкона с остеклением": "BALCONY_RENOVATION_WITH_GLAZING_SERVICE",
        "ремонт остекление балконов москва": "BALCONY_GLAZING_REPAIR_SERVICE",
        "ремонт остекление балкона французские окна": "BALCONY_GLAZING_REPAIR_SERVICE",

        # French-window dedicated boundaries.
        "французские занавески на окна": "OUTSIDE_CURTAINS",
        "французские вертикальные задвижки для окон": "WINDOW_HARDWARE",
        "французские окна название": "WINDOW_DEFINITION_INFO",
        "французское окно оформление": "DESIGN_INSPIRATION",
        "устанавливаем французские окна": "WINDOW_INSTALLATION",
        "французские окна вместо балконного блока": "WINDOW_REPLACEMENT_SERVICE",

        # V28 manual-QA corrections.
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
        "виды пластиковых окон": "WINDOW_SELECTION_INFO",
        "оконная фурнитура виды": "WINDOW_ACCESSORY_SELECTION_INFO",
    })

    unresolved({
        # Long-lived unresolved boundaries.
        "пластиковые окна монтаж ремонт",
        "пластиковые окна после ремонта",
        "покраска алюминиевых окон",
        "сборка алюминиевых окон",
        "подоконник после установки пластикового окна",
        "веранда без остекления",
        # V28 explicit mixed/context boundaries.
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
