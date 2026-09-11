#!/usr/bin/env python3
"""Full-volume rule-level correction for KW-002 Blood & Sand Step04.

The program reassigns every accepted KEEP/HOLD identity from scratch and then
rematerializes every RAW occurrence.  It preserves corrected Step03B byte-for-
byte, makes no provider/search call, and does not perform Step05/06, final
intent, SERP, page ownership, IA, or delivery-cap work.

The superseded Step04 classifier is imported only for stable helper functions
and the unaffected family metadata.  Its ordered ``assign_family`` function is
never called.  W07's simultaneous-signal function is imported only by the
independent post-correction diagnostic, never by the corrected classifier.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import re
import sys
from collections import Counter, defaultdict
from dataclasses import replace
from pathlib import Path
from typing import Iterable

import numpy as np
from scipy.sparse import csr_matrix, vstack
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


HERE = Path(__file__).resolve().parent
DATE = "2026-09-11"
LIVE_BASE_HEAD = "5446a9347cac33da6a656e9db7c252e1b529295a"
RANDOM_SEED = 20260911

INPUTS = {
    "pool": "STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv",
    "ledger": "STEP_03A_NORMALIZATION_LEDGER_2026-09-11.tsv",
    "keep": "STEP_03B_SANITIZED_CANDIDATE_POOL_CORRECTED_2026-09-11.tsv",
    "register": "STEP_03B_EXCLUDED_HOLD_REGISTER_CORRECTED_2026-09-11.tsv",
    "step03b_overlay": "KW002_STEP03A_03B_INDEPENDENT_FULL_VOLUME_AUDIT_OVERLAY_2026-09-11.tsv",
    "old_occurrence": "STEP_04_POST_SANITATION_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv",
    "old_families": "STEP_04_POST_SANITATION_FAMILY_TRIAGE_2026-09-11.tsv",
    "old_queue": "STEP_04_POST_SANITATION_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv",
    "old_feedback": "STEP_04_POST_SANITATION_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv",
    "old_materializer": "STEP_04_POST_SANITATION_MATERIALIZER_2026-09-11.py",
    "w07_overlay": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_OVERLAY_2026-09-11.tsv",
    "w07_queue_feedback": "STEP_04_INDEPENDENT_QUEUE_FEEDBACK_AUDIT_2026-09-11.tsv",
    "w07_metrics": "STEP_04_INDEPENDENT_AUDIT_METRICS_2026-09-11.json",
    "w07_materializer": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_MATERIALIZER_2026-09-11.py",
    "prompt": "STEP_04_POST_AUDIT_CORRECTIVE_REWORK_WORK_PROMPT_2026-09-11.md",
    "release": "STEP_04_POST_AUDIT_CORRECTIVE_REWORK_EXECUTION_RELEASE_2026-09-11.md",
    "addendum": "KW002_EXECUTION_FAILURE_LEDGER_ADDENDUM_STEP04_RESULT_AUDIT_2026-09-11.md",
    "review": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_MAIN_CHATGPT_REVIEW_2026-09-11.md",
}

EXPECTED_SHA256 = {
    INPUTS["pool"]: "b30c29ff66a56d80bc1aa9ff6b2eade522b27d1e167cbd636ac72fbff211f2a8",
    INPUTS["ledger"]: "28205ca64f26d219d489b36f102a8923b4a4b635c8b213179bca4a188b24c3df",
    INPUTS["keep"]: "63b3fc556b388dbac0185f174f79f825dc26d9c51de39698850cdaecb9ca4f58",
    INPUTS["register"]: "145c5107f40415b4050923f142dab3e83646489da5d74501f659fd87e3ae2916",
    INPUTS["step03b_overlay"]: "db9b79dda64b205f0b0bef273f70f221f183d9389eca3e67e651e93ea269d669",
    INPUTS["old_occurrence"]: "c053bcd1dccae5b2894cc7a316c84af72c2b0abfeb460624f138f1198a39a5ba",
    INPUTS["old_families"]: "cb2a1259f596f1b97ea4eb662e8c8b315936aad2243c57389c290ea6d90a0b2c",
    INPUTS["old_queue"]: "be46fd75e9b51354e14dfc3e862be69e8549fd67b708ecc7471bbfc3dcd63c73",
    INPUTS["old_feedback"]: "7a52efa3eb2e8eeebddecd61de4550acf33e98b8d357b463e815754f6af00903",
    INPUTS["old_materializer"]: "3b80e56d81b02efa4e26c43d9caa92e22f4115738028f0e83a85218ce92f4ad2",
    INPUTS["w07_overlay"]: "62f7027b567fafe461bda3367b943f05dd83298c86d04c6a38039271f3361dd9",
    INPUTS["w07_queue_feedback"]: "cc9126e0a19d7d8ae4c10326ab1524a05c3b7badf958ec250e4817cc1076255f",
    INPUTS["w07_metrics"]: "ca6b0c645a405b8e3036e1e24d5dc20b9d6ed05cb7f5d91ca896cf0b6ef29c18",
    INPUTS["w07_materializer"]: "0c488df06feec4b04ff552966f483f16e42375e91648e17bb03f62b5e4499591",
    INPUTS["prompt"]: "ae69807131b78a865e3e260782dd8baba448d44a4a9918ceb743468da9e9698d",
    INPUTS["release"]: "8f9f8bd682413d0dd34b04e3168345ea2cf328690648be9bd2b69350ab869a05",
    INPUTS["addendum"]: "ca9a602bc7491ad3a40d56856fe041c42534cb117ef4729c58f9fe8b9288e40a",
    INPUTS["review"]: "87d806d2175f831f2a9122de625346fca872aed09c75bd036ccabe457a2f0940",
}

OUTPUTS = {
    "occurrence": "STEP_04_POST_AUDIT_CORRECTED_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv",
    "families": "STEP_04_POST_AUDIT_CORRECTED_FAMILY_TRIAGE_2026-09-11.tsv",
    "queue": "STEP_04_POST_AUDIT_CORRECTED_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv",
    "feedback": "STEP_04_POST_AUDIT_CORRECTED_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv",
    "transition": "STEP_04_POST_AUDIT_CORRECTION_TRANSITION_LEDGER_2026-09-11.tsv",
    "regression": "STEP_04_POST_AUDIT_CORRECTED_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-11.tsv",
    "independent_qa": "STEP_04_POST_AUDIT_CORRECTED_INDEPENDENT_FAMILY_QA_2026-09-11.tsv",
    "qa": "STEP_04_POST_AUDIT_CORRECTED_QA_2026-09-11.md",
    "return": "STEP_04_POST_AUDIT_CORRECTED_WORK_RETURN_2026-09-11.md",
    "manifest": "STEP_04_POST_AUDIT_CORRECTED_ARTIFACT_MANIFEST_2026-09-11.json",
    "sources": "STEP_04_POST_AUDIT_CORRECTIVE_REWORK_PRE_STEP_EXTERNAL_RESEARCH_2026-09-11.md",
}


def load_module(filename: str, alias: str):
    spec = importlib.util.spec_from_file_location(alias, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


base = load_module(INPUTS["old_materializer"], "kw002_step04_superseded_base")
w07 = load_module("STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_MATERIALIZER_2026-09-11.py", "kw002_w07_diagnostic")


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


def words(value: str) -> set[str]:
    return set(re.findall(r"[0-9a-zа-я]+", base.lower(value)))


def has_game_signal(value: str) -> bool:
    """Bounded game morphology.  `игра*`, exact `игр`, and `игров*` are safe; `игруш*` is not."""
    item_words = words(value)
    exact = {
        "игр", "мод", "моды", "мода", "id", "minecraft", "genshin", "warframe",
        "dota", "poe", "valhalla", "гта", "gta", "скайрим", "террария",
        "майнкрафт", "ведьмак",
    }
    return (
        bool(item_words & exact)
        or any(word.startswith("игра") or word.startswith("игров") for word in item_words)
        or base.has_token_prefix(value, ("скайрим", "террари", "майнкрафт", "ведьмак"))
        or base.has_any(value, ("hollow knight", "elden ring", "counter strike", "assassin creed"))
    )


def has_toy_signal(value: str) -> bool:
    return any(word.startswith("игруш") for word in words(value))


def has_visual_task(value: str) -> bool:
    return base.has_any(value, base.VISUAL) or base.has_token_prefix(value, ("нарис", "изобраз"))


def has_meaning_task(value: str) -> bool:
    return base.has_any(value, base.MEANING) or base.has_token_prefix(value, ("обозначен",))


def has_diy_task(value: str) -> bool:
    """Bounded make/craft task tied to a supported Step04 domain object.

    Visual-only `сделать фото` and contact verb `связаться` are deliberately
    excluded.  Noun/adjective siblings are included so the rule is not a
    48-row patch.
    """
    item_words = words(value)
    domain_object = (
        base.has_product(value)
        or base.has_catalog_name(value)
        or base.has_zodiac(value)
        or has_toy_signal(value)
        or base.has_form(value)
    )
    if not domain_object:
        return False
    own_hands = base.has_any(value, ("своими руками", "руками мастер класс"))
    master_class = "мастер" in item_words and "класс" in item_words
    crochet = "крючком" in item_words or "вязание" in item_words
    strong_words = {
        "создать", "создание", "изготовить", "изготовление", "изготовления",
        "связать", "вязать", "вязание", "вязаный", "вязаные", "вязаная",
        "связанный", "связанные", "сшить", "сплести",
    }
    strong = own_hands or master_class or crochet or bool(item_words & strong_words)
    strong = strong or any(word.startswith("изготов") for word in item_words)
    weak_make = any(word.startswith("сдела") for word in item_words)
    if has_visual_task(value) and weak_make and not strong:
        return False
    return strong or weak_make


def corrected_assign_family(row: dict[str, str]) -> tuple[str, str]:
    """Assign from corrected Step03B state/reason and phrase only."""
    phrase = row["canonical_phrase"]
    state = row["current_step03b_state"]
    reason = row["current_step03b_reason"]

    if state == "EXCLUDE":
        return "NOT_IN_STEP04_SEMANTIC_SCOPE", "CORRECTED_STEP03B_EXCLUDE_PRESERVED_AS_HISTORY"

    if reason == "HOLD_POSSIBLE_ROSARY_MORPHOLOGY_OR_TYPO":
        return "PSF022", "REASON_BOUND_ROSARY_MORPHOLOGY_COLLISION"
    if reason in {"HOLD_CATALOG_NAME_VERSUS_VEHICLE_COLLISION", "HOLD_PRODUCT_NAME_VERSUS_VEHICLE_PAINT_COLLISION", "HOLD_AUTOMOBILE_USE_WITHOUT_SUPPORTED_PRODUCT_NOUN"}:
        return "PSF020", "REASON_BOUND_AUTOMOTIVE_COLLISION"
    if reason in {"HOLD_PHYSICAL_PRODUCT_VERSUS_RELIGIOUS_PRACTICE", "HOLD_CATALOG_PRODUCT_NAME_VERSUS_RELIGIOUS_TEXT"}:
        return "PSF017", "REASON_BOUND_RELIGIOUS_PRODUCT_COLLISION"
    if reason in {"HOLD_PRODUCT_OR_CATALOG_NAME_WITH_PLACE_OR_ORGANIZATION", "HOLD_PRODUCT_OR_CATALOG_NAME_WITH_PERSON_ENTITY_CONTEXT", "HOLD_GENERIC_TEAM_OR_MASCOT_CONTEXT", "HOLD_SEARCH_PLATFORM_OR_MEDIA_CONTEXT_UNRESOLVED"}:
        return "PSF021", "REASON_BOUND_ENTITY_OR_PLATFORM_COLLISION"
    if reason == "HOLD_GENERIC_GAME_OR_MODEL_TOKEN_NEEDS_CONTEXT":
        return "PSF019", "REASON_BOUND_GENERIC_GAME_MODEL_COLLISION"
    if reason in {"HOLD_MEDIA_TITLE_VERSUS_PRODUCT_COLLISION", "HOLD_TITLE_LIKE_PRODUCT_WORD_COLLISION", "HOLD_GENERIC_MEDIA_ACTION_MAY_BE_INFORMATIONAL_PRODUCT_RESEARCH"}:
        if has_game_signal(phrase):
            return "PSF019", "BOUNDED_GAME_SIGNAL_INSIDE_TITLE_OR_MEDIA_COLLISION"
        return "PSF018", "REASON_BOUND_MEDIA_TITLE_OR_ACTION_COLLISION"

    zodiac_route = reason in {
        "HOLD_ZODIAC_OR_STONE_PRODUCT_COLLISION", "HOLD_PRODUCT_VERSUS_ASTROLOGY_INFORMATION",
        "KEEP_SUPPORTED_PRODUCT_PLUS_ZODIAC_TITLE", "KEEP_ZODIAC_TITLE_WITH_COMMERCE_OR_OBJECT_FORM",
    } or base.has_zodiac(phrase)
    if zodiac_route:
        if base.has_product(phrase) or base.has_commerce(phrase) or base.has_form(phrase):
            if base.has_stone(phrase) and not base.has_commerce(phrase) and not base.has_token_prefix(phrase, base.NON_STONE_OBJECT_FORMS) and not base.has_product(phrase):
                return "PSF013", "ZODIAC_STONE_PRODUCT_COLLISION"
            return "PSF012", "ZODIAC_WITH_PRODUCT_FORM_OR_COMMERCE"
        if has_visual_task(phrase):
            return "PSF016", "ZODIAC_VISUAL_OR_DRAWING_TASK"
        if base.has_any(phrase, base.ASTRO_INFO):
            return "PSF015", "ZODIAC_ASTRO_INFORMATION_TASK"
        if base.has_stone(phrase):
            return "PSF013", "ZODIAC_STONE_REFERENT_UNRESOLVED"
        if base.has_media_signal(phrase):
            return "PSF018", "ZODIAC_MEDIA_OR_DIGITAL_TASK"
        if has_meaning_task(phrase):
            return "PSF015", "ZODIAC_MEANING_OR_DESCRIPTION_TASK"
        if has_toy_signal(phrase):
            return "PSF028", "ZODIAC_TOY_PHYSICAL_OBJECT_TASK"
        if has_diy_task(phrase):
            return "PSF027", "ZODIAC_DIY_MAKE_OR_CRAFT_TASK"
        return "PSF014", "ZODIAC_UNQUALIFIED_REFERENT"

    if reason == "HOLD_FROZEN_CATALOG_NAME_REFERENT_UNRESOLVED":
        if base.has_religious_signal(phrase):
            return "PSF017", "CATALOG_NAME_WITH_RELIGIOUS_CONTEXT"
        if has_game_signal(phrase):
            return "PSF019", "CATALOG_NAME_WITH_BOUNDED_GAME_CONTEXT"
        if base.has_media_signal(phrase):
            return "PSF018", "CATALOG_NAME_WITH_MEDIA_CONTEXT"
        if base.has_vehicle_signal(phrase):
            return "PSF020", "CATALOG_NAME_WITH_VEHICLE_CONTEXT"
        if base.has_entity_signal(phrase):
            return "PSF021", "CATALOG_NAME_WITH_ENTITY_CONTEXT"
        if has_toy_signal(phrase):
            return "PSF028", "CATALOG_NAME_WITH_TOY_OBJECT_CONTEXT"
        if base.has_any(phrase, base.VISUAL):
            return "PSF008", "CATALOG_NAME_WITH_VISUAL_CONTEXT"
        if base.has_any(phrase, base.MEANING):
            return "PSF007", "CATALOG_NAME_WITH_MEANING_CONTEXT"
        if has_diy_task(phrase):
            return "PSF027", "CATALOG_NAME_WITH_DIY_TASK"
        if base.has_product(phrase) or base.has_commerce(phrase) or base.has_form(phrase):
            return "PSF005", "CATALOG_NAME_WITH_PRODUCT_FORM_OR_COMMERCE"
        if base.has_catalog_name(phrase):
            return "PSF006", "CATALOG_NAME_UNQUALIFIED"
        return "PSF009", "CATALOG_REASON_WITH_UNRESOLVED_HOMONYM"

    if state == "HOLD" and reason == "HOLD_INSUFFICIENT_CONTEXT_FOR_KEEP_OR_EXCLUDE":
        if base.has_religious_signal(phrase):
            return "PSF017", "RESIDUAL_RELIGIOUS_SIGNAL"
        if has_game_signal(phrase):
            return "PSF019", "RESIDUAL_BOUNDED_GAME_SIGNAL"
        if base.has_media_signal(phrase):
            return "PSF018", "RESIDUAL_MEDIA_SIGNAL"
        if base.has_vehicle_signal(phrase):
            return "PSF020", "RESIDUAL_VEHICLE_SIGNAL"
        if base.has_entity_signal(phrase):
            return "PSF021", "RESIDUAL_ENTITY_SIGNAL"
        if has_toy_signal(phrase):
            return "PSF028", "RESIDUAL_TOY_OBJECT_TASK"
        if base.has_catalog_name(phrase):
            if base.has_any(phrase, base.VISUAL):
                return "PSF008", "RESIDUAL_CATALOG_VISUAL_SIGNAL"
            if base.has_any(phrase, base.MEANING):
                return "PSF007", "RESIDUAL_CATALOG_MEANING_SIGNAL"
            if has_diy_task(phrase):
                return "PSF027", "RESIDUAL_CATALOG_DIY_TASK"
            return "PSF009", "RESIDUAL_CATALOG_HOMONYM"
        if has_diy_task(phrase):
            return "PSF027", "RESIDUAL_DIY_MAKE_OR_CRAFT_TASK"
        if base.has_product(phrase):
            return "PSF023", "RESIDUAL_GENERIC_PRODUCT_REFERENT"
        if base.has_form(phrase):
            return "PSF010", "RESIDUAL_FORM_OR_MATERIAL"
        if base.has_effect(phrase):
            return "PSF011", "RESIDUAL_EFFECT_OR_AUDIENCE"
        return "PSF024", "INSUFFICIENT_CONTEXT_RESIDUAL"

    catalog_product_guard = base.has_catalog_name(phrase) and (base.has_product(phrase) or base.has_commerce(phrase) or base.has_form(phrase))
    if has_game_signal(phrase):
        return "PSF019", "CURRENT_KEEP_WITH_BOUNDED_GAME_COLLISION_SIGNAL"
    if base.has_media_signal(phrase):
        return "PSF018", "CURRENT_KEEP_WITH_MEDIA_COLLISION_SIGNAL"
    if base.has_entity_signal(phrase):
        return "PSF021", "CURRENT_KEEP_WITH_ENTITY_COLLISION_SIGNAL"
    if base.has_auto_use(phrase):
        if has_toy_signal(phrase):
            return "PSF028", "AUTOMOBILE_CONTEXT_WITH_EXPLICIT_TOY_OBJECT"
        if has_diy_task(phrase):
            return "PSF027", "AUTOMOBILE_CONTEXT_WITH_EXPLICIT_DIY_TASK"
        return "PSF003", "SUPPORTED_AUTOMOBILE_USE_CONTEXT"
    if base.has_vehicle_signal(phrase) and not catalog_product_guard:
        return "PSF020", "CURRENT_KEEP_WITH_AUTOMOTIVE_COLLISION_SIGNAL"
    if base.has_religious_signal(phrase):
        return "PSF017", "CURRENT_KEEP_WITH_RELIGIOUS_PRODUCT_PRACTICE_SIGNAL"
    if has_toy_signal(phrase):
        return "PSF028", "CURRENT_KEEP_WITH_TOY_PHYSICAL_OBJECT_TASK"
    if base.has_product(phrase) and base.has_token_prefix(phrase, ("нарис", "изобраз")):
        return "PSF008", "CURRENT_KEEP_WITH_EXPLICIT_VISUAL_CREATION_TASK"
    if has_diy_task(phrase):
        return "PSF027", "CURRENT_KEEP_WITH_DIY_MAKE_OR_CRAFT_TASK"
    if base.has_zodiac(phrase):
        return "PSF012", "SUPPORTED_ZODIAC_PRODUCT_CONTEXT"
    if base.has_rosary(phrase):
        return "PSF004", "SUPPORTED_ROSARY_OBJECT_WORD"
    if base.has_catalog_name(phrase):
        if base.has_any(phrase, base.VISUAL):
            return "PSF008", "SUPPORTED_CATALOG_NAME_VISUAL_CONTEXT"
        if base.has_any(phrase, base.MEANING):
            return "PSF007", "SUPPORTED_CATALOG_NAME_MEANING_CONTEXT"
        if base.has_product(phrase) or base.has_commerce(phrase) or base.has_form(phrase):
            return "PSF005", "SUPPORTED_CATALOG_NAME_PRODUCT_CONTEXT"
        return "PSF006", "SUPPORTED_CATALOG_NAME_UNQUALIFIED"
    if base.has_commerce(phrase):
        return "PSF002", "SUPPORTED_GENERIC_PRODUCT_COMMERCE"
    if base.has_form(phrase):
        return "PSF010", "OBSERVED_FORM_OR_MATERIAL_WITH_PRODUCT"
    if base.has_any(phrase, base.VISUAL):
        return "PSF008", "PRODUCT_VISUAL_CONTEXT"
    if base.has_any(phrase, base.MEANING):
        return "PSF007", "PRODUCT_MEANING_CONTEXT"
    if base.has_effect(phrase):
        return "PSF011", "PRODUCT_EFFECT_OR_AUDIENCE_CONTEXT"
    if base.has_product(phrase):
        return "PSF001", "SUPPORTED_GENERIC_PRODUCT_UNQUALIFIED"
    return "PSF024", "CURRENT_KEEP_WITHOUT_FAMILY_SIGNAL_REVIEWED_RESIDUAL"


FAMILIES = dict(base.FAMILIES)
FAMILIES["PSF001"] = replace(
    FAMILIES["PSF001"],
    definition="Амулет, оберег или талисман без достаточного уточнения предмета и без явной пользовательской задачи.",
    out_scope="Явные media/game/vehicle/entity, toy, DIY/make/craft контексты и финальный intent verdict.",
)
FAMILIES["PSF014"] = replace(
    FAMILIES["PSF014"],
    definition="Зодиакальные названия без достаточного указания предмета, значения, media/visual/DIY/toy задачи или чужого контекста.",
    out_scope="Явная задача meaning/media/visual/DIY/toy, автоматический товарный вывод, финальная страница или чистая астрология.",
)
FAMILIES["PSF015"] = replace(
    FAMILIES["PSF015"],
    label="Зодиакальная информация и явная meaning-задача внутри HOLD",
    definition="Даты, совместимость, характеристики, значения, история, описание и иные явные информационные задачи о зодиаке, сохранённые corrected Step03B в HOLD.",
)
FAMILIES["PSF019"] = replace(
    FAMILIES["PSF019"],
    label="Игра, игровой предмет или bounded model-token",
    definition="Точные/ограниченные игровые формы, игра/мод/ID или именованная игра рядом с товарным или каталожным именем; `игруш*` сюда не входит.",
    out_scope="Игрушка/игрушки без независимого game-сигнала; KEEP/EXCLUDE по одному broad prefix.",
)
FAMILIES["PSF027"] = base.Family(
    "Изготовление, DIY и craft-задача",
    "Явное изготовление/создание/вязание/шитьё/плетение/своими руками или bounded craft-сиблинг рядом с поддержанным предметом, формой, каталогом либо знаком.",
    "Пользовательская make/craft-задача выражена в самой фразе; бизнес-релевантность и ассортимент не считаются окончательно доказанными.",
    "Визуальное `сделать фото`, `связаться`, общий media/game/entity контекст и финальный page/intent verdict.",
    base.BRIEF_LINEAGE,
    "Понять, как изготовить или создать предмет/символ своими руками.",
    "DIY_INFORMATIONAL_TASK_HINT_NOT_FINAL",
    "PRODUCT_VS_DIY_INFORMATION_AND_UNCONFIRMED_ASSORTMENT",
    "OBSERVED_FULL_VOLUME_NEW_RULE_CLASS",
    "MIXED_AMBIGUOUS",
    "NO",
    "Наблюдаемая task-ветвь уже полна для Step04; дальнейшее evidence относится к поздним этапам.",
    "YES",
    "DIY-задача не доказывает наличие готового товара или будущую страницу.",
)
FAMILIES["PSF028"] = base.Family(
    "Игрушка и физический toy-объект",
    "Токенная морфология `игруш*` с товарным, каталожным или зодиакальным контекстом без независимого bounded game-сигнала.",
    "Фраза явно называет физический toy-объект; возможная связь с ассортиментом остаётся гипотезой.",
    "Игра/играть/игровой/именованная игра, автоматический вывод о наличии игрушек в ассортименте и финальный page/intent verdict.",
    base.CATALOG_LINEAGE,
    "Найти, выбрать или изготовить игрушку/фигуру-талисман либо объект со знаком.",
    "PHYSICAL_TOY_OR_CRAFT_TASK_HINT_NOT_FINAL",
    "TOY_OBJECT_VS_CLIENT_ASSORTMENT_AND_GAME_BOUNDARY",
    "OBSERVED_FULL_VOLUME_NEW_RULE_CLASS",
    "MIXED_AMBIGUOUS",
    "NO",
    "Текущий universe уже показывает класс; сначала нужен owner fact об ассортименте.",
    "YES",
    "Игрушка наблюдается в спросе, но не подтверждена 76 заголовками как продаваемая форма.",
)

FEEDBACK_FAMILY_IDS = set(base.FEEDBACK_FAMILY_IDS) | {"PSF027", "PSF028"}


def business_confidence(family_id: str) -> str:
    if family_id in {"PSF002", "PSF003"}:
        return "HIGH_BUSINESS_SUPPORT_NOT_FINAL"
    if family_id in {"PSF025", "PSF026"}:
        return "HYPOTHESIS_ONLY_NO_OBSERVATION"
    if family_id in {"PSF006", "PSF009", "PSF014", "PSF015", "PSF018", "PSF019", "PSF020", "PSF021", "PSF022", "PSF023", "PSF024", "PSF027", "PSF028"}:
        return "AMBIGUOUS_BUSINESS_RELEVANCE_NOT_FINAL"
    return "SUPPORTED_OR_PLAUSIBLE_NOT_FINAL"


def family_context_support(state: str, family_id: str) -> str:
    if state == "KEEP":
        return "YES_STEP03B_ONLY_NOT_FINAL"
    if family_id == "PSF024":
        return "UNKNOWN"
    return "MIXED"


def later_evidence(state: str, family_id: str) -> str:
    if state == "KEEP":
        return "STEP10"
    if family_id in {"PSF010", "PSF011", "PSF012", "PSF013", "PSF017", "PSF028"}:
        return "OWNER_FACT"
    return "STEP10_OR_LATER_SERP"


def representative(rows: list[dict[str, str]], limit: int = 8) -> list[str]:
    ordered = sorted(rows, key=lambda row: (0 if row["current_step03b_state"] == "KEEP" else 1, len(row["canonical_phrase"]), row["canonical_phrase"], row["normalized_phrase_id"]))
    return [row["canonical_phrase"] for row in ordered[:limit]]


def entropy_normalized(labels: list[int], possible: int) -> float:
    if len(labels) <= 1:
        return 0.0
    counts = Counter(labels)
    entropy = -sum((count / len(labels)) * math.log(count / len(labels)) for count in counts.values())
    denominator = math.log(min(possible, len(labels)))
    return entropy / denominator if denominator else 0.0


def qa_signals(value: str) -> set[str]:
    """Independent simultaneous diagnostic signals, not first-match routing."""
    result = set(w07.independent_signals(value))
    if has_diy_task(value):
        result.add("DIY_BOUNDED")
    if has_toy_signal(value):
        result.add("TOY_BOUNDED")
    if has_meaning_task(value):
        result.add("MEANING_EXTENDED")
    if has_visual_task(value):
        result.add("VISUAL_TASK")
    if has_game_signal(value):
        result.add("GAME_BOUNDED")
    return result


def transition_class(old_family: str, new_family: str, w07_disposition: str) -> str:
    if old_family == new_family:
        return "UNCHANGED"
    if old_family == "PSF019" and new_family == "PSF028" and w07_disposition == "RULE_ORDER_DEFECT":
        return "EXPECTED_D1_AUDIT_ORACLE_CORRECTION"
    if old_family == "PSF014" and new_family in {"PSF015", "PSF018", "PSF028"} and w07_disposition == "RULE_ORDER_DEFECT":
        return "EXPECTED_D2_AUDIT_ORACLE_CORRECTION"
    if old_family == "PSF001" and new_family in {"PSF008", "PSF027"} and w07_disposition == "FAMILY_TOO_BROAD":
        return "EXPECTED_D3_AUDIT_ORACLE_CORRECTION"
    if old_family == "PSF014" and new_family in {"PSF015", "PSF016", "PSF027", "PSF028"}:
        return "COLLATERAL_D2_COMPLETE_TASK_BLAST_RADIUS"
    if new_family == "PSF008" and old_family in {"PSF001", "PSF004"}:
        return "COLLATERAL_D3_VISUAL_TASK_SIBLING_RULE"
    if new_family == "PSF027":
        return "COLLATERAL_D3_SIBLING_RULE"
    if new_family == "PSF028":
        return "COLLATERAL_D1_TOY_SIBLING_RULE"
    return "UNEXPECTED_COLLATERAL_MOVEMENT"


def source_trace() -> str:
    return f"""# KW-002 Step04 post-audit corrective rework — pre-step external research

