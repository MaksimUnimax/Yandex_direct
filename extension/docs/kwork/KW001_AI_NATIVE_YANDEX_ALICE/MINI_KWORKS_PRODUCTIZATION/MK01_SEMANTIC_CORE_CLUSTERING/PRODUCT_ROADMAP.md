# MK01 — Семантическое ядро для сайта: сбор, чистка и кластеризация

Status: **PHASE 5 OKNO_MSK MK01-ONLY REHEARSAL PASS / PHASE 6 NEXT**

## Рабочее название карточки

**Семантическое ядро для сайта: сбор, чистка и кластеризация**

Яндекс не выносится в заголовок искусственной конструкцией «для Яндекса», но Yandex-only scope обязан быть явно указан в описании, составе работ, входных данных, FAQ, deliverable и QA.

## Yandex-only boundary

Работа выполняется только для экосистемы Яндекса: Яндекс Wordstat и обычная выдача Яндекса в пределах метода MK01. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в base scope не входят. Authority: `../YANDEX_ONLY_SCOPE.md`.

## Что продаётся

Клиент покупает самостоятельный результат: очищенное и сгруппированное семантическое ядро под реальный бизнес и спрос Яндекса.

`PRODUCT_SCOPE.md` и `CLIENT_INPUT_CONTRACT.md` заморожены.

## Зафиксированные границы

- base MK01 — существующий публичный сайт;
- первоначально один основной регион;
- Webmaster / Metrika / Direct не обязательны;
- Step5A competitor expansion исключён из base MK01 и относится к MK03/будущему add-on;
- ordinary Yandex Search — только точечные проверки материальных спорных границ;
- финал MK01 = semantic core + clustering, без page ownership / architecture / developer TZ;
- greenfield/no-site режим не заявляется как уже валидированный;
- Google research/tooling не входит.

## Автономный method set

| File | State |
|---|---|
| `PRODUCT_SCOPE.md` | **DONE** |
| `CLIENT_INPUT_CONTRACT.md` | **DONE** |
| `GENERAL_RULES.md` | **DONE** |
| `STEP_RULES_INDEX.md` | **DONE** |
| `steps/STEP_00_ORDER_SCOPE_FREEZE.md` | **DONE** |
| `steps/STEP_01_CURRENT_SITE_BUSINESS_MODEL.md` | **DONE** |
| `steps/STEP_02_WORDSTAT_ACQUISITION_PLAN.md` | **DONE** |
| `steps/STEP_03_WORDSTAT_ACQUISITION_PERSISTENCE.md` | **DONE** |
| `steps/STEP_04_FIRST_TRIAGE.md` | **DONE** |
| `steps/STEP_05_TARGETED_SECOND_ACQUISITION.md` | **DONE** |
| `steps/STEP_06_ROW_LEVEL_CLEANUP.md` | **DONE** |
| `steps/STEP_07_SEMANTIC_FREEZE_ROUTING.md` | **DONE** |
| `steps/STEP_08_TARGETED_YANDEX_SEARCH.md` | **DONE** |
| `steps/STEP_09_TASK_FIRST_CLUSTERING.md` | **DONE** |
| `steps/STEP_10_CLIENT_MATERIALIZATION_QA.md` | **DONE** |
| `ERRORS_AND_LESSONS.md` | **DONE — 30 inherited + 3 rehearsal failure classes** |
| `EXECUTION_ROADMAP.md` | **DONE** |
| `DELIVERABLE_SPEC.md` | **DONE / seven-sheet physical layout validated** |
| `QA_AND_RELEASE.md` | **DONE** |
| `KWORK_CARD.md` | PENDING PHASE 8 ECONOMICS + PACKAGING |
| `PORTFOLIO_ASSET_SPEC.md` | PENDING PACKAGING |
| `tests/OKNO_MSK/*` | **PHASE 5 PASS / REMOTE READBACK COMPLETE** |

## Source KW-001 extraction boundary

```text
Step0 scope freeze
Step1 existing-site/business discovery
Step2 seed/acquisition plan
Step3 Yandex Wordstat acquisition
Step4 first triage
Step5 targeted second acquisition only when justified
Step5A excluded from base MK01
Step6/6A excluded
Step7 row-level cleanup
Step8 semantic freeze/routing
Step9 targeted ordinary Yandex Search narrow controls
Step10 task/intent clustering
Step19 recipient materialization controls relevant to MK01
Step20 final semantic/workbook/recipient QA relevant to MK01
```

Steps11–18 are not silently inherited.

## Productization roadmap

```text
PHASE 0  PRODUCT PROMISE FREEZE                 = PASS
PHASE 1  MARKET REALITY BASELINE               = PASS / REFRESH BEFORE CARD
PHASE 2  CLIENT INPUT CONTRACT                 = PASS
PHASE 3  KW-001 METHOD/FAILURE EXTRACTION      = PASS
PHASE 4  AUTONOMOUS MK01 ROADMAP               = PASS
PHASE 5  OKNO_MSK MK01-ONLY REHEARSAL          = PASS
PHASE 6  MK01 CLIENT DELIVERABLE / PACKAGING   = NEXT
PHASE 7  QA                                    = PENDING
PHASE 8  PRICE/LIMITS/ECONOMICS FREEZE         = PENDING
PHASE 9  KWORK CARD                            = PENDING
PHASE 10 PORTFOLIO ILLUSTRATION                = PENDING
PHASE 11 OWNER PUBLICATION                     = PENDING OWNER ACTION
PHASE 12 PUBLISHED VERSION FREEZE/READBACK      = PENDING
```

## Current next action

```text
PHASE 6 — PACKAGE THE VALIDATED SEVEN-SHEET CLIENT DELIVERABLE
→ KEEP THE 2840-ROW PRE-STEP5A AUTHORITY AND 2185/187/468 PARTITION FROZEN
→ PREPARE CLIENT-HANDOFF WORDING/PRODUCT PACKAGING WITHOUT ADDING DOWNSTREAM SCOPE
→ USE REHEARSAL_METRICS.md AS INPUT TO PHASE 8; DO NOT INVENT PRICE/LIMITS
```
