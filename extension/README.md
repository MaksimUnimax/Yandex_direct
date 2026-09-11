# extension/

Постоянная зона разработки **Yandex Marketing Bridge**.

## ОБЯЗАТЕЛЬНО ПЕРЕД ЛЮБЫМ ПАТЧЕМ И ПЕРЕД ЛЮБОЙ ВЫДАЧЕЙ СБОРКИ

Главное owner-locked правило патчей, проверки затронутых зависимостей и ресурсной безопасности:

`docs/YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`

Его необходимо прочитать **до изменения production-кода** и повторно применить **до handoff любого installable ZIP/build**.

Критические положения:

- после каждого материального изменения строится dependency-impact matrix и тестируются **все реально затронутые зависимости**;
- функциональный PASS не заменяет memory/performance/resource PASS для больших файлов, больших строк, batch, storage, Base64, ArrayBuffer/Blob/File, polling/timers/observers/ports и других масштабируемых контуров;
- обязательный resource/browser test со статусом `BLOCKED`, `NOT_RUN`, `FAIL_HARNESS` или `FAIL` **запрещает выдачу сборки владельцу**;
- для крупных файлов обязательна stress-матрица минимум `1 MB / 10 MB / 32 MB / 64 MB`; для масштабируемого batch — минимум `10 / 100 / 500 / 1500` items, если функция рассчитана на такие объёмы;
- инцидент YMB 0.1.5 с многократной материализацией большого payload, Base64/storage amplification и повторным full-store read является постоянным отрицательным regression-case;
- exact installable artifact должен пройти fresh-extraction/package identity проверки и быть теми же байтами, для которых получена приёмка.

Если правило безопасности конфликтует с менее строгим feature-specific документом, действует более строгий `YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`, если владелец явно не распорядился иначе.

## Текущая версия

```text
Yandex Marketing Bridge = 0.1.2
```

Authoritative version fields:

- `src/manifest.json`
- `src/shared/product.js`
- `src/package.json`

Текущее функциональное изменение Search Batch `nextN` и его acceptance evidence:

`docs/SEARCH_BATCH_NEXTN100_V0_1_2_CHANGELOG_AND_ACCEPTANCE_2026-08-29.md`

Структура:

- `docs/` — каноническая проектная документация: цель, ТЗ, roadmap, reference baseline, append-only контекст разработки и обязательный pre-delivery regression gate.
- `src/` — рабочий исходный код расширения.
- `tests/` — тесты unified-расширения, phase/checkpoint evidence и validation reports.
- `reference/` — неизменяемый предоставленный владельцем reference Wordstat Bridge 1.1.5 и его артефакты.

## Обязательное правило тестирования

Во время разработки/исправления бага выполняются **только сфокусированные тесты по изменяемому коду и всем затронутым зависимостям** плюс необходимые static/syntax/changed-line и, когда применимо, resource/memory/performance проверки.

Обязательная authority для определения scope этих проверок:

`docs/YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`

Только когда работа над изменением закончена и готовая сборка уже собирается передаваться владельцу, точный кандидат замораживается и Codex обязан **одним полным прогоном** пройти:

`docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`

Этот Gate охватывает весь функционал, который Codex способен надёжно проверить. Любой обязательный FAIL блокирует передачу сборки. То же относится к обязательному `BLOCKED` / `NOT_RUN` доказательству безопасности из `YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`: оно не может быть засчитано как PASS и блокирует handoff.

После исправления дефекта весь applicable Gate прогоняется на новом точном кандидате в соответствии с текущими authority.

Gate является живым документом: новый/изменённый функционал должен получать соответствующие regression tests; тесты удаляются только вместе с намеренным удалением соответствующего функционала.

## Инвариант

`extension/` не используется для данных конкретного заказа. Любые клиентские данные и результаты рабочих API-съёмов должны находиться только в `work/<job_id>/`.
