# MK03 — SEO-анализ конкурентов + семантические/структурные пробелы

Status: **PLANNED / START ONLY AFTER MK02 OWNER GATE**

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

## Обязательные будущие файлы

Полный набор mini-kwork Level1 method + `tests/OKNO_MSK/*` после завершения MK02. Каждый будущий client-facing и QA-файл обязан явно повторять Yandex-only boundary согласно `../YANDEX_ONLY_SCOPE.md`.
