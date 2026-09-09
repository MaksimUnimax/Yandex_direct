# MK01 — PHASE 8 PRICE / LIMITS / ECONOMICS

Status: **PASS / COMMERCIAL PACKAGE V1 DEFINED**

Date: 2026-09-09

This phase converts the validated OKNO_MSK workload measurements into a sellable initial package. The pilot counts are evidence for workload, not automatic package limits.

## 1. Measured pilot workload

Authority: `tests/OKNO_MSK/REHEARSAL_METRICS.md`.

```text
public site discovery = 64 URLs
Wordstat requests = 22
Wordstat observations = 2965
unique governed phrases = 2840
working core = 2185
review / uncertain = 187
excluded = 468
ordinary Yandex Search requests = 75
Search TOP-10 rows = 750
active clustering review = 2332 rows
cluster correction impact = 927 rows
client result = 7-sheet XLSX
```

The principal analytical bottlenecks were row-level semantic review and task-first clustering, not provider API cost.

## 2. Fresh market baseline

Market checked on 2026-09-09.

### Kwork

Source:
`https://kwork.ru/land/semanticheskoe-yadro-s-wordstat`

Current examples visible on the landing page include:

- Wordstat collection + clustering from 2,000 ₽;
- up to 500 grouped phrases from 3,000 ₽;
- SEO semantic core for Yandex from 5,000 ₽;
- `Сбор и кластеризация семантического ядра с нуля + структура` from **8,000 ₽**, displayed as **800 ₽ per 100 keywords**;
- competitor-semantic product from 8,000 ₽.

The 8,000 ₽ item is the closest useful Kwork unit-price benchmark, but it is not treated as method identity with MK01.

### FL.ru

Source:
`https://www.fl.ru/projects/5499768/gruppirovka-i-chistka-semantiki-dlya-seo-na-2000-zaprosov.html`

Project dated 2026-04-12: **15,000 ₽** for cleaning/grouping roughly **2,000 queries**, explicitly requiring manual work and real Yandex + Google result analysis. It starts from an existing core and includes Google, so it is not a direct functional duplicate of Yandex-only MK01, but it is a useful labor-price signal.

### Kwork seller commission

Source:
`https://blog.kwork.ru/updates/obnovlenie-uslovij-dlya-polucheniya-lgotnoj-komissii`

From 2025-09-01 the published seller commission tiers are:

```text
turnover with a client up to 50,000 ₽ -> 20%
50,000–500,000 ₽ -> 12%
above 500,000 ₽ -> 7.5%
```

For a new-client 12,000 ₽ order, internal expected net at 20% commission is **9,600 ₽**. Commission is an internal economics consideration and is not shown as a client surcharge.

## 3. Commercial base package V1

Working marketplace title remains:

**«Семантическое ядро для сайта: сбор, чистка и кластеризация»**

Base package:

```text
PRICE = 12,000 ₽
DELIVERY TARGET = 5 calendar days
SITE = 1 existing public website
PRIMARY REGION = 1
AGREED BUSINESS DIRECTIONS = up to 10
GOVERNED UNIQUE PHRASES = up to 1,500
TARGETED ORDINARY YANDEX SEARCH CHECKS = up to 40, only when methodically justified
CLIENT RESULT = validated seven-sheet XLSX + short handoff summary
GOOGLE = excluded
COMPETITOR STEP5A = excluded
PAGE OWNERSHIP / ARCHITECTURE / TZ / AI = excluded
```

The phrase limit means the number of unique phrase rows entering full governed semantic cleanup/routing, not raw Wordstat occurrence rows and not only the final accepted core.

## 4. Why 12,000 ₽ / 1,500 phrases

12,000 / 1,500 = **800 ₽ per 100 governed phrases**.

That matches the current visible 8,000 ₽ / 800 ₽ per 100-key Kwork benchmark without undercutting a deeper process merely because provider requests are cheap.

The base package is intentionally smaller than the 2,840-row OKNO_MSK pilot. Scaling that pilot mechanically into a base package would make the entry product unnecessarily large and would expose the main manual bottlenecks before the seller has reviews for this new product line.

