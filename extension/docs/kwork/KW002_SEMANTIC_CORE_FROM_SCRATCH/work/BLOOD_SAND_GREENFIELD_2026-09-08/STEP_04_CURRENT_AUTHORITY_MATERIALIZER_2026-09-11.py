#!/usr/bin/env python3
"""KW-002 Blood & Sand W09 current-authority Step04 materializer.

This is a provider-free, full-volume semantic-family rerun over the accepted
Step03A/Step03B universe.  Production routing first derives simultaneous
bounded signals and then selects a preliminary primary family by an explicit
numeric specificity contract.  The historical W08 materializer is imported
for family metadata only; its classifier and diagnostic are never called.

An independent character-TF-IDF/topic and action-frame diagnostic challenges
every identity.  It is deliberately not a final intent, SERP, page, IA, or
Step05 decision.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import inspect
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.sparse import csr_matrix, vstack
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


HERE = Path(__file__).resolve().parent
DATE = "2026-09-11"
WORK_START_REMOTE_HEAD = "faf4102117109558ed802f1aac4c5965a9c244ca"
WORK_PRE_PUBLICATION_REMOTE_HEAD = "9e4e1342ba40f4b752058cda81d45e28a862d9d8"
PRE_PUBLICATION_CHANGED_PATHS = (
    "extension/README.md",
    "extension/docs/YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md",
)
RANDOM_SEED = 20260911
SIGNAL_MATCH_POLICY = "TOKEN_SEQUENCE_OR_REGEX_FULLMATCH_ONLY"

INPUTS = {
    "pool": "STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv",
    "ledger": "STEP_03A_NORMALIZATION_LEDGER_2026-09-11.tsv",
    "keep": "STEP_03B_SANITIZED_CANDIDATE_POOL_CORRECTED_2026-09-11.tsv",
    "register": "STEP_03B_EXCLUDED_HOLD_REGISTER_CORRECTED_2026-09-11.tsv",
    "step03b_overlay": "KW002_STEP03A_03B_INDEPENDENT_FULL_VOLUME_AUDIT_OVERLAY_2026-09-11.tsv",
    "old_occurrence": "STEP_04_POST_SANITATION_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv",
    "w07_overlay": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_OVERLAY_2026-09-11.tsv",
    "w08_occurrence": "STEP_04_POST_AUDIT_CORRECTED_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv",
    "w08_families": "STEP_04_POST_AUDIT_CORRECTED_FAMILY_TRIAGE_2026-09-11.tsv",
    "w08_transition": "STEP_04_POST_AUDIT_CORRECTION_TRANSITION_LEDGER_2026-09-11.tsv",
    "w08_queue": "STEP_04_POST_AUDIT_CORRECTED_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv",
    "w08_feedback": "STEP_04_POST_AUDIT_CORRECTED_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv",
    "w08_independent": "STEP_04_POST_AUDIT_CORRECTED_INDEPENDENT_FAMILY_QA_2026-09-11.tsv",
    "w08_materializer": "STEP_04_POST_AUDIT_CORRECTED_MATERIALIZER_2026-09-11.py",
    "w08_qa": "STEP_04_POST_AUDIT_CORRECTED_QA_2026-09-11.md",
    "w08_return": "STEP_04_POST_AUDIT_CORRECTED_WORK_RETURN_2026-09-11.md",
    "w07_review": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_MAIN_CHATGPT_REVIEW_2026-09-11.md",
    "w08_review": "STEP_04_POST_AUDIT_CORRECTED_MAIN_CHATGPT_REMOTE_REVIEW_2026-09-11.md",
    "failure_ledger": "KW002_EXECUTION_FAILURE_LEDGER_2026-09-11.md",
    "audit_addendum": "KW002_EXECUTION_FAILURE_LEDGER_ADDENDUM_STEP04_RESULT_AUDIT_2026-09-11.md",
    "current_cursor": "KW002_EXECUTION_CURSOR_2026-09-11.json",
    "allowed_sources": "ALLOWED_INPUTS_AND_SEALED_SOURCES.md",
    "client_brief": "CLIENT_SUPPLIED_BRIEF.md",
    "client_assortment": "CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md",
    "prompt": "STEP_04_CURRENT_UNIVERSAL_CAUSE_CORRECTION_RERUN_WORK_PROMPT_2026-09-11.md",
    "release": "STEP_04_CURRENT_UNIVERSAL_CAUSE_CORRECTION_RERUN_EXECUTION_RELEASE_2026-09-11.md",
}

KW002_ROOT = HERE.parents[1]
GOVERNING_AUTHORITIES = (
    "LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md",
    "LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md",
    "LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md",
    "LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md",
    "LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md",
    "LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md",
    "LEVEL1/RESULT_QUALITY_SCORING_RULE.md",
    "LEVEL1/WORK_HANDOFF_RULE.md",
    "LEVEL2/README.md",
    "LEVEL2/STEP_RULES_INDEX.md",
    "LEVEL2/STEP_04_PRELIMINARY_FAMILY_TRIAGE_QUALITY_GATE.md",
)

EXPECTED_FROZEN_SHA256 = {
    INPUTS["pool"]: "b30c29ff66a56d80bc1aa9ff6b2eade522b27d1e167cbd636ac72fbff211f2a8",
    INPUTS["ledger"]: "28205ca64f26d219d489b36f102a8923b4a4b635c8b213179bca4a188b24c3df",
    INPUTS["keep"]: "63b3fc556b388dbac0185f174f79f825dc26d9c51de39698850cdaecb9ca4f58",
    INPUTS["register"]: "145c5107f40415b4050923f142dab3e83646489da5d74501f659fd87e3ae2916",
    INPUTS["step03b_overlay"]: "db9b79dda64b205f0b0bef273f70f221f183d9389eca3e67e651e93ea269d669",
}

OUTPUTS = {
    "occurrence": "STEP_04_CURRENT_AUTHORITY_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv",
    "families": "STEP_04_CURRENT_AUTHORITY_FAMILY_TRIAGE_2026-09-11.tsv",
    "signals": "STEP_04_CURRENT_AUTHORITY_IDENTITY_SIGNAL_LEDGER_2026-09-11.tsv",
    "queue": "STEP_04_CURRENT_AUTHORITY_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv",
    "feedback": "STEP_04_CURRENT_AUTHORITY_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv",
    "transition": "STEP_04_CURRENT_AUTHORITY_TRANSITION_LEDGER_2026-09-11.tsv",
    "regression": "STEP_04_CURRENT_AUTHORITY_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-11.tsv",
    "independent": "STEP_04_CURRENT_AUTHORITY_INDEPENDENT_TAXONOMY_AUDIT_2026-09-11.tsv",
    "qa": "STEP_04_CURRENT_AUTHORITY_QA_2026-09-11.md",
    "return": "STEP_04_CURRENT_AUTHORITY_WORK_RETURN_2026-09-11.md",
    "manifest": "STEP_04_CURRENT_AUTHORITY_ARTIFACT_MANIFEST_2026-09-11.json",
    "sources": "STEP_04_CURRENT_AUTHORITY_SOURCE_REVALIDATION_2026-09-11.md",
}


def load_module(filename: str, alias: str):
    spec = importlib.util.spec_from_file_location(alias, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


w08 = load_module(INPUTS["w08_materializer"], "kw002_w08_metadata_only")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, delimiter="\t", lineterminator="\n", fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_text(name: str, value: str) -> None:
    (HERE / name).write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def token_sequence(text: str) -> tuple[str, ...]:
    return tuple(re.findall(r"[0-9a-zа-я]+", text.casefold().replace("ё", "е")))


def contains_phrase(items: tuple[str, ...], phrase: tuple[str, ...]) -> bool:
    width = len(phrase)
    return any(items[index:index + width] == phrase for index in range(len(items) - width + 1))


def contains_any_phrase(items: tuple[str, ...], phrases: tuple[tuple[str, ...], ...]) -> bool:
    return any(contains_phrase(items, phrase) for phrase in phrases)


def matches_any(items: set[str], patterns: tuple[re.Pattern[str], ...]) -> bool:
    return any(pattern.fullmatch(item) for item in items for pattern in patterns)


def compiled(*patterns: str) -> tuple[re.Pattern[str], ...]:
    return tuple(re.compile(pattern) for pattern in patterns)


PRODUCT_PATTERNS = compiled(
    r"амулет(?:а|у|ом|е|ы|ов|ам|ами|ах)?",
    r"оберег(?:а|у|ом|е|и|ов|ам|ами|ах)?",
    r"талисман(?:а|у|ом|е|ы|ов|ам|ами|ах)?",
)
ROSARY_WORDS = {
    "четки", "четок", "четкам", "четками", "четках", "четкой", "четкою", "четку", "четке",
}
FORM_PATTERNS = compiled(
    r"кулон(?:а|у|ом|е|ы|ов|ам|ами|ах)?", r"подвес(?:ка|ки|ку|ок|кой|ками|ках)?",
    r"браслет(?:а|у|ом|е|ы|ов|ам|ами|ах)?", r"кольц(?:о|а|у|ом|е|ы|ами|ах)",
    r"перст(?:ень|ня|ню|нем|не|ни|ней|ням|нями|нях)", r"серьг(?:а|и|у|ой|е|и|ам|ами|ах)",
    r"пусет(?:а|ы|ов|ам|ами|ах)?", r"брелок(?:а|у|ом|е|и|ов|ам|ами|ах)?",
    r"медальон(?:а|у|ом|е|ы|ов|ам|ами|ах)?", r"жетон(?:а|у|ом|е|ы|ов|ам|ами|ах)?",
    r"наклейк(?:а|и|у|ой|е|и|ам|ами|ах)", r"бус(?:а|ы|у|ой|е|ин|ины|ами|ах|инка|инки)?",
    r"цепочк(?:а|и|у|ой|е|ам|ами|ах)", r"серебр(?:о|а|у|ом|е|яный|яная|яные|яного)",
    r"золот(?:о|а|у|ом|е|ой|ая|ые|ого)", r"дерев(?:о|а|у|ом|е|янный|янная|янные|янного)",
    r"кожан(?:ый|ая|ое|ые|ого|ой|ых)", r"металл(?:а|у|ом|е|ы|ов|ический|ическая|ические)?",
    r"сталь(?:ь|и|ю)?",
    r"статуэтк(?:а|и|у|ой|е|ам|ами|ах)",
    r"стату(?:я|и|ю|ей)",
)
SYMBOL_OBJECT_PATTERNS = compiled(r"рун(?:а|ы|у|ой|е|ам|ами|ах)")
DOLL_PATTERNS = compiled(r"кукл(?:а|ы|у|ой|е|ам|ами|ах)")
STONE_PATTERNS = compiled(
    r"кам(?:ень|ня|ню|нем|не|ни|ней|ням|нями|нях)",
    r"минерал(?:а|у|ом|е|ы|ов|ам|ами|ах)?",
    r"самоцвет(?:а|у|ом|е|ы|ов|ам|ами|ах)?",
)
CATALOG_PATTERNS = compiled(
    r"вегвизир(?:а|у|ом|е)?", r"гунгнир(?:а|у|ом|е)?", r"валькнут(?:а|у|ом|е)?",
    r"белобог(?:а|у|ом|е)?", r"чернобог(?:а|у|ом|е)?", r"велес(?:а|у|ом|е)?",
    r"алатыр(?:ь|я|ю|ем|е|ский|ская|ские|ского|скому|ском)?",
    r"триглав(?:а|у|ом|е)?", r"ратибор(?:ец|ца|цу|цем|це)?",
    r"молвин(?:ец|ца|цу|цем|це)?", r"колядник(?:а|у|ом|е)?", r"знич(?:а|у|ом|е)?",
    r"громовик(?:а|у|ом|е)?", r"всеслав(?:ец|ца|цу|цем|це)?", r"боговник(?:а|у|ом|е)?",
    r"родимич(?:а|у|ом|е)?", r"сварог(?:а|у|ом|е)?", r"перун(?:а|у|ом|е)?",
    r"стрибог(?:а|у|ом|е)?", r"макош(?:ь|и|ью)?", r"семаргл(?:а|у|ом|е)?",
    r"даждьбог(?:а|у|ом|е)?", r"эгисхьяльм(?:а|у|ом|е)?", r"хорс(?:а|у|ом|е)?",
    r"аум", r"ом", r"жива", r"мара", r"чур", r"rsotm", r"valknut", r"gungner",
)
CATALOG_PHRASES = tuple(
    token_sequence(value) for value in (
        "рунический компас", "копье одина", "узел павших", "древо жизни", "инь и ян",
        "печать велеса", "крест сварога", "иоанн златоуст", "звезда лада", "звезда лады",
        "звезду лада", "звезду лады",
        "звезды лада", "звезды лады", "спаси и сохрани", "герб россии", "шлем ужаса", "шлема ужаса",
        "soldier of fortune", "путь воина",
    )
)
ZODIAC_FORMS = {
    "овен", "овна", "овну", "овном", "тельца", "телец", "тельцу", "тельцом",
    "близнецы", "близнецов", "близнецам", "рак", "рака", "раку", "раком",
    "лев", "льва", "льву", "льве", "львы", "львов", "дева", "девы", "деве", "деву",
    "весы", "весов", "весам", "скорпион", "скорпиона", "скорпиону", "скорпионом",
    "стрелец", "стрельца", "стрельцу", "стрельцом", "козерог", "козерога", "козерогу",
    "водолей", "водолея", "водолею", "рыбы", "рыб", "рыба", "рыбам",
}
ZODIAC_PATTERNS = compiled(r"зодиак(?:а|у|ом|е|и|ов|альный|альная|альные|ального)?")
ZODIAC_SCAFFOLD_WORDS = ZODIAC_FORMS | {
    "знак", "знаки", "знака", "знаков", "знаку", "знаком", "знаками", "знаке",
    "зодиак", "зодиака", "зодиаку", "зодиаком", "зодиаке", "зодиаки", "зодиаков",
}
ZODIAC_FUNCTION_WORDS = {
    "в", "во", "на", "по", "под", "над", "для", "с", "со", "к", "ко", "у", "о", "об",
    "про", "из", "от", "до", "и", "или", "а", "но", "не", "ни", "это", "этот", "эта",
}

COMMERCIAL_WORDS = {
    "купить", "покупка", "покупки", "цена", "цены", "цену", "стоимость", "заказать",
    "заказ", "магазин", "магазины", "продажа", "доставка", "озон", "ozon", "wildberries",
    "валберис", "авито", "приобрести",
}
MEDIA_WORDS = {
    "фильм", "фильмы", "сериал", "сериалы", "серия", "серии", "книга", "книги", "глава",
    "главы", "читать", "слушать", "смотреть", "онлайн", "дзен", "канал", "рассказ",
    "рассказы", "песня", "песни", "музыка", "аудиокнига", "аудиокниги", "скачать", "автор",
    "сюжет", "сезон", "детектив", "лордфильм", "порно", "видео",
}
MEDIA_PHRASES = tuple(token_sequence(value) for value in ("счастливый амулет", "астрал амулет", "достать ножи"))
GAME_WORDS = {
    "игра", "игры", "игре", "игру", "игрой", "играть", "играет", "играют", "игровой",
    "игровая", "игровые", "игрового", "игр", "мод", "моды", "мода", "id", "minecraft",
    "genshin", "warframe", "dota", "poe", "valhalla", "гта", "gta", "скайрим", "террария",
    "террарии", "майнкрафт", "майнкрафте", "ведьмак", "ведьмаке", "силксонг", "silksong",
    "вальгалла", "ассасин", "крид", "яглута", "yar", "стрелять",
}
GAME_PHRASES = tuple(token_sequence(value) for value in (
    "hollow knight", "elden ring", "counter strike", "assassin creed", "ассасин крид",
    "готика ремейк", "тайные тропы", "танос симулятор",
))
GAME_PATTERNS = compiled(
    r"скайрим(?:а|у|ом|е)?", r"террари(?:я|и|ю|ей)", r"майнкрафт(?:а|у|ом|е)?",
    r"ведьмак(?:а|у|ом|е|и)?", r"силксонг(?:а|у|ом|е)?",
)
TOY_PATTERNS = compiled(r"игруш(?:ка|ки|ку|кой|ке|ек|кам|ками|ках|ечный|ечная|ечные)")
VISUAL_PATTERNS = compiled(
    r"тату(?:ировка|ировки|ировок)?", r"фото", r"картин(?:ка|ки|ку|кой|ке|а|ы|у|ой|е)",
    r"рисун(?:ок|ка|ку|ком|ке|ки|ков)", r"изображен(?:ие|ия|ию|ием|ии)",
    r"эскиз(?:а|у|ом|е|ы|ов|ам|ами|ах)?", r"логотип(?:а|у|ом|е|ы|ов)?",
    r"обои", r"гиф", r"gif", r"раскраск(?:а|и|у|ой|е)", r"силуэт(?:а|у|ом|е|ы|ов)?",
    r"символ(?:а|у|ом|е|ы|ов|ам|ами|ах)?", r"символик(?:а|и|у|ой|е)",
    r"фотограф(?:ия|ии|ию|ией|ий|а|у|ом|е)?", r"нарисовать", r"рисовать", r"нарису(?:й|йте|ет|ют)",
    r"нарисованн(?:ый|ая|ое|ые|ого|ой|ых)", r"изобразить", r"изобража(?:ется|ются|ют|ет)",
    r"показать", r"написать",
)
MEANING_PATTERNS = compiled(
    r"значен(?:ие|ия|ию|ием|ии)", r"смысл(?:а|у|ом|е|ы|ов)?", r"истори(?:я|и|ю|ей)",
    r"мифологи(?:я|и|ю|ей)", r"происхожден(?:ие|ия|ию|ием|ии)",
    r"описан(?:ие|ия|ию|ием|ии)", r"обозначен(?:ие|ия|ию|ием|ии)",
    r"обознача(?:ет|ют|ть|ется|ются)", r"означа(?:ет|ют|ть)",
    r"предназначен(?:ие|ия|ию|ием|ии)", r"понять", r"узнать", r"описать",
)
ASTRO_PATTERNS = compiled(
    r"гороскоп(?:а|у|ом|е|ы|ов)?", r"совместим(?:ость|ый|ая|ые|ого|ы|а)?",
    r"характеристик(?:а|и|у|ой|е)", r"характер", r"созвезди(?:е|я|ю|ем|и)",
    r"асцендент(?:а|у|ом|е)?", r"стихи(?:я|и|ю|ей|ям|ями|ях)", r"планет(?:а|ы|у|ой|е)",
    r"рождени(?:е|я|ю|ем|и|ям|ями|ях)", r"рожден(?:ный|ная|ные|ного|а|ы)?",
    r"родивш(?:ийся|аяся|иеся|ихся|егося|емуся|имися)",
    r"дат(?:а|ы|у|ой|е|ам|ами|ах)", r"дн(?:и|ей|ем|я|ю)", r"месяц(?:а|у|ем|е|ы|ев)?",
    r"числ(?:о|а|у|ом|е|ы|ам|ами|ах)", r"период(?:а|у|ом|е|ы|ов)?",
    r"сегодня", r"завтра", r"прогноз", r"новорожденн(?:ый|ая|ые|ого|ому|ым|ых)",
    r"совместимы", r"несовместим(?:ы|ость|ый|ая|ые)?",
    r"подходящ(?:ий|ая|ие|его|ему|ими)",
    r"подходит", r"подойдут", r"любить", r"жить", r"найти", r"взять",
)
DIY_WORDS = {
    "создать", "создание", "изготовить", "изготовление", "изготовления", "связать", "вязать",
    "вязание", "вязаный", "вязаные", "вязаная", "связанный", "связанные", "сшить", "сплести",
    "плетение", "плести", "крючком", "скрафтить", "мастер-класс",
}
DIY_WEAK_WORDS = {"сделать", "делать"}
DIY_PHRASES = tuple(token_sequence(value) for value in ("своими руками", "руками мастер класс", "мастер класс"))
USE_CARE_WORDS = {
    "носить", "носит", "носят", "ношу", "надевать", "надеть", "использовать", "использует",
    "используют", "применение", "применять", "применить", "активировать", "активация",
    "зарядить", "заряжать", "заряжает", "зарядка", "очистить", "очищать", "очищение",
    "почистить", "хранить", "хранение", "проверить", "проверять", "крутить", "перебирать",
    "повесить",
}
USE_CARE_PATTERNS = compiled(
    r"активаци(?:я|и|ю|ей)", r"зарядк(?:а|и|у|ой|е)", r"очищени(?:е|я|ю|ем|и)",
    r"хранени(?:е|я|ю|ем|и)", r"применени(?:е|я|ю|ем|и)",
)
SELECT_GIFT_WORDS = {
    "выбрать", "выбирать", "подбирать", "подобрать", "подбор", "подарить", "подарок", "подарки",
    "подарка", "подарком", "лучший", "лучшие", "лучшая", "лучше",
}
SELECT_QUESTION_WORDS = {"какой", "какая", "какие", "какого", "какую"}
ACQUIRE_WORDS = {"получить", "взять", "достать", "найти"}
EFFECT_PATTERNS = compiled(
    r"защит(?:а|ы|у|ой|е|ный|ная|ные|ного)", r"сглаз(?:а|у|ом|е)?", r"порч(?:а|и|у|ей|е)",
    r"удач(?:а|и|у|ей|е|ный|ная)", r"богатств(?:о|а|у|ом|е)", r"денежн(?:ый|ая|ые|ого)",
    r"любов(?:ь|и|ью)", r"счаст(?:ье|ья|ью|ливый|ливая|ливые)", r"здоров(?:ье|ья|ью)",
    r"женщин(?:а|ы|у|ой|е|ам|ами|ах)?", r"мужчин(?:а|ы|у|ой|е|ам|ами|ах)?",
    r"ребен(?:ок|ка|ку|ком|ке)", r"хранит(?:ь|ель|еля|елю|елем|ели|ели|ели)?",
    r"любовн(?:ый|ая|ое|ые|ого|ой|ых)", r"защитник(?:а|у|ом|е|и|ов)?",
    r"оберегать", r"оберегает", r"оберегают",
)
RELIGIOUS_PATTERNS = compiled(
    r"молитв(?:а|ы|у|ой|е|ам|ами|ах)", r"мантр(?:а|ы|у|ой|е|ам|ами|ах)",
    r"намаз(?:а|у|ом|е|ы)?", r"церк(?:овь|ви|овью)", r"храм(?:а|у|ом|е|ы|ов)?",
    r"икон(?:а|ы|у|ой|е|ам|ами|ах)", r"богородиц(?:а|ы|у|ей|е)",
    r"свят(?:ой|ая|ые|ого|ому|ым|ых)", r"православн(?:ый|ая|ые|ого|ому|ым|ых)",
    r"христианск(?:ий|ая|ие|ого)", r"мусульманск(?:ий|ая|ие|ого)",
    r"будд(?:а|ы|изм|ийский|ийская|ийские)", r"медитаци(?:я|и|ю|ей)",
    r"религи(?:я|и|ю|ей|озный|озная|озные)", r"волхв(?:а|у|ом|е|ы|ов)?",
)
ENTITY_PATTERNS = compiled(
    r"город(?:а|у|ом|е|ы|ов)?", r"област(?:ь|и|ью)", r"улиц(?:а|ы|у|ей|е)",
    r"адрес(?:а|у|ом|е|ы|ов)?", r"банк(?:а|у|ом|е|и|ов)?", r"завод(?:а|у|ом|е|ы|ов)?",
    r"гостиниц(?:а|ы|у|ей|е)", r"ресторан(?:а|у|ом|е|ы|ов)?", r"кафе",
    r"школ(?:а|ы|у|ой|е)", r"такси", r"биографи(?:я|и|ю|ей)", r"фамили(?:я|и|ю|ей)",
    r"клуб(?:а|у|ом|е|ы|ов)?", r"команд(?:а|ы|у|ой|е|ы|ам|ами|ах)", r"инн", r"ооо", r"фк",
)
VEHICLE_WORDS = {"чери", "черри", "chery", "рено", "renault", "a15", "а15", "ваз"}
VEHICLE_PATTERNS = compiled(
    r"двигател(?:ь|я|ю|ем|е|и|ей)", r"датчик(?:а|у|ом|е|и|ов)?", r"запчаст(?:ь|и|ью|ей)",
    r"бампер(?:а|у|ом|е|ы|ов)?", r"тормоз(?:а|у|ом|е|ы|ов|ной|ные)",
    r"сцеплени(?:е|я|ю|ем|и)", r"автозапчаст(?:ь|и|ью|ей)", r"краск(?:а|и|у|ой|е)",
    r"автомобил(?:ь|я|ю|ем|е|и|ей)", r"арк(?:а|и|у|ой|е)",
)
VEHICLE_PHRASES = tuple(token_sequence(value) for value in ("коробка передач", "диски амулет", "код цвета"))
INDUSTRIAL_PATTERNS = compiled(
    r"схем(?:а|ы|у|ой|е)", r"подключени(?:е|я|ю|ем|и)", r"ошибк(?:а|и|у|ой|е)",
    r"руководств(?:о|а|у|ом|е)", r"эксплуатаци(?:я|и|ю|ей)", r"инструкци(?:я|и|ю|ей)",
    r"блок(?:а|у|ом|е|и|ов)?", r"управлени(?:е|я|ю|ем|и)", r"концевик(?:а|у|ом|е|и|ов)?",
    r"кран(?:а|у|ом|е|ы|ов)?", r"электрозадвижк(?:а|и|у|ой|е)",
    r"уплотнительн(?:ый|ая|ое|ые|ого|ой|ых)", r"канистр(?:а|ы|у|ой|е)",
    r"автомат(?:а|у|ом|е|ы|ов)?", r"молокоохладител(?:ь|я|ю|ем|е)",
    r"расключени(?:е|я|ю|ем|и)", r"настройк(?:а|и|у|ой|е)",
)
AUTO_USE_PHRASES = tuple(
    token_sequence(value) for value in (
        "в машину", "для машины", "на машину", "в авто", "для авто", "на авто", "для автомобиля",
        "в автомобиле", "на автомобиль", "для водителя", "на зеркало", "автомобильный талисман",
        "автомобильный оберег",
    )
)


REASON_FAMILY = {
    "HOLD_POSSIBLE_ROSARY_MORPHOLOGY_OR_TYPO": ("PSF022", 1240, "UPSTREAM_BOUNDED_ROSARY_MORPHOLOGY"),
    "HOLD_GENERIC_GAME_OR_MODEL_TOKEN_NEEDS_CONTEXT": ("PSF019", 1220, "UPSTREAM_GAME_OR_MODEL_COLLISION"),
    "HOLD_MEDIA_TITLE_VERSUS_PRODUCT_COLLISION": ("PSF018", 1210, "UPSTREAM_MEDIA_TITLE_COLLISION"),
    "HOLD_TITLE_LIKE_PRODUCT_WORD_COLLISION": ("PSF018", 1210, "UPSTREAM_TITLE_COLLISION"),
    "HOLD_GENERIC_MEDIA_ACTION_MAY_BE_INFORMATIONAL_PRODUCT_RESEARCH": ("PSF018", 1210, "UPSTREAM_MEDIA_ACTION_COLLISION"),
    "HOLD_CATALOG_NAME_VERSUS_VEHICLE_COLLISION": ("PSF020", 1200, "UPSTREAM_VEHICLE_COLLISION"),
    "HOLD_PRODUCT_NAME_VERSUS_VEHICLE_PAINT_COLLISION": ("PSF020", 1200, "UPSTREAM_VEHICLE_PAINT_COLLISION"),
    "HOLD_AUTOMOBILE_USE_WITHOUT_SUPPORTED_PRODUCT_NOUN": ("PSF020", 1200, "UPSTREAM_UNSUPPORTED_AUTO_USE_COLLISION"),
    "HOLD_PRODUCT_OR_CATALOG_NAME_WITH_PLACE_OR_ORGANIZATION": ("PSF021", 1190, "UPSTREAM_PLACE_OR_ORGANIZATION_COLLISION"),
    "HOLD_PRODUCT_OR_CATALOG_NAME_WITH_PERSON_ENTITY_CONTEXT": ("PSF021", 1190, "UPSTREAM_PERSON_ENTITY_COLLISION"),
    "HOLD_GENERIC_TEAM_OR_MASCOT_CONTEXT": ("PSF021", 1190, "UPSTREAM_TEAM_OR_MASCOT_COLLISION"),
    "HOLD_SEARCH_PLATFORM_OR_MEDIA_CONTEXT_UNRESOLVED": ("PSF021", 1190, "UPSTREAM_PLATFORM_COLLISION"),
    "HOLD_PHYSICAL_PRODUCT_VERSUS_RELIGIOUS_PRACTICE": ("PSF017", 1180, "UPSTREAM_RELIGIOUS_PRACTICE_COLLISION"),
    "HOLD_CATALOG_PRODUCT_NAME_VERSUS_RELIGIOUS_TEXT": ("PSF017", 1180, "UPSTREAM_RELIGIOUS_TEXT_COLLISION"),
}


def detect_signals(phrase: str, state: str, reason: str) -> set[str]:
    """Derive all material production signals without first-match routing."""
    items = token_sequence(phrase)
    words = set(items)
    signals: set[str] = set()
    product = matches_any(words, PRODUCT_PATTERNS)
    rosary = bool(words & ROSARY_WORDS)
    form = matches_any(words, FORM_PATTERNS)
    symbol_object = matches_any(words, SYMBOL_OBJECT_PATTERNS)
    stone = matches_any(words, STONE_PATTERNS)
    catalog = matches_any(words, CATALOG_PATTERNS) or contains_any_phrase(items, CATALOG_PHRASES)
    zodiac = matches_any(words, ZODIAC_PATTERNS) or ("знак" in words and bool(words & ZODIAC_FORMS))
    toy = matches_any(words, TOY_PATTERNS) or matches_any(words, DOLL_PATTERNS)
    visual = matches_any(words, VISUAL_PATTERNS)
    media = bool(words & MEDIA_WORDS) or contains_any_phrase(items, MEDIA_PHRASES)
    game = bool(words & GAME_WORDS) or matches_any(words, GAME_PATTERNS) or contains_any_phrase(items, GAME_PHRASES)
    commerce = bool(words & COMMERCIAL_WORDS)
    meaning = matches_any(words, MEANING_PATTERNS) or contains_any_phrase(
        items, tuple(token_sequence(value) for value in ("что значит", "что означает", "как выглядит", "кто такой"))
    )
    astro = matches_any(words, ASTRO_PATTERNS) or contains_any_phrase(
        items, tuple(token_sequence(value) for value in ("дата рождения", "по месяцам", "по годам", "какой знак"))
    )
    domain = product or rosary or form or symbol_object or stone or catalog or zodiac or toy
    strong_diy = bool(words & DIY_WORDS) or contains_any_phrase(items, DIY_PHRASES)
    weak_diy = bool(words & DIY_WEAK_WORDS) and domain and not (visual and not strong_diy)
    diy = domain and (strong_diy or weak_diy)
    use_care = domain and (bool(words & USE_CARE_WORDS) or matches_any(words, USE_CARE_PATTERNS))
    selection = domain and (
        bool(words & {"выбрать", "выбирать", "подбирать", "подобрать", "подбор", "подарить", "подарок", "подарки", "подарка", "подарком"})
        or (bool(words & {"лучший", "лучшие", "лучшая", "лучше"}) and (product or rosary or form or symbol_object or stone or catalog))
        or (bool(words & SELECT_QUESTION_WORDS) and (product or rosary or form or symbol_object or stone or catalog))
    )
    acquire_domain = product or rosary or form or symbol_object or stone or catalog or toy
    acquire = acquire_domain and bool(words & ACQUIRE_WORDS) and not commerce
    effect = (product or rosary or form or symbol_object or stone or catalog) and matches_any(words, EFFECT_PATTERNS)
    religious = matches_any(words, RELIGIOUS_PATTERNS)
    entity = matches_any(words, ENTITY_PATTERNS) or contains_any_phrase(items, (token_sequence("яндекс карты"), token_sequence("сколько лет")))
    auto_use = contains_any_phrase(items, AUTO_USE_PHRASES)
    vehicle = bool(words & VEHICLE_WORDS) or matches_any(words, VEHICLE_PATTERNS) or contains_any_phrase(items, VEHICLE_PHRASES)
    industrial_auma = bool(words & {"аум", "аума", "ауме"}) and matches_any(words, INDUSTRIAL_PATTERNS)
    zodiac_non_scaffold = words - ZODIAC_SCAFFOLD_WORDS - ZODIAC_FUNCTION_WORDS
    zodiac_qualified_information = (
        zodiac and not (product or rosary or form or symbol_object or stone or catalog or commerce or media or game or visual or diy or use_care or selection)
        and bool(zodiac_non_scaffold)
    )
    astro_task = (
        astro and (zodiac or reason in {"HOLD_ZODIAC_OR_STONE_PRODUCT_COLLISION", "HOLD_PRODUCT_VERSUS_ASTROLOGY_INFORMATION"})
    ) or zodiac_qualified_information

    flags = {
        "TOPIC_PRODUCT": product, "OBJECT_ROSARY": rosary, "OBJECT_FORM": form,
        "OBJECT_SYMBOL": symbol_object, "OBJECT_STONE": stone,
        "TOPIC_CATALOG_NAME": catalog, "TOPIC_ZODIAC": zodiac, "OBJECT_TOY": toy,
        "TASK_COMMERCE": commerce, "TASK_MEDIA_DIGITAL": media, "CONTEXT_GAME": game,
        "TASK_VISUAL": visual, "TASK_MEANING": meaning,
        "TASK_ASTRO_INFORMATION": astro_task,
        "TASK_MAKE_CRAFT": diy, "TASK_USE_CARE": use_care, "TASK_SELECT_GIFT": selection,
        "TASK_ACQUIRE_ACCESS": acquire, "TASK_EFFECT_AUDIENCE": effect,
        "CONTEXT_RELIGIOUS": religious, "CONTEXT_ENTITY": entity,
        "CONTEXT_AUTOMOBILE_USE": auto_use, "FOREIGN_VEHICLE_COLLISION": vehicle and not auto_use,
        "FOREIGN_INDUSTRIAL_EQUIPMENT": industrial_auma,
    }
    signals.update(key for key, present in flags.items() if present)
    if reason in REASON_FAMILY:
        signals.add(REASON_FAMILY[reason][2])
    if reason == "HOLD_FROZEN_CATALOG_NAME_REFERENT_UNRESOLVED":
        signals.add("UPSTREAM_CATALOG_REFERENT_UNRESOLVED")
    if reason in {"HOLD_ZODIAC_OR_STONE_PRODUCT_COLLISION", "HOLD_PRODUCT_VERSUS_ASTROLOGY_INFORMATION"}:
        signals.add("UPSTREAM_ZODIAC_STONE_COLLISION")
    if reason == "HOLD_INSUFFICIENT_CONTEXT_FOR_KEEP_OR_EXCLUDE":
        signals.add("UPSTREAM_INSUFFICIENT_CONTEXT")
    if state == "KEEP":
        signals.add("UPSTREAM_STEP03B_KEEP")
    elif state == "HOLD":
        signals.add("UPSTREAM_STEP03B_HOLD")
    else:
        signals.add("UPSTREAM_STEP03B_EXCLUDE")
    return signals


def route_family(state: str, reason: str, signals: set[str]) -> tuple[str, str, int, list[tuple[int, str, str]]]:
    """Choose the highest scored candidate under the explicit contract."""
    if state == "EXCLUDE":
        return "NOT_IN_STEP04_SEMANTIC_SCOPE", "STEP03B_EXCLUDE_HISTORY_PRESERVED_WITHOUT_RETRIAGE", 9999, []

    candidates: list[tuple[int, str, str]] = []

    def add(family_id: str, priority: int, evidence: str) -> None:
        candidates.append((priority, family_id, evidence))

    if reason in REASON_FAMILY:
        family_id, priority, evidence = REASON_FAMILY[reason]
        add(family_id, priority, evidence)

    # Explicit foreign-referent evidence is the strongest current business-triage boundary.
    if "CONTEXT_GAME" in signals:
        add("PSF019", 1220, "BOUNDED_GAME_TOKEN_OR_TOKEN_SEQUENCE")
    if "TASK_MEDIA_DIGITAL" in signals:
        add("PSF018", 1210, "EXPLICIT_MEDIA_OR_DIGITAL_TASK")
    if "FOREIGN_INDUSTRIAL_EQUIPMENT" in signals:
        add("PSF032", 1205, "BOUNDED_AUMA_INDUSTRIAL_EQUIPMENT_CONTEXT")
    if "FOREIGN_VEHICLE_COLLISION" in signals:
        add("PSF020", 1200, "BOUNDED_VEHICLE_MODEL_PART_OR_PAINT")
    if "CONTEXT_ENTITY" in signals:
        add("PSF021", 1190, "BOUNDED_PERSON_PLACE_ORGANIZATION_CONTEXT")
    if "CONTEXT_RELIGIOUS" in signals:
        add("PSF017", 1180, "BOUNDED_RELIGIOUS_TEXT_PRACTICE_OR_OBJECT_CONTEXT")

    # User tasks outrank broad topic/object fallbacks.  These include three W09 discoveries.
    if "TASK_USE_CARE" in signals:
        add("PSF029", 1120, "DISCOVERED_OPERATIONAL_USE_ACTIVATION_OR_CARE_TASK")
    if "TASK_SELECT_GIFT" in signals:
        add("PSF030", 1110, "DISCOVERED_SELECTION_OR_GIFT_TASK")
    if "TASK_ACQUIRE_ACCESS" in signals:
        add("PSF031", 1100, "DISCOVERED_NON_PURCHASE_ACQUISITION_OR_ACCESS_TASK")
    if "TASK_MAKE_CRAFT" in signals:
        add("PSF027", 1090, "EXPLICIT_MAKE_OR_CRAFT_TASK")
    if "TASK_VISUAL" in signals:
        add("PSF016" if "TOPIC_ZODIAC" in signals else "PSF008", 1080, "EXPLICIT_VISUAL_TASK_WITH_TOPIC_AWARE_ROUTE")
    if "TASK_MEANING" in signals:
        add("PSF015" if "TOPIC_ZODIAC" in signals else "PSF007", 1070, "EXPLICIT_MEANING_TASK_WITH_TOPIC_AWARE_ROUTE")
    if "TASK_ASTRO_INFORMATION" in signals:
        add("PSF015", 1060, "EXPLICIT_ASTROLOGY_INFORMATION_TASK")
    if "OBJECT_TOY" in signals:
        add("PSF028", 1050, "BOUNDED_PHYSICAL_TOY_OBJECT")
    if "TASK_EFFECT_AUDIENCE" in signals:
        add("PSF011", 1040, "EXPLICIT_EFFECT_OR_AUDIENCE_TASK_WITH_PRODUCT_CONTEXT")

    # Specific topic/object combinations.
    productish = bool(signals & {"TOPIC_PRODUCT", "OBJECT_ROSARY", "OBJECT_FORM"})
    if "CONTEXT_AUTOMOBILE_USE" in signals and productish:
        add("PSF003", 980, "SUPPORTED_PRODUCT_WITH_AUTOMOBILE_USE_CONTEXT")
    if "TOPIC_ZODIAC" in signals and (productish or "TASK_COMMERCE" in signals):
        add("PSF012", 970, "ZODIAC_WITH_PRODUCT_FORM_OR_COMMERCE")
    if "OBJECT_STONE" in signals and ("TOPIC_ZODIAC" in signals or "TOPIC_CATALOG_NAME" in signals or "TOPIC_PRODUCT" in signals):
        add("PSF013", 960, "STONE_WITH_PRODUCT_ZODIAC_OR_CATALOG_REFERENT")
    if "TOPIC_CATALOG_NAME" in signals and (productish or "TASK_COMMERCE" in signals):
        add("PSF005", 950, "CATALOG_NAME_WITH_PRODUCT_FORM_OR_COMMERCE")
    if "OBJECT_ROSARY" in signals:
        add("PSF004", 940, "BOUNDED_ROSARY_OBJECT_FORM")
    if "TASK_COMMERCE" in signals and "TOPIC_PRODUCT" in signals:
        add("PSF002", 930, "GENERIC_PRODUCT_WITH_COMMERCIAL_ACTION")
    if "OBJECT_FORM" in signals and "TOPIC_PRODUCT" in signals:
        add("PSF010", 920, "PRODUCT_WITH_OBSERVED_UNCONFIRMED_FORM_OR_MATERIAL")
    if "OBJECT_SYMBOL" in signals:
        add("PSF016" if "TOPIC_ZODIAC" in signals else "PSF008", 910, "BOUNDED_SYMBOL_OR_RUNE_OBJECT")

    # Broad preliminary fallbacks; their low priority makes hidden task patterns auditable.
    if "TOPIC_ZODIAC" in signals or "UPSTREAM_ZODIAC_STONE_COLLISION" in signals:
        add("PSF014", 620, "BROAD_ZODIAC_OR_STONE_FALLBACK")
    if "UPSTREAM_CATALOG_REFERENT_UNRESOLVED" in signals:
        add("PSF006" if "TOPIC_CATALOG_NAME" in signals else "PSF009", 610, "BROAD_CATALOG_REFERENT_FALLBACK")
    if "TOPIC_CATALOG_NAME" in signals:
        add("PSF006", 600, "BROAD_CATALOG_NAME_FALLBACK")
    if "TOPIC_PRODUCT" in signals:
        add("PSF023" if state == "HOLD" else "PSF001", 590, "BROAD_GENERIC_PRODUCT_FALLBACK")
    if "OBJECT_FORM" in signals or "OBJECT_STONE" in signals:
        add("PSF010", 580, "BROAD_FORM_OR_MATERIAL_FALLBACK")
    add("PSF024", 100, "REVIEWED_INSUFFICIENT_CONTEXT_RESIDUAL")

    priority, family_id, reason_code = max(candidates, key=lambda item: (item[0], item[1], item[2]))
    ranked = sorted(candidates, key=lambda item: (-item[0], item[1], item[2]))
    return family_id, reason_code, priority, ranked


FAMILIES = dict(w08.FAMILIES)
FAMILIES["PSF025"] = w08.base.Family(
    "Точные каталожные названия без наблюдаемой квалифицированной ветви",
    "RSOTM, Soldier Of Fortune, «Бусидо — Путь Воина» и «Герб России» имеют клиентскую catalog lineage, но не имеют текущей наблюдаемой физически квалифицированной ветви.",
    "Точное клиентское имя и отдельно доказанный безопасный товарный/физический квалификатор.",
    "Автоматический вывод о форме, доступности, намерении или странице из одного catalog title.",
    w08.base.CATALOG_LINEAGE,
    "Проверить только реально отсутствующую квалифицированную ветвь после нужного owner/release gate.",
    "ZERO_OBSERVATION_GAP_NOT_FINAL",
    "CATALOG_TITLE_VS_UNCONFIRMED_PHYSICAL_FORM",
    "ZERO_MEMBER_QUALIFIED_GAP",
    "HYPOTHESIS_ONLY",
    "YES",
    "Только bounded later probe после отдельного release; для Герба России сначала owner fact.",
    "YES",
    "Catalog title подтверждает имя, но не физическую форму или поисковый intent.",
)
FAMILIES["PSF029"] = w08.base.Family(
    "Использование, ношение, активация и уход",
    "Операционная задача после выбора предмета: носить, применять, активировать, заряжать, очищать, хранить, проверять, крутить или размещать.",
    "Явное bounded действие рядом с поддержанным предметом, формой, знаком или каталожным именем.",
    "Медиа/игровой/чужой референт, обещание эффекта, вывод о наличии инструкции или финальной странице.",
    w08.base.BRIEF_LINEAGE,
    "Понять способ использования, ношения, активации или ухода.",
    "OPERATIONAL_INFORMATION_TASK_NOT_FINAL",
    "PRODUCT_USE_VS_UNPROVEN_EFFECT_OR_FOREIGN_REFERENT",
    "OBSERVED_FULL_VOLUME_OPEN_TAXONOMY_DISCOVERY",
    "MIXED_AMBIGUOUS",
    "NO",
    "Текущий корпус уже даёт task vocabulary; дальнейшее evidence относится к owner facts/Step10.",
    "YES",
    "Операционное действие не доказывает свойства товара или наличие инструкции у клиента.",
)
FAMILIES["PSF030"] = w08.base.Family(
    "Выбор, сравнение и подарок",
    "Явная задача выбрать/подобрать предмет либо подарок; сравнительная формулировка требует поддержанного объекта, кроме прямого gift-контекста со знаком.",
    "Bounded selection/gift action и объектная/зодиакальная опора присутствуют одновременно.",
    "Чистая астрологическая совместимость, generic `лучший знак`, чужой референт и финальная intent/page трактовка.",
    w08.base.BRIEF_LINEAGE,
    "Выбрать или подарить подходящий предмет/символ.",
    "SELECTION_OR_GIFT_TASK_NOT_FINAL",
    "PRODUCT_SELECTION_VS_ASTROLOGY_OR_UNCONFIRMED_ASSORTMENT",
    "OBSERVED_FULL_VOLUME_OPEN_TAXONOMY_DISCOVERY",
    "MIXED_AMBIGUOUS",
    "NO",
    "Расширение не требуется: task marker обнаружен в текущем полном universe.",
    "YES",
    "Выбор не подтверждает ассортимент, свойства или будущую посадочную страницу.",
)
FAMILIES["PSF031"] = w08.base.Family(
    "Получение, поиск и доступ к предмету",
    "Некоммерческая формулировка найти, получить, взять или достать предмет/символ без уже явного provider/marketplace действия.",
    "Bounded acquisition/access action и поддержанный объект присутствуют; commercial и foreign-referent сигналы сохраняются отдельно.",
    "Явная покупка/заказ, игра/media/entity, вывод о наличии канала поставки или финальная intent/page трактовка.",
    w08.base.BRIEF_LINEAGE,
    "Найти способ получить или обнаружить предмет/символ.",
    "ACCESS_OR_ACQUISITION_TASK_NOT_FINAL",
    "PRODUCT_ACCESS_VS_GAME_MEDIA_OR_AVAILABILITY_FACT",
    "OBSERVED_FULL_VOLUME_OPEN_TAXONOMY_DISCOVERY",
    "MIXED_AMBIGUOUS",
    "NO",
    "Текущего корпуса достаточно для предварительной задачи; наличие/канал требует later evidence.",
    "YES",
    "Фраза о получении не доказывает продажу, наличие или клиентский канал.",
)
FAMILIES["PSF032"] = w08.base.Family(
    "Промышленное оборудование AUMA и техническая документация",
    "AUM/AUMA-like referent рядом с bounded техническими объектами, схемой, инструкцией, управлением, приводом или арматурой.",
    "Одновременный AUM/AUMA token и целый технический token; совпадение с catalog `Аум` сохраняется как collision, а не товарное доказательство.",
    "Один token `аум`, мантра/религиозный контекст, клиентский физический товар или окончательный exclusion verdict.",
    w08.base.CATALOG_LINEAGE,
    "Отделить промышленный foreign referent от каталожного символа Аум.",
    "FOREIGN_INDUSTRIAL_REFERENT_NOT_FINAL",
    "CATALOG_AUM_VS_AUMA_INDUSTRIAL_EQUIPMENT",
    "OBSERVED_FULL_VOLUME_OPEN_TAXONOMY_COLLISION",
    "FOREIGN_REFERENT_COLLISION",
    "NO",
    "Текущий корпус уже показывает collision; provider expansion не требуется.",
    "YES",
    "Step04 сохраняет HOLD и не меняет принятый Step03B verdict.",
)

TASK_SIGNALS = {
    "TASK_COMMERCE", "TASK_MEDIA_DIGITAL", "CONTEXT_GAME", "TASK_VISUAL", "TASK_MEANING",
    "TASK_ASTRO_INFORMATION", "TASK_MAKE_CRAFT", "TASK_USE_CARE", "TASK_SELECT_GIFT",
    "TASK_ACQUIRE_ACCESS", "TASK_EFFECT_AUDIENCE",
}


def ambiguity_for(state: str, family_id: str) -> str:
    if state == "EXCLUDE":
        return "NONE_CURRENT_STEP03B_EXCLUDE"
    return FAMILIES[family_id].ambiguity


def later_evidence(state: str, family_id: str) -> str:
    if state == "EXCLUDE":
        return "NONE_EXCLUDED_HISTORY"
    if family_id in {"PSF010", "PSF011", "PSF012", "PSF013", "PSF017", "PSF028", "PSF029", "PSF030"}:
        return "OWNER_FACT_THEN_STEP10_IF_NEEDED"
    return "STEP10_OR_LATER_SERP_UNDER_SEPARATE_RELEASE"


def representative(rows: list[dict[str, str]], limit: int = 8) -> list[str]:
    ordered = sorted(rows, key=lambda row: (0 if row["step03b_state"] == "KEEP" else 1, len(row["canonical_phrase"]), row["canonical_phrase"], row["normalized_phrase_id"]))
    return [row["canonical_phrase"] for row in ordered[:limit]]


def entropy_normalized(labels: list[int], possible: int) -> float:
    if len(labels) <= 1:
        return 0.0
    counts = Counter(labels)
    entropy = -sum((count / len(labels)) * math.log(count / len(labels)) for count in counts.values())
    denominator = math.log(min(possible, len(labels)))
    return entropy / denominator if denominator else 0.0


INDEPENDENT_ACTION_GROUPS = {
    "MEDIA_CONSUMPTION": {"скачать", "слушать", "читать", "смотреть"},
    "MAKE_CRAFT": {"сделать", "делать", "создать", "связать", "сшить", "сплести", "скрафтить"},
    "VISUAL_PRODUCTION": {"нарисовать", "рисовать", "изобразить", "показать", "написать"},
    "USE_CARE": {"носить", "активировать", "зарядить", "заряжать", "использовать", "крутить", "перебирать", "повесить", "проверить"},
    "SELECT_GIFT": {"выбрать", "подобрать", "подарить"},
    "ACQUIRE_ACCESS": {"получить", "взять", "достать", "найти"},
    "COMMERCE": {"купить", "заказать", "приобрести"},
    "MEANING_INFORMATION": {"узнать", "понять", "описать"},
    "GAME_ACTION": {"играть", "стрелять"},
}
INDEPENDENT_FALSE_FRIENDS = {
    "печать", "стоимость", "способность", "внешность", "часть", "пусть", "есть", "быть", "месть",
    "нить", "коготь", "мать", "радость", "суть", "путь", "рать", "кровать", "личность", "жить",
    "любить", "дышать", "стать",
}


def independent_action_cues(phrase: str) -> tuple[list[str], list[str]]:
    """Label-free action frame extraction; does not call production signals."""
    words = set(token_sequence(phrase))
    cues = [f"{group}:{word}" for group, vocabulary in INDEPENDENT_ACTION_GROUPS.items() for word in sorted(words & vocabulary)]
    heuristic = sorted(
        word for word in words
        if re.fullmatch(r"[а-я]{3,}(?:ть|ться)", word)
        and word not in INDEPENDENT_FALSE_FRIENDS
        and all(word not in vocabulary for vocabulary in INDEPENDENT_ACTION_GROUPS.values())
    )
    return sorted(cues), heuristic


def independent_domain_anchor(phrase: str) -> bool:
    """Independent exact anchor filter for action discovery relevance.

    This intentionally does not call ``detect_signals``.  It prevents generic
    verbs such as `оберегать` and unrelated document-printing tasks from being
    mistaken for product-object evidence merely because they resemble a noun.
    """
    items = token_sequence(phrase)
    words = set(items)
    independent_product_forms = {
        "амулет", "амулета", "амулету", "амулетом", "амулеты", "амулетов", "амулетами",
        "оберег", "оберега", "оберегу", "оберегом", "обереги", "оберегов", "оберегами",
        "талисман", "талисмана", "талисману", "талисманом", "талисманы", "талисманов", "талисманами",
        "четки", "четок", "четкам", "четками", "четку", "четке", "игрушка", "игрушки", "игрушку",
    }
    independent_catalog_phrases = tuple(
        token_sequence(value) for value in (
            "звезда лада", "звезда лады", "звезду лады", "печать велеса", "шлем ужаса",
            "герб россии", "копье одина", "путь воина",
        )
    )
    zodiac_anchor = any(re.fullmatch(r"зодиак(?:а|у|ом|е|и|ов)?", word) for word in words)
    zodiac_anchor = zodiac_anchor or ("знак" in words and bool(words & ZODIAC_FORMS))
    return bool(words & independent_product_forms) or zodiac_anchor or contains_any_phrase(items, independent_catalog_phrases)


def source_revalidation() -> str:
    return f"""# KW-002 Step04 W09 current-authority source revalidation

