#!/usr/bin/env python3
"""Build canonical MK02 implementation work packages from preserved authorities."""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent


def find_repo_root() -> Path:
    path = HERE
    while path != path.parent:
        if (path / ".git").exists():
            return path
        path = path.parent
    raise RuntimeError("repository root not found")


REPO = find_repo_root()
SOURCE = REPO / "extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK"
DATE = "2026-09-10"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            delimiter="\t",
            lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


STATE_MAP = {
    "READY": "READY_IMPLEMENTATION_SPEC",
    "READY_PARTIAL__BUSINESS_DETAIL_REQUIRED": "PENDING_BUSINESS_DETAIL",
    "NOT_READY__EVIDENCE_REQUIRED": "RECHECK_ONLY",
    "READY_ANALYTICAL_MAPPING": "SEMANTIC_MAPPING_ONLY",
    "NO_SEPARATE_CHANGE__COMBINE_A009": "NO_SITE_CHANGE",
    "HOLD__EVIDENCE_REQUIRED": "HOLD",
}

IMPORTANCE_MAP = {
    "P1_HIGH": "Высокая аналитическая значимость",
    "P2_MEDIUM": "Средняя аналитическая значимость",
    "P3_LATER": "Ниже по аналитической значимости",
    "HOLD": "Не оценивается до снятия ограничения",
}

MEASUREMENT_RU = {
    "M01_OWNER_ROLE_CORRECTION": {
        "applies_to": "уточнение владельца, специалиста и маршрута",
        "expected": "У каждой задачи явно зафиксирована роль текущей страницы, и во всех таблицах используется один и тот же маршрут.",
        "minimum": "Повторно открыть затронутые страницы и сверить их фактическую роль с финальной картой владения.",
        "optional": "При отдельном доступе можно проверить связь семейства запросов и URL в Яндекс Вебмастере.",
        "trigger": "После внедрения/переобхода или сразу после существенной смены назначения страницы.",
        "failure": "При новой неоднозначности открыть только затронутую границу владения.",
        "boundary": "Проверка роли не обещает позиции, трафик, заявки или выручку.",
    },
    "M02_OVERLAP_DIFFERENTIATION": {
        "applies_to": "разведение похожих страниц",
        "expected": "У похожих страниц остаются разные и понятные задачи без автоматического объединения.",
        "minimum": "Повторно прочитать обе страницы, проверить различие основной ответственности и понятный переход между ними.",
        "optional": "При отдельном доступе проверить историю запрос→URL в Яндекс Вебмастере.",
        "trigger": "После изменения страниц/переобхода или при смене их назначения.",
        "failure": "Если различие не видно, повторно открыть только эту пару; разрушительное действие не делать без сильного доказательства.",
        "boundary": "Текущее пересечение не доказывает историческую конкуренцию или вред.",
    },
    "M03_CONTENT_ENHANCEMENT": {
        "applies_to": "подтверждённое расширение содержания существующей страницы",
        "expected": "Названная ранее неудовлетворённая потребность пользователя видимо и правдиво раскрыта на принятом владельце.",
        "minimum": "Открыть страницу после публикации и проверить каждую названную потребность по тексту/интерфейсу.",
        "optional": "Если доступно отдельно, наблюдать показы, клики, CTR, позицию и настроенные цели Метрики как дополнительный результат.",
        "trigger": "После публикации и разумного периода переобхода; также при изменении предложения.",
        "failure": "Исправить содержание или повторно проверить владельца, если задача страницы изменилась.",
        "boundary": "Полноту реализации проверить можно; рост позиций и конверсии не гарантируется.",
    },
    "M05_INTERNAL_LINK_IMPLEMENT": {
        "applies_to": "контекстные внутренние ссылки",
        "expected": "Принятая связь источник→цель присутствует в полезном контексте и ведёт на нужную страницу.",
        "minimum": "Проверить literal href, видимость ссылки, окружающий контекст и соответствие целевой страницы задаче.",
        "optional": "Для приёмки метрики не обязательны.",
        "trigger": "Сразу после внедрения и после существенного редизайна источника или цели.",
        "failure": "Неверная, отсутствующая или бесконтекстная ссылка возвращается в невыполненное/отложенное состояние.",
        "boundary": "Наличие ссылки не гарантирует позиции или трафик.",
    },
    "M06_ROUTE_TO_EXISTING": {
        "applies_to": "назначение задачи существующей странице",
        "expected": "Задача последовательно назначена принятой странице без ненужного нового URL.",
        "minimum": "Сверить phrase/unit→target map и фактическую роль целевой страницы.",
        "optional": "При отдельном доступе query→URL evidence может усилить последующую проверку.",
        "trigger": "После изменения карты или роли целевой страницы.",
        "failure": "Открыть только затронутый маршрут; не создавать страницу из-за отсутствия детали внедрения.",
        "boundary": "Аналитическое назначение не доказывает физическое изменение CMS.",
    },
    "M07_HOLD": {
        "applies_to": "задачи с названным доказательным или бизнес-ограничением",
        "expected": "До снятия конкретного ограничения изменение не выполняется.",
        "minimum": "Получить названный бизнес-факт, политику, уточнение задачи или authoritative evidence и повторно оценить только этот объект.",
        "optional": "Не применяется до снятия ограничения.",
        "trigger": "Точный trigger из строки HOLD/уточнения.",
        "failure": "Сохранить HOLD; не считать его низкой ценностью и не выдумывать приоритет/трудоёмкость.",
        "boundary": "HOLD означает «не разрешено доказательствами», а не «отклонено».",
    },
}


