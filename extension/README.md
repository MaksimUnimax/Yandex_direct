# extension/

Постоянная зона разработки **Yandex Marketing Bridge**.

## Текущая версия

```text
Yandex Marketing Bridge = 0.1.3
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

Во время разработки/исправления бага выполняются **только сфокусированные тесты по изменяемому коду и затронутым зависимостям** плюс необходимые static/syntax/changed-line проверки.

Только когда работа над изменением закончена и готовая сборка уже собирается передаваться владельцу, точный кандидат замораживается и Codex обязан **одним полным прогоном** пройти:

`docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`

Этот Gate охватывает весь функционал, который Codex способен надёжно проверить. Любой обязательный FAIL блокирует передачу сборки. После исправления дефекта весь Gate прогоняется заново с начала на новом точном кандидате.

Gate является живым документом: новый/изменённый функционал должен получать соответствующие regression tests; тесты удаляются только вместе с намеренным удалением соответствующего функционала.

## Инвариант

`extension/` не используется для данных конкретного заказа. Любые клиентские данные и результаты рабочих API-съёмов должны находиться только в `work/<job_id>/`.

### v0.1.3 — Webmaster KW-001 read surface

The v0.1.3 branch expands the accepted read-only Webmaster service with query history, indexing/in-search URL samples and the official asynchronous query×URL export lifecycle. Export tasks are persisted in `chrome.storage.local`, signed downloads are restricted to the official Yandex storage origin, raw CSV plus normalized rows are retained locally, and large evidence is delivered to ChatGPT in bounded chunks. Stateful export POST has no automatic retry and requires explicit quota confirmation; PRO usage additionally requires an explicit PRO confirmation.