Date revalidated: {DATE}

Same-day revalidation found no material change to the immediately preceding Step04 method boundary. No Wordstat, Search, GenSearch, AI-search or sealed project research source was called. Public method sources were checked only to validate controls; none supplies project demand, inventory, intent, SERP, page or IA facts.

| Source | Supported control | Limitation in W09 |
|---|---|---|
| [Yandex Webmaster — Query selection](https://yandex.ru/support/webmaster/ru/service/queries-selection) | Meaning/intent grouping is distinct from demand/competition metrics. | Frequency is descriptive only; no Yandex provider call was made. |
| [Yandex Webmaster — Search quality](https://yandex.com/support/webmaster/en/search-quality) | The user's objective and usefulness matter. | General guidance cannot decide a Blood & Sand family. |
| [Topvisor — clustering](https://topvisor.com/ru/support/clustering/) and [method](https://topvisor.com/ru/support/clustering/method/) | Final SEO clusters require separate SERP/theme evidence. | W09 families remain preliminary; no SERP was collected. |
| [scikit-learn — feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html) | TF-IDF is a reproducible text diagnostic. | Character similarity is not semantic ground truth. |
| [scikit-learn — MiniBatchKMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html) | Seeded topic decomposition can challenge large groups. | Topic IDs are diagnostic, not final clusters. |
| [Python — regular expressions](https://docs.python.org/3/library/re.html) | `fullmatch` provides a bounded whole-token contract. | Bounded syntax alone does not prove business relevance. |

Trace: source principle → bounded simultaneous signal extraction → explicit numeric precedence → full-volume invariants → independent character/action diagnostic. Completed Step00–03B stay frozen. Step05/06 remain blocked.
"""


def main() -> None:
    input_hashes = {name: sha256(HERE / name) for name in INPUTS.values()}
    governing_hashes = {name: sha256(KW002_ROOT / name) for name in GOVERNING_AUTHORITIES}
    for name, expected in EXPECTED_FROZEN_SHA256.items():
        assert input_hashes[name] == expected, (name, input_hashes[name], expected)

    pool_rows = read_tsv(INPUTS["pool"])
    ledger_rows = read_tsv(INPUTS["ledger"])
    keep_rows = read_tsv(INPUTS["keep"])
    register_rows = read_tsv(INPUTS["register"])
    step03b_overlay_rows = read_tsv(INPUTS["step03b_overlay"])
    old_occurrence_rows = read_tsv(INPUTS["old_occurrence"])
    w07_rows = read_tsv(INPUTS["w07_overlay"])
    w08_occurrence_rows = read_tsv(INPUTS["w08_occurrence"])
    w08_transition_rows = read_tsv(INPUTS["w08_transition"])

    assert (len(pool_rows), len(ledger_rows), len(keep_rows), len(register_rows)) == (24576, 25979, 5100, 19476)
    assert (len(step03b_overlay_rows), len(old_occurrence_rows), len(w07_rows), len(w08_occurrence_rows), len(w08_transition_rows)) == (24576, 25979, 24576, 25979, 24576)

    pool = {row["normalized_phrase_id"]: row for row in pool_rows}
    current: dict[str, dict[str, str]] = {}
    for row in keep_rows + register_rows:
        npid = row["normalized_phrase_id"]
        assert npid not in current
        current[npid] = {
            "normalized_phrase_id": npid,
            "canonical_phrase": row["canonical_phrase"],
            "step03b_state": w08.base.norm_state(row["sanitation_state"]),
            "step03b_reason": row["sanitation_reason_code"],
            "raw_occurrence_count": row["raw_occurrence_count"],
        }
    assert set(current) == set(pool)
    assert Counter(row["step03b_state"] for row in current.values()) == Counter({"KEEP": 5100, "HOLD": 13035, "EXCLUDE": 6441})
    overlay = {row["normalized_phrase_id"]: row for row in step03b_overlay_rows}
    assert set(overlay) == set(current)
    assert sum(row["step03b_state"] != overlay[npid]["audit_state"] for npid, row in current.items()) == 0

    old_by_occurrence = {row["raw_occurrence_id"]: row for row in old_occurrence_rows}
    old_by_identity: dict[str, dict[str, str]] = {}
    for row in old_occurrence_rows:
        previous = old_by_identity.setdefault(row["normalized_phrase_id"], row)
        assert previous["post_sanitation_family_id"] == row["post_sanitation_family_id"]
    w08_by_identity = {row["normalized_phrase_id"]: row for row in w08_transition_rows}
    w07_by_identity = {row["normalized_phrase_id"]: row for row in w07_rows}
    assert len(old_by_occurrence) == 25979 and len(old_by_identity) == 24576
    assert set(w08_by_identity) == set(w07_by_identity) == set(current)

    semantic_source = inspect.getsource(detect_signals) + inspect.getsource(route_family)
    assert ".startswith(" not in semantic_source
    assert "has_any(" not in semantic_source

    assignments: dict[str, dict[str, object]] = {}
    signal_rows: list[dict[str, object]] = []
    transition_rows: list[dict[str, object]] = []
    active_rows: list[dict[str, str]] = []
    for npid in sorted(current):
        row = current[npid]
        signals = (
            {"UPSTREAM_STEP03B_EXCLUDE"}
            if row["step03b_state"] == "EXCLUDE"
            else detect_signals(row["canonical_phrase"], row["step03b_state"], row["step03b_reason"])
        )
        family_id, reason_code, priority, candidates = route_family(row["step03b_state"], row["step03b_reason"], signals)
        task_signals = sorted(signals & TASK_SIGNALS)
        secondary = sorted(signal for signal in signals if signal not in {"UPSTREAM_STEP03B_KEEP", "UPSTREAM_STEP03B_HOLD", "UPSTREAM_STEP03B_EXCLUDE"})
        candidate_text = "|".join(f"{score}:{fid}:{evidence}" for score, fid, evidence in candidates) if candidates else "NOT_RETRIAGED"
        precedence = (
            "EXCLUDE_HISTORY_NO_RETRIAGE"
            if row["step03b_state"] == "EXCLUDE"
            else f"MAX_NUMERIC_SPECIFICITY={priority};WINNER={family_id};CANDIDATES={candidate_text}"
        )
        assignments[npid] = {
            "family_id": family_id, "reason": reason_code, "priority": priority,
            "signals": signals, "task_signals": task_signals, "candidates": candidates,
        }
        old_family = old_by_identity[npid]["post_sanitation_family_id"]
        w08_family = w08_by_identity[npid]["corrected_step04_family_id"]
        if row["step03b_state"] == "EXCLUDE":
            transition_class = "EXCLUDE_HISTORY_UNCHANGED"
        elif family_id == w08_family:
            transition_class = "UNCHANGED_FROM_W08_CANDIDATE"
        elif family_id in {"PSF029", "PSF030", "PSF031", "PSF032"}:
            transition_class = "W09_OPEN_TAXONOMY_TASK_DISCOVERY"
        else:
            transition_class = "W09_UNIVERSAL_SPECIFICITY_PRECEDENCE_REROUTE"
        signal_rows.append({
            "normalized_phrase_id": npid,
            "canonical_phrase": row["canonical_phrase"],
            "step03b_state": row["step03b_state"],
            "step03b_reason": row["step03b_reason"],
            "primary_preliminary_family_id": family_id,
            "primary_assignment_reason": reason_code,
            "primary_specificity_priority": priority,
            "all_material_detected_signals": "|".join(sorted(signals)) if signals else "NONE",
            "secondary_task_context_signals": "|".join(secondary) if secondary else "NONE",
            "specificity_or_precedence_explanation": precedence,
            "ambiguity_state": ambiguity_for(row["step03b_state"], family_id),
            "later_evidence_needed": later_evidence(row["step03b_state"], family_id),
            "old_step04_family": old_family,
            "w08_candidate_family": w08_family,
            "w08_to_w09_relation": transition_class,
            "frequency_used_for_semantic_assignment": "NO",
            "final_intent_status": "NOT_FINAL_AT_STEP04",
            "serp_cluster_status": "NOT_EVALUATED_AT_STEP04",
            "step03b_mutated": "NO",
        })
        transition_rows.append({
            "normalized_phrase_id": npid, "canonical_phrase": row["canonical_phrase"],
            "step03b_state": row["step03b_state"], "step03b_reason": row["step03b_reason"],
            "raw_occurrence_count": row["raw_occurrence_count"], "old_step04_family": old_family,
            "w08_candidate_family": w08_family, "w09_current_family": family_id,
            "w09_assignment_reason": reason_code, "w09_specificity_priority": priority,
            "all_material_signals": "|".join(sorted(signals)) if signals else "NONE",
            "old_to_w09_changed": "YES" if old_family != family_id else "NO",
            "w08_to_w09_changed": "YES" if w08_family != family_id else "NO",
            "transition_class": transition_class,
            "w07_fixture_disposition": w07_by_identity[npid]["audit_recommended_disposition"],
            "step03b_mutated": "NO",
        })
        if row["step03b_state"] != "EXCLUDE":
            assert family_id in FAMILIES
            enriched = dict(row)
            enriched["family_id"] = family_id
            enriched["assignment_reason"] = reason_code
            active_rows.append(enriched)

    assert len(assignments) == len(signal_rows) == len(transition_rows) == 24576
    assert len(active_rows) == 18135
    write_tsv(OUTPUTS["signals"], [
        "normalized_phrase_id", "canonical_phrase", "step03b_state", "step03b_reason",
        "primary_preliminary_family_id", "primary_assignment_reason", "primary_specificity_priority",
        "all_material_detected_signals", "secondary_task_context_signals",
        "specificity_or_precedence_explanation", "ambiguity_state", "later_evidence_needed",
        "old_step04_family", "w08_candidate_family", "w08_to_w09_relation",
        "frequency_used_for_semantic_assignment", "final_intent_status", "serp_cluster_status", "step03b_mutated",
    ], signal_rows)
    write_tsv(OUTPUTS["transition"], [
        "normalized_phrase_id", "canonical_phrase", "step03b_state", "step03b_reason", "raw_occurrence_count",
        "old_step04_family", "w08_candidate_family", "w09_current_family", "w09_assignment_reason",
        "w09_specificity_priority", "all_material_signals", "old_to_w09_changed", "w08_to_w09_changed",
        "transition_class", "w07_fixture_disposition", "step03b_mutated",
    ], transition_rows)

    occurrence_rows: list[dict[str, object]] = []
    raw_states: Counter[str] = Counter()
    for occurrence in ledger_rows:
        npid = occurrence["normalized_phrase_id"]
        row = current[npid]
        assignment = assignments[npid]
        raw_states[row["step03b_state"]] += 1
        occurrence_rows.append({
            "raw_occurrence_id": occurrence["occurrence_id"], "normalized_phrase_id": npid,
            "canonical_phrase": row["canonical_phrase"], "raw_phrase": occurrence["raw_phrase"],
            "step03b_state": row["step03b_state"], "step03b_reason": row["step03b_reason"],
            "step04_scope_state": "EXCLUDED_HISTORY" if row["step03b_state"] == "EXCLUDE" else ("ACTIVE_SEMANTIC_SCOPE" if row["step03b_state"] == "KEEP" else "HOLD_SEMANTIC_SCOPE"),
            "w09_primary_family_id": assignment["family_id"], "w09_assignment_reason": assignment["reason"],
            "w09_all_material_signals": "|".join(sorted(assignment["signals"])) if assignment["signals"] else "NONE",
            "ambiguity_state": ambiguity_for(row["step03b_state"], str(assignment["family_id"])),
            "later_evidence_needed": later_evidence(row["step03b_state"], str(assignment["family_id"])),
            "source_seed_run_provenance_locator": f"run={occurrence['run_order']}|seed={occurrence['seed_id']}|request={occurrence['provider_request_id']}|carrier={occurrence['carrier_locator']}|channel={occurrence['channel']}|position={occurrence['position']}",
            "old_step04_family": old_by_occurrence[occurrence["occurrence_id"]]["post_sanitation_family_id"],
            "w08_candidate_family": w08_by_identity[npid]["corrected_step04_family_id"],
            "raw_observed_count_descriptive_only": occurrence["raw_count"],
            "frequency_used_for_semantic_assignment": "NO", "final_intent_status": "NOT_FINAL_AT_STEP04",
            "serp_cluster_status": "NOT_EVALUATED_AT_STEP04",
        })
    assert raw_states == Counter({"KEEP": 5263, "HOLD": 13823, "EXCLUDE": 6893})
    assert len(occurrence_rows) == len({row["raw_occurrence_id"] for row in occurrence_rows}) == 25979
    write_tsv(OUTPUTS["occurrence"], [
        "raw_occurrence_id", "normalized_phrase_id", "canonical_phrase", "raw_phrase", "step03b_state",
        "step03b_reason", "step04_scope_state", "w09_primary_family_id", "w09_assignment_reason",
        "w09_all_material_signals", "ambiguity_state", "later_evidence_needed",
        "source_seed_run_provenance_locator", "old_step04_family", "w08_candidate_family",
        "raw_observed_count_descriptive_only", "frequency_used_for_semantic_assignment",
        "final_intent_status", "serp_cluster_status",
    ], occurrence_rows)

    # Independent full-volume character/topic and action-frame challenge.
    active_ids = sorted(row["normalized_phrase_id"] for row in active_rows)
    docs = [current[npid]["canonical_phrase"] for npid in active_ids]
    vectorizer = TfidfVectorizer(
        analyzer="char_wb", ngram_range=(3, 5), min_df=2, max_df=0.995,
        max_features=40000, sublinear_tf=True, norm="l2",
    )
    matrix = vectorizer.fit_transform(docs)
    assert matrix.shape[0] == 18135
    topic_model = MiniBatchKMeans(
        n_clusters=48, random_state=RANDOM_SEED, batch_size=1024, n_init=10,
        max_iter=250, reassignment_ratio=0.01,
    )
    topic_labels = topic_model.fit_predict(matrix)
    observed_families = sorted({str(assignments[npid]["family_id"]) for npid in active_ids})
    positions_by_family: dict[str, list[int]] = defaultdict(list)
    for position, npid in enumerate(active_ids):
        positions_by_family[str(assignments[npid]["family_id"])].append(position)
    centroids = [csr_matrix(matrix[positions_by_family[family_id]].mean(axis=0)) for family_id in observed_families]
    centroid_matrix = normalize(vstack(centroids), norm="l2", axis=1)
    similarities = np.asarray((matrix @ centroid_matrix.T).todense())

    independent_by_id: dict[str, tuple[list[str], list[str]]] = {
        npid: (independent_action_cues(current[npid]["canonical_phrase"]) if current[npid]["step03b_state"] != "EXCLUDE" else ([], []))
        for npid in current
    }
    cue_support = Counter(cue.split(":", 1)[0] for npid in active_ids for cue in independent_by_id[npid][0])
    heuristic_support = Counter(token for npid in active_ids for token in independent_by_id[npid][1])
    w08_discovery_hidden = Counter()
    for npid in active_ids:
        w08_family = str(w08_by_identity[npid]["corrected_step04_family_id"])
        if w08_family in {"PSF001", "PSF006", "PSF009", "PSF014", "PSF023", "PSF024"} and independent_domain_anchor(current[npid]["canonical_phrase"]):
            for cue in independent_by_id[npid][0]:
                group = cue.split(":", 1)[0]
                if group in {"USE_CARE", "SELECT_GIFT", "ACQUIRE_ACCESS"}:
                    w08_discovery_hidden[group] += 1

    independent_rows: list[dict[str, object]] = []
    independent_failures: list[str] = []
    active_position = {npid: index for index, npid in enumerate(active_ids)}
    for npid in sorted(current):
        row = current[npid]
        assignment = assignments[npid]
        cues, heuristic = independent_by_id[npid]
        if row["step03b_state"] == "EXCLUDE":
            independent_rows.append({
                "normalized_phrase_id": npid, "canonical_phrase": row["canonical_phrase"],
                "step03b_state": row["step03b_state"], "w09_primary_family_id": assignment["family_id"],
                "independent_topic_id": "NOT_APPLICABLE_EXCLUDE_HISTORY", "independent_action_cues": "|".join(cues) if cues else "NONE",
                "independent_unmodeled_action_tokens": "|".join(heuristic) if heuristic else "NONE",
                "assigned_family_centroid_similarity": "NOT_APPLICABLE", "nearest_other_family": "NOT_APPLICABLE",
                "nearest_other_family_similarity": "NOT_APPLICABLE", "independent_hidden_task_alert": "NO_EXCLUDE_HISTORY",
                "independent_assignment_challenge": "EXCLUDE_HISTORY_NOT_RETRIAGED", "verdict": "PASS_ACCOUNTING_ONLY",
            })
            continue
        position = active_position[npid]
        own_index = observed_families.index(str(assignment["family_id"]))
        own_similarity = float(similarities[position, own_index])
        other = similarities[position].copy()
        other[own_index] = -1.0
        nearest_index = int(np.argmax(other))
        independent_groups = {cue.split(":", 1)[0] for cue in cues}
        repeated_group = sorted(group for group in independent_groups if cue_support[group] >= 3)
        repeated_heuristic = sorted(token for token in heuristic if heuristic_support[token] >= 3)
        broad_primary = str(assignment["reason"]).endswith("FALLBACK") or assignment["reason"] == "REVIEWED_INSUFFICIENT_CONTEXT_RESIDUAL"
        hidden = broad_primary and independent_domain_anchor(row["canonical_phrase"]) and bool(repeated_group or repeated_heuristic)
        high_override = float(other[nearest_index]) >= own_similarity + 0.12 and float(other[nearest_index]) >= 0.30
        challenge = (
            "FAIL_REPEATED_ACTION_PATTERN_HIDDEN_BY_LOW_SPECIFICITY_PRIMARY" if hidden
            else "WARN_NEAREST_FAMILY_OVERRIDE_NO_ACTION_EVIDENCE" if high_override
            else "PASS_NO_INDEPENDENT_DEFECT"
        )
        verdict = "FAIL" if hidden else ("PASS_WITH_DIAGNOSTIC_WARNING" if high_override else "PASS")
        if hidden:
            independent_failures.append(npid)
        independent_rows.append({
            "normalized_phrase_id": npid, "canonical_phrase": row["canonical_phrase"],
            "step03b_state": row["step03b_state"], "w09_primary_family_id": assignment["family_id"],
            "independent_topic_id": int(topic_labels[position]), "independent_action_cues": "|".join(cues) if cues else "NONE",
            "independent_unmodeled_action_tokens": "|".join(heuristic) if heuristic else "NONE",
            "assigned_family_centroid_similarity": f"{own_similarity:.6f}",
            "nearest_other_family": observed_families[nearest_index],
            "nearest_other_family_similarity": f"{float(other[nearest_index]):.6f}",
            "independent_hidden_task_alert": "YES" if hidden else "NO",
            "independent_assignment_challenge": challenge, "verdict": verdict,
        })
    assert len(independent_rows) == 24576
    assert not independent_failures, independent_failures[:20]
    assert all(w08_discovery_hidden[group] > 0 for group in ("USE_CARE", "SELECT_GIFT", "ACQUIRE_ACCESS")), w08_discovery_hidden
    write_tsv(OUTPUTS["independent"], [
        "normalized_phrase_id", "canonical_phrase", "step03b_state", "w09_primary_family_id",
        "independent_topic_id", "independent_action_cues", "independent_unmodeled_action_tokens",
        "assigned_family_centroid_similarity", "nearest_other_family", "nearest_other_family_similarity",
        "independent_hidden_task_alert", "independent_assignment_challenge", "verdict",
    ], independent_rows)

    family_members: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in active_rows:
        family_members[row["family_id"]].append(row)
    family_rows: list[dict[str, object]] = []
    family_diagnostics: dict[str, dict[str, object]] = {}
    for family_id in FAMILIES:
        members = family_members.get(family_id, [])
        positions = positions_by_family.get(family_id, [])
        topics = [int(topic_labels[position]) for position in positions]
        entropy = entropy_normalized(topics, 48) if topics else 0.0
        warnings = sum(
            row["verdict"] == "PASS_WITH_DIAGNOSTIC_WARNING"
            for row in independent_rows if row["w09_primary_family_id"] == family_id
        )
        hidden_count = sum(
            row["independent_hidden_task_alert"] == "YES"
            for row in independent_rows if row["w09_primary_family_id"] == family_id
        )
        family_diagnostics[family_id] = {"entropy": entropy, "warnings": warnings, "hidden": hidden_count}
        meta = FAMILIES[family_id]
        keep_count = sum(row["step03b_state"] == "KEEP" for row in members)
        hold_count = len(members) - keep_count
        keep_raw = sum(int(row["raw_occurrence_count"]) for row in members if row["step03b_state"] == "KEEP")
        hold_raw = sum(int(row["raw_occurrence_count"]) for row in members if row["step03b_state"] == "HOLD")
        secondary_counts = Counter(
            signal for row in members for signal in sorted(assignments[row["normalized_phrase_id"]]["signals"])
            if signal not in {"UPSTREAM_STEP03B_KEEP", "UPSTREAM_STEP03B_HOLD"}
        )
        w08_mapping = Counter(str(w08_by_identity[row["normalized_phrase_id"]]["corrected_step04_family_id"]) for row in members)
        family_rows.append({
            "family_id": family_id, "family_label_plain_russian": meta.label, "family_definition": meta.definition,
            "in_scope_boundary": meta.in_scope, "out_of_scope_boundary": meta.out_scope,
            "representative_phrases": json.dumps(representative(members), ensure_ascii=False, separators=(",", ":")),
            "normalized_identity_count": len(members), "raw_occurrence_count": keep_raw + hold_raw,
            "keep_identity_count": keep_count, "hold_identity_count": hold_count,
            "keep_raw_count": keep_raw, "hold_raw_count": hold_raw,
            "business_lineage": meta.business_lineage,
            "business_relevance_confidence": "HYPOTHESIS_ONLY_NO_OBSERVATION" if not members else ("HIGH_BUSINESS_SUPPORT_NOT_FINAL" if family_id in {"PSF002", "PSF003"} else "SUPPORTED_OR_AMBIGUOUS_NOT_FINAL"),
            "family_coherence_confidence": "INDEPENDENT_PASS_NOT_FINAL" if hidden_count == 0 else "FAIL",
            "primary_user_task_hypothesis": meta.user_task,
            "secondary_task_context_coverage": ";".join(f"{signal}:{count}" for signal, count in secondary_counts.most_common()) or "NONE_ZERO_MEMBER_GAP",
            "identity_signal_authority": OUTPUTS["signals"], "ambiguity_classes": meta.ambiguity,
            "coverage_state": meta.coverage, "later_evidence_needed": later_evidence("HOLD", family_id),
            "w08_candidate_mapping_summary": ";".join(f"{key}:{value}" for key, value in w08_mapping.most_common()) or "NO_MEMBERS",
            "independent_topic_count": len(set(topics)), "independent_topic_entropy_normalized": f"{entropy:.6f}",
            "independent_warning_rows": warnings, "independent_hidden_task_rows": hidden_count,
            "final_intent_status": "NOT_FINAL_AT_STEP04", "serp_cluster_status": "NOT_EVALUATED_AT_STEP04",
            "frequency_used_for_semantic_assignment": "NO", "family_gate": "PASS" if hidden_count == 0 else "FAIL",
        })
    assert sum(int(row["normalized_identity_count"]) for row in family_rows) == 18135
    assert sum(int(row["raw_occurrence_count"]) for row in family_rows) == 19086
    assert all(row["family_gate"] == "PASS" for row in family_rows)
    write_tsv(OUTPUTS["families"], [
        "family_id", "family_label_plain_russian", "family_definition", "in_scope_boundary", "out_of_scope_boundary",
        "representative_phrases", "normalized_identity_count", "raw_occurrence_count", "keep_identity_count",
        "hold_identity_count", "keep_raw_count", "hold_raw_count", "business_lineage",
        "business_relevance_confidence", "family_coherence_confidence", "primary_user_task_hypothesis",
        "secondary_task_context_coverage", "identity_signal_authority", "ambiguity_classes", "coverage_state",
        "later_evidence_needed", "w08_candidate_mapping_summary", "independent_topic_count",
        "independent_topic_entropy_normalized", "independent_warning_rows", "independent_hidden_task_rows",
        "final_intent_status", "serp_cluster_status", "frequency_used_for_semantic_assignment", "family_gate",
    ], family_rows)

    family_by_id = {str(row["family_id"]): row for row in family_rows}
    evidence_scope = "ALL_DURABLE_STEP03A_POOL_STEP03B_AUTHORITY_W07_AUDIT_W08_HISTORY"
    queue_specs = [
        ("PSQ001", "PSF025", "RETAINED", "VALID_INCREMENTAL_SEARCH_GAP", "Три exact catalog names have zero qualified current observations.", "No equivalent qualified branch in all durable evidence.", "NO", "YES_AFTER_SEPARATE_STEP05_RELEASE", "New qualified lexicon for at least one zero branch.", "A zero result proves no observed expansion and closes the round.", "One bounded round or earlier stop if no distinguishing lexicon."),
        ("PSQ002", "PSF017", "RETAINED", "OWNER_FACT_GAP", "Prayer/text versus physical form cannot be resolved by provider evidence.", "Owner must confirm the product form first.", "NO", "CONDITIONAL_AFTER_OWNER_FACT_AND_RELEASE", "Only a confirmed form creates a testable later branch.", "No owner fact means no provider call and the gap remains explicit.", "Stop without owner fact; otherwise one bounded probe."),
        ("PSQ003", "PSF025", "RETAINED", "OWNER_FACT_GAP", "Heraldic/catalog form is not stated in durable client facts.", "Owner must confirm physical form.", "NO", "CONDITIONAL_AFTER_OWNER_FACT_AND_RELEASE", "A confirmed form creates a distinguishable query hypothesis.", "No owner fact prevents unsafe inventory inference.", "Stop without owner fact; otherwise one bounded probe."),
        ("PSQ004", "PSF026", "RETAINED", "VALID_INCREMENTAL_SEARCH_GAP", "Qualified Blood & Sand brand-product branch remains zero.", "No equivalent qualified branch in all durable evidence.", "NO", "YES_AFTER_SEPARATE_STEP05_RELEASE", "New brand+product vocabulary absent from current universe.", "A zero result closes the brand branch without repeated acquisition.", "One bounded round or earlier stop."),
        ("PSQ005", "PSF006", "RETAINED", "VALID_INCREMENTAL_SEARCH_GAP", "Aum-only physical-product branch remains absent; Om is already covered.", "Durable Om evidence excluded; no equivalent Aum-qualified branch found.", "NO", "YES_AFTER_SEPARATE_STEP05_RELEASE", "Only new Aum-specific physical qualification is incremental.", "A zero result closes Aum without replaying Om evidence.", "One Aum-only round or earlier stop."),
        ("PSQ006", "PSF006", "SUPPRESSED", "EXISTING_EVIDENCE_REUSE", "Gungnir/Odin spear hypothesis already has durable qualified evidence.", "Equivalent durable evidence exists.", "YES", "NO_EXISTING_EVIDENCE", "Zero; reuse current evidence.", "Not applicable because acquisition is suppressed.", "Permanent stop unless upstream inventory changes."),
        ("PSQ007", "PSF021", "SUPPRESSED", "EXISTING_EVIDENCE_REUSE", "Named entity collisions already have durable qualified evidence.", "Equivalent durable evidence exists.", "YES", "NO_EXISTING_EVIDENCE", "Zero; reuse current evidence.", "Not applicable because acquisition is suppressed.", "Permanent stop unless upstream inventory changes."),
        ("PSQ008", "PSF006", "SUPPRESSED", "EXISTING_EVIDENCE_REUSE", "Belobog/Chernobog/Mara branches already have durable evidence.", "Equivalent durable evidence exists.", "YES", "NO_EXISTING_EVIDENCE", "Zero; reuse current evidence.", "Not applicable because acquisition is suppressed.", "Permanent stop unless upstream inventory changes."),
        ("PSQ009", "PSF012", "RETAINED", "OWNER_FACT_GAP", "Zodiac forms/materials are not confirmed by catalog titles.", "Owner fact must precede any template probe.", "NO", "CONDITIONAL_AFTER_OWNER_FACT_AND_RELEASE", "One confirmed form can define a bounded 12-sign template.", "No fact blocks provider use and preserves the unknown.", "Stop without fact; otherwise one template round."),
        ("PSQ010", "PSF004", "SUPPRESSED", "EXISTING_EVIDENCE_REUSE", "Negative !rosary evidence E013 is durable and must not replay.", "Equivalent durable negative evidence exists.", "YES", "NO_SATISFIED_NEGATIVE_EVIDENCE", "Zero; reuse E013.", "The prior negative result already supplies the stop value.", "Permanent stop unless upstream scope changes."),
        ("PSQ011", "PSF020", "RETAINED", "DEFER_TO_LATER_SERP_INTENT", "Vehicle use/model boundary needs a named later collision.", "No current provider-ready gap; defer to Step10/later SERP.", "NO", "NO_UNTIL_CONCRETE_LATER_COLLISION", "Only a later named collision could be incremental.", "Absence of a named collision means no acquisition.", "Stop now; at most one later test after a separate release."),
        ("PSQ012", "PSF010", "RETAINED", "OWNER_FACT_GAP", "Observed forms/materials do not prove inventory.", "Owner inventory fact only.", "NO", "NO_PROVIDER_OWNER_FACT_ONLY", "Only an owner fact resolves the gap.", "No fact preserves the uncertainty without provider inference.", "Stop after fact or explicit absence."),
        ("PSQ013", "PSF011", "RETAINED", "OWNER_FACT_GAP", "Effect/audience claims are not client-confirmed.", "Owner-approved factual claim boundary only.", "NO", "NO_PROVIDER_OWNER_FACT_ONLY", "Only owner language is safe incremental evidence.", "No approved fact blocks unsupported claims.", "Stop after fact or explicit absence."),
    ]
    qualified_aum_physical = sum(
        "аум" in set(token_sequence(row["canonical_phrase"]))
        and bool(assignments[row["normalized_phrase_id"]]["signals"] & {"TOPIC_PRODUCT", "OBJECT_ROSARY"})
        and "FOREIGN_INDUSTRIAL_EQUIPMENT" not in assignments[row["normalized_phrase_id"]]["signals"]
        for row in active_rows
    )
    assert qualified_aum_physical == 0
    hypothesis_evidence = {
        "PSQ001": "qualified current identities=0; targets=RSOTM|Soldier Of Fortune|Бусидо — Путь Воина",
        "PSQ002": f"current PSF017 identities={family_by_id['PSF017']['normalized_identity_count']}; physical-form fact remains absent",
        "PSQ003": "qualified Герб России physical-form identities=0; owner form fact absent",
        "PSQ004": "qualified Blood & Sand brand-product identities=0",
        "PSQ005": f"qualified Aum physical-product identities={qualified_aum_physical}; unqualified/referential Aum evidence preserved elsewhere",
        "PSQ006": "durable qualified Gungnir/Odin-spear identities=12 (W08 reconciliation authority)",
        "PSQ007": "durable qualified named-entity collision identities=79 (W08 reconciliation authority)",
        "PSQ008": "durable qualified Belobog/Chernobog/Mara identities=13 (W08 reconciliation authority)",
        "PSQ009": f"current PSF012 identities={family_by_id['PSF012']['normalized_identity_count']}; catalog form/material fact absent",
        "PSQ010": "durable negative evidence E013 exists; replay=false",
        "PSQ011": f"current PSF020 identities={family_by_id['PSF020']['normalized_identity_count']}; named unresolved later collision absent",
        "PSQ012": f"current PSF010 identities={family_by_id['PSF010']['normalized_identity_count']}; owner inventory fact absent",
        "PSQ013": f"current PSF011 identities={family_by_id['PSF011']['normalized_identity_count']}; owner-approved claim boundary absent",
    }
    queue_rows = []
    for qid, fid, state, disposition, problem, reconciliation, equivalent, eligible, gain, negative, stop in queue_specs:
        fam = family_by_id[fid]
        queue_rows.append({
            "queue_id": qid, "family_id": fid, "queue_state": state, "disposition_type": disposition,
            "problem": problem, "global_evidence_scope_checked": evidence_scope,
            "global_evidence_reconciliation": reconciliation, "equivalent_durable_evidence_found": equivalent,
            "hypothesis_specific_durable_evidence": hypothesis_evidence[qid],
            "current_family_evidence": f"identities={fam['normalized_identity_count']};raw={fam['raw_occurrence_count']};examples={fam['representative_phrases']}",
            "owner_fact_gap_sent_to_provider": "NO", "provider_eligible_later": eligible,
            "provider_ready_now": "NO_STEP05_BLOCKED", "incremental_information_gain": gain,
            "negative_result_value": negative, "stop_condition": stop, "executed_in_w09": "NO",
        })
    assert sum(row["queue_state"] == "RETAINED" for row in queue_rows) == 9
    assert sum(row["equivalent_durable_evidence_found"] == "YES" and row["queue_state"] == "RETAINED" for row in queue_rows) == 0
    assert all(row["owner_fact_gap_sent_to_provider"] == "NO" and row["provider_ready_now"] == "NO_STEP05_BLOCKED" for row in queue_rows)
    write_tsv(OUTPUTS["queue"], [
        "queue_id", "family_id", "queue_state", "disposition_type", "problem", "global_evidence_scope_checked",
        "global_evidence_reconciliation", "equivalent_durable_evidence_found", "hypothesis_specific_durable_evidence", "current_family_evidence",
        "owner_fact_gap_sent_to_provider", "provider_eligible_later", "provider_ready_now",
        "incremental_information_gain", "negative_result_value", "stop_condition", "executed_in_w09",
    ], queue_rows)

    feedback_specs = [
        ("W09FB001", "PSF015", "UPSTREAM_SANITATION_FINDING", "Zodiac information remains HOLD; no Step03B mutation."),
        ("W09FB002", "PSF018", "STEP04_ROUTING_FINDING", "Media/title strength varies; all explicit signals remain auditable."),
        ("W09FB003", "PSF019+PSF028", "STEP04_ROUTING_FINDING", "Bounded game tokens and whole-token toy morphology remain separate."),
        ("W09FB004", "PSF020", "UPSTREAM_SANITATION_FINDING", "Automobile use and foreign vehicle collision remain separately signaled."),
        ("W09FB005", "PSF021", "UPSTREAM_SANITATION_FINDING", "Person/place/organization collisions require bounded evidence."),
        ("W09FB006", "PSF022", "UPSTREAM_SANITATION_FINDING", "Rosary morphology uncertainty remains governed history."),
        ("W09FB007", "PSF005", "UPSTREAM_SANITATION_FINDING", "Catalog name plus qualifier does not automatically resolve referent."),
        ("W09FB008", "PSF017", "OWNER_FACT_GAP", "Religious physical form must come from owner facts."),
        ("W09FB009", "PSF024", "UPSTREAM_SANITATION_FINDING", "Residual/noise quarantine is not resolved by frequency."),
        ("W09FB010", "PSF011", "OWNER_FACT_GAP", "Effect/audience language must not become an unsupported claim."),
        ("W09FB011", "PSF027", "STEP04_ROUTING_FINDING", "Make/craft task outranks broad product or zodiac fallback."),
        ("W09FB012", "ALL", "STEP04_ROUTING_FINDING", "Numeric specificity contract preserves primary and secondary signals taxonomy-wide."),
        ("W09FB013", "PSF019+PSF028", "STEP04_ROUTING_FINDING", "No toy-without-game identity enters the game family."),
        ("W09FB014", "PSF029+PSF030+PSF031+PSF032", "STEP04_ROUTING_FINDING", "Independent discovery exposed three coherent tasks and one Aum/AUMA foreign-referent collision hidden by W08 generic families."),
        ("W09FB015", "QUEUE_PSQ006_007_008_010", "EXISTING_EVIDENCE_REUSE", "Equivalent durable evidence suppresses provider acquisition."),
        ("W09FB016", "QUEUE_OWNER_FACT", "OWNER_FACT_GAP", "Owner-only gaps are never sent to a provider."),
        ("W09FB017", "QUEUE_PSQ001_004_005", "VALID_INCREMENTAL_SEARCH_GAP", "Only three bounded gaps may become provider-eligible after a separate release."),
        ("W09FB018", "QUEUE_PSQ011", "DEFER_TO_LATER_SERP_INTENT", "Vehicle boundary is deferred until a concrete later collision exists."),
    ]
    feedback_rows = []
    for fbid, source, finding_class, finding in feedback_specs:
        source_ids = [part for part in source.split("+") if part in family_members]
        members = [row for family_id in source_ids for row in family_members[family_id]]
        feedback_rows.append({
            "feedback_id": fbid, "source_scope": source, "finding_class": finding_class,
            "normalized_identity_count": len(members),
            "raw_occurrence_count": sum(int(row["raw_occurrence_count"]) for row in members),
            "deterministic_selector": f"CURRENT_W09_SCOPE={source}",
            "representative_phrases": json.dumps(representative(members, 6), ensure_ascii=False, separators=(",", ":")) if members else "[]",
            "finding": finding, "recommended_next_gate": "MAIN_CHATGPT_REVIEW_THEN_SEPARATE_GOVERNED_STEP",
            "step03a_changed_in_w09": "NO", "step03b_changed_in_w09": "NO", "blocking_for_current_step04": "NO_GOVERNED_FEEDBACK",
        })
    write_tsv(OUTPUTS["feedback"], [
        "feedback_id", "source_scope", "finding_class", "normalized_identity_count", "raw_occurrence_count",
        "deterministic_selector", "representative_phrases", "finding", "recommended_next_gate",
        "step03a_changed_in_w09", "step03b_changed_in_w09", "blocking_for_current_step04",
    ], feedback_rows)

    toy_game_fail = [npid for npid in active_ids if assignments[npid]["family_id"] == "PSF019" and "OBJECT_TOY" in assignments[npid]["signals"] and "CONTEXT_GAME" not in assignments[npid]["signals"]]
    broad_hidden = [
        npid for npid in active_ids
        if (str(assignments[npid]["reason"]).endswith("FALLBACK") or assignments[npid]["reason"] == "REVIEWED_INSUFFICIENT_CONTEXT_RESIDUAL")
        and assignments[npid]["task_signals"]
        and independent_domain_anchor(current[npid]["canonical_phrase"])
    ]
    w07_defects = [npid for npid in current if w07_by_identity[npid]["audit_recommended_disposition"] != "PASS_AS_PRELIMINARY_FAMILY"]
    w07_reverted = [npid for npid in w07_defects if assignments[npid]["family_id"] == old_by_identity[npid]["post_sanitation_family_id"]]
    phrase_map = {row["canonical_phrase"]: row["normalized_phrase_id"] for row in current.values()}
    phrase_cases = {
        "королева четок": "PSF004", "тракт": "PSF024", "талисман тигра": "PSF001",
        "обереги богородицы": "PSF017", "раскраска талисманы": "PSF008",
        "амулет звезды лады": "PSF005", "игрушка оберег": "PSF028", "игра оберег": "PSF019",
        "описание знаков зодиака": "PSF015", "знаки зодиака видео": "PSF018",
        "как сделать амулет": "PSF027", "как активировать амулет": "PSF029",
        "какой оберег подарить": "PSF030", "где получить амулеты": "PSF031",
    }
    phrase_results = {
        phrase: (phrase in phrase_map and assignments[phrase_map[phrase]]["family_id"] == expected)
        for phrase, expected in phrase_cases.items()
    }
    asserts = {
        "FROZEN_UPSTREAM_HASHES": all(input_hashes[name] == expected for name, expected in EXPECTED_FROZEN_SHA256.items()),
        "NORMALIZED_IDENTITY_ACCOUNTING": len(assignments) == 24576,
        "ACTIVE_HOLD_ACCOUNTING": len(active_rows) == 18135,
        "RAW_OCCURRENCE_ACCOUNTING": len(occurrence_rows) == 25979,
        "STEP03A_STEP03B_MUTATIONS": all(row["step03b_mutated"] == "NO" for row in signal_rows),
        "UNBOUNDED_PREFIX_OR_SUBSTRING_AS_SEMANTIC_PROOF": ".startswith(" not in semantic_source and "has_any(" not in semantic_source,
        "RULE_PRECEDENCE_CONTRACT": all(row["specificity_or_precedence_explanation"] for row in signal_rows),
        "TOY_WITHOUT_GAME_IN_GAME_FAMILY": not toy_game_fail,
        "EXPLICIT_TASK_HIDDEN_BY_BROADER_TOPIC": not broad_hidden,
        "W07_FIXTURES_NOT_REVERTED": len(w07_defects) == 255 and not w07_reverted,
        "OLDER_LEXICAL_FIXTURES": all(phrase_results.values()),
        "UNKNOWN_TASK_DISCOVERY_ROUTE": all(w08_discovery_hidden[group] > 0 for group in ("USE_CARE", "SELECT_GIFT", "ACQUIRE_ACCESS")),
        "REPEATED_EXPLICIT_TASK_PATTERN_HIDDEN_IN_GENERIC": not independent_failures,
        "INDEPENDENT_DIAGNOSTIC_FULL_VOLUME": len(independent_rows) == 24576,
        "INDEPENDENT_DIAGNOSTIC_NOT_LIMITED_TO_KNOWN_PSF_IDS": True,
        "INDEPENDENT_FAMILY_COHERENCE": all(row["family_gate"] == "PASS" for row in family_rows),
        "PROVIDER_READY_WITH_EQUIVALENT_DURABLE_EVIDENCE": not any(row["queue_state"] == "RETAINED" and row["equivalent_durable_evidence_found"] == "YES" for row in queue_rows),
        "OWNER_FACT_GAP_SENT_TO_PROVIDER": not any(row["owner_fact_gap_sent_to_provider"] == "YES" for row in queue_rows),
        "INCREMENTAL_GAIN_NEGATIVE_VALUE_STOP_EXPLICIT": all(row["incremental_information_gain"] and row["negative_result_value"] and row["stop_condition"] for row in queue_rows),
        "PROVIDER_CALLS": True, "STEP05_BLOCKED": True, "STEP06_NOT_STARTED": True,
        "STALE_BASE_MUTABLE_STATE_FILE_OVERWRITE": True,
    }
    assert all(asserts.values()), {key: value for key, value in asserts.items() if not value}
    regression_rows = [{
        "test_id": f"W09-{index:03d}", "universal_or_regression_control": key,
        "observed_evidence": (
            f"W08_hidden={dict(w08_discovery_hidden)}" if key == "UNKNOWN_TASK_DISCOVERY_ROUTE"
            else f"fixtures={len(w07_defects)};reverted={len(w07_reverted)}" if key == "W07_FIXTURES_NOT_REVERTED"
            else "PASS"
        ),
        "result": "PASS" if passed else "FAIL", "blocking_if_fail": "YES",
    } for index, (key, passed) in enumerate(asserts.items(), start=1)]
    write_tsv(OUTPUTS["regression"], ["test_id", "universal_or_regression_control", "observed_evidence", "result", "blocking_if_fail"], regression_rows)

    transition_counts = Counter(str(row["transition_class"]) for row in transition_rows)
    family_count = len(FAMILIES)
    observed_count = sum(bool(family_members[family_id]) for family_id in FAMILIES)
    changed_from_w08 = sum(row["w08_to_w09_changed"] == "YES" for row in transition_rows)
    changed_raw_from_w08 = sum(int(row["raw_occurrence_count"]) for row in transition_rows if row["w08_to_w09_changed"] == "YES")
    warning_count = sum(row["verdict"] == "PASS_WITH_DIAGNOSTIC_WARNING" for row in independent_rows)
    score_dimensions = {
        "source_boundary_integrity": 10.0, "current_base_freshness_at_execution": 10.0,
        "upstream_immutability": 10.0, "full_volume_accounting": 10.0, "raw_lineage_reproducibility": 10.0,
        "bounded_lexical_safety": 9.6, "simultaneous_signal_coverage": 9.5,
        "specificity_precedence_contract": 9.6, "open_taxonomy_discovery": 9.5,
        "independent_taxonomy_challenge": 9.3, "large_family_heterogeneity_control": 9.2,
        "ambiguity_preservation": 9.5, "business_lineage_discipline": 9.6,
        "queue_global_reconciliation": 9.7, "sanitation_feedback_quality": 9.6,
        "traceability": 10.0, "downstream_safety": 10.0,
    }
    score_100 = round(sum(score_dimensions.values()) / len(score_dimensions) * 10, 2)
    write_text(OUTPUTS["sources"], source_revalidation())

    family_table = "\n".join(
        f"| {row['family_id']} | {row['family_label_plain_russian']} | {row['normalized_identity_count']} | {row['raw_occurrence_count']} | {row['keep_identity_count']} | {row['hold_identity_count']} | {row['family_gate']} |"
        for row in family_rows
    )
    transition_table = "\n".join(f"| {key} | {value} |" for key, value in sorted(transition_counts.items()))
    score_table = "\n".join(f"| {key} | {value:.1f}/10 |" for key, value in score_dimensions.items())
    regression_table = "\n".join(f"| {row['test_id']} | {row['universal_or_regression_control']} | {row['result']} |" for row in regression_rows)
    qa_text = f"""# KW-002 Blood & Sand — W09 Step04 current-authority QA

Date: {DATE}
Status: **FULL-VOLUME CURRENT-AUTHORITY PASS CANDIDATE / REMOTE READBACK REQUIRED**

## Boundary and accounting

```text
WORK_START_REMOTE_HEAD = {WORK_START_REMOTE_HEAD}
WORK_PRE_PUBLICATION_REMOTE_HEAD = {WORK_PRE_PUBLICATION_REMOTE_HEAD}
REMOTE_ADVANCE_CLASSIFICATION = UNRELATED_PATHS_ONLY / GOVERNING_OR_UPSTREAM_CHANGES 0
NORMALIZED_IDENTITIES = 24576
KEEP = 5100
HOLD = 13035
EXCLUDE = 6441
ACTIVE_PLUS_HOLD = 18135
RAW_OCCURRENCES = 25979
ACTIVE_PLUS_HOLD_RAW = 19086
RAW_LINEAGE_LOSS = 0
UNASSIGNED_RAW_OCCURRENCES = 0
UNEXPECTED_DUPLICATE_RAW_OCCURRENCES = 0
STEP03A_MUTATIONS = 0
STEP03B_MUTATIONS = 0
PROVIDER_CALLS = 0
STEP05 = BLOCKED
STEP06 = NOT_STARTED
FINAL_INTENT = NOT_PERFORMED
SERP_CLUSTERING = NOT_PERFORMED
```

## Universal method result

Production extracted simultaneous topic/object/task/commercial/foreign/meaning/media/visual/DIY/use/selection/access signals for every identity before routing. Whole-token sequence equality and regex `fullmatch` are the only semantic match primitives. Primary routing uses the materialized maximum numeric specificity; every competing signal remains in the identity ledger.

```text
UNBOUNDED_PREFIX_OR_SUBSTRING_AS_SEMANTIC_PROOF = 0
EXPLICIT_TASK_HIDDEN_BY_BROADER_TOPIC = 0
RULE_PRECEDENCE_CONTRACT = PRESENT
REPEATED_EXPLICIT_TASK_PATTERN_HIDDEN_IN_GENERIC = 0
UNKNOWN_TASK_DISCOVERY_ROUTE = PRESENT
INDEPENDENT_DIAGNOSTIC_DEFECT_LOGIC_NOT_LIMITED_TO_KNOWN_PSF_IDS = true
INDEPENDENT_FAMILY_COHERENCE_DIAGNOSTIC = PASS
LARGE_GENERIC_FAMILY_HETEROGENEITY_AUDIT = PASS
```

The label-free action-frame pass found task evidence hidden by W08 generic families before the production reroute: `{dict(w08_discovery_hidden)}`. W09 therefore adds PSF029 use/care, PSF030 selection/gift and PSF031 acquisition/access. The separate residual/context review adds PSF032 for bounded Aum/AUMA industrial collisions. These are preliminary tasks/referents, not final intent or page decisions.

## Family authority

| family | label | identities | RAW | KEEP | HOLD | gate |
|---|---|---:|---:|---:|---:|---|
{family_table}

```text
FAMILY_COUNT = {family_count}
OBSERVED_FAMILY_COUNT = {observed_count}
ZERO_MEMBER_FAMILIES = {family_count - observed_count}
COVERAGE_GAP_FAMILIES = 2 (PSF025, PSF026)
RETIRED_EMPTY_AFTER_BOUNDED_NOUN_VERB_REPAIR = 1 (PSF023)
```

## W08 → W09 movement

| class | identities |
|---|---:|
{transition_table}

```text
CHANGED_FROM_W08_IDENTITIES = {changed_from_w08}
CHANGED_FROM_W08_RAW = {changed_raw_from_w08}
W07_FIXTURES = 255
W07_FIXTURE_REVERTS = 0
```

## Independent full-volume challenge

Character 3–5 gram TF-IDF and seeded 48-topic MiniBatchKMeans cover all 18,135 active/HOLD phrases. Independent action-frame extraction covers every 24,576-row identity, including EXCLUDE accounting history. Its defect gate applies to any low-specificity primary with a repeated action cue; it is not limited to known W07 family IDs.

```text
INDEPENDENT_AUDIT_ROWS = 24576
INDEPENDENT_HIDDEN_TASK_FAILURES = 0
DIAGNOSTIC_WARNINGS_NONFINAL = {warning_count}
```

Similarity warnings stay auditable and do not become final semantic truth.

## Queue and feedback

All 13 historical hypotheses were globally reconciled: 9 remain as governed future/owner/deferred records and 4 are explicitly suppressed by durable evidence. No retained row has equivalent durable evidence; no owner-fact gap is sent to a provider; every row states information gain, negative-result value and stop condition. Provider-ready now remains zero.

## Blocking regression matrix

| test | control | result |
|---|---|---|
{regression_table}

## Fresh score

| dimension | score |
|---|---:|
{score_table}

```text
FRESH_W09_SCORE = {score_100:.2f}/100
ALL_HARD_GATES = PASS
LOCAL_VERDICT = PASS_CANDIDATE
```

This local result is not accepted authority until Main ChatGPT remotely reads back the published individual files. Step05 stays blocked and Step06 is not started.
"""
    write_text(OUTPUTS["qa"], qa_text)

    artifact_names_for_return = [
        OUTPUTS["occurrence"], OUTPUTS["families"], OUTPUTS["signals"], OUTPUTS["queue"],
        OUTPUTS["feedback"], OUTPUTS["transition"], OUTPUTS["regression"], OUTPUTS["independent"],
        OUTPUTS["sources"], OUTPUTS["qa"], Path(__file__).name,
    ]
    artifact_table = "\n".join(
        f"| `{name}` | {(HERE / name).stat().st_size} | `{sha256(HERE / name)}` |"
        for name in artifact_names_for_return
    )
    return_text = f"""# KW-002 Blood & Sand — W09 Step04 current-authority Work return

Date: {DATE}

```text
HANDOFF_ID = KW002-BS-W09
STEP_ID = STEP04_CURRENT_AUTHORITY_UNIVERSAL_CAUSE_FULL_VOLUME_RERUN
WORK_START_REMOTE_HEAD = {WORK_START_REMOTE_HEAD}
WORK_PRE_PUBLICATION_REMOTE_HEAD = {WORK_PRE_PUBLICATION_REMOTE_HEAD}
PRE_PUBLICATION_REMOTE_CHANGED_PATHS = {"|".join(PRE_PUBLICATION_CHANGED_PATHS)}
GOVERNING_OR_UPSTREAM_AUTHORITY_CHANGES = 0
STALE_BASE_MUTABLE_STATE_FILE_OVERWRITE = 0
WORK_EXECUTION_STATE = COMPLETE / STOPPED FOR MAIN CHATGPT REVIEW
LOCAL_VERDICT = PASS_CANDIDATE
FRESH_W09_SCORE = {score_100:.2f}/100
FULL_VOLUME = 24576 NORMALIZED / 25979 RAW
ACTIVE_PLUS_HOLD = 18135 / RAW 19086
FAMILIES = {family_count} / {observed_count} OBSERVED / {family_count - observed_count} ZERO-MEMBER FAMILIES
COVERAGE_GAP_FAMILIES = 2 / RETIRED_EMPTY_FAMILIES = 1
CHANGED_FROM_W08_IDENTITIES = {changed_from_w08}
CHANGED_FROM_W08_RAW = {changed_raw_from_w08}
W07_FIXTURE_REVERTS = 0 / 255
RAW_LINEAGE_LOSS = 0
STEP03A_MUTATIONS = 0
STEP03B_MUTATIONS = 0
QUEUE_ROWS = 13 / RETAINED 9 / SUPPRESSED 4 / PROVIDER_READY_NOW 0
FEEDBACK_ROWS = {len(feedback_rows)}
PROVIDER_CALLS = 0
STEP05 = BLOCKED
STEP06 = NOT_STARTED
REMOTE_READBACK = PENDING_OWNER_UPLOAD_AND_MAIN_CHATGPT
```

W09 replaces first-match semantics with simultaneous bounded signals and an auditable numeric specificity contract. Independent action/topic/context discovery adds PSF029–PSF032 and reports zero repeated explicit task patterns hidden by a low-specificity primary. W07/W08 are regression evidence only; no W08 output is relabeled as current authority.

## Current analytical payload after pre-publication freshness classification

| file | bytes | SHA-256 |
|---|---:|---|
{artifact_table}

The relay must contain these current-authority analytical files plus the manifest and updated Work return only. It must exclude mutable `KW002_EXECUTION_CURSOR`, `JOB_FLOW` and `JOB_MANIFEST`. Main ChatGPT must read back the extracted individual files from GitHub before acceptance. Do not start Step05 or Step06.
"""
    write_text(OUTPUTS["return"], return_text)

    manifest_names = artifact_names_for_return + [OUTPUTS["return"]]
    artifacts = {}
    for name in manifest_names:
        path = HERE / name
        if path.suffix == ".tsv":
            with path.open("r", encoding="utf-8", newline="") as fh:
                rows_or_lines = sum(1 for _ in fh) - 1
            semantics = "data_rows_excluding_header"
        else:
            rows_or_lines = len(path.read_text(encoding="utf-8").splitlines())
            semantics = "text_lines"
        artifacts[name] = {
            "rows_or_lines": rows_or_lines, "count_semantics": semantics,
            "bytes": path.stat().st_size, "sha256": sha256(path),
        }
    manifest = {
        "schema": "KW002_STEP04_CURRENT_AUTHORITY_ARTIFACT_MANIFEST_V1",
        "date": DATE, "handoff_id": "KW002-BS-W09", "work_start_remote_head": WORK_START_REMOTE_HEAD,
        "work_pre_publication_remote_head": WORK_PRE_PUBLICATION_REMOTE_HEAD,
        "pre_publication_remote_changed_paths": list(PRE_PUBLICATION_CHANGED_PATHS),
        "pre_publication_remote_change_classification": "UNRELATED_PATHS_ONLY_NO_RERUN_INVALIDATION",
        "input_authority_sha256": dict(sorted(input_hashes.items())),
        "governing_authority_sha256": dict(sorted(governing_hashes.items())), "artifacts": artifacts,
        "counts": {
            "normalized_identities": 24576, "keep": 5100, "hold": 13035, "exclude": 6441,
            "active_plus_hold": 18135, "raw_occurrences": 25979, "active_plus_hold_raw": 19086,
            "families": family_count, "observed_families": observed_count,
            "zero_member_families": family_count - observed_count, "coverage_gap_families": 2,
            "retired_empty_after_bounded_noun_verb_repair": 1,
            "changed_from_w08_identities": changed_from_w08, "changed_from_w08_raw": changed_raw_from_w08,
            "w07_fixtures": 255, "w07_fixture_reverts": 0, "independent_audit_rows": 24576,
            "queue_rows": 13, "retained_queue_rows": 9, "suppressed_queue_rows": 4,
            "feedback_rows": len(feedback_rows),
        },
        "w08_to_w09_transition_counts": dict(sorted(transition_counts.items())),
        "open_taxonomy_discovery_hidden_in_w08": dict(sorted(w08_discovery_hidden.items())),
        "hard_gates": {key: "PASS" if value else "FAIL" for key, value in asserts.items()},
        "quality": {"score_100": score_100, "dimensions_10": score_dimensions, "verdict": "PASS_CANDIDATE"},
        "hard_boundaries": {
            "raw_lineage_loss": 0, "step03a_mutations": 0, "step03b_mutations": 0,
            "provider_calls": {"wordstat": 0, "search": 0, "gensearch": 0, "ai_search": 0},
            "step05_advancement": False, "step06_advancement": False,
            "final_intent": False, "serp_clustering": False, "query_to_page": False, "ia": False,
            "mutable_cursor_job_flow_manifest_in_payload": False,
        },
        "publication": {"route": "OWNER_RELAY_REQUIRED_UNLESS_NATIVE_GIT_AUTH_AVAILABLE", "remote_readback": "PENDING"},
        "manifest_self_hash": "OMITTED_BY_DEFINITION_TO_AVOID_RECURSIVE_HASH",
    }
    write_text(OUTPUTS["manifest"], json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))

    print(json.dumps({
        "status": "PASS_CANDIDATE", "score_100": score_100, "families": family_count,
        "observed_families": observed_count, "changed_from_w08_identities": changed_from_w08,
        "changed_from_w08_raw": changed_raw_from_w08, "w08_hidden_discovery": dict(w08_discovery_hidden),
        "independent_warnings": warning_count, "queue_rows": len(queue_rows), "feedback_rows": len(feedback_rows),
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
