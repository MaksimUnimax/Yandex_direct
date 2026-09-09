# MK01 — Семантическое ядро для сайта: сбор, чистка и кластеризация

Status: **PRODUCT SCOPE + CLIENT INPUT FROZEN / KW-001 EXTRACTION IN PROGRESS**

## Рабочее название карточки

**Семантическое ядро для сайта: сбор, чистка и кластеризация**

Название зафиксировано после проверки живых формулировок Kwork. Яндекс не выносится в заголовок искусственной конструкцией «для Яндекса», но Yandex-only scope обязан быть явно указан в описании, составе работ, входных данных, FAQ, deliverable и QA.

## Yandex-only boundary

Работа выполняется **только для экосистемы Яндекса**: Яндекс Wordstat и обычная выдача Яндекса в пределах метода MK01. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в base scope не входят. Обязательная общая политика: `../YANDEX_ONLY_SCOPE.md`.

## Продажа

Клиент покупает самостоятельный результат: очищенное и сгруппированное семантическое ядро под реальный бизнес и спрос Яндекса.

Точный контракт продукта уже заморожен в `PRODUCT_SCOPE.md`.

Точный контракт входных данных уже заморожен в `CLIENT_INPUT_CONTRACT.md`.

## Зафиксированные продуктовые границы

- базовый MK01 сейчас предназначен для **существующего публичного сайта**;
- одна основная региональная область исследования является проверенным стартовым режимом; окончательные коммерческие multi-region limits замораживаются после rehearsal/economics;
- доступ к Яндекс Вебмастеру / Метрике / Директу не обязателен;
- Step5A competitor semantic expansion исключён из base MK01 и относится к MK03 / будущему явно оценённому add-on;
- ordinary Yandex Search используется точечно только для материальных спорных semantic/intent boundaries;
- MK01 заканчивается на semantic core + clustering и не включает page ownership / architecture / developer TZ;
- greenfield/no-site mode не заявляется как уже валидированный MK01 режим;
- Google research/tooling не входит.

## Не продаём скрытно

- полный SEO-аудит;
- полную архитектуру сайта;
- page ownership;
- implementation-ready ТЗ разработчику;
- полный конкурентный SEO-аудит;
- Step5A competitor expansion в base package;
- полный Alice/AEO layer;
- Google SEO / Google Ads / Google Keyword Planner / Google Search validation.

## KW-001 extraction boundary

Autonomous MK01 method extracts only:

```text
Step 0  scope freeze
Step 1  existing-site / business discovery
Step 2  seed / acquisition plan
Step 3  Yandex Wordstat acquisition
Step 4  first triage
Step 5  targeted second acquisition only when justified
Step 5A excluded from base MK01
Step 6/6A excluded unless later explicitly validated/added
Step 7  row-level semantic cleanup
Step 8  semantic freeze/routing
Step 9  targeted ordinary Yandex Search narrow controls only
Step 10 task/intent clustering
Step 19 recipient materialization rules relevant to MK01
Step 20 final data/workbook/recipient QA relevant to MK01
```

Steps 11–18 are not silently inherited.

## Обязательные файлы MK01

| File | State |
|---|---|
| `PRODUCT_SCOPE.md` | **DONE** |
| `CLIENT_INPUT_CONTRACT.md` | **DONE** |
| `GENERAL_RULES.md` | IN PROGRESS |
| `STEP_RULES_INDEX.md` | PENDING EXTRACTION |
| `steps/*` | PENDING EXTRACTION |
| `DELIVERABLE_SPEC.md` | PENDING |
| `ERRORS_AND_LESSONS.md` | PENDING |
| `QA_AND_RELEASE.md` | PENDING |
| `KWORK_CARD.md` | PENDING REHEARSAL |
| `PORTFOLIO_ASSET_SPEC.md` | PENDING REHEARSAL |
| `tests/OKNO_MSK/*` | PENDING AUTONOMOUS MK01 REHEARSAL |

Каждый клиентский и QA-файл обязан явно повторять Yandex-only boundary согласно `../YANDEX_ONLY_SCOPE.md`; одной внутренней ссылки недостаточно.

## Productization roadmap

```text
PHASE 0  PRODUCT PROMISE FREEZE                 = PASS
PHASE 1  MARKET REALITY BASELINE               = PASS / REFRESH AGAIN BEFORE CARD
PHASE 2  CLIENT INPUT CONTRACT                 = PASS
PHASE 3  KW-001 METHOD/FAILURE EXTRACTION      = IN PROGRESS
PHASE 4  AUTONOMOUS MK01 ROADMAP               = PENDING
PHASE 5  OKNO_MSK MK01-ONLY REHEARSAL          = PENDING
PHASE 6  MK01 CLIENT DELIVERABLE               = PENDING
PHASE 7  QA                                    = PENDING
PHASE 8  PRICE/LIMITS/ECONOMICS FREEZE         = PENDING
PHASE 9  KWORK CARD                            = PENDING
PHASE 10 PORTFOLIO ILLUSTRATION                = PENDING
PHASE 11 OWNER PUBLICATION                     = PENDING OWNER ACTION
PHASE 12 PUBLISHED VERSION FREEZE/READBACK      = PENDING
```

## Current next action

```text
READ ALL RELEVANT KW-001 AUTHORITIES
→ EXTRACT COMMON RULES
→ EXTRACT PER-STEP METHODS
→ EXTRACT ALL RELEVANT FAILURE CLASSES / ROOT CAUSES / NON-REPEAT CONTROLS
→ MATERIALIZE GENERAL_RULES.md + STEP_RULES_INDEX.md + steps/* + ERRORS_AND_LESSONS.md
```
