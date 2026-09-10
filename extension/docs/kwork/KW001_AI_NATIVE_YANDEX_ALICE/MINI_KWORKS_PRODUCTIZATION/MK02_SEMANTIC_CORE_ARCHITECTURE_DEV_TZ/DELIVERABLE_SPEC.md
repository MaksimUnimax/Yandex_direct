# MK02 — DELIVERABLE SPEC

Status: **LOGICAL CLIENT-RESULT CONTRACT + PHASE-6 PHYSICAL PACKAGE FROZEN / PHASE 7 QA NEXT**

## 1. Sold result

The client must receive a standalone result that connects Yandex demand to current pages, target Search architecture and evidence-supported implementation work without requiring repository knowledge or manual joins of internal files.

The result must answer:

1. what site/region/business scope was researched;
2. what semantic core and user-task groups were accepted;
3. which current page is the primary owner for each applicable task/phrase;
4. where exact phrase owner, family owner and supporting page differ;
5. which tasks have no suitable current owner or remain unresolved;
6. what current site architecture/topology exists;
7. what target Search architecture is recommended;
8. what differs between current and target state;
9. which findings require an actual site change and which are semantic mapping/no-change only;
10. which changes are ready to implement now;
11. which changes require one concrete clarification/check first;
12. how to verify each implemented change;
13. what evidence/limitations bound the conclusions;
14. what is explicitly outside MK02.

## 2. Logical client views — mandatory

The Phase-6 physical file split is frozen, but these logical views remain authoritative and may not disappear during materialization.

### A. Scope / how to use

Plain-language explanation of site, region, Yandex-only boundary, what was researched, what files/views exist and how to navigate the result.

### B. Semantic core

Client-usable phrase-level view preserving at least:

- phrase;
- useful Yandex demand indicator with correct metric meaning;
- semantic state;
- user-task cluster;
- task/intent meaning;
- uncertainty/review status;
- exclusion reason where applicable.

Full row accounting must reconcile to current authority.

### C. Task / cluster map

For every material working task/group:

- human-readable group name;
- user task / intent;
- member count;
- real representative phrases;
- important boundary notes;
- current ownership state.

### D. Phrase/task → page ownership map

For every applicable active phrase/task:

- current primary owner page or explicit no-page/unresolved state;
- family/structural-unit owner when materially different;
- supporting page(s) when material;
- observed Search-relevant URL only when directly evidenced and clearly separated from intended owner;
- human-readable reason/evidence meaning.

Critical display rule:

```text
EXACT QUERY OWNER
!= FAMILY OWNER
!= SUPPORTING PAGE
!= OBSERVED SEARCH URL
```

The client must not see these compressed into one ambiguous “Основной URL” when they differ.

### E. Current architecture / topology

Show the material current public site state relevant to the project:

- current pages/roles;
- current hierarchy/relationship where material;
- literal current internal-link state where the recommendation depends on it;
- newly discovered material pages reconciled during architecture freeze.

### F. Target Search architecture

Show intended Search responsibility separately from current topology:

- target primary page for each task/unit;
- supporting pages/relationships;
- new/split/merge/route recommendations only where supported;
- unresolved boundaries;
- recommended page relations/internal links where supported.

### G. Current → target delta / action map

Every material architecture finding must resolve to an explicit implementation effect:

```text
REAL SITE CHANGE = YES
REAL SITE CHANGE = NO
REAL SITE CHANGE = UNRESOLVED
```

The client must be able to distinguish:

- semantic mapping only;
- structural keep/no-change;
- content/section change;
- navigation/link change;
- create/split/merge candidate;
- recheck/clarification/HOLD.

### H. READY implementation specifications

Every item shown as ready must be self-contained enough to execute.

Client-visible fields when applicable:

```text
Страница / объект
Зачем менять
Что сделать
Где
Порядок работы
Пример / содержание изменения where useful
Что должно остаться / сохраниться where material
Как проверить результат
```

Internal field names/IDs may differ, but recipient meaning must be equivalent.

### I. Clarifications / checks before implementation

For every useful but not-ready recommendation:

```text
Страница / объект
Что хотим изменить
Что конкретно нужно уточнить / проверить
Зачем это нужно
Как получить ответ / как проверить
Какое решение станет возможным после ответа
```

No vague “нужно дополнительное исследование” without the decision purpose.

### J. Topic-to-page guidance

Where a supporting mapping table is useful, explain before the table:

```text
WHAT IT SHOWS
WHY IT EXISTS
HOW TO USE IT
```

Preferred ordinary-Russian meaning: topic/user question → primary page → related/supporting page where applicable.

### K. Page-to-page connections

Where internal relationships are recommended, explain what the source and target pages mean, why the transition helps the visitor and how the direction should be implemented.

Current literal link state and recommended link state remain separate.

Duplicate visible source→target pairs are consolidated unless genuinely different contexts are explicitly explained.

### L. Analytical explanation

A client/owner should understand what the research found, not only receive action tables.

Required finding classes when supported:

- material demand/task structure;
- important current ownership/coverage patterns;
- material current-vs-target architecture differences;
- supported KEEP/no-change findings;
- unresolved/blocked architecture boundaries;
- why major actions exist.

Canonical rule:

```text
CLIENT ANALYTICAL REPORT != EXECUTION PROTOCOL
```

### M. Implementation acceptance / measurement interface

At minimum each READY change has an observable implementation acceptance check.

