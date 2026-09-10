# MK03 — SEO-анализ конкурентов + семантические/структурные пробелы

Status: **PLANNED / START ONLY AFTER MK02 OWNER GATE**

## MANDATORY SERIES DEVELOPMENT AUTHORITY — READ FIRST

Before any MK03 productization work, first fully read:

`../MINI_KWORK_DEVELOPMENT_PROTOCOL.md`

Then read `../SERIES_ROADMAP.md`, `../YANDEX_ONLY_SCOPE.md`, this roadmap, and only after that extract the required current KW-001 authorities.

```text
DEVELOPMENT PROTOCOL = HOW TO BUILD MK03
MK03 LEVEL-1 RULES = HOW TO EXECUTE MK03 AFTER THEY ARE BUILT
OKNO_MSK = LEVEL-2 REHEARSAL EVIDENCE
WORK = LARGE-DATA EXECUTOR AFTER LEVEL-1 METHOD PASS
```

Do not start MK03 by copying MK02, by reading OKNO_MSK results first, or by asking Work to invent the method.

## Yandex-only boundary

Работа выполняется **только для экосистемы Яндекса**: реальные конкуренты определяются по текущей выдаче Яндекса, новый спрос подтверждается Яндекс Wordstat, а query→competitor visibility — текущей выдачей Яндекса. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в base scope не входят. Обязательная общая политика: `../YANDEX_ONLY_SCOPE.md`.

## Продажа

Клиент получает проверенных реальных Search-конкурентов, missed topics/seeds, подтверждение спроса, tested query→competitor visibility там, где заявляется такое отношение, и список подтверждённых gaps.

## Критическая граница

```text
COMPETITOR PAGE TOPIC != EXACT QUERY RANKING
TESTED QUERY VISIBILITY != FULL COMPETITOR KEYWORD UNIVERSE
COMPETITOR-DERIVED SEED != FINAL KEYWORD
```

Не обещаем полный reverse-domain SEO-аудит без соответствующего evidence provider. Не обещаем Google-конкурентов или Google keyword universe.

## Планируемый KW-001 extraction

Scope/business/site basics + Step5A permanent competitor method + необходимые Step3/5 Wordstat durability rules + targeted current Yandex Search + Step7/8 merge/cleanup + mini-deliverable/QA rules Steps19–20.

Extraction выполняется по `../MINI_KWORK_DEVELOPMENT_PROTOCOL.md`: переносится не номер шага, а актуальная методика, failure history, root causes, non-repeat controls, claim boundaries и PASS gates. До consistency PASS Level-1 метода большой OKNO_MSK dataset не обрабатывается.

## Обязательные будущие файлы

Полный набор mini-kwork Level1 method + `tests/OKNO_MSK/*` после завершения MK02. Каждый будущий client-facing и QA-файл обязан явно повторять Yandex-only boundary согласно `../YANDEX_ONLY_SCOPE.md`.

После Level-1 method consistency PASS большой OKNO_MSK rehearsal передаётся в Work отдельным закрытым Phase-5 handoff. Work выполняет уже утверждённый метод и сообщает доказанные method defects, но не меняет продуктовую архитектуру самовольно.