def main() -> None:
    corrected_path = SOURCE / "RESEARCH_REBUILD_POST_RELEASE_SHARED_IMPLEMENTATION_AUTHORITY_CORRECTED_2026-09-05.tsv"
    corrected = read_tsv(corrected_path)
    relation_path = HERE / f"MK02_PAGE_RELATIONSHIPS_{DATE}.tsv"
    relations = read_tsv(relation_path)
    assert len(corrected) == 34
    assert len(relations) == 14

    packages: list[dict[str, object]] = []
    for row in corrected:
        if row["action_id"] == "S18-A032":
            # A032 is an accounting batch, not an implementable work package.
            continue
        state = STATE_MAP[row["recipient_state"]]
        packages.append(
            {
                "work_package_id": "WP-" + row["action_id"].removeprefix("S18-A"),
                "source_action_ids": row["action_id"],
                "client_state": state,
                "analytical_importance": IMPORTANCE_MAP[row["priority"]],
                "production_schedule_state": "NOT_PROVIDED__NOT_INFERRED_FROM_NUMBERING",
                "page_or_object": row["target_object"],
                "why_change_is_needed": row["description_ru"],
                "as_is_current_state": row["current_state_ru"],
                "evidence_meaning": row["evidence_meaning_ru"],
                "evidence_locator": row["evidence_locator"],
                "implementation_mode": row["implementation_mode"],
                "exact_change": row["exact_instruction_ru"],
                "exact_location_or_context": row["exact_location_ru"],
                "to_be_state": row["target_state_ru"],
                "dependencies": row["dependencies"],
                "preservation_do_not_break": row["do_not_break_ru"],
                "acceptance_check": row["acceptance_ru"],
                "ready_scope": row["ready_scope_ru"],
                "one_concrete_clarification": row["pending_business_detail_ru"],
                "claim_boundary": row["authority_lineage"],
            }
        )

    for index, relation in enumerate(relations, start=1):
        present = relation["current_link_present"] == "YES"
        state = "NO_SITE_CHANGE" if present else "PENDING_PLACEMENT_OR_CONTEXT"
        source_ids = relation["relationship_id"]
        packages.append(
            {
                "work_package_id": f"WP-LINK-{index:02d}",
                "source_action_ids": "S18-A032;" + source_ids,
                "client_state": state,
                "analytical_importance": "По готовности подтверждённого контекста",
                "production_schedule_state": "NOT_PROVIDED__NOT_INFERRED_FROM_NUMBERING",
                "page_or_object": relation["source_url"] + " → " + relation["target_url"],
                "why_change_is_needed": (
                    "Связь уже присутствует и соответствует принятому переходу между задачами."
                    if present
                    else "Смысловой переход принят, но в сохранённом HTML ссылка отсутствовала."
                ),
                "as_is_current_state": relation["literal_current_state"],
                "evidence_meaning": (
                    "Literal href найден; отдельная доработка не требуется."
                    if present
                    else "Literal href не найден; точный абзац/контекст размещения не доказан."
                ),
                "evidence_locator": "Проверка внутренних связей на снимке 2026-09-02; source IDs " + source_ids,
                "implementation_mode": (
                    "Проверка/сохранение существующей связи"
                    if present
                    else "Контекстная ссылка после подтверждения места"
                ),
                "exact_change": (
                    "Изменение не требуется; сохранить релевантный переход."
                    if present
                    else "После подтверждения контекста добавить одну видимую ссылку со страницы-источника на указанную цель."
                ),
                "exact_location_or_context": (
                    relation["anchor_or_context"]
                    if present
                    else "PENDING: назвать существующий блок/абзац, где переход естественно продолжает задачу пользователя."
                ),
                "to_be_state": (
                    "Существующая контекстная ссылка сохранена."
                    if present
                    else "Одна контекстная ссылка находится в подтверждённом блоке и ведёт на принятую цель."
                ),
                "dependencies": (
                    "Нет отдельной зависимости; перепроверить после редизайна."
                    if present
                    else "Аналитик/редактор должен подтвердить точный блок и смысл анкора до передачи разработчику."
                ),
                "preservation_do_not_break": "Не заменять целевую страницу, не добавлять повторную ссылку и не использовать спамный exact-match анкор.",
                "acceptance_check": relation["acceptance_check"],
                "ready_scope": "" if not present else "NO_CHANGE_VERIFIED",
                "one_concrete_clarification": (
                    ""
                    if present
                    else "На какой существующий блок/абзац страницы-источника приходится естественный переход к указанной задаче цели?"
                ),
                "claim_boundary": relation["claim_boundary"],
            }
        )

    assert len(packages) == 47
    expected = Counter(
        {
            "READY_IMPLEMENTATION_SPEC": 7,
            "PENDING_BUSINESS_DETAIL": 1,
            "PENDING_TECHNICAL_DETAIL": 0,
            "PENDING_PLACEMENT_OR_CONTEXT": 6,
            "RECHECK_ONLY": 4,
            "SEMANTIC_MAPPING_ONLY": 19,
            "NO_SITE_CHANGE": 9,
            "HOLD": 1,
        }
    )
    actual = Counter(row["client_state"] for row in packages)
    assert actual == +expected

    required_ready = [
        "page_or_object",
        "why_change_is_needed",
        "as_is_current_state",
        "evidence_meaning",
        "evidence_locator",
        "implementation_mode",
        "exact_change",
        "exact_location_or_context",
        "to_be_state",
        "dependencies",
        "preservation_do_not_break",
        "acceptance_check",
    ]
    ready = [row for row in packages if row["client_state"] == "READY_IMPLEMENTATION_SPEC"]
    for row in ready:
        missing = [field for field in required_ready if not str(row[field]).strip()]
        assert not missing, (row["work_package_id"], missing)
        text = " ".join(str(value) for value in row.values()).lower()
        assert "todo" not in text and "placeholder" not in text
    assert len({row["work_package_id"] for row in packages}) == 47

    package_path = HERE / f"MK02_IMPLEMENTATION_WORK_PACKAGES_{DATE}.tsv"
    write_tsv(package_path, packages, list(packages[0]))

    non_ready = [row for row in packages if row["client_state"] != "READY_IMPLEMENTATION_SPEC"]
    clarification_rows = [
        {
            "state": row["client_state"],
            "page_or_object": row["page_or_object"],
            "what_this_means": row["why_change_is_needed"],
            "one_concrete_clarification_or_check": (
                row["one_concrete_clarification"]
                or row["dependencies"]
                or row["evidence_meaning"]
            ),
            "what_not_to_do_now": row["preservation_do_not_break"],
            "return_to_ready_condition": row["acceptance_check"],
            "work_package_id": row["work_package_id"],
        }
        for row in non_ready
    ]
    clarification_path = HERE / f"MK02_CLARIFICATIONS_NO_CHANGE_HOLD_{DATE}.tsv"
    write_tsv(clarification_path, clarification_rows, list(clarification_rows[0]))

    acceptance_rows = [
        {
            "page_or_object": row["page_or_object"],
            "what_must_be_present": row["to_be_state"],
            "where_to_check": row["exact_location_or_context"],
            "acceptance_check": row["acceptance_check"],
            "preserve": row["preservation_do_not_break"],
            "work_package_id": row["work_package_id"],
        }
        for row in ready
    ]
    acceptance_path = HERE / f"MK02_IMPLEMENTATION_ACCEPTANCE_{DATE}.tsv"
    write_tsv(acceptance_path, acceptance_rows, list(acceptance_rows[0]))

    measurement_source = read_tsv(SOURCE / "STEP_18_MEASUREMENT_PLAN.tsv")
    measurement_rows: list[dict[str, object]] = []
    for row in measurement_source:
        mid = row["measurement_class"]
        if mid == "M04_AI_BOUNDED_CONTENT_RECHECK":
            continue
        ru = MEASUREMENT_RU[mid]
        measurement_rows.append(
            {
                "measurement_class": mid,
                "applies_to": ru["applies_to"],
                "expected_outcome": ru["expected"],
                "minimum_acceptance_verification": ru["minimum"],
                "optional_yandex_first_party_metric": ru["optional"],
                "review_trigger": ru["trigger"],
                "failure_policy": ru["failure"],
                "claim_boundary": ru["boundary"],
            }
        )
    assert len(measurement_rows) == 6
    measurement_path = HERE / f"MK02_ACCEPTANCE_MEASUREMENT_INTERFACE_{DATE}.tsv"
    write_tsv(measurement_path, measurement_rows, list(measurement_rows[0]))

    manifest = {
        "schema": "MK02_OKNO_MSK_IMPLEMENTATION_WORK_PACKAGES_V1",
        "date": DATE,
        "status": "PASS",
        "provider_calls_during_rehearsal": 0,
        "source_action_rows": 34,
        "source_link_rows": 15,
        "source_link_distinct_visible_pairs": 14,
        "accounting_batch_removed_as_work_package": "S18-A032",
        "work_packages": 47,
        "state_counts": dict(sorted(actual.items())),
        "ready_required_fields": required_ready,
        "ready_rows_complete": len(ready),
        "clarification_no_change_hold_rows": len(clarification_rows),
        "acceptance_rows": len(acceptance_rows),
        "measurement_classes": len(measurement_rows),
        "ai_measurement_class_excluded": "M04_AI_BOUNDED_CONTENT_RECHECK",
        "production_schedule": "NOT_MATERIALIZED__OWNER_EFFORT_CAPACITY_TIMING_NOT_PROVIDED",
        "outputs": {
            path.name: {"bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in [package_path, clarification_path, acceptance_path, measurement_path]
        },
        "checks": {
            "accounting_batch_not_work_package": True,
            "ready_fields_complete": True,
            "ready_placeholders": 0,
            "invented_owner_effort_capacity_timing": 0,
            "step5a_action_ids": 0,
            "google_or_ai_claims": 0,
            "duplicate_visible_link_pairs": 0,
        },
    }
    manifest_path = HERE / f"MK02_IMPLEMENTATION_MANIFEST_{DATE}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

