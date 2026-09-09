# MK01 — Семантическое ядро для сайта: сбор, чистка и кластеризация

Status: **PHASE 7 PRODUCT/PACKAGING QA PASS / PHASE 8 NEXT**

## Рабочее название карточки

**Семантическое ядро для сайта: сбор, чистка и кластеризация**

Яндекс не выносится в заголовок искусственной конструкцией «для Яндекса», но Yandex-only scope обязан быть явно указан в описании, составе работ, входных данных, FAQ, deliverable и QA.

## Yandex-only boundary

Работа выполняется только для экосистемы Яндекса: Яндекс Wordstat и обычная выдача Яндекса в пределах метода MK01. Google Ads / Google Keyword Planner, Google Search, Google Search Console и другие Google-инструменты в base scope не входят. Authority: `../YANDEX_ONLY_SCOPE.md`.

## Что продаётся

Клиент покупает самостоятельный результат: очищенное и сгруппированное семантическое ядро под реальный бизнес и спрос Яндекса.

## Зафиксированные границы метода

- base MK01 — существующий публичный сайт;
- первоначально один основной регион;
- Webmaster / Metrika / Direct не обязательны;
- Step5A competitor expansion исключён из base MK01 и относится к MK03/будущему add-on;
- ordinary Yandex Search — только точечные проверки материальных спорных границ;
- финал MK01 = semantic core + clustering, без page ownership / architecture / developer TZ;
- greenfield/no-site режим не заявляется как уже валидированный;
- Google research/tooling не входит.

## Автономный method/product set

| File | State |
|---|---|
| `PRODUCT_SCOPE.md` | **DONE / post-rehearsal synchronized** |
| `CLIENT_INPUT_CONTRACT.md` | **DONE / post-rehearsal synchronized** |
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
| `ERRORS_AND_LESSONS.md` | **DONE — E01–E35** |
| `EXECUTION_ROADMAP.md` | **DONE / validated on OKNO_MSK** |
| `DELIVERABLE_SPEC.md` | **DONE / seven-sheet physical layout validated** |
| `QA_AND_RELEASE.md` | **DONE** |
| `PRODUCT_PACKAGING.md` | **DONE** |
| `CLIENT_HANDOFF_TEMPLATE.md` | **DONE / conditional Search wording corrected** |
| `PHASE_7_PRODUCT_PACKAGING_QA.md` | **PASS — 18/18** |
| `tests/OKNO_MSK/CLIENT_HANDOFF_PACKAGE.md` | **DONE** |
| `KWORK_CARD.md` | PENDING PHASE 8 ECONOMICS + PHASE 9 |
| `PORTFOLIO_ASSET_SPEC.md` | PENDING PHASE 10 |
| `tests/OKNO_MSK/*` | **PHASE 5 PASS / REMOTE READBACK COMPLETE** |

## Productization roadmap

```text
PHASE 0  PRODUCT PROMISE FREEZE                 = PASS
PHASE 1  MARKET REALITY BASELINE               = PASS / REFRESH BEFORE CARD
PHASE 2  CLIENT INPUT CONTRACT                 = PASS
PHASE 3  KW-001 METHOD/FAILURE EXTRACTION      = PASS
PHASE 4  AUTONOMOUS MK01 ROADMAP               = PASS
PHASE 5  OKNO_MSK MK01-ONLY REHEARSAL          = PASS
PHASE 6  MK01 CLIENT DELIVERABLE / PACKAGING   = PASS
PHASE 7  PRODUCT/PACKAGING QA                  = PASS
PHASE 8  PRICE/LIMITS/ECONOMICS                = NEXT
PHASE 9  KWORK CARD                            = PENDING
PHASE 10 PORTFOLIO ILLUSTRATION                = PENDING
PHASE 11 OWNER PUBLICATION                     = PENDING OWNER ACTION
PHASE 12 PUBLISHED VERSION FREEZE/READBACK      = PENDING
```

## Current next action

```text
PHASE 8 — PRICE / LIMITS / ECONOMICS
→ USE tests/OKNO_MSK/REHEARSAL_METRICS.md AS MEASURED WORKLOAD INPUT
→ REFRESH REAL KWORK / FL.RU MARKET ANALOGUES BEFORE SETTING PRICE
→ DEFINE BASE PACKAGE BOUNDARIES WITHOUT COPYING 2840 AS A UNIVERSAL LIMIT
→ DEFINE WHAT DRIVES SURCHARGES / ADD-ONS
→ DEFINE DELIVERY-TIME BASIS
→ KEEP YANDEX-ONLY AND MK01 SCOPE BOUNDARIES
→ COMMIT + REMOTE READBACK
→ THEN PHASE 9 KWORK CARD
```
