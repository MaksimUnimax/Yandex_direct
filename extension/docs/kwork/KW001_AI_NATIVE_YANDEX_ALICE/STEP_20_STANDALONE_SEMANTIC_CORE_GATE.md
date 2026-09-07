# KW-001 — STEP 20 STANDALONE SEMANTIC CORE ACCEPTANCE GATE

Updated: 2026-09-07
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**
Scope: **separate client XLSX semantic-core deliverable**

## 1. Recipient and physical result

Recipient: SEO, semantic or implementation specialist.

Physical result: a standalone XLSX semantic core. It is a separate deliverable, not Report №02 and not a promise that the recipient will reconstruct a workbook from repository tables.

Purpose: filtering, sorting, cluster review, phrase→page work, unresolved-case review, prioritization and implementation use.

## 2. Required authority and views

The workbook must be generated reproducibly from the current accepted phrase, structural-unit, demand/provenance and page/action authorities. A historical materialization may supply provenance only; it cannot override a later final authority.

Unless the sold contract defines an equally usable equivalent, the workbook exposes:

1. all preserved phrases;
2. the active core;
3. a cluster summary;
4. a page summary including governed no-page groups;
5. unresolved/Search-required work;
6. a dictionary explaining fields, metrics, decisions and technical traceability.

All phrase states must reconcile. Active, assigned, unresolved, excluded, deferred, URL and governed no-URL totals must be mechanically derived from current authority. Phrase keys and stable IDs must remain unique where their contract requires uniqueness.

## 3. Frequency semantics

Every displayed demand value must state the actual report/method, region, device filter, operator mode, snapshot and aggregation rule. A value collected without operators must not be called exact frequency or a traffic forecast.

Official Russian client terminology takes precedence in the display layer: «Вордстат», «Топы запросов», «популярные запросы», «похожие запросы», «число запросов», «регион», «тип устройства», «все устройства», «без операторов».

Technical acquisition identifiers such as `GetTop`, `DEVICE_ALL`, `results[]`, `associations[]`, `phrase` and `count` may remain in a clearly technical note, code column or provenance row. They must not replace the Russian client explanation.

## 4. Client display language and traceability

For a Russian client artifact:

```text
CLIENT_DISPLAY_LANGUAGE = RUSSIAN
CANONICAL MACHINE VALUE != CLIENT DISPLAY VALUE
TECHNICAL API TERM != CLIENT TERM
PROJECT ENUM != CLIENT EXPLANATION
```

Primary headers, statuses, intent, business boundaries, page roles, recommendations, readiness, uncertainty, priorities, metric descriptions and explanatory notes must use clear Russian professional language.

A visible worksheet title is part of client presentation language:

```text
WORKSHEET TITLE IS PART OF CLIENT PRESENTATION LANGUAGE
CELL LANGUAGE QA != WHOLE-WORKBOOK LANGUAGE QA
```

Visible sheet names must use the recipient language and must not expose an internal project/API enum as their primary meaning.

Stable phrase/unit/source IDs, URLs, filenames, product names and explicit technical-code fields may retain Latin characters or machine codes. They are secondary traceability. The recipient must not need them to understand the decision.

Every client-visible categorical value must use a deterministic display map. An unknown enum without a Russian display label is a build failure.

## 5. Workbook usability

PASS requires:

- required sheets in the declared order;
- usable filters/tables and frozen headers;
- readable widths, wrapped long text and visible URLs;
- no hidden critical meaning;
- numeric demand cells and no broken formulas;
- correct Cyrillic rendering and no workbook repair warning;
- representative visual inspection of every required sheet;
- a recipient can understand phrase, cluster, intent, page/no-page reason and recommendation without repository knowledge.

## 6. Known failure — internal technical schema leaked into client-facing semantic core

### What failed

A workbook passed phrase reconciliation, final-authority equivalence, demand equivalence, stale-materialization protection, sheet/filter/freeze checks and visual rendering, but still exposed internal English API/project codes as normal recipient terminology.

### Root cause

```text
INTERNAL REPRESENTATION WAS TREATED AS CLIENT PRESENTATION
TECHNICAL TRACEABILITY WAS CONFUSED WITH CLIENT READABILITY
SPECIALIST RECIPIENT WAS TREATED AS PERMISSION TO DUMP INTERNAL SCHEMA
```

The earlier QA checked structure and data correctness but had no semantic-core recipient-language scan.

### Corrected control

```text
CLIENT DISPLAY VALUE = CLEAR RECIPIENT-LANGUAGE MEANING
TECHNICAL CODE = OPTIONAL SECONDARY TRACEABILITY

CORRECT DATA != CLIENT-USABLE SEMANTIC CORE
WORKBOOK STRUCTURE QA != RECIPIENT LANGUAGE QA
SPECIALIST RECIPIENT != PERMISSION TO DUMP INTERNAL SCHEMA
```

Permanent PASS requires:

```text
DATA QA = PASS
WORKBOOK QA = PASS
RUSSIAN CLIENT-LANGUAGE QA = PASS
TECHNICAL TRACEABILITY = PRESERVED
UNEXPLAINED INTERNAL ENGLISH = 0
UNKNOWN UNMAPPED CLIENT ENUMS = 0
CLIENT-FACING WORKSHEET TITLES = RECIPIENT LANGUAGE
UNEXPLAINED INTERNAL ENGLISH IN WORKSHEET TITLES = 0
```

## 7. Acquisition-to-deliverable continuity

Late materialization must not discover that fields already returned by the provider were discarded. The governing principle is:

```text
COLLECT ONCE
PRESERVE COMPLETELY
DERIVE MANY VIEWS LATER
```

Step 20 does not normalize provider recollection caused by earlier persistence loss. New acquisition is justified only by a genuinely new information requirement.

## 8. External source boundary

- Yandex Wordstat interface: https://yandex.ru/support2/wordstat/ru/interface/new
- Yandex Wordstat operators: https://yandex.ru/support2/wordstat/ru/content/operators
- Yandex AI Studio Wordstat GetTop API: https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop
- Yandex Webmaster query/site fit: https://yandex.ru/support/webmaster/ru/recommendations/targeting
- Semrush keyword clustering: https://www.semrush.com/blog/keyword-clustering/
- Semrush keyword mapping: https://www.semrush.com/blog/keyword-mapping/
- Ahrefs keyword intent: https://ahrefs.com/blog/keyword-intent/
- Ahrefs keyword cannibalization: https://ahrefs.com/blog/keyword-cannibalization/

Official sources govern Yandex terminology and product semantics. Professional SEO sources support clustering, intent and mapping practice. Neither may override accepted project authority.

## 9. Final gate

```text
CANONICAL AUTHORITY RECONCILIATION = PASS
FULL PHRASE ACCOUNTING = PASS
DEMAND / PROVENANCE EQUIVALENCE = PASS
STALE AUTHORITY LEAKAGE = 0
REQUIRED VIEWS = PASS
WORKBOOK USABILITY = PASS
VISUAL QA OF EVERY SHEET = PASS
RUSSIAN CLIENT-LANGUAGE QA = PASS
CLIENT-FACING WORKSHEET TITLES = RECIPIENT LANGUAGE
UNEXPLAINED INTERNAL ENGLISH IN WORKSHEET TITLES = 0
UNEXPLAINED INTERNAL ENGLISH = 0
TECHNICAL TRACEABILITY = PRESERVED
PERSISTED REMOTE READBACK = PASS
```