Performance baselines/metrics/windows appear only when real source/data exist and are in scope. Do not invent uplift or a measurement schedule.

## 3. Client-language contract

For a Russian client:

- normal headings/statuses/reasons/instructions are in Russian;
- action IDs, Stage/Step labels, repository filenames, QA IDs and internal enums do not appear as ordinary client vocabulary;
- technical identifiers may remain only in clearly secondary audit fields when useful;
- document identity is based on purpose/result, not recipient profession.

Forbidden as primary document identity:

```text
«Руководство SEO-специалиста»
«Гайд для разработчика»
«Документ для редактора»
```

The implementation document is named by the result/purpose: **«ТЗ на доработку сайта»** or an equivalent result-based title.

## 4. Data-truth contract

All client views derive from one current accepted authority chain.

Before generation freeze a materialization manifest containing equivalent:

```text
CURRENT FINAL SEMANTIC AUTHORITY
CURRENT CLUSTER AUTHORITY
CURRENT OWNERSHIP AUTHORITY
CURRENT STRUCTURAL ACTION AUTHORITY
CURRENT COMPETING-PAGE CORRECTIONS / LIMITATIONS
CURRENT SEARCH-ONLY ARCHITECTURE AUTHORITY
CURRENT IMPLEMENTATION WORK-PACKAGE AUTHORITY
STABLE JOIN KEYS
SOURCE REVISION IDENTITIES
OVERLAY PRECEDENCE
GENERATION VERSION
CLIENT CONSUMER VIEWS
```

No polished workbook/report can override stale/wrong canonical data.

## 5. Physical package boundary — frozen in Phase 6

After the OKNO_MSK MK02-only rehearsal and owner review, base MK02 V1 uses this physical client package:

```text
1. XLSX — WORKING SEMANTIC / OWNERSHIP / ARCHITECTURE / IMPLEMENTATION WORKBOOK
2. PDF — ANALYTICAL RESEARCH-AND-ARCHITECTURE REPORT
3. PDF — ACTION-FIRST SITE-IMPROVEMENT TZ
4. SHORT KWORK/CHAT HANDOFF MESSAGE — NOT A SEPARATE FILE
```

Detailed authority: `PRODUCT_PACKAGING.md`.

Carrier-role mapping:

| Logical need | Primary carrier |
|---|---|
| Scope / how to use | analytical PDF + XLSX start view + handoff message |
| Semantic core / clusters | XLSX |
| Phrase/task ownership | XLSX |
| Current / target architecture detail | XLSX |
| Material architecture conclusions | analytical PDF |
| Current→target delta | XLSX + analytical PDF summary |
| READY implementation specifications | implementation-TZ PDF + XLSX detail |
| Clarifications / recheck / HOLD | implementation-TZ PDF + XLSX detail |
| Page relationships | XLSX; implementation PDF when action-relevant |
| Analytical explanation | analytical PDF |
| Acceptance / verification | implementation-TZ PDF + XLSX detail |

The analytical PDF and implementation-TZ PDF remain separate because they answer different recipient tasks:

```text
ANALYTICAL PDF = WHAT THE RESEARCH SHOWED
IMPLEMENTATION-TZ PDF = WHAT TO DO / WHY / WHERE / HOW TO CHECK
```

A mandatory duplicate DOCX is **not** part of base MK02 V1. If DOCX is used internally during materialization, it is an intermediate/source artifact. An editable text copy may be produced only as a separately requested variant from the same accepted source, not as an independently diverging authority.

Permanent boundaries:

```text
LOGICAL DELIVERABLE REQUIREMENTS = FROZEN
PHYSICAL SPLIT = XLSX + TWO PDF
PAGE COUNT != QUALITY GATE
WORKBOOK SHEET COUNT != PRODUCT VALUE PROXY
```

Do not repeat the earlier MK01 mistake of using an invented page-count range as a quality gate.

## 6. Explicit product exclusions in client output

No client artifact may imply completion of:

- Google research/SEO;
- competitor-derived semantic gap research;
- Alice/Yandex Neuro/GenSearch/AEO analysis;
- website coding/implementation;
- full technical SEO audit;
- guaranteed rankings/traffic/leads/revenue;
- standalone historical harmful-cannibalization audit beyond MK02's architecture-safety scope;
- production implementation schedule when owner/effort/capacity/timing were not calibrated.

## 7. Release boundary

The client package cannot pass until:

```text
SEMANTIC ROW ACCOUNTING PASS
+ OWNERSHIP ROW ACCOUNTING PASS
+ CURRENT/TARGET ARCHITECTURE RECONCILIATION PASS
+ ACTION READINESS STATES PASS
+ READY IMPLEMENTATION COMPLETENESS PASS
+ ANALYTICAL EXPLANATION PASS
+ CLIENT LANGUAGE PASS
+ XLSX USABILITY / PHYSICAL QA PASS
+ ANALYTICAL PDF PHYSICAL/RENDER QA PASS
+ IMPLEMENTATION-TZ PDF PHYSICAL/RENDER QA PASS
+ RECIPIENT TASK REVIEW OF EACH DOCUMENT PASS
+ YANDEX-ONLY BOUNDARY IN EACH CLIENT FILE PASS
+ PERSISTENCE/READBACK PASS
```

These are Phase-7 release tests for the Phase-6 package design. Phase-6 packaging PASS does not predeclare Phase-7 physical QA PASS.
