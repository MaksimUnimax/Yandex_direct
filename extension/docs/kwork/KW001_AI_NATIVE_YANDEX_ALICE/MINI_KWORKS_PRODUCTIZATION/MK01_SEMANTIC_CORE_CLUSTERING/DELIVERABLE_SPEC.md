# MK01 — DELIVERABLE SPEC

Status: **METHOD CONTRACT + XLSX + ANALYTICAL CLIENT PDF VALIDATED ON OKNO_MSK**

## 1. Sold result

The client receives a standalone, recipient-readable semantic core for the frozen existing-site scope based on Yandex demand evidence, conservative cleanup and task-first clustering.

The complete delivery must let the client understand without repository knowledge:

1. what scope/region was researched;
2. what phrases were preserved;
3. which phrases form the active core;
4. how active phrases are grouped and what each group means;
5. what the research showed about the structure of the working corpus;
6. which phrases remain uncertain/deferred and why;
7. what was excluded and why;
8. what the displayed Wordstat metrics mean;
9. how to use the working XLSX;
10. what can reasonably be done next;
11. that Google/page architecture/AI are outside MK01.

## 2. Canonical recipient workbook views

The seven-sheet physical layout has been validated on the OKNO_MSK standalone rehearsal. Changing sheet names/order or removing a view requires an explicit product-method revision and QA.

### A. «Как пользоваться»
Site, region, directions, Yandex-only boundary, short workflow and limitations.

### B. «Все запросы»
Full preserved client-visible governed semantic universe.

### C. «Рабочее ядро»
Final active/accepted phrases with demand metric, cluster, task/intent meaning and useful sorting/filter fields.

### D. «Группы запросов»
Human-readable group summary: name, task/meaning, member count, representative accepted phrases, material boundary notes.

### E. «На проверку»
Unresolved/Search-required/deferred/HOLD rows with reason and current state.

### F. «Исключено»
Excluded demand/reasons sufficient to prove deliberate cleaning.

### G. «Методика»
Russian explanation of Wordstat metric semantics, region/device/operator/snapshot where applicable, state/group meaning and limitations.

## 3. Mandatory analytical client PDF

Every completed MK01 order also includes a client PDF governed by `CLIENT_REPORT_SPEC.md`.

Canonical rule:

```text
CLIENT REPORT != EXECUTION PROTOCOL
CORRECT COUNTS + CLEAN LAYOUT != ANALYTICAL REPORT PASS
```

The PDF must explain in ordinary Russian:

- evidence-backed executive findings — **what the research showed**, not just what was done;
- site, region and data/snapshot scope;
- headline counts from current authority;
- working-core structure by current evidence-backed task/intent taxonomy where available;
- major/material semantic groups chosen by an explicit rule rather than arbitrary examples;
- what remains uncertain/reviewed and why;
- what was excluded and why;
- how to use the XLSX;
- Wordstat metric limitations;
- Yandex-only boundary;
- what is outside MK01;
- reasonable next-step options without claiming those later products were already completed.

The PDF must not invent examples, counts, shares, frequency values, traffic/ranking forecasts, commercial priorities or downstream conclusions.

There is **no fixed page-count PASS target**. Page count is descriptive only; information value and recipient usefulness are the acceptance criteria.

## 4. Handoff message

The marketplace/chat handoff message is short and attaches both client files. It is not a separate TXT deliverable and is not a substitute for the PDF report.

## 5. Display-language contract

For a Russian client:

- visible sheet names, headers, statuses, report headings and explanations are Russian;
- internal API/stage/status codes do not become the main display vocabulary;
- technical IDs remain only where useful for traceability;
- internal words such as Stage, Step, authority, provenance, route state, failure class, exact-universe join, phrase key and request IDs must not appear unexplained in the client PDF;
- internal pilot history is excluded unless needed to understand the purchased result;
- «частотность» wording must correspond to the actual Wordstat metric.

## 6. Data-truth contract

XLSX and PDF are generated views of the current accepted semantic/demand/cluster authorities. Neither becomes a competing analytical source of truth.

Before generation:

```text
SOURCE IDENTITIES
+ SOURCE COUNTS
+ CURRENT VERSION/TIMESTAMP
+ EXPECTED JOIN COUNTS
+ DISPLAY MAPPING VERSION
+ PURCHASED GOVERNED-PHRASE / SEARCH CAPACITY
+ COMMERCIAL VOLUME-GATE RESULT
+ REPORT DERIVED-METRIC RECONCILIATION
```

Every report chart/share/top-group list must reconcile to current accepted authority.

## 7. Explicit exclusions

No final query→URL ownership, architecture, create/split/merge recommendations, cannibalization audit, developer TZ, competitor gap report, Alice/AEO result, Google data or ranking guarantee.

## 8. Physical client package

Mandatory client package:

```text
SEMANTIC_CORE_<CLIENT_OR_DOMAIN>_<YYYY-MM-DD>.xlsx
CLIENT_REPORT_<CLIENT_OR_DOMAIN>_<YYYY-MM-DD>.pdf
short marketplace/chat handoff message attaching both files
```

The workbook has exactly seven recipient sheets in this order: `Как пользоваться`; `Все запросы`; `Рабочее ядро`; `Группы запросов`; `На проверку`; `Исключено`; `Методика`.

Internal audit TSV/TSV.GZ, cluster TSV, manifest, machine-QA JSON, build receipts and source-authority audits are not automatically delivered to the client.

## 9. Commercial V1 capacity

Current base package authority is `PHASE_8_PRICE_LIMITS_ECONOMICS.md`:

```text
1 existing public website
1 primary region
up to 10 agreed business directions
up to 1,500 governed unique phrase rows
up to 40 justified exact-query Yandex Search checks
5 calendar days
12,000 ₽
```

The governed-phrase limit does not permit silent truncation of provider evidence.

## 10. Acceptance

Delivery is accepted only after data, semantic, workbook, analytical-report, language, visual and recipient-task QA from `QA_AND_RELEASE.md` all pass.

The OKNO_MSK current analytical report revision is dated **2026-09-10**. Its descriptive length is 8 pages, but that number is not a method requirement. Its acceptance is based on evidence-backed findings, reconciliation, readability and recipient usefulness.
