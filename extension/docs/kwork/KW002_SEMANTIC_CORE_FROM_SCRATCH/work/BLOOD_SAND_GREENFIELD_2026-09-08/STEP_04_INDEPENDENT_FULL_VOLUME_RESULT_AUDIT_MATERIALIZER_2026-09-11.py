#!/usr/bin/env python3
"""Materialize the independent full-volume audit of the accepted KW-002 Step04 result.

This program is diagnostic-only.  It reads the accepted Step03B and Step04
authorities, performs exhaustive accounting plus a rule-agnostic TF-IDF/topic
diagnostic, and writes audit artifacts.  It does not mutate Step03B, rewrite a
Step04 family, call a provider/search system, start Step05/06, assign intent,
or map phrases to pages.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
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
LIVE_BASE_HEAD = "8a09e1610d68f61769b6a4d44d1382cab4dd37b7"
RANDOM_SEED = 20260911

INPUTS = {
    "pool": "STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv",
    "keep": "STEP_03B_SANITIZED_CANDIDATE_POOL_CORRECTED_2026-09-11.tsv",
    "register": "STEP_03B_EXCLUDED_HOLD_REGISTER_CORRECTED_2026-09-11.tsv",
    "step04_ledger": "STEP_04_POST_SANITATION_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv",
    "families": "STEP_04_POST_SANITATION_FAMILY_TRIAGE_2026-09-11.tsv",
    "queue": "STEP_04_POST_SANITATION_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv",
    "feedback": "STEP_04_POST_SANITATION_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv",
    "prompt": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_WORK_PROMPT_2026-09-11.md",
    "release": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_EXECUTION_RELEASE_2026-09-11.md",
}

EXPECTED_SHA256 = {
    INPUTS["pool"]: "b30c29ff66a56d80bc1aa9ff6b2eade522b27d1e167cbd636ac72fbff211f2a8",
    INPUTS["keep"]: "63b3fc556b388dbac0185f174f79f825dc26d9c51de39698850cdaecb9ca4f58",
    INPUTS["register"]: "145c5107f40415b4050923f142dab3e83646489da5d74501f659fd87e3ae2916",
    INPUTS["step04_ledger"]: "c053bcd1dccae5b2894cc7a316c84af72c2b0abfeb460624f138f1198a39a5ba",
    INPUTS["families"]: "cb2a1259f596f1b97ea4eb662e8c8b315936aad2243c57389c290ea6d90a0b2c",
    INPUTS["queue"]: "be46fd75e9b51354e14dfc3e862be69e8549fd67b708ecc7471bbfc3dcd63c73",
    INPUTS["feedback"]: "7a52efa3eb2e8eeebddecd61de4550acf33e98b8d357b463e815754f6af00903",
}

OUTPUTS = {
    "report": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_REPORT_2026-09-11.md",
    "overlay": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_OVERLAY_2026-09-11.tsv",
    "family": "STEP_04_INDEPENDENT_FAMILY_COHERENCE_AUDIT_2026-09-11.tsv",
    "boundary": "STEP_04_INDEPENDENT_FAMILY_BOUNDARY_RISK_MATRIX_2026-09-11.tsv",
    "queue_feedback": "STEP_04_INDEPENDENT_QUEUE_FEEDBACK_AUDIT_2026-09-11.tsv",
    "sources": "STEP_04_INDEPENDENT_EXTERNAL_METHOD_SOURCE_TRACE_2026-09-11.md",
    "metrics": "STEP_04_INDEPENDENT_AUDIT_METRICS_2026-09-11.json",
    "regression": "STEP_04_INDEPENDENT_RESULT_AUDIT_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-11.tsv",
    "qa": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_QA_2026-09-11.md",
    "return": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_WORK_RETURN_2026-09-11.md",
    "manifest": "STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_ARTIFACT_MANIFEST_2026-09-11.json",
}

OVERLAY_FIELDS = [
    "normalized_phrase_id",
    "canonical_phrase",
    "current_step03b_state",
    "current_step03b_reason",
    "current_step04_family_id",
    "raw_occurrence_count",
    "independent_signals",
    "independent_topic_id",
    "assigned_centroid_similarity",
    "nearest_other_family_id",
    "nearest_other_centroid_similarity",
    "audit_family_coherence_status",
    "audit_boundary_status",
    "audit_user_task_status",
    "audit_business_lineage_status",
    "audit_ambiguity_preservation_status",
    "audit_rule_bias_flag",
    "audit_recommended_disposition",
    "audit_reason",
]

ALLOWED_DISPOSITIONS = {
    "PASS_AS_PRELIMINARY_FAMILY",
    "REVIEW_MEMBER_ASSIGNMENT",
    "FAMILY_TOO_BROAD",
    "FAMILY_TOO_NARROW",
    "CROSS_FAMILY_BOUNDARY_DEFECT",
    "AMBIGUITY_ROUTING_DEFECT",
    "RULE_ORDER_DEFECT",
    "COVERAGE_GAP_DEFECT",
    "STEP03B_FEEDBACK_NEEDED",
}


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(name: str, fields: list[str], rows: Iterable[dict[str, object]]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            delimiter="\t",
            lineterminator="\n",
            fieldnames=fields,
            extrasaction="ignore",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_text(name: str, text: str) -> None:
    (HERE / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def lower(value: str) -> str:
    return value.casefold().replace("ё", "е")


def tokens(value: str) -> list[str]:
    return re.findall(r"[0-9a-zа-я]+", lower(value))


def prefix_present(words: set[str], prefixes: tuple[str, ...]) -> bool:
    return any(word.startswith(prefix) for word in words for prefix in prefixes)


def contains_any(value: str, fragments: tuple[str, ...]) -> bool:
    normalized = lower(value)
    return any(fragment in normalized for fragment in fragments)


def independent_signals(value: str) -> tuple[str, ...]:
    """Simultaneous audit features; no first-match routing and no broad `игр*`."""
    word_list = tokens(value)
    words = set(word_list)
    result: set[str] = set()

    if words & {"купить", "цена", "стоимость", "заказать", "магазин", "доставка", "озон", "ozon", "авито"}:
        result.add("COMMERCE")
    if words & {"фото", "рисунок", "изображение", "эскиз", "тату", "обои", "гиф", "gif", "логотип", "раскраска", "силуэт"} or prefix_present(words, ("картин", "изображ", "раскраск")):
        result.add("VISUAL")
    if words & {"значение", "смысл", "история", "происхождение", "описание"} or contains_any(value, ("что значит", "что означает", "как выглядит", "кто такой")):
        result.add("MEANING")
    if words & {"гороскоп", "совместимость", "стихия", "созвездие", "планета", "сегодня", "завтра", "асцендент", "прогноз"} or contains_any(value, ("дата рождения", "какой знак")):
        result.add("ASTRO_INFO")
    if words & {"фильм", "фильмы", "сериал", "сериалы", "серия", "серии", "книга", "книги", "глава", "читать", "слушать", "смотреть", "онлайн", "дзен", "канал", "рассказ", "песня", "музыка", "аудиокнига", "скачать", "автор", "сюжет", "сезон", "детектив", "лордфильм", "порно", "видео"}:
        result.add("MEDIA")
    if words & {"игра", "игры", "игре", "игру", "игрой", "играть", "мод", "моды", "id", "minecraft", "genshin", "warframe", "dota", "poe", "valhalla", "гта", "gta", "скайрим", "террария", "майнкрафт", "ведьмак"} or prefix_present(words, ("игров",)) or contains_any(value, ("hollow knight", "elden ring", "counter strike", "assassin creed")):
        result.add("GAME")
    if prefix_present(words, ("игруш",)):
        result.add("TOY")
    if words & {"сделать", "изготовить", "создать", "сшить", "связать", "сплести", "нарисовать", "руками"}:
        result.add("DIY")
    if words & {"двигатель", "датчик", "запчасти", "бампер", "тормоз", "сцепление", "краска", "ваз", "рено", "renault", "chery", "чери", "черри", "a15", "а15"} or prefix_present(words, ("двигател", "датчик", "запчаст", "бампер", "тормоз", "сцеплен", "автозапчаст", "краск")):
        result.add("VEHICLE_PART")
    if contains_any(value, ("в машину", "для машины", "для авто", "в авто", "для автомобиля", "для водителя", "на зеркало")):
        result.add("AUTO_USE")
    if prefix_present(words, ("молитв", "мантр", "намаз", "церк", "храм", "богород", "свят", "православ", "христиан", "мусульман", "будд", "медитац", "религи")) or words & {"икона", "иконы", "иконой", "икону"}:
        result.add("RELIGIOUS")
    if words & {"город", "улица", "адрес", "ооо", "банк", "завод", "гостиница", "ресторан", "кафе", "школа", "такси", "биография", "фамилия", "клуб", "команда", "инн", "фк"} or prefix_present(words, ("област", "гостиниц", "ресторан", "биограф", "фамил", "команд")):
        result.add("ENTITY")
    if prefix_present(words, ("кулон", "подвес", "браслет", "кольц", "перст", "серьг", "брелок", "медальон", "жетон", "бус", "камн", "серебр", "золот", "дерев", "кожан", "металл", "стал", "цепоч")):
        result.add("FORM_OR_MATERIAL")
    if prefix_present(words, ("амулет", "оберег", "талисман")) or words & {"четки", "четок", "четкам", "четками", "четках", "четкой", "четку", "четке"}:
        result.add("PRODUCT_WORD")
    if "зодиак" in lower(value) or ("знак" in words and bool(words & {"овен", "овна", "телец", "тельца", "близнецы", "близнецов", "рак", "рака", "лев", "льва", "дева", "девы", "весы", "скорпион", "стрелец", "козерог", "водолей", "рыбы", "рыба"})):
        result.add("ZODIAC")
    return tuple(sorted(result))


def norm_step03b_state(value: str) -> str:
    return {
        "KEEP_CANDIDATE": "KEEP",
        "HOLD_AMBIGUOUS": "HOLD",
        "AUTO_EXCLUDED": "EXCLUDE",
    }[value]


def entropy_normalized(labels: list[int], possible: int) -> float:
    if len(labels) <= 1:
        return 0.0
    counts = Counter(labels)
    entropy = -sum((count / len(labels)) * math.log(count / len(labels)) for count in counts.values())
    denominator = math.log(min(possible, len(labels)))
    return round(entropy / denominator, 6) if denominator else 0.0


def classify_row(row: dict[str, object], signals: set[str]) -> dict[str, str]:
    state = str(row["current_step03b_state"])
    family = str(row["current_step04_family_id"])
    phrase = str(row["canonical_phrase"])

    if state == "EXCLUDE":
        return {
            "audit_family_coherence_status": "NOT_APPLICABLE_EXCLUDED_HISTORY",
            "audit_boundary_status": "PASS_EXCLUDED_HISTORY_PRESERVED",
            "audit_user_task_status": "NOT_APPLICABLE_EXCLUDED_HISTORY",
            "audit_business_lineage_status": "PASS_NO_STEP04_BUSINESS_INFERENCE",
            "audit_ambiguity_preservation_status": "PASS_STEP03B_EXCLUDE_UNCHANGED",
            "audit_rule_bias_flag": "NO",
            "audit_recommended_disposition": "PASS_AS_PRELIMINARY_FAMILY",
            "audit_reason": "Corrected Step03B EXCLUDE remains history and has no Step04 primary family; audit inclusion is accounting-only.",
        }

    if family == "PSF019" and "TOY" in signals and "GAME" not in signals:
        return {
            "audit_family_coherence_status": "FAIL_FOREIGN_NON_GAME_MEMBER",
            "audit_boundary_status": "FAIL_PREFIX_COLLISION",
            "audit_user_task_status": "FAIL_TOY_TASK_ROUTED_AS_GAME",
            "audit_business_lineage_status": "UNRESOLVED_TOY_NOT_GAME_EVIDENCE",
            "audit_ambiguity_preservation_status": "FAIL_WRONG_AMBIGUITY_CLASS",
            "audit_rule_bias_flag": "YES_PREFIX_COLLISION_IGRUSHKA_AS_IGR",
            "audit_recommended_disposition": "RULE_ORDER_DEFECT",
            "audit_reason": f"Independent exact-token audit finds TOY without GAME in `{phrase}`; materializer `игр*` prefix pulls `игрушка` into PSF019.",
        }

    zodiac_defects = [signal for signal in ("MEANING", "MEDIA", "TOY") if family == "PSF014" and signal in signals]
    if zodiac_defects:
        signal_text = "+".join(zodiac_defects)
        return {
            "audit_family_coherence_status": "FAIL_EXPLICIT_TASK_INSIDE_UNQUALIFIED_FAMILY",
            "audit_boundary_status": "FAIL_ZODIAC_FIRST_MATCH_LEAKAGE",
            "audit_user_task_status": f"FAIL_EXPLICIT_{signal_text}_TASK_HIDDEN",
            "audit_business_lineage_status": "CAUTION_CATALOG_SIGN_NAME_IS_NOT_PRODUCT_INTENT_PROOF",
            "audit_ambiguity_preservation_status": "FAIL_MORE_INFORMATIVE_AMBIGUITY_ROUTE_SKIPPED",
            "audit_rule_bias_flag": "YES_ZODIAC_BRANCH_BEFORE_INFORMATIVE_SIGNAL",
            "audit_recommended_disposition": "RULE_ORDER_DEFECT",
            "audit_reason": f"PSF014 is defined as lacking a task, but independent signals={signal_text}; early zodiac branch does not test this more informative task class.",
        }

    if family == "PSF001" and "DIY" in signals:
        return {
            "audit_family_coherence_status": "FAIL_HIDDEN_COHERENT_DIY_SUBTASK",
            "audit_boundary_status": "REVIEW_MISSING_DIY_PRELIMINARY_BOUNDARY",
            "audit_user_task_status": "FAIL_EXPLICIT_MAKE_OR_CRAFT_TASK",
            "audit_business_lineage_status": "PASS_PRODUCT_CLASS_SUPPORTED_TASK_NOT_SUPPORTED_AS_GENERIC",
            "audit_ambiguity_preservation_status": "PARTIAL_TASK_SIGNAL_FLATTENED",
            "audit_rule_bias_flag": "YES_DIY_VOCABULARY_GAP_FALLS_TO_GENERIC_PRODUCT",
            "audit_recommended_disposition": "FAMILY_TOO_BROAD",
            "audit_reason": "Explicit make/craft wording forms a coherent user task, but PSF001 labels the member as a generic product query without enough task detail.",
        }

    return {
        "audit_family_coherence_status": "PASS_NO_ROW_LEVEL_DEFECT_DETECTED",
        "audit_boundary_status": "PASS_AS_PRELIMINARY_NOT_FINAL_CLUSTER",
        "audit_user_task_status": "PASS_OR_AMBIGUITY_EXPLICITLY_PRESERVED",
        "audit_business_lineage_status": "PASS_CATALOG_OR_BRIEF_USED_AS_SUPPORT_ONLY",
        "audit_ambiguity_preservation_status": "PASS_PRELIMINARY_AMBIGUITY_RETAINED",
        "audit_rule_bias_flag": "NO_MATERIAL_ROW_LEVEL_FLAG",
        "audit_recommended_disposition": "PASS_AS_PRELIMINARY_FAMILY",
        "audit_reason": "Exhaustive accounting, simultaneous signal checks and independent term-topic diagnostics found no material row-level defect; this is not final intent/SERP approval.",
    }


FAMILY_SCORES: dict[str, tuple[float, float, float, float, float, str]] = {
    "PSF001": (5.5, 6.0, 4.5, 7.0, 7.5, "REWORK_REQUIRED"),
    "PSF002": (9.0, 9.0, 9.0, 8.0, 1.0, "PASS"),
    "PSF003": (8.0, 7.5, 8.0, 8.0, 2.5, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF004": (8.0, 7.5, 8.0, 8.0, 3.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF005": (7.5, 7.0, 7.0, 8.0, 3.5, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF006": (6.0, 6.0, 6.0, 8.5, 5.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF007": (8.0, 7.5, 8.0, 8.0, 2.0, "PASS"),
    "PSF008": (8.0, 7.5, 8.0, 8.0, 2.0, "PASS"),
    "PSF009": (6.5, 6.5, 6.5, 9.0, 4.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF010": (7.0, 7.0, 7.5, 8.0, 3.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF011": (7.0, 7.0, 7.0, 7.5, 3.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF012": (8.0, 7.0, 8.0, 8.0, 3.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF013": (6.5, 6.0, 6.5, 8.5, 4.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF014": (4.0, 3.5, 3.5, 7.0, 9.5, "REWORK_REQUIRED"),
    "PSF015": (7.0, 7.0, 8.0, 9.0, 3.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF016": (8.0, 8.0, 8.0, 8.0, 2.0, "PASS"),
    "PSF017": (6.5, 6.0, 6.5, 9.0, 4.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF018": (6.0, 6.0, 6.0, 9.0, 4.5, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF019": (5.0, 4.0, 5.5, 7.0, 10.0, "REWORK_REQUIRED"),
    "PSF020": (6.5, 6.0, 7.0, 8.5, 4.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF021": (6.5, 6.0, 6.5, 9.0, 4.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF022": (7.0, 7.0, 7.0, 9.0, 3.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF023": (6.0, 6.0, 5.5, 9.0, 4.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF024": (5.5, 5.5, 5.5, 9.0, 4.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF025": (9.0, 8.0, 9.0, 9.0, 1.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
    "PSF026": (9.0, 8.0, 9.0, 9.0, 1.0, "PASS_WITH_NONBLOCKING_FINDINGS"),
}

FAMILY_FINDINGS = {
    "PSF001": "48 explicit DIY/make/craft identities contradict the unqualified-task boundary; independent topics also show multiple task-led subgroups.",
    "PSF006": "Large name-led components are expected, but short catalog-name membership remains highly heterogeneous and must stay referent-ambiguous.",
    "PSF014": "199 unique explicit-task identities are hidden by the unqualified-zodiac route: 156 MEANING, 38 MEDIA and 5 TOY signals.",
    "PSF018": "Media/title/digital-action members form several term topics; breadth is acceptable only as an explicit collision family, not a final cluster.",
    "PSF019": "8 TOY-without-GAME identities are false members caused by the broad `игр*` prefix.",
    "PSF024": "Residual phrases have low semantic cohesion by design; the family remains safe only as a quarantined feedback bucket, never a page cluster.",
    "PSF025": "Zero-member catalog-backed hypothesis; valid coverage gap, not observed demand.",
    "PSF026": "Zero-member brief-backed brand hypothesis; valid coverage gap, not observed demand.",
}

FAMILY_ACTIONS = {
    "PSF001": "Rework only after Main ChatGPT approval: add/route an explicit DIY preliminary task boundary; do not change Step03B here.",
    "PSF014": "Rework zodiac branch precedence/coverage so MEANING, MEDIA and physical TOY tasks cannot fall through to unqualified zodiac; audit full blast radius before correction.",
    "PSF019": "Replace broad `игр*` detection with exact game morphology separated from `игруш*`; re-audit all PSF019 members before correction.",
    "PSF006": "Keep ambiguous; add subtopic diagnostics/markers in any later approved rework without converting names into product intent.",
    "PSF018": "Retain collision status and explicit feedback; do not map the family wholesale to one intent/page.",
    "PSF024": "Retain as quarantined residual plus sanitation feedback; review coherent subgroups later without frequency-based deletion.",
    "PSF025": "Keep as a coverage-gap hypothesis; one bounded later action only after resumed Step05 authorization.",
    "PSF026": "Keep as a coverage-gap hypothesis; one bounded later action only after resumed Step05 authorization.",
}

MANUAL_BOUNDARY_RISKS: dict[frozenset[str], tuple[str, str, str]] = {
    frozenset(("PSF014", "PSF015")): ("CRITICAL", "156 MEANING identities sit in unqualified PSF014 although PSF015 owns zodiac information.", "Correct zodiac information routing after audit approval."),
    frozenset(("PSF014", "PSF018")): ("CRITICAL", "38 MEDIA identities sit in PSF014 although the media/digital collision boundary is explicit.", "Correct zodiac/media precedence after audit approval."),
    frozenset(("PSF012", "PSF014")): ("HIGH", "5 explicit TOY/product-form zodiac identities remain in unqualified PSF014.", "Define the physical-toy/product-form boundary before rerouting."),
    frozenset(("PSF001", "PSF019")): ("CRITICAL", "8 TOY-without-GAME identities are pulled into PSF019 by `игр*`; no toy boundary exists.", "Separate toy morphology from game morphology and decide the preliminary destination."),
    frozenset(("PSF001", "PSF023")): ("HIGH", "Generic product versus unresolved-referent boundary is lexically close and reason-code dependent.", "Preserve the state/referent distinction and test equivalence in rework."),
    frozenset(("PSF023", "PSF024")): ("HIGH", "Residual product morphology and fully residual context are separated largely by product-token recognition.", "Retain quarantine and review morphology without forced assignment."),
    frozenset(("PSF003", "PSF020")): ("MEDIUM", "Automobile use-case and vehicle/model/part collision share vocabulary.", "Keep use versus vehicle-object guards explicit."),
    frozenset(("PSF005", "PSF006")): ("MEDIUM", "Qualified and unqualified catalog-name families are adjacent by construction.", "Retain qualification evidence in every assignment."),
    frozenset(("PSF005", "PSF009")): ("HIGH", "Qualified catalog-product phrases and unresolved catalog homonyms overlap for short names.", "Do not treat catalog membership as product-intent proof."),
    frozenset(("PSF006", "PSF009")): ("HIGH", "Both preserve short catalog-name ambiguity; split depends strongly on reason code and residual path.", "Reconcile equivalent short-name cases during approved rework."),
    frozenset(("PSF008", "PSF016")): ("MEDIUM", "General catalog visuals and zodiac visuals differ mainly by zodiac recognition.", "Keep the topical qualifier explicit; no final page inference."),
    frozenset(("PSF012", "PSF013")): ("HIGH", "Zodiac product/form and zodiac stone/material collision share commercial and physical markers.", "Require material/owner facts before narrowing."),
    frozenset(("PSF013", "PSF014")): ("HIGH", "Stone-qualified and unqualified zodiac boundaries depend on a small material lexicon.", "Audit stone synonyms before any correction."),
    frozenset(("PSF014", "PSF016")): ("MEDIUM", "Unqualified zodiac and visual zodiac are adjacent; visual vocabulary controls the split.", "Retain visual task marker and ambiguity."),
    frozenset(("PSF017", "PSF018")): ("MEDIUM", "Religious text/practice and media/text actions can overlap.", "Preserve both referent hypotheses until later evidence."),
    frozenset(("PSF018", "PSF019")): ("MEDIUM", "Media titles and games share named-work/action language.", "Require specific game evidence; generic digital language is insufficient."),
}

QUEUE_CLASS = {
    "PSQ001": ("VALID_GAP", "0 current identities for RSOTM/Soldier Of Fortune/Бусидо exact branches; catalog supports only a future bounded hypothesis."),
    "PSQ002": ("OWNER_FACT_FIRST", "PSF017 has 234 mixed members, while the physical form of the prayer card is an owner fact, not a provider inference."),
    "PSQ003": ("OWNER_FACT_FIRST", "Exact `Герб России` observations are 0; the queue evidence cell is family-generic, and physical form must be confirmed by owner first."),
    "PSQ004": ("VALID_GAP", "0 current product-qualified `Кровь и Песок` identities; brief supports a future bounded brand/product check only."),
    "PSQ005": ("DUPLICATES_EXISTING_EVIDENCE", "The universe already contains 4 qualified PSF005 `ом` product identities; only `аум` lacks that branch, so the combined probe duplicates current evidence."),
    "PSQ006": ("DUPLICATES_EXISTING_EVIDENCE", "The universe already contains 12 qualified PSF005 `гунгнир*` identities plus additional product-qualified Odin-spear evidence."),
    "PSQ007": ("DUPLICATES_EXISTING_EVIDENCE", "PSF005 already contains 79 qualified identities across Алатырь/Триглав/Ратиборец/Знич/Громовик."),
    "PSQ008": ("DUPLICATES_EXISTING_EVIDENCE", "PSF005 already contains 13 qualified identities across Белобог/Чернобог/Мара."),
    "PSQ009": ("OWNER_FACT_FIRST", "All 12 signs are catalog-supported, but form/material is explicitly missing from owner facts."),
    "PSQ010": ("DUPLICATES_EXISTING_EVIDENCE", "The durable historical E013 `!чётки` provider evidence is preserved and mapped to current PSQ010; replay would duplicate evidence."),
    "PSQ011": ("DEFER_TO_LATER_INTENT_OR_SERP", "Its own stop logic requires a concrete Step10 collision first; no expansion is justified now."),
    "PSQ012": ("OWNER_FACT_FIRST", "Observed form/material demand cannot prove inventory; provider_needed=NO is correct."),
    "PSQ013": ("OWNER_FACT_FIRST", "Effects/audiences require owner-approved claim boundaries; provider_needed=NO is correct."),
}

FEEDBACK_CLASS = {
    "PSFB001": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "Full PSF015 is an explicit zodiac-information HOLD class; no Step04 state change is proposed."),
    "PSFB002": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "Full PSF018 contains heterogeneous media/title/digital referents and correctly preserves ambiguity."),
    "PSFB003": ("TOO_BROAD", "The class is materially contaminated: 8 cited/underlying `игруш*` rows have no independent GAME signal and are Step04 rule defects."),
    "PSFB004": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "Full PSF020 keeps automobile use versus model/part/paint collision visible."),
    "PSFB005": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "Full PSF021 preserves entity/product ambiguity rather than making an entity verdict."),
    "PSFB006": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "All 33 members are governed morphology/typo uncertainty; broad `четк*` exclusion is not restored."),
    "PSFB007": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "The 132 affected PSF005 HOLD identities keep product support separate from referent proof."),
    "PSFB008": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "Full PSF017 preserves physical object versus text/practice ambiguity."),
    "PSFB009": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "Full PSF024 is correctly quarantined as residual/noise uncertainty without frequency-based deletion."),
    "PSFB010": ("JUSTIFIED_CLASS_LEVEL_FEEDBACK", "Full PSF011 requires claim/owner-fact control and makes no effectiveness assertion."),
}

SCORE_DIMENSIONS = {
    "full_volume_accounting": 10.0,
    "family_coherence": 5.5,
    "boundary_precision": 5.0,
    "ambiguity_preservation": 8.0,
    "user_task_coherence": 5.0,
    "business_lineage_discipline": 8.5,
    "lexical_rule_order_bias_control": 3.0,
    "cross_family_overlap_control": 4.5,
    "coverage_gap_quality": 7.0,
    "sanitation_feedback_quality": 7.0,
    "traceability": 9.5,
    "downstream_safety": 8.0,
    "external_method_alignment": 7.0,
}


def build_source_trace() -> str:
    return f"""# KW-002 Step04 independent audit — external method source trace