The package also includes work not represented by a flat-parser export: scope freeze, current-site interpretation, preserved Wordstat evidence, explicit uncertainty, conditional exact-query Yandex Search, task-first grouping, exclusions ledger and recipient QA.

## 5. Initial add-ons

### A. Additional governed phrase block

```text
+500 unique governed phrases
PRICE = +4,000 ₽
DELIVERY = +2 calendar days
```

This preserves the same 800 ₽ / 100 phrase unit rate.

Normal self-service expansion ceiling for this initial package:

```text
up to 3,000 governed unique phrases
```

Above 3,000 phrases: custom quote after scope review rather than unlimited automatic add-ons.

### B. Additional targeted Yandex Search block

```text
+10 exact-query Search checks
PRICE = +1,500 ₽
DELIVERY = +1 calendar day
```

This add-on is used only when more evidence-resolvable ambiguities genuinely exist. It is not bulk rank tracking. If extra Search is not purchased, unresolved rows beyond the included capacity remain honestly visible on `На проверку`; they are not fabricated as resolved.

## 6. Commercial volume gate

The commercial phrase cap may never cause silent evidence loss.

Canonical sequence:

```text
ACQUIRE AUTHORIZED WORDSTAT EVIDENCE
→ PERSIST ALL USEFUL RETURNED OCCURRENCES
→ NORMALIZE / EXACT-DEDUPE
→ MEASURE UNIQUE CANDIDATE UNIVERSE
→ COMPARE TO PURCHASED GOVERNED-PHRASE CAPACITY
```

If candidate universe <= purchased capacity:

```text
continue full row-level cleanup
```

If candidate universe > purchased capacity:

```text
DO NOT silently delete overflow
DO NOT keep only highest-frequency rows
DO NOT start full deep review of overflow for free
```

Allowed outcomes:

1. client purchases one or more +500 phrase blocks; or
2. a documented scope revision narrows included business directions before full row-level review.

All acquired provider evidence remains durably preserved. Scope revision changes the governed review set, not history.

## 7. Search-cap gate

Included Search capacity is **up to 40 exact checks when justified**.

If fewer than 40 are needed, unused capacity is not converted into fake work or another deliverable.

If more than 40 material Search-resolvable ambiguities exist:

- additional +10 Search blocks may be added; or
- remaining cases stay explicit `На проверку` / deferred under the method.

Search count is driven by unresolved evidence questions, not by a promise to spend all included calls.

## 8. What is deliberately NOT sold yet

Not offered as an MK01 V1 add-on until separately validated:

- second geographic region;
- greenfield/no-site mode;
- competitor semantic expansion (belongs to MK03);
- page mapping / site architecture / cannibalization;
- developer/content TZ;
- Alice / Yandex Neuro / AI analysis;
- Google research;
- rush delivery.

## 9. Economics notes

At a new-client Kwork commission of 20%:

```text
12,000 ₽ base -> 9,600 ₽ net before taxes/other business costs
+4,000 ₽ phrase block -> 3,200 ₽ incremental net
+1,500 ₽ Search block -> 1,200 ₽ incremental net
```

Provider execution cost observed in OKNO_MSK was negligible relative to analytical review. Therefore price is based on governed analytical workload and client-ready QA, not API cost.

## 10. Phase 8 acceptance

```text
REAL MARKET BASELINE REFRESHED = PASS
PILOT WORKLOAD USED = PASS
BASE PRICE SET = 12,000 ₽
BASE PHRASE CAPACITY = 1,500 governed unique phrases
BASE SEARCH CAPACITY = up to 40 justified exact checks
SITE / REGION = 1 / 1
BUSINESS DIRECTIONS = up to 10
DELIVERY TARGET = 5 calendar days
+500 PHRASES = +4,000 ₽ / +2 days
+10 SEARCH = +1,500 ₽ / +1 day
SILENT COMMERCIAL TRUNCATION = FORBIDDEN
YANDEX-ONLY = PRESERVED
NEXT = PHASE 9 KWORK CARD
```