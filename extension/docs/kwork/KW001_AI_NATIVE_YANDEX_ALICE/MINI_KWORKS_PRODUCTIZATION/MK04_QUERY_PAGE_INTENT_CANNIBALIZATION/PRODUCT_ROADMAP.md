# MK04 — Запрос → страница + интенты + каннибализация

Status: **PLANNED / START ONLY AFTER MK03 OWNER GATE**

## Yandex-only boundary

Работа выполняется **только для экосистемы Яндекса**. Интенты, query/page mapping, спорные границы и каннибализация проверяются по Яндекс-данным и текущему сайту. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в base scope не входят. Обязательная общая политика: `../YANDEX_ONLY_SCOPE.md`.

## Продажа

Клиент получает проверенную модель `query/family/user task → exact owner/family route/supporting page` и диагностику конкурирующих страниц.

## Base input boundary

Base scope предполагает существующий semantic set клиента или отдельно приобретённый MK01. Полный новый Wordstat collection нельзя незаметно включать в эту цену. Если входное ядро клиента собрано по Google, его нельзя автоматически трактовать как подтверждённый спрос Яндекса: нужна отдельная проверка/нормализация в рамках согласованного Yandex-only scope.

## Планируемый KW-001 extraction

Step0–1 scope/current site + Step8 frozen input contract + Step9 Yandex Search validation + Step10 task/intent clustering + Step11 ownership + Step12 action boundary + Step13 cannibalization + Step14 topology/architecture reconciliation + Steps19–20 materialization/QA.

## Обязательные будущие файлы

Полный набор mini-kwork Level1 method + `tests/OKNO_MSK/*` после завершения MK03. Каждый будущий client-facing и QA-файл обязан явно повторять Yandex-only boundary согласно `../YANDEX_ONLY_SCOPE.md`.