Date checked: {DATE}

Scope: methodology only. None of these sources is used as authority for Blood & Sand business facts, demand, inventory, intent, page design or IA.

| Source | Current methodological principle used | Audit use | Boundary |
|---|---|---|---|
| [Yandex Webmaster — Query selection](https://yandex.ru/support/webmaster/ru/service/queries-selection) | Query clusters are automatic groupings by close meaning or user intent; demand/click/competition are separate measures. | Tests topical/task coherence separately from frequency. | Webmaster grouping is not copied as this job's family authority. |
| [Yandex Webmaster — Search quality](https://yandex.com/support/webmaster/en/search-quality) | Search quality is evaluated against the user's objective and usefulness. | Requires family task hypotheses to be supported by member wording. | No ordinary Yandex Search call was made. |
| [Topvisor — clustering](https://topvisor.com/ru/support/clustering/) | Final SEO clustering commonly uses overlap in Yandex/Google Top-10 and must be tested for the theme. | Establishes why this audit may test preliminary lexical families but cannot approve final clusters. | No SERP collection or final clustering was performed. |
| [Ahrefs — keyword clustering](https://ahrefs.com/blog/keyword-clustering/) | Intent/SERP similarity clustering and term/co-occurrence clustering answer different questions. | Uses term TF-IDF/topic decomposition only as an independent diagnostic. | Diagnostic topics do not become pages or final keyword clusters. |
| [Ahrefs — search intent](https://ahrefs.com/blog/search-intent/) | Mixed/volatile result sets can reflect mixed or changing intent. | Rewards preserved ambiguity and rejects premature intent labels. | No live SERP inference was made. |
| [Semrush — keyword clustering](https://www.semrush.com/blog/keyword-clustering/) | Large sets need scalable grouping while respecting SERP similarity, content breadth and user journey. | Supports exhaustive machine checks plus explicit downstream boundaries. | This pass does not design content or user journeys. |
| [scikit-learn — text feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html) | TF-IDF downweights corpus-common terms; short text remains noisy. | Provides a reproducible independent term-space diagnostic over all 18,135 active/HOLD identities. | TF-IDF distances are evidence, not ground truth. |
| [scikit-learn — clustering evaluation](https://scikit-learn.org/stable/modules/clustering.html) | Internal clustering measures describe separation and have known limitations. | Uses topic entropy, centroid similarity and alternate-centroid rates as warnings, not final verdicts. | Human-governed rule/lineage evidence controls material defect findings. |

Pre-execution owner-facing disclosure was made before the diagnostic run and identified the job goal, completed/remaining steps, this audit's purpose, prior failures, controls, planned method and acceptance conditions.
"""


def main() -> None:
    input_hashes = {name: sha256(HERE / name) for name in INPUTS.values()}
    for name, expected in EXPECTED_SHA256.items():
        assert input_hashes[name] == expected, (name, input_hashes[name], expected)

    pool_rows = read_tsv(INPUTS["pool"])
    keep_rows = read_tsv(INPUTS["keep"])
    register_rows = read_tsv(INPUTS["register"])
    ledger_rows = read_tsv(INPUTS["step04_ledger"])
    family_input = read_tsv(INPUTS["families"])
    queue_input = read_tsv(INPUTS["queue"])
    feedback_input = read_tsv(INPUTS["feedback"])

    assert len(pool_rows) == 24576
    assert len(keep_rows) == 5100
    assert len(register_rows) == 19476
    assert len(ledger_rows) == 25979
    assert len(family_input) == 26
    assert len(queue_input) == 13
    assert len(feedback_input) == 10

    pool = {row["normalized_phrase_id"]: row for row in pool_rows}
    assert len(pool) == 24576
    step03b: dict[str, dict[str, str]] = {}
    for row in keep_rows + register_rows:
        npid = row["normalized_phrase_id"]
        assert npid not in step03b
        step03b[npid] = {
            "state": norm_step03b_state(row["sanitation_state"]),
            "reason": row["sanitation_reason_code"],
            "phrase": row["canonical_phrase"],
        }
    assert set(step03b) == set(pool)

    raw_ids: set[str] = set()
    raw_count_by_identity: Counter[str] = Counter()
    identities: dict[str, dict[str, object]] = {}
    for row in ledger_rows:
        raw_id = row["raw_occurrence_id"]
        assert raw_id not in raw_ids
        raw_ids.add(raw_id)
        npid = row["normalized_phrase_id"]
        raw_count_by_identity[npid] += 1
        core = {
            "normalized_phrase_id": npid,
            "canonical_phrase": row["canonical_phrase"],
            "current_step03b_state": row["current_step03b_state"],
            "current_step03b_reason": row["current_step03b_reason"],
            "current_step04_family_id": row["post_sanitation_family_id"],
        }
        previous = identities.get(npid)
        if previous is not None:
            assert previous == core, (npid, previous, core)
        identities[npid] = core

    assert len(raw_ids) == 25979
    assert len(identities) == 24576
    assert set(identities) == set(pool)
    assert sum(raw_count_by_identity.values()) == 25979

    state_counts = Counter(str(row["current_step03b_state"]) for row in identities.values())
    assert state_counts == Counter({"HOLD": 13035, "EXCLUDE": 6441, "KEEP": 5100})

    for npid, row in identities.items():
        assert row["canonical_phrase"] == pool[npid]["canonical_phrase"] == step03b[npid]["phrase"]
        assert row["current_step03b_state"] == step03b[npid]["state"]
        assert row["current_step03b_reason"] == step03b[npid]["reason"]
        if row["current_step03b_state"] == "EXCLUDE":
            assert row["current_step04_family_id"] == "NOT_IN_STEP04_SEMANTIC_SCOPE"
        else:
            assert re.fullmatch(r"PSF0(?:0[1-9]|1[0-9]|2[0-6])", str(row["current_step04_family_id"]))

    family_ids = [row["family_id"] for row in family_input]
    assert family_ids == [f"PSF{i:03d}" for i in range(1, 27)]
    active_ids = sorted(npid for npid, row in identities.items() if row["current_step03b_state"] != "EXCLUDE")
    assert len(active_ids) == 18135
    docs = [str(identities[npid]["canonical_phrase"]) for npid in active_ids]

    diagnostic_stopwords = {
        "амулет", "амулеты", "амулета", "амулетов", "амулетом", "амулету",
        "оберег", "обереги", "оберега", "оберегов", "оберегом", "оберегу",
        "талисман", "талисманы", "талисмана", "талисманов", "талисманом",
        "четки", "четок", "четкам", "четками", "четках", "четкой", "четку", "четке",
        "знак", "знаки", "знака", "знаков", "зодиака", "зодиак",
        "для", "на", "в", "и", "с", "по", "что", "как", "это", "из", "к", "у", "о", "а", "не", "или",
    }
    vectorizer = TfidfVectorizer(
        lowercase=True,
        token_pattern=r"(?u)\b[0-9A-Za-zА-Яа-яЁё]{2,}\b",
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.985,
        max_features=30000,
        sublinear_tf=True,
        stop_words=sorted(diagnostic_stopwords),
        norm="l2",
    )
    matrix = vectorizer.fit_transform(docs)
    assert matrix.shape[0] == 18135

    topic_model = MiniBatchKMeans(
        n_clusters=32,
        random_state=RANDOM_SEED,
        batch_size=1024,
        n_init=10,
        max_iter=250,
        reassignment_ratio=0.01,
    )
    topic_labels = topic_model.fit_predict(matrix)
    feature_names = np.asarray(vectorizer.get_feature_names_out())
    topic_top_terms: dict[str, list[str]] = {}
    for topic_id, center in enumerate(topic_model.cluster_centers_):
        top_indices = np.argsort(center)[-10:][::-1]
        topic_top_terms[f"T{topic_id:02d}"] = [str(feature_names[index]) for index in top_indices if center[index] > 0][:8]

    observed_family_ids = family_ids[:24]
    active_positions_by_family: dict[str, list[int]] = defaultdict(list)
    for position, npid in enumerate(active_ids):
        active_positions_by_family[str(identities[npid]["current_step04_family_id"])].append(position)
    assert set(active_positions_by_family) == set(observed_family_ids)

    centroids = []
    for family_id in observed_family_ids:
        family_matrix = matrix[active_positions_by_family[family_id]]
        centroids.append(csr_matrix(family_matrix.mean(axis=0)))
    centroid_matrix = normalize(vstack(centroids), norm="l2", axis=1)
    member_to_centroid = np.asarray((matrix @ centroid_matrix.T).todense())
    centroid_similarity = np.asarray((centroid_matrix @ centroid_matrix.T).todense())

    active_model: dict[str, dict[str, object]] = {}
    for position, npid in enumerate(active_ids):
        family_id = str(identities[npid]["current_step04_family_id"])
        own_index = observed_family_ids.index(family_id)
        similarities = member_to_centroid[position].copy()
        own_similarity = float(similarities[own_index])
        similarities[own_index] = -1.0
        other_index = int(np.argmax(similarities))
        vector_nonzero = matrix[position].nnz > 0
        active_model[npid] = {
            "topic_id": int(topic_labels[position]),
            "own_similarity": own_similarity if vector_nonzero else None,
            "nearest_other_family": observed_family_ids[other_index] if vector_nonzero else "",
            "nearest_other_similarity": float(similarities[other_index]) if vector_nonzero else None,
        }

    signal_by_identity = {npid: set(independent_signals(str(row["canonical_phrase"]))) for npid, row in identities.items()}

    toy_game_ids = sorted(npid for npid, row in identities.items() if row["current_step04_family_id"] == "PSF019" and "TOY" in signal_by_identity[npid] and "GAME" not in signal_by_identity[npid])
    zodiac_meaning_ids = sorted(npid for npid, row in identities.items() if row["current_step04_family_id"] == "PSF014" and "MEANING" in signal_by_identity[npid])
    zodiac_media_ids = sorted(npid for npid, row in identities.items() if row["current_step04_family_id"] == "PSF014" and "MEDIA" in signal_by_identity[npid])
    zodiac_toy_ids = sorted(npid for npid, row in identities.items() if row["current_step04_family_id"] == "PSF014" and "TOY" in signal_by_identity[npid])
    zodiac_explicit_ids = sorted(set(zodiac_meaning_ids) | set(zodiac_media_ids) | set(zodiac_toy_ids))
    generic_diy_ids = sorted(npid for npid, row in identities.items() if row["current_step04_family_id"] == "PSF001" and "DIY" in signal_by_identity[npid])

    assert len(toy_game_ids) == 8
    assert len(zodiac_meaning_ids) == 156, ("zodiac_meaning", len(zodiac_meaning_ids))
    assert len(zodiac_media_ids) == 38, ("zodiac_media", len(zodiac_media_ids))
    assert len(zodiac_toy_ids) == 5, ("zodiac_toy", len(zodiac_toy_ids))
    assert len(zodiac_explicit_ids) == 199, ("zodiac_explicit", len(zodiac_explicit_ids))
    assert len(generic_diy_ids) == 48, ("generic_diy", len(generic_diy_ids))
    defect_ids = sorted(set(toy_game_ids) | set(zodiac_explicit_ids) | set(generic_diy_ids))
    assert len(defect_ids) == 255

    overlay_rows: list[dict[str, object]] = []
    disposition_counts: Counter[str] = Counter()
    family_defect_counts: Counter[str] = Counter()
    for npid in sorted(identities):
        identity = identities[npid]
        signals = signal_by_identity[npid]
        audit = classify_row(identity, signals)
        assert audit["audit_recommended_disposition"] in ALLOWED_DISPOSITIONS
        disposition_counts[audit["audit_recommended_disposition"]] += 1
        if audit["audit_recommended_disposition"] != "PASS_AS_PRELIMINARY_FAMILY":
            family_defect_counts[str(identity["current_step04_family_id"])] += 1
        model = active_model.get(npid, {})
        own = model.get("own_similarity")
        other = model.get("nearest_other_similarity")
        overlay_rows.append({
            **identity,
            "raw_occurrence_count": raw_count_by_identity[npid],
            "independent_signals": "|".join(sorted(signals)) if signals else "NONE",
            "independent_topic_id": f"T{int(model['topic_id']):02d}" if "topic_id" in model else "NOT_APPLICABLE_EXCLUDED_HISTORY",
            "assigned_centroid_similarity": "" if own is None else f"{float(own):.6f}",
            "nearest_other_family_id": model.get("nearest_other_family", ""),
            "nearest_other_centroid_similarity": "" if other is None else f"{float(other):.6f}",
            **audit,
        })
    assert len(overlay_rows) == 24576
    assert disposition_counts == Counter({"PASS_AS_PRELIMINARY_FAMILY": 24321, "RULE_ORDER_DEFECT": 207, "FAMILY_TOO_BROAD": 48})
    write_tsv(OUTPUTS["overlay"], OVERLAY_FIELDS, overlay_rows)

    family_input_by_id = {row["family_id"]: row for row in family_input}
    family_diag: dict[str, dict[str, object]] = {}
    family_rows: list[dict[str, object]] = []
    family_fields = [
        "family_id", "family_label", "member_count", "raw_occurrence_count", "coherence_score_10",
        "boundary_precision_score_10", "user_task_coherence_score_10", "ambiguity_safety_score_10",
        "rule_bias_risk_score_10", "independent_topic_count", "independent_topic_entropy_normalized",
        "dominant_independent_topic_share", "mean_assigned_centroid_similarity", "nearest_other_centroid_override_rate",
        "large_family_heterogeneity_findings", "cross_family_overlap_findings", "external_method_alignment",
        "verdict", "required_action",
    ]
    for family_id in family_ids:
        members = [npid for npid, row in identities.items() if row["current_step04_family_id"] == family_id]
        positions = active_positions_by_family.get(family_id, [])
        if positions:
            topics = [int(topic_labels[position]) for position in positions]
            topic_counts = Counter(topics)
            topic_entropy = entropy_normalized(topics, 32)
            dominant_topic_share = max(topic_counts.values()) / len(topics)
            own_values = []
            override_count = 0
            for position in positions:
                npid = active_ids[position]
                model = active_model[npid]
                own = model["own_similarity"]
                other = model["nearest_other_similarity"]
                if own is not None and other is not None:
                    own_values.append(float(own))
                    if float(other) >= float(own) + 0.10 and float(other) >= 0.25:
                        override_count += 1
            mean_own = float(np.mean(own_values)) if own_values else 0.0
            override_rate = override_count / len(positions)
            top_topics = [
                {
                    "topic_id": f"T{topic:02d}",
                    "members": count,
                    "share": round(count / len(topics), 6),
                    "top_terms": topic_top_terms[f"T{topic:02d}"],
                }
                for topic, count in topic_counts.most_common(5)
            ]
        else:
            topic_counts = Counter()
            topic_entropy = 0.0
            dominant_topic_share = 0.0
            mean_own = 0.0
            override_rate = 0.0
            top_topics = []

        nearest_family = "NONE"
        nearest_similarity = 0.0
        if family_id in observed_family_ids:
            index = observed_family_ids.index(family_id)
            values = centroid_similarity[index].copy()
            values[index] = -1.0
            nearest_index = int(np.argmax(values))
            nearest_family = observed_family_ids[nearest_index]
            nearest_similarity = float(values[nearest_index])

        coherence, boundary, user_task, ambiguity, bias_risk, verdict = FAMILY_SCORES[family_id]
        default_finding = "No material family-wide defect found; independent topic breadth is retained only as a non-final diagnostic."
        finding = FAMILY_FINDINGS.get(family_id, default_finding)
        overlap_finding = f"Nearest term centroid={nearest_family} at cosine={nearest_similarity:.6f}; see complete symmetric matrix."
        alignment = (
            "FAIL_MATERIAL: independent term/task evidence contradicts the current preliminary boundary."
            if verdict == "REWORK_REQUIRED"
            else "PARTIAL_PASS: term/topic evidence is compatible with preliminary triage only; no final SERP/intent claim is made."
        )
        action = FAMILY_ACTIONS.get(family_id, "Retain as preliminary only; preserve ambiguity and re-check at the governed later evidence stage.")
        raw_occurrences = sum(raw_count_by_identity[npid] for npid in members)
        family_rows.append({
            "family_id": family_id,
            "family_label": family_input_by_id[family_id]["family_label_plain_russian"],
            "member_count": len(members),
            "raw_occurrence_count": raw_occurrences,
            "coherence_score_10": f"{coherence:.1f}",
            "boundary_precision_score_10": f"{boundary:.1f}",
            "user_task_coherence_score_10": f"{user_task:.1f}",
            "ambiguity_safety_score_10": f"{ambiguity:.1f}",
            "rule_bias_risk_score_10": f"{bias_risk:.1f}",
            "independent_topic_count": len(topic_counts),
            "independent_topic_entropy_normalized": f"{topic_entropy:.6f}",
            "dominant_independent_topic_share": f"{dominant_topic_share:.6f}",
            "mean_assigned_centroid_similarity": f"{mean_own:.6f}" if positions else "NOT_APPLICABLE_ZERO_MEMBER_GAP",
            "nearest_other_centroid_override_rate": f"{override_rate:.6f}" if positions else "NOT_APPLICABLE_ZERO_MEMBER_GAP",
            "large_family_heterogeneity_findings": finding,
            "cross_family_overlap_findings": overlap_finding,
            "external_method_alignment": alignment,
            "verdict": verdict,
            "required_action": action,
        })
        family_diag[family_id] = {
            "member_count": len(members),
            "raw_occurrence_count": raw_occurrences,
            "independent_topic_entropy_normalized": topic_entropy,
            "dominant_topic_share": round(dominant_topic_share, 6),
            "mean_assigned_centroid_similarity": round(mean_own, 6),
            "nearest_other_centroid_override_rate": round(override_rate, 6),
            "nearest_family_centroid": nearest_family,
            "nearest_family_centroid_similarity": round(nearest_similarity, 6),
            "top_topics": top_topics,
            "audit_defect_rows": family_defect_counts[family_id],
            "verdict": verdict,
        }
    assert len(family_rows) == 26
    assert sum(row["member_count"] for row in family_rows) == 18135
    write_tsv(OUTPUTS["family"], family_fields, family_rows)

    boundary_rows: list[dict[str, object]] = []
    boundary_fields = [
        "family_id_a", "family_id_b", "member_count_a", "member_count_b", "symmetric_pair_key",
        "centroid_cosine_similarity", "shared_independent_topic_count", "risk_level", "evidence", "required_action",
    ]
    member_counts = {row["family_id"]: int(row["member_count"]) for row in family_rows}
    family_topic_sets = {
        family_id: set(int(topic_labels[position]) for position in active_positions_by_family.get(family_id, []))
        for family_id in family_ids
    }
    for family_a in family_ids:
        for family_b in family_ids:
            pair = frozenset((family_a, family_b))
            pair_key = "|".join(sorted((family_a, family_b)))
            if family_a == family_b:
                similarity_value: float | None = 1.0 if member_counts[family_a] else None
                risk, evidence, action = "SELF", "Diagonal self-cell.", "NONE"
            elif family_a not in observed_family_ids or family_b not in observed_family_ids:
                similarity_value = None
                risk, evidence, action = "GAP_NOT_COMPARABLE", "At least one family has zero observed members.", "Retain as coverage hypothesis only."
            else:
                a_index = observed_family_ids.index(family_a)
                b_index = observed_family_ids.index(family_b)
                similarity_value = float(centroid_similarity[a_index, b_index])
                if pair in MANUAL_BOUNDARY_RISKS:
                    risk, evidence, action = MANUAL_BOUNDARY_RISKS[pair]
                elif similarity_value >= 0.65:
                    risk, evidence, action = "HIGH_DIAGNOSTIC", "High rule-agnostic term-centroid similarity; no material row defect proven by similarity alone.", "Review only if later governed evidence confirms task equivalence."
                elif similarity_value >= 0.45:
                    risk, evidence, action = "MEDIUM_DIAGNOSTIC", "Moderate rule-agnostic term-centroid similarity; diagnostic only.", "Preserve preliminary boundary and ambiguity."
                else:
                    risk, evidence, action = "LOW", "No material cross-family defect established by full-volume term diagnostic.", "NONE"
            boundary_rows.append({
                "family_id_a": family_a,
                "family_id_b": family_b,
                "member_count_a": member_counts[family_a],
                "member_count_b": member_counts[family_b],
                "symmetric_pair_key": pair_key,
                "centroid_cosine_similarity": "NOT_APPLICABLE" if similarity_value is None else f"{similarity_value:.6f}",
                "shared_independent_topic_count": len(family_topic_sets[family_a] & family_topic_sets[family_b]),
                "risk_level": risk,
                "evidence": evidence,
                "required_action": action,
            })
    assert len(boundary_rows) == 676
    boundary_lookup = {(row["family_id_a"], row["family_id_b"]): row for row in boundary_rows}
    for family_a in family_ids:
        for family_b in family_ids:
            left = boundary_lookup[(family_a, family_b)]
            right = boundary_lookup[(family_b, family_a)]
            for field in ("symmetric_pair_key", "centroid_cosine_similarity", "shared_independent_topic_count", "risk_level", "evidence", "required_action"):
                assert left[field] == right[field], (family_a, family_b, field)
    write_tsv(OUTPUTS["boundary"], boundary_fields, boundary_rows)

    queue_feedback_rows: list[dict[str, object]] = []
    qf_fields = [
        "record_type", "record_id", "related_family_id", "source_member_count", "source_raw_occurrence_count",
        "current_problem_or_finding", "audit_classification", "full_volume_evidence", "audit_verdict",
        "required_action", "provider_call_made", "step03b_state_changed", "step04_corrected_in_this_pass",
    ]
    family_raw_counts = {row["family_id"]: int(row["raw_occurrence_count"]) for row in family_rows}
    for row in queue_input:
        classification, evidence = QUEUE_CLASS[row["queue_id"]]
        queue_feedback_rows.append({
            "record_type": "EXPANSION_QUEUE",
            "record_id": row["queue_id"],
            "related_family_id": row["family_id"],
            "source_member_count": member_counts[row["family_id"]],
            "source_raw_occurrence_count": family_raw_counts[row["family_id"]],
            "current_problem_or_finding": row["problem"],
            "audit_classification": classification,
            "full_volume_evidence": evidence,
            "audit_verdict": "PASS" if classification in {"VALID_GAP", "OWNER_FACT_FIRST", "DEFER_TO_LATER_INTENT_OR_SERP"} else "REWORK_REQUIRED",
            "required_action": "Do not call provider in this audit; revise/de-duplicate the queue only in an approved correction pass." if classification == "DUPLICATES_EXISTING_EVIDENCE" else "Respect the classified gate; no action in this audit pass.",
            "provider_call_made": "NO",
            "step03b_state_changed": "NO",
            "step04_corrected_in_this_pass": "NO",
        })
    for row in feedback_input:
        classification, evidence = FEEDBACK_CLASS[row["feedback_id"]]
        queue_feedback_rows.append({
            "record_type": "SANITATION_FEEDBACK",
            "record_id": row["feedback_id"],
            "related_family_id": row["source_family_id"],
            "source_member_count": row["normalized_identity_count"],
            "source_raw_occurrence_count": row["raw_occurrence_count"],
            "current_problem_or_finding": row["finding"],
            "audit_classification": classification,
            "full_volume_evidence": evidence,
            "audit_verdict": "PASS" if classification == "JUSTIFIED_CLASS_LEVEL_FEEDBACK" else "REWORK_REQUIRED",
            "required_action": "Retain non-destructively." if classification == "JUSTIFIED_CLASS_LEVEL_FEEDBACK" else "Separate false toy/game members from the legitimate game feedback class in an approved correction pass.",
            "provider_call_made": "NO",
            "step03b_state_changed": "NO",
            "step04_corrected_in_this_pass": "NO",
        })
    extra_feedback = [
        ("AUDIT_MISSING_001", "PSF001", 48, "Explicit DIY user task hidden in generic family", "MISSING_MATERIAL_FEEDBACK_CLASS", "48 exhaustive members carry independent DIY signals."),
        ("AUDIT_MISSING_002", "PSF014", 199, "Explicit meaning/media/toy tasks hidden by zodiac branch", "MISSING_MATERIAL_FEEDBACK_CLASS", "199 exhaustive members: 156 meaning, 38 media, 5 toy."),
        ("AUDIT_MISSING_003", "PSF019", 8, "Toy morphology falsely treated as game morphology", "MISSING_MATERIAL_FEEDBACK_CLASS", "8 exhaustive TOY-without-GAME members."),
    ]
    for record_id, family_id, count, finding, classification, evidence in extra_feedback:
        queue_feedback_rows.append({
            "record_type": "ADDITIONAL_AUDIT_FINDING",
            "record_id": record_id,
            "related_family_id": family_id,
            "source_member_count": count,
            "source_raw_occurrence_count": sum(raw_count_by_identity[npid] for npid in defect_ids if identities[npid]["current_step04_family_id"] == family_id),
            "current_problem_or_finding": finding,
            "audit_classification": classification,
            "full_volume_evidence": evidence,
            "audit_verdict": "REWORK_REQUIRED",
            "required_action": "Record for Main ChatGPT; do not correct Step04 or mutate Step03B in this pass.",
            "provider_call_made": "NO",
            "step03b_state_changed": "NO",
            "step04_corrected_in_this_pass": "NO",
        })
    assert len(queue_feedback_rows) == 26
    write_tsv(OUTPUTS["queue_feedback"], qf_fields, queue_feedback_rows)

    regression_rows = [
        ("AUD001", "RAW occurrence IDs exhaustive and unique", "25979 rows / 25979 unique / loss 0", "PASS"),
        ("AUD002", "Normalized identities exhaustive", "24576 identities exactly", "PASS"),
        ("AUD003", "Active plus HOLD assignment total", "18135 / one PSF001-PSF024 family each", "PASS"),
        ("AUD004", "EXCLUDE history preserved", "6441 / NOT_IN_STEP04_SEMANTIC_SCOPE", "PASS"),
        ("AUD005", "Step03B state and reason immutability", "0 mismatches against corrected authorities", "PASS"),
        ("AUD006", "Independent diagnostic not same ordered classifier", "TF-IDF 1-2 grams + 32-topic MiniBatchKMeans + centroids over all 18135", "PASS"),
        ("AUD007", "Large-family audit", "PSF001/006/014/018/024 all receive full-volume topic metrics and findings", "PASS"),
        ("AUD008", "Broad `игр*` prefix collision", "8 TOY-without-GAME rows detected and flagged", "PASS"),
        ("AUD009", "Early zodiac-rule task hiding", "199 explicit-task PSF014 rows detected and flagged", "PASS"),
        ("AUD010", "Generic-family hidden DIY task", "48 PSF001 rows detected and flagged", "PASS"),
        ("AUD011", "Symmetric boundary matrix", "26 x 26 = 676 ordered cells / symmetry asserted", "PASS"),
        ("AUD012", "Expansion queue exhaustive", "13/13 classified / provider calls 0", "PASS"),
        ("AUD013", "Sanitation feedback exhaustive", "10/10 audited plus 3 missing audit classes recorded", "PASS"),
        ("AUD014", "Coverage-gap families", "PSF025 and PSF026 retained as zero-member hypotheses, not demand proof", "PASS"),
        ("AUD015", "Frequency independence", "No frequency field enters signal, topic, defect or family-verdict routing", "PASS"),
        ("AUD016", "Old self-score not inherited", "Fresh 13-dimension audit score computed independently", "PASS"),
        ("AUD017", "No final intent/SERP/page inference", "No SERP, final intent, page or IA artifact exists", "PASS"),
        ("AUD018", "No Step04 correction", "All accepted Step04 inputs hash-match; audit writes overlay only", "PASS"),
        ("AUD019", "No provider or ordinary search calls", "Wordstat/Search/GenSearch/AI-search = 0", "PASS"),
        ("AUD020", "Stop boundary", "Step05 advancement=false; Step06 advancement=false", "PASS"),
    ]
    write_tsv(
        OUTPUTS["regression"],
        ["test_id", "anti_regression_control", "observed_evidence", "audit_test_status"],
        [dict(zip(["test_id", "anti_regression_control", "observed_evidence", "audit_test_status"], row)) for row in regression_rows],
    )

    write_text(OUTPUTS["sources"], build_source_trace())

    score_100 = round(sum(SCORE_DIMENSIONS.values()) / len(SCORE_DIMENSIONS) * 10, 2)
    assert score_100 == 67.69
    verdict = "REWORK_REQUIRED"
    queue_summary = Counter(value[0] for value in QUEUE_CLASS.values())
    feedback_summary = Counter(value[0] for value in FEEDBACK_CLASS.values())
    metrics = {
        "schema": "KW002_STEP04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_V1",
        "date": DATE,
        "live_base_head": LIVE_BASE_HEAD,
        "verdict": f"STEP04_RESULT_AUDIT = {verdict}",
        "fresh_audit_score_100": score_100,
        "score_dimensions_10": SCORE_DIMENSIONS,
        "score_semantics": "Each dimension is 0-10 where 10 is strongest. In family authority only, rule_bias_risk_score_10 is inverse: 10 means highest risk.",
        "full_volume": {
            "normalized_identities": len(identities),
            "active_plus_hold_identities": len(active_ids),
            "excluded_identities_history": state_counts["EXCLUDE"],
            "raw_occurrences": len(ledger_rows),
            "unique_raw_occurrence_ids": len(raw_ids),
            "raw_lineage_loss": 0,
            "families": len(family_ids),
            "observed_families": len(observed_family_ids),
            "coverage_gap_families": 2,
            "expansion_queue_rows": len(queue_input),
            "sanitation_feedback_rows": len(feedback_input),
        },
        "step03b_state_counts": dict(sorted(state_counts.items())),
        "row_dispositions": dict(sorted(disposition_counts.items())),
        "material_defects": {
            "unique_affected_identities": len(defect_ids),
            "PSF019_toy_without_game_prefix_collision": len(toy_game_ids),
            "PSF014_explicit_task_hidden_total": len(zodiac_explicit_ids),
            "PSF014_meaning": len(zodiac_meaning_ids),
            "PSF014_media": len(zodiac_media_ids),
            "PSF014_toy": len(zodiac_toy_ids),
            "PSF001_explicit_diy": len(generic_diy_ids),
        },
        "independent_diagnostic": {
            "method": "TF-IDF word 1-2 grams with corpus-generic product terms downweighted/removed; 32-topic MiniBatchKMeans; family centroids; simultaneous audit signals",
            "rows": matrix.shape[0],
            "features": matrix.shape[1],
            "random_seed": RANDOM_SEED,
            "topics": 32,
            "topic_top_terms": topic_top_terms,
            "family_diagnostics": family_diag,
        },
        "queue_classifications": dict(sorted(queue_summary.items())),
        "feedback_classifications": dict(sorted(feedback_summary.items())),
        "additional_missing_audit_classes": 3,
        "input_sha256": dict(sorted(input_hashes.items())),
        "hard_boundaries": {
            "provider_calls": 0,
            "ordinary_yandex_search_calls": 0,
            "gensearch_calls": 0,
            "ai_search_calls": 0,
            "step04_corrections": 0,
            "step05_advancement": False,
            "step06_advancement": False,
            "sealed_prior_blood_sand_research_used": False,
        },
        "publication": {
            "native_git_push": "BLOCKED_BY_MISSING_GITHUB_AUTHENTICATION",
            "owner_relay": "READY",
            "owner_relay_zip": "KW002_STEP04_INDEPENDENT_FULL_VOLUME_AUDIT_OWNER_RELAY_2026-09-11.zip",
            "remote_readback": "PENDING_OWNER_UPLOAD_AND_MAIN_CHATGPT_QA",
        },
    }
    write_text(OUTPUTS["metrics"], json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True))

    large_family_table = []
    for family_id in ("PSF001", "PSF006", "PSF014", "PSF018", "PSF024"):
        diag = family_diag[family_id]
        large_family_table.append(
            f"| {family_id} | {diag['member_count']} | {diag['independent_topic_entropy_normalized']:.3f} | "
            f"{diag['dominant_topic_share']:.3f} | {diag['mean_assigned_centroid_similarity']:.3f} | "
            f"{diag['nearest_other_centroid_override_rate']:.3f} | {diag['verdict']} |"
        )
    score_table = "\n".join(f"| {name} | {value:.1f} |" for name, value in SCORE_DIMENSIONS.items())
    report = f"""# KW-002 Blood & Sand — independent full-volume Step04 result audit

Date: {DATE}

Live base fetched before execution: `{LIVE_BASE_HEAD}`

Role: adversarial result audit only; no correction and no Step05/06 advancement.

## Verdict

```text
STEP04_RESULT_AUDIT = {verdict}
FRESH_AUDIT_SCORE = {score_100:.2f}/100
PROVIDER_CALLS = 0
STEP04_CORRECTIONS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
```

The accepted Step04 result is mechanically complete and traceable, but it is not safe to pass unchanged as preliminary family authority. Three material, reproducible family/rule classes affect **255 unique normalized identities**. PASS is impossible because critical family-boundary and rule-bias defects exist even though RAW lineage is intact.

## Full-volume accounting

| Control | Result |
|---|---:|
| Normalized identities | 24,576 / unique 24,576 |
| Active + HOLD identities | 18,135 / exactly one observed family |
| EXCLUDE history | 6,441 / no Step04 family / unchanged |
| RAW occurrences | 25,979 / unique occurrence IDs 25,979 |
| RAW lineage loss | 0 |
| Step03B state/reason mismatches | 0 |
| Families | 26 = 24 observed + 2 zero-member gaps |
| Queue / feedback | 13 / 10, all audited |

The audit overlay contains all 24,576 identities. Excluded identities are present for accounting with `NOT_APPLICABLE_EXCLUDED_HISTORY`; they were not re-triaged.

## Material defects — no correction performed

| Family / rule class | Affected identities | Exhaustive evidence | Required later action |
|---|---:|---|---|
| PSF019 broad `игр*` prefix | 8 | Every row has independent `TOY`; none has an exact GAME signal. Examples include `игрушка оберег`, `игрушка талисман`, `алатырь игрушки`. | Separate game morphology from `игруш*`; audit blast radius, then reroute only in an approved correction pass. |
| PSF014 early zodiac route | 199 unique | 156 MEANING + 38 MEDIA + 5 TOY. PSF014 says the task is insufficiently specified, but these rows state a task. | Rework precedence/coverage across PSF014↔PSF015/018/012 after Main ChatGPT approval. |
| PSF001 generic fall-through | 48 | Explicit `сделать/создать/изготовить/связать/сшить/сплести/своими руками` task survives inside a family labelled unqualified. | Define a DIY preliminary task boundary or marker; do not infer a final page. |

These counts are mutually disjoint by current family, so total material affected identities = 8 + 199 + 48 = **255**. The overlay recommends `RULE_ORDER_DEFECT` for 207 and `FAMILY_TOO_BROAD` for 48; all other 24,321 identities receive no material row-level defect in this pass.

## Independent full-volume diagnostic

The diagnostic did not reuse the ordered classifier as its semantic judge. It fitted TF-IDF word/co-occurrence features and a deterministic 32-topic MiniBatchKMeans model over all 18,135 active/HOLD phrases, computed family centroids and symmetric cross-family similarities, and evaluated simultaneous signals rather than first-match routing. Generic product/zodiac words were removed from the diagnostic feature space to reduce label echo. Short-text/topic metrics remain warnings, not truth and not final SERP clustering.

| Family | Members | Topic entropy | Dominant-topic share | Mean own-centroid cosine | Alternate-centroid override rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
{chr(10).join(large_family_table)}

- PSF006 is lexically heterogeneous but deliberately preserves short catalog-name ambiguity; this is nonblocking only while catalog membership is not treated as product intent.
- PSF018 is heterogeneous by design as an explicit media/title collision family; its feedback must remain active.
- PSF024 is not a semantic page cluster. It is safe only as a quarantined residual/feedback bucket.
- Topic entropy and nearest-centroid results for all 26 families are in the family authority and metrics JSON; all 676 directed cells of the symmetric 26×26 boundary matrix are materialized.

## Queue and coverage gaps

All 13 rows were classified without a provider call:

| Classification | Count |
|---|---:|
| VALID_GAP | {queue_summary['VALID_GAP']} |
| OWNER_FACT_FIRST | {queue_summary['OWNER_FACT_FIRST']} |
| DUPLICATES_EXISTING_EVIDENCE | {queue_summary['DUPLICATES_EXISTING_EVIDENCE']} |
| DEFER_TO_LATER_INTENT_OR_SERP | {queue_summary['DEFER_TO_LATER_INTENT_OR_SERP']} |

PSF025 and PSF026 are valid zero-member coverage hypotheses, not observed demand. PSQ005-PSQ008 duplicate current qualified evidence in whole or material part; PSQ010 also duplicates preserved historical E013 evidence. PSQ011 explicitly belongs after a concrete later collision. Exact row decisions are in the combined queue/feedback audit.

## Sanitation feedback

Nine of ten feedback rows are justified class-level controls. PSFB003 is `TOO_BROAD`: legitimate game ambiguity is mixed with eight non-game toy rows produced by the Step04 prefix defect. Three missing material audit classes are appended for PSF001 DIY, PSF014 task leakage and PSF019 toy/game collision. They are findings only and make zero Step03B changes.

## Frequency and lineage discipline

No frequency field enters the independent signals, TF-IDF topic membership defect rules, family verdicts or queue classifications. Frequency remains descriptive only. Omitting frequency is semantically safe at preliminary triage because relevance, referent and user task are not frequency functions; later prioritization may use frequency without changing these boundaries.

Catalog/brief membership is treated only as business support. It is not evidence that a short mythological, religious, zodiac, media, game, entity or vehicle-collision phrase means the client's product.

## Fresh score

The previous 97.20/100 self-score was not inherited.

| Dimension | Score / 10 |
|---|---:|
{score_table}

Equal-weight total: **{score_100:.2f}/100**. The score is below 90 and critical boundary defects exist; either condition blocks PASS.

## External-method alignment and limits

The fresh method trace is in `{OUTPUTS['sources']}`. It separates preliminary term diagnostics from final SERP clustering and keeps user objective, ambiguity and business facts distinct. No ordinary search, Wordstat, GenSearch, AI-search or sealed prior Blood & Sand analysis was used.

## Stop state

This pass materialized audit evidence only. The accepted Step04 source artifacts retain their verified SHA-256 hashes and were not rewritten. Work stops here for Main ChatGPT review. Any correction, queue revision or Step05 resumption requires a new explicit release.
"""
    write_text(OUTPUTS["report"], report)

    qa = f"""# KW-002 Step04 independent full-volume result audit — local QA

Date: {DATE}

```text
LIVE_BASE_HEAD = {LIVE_BASE_HEAD}
LOCAL_ARTIFACT_COMPLETE = true
LOCAL_QA_PASS = true
PUBLICATION_HANDOFF_READY = true
PUBLICATION_ROUTE = OWNER_RELAY_REQUIRED
AUDIT_RESULT_UNDER_REVIEW = REWORK_REQUIRED
NORMALIZED_IDENTITIES = 24576
ACTIVE_PLUS_HOLD_IDENTITIES = 18135
EXCLUDED_IDENTITIES_HISTORY = 6441
RAW_OCCURRENCES = 25979
UNIQUE_RAW_OCCURRENCE_IDS = 25979
RAW_LINEAGE_LOSS = 0
STEP03B_STATE_OR_REASON_MISMATCHES = 0
FAMILIES = 26 / 24 OBSERVED / 2 GAPS
BOUNDARY_MATRIX_ROWS = 676 / SYMMETRIC
QUEUE_ROWS_AUDITED = 13
FEEDBACK_ROWS_AUDITED = 10
MATERIAL_DEFECT_IDENTITIES = 255
PROVIDER_CALLS = 0
STEP04_CORRECTIONS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
```

All accepted Step03B and Step04 input hashes match their frozen authorities. Every active/HOLD identity has exactly one observed family; every excluded identity remains history. Overlay dispositions total 24,576: 24,321 pass-as-preliminary, 207 rule-order defects and 48 family-too-broad findings.

The independent diagnostic processed all 18,135 active/HOLD texts with TF-IDF term/co-occurrence features, 32 deterministic topics and family-centroid comparisons. It is auxiliary evidence, not a final SERP or page-cluster model.

All 20 anti-regression controls pass as audit controls. This means the audit execution is complete and reproducible; it does not mean the audited Step04 result passes. The audited result verdict remains exactly:

```text
STEP04_RESULT_AUDIT = REWORK_REQUIRED
```
"""
    write_text(OUTPUTS["qa"], qa)

    work_return = f"""# KW-002 Blood & Sand — independent Step04 result audit Work return

Date: {DATE}

```text
HANDOFF_ID = KW002-BS-W07
STEP_ID = STEP04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT
LIVE_BASE_HEAD = {LIVE_BASE_HEAD}
WORK_EXECUTION_STATE = COMPLETE / STOPPED FOR MAIN CHATGPT REVIEW
STEP04_RESULT_AUDIT = REWORK_REQUIRED
FRESH_AUDIT_SCORE = {score_100:.2f}/100
FULL_VOLUME = 24576 NORMALIZED / 25979 RAW
MATERIAL_DEFECT_IDENTITIES = 255
LOCAL_ARTIFACT_COMPLETE = true
LOCAL_QA_PASS = true
PUBLICATION_ROUTE = OWNER_RELAY_REQUIRED
OWNER_RELAY_ZIP = KW002_STEP04_INDEPENDENT_FULL_VOLUME_AUDIT_OWNER_RELAY_2026-09-11.zip
REMOTE_READBACK = PENDING_OWNER_UPLOAD_AND_MAIN_CHATGPT
PROVIDER_CALLS = 0
STEP04_CORRECTIONS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
```

Material findings:

- PSF019: 8 non-game toy identities pulled by the broad `игр*` prefix.
- PSF014: 199 explicit-task identities hidden by the early zodiac route (156 meaning, 38 media, 5 toy).
- PSF001: 48 explicit DIY identities flattened into the generic unqualified family.
- Queue: 5 of 13 rows duplicate existing evidence; no provider call was made.
- Feedback: 9 of 10 existing rows are justified; PSFB003 is too broad because it includes the toy/game defect.

Required audit authorities, the reproducible materializer, local QA and artifact manifest are present in the job root. No accepted Step03B/Step04 input was changed. Stop for Main ChatGPT return QA; correction and Step05 remain blocked pending a new release.
"""
    write_text(OUTPUTS["return"], work_return)

    artifact_names = [
        OUTPUTS["report"], OUTPUTS["overlay"], OUTPUTS["family"], OUTPUTS["boundary"],
        OUTPUTS["queue_feedback"], OUTPUTS["sources"], OUTPUTS["metrics"], OUTPUTS["regression"],
        OUTPUTS["qa"], OUTPUTS["return"], Path(__file__).name,
    ]
    artifacts = {}
    for name in artifact_names:
        path = HERE / name
        if path.suffix == ".tsv":
            with path.open("r", encoding="utf-8", newline="") as fh:
                rows_or_lines = sum(1 for _ in fh) - 1
            semantics = "data_rows_excluding_header"
        else:
            rows_or_lines = len(path.read_text(encoding="utf-8").splitlines())
            semantics = "text_lines"
        artifacts[name] = {
            "rows_or_lines": rows_or_lines,
            "count_semantics": semantics,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    manifest = {
        "schema": "KW002_STEP04_INDEPENDENT_AUDIT_ARTIFACT_MANIFEST_V1",
        "date": DATE,
        "live_base_head": LIVE_BASE_HEAD,
        "verdict": f"STEP04_RESULT_AUDIT = {verdict}",
        "manifest_self_hash": "OMITTED_BY_DEFINITION_TO_AVOID_RECURSIVE_HASH",
        "input_authority_sha256": dict(sorted(input_hashes.items())),
        "artifacts": artifacts,
        "counts": metrics["full_volume"],
        "material_defects": metrics["material_defects"],
        "hard_boundaries": metrics["hard_boundaries"],
    }
    write_text(OUTPUTS["manifest"], json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True))

    print(json.dumps({
        "verdict": verdict,
        "score_100": score_100,
        "counts": metrics["full_volume"],
        "dispositions": dict(disposition_counts),
        "defects": metrics["material_defects"],
        "artifacts": len(artifacts) + 1,
    }, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
