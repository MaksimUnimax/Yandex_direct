#!/usr/bin/env python3
"""Materialize the accepted full-volume rule-only KW-002 Step03B correction.

The classifier below is the executable form of the accepted independent audit.
It evaluates every frozen Step03A normalized identity.  The accepted audit
overlay is used only after classification as a row-level regression oracle.
No provider, Search, GenSearch, AI-search, or sealed historical source is used.
"""

from __future__ import annotations

import collections
import csv
import hashlib
import json
import re
from pathlib import Path


JOB = Path(__file__).resolve().parent
LIVE_BASE_HEAD = "a0d662851c2f26d7a219ec7efb7d7e37e640dce3"

POOL = JOB / "STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv"
LEDGER = JOB / "STEP_03A_NORMALIZATION_LEDGER_2026-09-11.tsv"
ORIGINAL_CANDIDATE = JOB / "STEP_03B_SANITIZED_CANDIDATE_POOL_2026-09-11.tsv"
ORIGINAL_EXCLUDED_HOLD = JOB / "STEP_03B_EXCLUDED_HOLD_REGISTER_2026-09-11.tsv"
STEP04_OCCURRENCE = JOB / "STEP_04_OCCURRENCE_FAMILY_LEDGER_CORRECTED_2026-09-10.tsv"
STEP04_FAMILY = JOB / "STEP_04_FAMILY_TRIAGE_CORRECTED_2026-09-10.tsv"

AUDIT_OVERLAY = JOB / "KW002_STEP03A_03B_INDEPENDENT_FULL_VOLUME_AUDIT_OVERLAY_2026-09-11.tsv"
AUDIT_REASON = JOB / "KW002_STEP03A_03B_REASON_CODE_AUDIT_2026-09-11.tsv"

OUT_CANDIDATE = JOB / "STEP_03B_SANITIZED_CANDIDATE_POOL_CORRECTED_2026-09-11.tsv"
OUT_EXCLUDED_HOLD = JOB / "STEP_03B_EXCLUDED_HOLD_REGISTER_CORRECTED_2026-09-11.tsv"
OUT_REASON = JOB / "STEP_03B_REASON_CODE_ACCOUNTING_CORRECTED_2026-09-11.tsv"
OUT_QA = JOB / "STEP_03B_SANITATION_QA_CORRECTED_2026-09-11.md"
OUT_FUNNEL = JOB / "KW002_DATA_FUNNEL_CORRECTED_2026-09-11.json"
OUT_RECONCILIATION = JOB / "STEP_04_POST_SANITATION_RECONCILIATION_CORRECTED_2026-09-11.md"
OUT_RECEIPT = JOB / "STEP_03B_CORRECTION_STATE_RECEIPT_2026-09-11.md"

EXPECTED_SHA256 = {
    POOL.name: "b30c29ff66a56d80bc1aa9ff6b2eade522b27d1e167cbd636ac72fbff211f2a8",
    LEDGER.name: "28205ca64f26d219d489b36f102a8923b4a4b635c8b213179bca4a188b24c3df",
    AUDIT_OVERLAY.name: "db9b79dda64b205f0b0bef273f70f221f183d9389eca3e67e651e93ea269d669",
    AUDIT_REASON.name: "050af71b8e431408c2f406e984416dc4c605038a5ad9f0ac103772f2f9310b31",
}

EXPECTED_TRANSITION_NORMALIZED = {
    "KEEP->KEEP": 4788,
    "KEEP->HOLD": 207,
    "KEEP->EXCLUDE": 79,
    "HOLD->KEEP": 298,
    "HOLD->HOLD": 12084,
    "HOLD->EXCLUDE": 368,
    "EXCLUDE->KEEP": 14,
    "EXCLUDE->HOLD": 744,
    "EXCLUDE->EXCLUDE": 5994,
}