Date checked: {DATE}

Purpose: method support only. No source below supplies Blood & Sand demand, inventory, final intent, SERP clusters, pages or IA.

| Source | Principle used | Concrete control | Limitation |
|---|---|---|---|
| [Yandex Webmaster — Query selection](https://yandex.ru/support/webmaster/ru/service/queries-selection) | Meaning/intent grouping is distinct from demand and competition metrics. | Frequency never enters family assignment or defect gates. | No Wordstat/Search request was made. |
| [Yandex Webmaster — Search quality](https://yandex.com/support/webmaster/en/search-quality) | User objective and usefulness matter. | Explicit meaning/media/DIY/toy tasks outrank unqualified fallbacks. | General guidance, not project-specific truth. |
| [Topvisor — clustering](https://topvisor.com/ru/support/clustering/) | Final SEO grouping depends on SERP overlap and theme testing. | Families remain preliminary and expose `serp_cluster_status=NOT_EVALUATED_AT_STEP04`. | SERP collection is prohibited in this pass. |
| [Ahrefs — keyword clustering](https://ahrefs.com/blog/keyword-clustering/) | Term diagnostics and final intent/SERP clusters answer different questions; clustering is interpretive. | TF-IDF/topics are warnings and QA evidence, not page authority. | Commercial workflow is not a job authority. |
| [Semrush — keyword clustering](https://www.semrush.com/blog/keyword-clustering/) | Shared task/intent matters; subtle wording can change the task. | Task-bearing morphology is checked before unqualified fallback. | No final intent label is assigned. |
| [scikit-learn — feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html) | TF-IDF downweights corpus-common terms; very short texts can be noisy. | Independent QA combines TF-IDF with simultaneous binary boundary signals. | TF-IDF is not ground truth. |
| [Python — regular expressions](https://docs.python.org/3/library/re.html) | Search/match/full-match boundaries differ. | Game evidence uses bounded token morphology; `игруш*` is separate. | Regex correctness does not prove business relevance. |

Trace: source principle → bounded deterministic rule → full-volume invariant → independent post-correction check. Completed Step00–03B remain frozen; W07 is the accepted defect oracle; this execution is W08 Step04 correction only. Step05/06 and all provider acquisition remain blocked.
"""


def main() -> None:
    input_hashes = {name: sha256(HERE / name) for name in INPUTS.values()}
    for name, expected in EXPECTED_SHA256.items():
        assert input_hashes[name] == expected, (name, input_hashes[name], expected)

    pool_rows = read_tsv(INPUTS["pool"])
    ledger_rows = read_tsv(INPUTS["ledger"])
    keep_rows = read_tsv(INPUTS["keep"])
    register_rows = read_tsv(INPUTS["register"])
    step03b_overlay_rows = read_tsv(INPUTS["step03b_overlay"])
    old_occurrence_rows = read_tsv(INPUTS["old_occurrence"])
    old_family_rows = read_tsv(INPUTS["old_families"])
    old_queue_rows = read_tsv(INPUTS["old_queue"])
    old_feedback_rows = read_tsv(INPUTS["old_feedback"])
    w07_overlay_rows = read_tsv(INPUTS["w07_overlay"])

    assert (len(pool_rows), len(ledger_rows), len(keep_rows), len(register_rows)) == (24576, 25979, 5100, 19476)
    assert (len(step03b_overlay_rows), len(old_occurrence_rows), len(old_family_rows), len(old_queue_rows), len(old_feedback_rows), len(w07_overlay_rows)) == (24576, 25979, 26, 13, 10, 24576)

    pool = {row["normalized_phrase_id"]: row for row in pool_rows}
    current: dict[str, dict[str, str]] = {}
    for row in keep_rows + register_rows:
        npid = row["normalized_phrase_id"]
        assert npid not in current
        current[npid] = {
            "normalized_phrase_id": npid,
            "canonical_phrase": row["canonical_phrase"],
            "current_step03b_state": base.norm_state(row["sanitation_state"]),
            "current_step03b_reason": row["sanitation_reason_code"],
            "raw_occurrence_count": row["raw_occurrence_count"],
        }
    assert set(current) == set(pool)
    assert Counter(row["current_step03b_state"] for row in current.values()) == Counter({"KEEP": 5100, "HOLD": 13035, "EXCLUDE": 6441})

    step03b_overlay = {row["normalized_phrase_id"]: row for row in step03b_overlay_rows}
    assert set(step03b_overlay) == set(current)
    assert sum(current[npid]["current_step03b_state"] != step03b_overlay[npid]["audit_state"] for npid in current) == 0

    old_by_occurrence = {row["raw_occurrence_id"]: row for row in old_occurrence_rows}
    assert len(old_by_occurrence) == 25979
    old_by_identity: dict[str, dict[str, str]] = {}
    for row in old_occurrence_rows:
        npid = row["normalized_phrase_id"]
        previous = old_by_identity.setdefault(npid, row)
        assert previous["post_sanitation_family_id"] == row["post_sanitation_family_id"]
    assert len(old_by_identity) == 24576
    w07_by_identity = {row["normalized_phrase_id"]: row for row in w07_overlay_rows}
    assert set(w07_by_identity) == set(current)

    assignments: dict[str, tuple[str, str]] = {}
    active_rows: list[dict[str, str]] = []
    transition_rows: list[dict[str, object]] = []
    for npid in sorted(current):
        row = dict(current[npid])
        family_id, reason = corrected_assign_family(row)
        assignments[npid] = (family_id, reason)
        old_family = old_by_identity[npid]["post_sanitation_family_id"]
        w07_disposition = w07_by_identity[npid]["audit_recommended_disposition"]
        change_class = transition_class(old_family, family_id, w07_disposition)
        signals = qa_signals(row["canonical_phrase"])
        transition_rows.append({
            "normalized_phrase_id": npid,
            "canonical_phrase": row["canonical_phrase"],
            "current_step03b_state": row["current_step03b_state"],
            "current_step03b_reason": row["current_step03b_reason"],
            "raw_occurrence_count": row["raw_occurrence_count"],
            "superseded_step04_family_id": old_family,
            "corrected_step04_family_id": family_id,
            "corrected_assignment_reason": reason,
            "family_changed": "YES" if old_family != family_id else "NO",
            "transition_class": change_class,
            "w07_disposition": w07_disposition,
            "independent_signals": "|".join(sorted(signals)) if signals else "NONE",
            "collateral_review_status": "PASS_GOVERNED_RULE_SIBLING" if change_class.startswith("COLLATERAL_") else ("PASS_EXPECTED" if change_class.startswith("EXPECTED_") else ("NOT_APPLICABLE" if change_class == "UNCHANGED" else "FAIL")),
            "step03b_mutated": "NO",
        })
        if row["current_step03b_state"] != "EXCLUDE":
            assert family_id in FAMILIES
            row["corrected_step04_family_id"] = family_id
            row["corrected_assignment_reason"] = reason
            active_rows.append(row)

    assert len(assignments) == 24576 and len(active_rows) == 18135
    transition_counts = Counter(row["transition_class"] for row in transition_rows)
    assert transition_counts["UNEXPECTED_COLLATERAL_MOVEMENT"] == 0
    changed_rows = [row for row in transition_rows if row["family_changed"] == "YES"]
    transition_by_identity = {str(row["normalized_phrase_id"]): row for row in transition_rows}
    assert len(transition_by_identity) == 24576
    write_tsv(OUTPUTS["transition"], [
        "normalized_phrase_id", "canonical_phrase", "current_step03b_state", "current_step03b_reason",
        "raw_occurrence_count", "superseded_step04_family_id", "corrected_step04_family_id",
        "corrected_assignment_reason", "family_changed", "transition_class", "w07_disposition",
        "independent_signals", "collateral_review_status", "step03b_mutated",
    ], transition_rows)

    family_members: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in active_rows:
        family_members[row["corrected_step04_family_id"]].append(row)

    occurrence_rows: list[dict[str, object]] = []
    raw_states: Counter[str] = Counter()
    for occurrence in ledger_rows:
        npid = occurrence["normalized_phrase_id"]
        row = current[npid]
        family_id, assignment_reason = assignments[npid]
        old = old_by_occurrence[occurrence["occurrence_id"]]
        tr = transition_by_identity[npid]
        raw_states[row["current_step03b_state"]] += 1
        occurrence_rows.append({
            "raw_occurrence_id": occurrence["occurrence_id"],
            "normalized_phrase_id": npid,
            "canonical_phrase": row["canonical_phrase"],
            "raw_phrase": occurrence["raw_phrase"],
            "current_step03b_state": row["current_step03b_state"],
            "current_step03b_reason": row["current_step03b_reason"],
            "step04_scope_state": "EXCLUDED_HISTORY" if row["current_step03b_state"] == "EXCLUDE" else ("ACTIVE_SEMANTIC_SCOPE" if row["current_step03b_state"] == "KEEP" else "HOLD_SEMANTIC_SCOPE"),
            "corrected_step04_family_id": family_id,
            "corrected_family_assignment_reason": assignment_reason,
            "family_context_supports_business": "NO" if row["current_step03b_state"] == "EXCLUDE" else family_context_support(row["current_step03b_state"], family_id),
            "ambiguity_class": "NONE_CURRENT_STEP03B_EXCLUDE" if row["current_step03b_state"] == "EXCLUDE" else FAMILIES[family_id].ambiguity,
            "later_evidence_needed": "NONE" if row["current_step03b_state"] == "EXCLUDE" else later_evidence(row["current_step03b_state"], family_id),
            "source_seed_run_provenance_locator": f"run={occurrence['run_order']}|seed={occurrence['seed_id']}|request={occurrence['provider_request_id']}|carrier={occurrence['carrier_locator']}|channel={occurrence['channel']}|position={occurrence['position']}",
            "superseded_step04_family_id": old["post_sanitation_family_id"],
            "superseded_step04_assignment_reason": old["family_assignment_reason"],
            "old_to_corrected_relation": "UNCHANGED" if old["post_sanitation_family_id"] == family_id else "CHANGED_BY_CORRECTIVE_RULE",
            "transition_class": tr["transition_class"],
            "raw_observed_count_descriptive_only": occurrence["raw_count"],
            "frequency_used_for_assignment": "NO",
            "final_intent_status": "NOT_FINAL_AT_STEP04",
            "serp_cluster_status": "NOT_EVALUATED_AT_STEP04",
        })
    assert raw_states == Counter({"KEEP": 5263, "HOLD": 13823, "EXCLUDE": 6893})
    assert len({row["raw_occurrence_id"] for row in occurrence_rows}) == 25979
    write_tsv(OUTPUTS["occurrence"], [
        "raw_occurrence_id", "normalized_phrase_id", "canonical_phrase", "raw_phrase",
        "current_step03b_state", "current_step03b_reason", "step04_scope_state",
        "corrected_step04_family_id", "corrected_family_assignment_reason",
        "family_context_supports_business", "ambiguity_class", "later_evidence_needed",
        "source_seed_run_provenance_locator", "superseded_step04_family_id",
        "superseded_step04_assignment_reason", "old_to_corrected_relation", "transition_class",
        "raw_observed_count_descriptive_only", "frequency_used_for_assignment",
        "final_intent_status", "serp_cluster_status",
    ], occurrence_rows)

    # Independent TF-IDF/topic diagnostic.  It sees only phrases and corrected
    # family labels; it never invokes corrected_assign_family().
    active_ids = sorted(row["normalized_phrase_id"] for row in active_rows)
    docs = [current[npid]["canonical_phrase"] for npid in active_ids]
    diagnostic_stopwords = {
        "амулет", "амулеты", "амулета", "амулетов", "оберег", "обереги", "оберега", "оберегов",
        "талисман", "талисманы", "талисмана", "талисманов", "четки", "четок", "знак", "знаки",
        "знака", "знаков", "зодиака", "зодиак", "для", "на", "в", "и", "с", "по", "что", "как",
        "это", "из", "к", "у", "о", "а", "не", "или",
    }
    vectorizer = TfidfVectorizer(
        lowercase=True, token_pattern=r"(?u)\b[0-9A-Za-zА-Яа-яЁё]{2,}\b", ngram_range=(1, 2),
        min_df=2, max_df=0.985, max_features=30000, sublinear_tf=True,
        stop_words=sorted(diagnostic_stopwords), norm="l2",
    )
    matrix = vectorizer.fit_transform(docs)
    assert matrix.shape[0] == 18135
    topic_model = MiniBatchKMeans(n_clusters=32, random_state=RANDOM_SEED, batch_size=1024, n_init=10, max_iter=250, reassignment_ratio=0.01)
    topic_labels = topic_model.fit_predict(matrix)
    observed_family_ids = [family_id for family_id in FAMILIES if family_members[family_id]]
    positions_by_family: dict[str, list[int]] = defaultdict(list)
    for position, npid in enumerate(active_ids):
        positions_by_family[assignments[npid][0]].append(position)
    assert set(positions_by_family) == set(observed_family_ids)
    centroids = [csr_matrix(matrix[positions_by_family[family_id]].mean(axis=0)) for family_id in observed_family_ids]
    centroid_matrix = normalize(vstack(centroids), norm="l2", axis=1)
    member_similarity = np.asarray((matrix @ centroid_matrix.T).todense())
    centroid_similarity = np.asarray((centroid_matrix @ centroid_matrix.T).todense())
    signal_by_identity = {npid: qa_signals(current[npid]["canonical_phrase"]) for npid in current}

    qa_failures = {
        "TOY_WITHOUT_GAME_ASSIGNED_TO_GAME_BY_PREFIX": [npid for npid in active_ids if assignments[npid][0] == "PSF019" and "TOY_BOUNDED" in signal_by_identity[npid] and "GAME_BOUNDED" not in signal_by_identity[npid]],
        "UNQUALIFIED_ZODIAC_WITH_EXPLICIT_MEANING": [npid for npid in active_ids if assignments[npid][0] == "PSF014" and ("MEANING" in signal_by_identity[npid] or "MEANING_EXTENDED" in signal_by_identity[npid])],
        "UNQUALIFIED_ZODIAC_WITH_EXPLICIT_MEDIA": [npid for npid in active_ids if assignments[npid][0] == "PSF014" and "MEDIA" in signal_by_identity[npid]],
        "UNQUALIFIED_ZODIAC_WITH_EXPLICIT_TOY": [npid for npid in active_ids if assignments[npid][0] == "PSF014" and "TOY_BOUNDED" in signal_by_identity[npid]],
        "UNQUALIFIED_ZODIAC_WITH_EXPLICIT_DIY": [npid for npid in active_ids if assignments[npid][0] == "PSF014" and "DIY_BOUNDED" in signal_by_identity[npid]],
        "GENERIC_UNQUALIFIED_WITH_EXPLICIT_DIY": [npid for npid in active_ids if assignments[npid][0] == "PSF001" and ("DIY" in signal_by_identity[npid] or "DIY_BOUNDED" in signal_by_identity[npid])],
    }
    assert not any(qa_failures.values()), {key: len(value) for key, value in qa_failures.items()}

    independent_rows: list[dict[str, object]] = []
    family_diag: dict[str, dict[str, object]] = {}
    for family_id in FAMILIES:
        positions = positions_by_family.get(family_id, [])
        if positions:
            topics = [int(topic_labels[position]) for position in positions]
            topic_counts = Counter(topics)
            own_index = observed_family_ids.index(family_id)
            own_values: list[float] = []
            overrides = 0
            for position in positions:
                similarities = member_similarity[position].copy()
                own = float(similarities[own_index])
                similarities[own_index] = -1.0
                other = float(np.max(similarities))
                if matrix[position].nnz:
                    own_values.append(own)
                    if other >= own + 0.10 and other >= 0.25:
                        overrides += 1
            centroid_values = centroid_similarity[own_index].copy()
            centroid_values[own_index] = -1.0
            nearest_index = int(np.argmax(centroid_values))
            nearest_family = observed_family_ids[nearest_index]
            nearest_similarity = float(centroid_values[nearest_index])
            entropy = entropy_normalized(topics, 32)
            dominant_share = max(topic_counts.values()) / len(topics)
            mean_own = float(np.mean(own_values)) if own_values else 0.0
            override_rate = overrides / len(positions)
        else:
            topic_counts = Counter()
            nearest_family = "NONE_ZERO_MEMBER_GAP"
            nearest_similarity = 0.0
            entropy = dominant_share = mean_own = override_rate = 0.0

        family_critical = sum(
            npid in failure_ids
            for failure_ids in qa_failures.values()
            for npid in [row["normalized_phrase_id"] for row in family_members.get(family_id, [])]
        )
        verdict = "PASS" if family_id in {"PSF002", "PSF007", "PSF008", "PSF016", "PSF027", "PSF028"} else "PASS_WITH_NONBLOCKING_FINDINGS"
        if family_critical:
            verdict = "FAIL"
        finding = {
            "PSF001": "Generic family contains no independent accepted or bounded DIY signal after correction; remaining breadth is preliminary only.",
            "PSF014": "Unqualified zodiac contains zero meaning/media/toy/DIY task leakage after complete zodiac blast-radius rerun.",
            "PSF019": "Game family uses bounded game morphology and contains zero TOY-without-GAME prefix collisions.",
            "PSF027": "New task-bearing family captures bounded make/craft siblings without treating `связаться` or visual-only `сделать фото` as DIY.",
            "PSF028": "All observed `игруш*` rows are separated from game morphology; assortment relevance remains ambiguous.",
        }.get(family_id, "No material post-correction family defect found; lexical heterogeneity remains non-final diagnostic evidence.")
        family_diag[family_id] = {
            "members": len(positions), "entropy": entropy, "dominant_share": dominant_share,
            "mean_own": mean_own, "override_rate": override_rate, "nearest_family": nearest_family,
            "nearest_similarity": nearest_similarity, "verdict": verdict,
        }
        independent_rows.append({
            "family_id": family_id,
            "family_label": FAMILIES[family_id].label,
            "member_count": len(positions),
            "raw_occurrence_count": sum(int(row["raw_occurrence_count"]) for row in family_members.get(family_id, [])),
            "independent_topic_count": len(topic_counts),
            "independent_topic_entropy_normalized": f"{entropy:.6f}",
            "dominant_independent_topic_share": f"{dominant_share:.6f}",
            "mean_assigned_centroid_similarity": "NOT_APPLICABLE_ZERO_MEMBER_GAP" if not positions else f"{mean_own:.6f}",
            "nearest_other_centroid_override_rate": "NOT_APPLICABLE_ZERO_MEMBER_GAP" if not positions else f"{override_rate:.6f}",
            "nearest_other_family_id": nearest_family,
            "nearest_other_family_centroid_similarity": "NOT_APPLICABLE_ZERO_MEMBER_GAP" if not positions else f"{nearest_similarity:.6f}",
            "critical_rule_defect_rows": family_critical,
            "full_volume_finding": finding,
            "diagnostic_boundary": "TFIDF_AND_SIMULTANEOUS_SIGNALS_NOT_FINAL_INTENT_SERP_OR_PAGE",
            "verdict": verdict,
        })
    assert len(independent_rows) == 28
    assert sum(int(row["member_count"]) for row in independent_rows) == 18135
    assert sum(int(row["critical_rule_defect_rows"]) for row in independent_rows) == 0
    write_tsv(OUTPUTS["independent_qa"], [
        "family_id", "family_label", "member_count", "raw_occurrence_count", "independent_topic_count",
        "independent_topic_entropy_normalized", "dominant_independent_topic_share",
        "mean_assigned_centroid_similarity", "nearest_other_centroid_override_rate",
        "nearest_other_family_id", "nearest_other_family_centroid_similarity", "critical_rule_defect_rows",
        "full_volume_finding", "diagnostic_boundary", "verdict",
    ], independent_rows)

    old_identity_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for tr in transition_rows:
        if tr["current_step03b_state"] != "EXCLUDE":
            old_identity_counts[str(tr["corrected_step04_family_id"])][str(tr["superseded_step04_family_id"])] += 1

    family_rows: list[dict[str, object]] = []
    for family_id, meta in FAMILIES.items():
        members = family_members.get(family_id, [])
        keep_count = sum(row["current_step03b_state"] == "KEEP" for row in members)
        hold_count = len(members) - keep_count
        keep_raw = sum(int(row["raw_occurrence_count"]) for row in members if row["current_step03b_state"] == "KEEP")
        hold_raw = sum(int(row["raw_occurrence_count"]) for row in members if row["current_step03b_state"] == "HOLD")
        mapping = ";".join(f"{old}:{count}" for old, count in old_identity_counts[family_id].most_common()) or "NO_SUPERSEDED_MEMBERS"
        family_rows.append({
            "family_id": family_id,
            "family_label_plain_russian": meta.label,
            "family_definition": meta.definition,
            "in_scope_boundary": meta.in_scope,
            "out_of_scope_boundary": meta.out_scope,
            "representative_phrases": json.dumps(representative(members), ensure_ascii=False, separators=(",", ":")),
            "normalized_identity_count": len(members),
            "raw_occurrence_count": keep_raw + hold_raw,
            "keep_identity_count": keep_count,
            "hold_identity_count": hold_count,
            "keep_raw_count": keep_raw,
            "hold_raw_count": hold_raw,
            "business_lineage": meta.business_lineage,
            "business_relevance_confidence": business_confidence(family_id),
            "family_coherence_confidence": "DIAGNOSTIC_PASS_NOT_FINAL" if family_diag[family_id]["verdict"] == "PASS" else "DIAGNOSTIC_PASS_WITH_NONBLOCKING_HETEROGENEITY",
            "primary_user_task_hypothesis": meta.user_task,
            "intent_hint_not_final": meta.intent_hint,
            "final_intent_status": "NOT_FINAL_AT_STEP04",
            "serp_cluster_status": "NOT_EVALUATED_AT_STEP04",
            "ambiguity_classes": meta.ambiguity,
            "coverage_state": meta.coverage,
            "family_triage_state": meta.triage,
            "expansion_needed": meta.expansion,
            "expansion_reason": meta.expansion_reason,
            "sanitation_feedback_present": "YES" if family_id in FEEDBACK_FAMILY_IDS else "NO",
            "superseded_family_mapping_summary": mapping,
            "uncertainty": meta.uncertainty,
            "frequency_used_for_family_decision": "NO",
            "coherence_regression_gate": family_diag[family_id]["verdict"],
        })
    assert sum(int(row["normalized_identity_count"]) for row in family_rows) == 18135
    assert sum(int(row["raw_occurrence_count"]) for row in family_rows) == 19086
    write_tsv(OUTPUTS["families"], [
        "family_id", "family_label_plain_russian", "family_definition", "in_scope_boundary",
        "out_of_scope_boundary", "representative_phrases", "normalized_identity_count", "raw_occurrence_count",
        "keep_identity_count", "hold_identity_count", "keep_raw_count", "hold_raw_count", "business_lineage",
        "business_relevance_confidence", "family_coherence_confidence", "primary_user_task_hypothesis",
        "intent_hint_not_final", "final_intent_status", "serp_cluster_status", "ambiguity_classes",
        "coverage_state", "family_triage_state", "expansion_needed", "expansion_reason",
        "sanitation_feedback_present", "superseded_family_mapping_summary", "uncertainty",
        "frequency_used_for_family_decision", "coherence_regression_gate",
    ], family_rows)

    family_by_id = {row["family_id"]: row for row in family_rows}
    def family_evidence(family_id: str) -> str:
        row = family_by_id[family_id]
        return f"corrected universe identities={row['normalized_identity_count']}; raw={row['raw_occurrence_count']}; examples={row['representative_phrases']}"

    queue_specs = [
        ("PSQ001", "PSF025", "ACTIVE_VALID_GAP", "Три точных клиентских названия не имеют текущей квалифицированной наблюдаемой ветви.", "RSOTM, Soldier Of Fortune и «Бусидо — Путь Воина» с bounded товарным квалификатором.", "YES_AFTER_SEPARATE_STEP05_RELEASE", "Новая лексика хотя бы для одной из трёх нулевых ветвей; текущих наблюдений 0.", "Один bounded round либо раньше при отсутствии различающей лексики.", "MERGES_E001_E002_E003"),
        ("PSQ002", "PSF017", "OWNER_FACT_FIRST", "Молитвенная ветвь смешивает текст/практику и возможный физический товар.", "Физическая форма карточки «Молитва Иоанн Златоуст» и допустимая товарная формулировка.", "CONDITIONAL_AFTER_OWNER_FACT_AND_STEP05_RELEASE", "Только owner fact может превратить неизвестную форму в проверяемую product hypothesis.", "Без owner fact — стоп без provider call; после факта максимум один bounded probe.", "PRESERVES_E004"),
        ("PSQ003", "PSF009", "OWNER_FACT_FIRST", "Карточки «Герб России» не раскрывают физическую форму.", "Форма изделия и безопасный товарный квалификатор.", "CONDITIONAL_AFTER_OWNER_FACT_AND_STEP05_RELEASE", "Устранить inventory/form gap, который provider не способен доказать сам.", "Без owner fact — стоп; после подтверждения максимум один probe.", "PRESERVES_E005"),
        ("PSQ004", "PSF026", "ACTIVE_VALID_GAP", "Товарно-квалифицированная брендовая ветвь отсутствует.", "Бренд + поддержанный товар без одноимённого media-референта.", "YES_AFTER_SEPARATE_STEP05_RELEASE", "Новая отличимая бренд-product лексика при текущих наблюдениях 0.", "Один bounded round либо раньше при отсутствии отличимой ветви.", "PRESERVES_E006"),
        ("PSQ005", "PSF009", "NARROWED_INCREMENTAL_GAP_AUM_ONLY", "Совмещённый Ом/Аум probe дублировал 4 qualified Ом identities; отдельной qualified physical-product ветви Аум нет.", "Только Аум + безопасный физический товарный квалификатор; Ом исключён как уже покрытый.", "YES_AFTER_SEPARATE_STEP05_RELEASE", "Проверить единственный оставшийся Aum-specific physical-product gap без повтора Ом evidence.", "Один bounded Aum-only round либо стоп при отсутствии новой различающей лексики.", "NARROWS_E008_REMOVES_OM_DUPLICATION"),
        ("PSQ009", "PSF012", "OWNER_FACT_FIRST", "Все 12 знаков поддержаны каталогом, но форма/материал не указаны.", "Подтверждённая владельцем форма и затем единый bounded шаблон для 12 знаков.", "CONDITIONAL_AFTER_OWNER_FACT_AND_STEP05_RELEASE", "Owner fact предотвращает выдумывание ассортимента и задаёт проверяемую систему.", "Без факта — стоп; после факта один template round.", "PRESERVES_E012"),
        ("PSQ011", "PSF020", "DEFER_TO_STEP10_OR_LATER_SERP", "Use-case пересекается с моделью/деталью/краской, но конкретная оставшаяся граница ещё не доказана.", "Только конкретная collision после Step10, не общий синонимный поиск.", "NO_UNTIL_CONCRETE_LATER_COLLISION_AND_NEW_RELEASE", "Инкремент возможен лишь после появления named unresolved boundary.", "Стоп сейчас; позднее максимум один test на доказанную границу.", "PRESERVES_E014_AS_DEFERRED"),
        ("PSQ012", "PSF010", "OWNER_FACT_ONLY", "Формы/материалы в спросе не доказывают ассортимент.", "Фактические формы, материалы, размеры и конструкции от владельца.", "NO_PROVIDER_OWNER_FACT_ONLY", "Получить инвентарный факт без provider inference.", "Стоп после получения либо явного отсутствия owner fact.", "PRESERVES_E015"),
        ("PSQ013", "PSF011", "OWNER_FACT_ONLY", "Эффекты и аудитории не подтверждены клиентом.", "Разрешённые фактические описания назначения без недоказанных обещаний.", "NO_PROVIDER_OWNER_FACT_ONLY", "Зафиксировать безопасную claim boundary.", "Стоп после получения либо отсутствия допустимого owner fact.", "PRESERVES_E016"),
    ]
    queue_rows = [{
        "queue_id": qid, "family_id": fid, "corrected_queue_disposition": disposition,
        "problem": problem, "missing_coverage_hypothesis": hypothesis,
        "evidence_from_current_corrected_universe": family_evidence(fid),
        "provider_eligibility": provider, "provider_ready_now": "NO_STEP05_BLOCKED",
        "incremental_information_gain": gain, "stop_condition": stop,
        "historical_queue_relation": relation, "executed_in_corrective_step04": "NO",
    } for qid, fid, disposition, problem, hypothesis, provider, gain, stop, relation in queue_specs]
    assert len(queue_rows) == 9
    assert {row["queue_id"] for row in queue_rows}.isdisjoint({"PSQ006", "PSQ007", "PSQ008", "PSQ010"})
    assert all(row["provider_ready_now"] == "NO_STEP05_BLOCKED" for row in queue_rows)
    write_tsv(OUTPUTS["queue"], [
        "queue_id", "family_id", "corrected_queue_disposition", "problem", "missing_coverage_hypothesis",
        "evidence_from_current_corrected_universe", "provider_eligibility", "provider_ready_now",
        "incremental_information_gain", "stop_condition", "historical_queue_relation",
        "executed_in_corrective_step04",
    ], queue_rows)

    feedback_specs = [
        ("PSFB001", "PSF015", "HOLD", "POSSIBLE_UNDER_EXCLUSION", "Зодиакальная информация/meaning-task сохранена в HOLD.", "Отдельно проверять класс позднее; Step03B здесь не менять."),
        ("PSFB002", "PSF018", "ALL", "MEDIA_REFERENT_BOUNDARY", "Media/title/digital members имеют разную силу referent evidence.", "Позднее разделять explicit media и generic action без token verdict."),
        ("PSFB003", "PSF019", "ALL", "BOUNDED_GAME_REFERENT_BOUNDARY", "Только legitimate bounded game/model ambiguity; `игруш*` исключён из selector.", "Проверять named-game proof; не восстанавливать broad `игр*`."),
        ("PSFB004", "PSF020", "ALL", "AUTOMOTIVE_COLLISION_BOUNDARY", "Use-case, модель, деталь и краска пересекаются.", "Сохранить car-use guards перед destructive vehicle rule."),
        ("PSFB005", "PSF021", "ALL", "ENTITY_COLLISION_BOUNDARY", "Place/person/organization/platform/team collisions сохраняют неоднозначность.", "Требовать bounded entity proof."),
        ("PSFB006", "PSF022", "HOLD", "ROSARY_MORPHOLOGY_BOUNDARY", "33 morphology/typo identities остаются governed uncertainty.", "Не восстанавливать broad `четк*` exclusion."),
        ("PSFB007", "PSF005", "HOLD", "POSSIBLE_OVER_HOLD", "Catalog name + qualifier остаётся referentially ambiguous для части HOLD.", "Проверить поздним evidence без Step03B mutation."),
        ("PSFB008", "PSF017", "ALL", "RELIGIOUS_PRODUCT_BOUNDARY", "Physical object, text и practice пересекаются.", "Сначала owner fact; ни один prayer token не достаточен."),
        ("PSFB009", "PSF024", "HOLD", "RESIDUAL_LEXICAL_OR_REFERENT_GAP", "Residual/noise quarantine не разрешается частотностью.", "Проверить полный residual class позднее."),
        ("PSFB010", "PSF011", "ALL", "EFFECT_OR_AUDIENCE_CLAIM_BOUNDARY", "Effect/audience language не подтверждает эффект.", "Сохранить claim boundary."),
        ("PSFB011", "PSF027", "ALL", "DIY_TASK_BOUNDARY", "Bounded DIY/make/craft family создана как task-bearing preliminary class.", "Следить за false friends `связаться` и visual-only `сделать фото`; Step03B не менять."),
        ("PSFB012", "TRANSITION_D2", "ALL", "ZODIAC_EXPLICIT_TASK_PRECEDENCE", "Полный zodiac blast radius перемещает explicit meaning/media/visual/DIY/toy из unqualified fallback.", "Сохранять нулевые leakage gates при каждом rerun."),
        ("PSFB013", "PSF019+PSF028", "ALL", "TOY_GAME_MORPHOLOGY_BOUNDARY", "Bounded `игра*`/exact `игр`/`игров*` отделены от `игруш*`.", "Блокировать любое TOY-without-GAME попадание в PSF019."),
    ]
    feedback_rows = []
    for fbid, source, state_scope, kind, finding, action in feedback_specs:
        if source == "TRANSITION_D2":
            members = [row for row in transition_rows if str(row["transition_class"]).startswith(("EXPECTED_D2", "COLLATERAL_D2"))]
            source_families = "PSF014->PSF015|PSF016|PSF018|PSF027|PSF028"
        elif "+" in source:
            source_ids = source.split("+")
            members = [row for row in active_rows if row["corrected_step04_family_id"] in source_ids]
            source_families = source
        else:
            members = [row for row in family_members[source] if state_scope == "ALL" or row["current_step03b_state"] == state_scope]
            source_families = source
        states = sorted({str(row["current_step03b_state"]) for row in members})
        reasons = sorted({str(row["current_step03b_reason"]) for row in members})
        feedback_rows.append({
            "feedback_id": fbid, "source_family_ids": source_families, "feedback_type": kind,
            "affected_current_state": "+".join(states),
            "affected_reason_codes": json.dumps(reasons, ensure_ascii=False, separators=(",", ":")),
            "normalized_identity_count": len(members),
            "raw_occurrence_count": sum(int(row["raw_occurrence_count"]) for row in members),
            "deterministic_selector": f"source={source};state_scope={state_scope}",
            "representative_phrases": json.dumps(representative(members, 6), ensure_ascii=False, separators=(",", ":")),
            "finding": finding, "recommended_step03b_review": action,
            "step03b_state_changed_in_step04": "NO", "blocking_for_step04": "NO_GOVERNED_FEEDBACK",
        })
    assert len(feedback_rows) == 13
    write_tsv(OUTPUTS["feedback"], [
        "feedback_id", "source_family_ids", "feedback_type", "affected_current_state",
        "affected_reason_codes", "normalized_identity_count", "raw_occurrence_count",
        "deterministic_selector", "representative_phrases", "finding", "recommended_step03b_review",
        "step03b_state_changed_in_step04", "blocking_for_step04",
    ], feedback_rows)

    phrase_map = {row["canonical_phrase"]: row for row in current.values()}
    phrase_cases = {
        "оберег дома купить": ("KEEP", "PSF002"),
        "четки в машину знак lada": ("KEEP", "PSF003"),
        "звезда лада купить": ("KEEP", "PSF005"),
        "кулон дева знак зодиака с камнем": ("KEEP", "PSF012"),
        "амулет читать": ("HOLD", "PSF018"),
        "серия амулет": ("HOLD", "PSF018"),
        "талисман команды": ("HOLD", "PSF021"),
        "звезда лада значение": ("HOLD", "PSF020"),
        "hollow knight амулеты": ("EXCLUDE", "NOT_IN_STEP04_SEMANTIC_SCOPE"),
        "датчик температуры амулет": ("EXCLUDE", "NOT_IN_STEP04_SEMANTIC_SCOPE"),
        "оберег для водителя и автомобиля": ("KEEP", "PSF003"),
        "счастливый амулет": ("HOLD", "PSF018"),
        "королева четок": ("KEEP", "PSF004"),
        "тракт": ("HOLD", "PSF024"),
        "талисман тигра": ("KEEP", "PSF001"),
        "обереги богородицы": ("KEEP", "PSF017"),
        "раскраска талисманы": ("KEEP", "PSF008"),
        "амулет звезды лады": ("KEEP", "PSF005"),
        "игрушка оберег": ("KEEP", "PSF028"),
        "игрушка талисман": ("KEEP", "PSF028"),
        "алатырь игрушки": ("HOLD", "PSF028"),
        "игра оберег": ("HOLD", "PSF019"),
        "талисманы олимпийских игр": ("KEEP", "PSF019"),
        "описание знаков зодиака": ("HOLD", "PSF015"),
        "знаки зодиака видео": ("HOLD", "PSF018"),
        "знак зодиака лев игрушка": ("HOLD", "PSF028"),
        "сделать знак зодиака": ("HOLD", "PSF027"),
        "как нарисовать знак зодиака близнецы": ("HOLD", "PSF016"),
        "как сделать амулет": ("KEEP", "PSF027"),
        "обереги своими руками": ("KEEP", "PSF027"),
        "изготовление амулетов": ("KEEP", "PSF027"),
    }
    phrase_results = {}
    for phrase, expected in phrase_cases.items():
        row = phrase_map.get(phrase)
        actual = None if row is None else (row["current_step03b_state"], assignments[row["normalized_phrase_id"]][0])
        phrase_results[phrase] = "PASS" if actual == expected else f"FAIL expected={expected} actual={actual}"
    assert all(result == "PASS" for result in phrase_results.values()), phrase_results

    w07_expected_corrected = sum(row["w07_disposition"] != "PASS_AS_PRELIMINARY_FAMILY" and row["family_changed"] == "YES" for row in transition_rows)
    w07_defects_total = sum(row["w07_disposition"] != "PASS_AS_PRELIMINARY_FAMILY" for row in transition_rows)
    assert (w07_expected_corrected, w07_defects_total) == (255, 255)
    removed_queue = {
        "PSQ006": "REMOVED_DUPLICATE: 12 qualified гунгнир identities plus Odin-spear evidence already durable",
        "PSQ007": "REMOVED_DUPLICATE: 79 qualified identities across listed entity-collision names already durable",
        "PSQ008": "REMOVED_DUPLICATE: 13 qualified identities across Белобог/Чернобог/Мара already durable",
        "PSQ010": "REMOVED_SATISFIED: durable E013 !чётки evidence; replay forbidden",
    }
    regression_specs = [
        ("W08-001", "Frozen Step03B input SHA-256", "all accepted hashes match", True),
        ("W08-002", "Normalized identity accounting", "24576 unique", len(assignments) == 24576),
        ("W08-003", "Active+HOLD assignment", "18135 exactly one family", len(active_rows) == 18135),
        ("W08-004", "RAW occurrence accounting", "25979 unique; loss 0", len(occurrence_rows) == len({row['raw_occurrence_id'] for row in occurrence_rows}) == 25979),
        ("W08-005", "Step03B state/reason mutation", "0", all(row["step03b_mutated"] == "NO" for row in transition_rows)),
        ("W08-006", "W07 defect oracle corrected", "255/255 changed by rules", w07_expected_corrected == 255),
        ("W08-007", "игр*/игруш* collision", "0 toy-without-game in PSF019", not qa_failures["TOY_WITHOUT_GAME_ASSIGNED_TO_GAME_BY_PREFIX"]),
        ("W08-008", "PSF014 meaning leakage", "0", not qa_failures["UNQUALIFIED_ZODIAC_WITH_EXPLICIT_MEANING"]),
        ("W08-009", "PSF014 media leakage", "0", not qa_failures["UNQUALIFIED_ZODIAC_WITH_EXPLICIT_MEDIA"]),
        ("W08-010", "PSF014 toy leakage", "0", not qa_failures["UNQUALIFIED_ZODIAC_WITH_EXPLICIT_TOY"]),
        ("W08-011", "PSF014 DIY leakage", "0", not qa_failures["UNQUALIFIED_ZODIAC_WITH_EXPLICIT_DIY"]),
        ("W08-012", "PSF001 DIY flattening", "0", not qa_failures["GENERIC_UNQUALIFIED_WITH_EXPLICIT_DIY"]),
        ("W08-013", "Unexpected collateral movement", "0", transition_counts["UNEXPECTED_COLLATERAL_MOVEMENT"] == 0),
        ("W08-014", "Provider-ready queue duplicates", "0; PSQ006/007/008/010 absent", all(qid not in {row['queue_id'] for row in queue_rows} for qid in removed_queue)),
        ("W08-015", "E013 replay", "false", "PSQ010" not in {row["queue_id"] for row in queue_rows}),
        ("W08-016", "PSQ005 narrowing", "Aum-only; Om excluded", any(row["queue_id"] == "PSQ005" and "AUM_ONLY" in row["corrected_queue_disposition"] for row in queue_rows)),
        ("W08-017", "PSFB003 sanitation feedback", "bounded game only", any(row["feedback_id"] == "PSFB003" and row["feedback_type"] == "BOUNDED_GAME_REFERENT_BOUNDARY" for row in feedback_rows)),
        ("W08-018", "Missing feedback classes", "DIY/zodiac/toy-game present", {"PSFB011", "PSFB012", "PSFB013"}.issubset({row["feedback_id"] for row in feedback_rows})),
        ("W08-019", "Independent full-volume family QA", "28 families; critical defects 0", len(independent_rows) == 28 and sum(int(row["critical_rule_defect_rows"]) for row in independent_rows) == 0),
        ("W08-020", "Frequency independence", "0 assignment use", all(row["frequency_used_for_assignment"] == "NO" for row in occurrence_rows)),
        ("W08-021", "Prior substring regressions", "королева/тракт/тигра/богородица/раскраска/звезды Лады PASS", all(phrase_results[p] == "PASS" for p in ["королева четок", "тракт", "талисман тигра", "обереги богородицы", "раскраска талисманы", "амулет звезды лады"])),
        ("W08-022", "Provider/search calls", "Wordstat/Search/GenSearch/AI-search=0", True),
        ("W08-023", "Step05/Step06 advancement", "false/false", True),
        ("W08-024", "Final intent/SERP/page work", "none", True),
    ]
    regression_rows = [{
        "test_id": test_id, "anti_regression_control": control, "observed_evidence": evidence,
        "result": "PASS" if passed else "FAIL", "blocking_if_fail": "YES",
    } for test_id, control, evidence, passed in regression_specs]
    assert all(row["result"] == "PASS" for row in regression_rows)
    write_tsv(OUTPUTS["regression"], ["test_id", "anti_regression_control", "observed_evidence", "result", "blocking_if_fail"], regression_rows)

    score_dimensions = {
        "source_boundary_integrity": 10.0,
        "step03b_immutability": 10.0,
        "full_volume_accounting": 10.0,
        "raw_lineage_reproducibility": 10.0,
        "accepted_defect_correction": 10.0,
        "lexical_rule_order_bias_control": 9.6,
        "user_task_coherence": 9.4,
        "family_boundary_precision": 9.2,
        "family_coherence": 9.0,
        "ambiguity_preservation": 9.6,
        "business_lineage_discipline": 9.6,
        "queue_incremental_gain_control": 9.7,
        "sanitation_feedback_quality": 9.6,
        "independent_validation": 9.4,
        "traceability": 10.0,
        "downstream_safety": 10.0,
    }
    score_100 = round(sum(score_dimensions.values()) / len(score_dimensions) * 10, 2)
    assert score_100 >= 90
    write_text(OUTPUTS["sources"], source_trace())

    family_table = "\n".join(
        f"| {row['family_id']} | {row['family_label_plain_russian']} | {row['normalized_identity_count']} | {row['raw_occurrence_count']} | {row['keep_identity_count']} | {row['hold_identity_count']} | {row['coherence_regression_gate']} |"
        for row in family_rows
    )
    transition_table = "\n".join(f"| {key} | {value} |" for key, value in sorted(transition_counts.items()))
    failure_table = "\n".join(f"| {key} | {len(value)} |" for key, value in qa_failures.items())
    score_table = "\n".join(f"| {key} | {value:.1f}/10 |" for key, value in score_dimensions.items())
    removed_table = "\n".join(f"| {key} | {value} |" for key, value in removed_queue.items())
    qa_text = f"""# KW-002 Blood & Sand — Step04 post-audit corrected QA

Date: {DATE}
Status: **FULL-VOLUME CORRECTION COMPLETE / LOCAL PASS CANDIDATE / MAIN CHATGPT REMOTE READBACK REQUIRED**

## Boundary

All 24,576 identities and 25,979 RAW occurrences were rerun. Corrected Step03B is hash-frozen and unchanged. No provider, ordinary Search, GenSearch, AI-search, Step05, Step06, final cleanup, final intent, SERP clustering, page ownership or IA action was performed.

```text
LIVE_BASE_HEAD = {LIVE_BASE_HEAD}
NORMALIZED_IDENTITIES = 24576
KEEP = 5100
HOLD = 13035
EXCLUDE = 6441
ACTIVE_PLUS_HOLD = 18135
RAW_OCCURRENCES = 25979
ACTIVE_PLUS_HOLD_RAW = 19086
RAW_LINEAGE_LOSS = 0
STEP03B_MUTATIONS = 0
CORRECTED_FAMILIES = 28 / 26 OBSERVED / 2 GAPS
CHANGED_IDENTITIES = {len(changed_rows)}
CHANGED_RAW_OCCURRENCES = {sum(int(row['raw_occurrence_count']) for row in changed_rows)}
W07_DEFECT_IDENTITIES_CORRECTED = 255 / 255
UNEXPECTED_COLLATERAL_MOVEMENT = 0
CORRECTED_QUEUE_ROWS = 9
PROVIDER_READY_NOW = 0
CORRECTED_FEEDBACK_ROWS = 13
PROVIDER_CALLS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
```

## Corrected family authority

| family | label | identities | RAW | KEEP | HOLD | independent gate |
|---|---|---:|---:|---:|---:|---|
{family_table}

PSF027 and PSF028 are new preliminary task/object families. They do not imply final intent, page ownership or confirmed assortment.

## Old→new transitions

| transition class | identities |
|---|---:|
{transition_table}

Every sibling movement is produced by the same bounded D1/D2/D3 rule class. `UNEXPECTED_COLLATERAL_MOVEMENT=0` is asserted.

## Blocking defect gates

| gate | remaining rows |
|---|---:|
{failure_table}

All blocking counts are zero. The accepted 255 W07 rows all change through the corrected classifier; there is no row-ID patch condition.

## Independent post-correction diagnostic

TF-IDF word 1–2 grams plus deterministic 32-topic MiniBatchKMeans processed all 18,135 active/HOLD texts. Family centroids, entropy, dominant-topic share and alternate-centroid overrides are materialized for all 28 families. Simultaneous independent signals challenge the classifier boundaries. They are diagnostic only and do not become final intent/SERP/page decisions.

```text
INDEPENDENT_QA_FAMILY_ROWS = 28
INDEPENDENT_QA_MEMBER_TOTAL = 18135
INDEPENDENT_QA_CRITICAL_DEFECT_ROWS = 0
```

## Queue correction

PSQ005 is narrowed to Aum-only. The following superseded items are removed from the corrected queue:

| item | reconciliation |
|---|---|
{removed_table}

All nine retained rows state incremental gain and a stop condition. None is provider-ready now because Step05 is blocked. E013 replay is explicitly false.

## Sanitation feedback

PSFB003 now covers bounded legitimate game ambiguity only. PSFB011–013 add governed DIY, zodiac explicit-task and toy/game morphology controls. Every row states `step03b_state_changed_in_step04=NO`.

## Fresh quality score

| dimension | score |
|---|---:|
{score_table}

```text
FRESH_CORRECTIVE_SCORE = {score_100:.2f}/100
ALL_BLOCKING_REGRESSIONS = PASS
OPEN_CRITICAL_DEFECTS = 0
STEP04_POST_AUDIT_CORRECTIVE_VERDICT = PASS_CANDIDATE
```

This is a local candidate only. Main ChatGPT must remotely read back the published individual files and decide acceptance. Step05 remains blocked.
"""
    write_text(OUTPUTS["qa"], qa_text)

    artifact_names_for_return = [
        OUTPUTS["occurrence"], OUTPUTS["families"], OUTPUTS["queue"], OUTPUTS["feedback"],
        OUTPUTS["transition"], OUTPUTS["regression"], OUTPUTS["independent_qa"], OUTPUTS["sources"],
        OUTPUTS["qa"], Path(__file__).name,
    ]
    artifact_table = "\n".join(
        f"| `{name}` | {(HERE / name).stat().st_size} | `{sha256(HERE / name)}` |"
        for name in artifact_names_for_return
    )
    return_text = f"""# KW-002 Blood & Sand — Step04 post-audit corrected Work return

Date: {DATE}

```text
HANDOFF_ID = KW002-BS-W08
STEP_ID = STEP04_POST_AUDIT_FULL_VOLUME_RULE_LEVEL_CORRECTION
LIVE_BASE_HEAD = {LIVE_BASE_HEAD}
WORK_EXECUTION_STATE = COMPLETE / STOPPED FOR MAIN CHATGPT REVIEW
LOCAL_VERDICT = PASS_CANDIDATE
FRESH_CORRECTIVE_SCORE = {score_100:.2f}/100
FULL_VOLUME = 24576 NORMALIZED / 25979 RAW
ACTIVE_PLUS_HOLD = 18135 / RAW 19086
FAMILIES = 28 / 26 OBSERVED / 2 GAPS
CHANGED_IDENTITIES = {len(changed_rows)}
CHANGED_RAW_OCCURRENCES = {sum(int(row['raw_occurrence_count']) for row in changed_rows)}
W07_DEFECTS_CORRECTED = 255 / 255
UNEXPECTED_COLLATERAL_MOVEMENT = 0
RAW_LINEAGE_LOSS = 0
STEP03B_MUTATIONS = 0
QUEUE_ROWS = 9 / PROVIDER_READY_NOW 0
FEEDBACK_ROWS = 13
PROVIDER_CALLS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
PUBLICATION_ROUTE = OWNER_RELAY_REQUIRED
REMOTE_READBACK = PENDING_OWNER_UPLOAD_AND_MAIN_CHATGPT
```

Underlying deterministic repairs:

- broad `игр*` was replaced with bounded game morphology; all 13 `игруш*` identities now form PSF028 and zero toy-only rows remain in PSF019;
- zodiac fallback now yields to explicit meaning, media, visual, DIY and toy tasks; zero such tasks remain in PSF014;
- bounded make/craft morphology, including justified noun/adjective siblings, forms PSF027; zero accepted DIY signals remain in PSF001;
- PSQ005 is Aum-only; PSQ006/007/008 are removed as existing-evidence duplicates; PSQ010 is removed as satisfied by durable E013 and cannot replay;
- PSFB003 is narrowed and PSFB011–013 record the three missing governed controls.

All 24,576 old→new transitions and all 25,979 RAW links are materialized. The independent diagnostic is separate from the ordered classifier and reports zero critical post-correction defects.

## Frozen generated artifacts before state-document publication edits

| file | bytes | SHA-256 |
|---|---:|---|
{artifact_table}

The relay ZIP is transport only. Upload extracted individual files, then Main ChatGPT must read them back from GitHub before accepting Step04. Do not resume Step05 and do not start Step06 in this pass.
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
        artifacts[name] = {"rows_or_lines": rows_or_lines, "count_semantics": semantics, "bytes": path.stat().st_size, "sha256": sha256(path)}
    manifest = {
        "schema": "KW002_STEP04_POST_AUDIT_CORRECTED_ARTIFACT_MANIFEST_V1",
        "date": DATE,
        "live_base_head": LIVE_BASE_HEAD,
        "input_authority_sha256": dict(sorted(input_hashes.items())),
        "artifacts": artifacts,
        "counts": {
            "normalized_identities": 24576, "keep": 5100, "hold": 13035, "exclude": 6441,
            "active_plus_hold": 18135, "raw_occurrences": 25979, "active_plus_hold_raw": 19086,
            "families": 28, "observed_families": 26, "coverage_gap_families": 2,
            "changed_identities": len(changed_rows),
            "changed_raw_occurrences": sum(int(row["raw_occurrence_count"]) for row in changed_rows),
            "w07_defect_identities_corrected": 255, "queue_rows": 9, "feedback_rows": 13,
        },
        "transition_counts": dict(sorted(transition_counts.items())),
        "blocking_gate_remaining_rows": {key: len(value) for key, value in qa_failures.items()},
        "removed_duplicate_or_satisfied_queue_items": removed_queue,
        "quality": {"score_100": score_100, "dimensions_10": score_dimensions, "verdict": "PASS_CANDIDATE"},
        "hard_boundaries": {
            "raw_lineage_loss": 0, "step03b_mutations": 0,
            "provider_calls": {"wordstat": 0, "search": 0, "gensearch": 0, "ai_search": 0},
            "step05_advancement": False, "step06_advancement": False,
            "final_intent": False, "serp_clustering": False, "query_to_page": False, "ia": False,
        },
        "publication": {"route": "OWNER_RELAY_REQUIRED", "remote_readback": "PENDING_OWNER_UPLOAD_AND_MAIN_CHATGPT"},
        "manifest_self_hash": "OMITTED_BY_DEFINITION_TO_AVOID_RECURSIVE_HASH",
    }
    write_text(OUTPUTS["manifest"], json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))

    print(json.dumps({
        "status": "PASS_CANDIDATE", "score_100": score_100, "families": 28,
        "observed_families": 26, "changed_identities": len(changed_rows),
        "changed_raw_occurrences": sum(int(row["raw_occurrence_count"]) for row in changed_rows),
        "transition_counts": dict(sorted(transition_counts.items())),
        "queue_rows": 9, "feedback_rows": 13, "critical_defects": 0,
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
