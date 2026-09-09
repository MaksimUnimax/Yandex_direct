# MK05 — SEO-ТЗ на внедрение

Status: **PLANNED / START ONLY AFTER MK04 OWNER GATE**

## Yandex-only boundary

Работа выполняется **только для SEO-решений под Яндекс**. Если исходная аналитика клиента основана на Google, она не принимается автоматически как доказанная authority для Яндекса. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в base scope не входят. Обязательная общая политика: `../YANDEX_ONLY_SCOPE.md`.

## Продажа

Клиент получает implementation-ready инструкцию для разработчика/контентщика по уже доказанным SEO-действиям: точный объект, URL, место изменения, содержание, ограничения, dependency и acceptance criteria.

## Критическая граница

Base scope не является скрытым полным SEO-исследованием. На входе нужна достаточно надёжная decision authority под Яндекс; если её нет, требуется отдельный research add-on или другой mini-kwork.

## Планируемый KW-001 extraction

Current-site freshness/recheck gates + Step12 action semantics + Step18 execution-ticket completeness and prioritization boundaries + Step19 recipient packaging + Step20 report-specific QA.

Особое внимание переносится из реальных ошибок Document №02 KW-001: generic steps, ambiguous placement, analysis left to implementer, placeholders, misleading sequence, duplicate link decisions, missing methodological sources, leakage of internal IDs.

## Обязательные будущие файлы

Полный набор mini-kwork Level1 method + `tests/OKNO_MSK/*` после завершения MK04. Каждый будущий client-facing и QA-файл обязан явно повторять Yandex-only boundary согласно `../YANDEX_ONLY_SCOPE.md`.
