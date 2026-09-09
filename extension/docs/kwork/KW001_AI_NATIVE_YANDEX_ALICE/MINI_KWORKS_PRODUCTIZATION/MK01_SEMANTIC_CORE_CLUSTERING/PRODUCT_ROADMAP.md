# MK01 — Семантическое ядро для сайта: сбор, чистка и кластеризация

Status: **NEXT / PRODUCTIZATION NOT YET COMPLETE**

## Рабочее название карточки

**Семантическое ядро для сайта: сбор, чистка и кластеризация**

Название зафиксировано после проверки живых формулировок Kwork. Яндекс не выносится в заголовок искусственной конструкцией «для Яндекса», но Yandex-only scope обязан быть явно указан в описании, составе работ, входных данных, FAQ, deliverable и QA.

## Yandex-only boundary

Работа выполняется **только для экосистемы Яндекса**: Яндекс Wordstat и обычная выдача Яндекса в пределах метода MK01. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в base scope не входят. Обязательная общая политика: `../YANDEX_ONLY_SCOPE.md`.

## Продажа

Клиент покупает самостоятельный результат: очищенное и сгруппированное семантическое ядро под реальный бизнес и спрос Яндекса.

## Не продаём скрытно

- полный SEO-аудит;
- полную архитектуру сайта;
- implementation-ready ТЗ разработчику;
- полный конкурентный SEO-аудит;
- полный Alice/AEO layer;
- Google SEO / Google Ads / Google Keyword Planner / Google Search validation.

## Планируемый KW-001 extraction

Base: Step 0–8, targeted Step9 только для спорных границ, Step10 clustering, затем mini-deliverable materialization и QA по релевантным правилам Steps19–20.

Step5A competitor expansion должен быть отдельно решён как base или add-on при детальной productization MK01; нельзя включить его молча.

## Обязательные будущие файлы

`PRODUCT_SCOPE.md`, `CLIENT_INPUT_CONTRACT.md`, `GENERAL_RULES.md`, `STEP_RULES_INDEX.md`, `steps/*`, `DELIVERABLE_SPEC.md`, `ERRORS_AND_LESSONS.md`, `QA_AND_RELEASE.md`, `KWORK_CARD.md`, `PORTFOLIO_ASSET_SPEC.md`, `tests/OKNO_MSK/*`.

Каждый клиентский и QA-файл обязан явно повторять Yandex-only boundary согласно `../YANDEX_ONLY_SCOPE.md`; одной внутренней ссылки недостаточно.

## Текущий следующий шаг

```text
1. Freeze exact promise and limits.
2. Record exact client inputs.
3. Audit full KW-001 authorities for Steps 0–10 and all failure classes affecting this product.
4. Build autonomous MK01 roadmap.
5. Re-materialize OKNO_MSK as if only MK01 had been purchased.
```
