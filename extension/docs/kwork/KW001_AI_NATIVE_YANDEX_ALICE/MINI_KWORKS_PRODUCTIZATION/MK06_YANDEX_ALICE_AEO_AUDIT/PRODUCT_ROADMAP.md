# MK06 — Яндекс Нейро / Алиса / AEO-аудит

Status: **PLANNED / START ONLY AFTER MK05 OWNER GATE**

## Yandex-only boundary

Работа выполняется **только внутри экосистемы Яндекса**: ordinary Yandex Search + Алиса / Яндекс Нейро / GenSearch в пределах доказанного метода. Google Search, Google AI Overviews, Google Ads / Keyword Planner, Search Console и другие Google-инструменты в base scope не входят. Обязательная общая политика: `../YANDEX_ONLY_SCOPE.md`.

## Продажа

Клиент получает не обещание попадания в AI-ответ, а доказанную проверку: ordinary Yandex Search baseline → meaningful AI cases → Alice/GenSearch evidence → Search↔AI delta → изменения/NO_CHANGE/de-risk/insufficient.

## Критические границы

- AI не заменяет Ordinary Yandex Search.
- GenSearch observation не выдаётся за consumer Alice observation без основания.
- AI mention не создаёт автоматически страницу/услугу/категорию.
- NO_CHANGE является валидным результатом.
- Не обещаем guaranteed inclusion/citation/traffic/position.
- Google AI/Google Search не подменяют и не дополняют Yandex evidence в base scope.

## Планируемый KW-001 extraction

Scope/current site + достаточный frozen semantic/search input + Yandex Search/task/ownership baseline по нужным случаям + Step14 Search-only freeze + Step15 AI case selection + Step16 AI acquisition controls + Step17 Search-vs-AI comparison + Step18 recommendation readiness + Steps19–20 materialization/QA.

Полный новый semantic acquisition не входит в base scope и может быть add-on/MK01.

## Обязательные будущие файлы

Полный набор mini-kwork Level1 method + `tests/OKNO_MSK/*` после завершения MK05. Каждый будущий client-facing и QA-файл обязан явно повторять Yandex-only boundary согласно `../YANDEX_ONLY_SCOPE.md`.
