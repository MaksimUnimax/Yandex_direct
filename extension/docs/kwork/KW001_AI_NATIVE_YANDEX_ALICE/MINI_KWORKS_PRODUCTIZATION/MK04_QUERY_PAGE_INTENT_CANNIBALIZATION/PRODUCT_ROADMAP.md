# MK04 — Запрос → страница + интенты + каннибализация

Status: **PLANNED / START ONLY AFTER MK03 OWNER GATE**

## MANDATORY SERIES DEVELOPMENT AUTHORITY — READ FIRST

Before any MK04 productization work, first fully read:

`../MINI_KWORK_DEVELOPMENT_PROTOCOL.md`

Then read `../SERIES_ROADMAP.md`, `../YANDEX_ONLY_SCOPE.md`, this roadmap, and only after that extract the required current KW-001 authorities.

```text
DEVELOPMENT PROTOCOL = HOW TO BUILD MK04
MK04 LEVEL-1 RULES = HOW TO EXECUTE MK04 AFTER THEY ARE BUILT
OKNO_MSK = LEVEL-2 REHEARSAL EVIDENCE
WORK = LARGE-DATA EXECUTOR AFTER LEVEL-1 METHOD PASS
```

Do not start from a remembered ownership/cannibalization rule, an old client map, or a Work result.

## Yandex-only boundary

Работа выполняется **только для экосистемы Яндекса**. Интенты, query/page mapping, спорные границы и каннибализация проверяются по Яндекс-данным и текущему сайту. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в base scope не входят. Обязательная общая политика: `../YANDEX_ONLY_SCOPE.md`.

## Продажа

Клиент получает проверенную модель `query/family/user task → exact owner/family route/supporting page` и диагностику конкурирующих страниц.

## Base input boundary

Base scope предполагает существующий semantic set клиента или отдельно приобретённый MK01. Полный новый Wordstat collection нельзя незаметно включать в эту цену. Если входное ядро клиента собрано по Google, его нельзя автоматически трактовать как подтверждённый спрос Яндекса: нужна отдельная проверка/нормализация в рамках согласованного Yandex-only scope.

## Планируемый KW-001 extraction

Step0–1 scope/current site + Step8 frozen input contract + Step9 Yandex Search validation + Step10 task/intent clustering + Step11 ownership + Step12 action boundary + Step13 cannibalization + Step14 topology/architecture reconciliation + Steps19–20 materialization/QA.

Extraction выполняется по `../MINI_KWORK_DEVELOPMENT_PROTOCOL.md`: переносится актуальная accepted method authority и вся релевантная failure/correction history, а не только номера этапов. Сначала Level-1 method + consistency audit; только потом большой OKNO_MSK rehearsal в Work.

## Обязательные будущие файлы

Полный набор mini-kwork Level1 method + `tests/OKNO_MSK/*` после завершения MK03. Каждый будущий client-facing и QA-файл обязан явно повторять Yandex-only boundary согласно `../YANDEX_ONLY_SCOPE.md`.

После Level-1 method consistency PASS Work выполняет отдельный MK04-only rehearsal на Level-2 данных и не имеет права самовольно расширить scope до полного нового semantic collection или соседнего mini-kwork.