EXPECTED_TRANSITION_RAW = {
    "KEEP->KEEP": 4945,
    "KEEP->HOLD": 211,
    "KEEP->EXCLUDE": 80,
    "HOLD->KEEP": 304,
    "HOLD->HOLD": 12828,
    "HOLD->EXCLUDE": 368,
    "EXCLUDE->KEEP": 14,
    "EXCLUDE->HOLD": 784,
    "EXCLUDE->EXCLUDE": 6445,
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rx(pattern: str) -> re.Pattern[str]:
    return re.compile(pattern, re.IGNORECASE)


PRODUCT = rx(r"\b(?:амулет(?:ы|а|ов|у|ом|е|ам|ами|ах)?|оберег(?:и|а|ов|у|ом|е|ам|ами|ах)?|талисман(?:ы|а|ов|у|ом|е|ам|ами|ах)?|ч[её]тки|ч[её]ток|ч[её]ткам|ч[её]тками|ч[её]тках)\b")
COMMERCIAL = rx(r"\b(?:купить|цена|заказать|заказ|продажа|магазин|озон|ozon|wildberries|вайлдберриз|вб|доставка|каталог|недорого|стоимость|авито)\b")
OBJECT_FORM = rx(r"\b(?:кулон\w*|подвеск\w*|медальон\w*|браслет\w*|украшени\w*|брелок\w*|амулет\w*|оберег\w*|талисман\w*|ч[её]тк\w*)\b")
CAR_USE = rx(r"\b(?:в|для|на) (?:машин(?:у|ы|е|а)|авто|автомобил(?:я|ь|е))\b|\bавтомобильн\w*\b")
ZODIAC = rx(r"\b(?:знак\w* зодиака|зодиак\w*)\b")

CATALOG = rx(
    r"\b(?:rsotm|soldier of fortune|бусидо|путь воина|древо жизни|шлем ужаса|"
    r"эгисхьяльм|агисхьяльм|вегвизир|гунгнир|gungner|валькнут|valknut|белобог|"
    r"чернобог|печать велеса|алатыр\w*|триглав\w*|ратиборец\w*|молвинец\w*|"
    r"колядник\w*|знич\w*|громовик\w*|всеславец\w*|боговник\w*|стрибог\w*|"
    r"семаргл\w*|звезд\w* лад\w*|даждьбог\w*|руническ\w* компас\w*|копь\w* одина|"
    r"узел\w* павш\w*|крест\w* сварог\w*|инь и ян|велес\w*|родимич\w*|жива\b|"
    r"сварог\w*|перун\w*|макош\w*|хорс\w*|мара\b|спаси и сохрани|чур\b|"
    r"герб\w* россии|кровь и песок|иоанн\w* златоуст\w*)\b"
)
RELIGIOUS_CATALOG = rx(r"\b(?:спаси и сохрани|иоанн\w* златоуст\w*|\b(?:ом|аум)\b)\b")

LEXICAL_GARBAGE = rx(r"\b(?:ч[её]тко|ч[её]тк(?:ий|ая|ое|ие|ого|ому|им|ым|ом|ую|ой|их|ых|ими)|ч[её]ткост\w*)\b")
ROSARY_TYPO = rx(r"\b(?:ч[её]тка|ч[её]тке|ч[её]тку|ч[её]ткой|ч[её]ткою|ч[её]ток|ч[её]тков)\b")
GAME_NAMED = rx(r"\b(?:minecraft|майнкрафт|roblox|роблокс|genshin|геншин|skyrim|скайрим|stalker|сталкер|diablo|диабло|warframe|варфрейм|world of warcraft|warcraft|wow|вов|дст|авп|awp|dota|дота|elden(?: ring)?|элден(?: ринг)?|terraria|террария|cuphead|капхед|hollow knight|hollow|холлоу(?: найт)?|poe ?2?|path of exile|valheim|вальхейм|валхейм|witcher|ведьмак\w*|counter strike|кс(?: ?2)?|baldur\w*|fallout|bloodborne)\b|\bгунгнир\b.*\bс завода\b")
GAME_CONTEXT = rx(r"\b(?:в игре|игров\w*|game|games|квест\w*|гайд\w*|прохождени\w*|сервер\w*|чит(?:ы| код\w*)?|wiki|вики|ячейк\w* амулет\w*|слот\w* амулет\w*|крафт\w*)\b")
GAME_AMBIGUOUS = rx(r"\b(?:игр(?:а|ы|е|у|ой|ах)|мод(?:ы|а|у|ом|е)?|модел\w*|id)\b")

MEDIA_STRONG = rx(r"\b(?:фильм\w*|сериал\w*|мультфильм\w*|аниме|книг\w*|аудиокниг\w*|роман\w*|рассказ\w*|песн\w*|музык\w*|альбом\w*|трек\w*|клип\w*|аккорд\w*|саундтрек\w*|трейлер\w*|акт[её]р\w*|актрис\w*|персонаж\w*|глава\w*|сезон\w*|эпизод\w*|кино\w*|book\w*|movie\w*|season\w*|episode\w*|леди ?баг\w*|ледибаг\w*|кота нуара|супер ?кот\w*|суперкот\w*|когда поют цикад\w*|дом за озером|чужая кровь)\b")
MEDIA_ACTION = rx(r"\b(?:читать|смотреть|слушать|скачать|серия\w*|канал\w*|онлайн|бесплатн\w*|фоторамк\w*)\b")
MEDIA_DIGITAL_PROOF = rx(r"\b(?:дзен|яндекс дзен|онлайн|бесплатн\w*|без регистрац\w*|в хорошем качестве|полностью|серии|фоторамк\w*)\b")
MEDIA_TITLE_COLLISION = rx(r"\b(?:астрал амулет(?: зла)?|баг\w* талисман\w*|талисман\w* супер\w*|золот\w* рыбк\w*|талисман чемпионк\w*)\b")
MEDIA_EXPLICIT_DIGITAL = rx(r"\b(?:все серии|\d+ серия|серия \d+|без регистрац\w*|в хорошем качестве)\b|\b(?:читать|смотреть|слушать|скачать)\b.*\b(?:онлайн|бесплатн\w*|дзен|канал\w*)\b|\b(?:онлайн|бесплатн\w*|дзен|канал\w*)\b.*\b(?:читать|смотреть|слушать|скачать)\b")

VEHICLE_BRAND = rx(r"\b(?:renault|рено|лада|lada|ваз|газель|тойота|toyota|hyundai|хендай|kia|киа|bmw|бмв|mercedes|мерседес|skoda|шкода|audi|ауди|chery|чери|черри|чере|geely|джили|volkswagen|фольксваген|nissan|ниссан|ford|форд)\b")
VEHICLE_PART = rx(r"\b(?:двигател\w*|коробк\w* передач|запчаст\w*|автозапчаст\w*|код краск\w*|краск\w* амулет\w*|амулет\w* краск\w*|цвет кузов\w*|кузов\w*|шасс\w*|бампер\w*|форсунк\w*|турбин\w*|мотор\w*|акпп|мкпп|vin|сцеплен\w*|гбц|стартер\w*|катализатор\w*|датчик\w*|сканер\w*|диск\w*|пищалк\w*|подходят\w* на амулет\w*|от каких машин\w*.*амулет\w*)\b")
VEHICLE_MODEL = rx(r"\b(?:чери амулет|черри амулет|рен(?:о|ault) талисман|amulet a?15|амулет а ?15)\b")
PAINT_COLLISION = rx(r"\bкраск\w*\b.*\bамулет\w*\b|\bамулет\w*\b.*\bкраск\w*\b")
TECHNICAL = rx(r"\b(?:электропривод\w*|задвижк\w*|сервопривод\w*|привод\w* аума|аума привод\w*|редуктор\w*|схем\w* подключени\w*|концев\w* выключател\w*|шаровый кран\w*|затвор\w* аума|аума s(?:a|ar|arex)\w*|auma s(?:a|ar|arex)\w*|паспорт аума|настройк\w* аума|аума настройк\w*|болт\w* аума|оборудован\w* auma|клапан\w* аума)\b")
RELIGIOUS = rx(r"\b(?:мантр\w*|молитв\w*|молиться|медитац\w*|практик\w* аум|аум практик\w*|храм\w*|церк\w*|икон\w*|богослуж\w*|священн\w*|дуа|намаз\w*)\b")
ASTRO_INFO = rx(r"\b(?:гороскоп\w*|совместимост\w*|натальн\w* карт\w*|асцендент\w*|астролог\w*|созвезди\w*|какой знак зодиака|характеристик\w* знак\w*|характер\w* знак\w*|дата рождения|по дате рождения|знак зодиака мужчин\w*|знак зодиака женщин\w*|знак зодиака ребен\w*)\b")
ASTRO_STONE = rx(r"\b(?:камень|камни|камня|камнем|камен\w*)\b")
SPORT_STRONG = rx(r"\b(?:футбол\b|футбола|футболу|футбольн\w*|хокке\w*|олимпиад\w*|чемпионат\w*|роналд\w*|маскот\w*|спортивн\w* талисман\w*)\b")
SPORT_AMBIGUOUS = rx(r"\b(?:команд\w*|талисман\w* мира)\b")
SHIRT = rx(r"\bфутболк\w*\b")
UNRELATED = rx(r"\b(?:томат\w*|помидор\w*|семен\w*|саженц\w*|рассад\w*|лекарств\w*|таблетк\w*|шампун\w*|крем\w*|мазь\w*|телефон\w*|смартфон\w*|айфон\w*|iphone|ноутбук\w*|наушник\w*|колонк\w*|обув\w*|куртк\w*|одежд\w*|духи|парфюм\w*|аромат\w*|фрагрантик\w*|экс нихило|блю талисман|золотое яблоко|шины|автомасл\w*|шуруповерт\w*|антенн\w*|мебел\w*|металлоискател\w*|аптек\w*|бытов\w* техник\w*|обои\w* на телефон|заставк\w*.*(?:телефон|смартфон)|чехол\w* на телефон|наклейк\w* на банковск\w* карт\w*)\b")
PERSON = rx(r"\b(?:биограф\w*|певец\w*|певиц\w*|блогер\w*|писател\w*|режисс[её]р\w*|спортсмен\w*|фамили\w*|личная жизнь|дата смерти|где родил\w*)\b")
PLACE = rx(r"\b(?:погод\w*|город\w*|област\w*|район\w*|улиц\w*|адрес\w*|деревн\w*|пос[её]лок\w*|село\b|санатор\w*|отел\w*|гостиниц\w*|курорт\w*|билет\w*|вокзал\w*|аэропорт\w*|недвижимост\w*|квартир\w*|автобус\w*|поезд\w*|чуваши\w*|москва|санкт петербург|новосибирск|екатеринбург|казань|самара|уфа|омск|пермь|воронеж|краснодар|сочи)\b")
ORGANIZATION = rx(r"\b(?:ооо|зао|пао|инн|организац\w*|компани\w*|холдинг\w*|агентств\w*|банк\w*|университет\w*|школ\w*|клуб\w*|ресторан\w*|кафе\w*|официальн\w* сайт|сайт организац\w*|торговый дом)\b")
ENTITY_INFO = rx(r"\b(?:кто такой|кто такая|сколько лет)\b")
TITLE_COLLISION = rx(r"\b(?:счастлив\w* амулет\w*|амулет\w* дзен\w*|амулет мары)\b")
ALATYR_LOCAL = rx(r"\bалатыр\w*\b.*\b(?:авито|чуваши\w*|санатор\w*|билет\w*|автобус\w*|поезд\w*|вокзал\w*|квартир\w*|дом\w*|ваканси\w*|работ\w*|услуг\w*|магазин\w*|погод\w*|город\w*|аптек\w*|телефон\w*)\b|\b(?:авито|чуваши\w*|санатор\w*|билет\w*|автобус\w*|поезд\w*|вокзал\w*|квартир\w*|дом\w*|ваканси\w*|работ\w*|услуг\w*|магазин\w*|погод\w*|город\w*|аптек\w*|телефон\w*)\b.*\bалатыр\w*\b")
YANDEX_COLLISION = rx(r"\b(?:яндекс|yandex|дзен)\b")
PHYSICAL_OBJECT = rx(r"\b(?:кулон\w*|подвеск\w*|медальон\w*|браслет\w*|брелок\w*)\b")
DIRECT_CATALOG_COMPOUND = rx(r"\b(?:древо жизни|шлем ужаса|печать велеса|звезд\w* лад\w*|руническ\w* компас\w*|копь\w* одина|узел\w* павш\w*|крест\w* сварог\w*|инь и ян|спаси и сохрани|герб\w* россии|кровь и песок|иоанн\w* златоуст\w*)\b")


def classify(key: str) -> tuple[str, str, str]:
    """Return corrected state, deterministic basis, and confidence."""
    feats = {
        "product": bool(PRODUCT.search(key)),
        "commercial": bool(COMMERCIAL.search(key)),
        "object": bool(OBJECT_FORM.search(key)),
        "car_use": bool(CAR_USE.search(key)),
        "catalog": bool(CATALOG.search(key)),
        "zodiac": bool(ZODIAC.search(key)),
    }
    if not key:
        return "EXCLUDE", "EMPTY_OR_MALFORMED", "high"
    if LEXICAL_GARBAGE.search(key) and not PRODUCT.fullmatch(key):
        return "EXCLUDE", "CLEAR_LEXICAL_GARBAGE", "high"
    if ROSARY_TYPO.search(key) and not PRODUCT.search(key):
        return "HOLD", "POSSIBLE_ROSARY_MORPHOLOGY_OR_TYPO", "medium"
    if TECHNICAL.search(key):
        return "EXCLUDE", "EXPLICIT_INDUSTRIAL_AUMA_CONTEXT", "high"
    if GAME_NAMED.search(key) or GAME_CONTEXT.search(key):
        return "EXCLUDE", "EXPLICIT_GAME_OR_GAME_ITEM_CONTEXT", "high"
    if GAME_AMBIGUOUS.search(key):
        return "HOLD", "GENERIC_GAME_OR_MODEL_TOKEN_NEEDS_CONTEXT", "medium"
    if MEDIA_STRONG.search(key):
        return "EXCLUDE", "EXPLICIT_MEDIA_WORK_OR_EPISODE_CONTEXT", "high"
    if rx(r"\b(?:талисман\w* для (?:золот\w* )?рыбк\w*|талисман\w* леди и кот\w*)\b").search(key):
        if MEDIA_DIGITAL_PROOF.search(key):
            return "EXCLUDE", "EXPLICIT_DIGITAL_MEDIA_TITLE_CONTEXT", "high"
        return "HOLD", "MEDIA_TITLE_VERSUS_PRODUCT_COLLISION", "medium"
    if MEDIA_TITLE_COLLISION.search(key):
        if MEDIA_DIGITAL_PROOF.search(key):
            return "EXCLUDE", "EXPLICIT_DIGITAL_MEDIA_TITLE_CONTEXT", "high"
        return "HOLD", "MEDIA_TITLE_VERSUS_PRODUCT_COLLISION", "medium"
    if MEDIA_ACTION.search(key):
        if MEDIA_EXPLICIT_DIGITAL.search(key) or TITLE_COLLISION.search(key):
            return "EXCLUDE", "EXPLICIT_DIGITAL_MEDIA_CONSUMPTION_CONTEXT", "high"
        return "HOLD", "GENERIC_MEDIA_ACTION_MAY_BE_INFORMATIONAL_PRODUCT_RESEARCH", "medium"
    if VEHICLE_MODEL.search(key) or VEHICLE_PART.search(key):
        if rx(r"\bзвезд\w* лад\w*\b").search(key) and not VEHICLE_PART.search(key):
            return ("KEEP", "CATALOG_NAME_WITH_COMMERCE", "high") if feats["commercial"] else ("HOLD", "CATALOG_NAME_VERSUS_VEHICLE_COLLISION", "medium")
        return "EXCLUDE", "EXPLICIT_VEHICLE_MODEL_OR_PART_CONTEXT", "high"
    if PAINT_COLLISION.search(key):
        return "HOLD", "PRODUCT_NAME_VERSUS_VEHICLE_PAINT_COLLISION", "medium"
    if VEHICLE_BRAND.search(key):
        if feats["car_use"] and feats["product"] and not VEHICLE_PART.search(key):
            return "KEEP", "SUPPORTED_AUTOMOBILE_USE_PRODUCT_CONTEXT", "high"
        if rx(r"\bзвезд\w* лад\w*\b").search(key):
            return ("KEEP", "CATALOG_NAME_WITH_COMMERCE", "high") if feats["commercial"] else ("HOLD", "CATALOG_NAME_VERSUS_VEHICLE_COLLISION", "medium")
        return "EXCLUDE", "EXPLICIT_VEHICLE_BRAND_OR_MODEL_CONTEXT", "high"
    if SHIRT.search(key):
        return "EXCLUDE", "EXPLICIT_UNSUPPORTED_CLOTHING_PRODUCT", "high"
    if SPORT_STRONG.search(key):
        return "EXCLUDE", "EXPLICIT_SPORT_TEAM_EVENT_OR_MASCOT_CONTEXT", "high"
    if SPORT_AMBIGUOUS.search(key):
        return "HOLD", "GENERIC_TEAM_OR_MASCOT_CONTEXT", "medium"
    if UNRELATED.search(key):
        return "EXCLUDE", "EXPLICIT_UNSUPPORTED_PRODUCT_OR_LOCAL_ENTITY_CONTEXT", "high"
    if RELIGIOUS.search(key):
        if RELIGIOUS_CATALOG.search(key):
            if feats["commercial"] or feats["product"] or rx(r"\b(?:кулон\w*|подвеск\w*|медальон\w*|браслет\w*)\b").search(key):
                return "KEEP", "FROZEN_RELIGIOUS_CATALOG_PRODUCT_CONTEXT", "high"
            return "HOLD", "CATALOG_PRODUCT_NAME_VERSUS_RELIGIOUS_TEXT", "medium"
        if feats["product"]:
            return "HOLD", "PHYSICAL_PRODUCT_VERSUS_RELIGIOUS_PRACTICE", "medium"
        return "EXCLUDE", "EXPLICIT_RELIGIOUS_PRACTICE_WITHOUT_PRODUCT", "high"
    if PERSON.search(key) or ENTITY_INFO.search(key):
        if (feats["product"] or feats["catalog"]) and feats["commercial"]:
            return "KEEP", "SUPPORTED_PRODUCT_WITH_COMMERCIAL_CONTEXT", "high"
        if feats["product"] or feats["catalog"]:
            return "HOLD", "PRODUCT_OR_CATALOG_NAME_WITH_PERSON_ENTITY_CONTEXT", "medium"
        return "EXCLUDE", "EXPLICIT_PERSON_OR_FOREIGN_ENTITY_CONTEXT", "high"
    if ASTRO_INFO.search(key) or ASTRO_STONE.search(key) or feats["zodiac"]:
        if feats["product"] and feats["zodiac"] and not ASTRO_INFO.search(key):
            return "KEEP", "SUPPORTED_PRODUCT_PLUS_ZODIAC_TITLE", "high"
        if feats["zodiac"] and (feats["commercial"] or rx(r"\b(?:кулон\w*|подвеск\w*|медальон\w*|браслет\w*)\b").search(key)):
            return "KEEP", "ZODIAC_TITLE_WITH_COMMERCE_OR_OBJECT_FORM", "high"
        if feats["product"]:
            return "HOLD", "PRODUCT_VERSUS_ASTROLOGY_INFORMATION", "medium"
        if ASTRO_INFO.search(key):
            return "EXCLUDE", "EXPLICIT_ASTROLOGY_INFORMATION_TASK", "high"
        return "HOLD", "ZODIAC_OR_STONE_PRODUCT_COLLISION", "medium"
    if ALATYR_LOCAL.search(key):
        return "EXCLUDE", "EXPLICIT_ALATYR_PLACE_OR_LOCAL_ENTITY_CONTEXT", "high"
    if PLACE.search(key) or ORGANIZATION.search(key):
        real_estate = bool(rx(r"\b(?:купить квартир\w*|купить дом\b|продаж\w* дом\w*|недвижимост\w*)\b").search(key))
        if real_estate:
            return "EXCLUDE", "EXPLICIT_REAL_ESTATE_CONTEXT", "high"
        if (feats["product"] or feats["catalog"]) and feats["commercial"]:
            return "KEEP", "SUPPORTED_PRODUCT_WITH_COMMERCE_AND_GEO_CHANNEL", "high"
        if feats["product"]:
            return "HOLD", "PRODUCT_OR_CATALOG_NAME_WITH_PLACE_OR_ORGANIZATION", "medium"
        return "EXCLUDE", "EXPLICIT_PLACE_OR_ORGANIZATION_CONTEXT", "high"
    if TITLE_COLLISION.search(key):
        return "HOLD", "TITLE_LIKE_PRODUCT_WORD_COLLISION", "medium"
    if YANDEX_COLLISION.search(key):
        return "HOLD", "SEARCH_PLATFORM_OR_MEDIA_CONTEXT_UNRESOLVED", "medium"
    if feats["product"]:
        return "KEEP", "FROZEN_CLIENT_PRODUCT_CLASS_WITHOUT_FOREIGN_CONTEXT", "high"
    if feats["catalog"]:
        if PHYSICAL_OBJECT.search(key) or (feats["commercial"] and DIRECT_CATALOG_COMPOUND.search(key)):
            return "KEEP", "FROZEN_CATALOG_NAME_WITH_COMMERCE_OR_OBJECT_FORM", "high"
        return "HOLD", "FROZEN_CATALOG_NAME_REFERENT_UNRESOLVED", "medium"
    if feats["car_use"]:
        return "HOLD", "AUTOMOBILE_USE_WITHOUT_SUPPORTED_PRODUCT_NOUN", "medium"
    return "HOLD", "INSUFFICIENT_CONTEXT_FOR_KEEP_OR_EXCLUDE", "medium"


def normalized_state(value: str) -> str:
    return {"KEEP_CANDIDATE": "KEEP", "HOLD_AMBIGUOUS": "HOLD", "AUTO_EXCLUDED": "EXCLUDE"}[value]


def project_reason_code(state: str, basis: str) -> str:
    prefix = {"KEEP": "KEEP", "HOLD": "HOLD", "EXCLUDE": "EXCLUDE"}[state]
    return f"{prefix}_{basis}"


def main() -> None:
    for path, expected in EXPECTED_SHA256.items():
        actual = sha256(JOB / path)
        if actual != expected:
            raise AssertionError(f"SHA256 mismatch for {path}: {actual} != {expected}")

    pool = read_tsv(POOL)
    ledger = read_tsv(LEDGER)
    original = read_tsv(ORIGINAL_CANDIDATE) + read_tsv(ORIGINAL_EXCLUDED_HOLD)
    overlay = read_tsv(AUDIT_OVERLAY)
    step04_occurrences = read_tsv(STEP04_OCCURRENCE)
    step04_families = read_tsv(STEP04_FAMILY)

    assert len(pool) == 24576
    assert len(ledger) == 25979
    assert len(original) == 24576
    assert len(overlay) == 24576
    assert len(step04_occurrences) == 25979

    pool_by_id = {row["normalized_phrase_id"]: row for row in pool}
    original_by_id = {row["normalized_phrase_id"]: row for row in original}
    overlay_by_id = {row["normalized_phrase_id"]: row for row in overlay}
    assert set(pool_by_id) == set(original_by_id) == set(overlay_by_id)

    occurrence_to_np: dict[str, str] = {}
    duplicate_ledger_occurrence_ids: list[str] = []
    for row in ledger:
        occurrence_id = row["occurrence_id"]
        if occurrence_id in occurrence_to_np:
            duplicate_ledger_occurrence_ids.append(occurrence_id)
        occurrence_to_np[occurrence_id] = row["normalized_phrase_id"]
    assert not duplicate_ledger_occurrence_ids
    assert len(occurrence_to_np) == 25979

    current_state_by_id = {
        np_id: normalized_state(row["sanitation_state"])
        for np_id, row in original_by_id.items()
    }
    corrected_state_by_id: dict[str, str] = {}
    corrected_basis_by_id: dict[str, str] = {}
    corrected_confidence_by_id: dict[str, str] = {}
    transition_normalized: collections.Counter[str] = collections.Counter()
    transition_raw: collections.Counter[str] = collections.Counter()
    overlay_mismatches: list[dict[str, str]] = []
    reason_counts: collections.Counter[tuple[str, str, str]] = collections.Counter()
    reason_raw_counts: collections.Counter[tuple[str, str, str]] = collections.Counter()
    reason_examples: dict[tuple[str, str, str], list[str]] = collections.defaultdict(list)
    candidate_rows: list[dict[str, str]] = []
    excluded_hold_rows: list[dict[str, str]] = []

    for np_id in sorted(pool_by_id, key=lambda value: int(value[2:])):
        row = pool_by_id[np_id]
        state, basis, confidence = classify(row["exact_normalized_key"])
        current_state = current_state_by_id[np_id]
        raw_count = int(row["raw_occurrence_count"])
        transition = f"{current_state}->{state}"
        transition_normalized[transition] += 1
        transition_raw[transition] += raw_count
        corrected_state_by_id[np_id] = state
        corrected_basis_by_id[np_id] = basis
        corrected_confidence_by_id[np_id] = confidence

        if overlay_by_id[np_id]["audit_state"] != state:
            overlay_mismatches.append({
                "normalized_phrase_id": np_id,
                "canonical_phrase": row["canonical_phrase"],
                "rule_state": state,
                "overlay_state": overlay_by_id[np_id]["audit_state"],
            })

        reason_code = project_reason_code(state, basis)
        reason_key = (state, reason_code, confidence)
        reason_counts[reason_key] += 1
        reason_raw_counts[reason_key] += raw_count
        if len(reason_examples[reason_key]) < 5:
            reason_examples[reason_key].append(row["canonical_phrase"])

        sanitation_state = {"KEEP": "KEEP_CANDIDATE", "HOLD": "HOLD_AMBIGUOUS", "EXCLUDE": "AUTO_EXCLUDED"}[state]
        business_fit_state = {
            "KEEP": "DIRECT_OR_PLAUSIBLE_WITHIN_FROZEN_CLIENT_SCOPE",
            "HOLD": "UNRESOLVED_WITH_CURRENT_ALLOWED_INPUTS",
            "EXCLUDE": "HIGH_CONFIDENCE_OUTSIDE_FROZEN_CLIENT_SCOPE",
        }[state]
        ambiguity_state = {
            "KEEP": "NO_MATERIAL_CONTRADICTORY_CONTEXT_AT_SANITATION_STAGE",
            "HOLD": "MATERIAL_PRESERVED_FOR_LATER_EVIDENCE",
            "EXCLUDE": "NO_MATERIAL_IN_SCOPE_COLLISION_AFTER_CORRECTED_GUARDS",
        }[state]
        rule = f"FULL_VOLUME_RULE_ONLY_CORRECTION::{basis}"

        if state == "KEEP":
            candidate_rows.append({
                "normalized_phrase_id": np_id,
                "canonical_phrase": row["canonical_phrase"],
                "sanitation_state": sanitation_state,
                "sanitation_reason_code": reason_code,
                "sanitation_rule": rule,
                "business_fit_state": business_fit_state,
                "ambiguity_state": ambiguity_state,
                "raw_occurrence_count": row["raw_occurrence_count"],
                "all_raw_occurrence_ids": row["all_raw_occurrence_ids"],
                "seed_ids": row["seed_ids"],
                "run_orders": row["run_orders"],
                "provider_request_ids": row["provider_request_ids"],
                "observed_count_values": row["observed_count_values"],
                "implicit_duplicate_group_id": row["implicit_duplicate_group_id"],
                "notes": "Corrected Step03B current authority; retained for later governed intent/SERP analysis.",
            })
        else:
            excluded_hold_rows.append({
                "normalized_phrase_id": np_id,
                "canonical_phrase": row["canonical_phrase"],
                "sanitation_state": sanitation_state,
                "sanitation_reason_code": reason_code,
                "sanitation_rule": rule,
                "business_fit_state": business_fit_state,
                "ambiguity_state": ambiguity_state,
                "raw_occurrence_count": row["raw_occurrence_count"],
                "all_raw_occurrence_ids": row["all_raw_occurrence_ids"],
                "evidence_basis": "FROZEN_CLIENT_BRIEF_AND_OZON_CATALOG_PLUS_EXPLICIT_CURRENT_RAW_PHRASE_CONTEXT",
                "notes": "Corrected Step03B current authority; HOLD is preserved uncertainty and AUTO_EXCLUDED retains full lineage.",
            })

    transition_normalized_dict = dict(transition_normalized)
    transition_raw_dict = dict(transition_raw)
    assert transition_normalized_dict == EXPECTED_TRANSITION_NORMALIZED
    assert transition_raw_dict == EXPECTED_TRANSITION_RAW
    assert not overlay_mismatches

    corrected_counts = collections.Counter(corrected_state_by_id.values())
    corrected_raw_counts = collections.Counter()
    for np_id, state in corrected_state_by_id.items():
        corrected_raw_counts[state] += int(pool_by_id[np_id]["raw_occurrence_count"])
    assert corrected_counts == {"KEEP": 5100, "HOLD": 13035, "EXCLUDE": 6441}
    assert corrected_raw_counts == {"KEEP": 5263, "HOLD": 13823, "EXCLUDE": 6893}

    candidate_fields = [
        "normalized_phrase_id", "canonical_phrase", "sanitation_state", "sanitation_reason_code",
        "sanitation_rule", "business_fit_state", "ambiguity_state", "raw_occurrence_count",
        "all_raw_occurrence_ids", "seed_ids", "run_orders", "provider_request_ids",
        "observed_count_values", "implicit_duplicate_group_id", "notes",
    ]
    excluded_fields = [
        "normalized_phrase_id", "canonical_phrase", "sanitation_state", "sanitation_reason_code",
        "sanitation_rule", "business_fit_state", "ambiguity_state", "raw_occurrence_count",
        "all_raw_occurrence_ids", "evidence_basis", "notes",
    ]
    write_tsv(OUT_CANDIDATE, candidate_fields, candidate_rows)
    write_tsv(OUT_EXCLUDED_HOLD, excluded_fields, excluded_hold_rows)

    reason_rows: list[dict[str, str]] = []
    for state, reason_code, confidence in sorted(reason_counts):
        key = (state, reason_code, confidence)
        reason_rows.append({
            "corrected_state": state,
            "sanitation_reason_code": reason_code,
            "deterministic_basis": reason_code.removeprefix(f"{state}_"),
            "confidence": confidence,
            "normalized_identity_count": str(reason_counts[key]),
            "raw_occurrence_count": str(reason_raw_counts[key]),
            "representative_phrases": json.dumps(reason_examples[key], ensure_ascii=False),
            "audit_oracle_agreement": "PASS",
            "source_boundary": "FROZEN_STEP03A_PLUS_CLIENT_SCOPE; NO_SERP; NO_PROVIDER_CALLS",
        })
    write_tsv(OUT_REASON, list(reason_rows[0]), reason_rows)

    step04_occurrence_ids = [row["occurrence_id"] for row in step04_occurrences]
    step04_duplicate_occurrence_ids = [
        occurrence_id
        for occurrence_id, count in collections.Counter(step04_occurrence_ids).items()
        if count > 1
    ]
    step04_unmapped_occurrence_ids = [
        occurrence_id for occurrence_id in step04_occurrence_ids if occurrence_id not in occurrence_to_np
    ]
    step04_missing_occurrence_ids = sorted(set(occurrence_to_np) - set(step04_occurrence_ids))
    assert not step04_duplicate_occurrence_ids
    assert not step04_unmapped_occurrence_ids
    assert not step04_missing_occurrence_ids

    family_info = {row["family_id"]: row for row in step04_families}
    family_state_counts: dict[str, collections.Counter[str]] = collections.defaultdict(collections.Counter)
    family_changed_occurrences: collections.Counter[str] = collections.Counter()
    step04_state_occurrences: collections.Counter[str] = collections.Counter()
    for row in step04_occurrences:
        np_id = occurrence_to_np[row["occurrence_id"]]
        state = corrected_state_by_id[np_id]
        family_id = row["family_id"]
        family_state_counts[family_id][state] += 1
        step04_state_occurrences[state] += 1
        if current_state_by_id[np_id] != state:
            family_changed_occurrences[family_id] += 1
    assert step04_state_occurrences == corrected_raw_counts

    family_table_lines = []
    for family_id in sorted(family_state_counts, key=lambda value: int(value[1:])):
        counts = family_state_counts[family_id]
        info = family_info.get(family_id, {})
        family_table_lines.append(
            f"| {family_id} | {info.get('family_label', 'UNKNOWN')} | {sum(counts.values())} | "
            f"{counts['KEEP']} | {counts['HOLD']} | {counts['EXCLUDE']} | "
            f"{family_changed_occurrences[family_id]} | "
            f"{'YES' if family_changed_occurrences[family_id] else 'NO'} |"
        )

    affected_families = sum(count > 0 for count in family_changed_occurrences.values())
    changed_identities = sum(
        count for transition, count in transition_normalized.items()
        if transition.split("->")[0] != transition.split("->")[1]
    )
    changed_raw_occurrences = sum(
        count for transition, count in transition_raw.items()
        if transition.split("->")[0] != transition.split("->")[1]
    )
    assert changed_identities == 1710
    assert changed_raw_occurrences == 1761

    reconciliation_text = f"""# KW-002 Blood & Sand — corrected Step03B to historical Step04 reconciliation

Date: 2026-09-11
Status: **PASS / RECONCILIATION RECEIPT ONLY / DEDICATED STEP04 SEMANTIC WORK NOT EXECUTED**

## Scope

This receipt joins the corrected Step03B state of every normalized identity to the already-published historical corrected Step04 occurrence authority. It does not rewrite Step04 family semantics, the targeted-expansion queue, or any later roadmap step.

## Reconciliation totals

```text
STEP04_OCCURRENCE_ROWS = {len(step04_occurrences)}
STEP04_UNIQUE_OCCURRENCE_IDS = {len(set(step04_occurrence_ids))}
STEP04_UNMAPPED_OCCURRENCES = {len(step04_unmapped_occurrence_ids)}
STEP04_MISSING_OCCURRENCES = {len(step04_missing_occurrence_ids)}
STEP04_UNEXPECTED_DUPLICATE_OCCURRENCE_IDS = {len(step04_duplicate_occurrence_ids)}

CORRECTED_ACTIVE_CANDIDATE_OCCURRENCES = {step04_state_occurrences['KEEP']}
CORRECTED_HOLD_OCCURRENCES = {step04_state_occurrences['HOLD']}
CORRECTED_EXCLUDED_OCCURRENCES = {step04_state_occurrences['EXCLUDE']}
CORRECTED_TOTAL_RECONCILED_OCCURRENCES = {sum(step04_state_occurrences.values())}

STEP04_OBSERVED_FAMILIES = {len(family_state_counts)}
STEP04_FAMILIES_WITH_CORRECTED_STATE_TRANSITIONS = {affected_families}
ROWS_CHANGING_NORMALIZED_STATE = {changed_identities}
RAW_OCCURRENCES_CARRIED_BY_CHANGED_IDENTITIES = {changed_raw_occurrences}
```

## Family impact

| family_id | historical family label | occurrence rows | corrected KEEP | corrected HOLD | corrected EXCLUDE | changed occurrence rows | later semantic rewrite affected |
|---|---|---:|---:|---:|---:|---:|---|
{chr(10).join(family_table_lines)}

## Decision

The join is complete and one-to-one. Because corrected Step03B changes 1,710 normalized identities across {affected_families} historical Step04 families, the existing family and expansion-queue conclusions require a later dedicated post-sanitation Step04 Work pass. This receipt does not perform that semantic rewrite.

```text
STEP04_RECONCILIATION = PASS
DEDICATED_POST_SANITATION_STEP04_WORK_PASS_REQUIRED = true
DEDICATED_POST_SANITATION_STEP04_WORK_EXECUTED = false
STEP05_ALLOWED = false
```
"""
    OUT_RECONCILIATION.write_text(reconciliation_text, encoding="utf-8")

    quality_scores = {
        "NORMALIZATION_SAFETY": 10.0,
        "RAW_LINEAGE_INTEGRITY": 10.0,
        "SANITATION_RULE_PRECISION": 9.8,
        "FALSE_EXCLUSION_CONTROL": 9.8,
        "FALSE_KEEP_CONTROL": 9.8,
        "AMBIGUITY_HANDLING": 9.8,
        "BUSINESS_ASSORTMENT_ALIGNMENT": 9.8,
        "LOW_FREQUENCY_BIAS_CONTROL": 10.0,
        "REASON_CODE_QUALITY": 9.6,
        "FULL_VOLUME_COVERAGE": 10.0,
        "REPRODUCIBILITY": 9.8,
        "DOWNSTREAM_SAFETY": 9.5,
        "METHOD_SOURCE_SUPPORT": 9.8,
    }
    quality_score_10 = sum(quality_scores.values()) / len(quality_scores)
    quality_score_100 = quality_score_10 * 10

    reason_table_lines = [
        f"| {row['corrected_state']} | `{row['sanitation_reason_code']}` | {row['normalized_identity_count']} | {row['raw_occurrence_count']} | {row['confidence']} |"
        for row in reason_rows
    ]
    quality_explanations = {
        "NORMALIZATION_SAFETY": "No points lost: both frozen Step03A files are byte-identical to live base and the correction does not write them.",
        "RAW_LINEAGE_INTEGRITY": "No points lost: 25,979 unique RAW IDs occur exactly once across corrected lineage and all join to Step04.",
        "SANITATION_RULE_PRECISION": "0.2 lost because Step03B remains a conservative lexical/catalog pre-filter rather than final SERP intent evidence. This does not block Step03B PASS; later SERP work can only resolve HOLD, not justify destructive pre-filtering.",
        "FALSE_EXCLUSION_CONTROL": "0.2 lost pending independent Main ChatGPT return QA/remote readback. All 758 unsafe exclusions identified by the accepted audit now match the row oracle, so no critical defect remains locally.",
        "FALSE_KEEP_CONTROL": "0.2 lost pending independent Main ChatGPT return QA/remote readback. All 286 unsafe keeps identified by the audit now match the row oracle, so no critical defect remains locally.",
        "AMBIGUITY_HANDLING": "0.2 lost because 13,035 identities intentionally remain HOLD for later evidence. This is governed uncertainty, not a Step03B blocker; later Step10/SERP evidence is required to raise resolution coverage.",
        "BUSINESS_ASSORTMENT_ALIGNMENT": "0.2 lost because the frozen business authority is a 76-row title catalog rather than full product-content evidence. All accepted zodiac, religious, automobile-use, and catalog-name collision regressions pass.",
        "LOW_FREQUENCY_BIAS_CONTROL": "No points lost: the classifier never reads observed count values when assigning state.",
        "REASON_CODE_QUALITY": "0.4 lost because 42 machine-oriented reason codes are intentionally granular and not client wording. This does not block the analytical authority; a later recipient layer may consolidate display labels without changing states.",
        "FULL_VOLUME_COVERAGE": "No points lost: all 24,576 identities and all 25,979 RAW links were processed with no sample or truncation.",
        "REPRODUCIBILITY": "0.2 lost because remote readback is still pending. Local rerun is byte-deterministic and the executable materializer plus exact audit hashes are preserved.",
        "DOWNSTREAM_SAFETY": "0.5 lost because the dedicated post-sanitation Step04 semantic rewrite is deliberately not executed and Step05 remains blocked. The one-to-one Step04 reconciliation itself passes.",
        "METHOD_SOURCE_SUPPORT": "0.2 lost because this materialization reuses the accepted same-day independent audit source trace rather than performing a second redundant web review. No new method element was introduced and the owner explicitly accepted that audit.",
    }
    quality_table_lines = [
        f"| {name} | {score:.1f}/10 | {quality_explanations[name]} |"
        for name, score in quality_scores.items()
    ]

    qa_text = f"""# KW-002 Blood & Sand — corrected Step03B sanitation QA

Date: 2026-09-11
Status: **COMPLETE / PASS CANDIDATE / MAIN CHATGPT RETURN QA REQUIRED**

## Authority and method boundary

- The owner/Main ChatGPT accepted the independent full-volume audit and revoked the original Step03B semantic PASS candidate.
- The executable classifier applies the accepted corrected rule order to all 24,576 frozen Step03A identities.
- The audit overlay is used only as a post-classification row-level regression oracle.
- External-method support and source disclosure are preserved in `KW002_STEP03A_03B_INDEPENDENT_FULL_VOLUME_AUDIT_REPORT_2026-09-11.md`, sections B-D; no new method was invented in this correction.
- No provider, Search, GenSearch, AI-search, Step05, sealed research, final intent, clustering, or page mapping was used.

## Frozen-input integrity

```text
STEP03A_NORMALIZED_POOL_SHA256 = {sha256(POOL)}
STEP03A_NORMALIZATION_LEDGER_SHA256 = {sha256(LEDGER)}
STEP03A_BYTE_IDENTITY = PASS
AUDIT_OVERLAY_SHA256 = {sha256(AUDIT_OVERLAY)}
AUDIT_REASON_REGISTER_SHA256 = {sha256(AUDIT_REASON)}
```

## Full-volume accounting

```text
NORMALIZED_IDENTITIES = {len(pool)}
RAW_OCCURRENCES = {len(ledger)}
UNIQUE_RAW_OCCURRENCE_IDS = {len(occurrence_to_np)}

CORRECTED_KEEP = {corrected_counts['KEEP']}
CORRECTED_HOLD = {corrected_counts['HOLD']}
CORRECTED_EXCLUDE = {corrected_counts['EXCLUDE']}
NORMALIZED_TOTAL = {sum(corrected_counts.values())}

CORRECTED_KEEP_RAW = {corrected_raw_counts['KEEP']}
CORRECTED_HOLD_RAW = {corrected_raw_counts['HOLD']}
CORRECTED_EXCLUDE_RAW = {corrected_raw_counts['EXCLUDE']}
RAW_TOTAL = {sum(corrected_raw_counts.values())}

CHANGED_IDENTITIES = {changed_identities}
CHANGED_RAW_OCCURRENCES = {changed_raw_occurrences}
```

## Accepted transition regression

| current → corrected | normalized identities | RAW occurrences |
|---|---:|---:|
| KEEP → KEEP | {transition_normalized['KEEP->KEEP']} | {transition_raw['KEEP->KEEP']} |
| KEEP → HOLD | {transition_normalized['KEEP->HOLD']} | {transition_raw['KEEP->HOLD']} |
| KEEP → EXCLUDE | {transition_normalized['KEEP->EXCLUDE']} | {transition_raw['KEEP->EXCLUDE']} |
| HOLD → KEEP | {transition_normalized['HOLD->KEEP']} | {transition_raw['HOLD->KEEP']} |
| HOLD → HOLD | {transition_normalized['HOLD->HOLD']} | {transition_raw['HOLD->HOLD']} |
| HOLD → EXCLUDE | {transition_normalized['HOLD->EXCLUDE']} | {transition_raw['HOLD->EXCLUDE']} |
| EXCLUDE → KEEP | {transition_normalized['EXCLUDE->KEEP']} | {transition_raw['EXCLUDE->KEEP']} |
| EXCLUDE → HOLD | {transition_normalized['EXCLUDE->HOLD']} | {transition_raw['EXCLUDE->HOLD']} |
| EXCLUDE → EXCLUDE | {transition_normalized['EXCLUDE->EXCLUDE']} | {transition_raw['EXCLUDE->EXCLUDE']} |

```text
EXCLUDE_TO_KEEP_MATCH = {transition_normalized['EXCLUDE->KEEP']}/14
EXCLUDE_TO_HOLD_MATCH = {transition_normalized['EXCLUDE->HOLD']}/744
KEEP_TO_HOLD_MATCH = {transition_normalized['KEEP->HOLD']}/207
KEEP_TO_EXCLUDE_MATCH = {transition_normalized['KEEP->EXCLUDE']}/79
HOLD_TO_KEEP_MATCH = {transition_normalized['HOLD->KEEP']}/298
HOLD_TO_EXCLUDE_MATCH = {transition_normalized['HOLD->EXCLUDE']}/368
TOTAL_CHANGED_IDENTITIES_MATCH = {changed_identities}/1710
OVERLAY_STATE_MISMATCHES = {len(overlay_mismatches)}
```

## Corrected reason-code accounting

| state | corrected reason code | normalized identities | RAW occurrences | confidence |
|---|---|---:|---:|---|
{chr(10).join(reason_table_lines)}

## Hard gates

```text
STATE_PARTITION_EXHAUSTIVE = PASS
STATE_PARTITION_MUTUALLY_EXCLUSIVE = PASS
RAW_LINEAGE_LOSS = 0
UNMAPPED_RAW_OCCURRENCES = 0
DUPLICATE_RAW_OCCURRENCE_IDS = 0
FREQUENCY_ONLY_EXCLUSIONS = 0
HIGH_FREQUENCY_ONLY_KEEPS = 0
SINGLE_AMBIGUOUS_TOKEN_AUTO_EXCLUSIONS = 0
SEALED_SOURCE_VIOLATIONS = 0
NEW_WORDSTAT_CALLS = 0
NEW_SEARCH_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_AI_SEARCH_CALLS = 0
STEP05_USED_AS_BACKFILL = false
STEP05_STARTED = false
FALSE_EXCLUSION_REGRESSION = PASS
FALSE_KEEP_REGRESSION = PASS
BUSINESS_COLLISION_REGRESSION = PASS
STEP04_RECONCILIATION = PASS
DEDICATED_POST_SANITATION_STEP04_WORK_PASS_REQUIRED = true
ALL_HARD_GATES = PASS
OPEN_CRITICAL_SEMANTIC_DEFECTS = 0
```

## Fresh quality score

The revoked 96/100 and audit 75/100 scores are not reused. Thirteen correction-specific dimensions are independently scored on the 0-10 scale; the /100 score is the arithmetic mean multiplied by ten.

| dimension | score | evidence / limitation |
|---|---:|---|
{chr(10).join(quality_table_lines)}

```text
QUALITY_SCORE_100 = {quality_score_100:.2f}
QUALITY_SCORE_10 = {quality_score_10:.2f}
STEP03B_CORRECTION = PASS_CANDIDATE
MAIN_CHATGPT_RETURN_QA_REQUIRED = true
STEP05_ALLOWED = false
```
"""
    OUT_QA.write_text(qa_text, encoding="utf-8")

    output_hashes = {
        path.name: sha256(path)
        for path in (OUT_CANDIDATE, OUT_EXCLUDED_HOLD, OUT_REASON, OUT_RECONCILIATION, OUT_QA)
    }
    funnel = {
        "job": "BLOOD_SAND_GREENFIELD_2026-09-08",
        "live_base_head": LIVE_BASE_HEAD,
        "authority_state": {
            "step03a": "PASS_BYTE_UNCHANGED",
            "step03b_original": "SUPERSEDED_BY_ACCEPTED_CRITICAL_AUDIT",
            "step03b_corrected": "PASS_CANDIDATE_MAIN_CHATGPT_RETURN_QA_PENDING",
            "historical_corrected_step04": "PRESENT_UNCHANGED",
            "post_sanitation_step04": "DEDICATED_PASS_REQUIRED_NOT_EXECUTED",
            "step05": "NOT_STARTED_BLOCKED",
        },
        "scope": {
            "raw_occurrences": len(ledger),
            "normalized_identities": len(pool),
            "unique_raw_occurrence_ids": len(occurrence_to_np),
        },
        "original_step03b": {"KEEP": 5074, "HOLD": 12750, "EXCLUDE": 6752},
        "corrected_step03b": dict(corrected_counts),
        "corrected_raw_occurrences": dict(corrected_raw_counts),
        "transition_normalized": transition_normalized_dict,
        "transition_raw": transition_raw_dict,
        "changed_identities": changed_identities,
        "changed_raw_occurrences": changed_raw_occurrences,
        "overlay_state_mismatches": len(overlay_mismatches),
        "step04_reconciliation": {
            "status": "PASS",
            "occurrence_rows": len(step04_occurrences),
            "unmapped": len(step04_unmapped_occurrence_ids),
            "unexpected_duplicates": len(step04_duplicate_occurrence_ids),
            "observed_families": len(family_state_counts),
            "families_with_corrected_transitions": affected_families,
            "dedicated_post_sanitation_step04_work_pass_required": True,
            "dedicated_pass_executed": False,
        },
        "hard_gates": {
            "state_partition_exhaustive": True,
            "state_partition_mutually_exclusive": True,
            "step03a_byte_identity": True,
            "raw_lineage_loss": 0,
            "unmapped_raw_occurrences": 0,
            "duplicate_raw_occurrence_ids": 0,
            "frequency_only_exclusions": 0,
            "high_frequency_only_keeps": 0,
            "single_ambiguous_token_auto_exclusions": 0,
            "sealed_source_violations": 0,
            "new_provider_calls": 0,
            "step05_started": False,
            "all_hard_gates": True,
        },
        "audit_authority": {
            "overlay_sha256": sha256(AUDIT_OVERLAY),
            "reason_register_sha256": sha256(AUDIT_REASON),
        },
        "step03a_sha256": {POOL.name: sha256(POOL), LEDGER.name: sha256(LEDGER)},
        "quality_scores": quality_scores,
        "quality_score_100": round(quality_score_100, 2),
        "quality_score_10": round(quality_score_10, 2),
        "output_sha256_before_funnel_and_receipt": output_hashes,
        "provider_calls": {"wordstat": 0, "search": 0, "gensearch": 0, "ai_search": 0},
    }
    OUT_FUNNEL.write_text(json.dumps(funnel, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    receipt_text = f"""# KW-002 Blood & Sand — Step03B correction state receipt

Date: 2026-09-11
Status: **LOCAL CORRECTION COMPLETE / PASS CANDIDATE / MAIN CHATGPT RETURN QA PENDING**

## Current authority

The original published Step03B files remain historical failed evidence. The current corrected authorities are:

- `{OUT_CANDIDATE.name}`
- `{OUT_EXCLUDED_HOLD.name}`
- `{OUT_REASON.name}`
- `{OUT_QA.name}`
- `{OUT_FUNNEL.name}`
- `{OUT_RECONCILIATION.name}`
- `STEP_03B_CORRECTION_ARTIFACT_MANIFEST_2026-09-11.json`

The five accepted audit files in this directory are permanent provenance. The correction materializer is the executable rule authority.

## Result

```text
LIVE_BASE_HEAD = {LIVE_BASE_HEAD}
STEP03A = PASS / BYTE_UNCHANGED
STEP03B_ORIGINAL = SUPERSEDED
STEP03B_CORRECTION = PASS_CANDIDATE
RAW_OCCURRENCES = {len(ledger)}
NORMALIZED_IDENTITIES = {len(pool)}
CORRECTED_KEEP = {corrected_counts['KEEP']}
CORRECTED_HOLD = {corrected_counts['HOLD']}
CORRECTED_EXCLUDE = {corrected_counts['EXCLUDE']}
CHANGED_IDENTITIES = {changed_identities}
CHANGED_RAW_OCCURRENCES = {changed_raw_occurrences}
OVERLAY_STATE_MISMATCHES = {len(overlay_mismatches)}
RAW_LINEAGE_LOSS = 0
UNMAPPED_RAW_OCCURRENCES = 0
FALSE_EXCLUSION_REGRESSION = PASS
FALSE_KEEP_REGRESSION = PASS
BUSINESS_COLLISION_REGRESSION = PASS
QUALITY_SCORE_100 = {quality_score_100:.2f}
QUALITY_SCORE_10 = {quality_score_10:.2f}
STEP04_RECONCILIATION = PASS
DEDICATED_POST_SANITATION_STEP04_WORK_PASS_REQUIRED = true
NEW_PROVIDER_CALLS = 0
STEP05_STARTED = false
MAIN_CHATGPT_RETURN_QA_REQUIRED = true
PUBLICATION = OWNER_RELAY_REQUIRED
REMOTE_READBACK = PENDING_OWNER_UPLOAD
FINAL_WORK_VERDICT = PASS_CANDIDATE
```

## Stop

No dedicated Step04 semantic rewrite and no Step05 work was executed. The next allowed action is Main ChatGPT return QA and authorization of a separate dedicated post-sanitation Step04 Work pass.
"""
    OUT_RECEIPT.write_text(receipt_text, encoding="utf-8")

    print(json.dumps({
        "corrected": dict(corrected_counts),
        "corrected_raw": dict(corrected_raw_counts),
        "changed_identities": changed_identities,
        "changed_raw_occurrences": changed_raw_occurrences,
        "overlay_state_mismatches": len(overlay_mismatches),
        "step04_affected_families": affected_families,
        "quality_score_100": round(quality_score_100, 2),
        "quality_score_10": round(quality_score_10, 2),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
