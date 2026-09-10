# MK02 — DELIVERABLE SPEC

Status: **TARGET-FIRST CLIENT-RESULT CONTRACT / PHASE 7 SECOND QUALITY CORRECTION REQUIRED**

Owner correction authorities:

- `PHASE_7_OWNER_PRODUCT_GAP_CORRECTION_2026-09-10.md`;
- `PHASE_7_OWNER_MARKET_GRADE_QUALITY_CORRECTION_2026-09-10.md`.

## 1. Sold result

The client must receive a standalone result that connects Yandex demand to a complete intended landing-page model, target Search architecture, reconciliation with the current site and evidence-supported implementation work.

The result must answer:

1. what site/region was researched;
2. what semantic core and user-task groups were accepted;
3. for every active phrase, which target landing page/task owns it or what explicit unresolved/no-standalone state applies;
4. for every material cluster/task, which intended landing page owns it;
5. what page type, purpose, parent/section and target route each intended landing page has;
6. what the complete target page registry/hierarchy is;
7. which target pages already match current pages, which need optimization, which are new candidates, which should not be standalone and which remain unresolved;
8. where exact phrase owner, family owner, supporting page and observed Search URL differ;
9. what differs between current and target state;
10. what full page-by-page target specification applies even where no physical change is required;
11. which findings require an actual site change;
12. which changes are ready, which require clarification/recheck and how to verify them;
13. what evidence/limitations bound the conclusions;
14. what is explicitly outside MK02.

## 2. Mandatory logical client views

### A. Scope / how to use
Plain-language explanation of site, region, Yandex-only boundary, file roles and navigation.

### B. Full semantic core
Phrase-level view preserving phrase, demand indicator, semantic state, cluster/task, intent, target landing-page key/route, uncertainty/review status and exclusion reason where applicable.

### C. Cluster / task map
For every material cluster/task: human-readable name, user task/intent, member count, representative phrases, boundary notes and target landing-page key.

### D. Phrase → target landing-page map
For every applicable active phrase:

```text
PHRASE
→ INDIVIDUAL WORDSTAT DEMAND INDICATOR
→ CLUSTER / TASK
→ INTENDED TARGET LANDING PAGE KEY
→ TARGET URL / ROUTE OR EXPLICIT UNRESOLVED / NO-STANDALONE STATE
```

The demand indicator must be present in this direct mapping view; the client must not need another sheet merely to sort phrases of one target page by demand.

Full row accounting must reconcile to current semantic authority.

### E. Cluster → target landing-page map
For every material cluster/task:

- intended primary landing page;
- page purpose;
- page type;
- one primary page job / intent;
- primary/representative query with its individual Wordstat indicator;
- top compatible secondary queries with individual Wordstat indicators where available;
- member phrase count;
- target URL/route;
- parent/section;
- supporting/child relationships when material;
- current-page match state kept separately.

### F. Current page / supporting-role evidence
Preserve separately:

```text
INTENDED TARGET LANDING
!= CURRENT PAGE MATCH / CURRENT OWNER
!= EXACT QUERY OWNER
!= FAMILY / STRUCTURAL-UNIT OWNER
!= SUPPORTING PAGE
!= OBSERVED SEARCH-RELEVANT URL
```

These roles must not be compressed into one ambiguous URL field.

### G. Target Search architecture / page registry
One row per material intended landing page with at least:

- page key;
- page purpose;
- page type;
- one primary task/intent;
- primary query + individual Wordstat indicator;
- secondary query set + individual Wordstat indicators where available;
- member phrase count;
- recommended H1;
- Title direction/draft for CREATE/OPTIMIZE where supported or explicit blocker;
- analytical SEO priority + basis;
- target URL/route;
- parent/section;
- child/supporting relationships where material;
- current URL match;
- current match state;
- action state;
- uncertainty/evidence boundary.

The target architecture must also be understandable as a hierarchy/tree or hierarchical table independent of the current site's navigation. The analytical PDF additionally requires a scannable visual/indented tree representation, not only a wide table.

### H. Current-site reconciliation
For every target page classify an equivalent current-match state such as:

```text
EXISTING_MATCH
EXISTING_NEEDS_OPTIMIZATION
EXISTING_RELATIONSHIP_CHANGE
NEW_PAGE_CANDIDATE
NO_STANDALONE_PAGE_ROUTE_TO_PARENT
UNRESOLVED
```

The current site is evidence and implementation context; it is not allowed to substitute for independent target design.

### I. Full page-by-page target specification
Every material target page receives a specification even when `REAL SITE CHANGE = NO`.

Equivalent client meaning:

```text
TARGET PAGE / URL OR ROUTE
PAGE TYPE
PARENT / SECTION
PAGE PURPOSE
ONE PRIMARY USER TASK / INTENT
PRIMARY QUERY + INDIVIDUAL WORDSTAT INDICATOR
TOP SECONDARY QUERIES + INDIVIDUAL WORDSTAT INDICATORS
MEMBER PHRASE COUNT
RECOMMENDED H1
TITLE DIRECTION / DRAFT FOR CREATE/OPTIMIZE OR EXPLICIT BLOCKER
ANALYTICAL SEO PRIORITY + BASIS
SEMANTIC SCOPE / CLUSTER
OWN COVERAGE
SUPPORT / MENTION / LINK TOPICS WHEN MATERIAL
ELSEWHERE / NAMED OWNER / NO-STANDALONE BOUNDARY WHEN MATERIAL
SUPPORTING / CHILD / RELATED PAGES WHEN MATERIAL
CURRENT URL MATCH / CURRENT STATE
TARGET ACTION = CREATE | OPTIMIZE | ROUTE | KEEP | NO_STANDALONE | RECHECK
REAL SITE CHANGE = YES | NO | UNRESOLVED
IMPLEMENTATION DETAIL WHEN CHANGE IS REAL AND RESOLVED
ACCEPTANCE / TARGET END STATE
UNCERTAINTY / CLARIFICATION WHEN REQUIRED
```

The following is a hard quality rule:

```text
NORMALIZED OWN COVERAGE ∩ UNEXPLAINED ELSEWHERE = ∅
```

`KEEP` is a full target-page specification outcome, not an omission. However, full authority does not require one full PDF page per KEEP role.

### J. Current → target change delta
The physical change register is a **subset** of the full page-spec register.

The client must distinguish semantic mapping only, structural KEEP/no-change, content/section change, navigation/link change, create/split/merge candidate, recheck/clarification and deferred/hold states.

### K. READY implementation specifications
Every physical change shown as ready must be self-contained enough to execute: page/object, why, what to do, where/context when material, preservation boundary and acceptance check.

### L. Clarifications / checks
Every useful but not-ready change must state exactly what must be clarified/checked, why, how, and what decision becomes possible afterward.

### M. Page relationships
Where internal relationships are recommended, explain source/target meaning, visitor purpose and implementation direction. Current literal link state and recommended state remain separate.

### N. Analytical explanation
The analytical layer must visibly show the **target site/page model**, not mainly counts. It must explain demand/task directions, how clusters became landing pages, target page registry/hierarchy, current-vs-target match and meaningful examples.

Required architecture presentation:

```text
SCANNABLE TREE / INDENTED HIERARCHY / BRANCH VIEW
+
DETAILED TABLE AS COMPANION
```

### O. Acceptance / measurement interface
Each READY physical change has an observable implementation acceptance check. No invented ranking/traffic uplift or schedule.

## 3. Physical package — retained

Base MK02 package remains:

```text
1. XLSX — semantic core + phrase map + landing map + target structure + page specs + delta
2. PDF — analytical target-structure / landing-map report
3. PDF — complete target-page register + detailed page-spec / site-improvement TZ
4. short Kwork/chat handoff message — not a separate file
```

A mandatory duplicate DOCX is not part of base V1.

## 4. Carrier-role mapping

| Logical need | Primary carrier |
|---|---|
| Full phrase-level semantic core | XLSX |
| Phrase→target page mapping with individual demand | XLSX |
| Cluster→target landing map | XLSX + analytical PDF summary/examples |
| Target page registry / hierarchy | XLSX + analytical PDF |
| Scannable architecture tree | analytical PDF + XLSX hierarchy view |
| Current-site reconciliation | XLSX + analytical PDF summary |
| Full page-by-page target specs | XLSX + compact complete TZ register |
| Detailed CREATE/OPTIMIZE/ROUTE/RECHECK specs | TZ PDF + XLSX |
| Material KEEP exception detail | TZ PDF when needed + XLSX always |
| Physical change delta / READY tasks | XLSX + TZ PDF |
| Clarifications / recheck / unresolved | XLSX + TZ PDF |
| Page relationships | XLSX; TZ PDF when action-relevant |
| Analytical explanation | analytical PDF |
| Acceptance / verification | TZ PDF + XLSX detail |

## 5. Critical non-equivalences

```text
PHRASE→TARGET MAP != CLUSTER→LANDING MAP
TARGET LANDING != CURRENT PAGE MATCH
TARGET ARCHITECTURE != CURRENT SITE TOPOLOGY
FULL PAGE SPEC != PHYSICAL CHANGE TICKET
NO SITE CHANGE != NO DELIVERABLE ENTRY
KEEP VISIBLE != ONE FULL PDF PAGE PER KEEP
SMALL CHANGE DELTA != SMALL PRODUCT RESULT
THOUSANDS OF PHRASES IN PDF != USEFUL PAGE-BY-PAGE TZ
ANALYTICAL SEO PRIORITY != IMPLEMENTATION ORDER
WORDSTAT INDIVIDUAL COUNTS != SUMMABLE PAGE TRAFFIC FORECAST
```

## 6. Rehearsal honesty

Do not pretend an existing site has no pages or no current routing.

Correct mode:

```text
REAL CURRENT SITE = AS-IS EVIDENCE
CURRENT ROUTING = NOT PRE-ACCEPTED AS TARGET ANSWER
TARGET LANDING MODEL = INDEPENDENTLY DERIVED FROM SEMANTICS/TASKS
THEN TARGET MODEL IS RECONCILED WITH CURRENT SITE
```

## 7. Client-language contract

Russian ordinary headings/statuses/reasons/instructions. Internal action IDs, Stage/Step labels, repository filenames, QA IDs and enums do not appear as ordinary client vocabulary. Document identity is based on purpose/result.

## 8. Data-truth contract

All client views derive from the current accepted authority chain. No polished workbook/report may override canonical semantic/cluster/target-page/action truth.

## 9. Explicit exclusions

No client artifact may imply completion of Google research/SEO, competitor-derived semantic gap research, Alice/Yandex Neuro/GenSearch/AEO analysis, website coding, full technical SEO audit, guaranteed rankings/traffic/leads/revenue, standalone historical harmful-cannibalization audit, or a production schedule without real owner/effort/capacity/timing inputs.

Description production for every page is not silently added merely because H1/Title direction is part of page-spec quality.

## 10. Release boundary

The package cannot pass until:

```text
SEMANTIC ROW ACCOUNTING PASS
+ PHRASE→TARGET MAP ACCOUNTING PASS
+ WORDSTAT-IN-MAPPING PASS
+ CLUSTER→LANDING MAP PASS
+ TARGET PAGE REGISTRY / HIERARCHY PASS
+ PRIMARY/SECONDARY KEYWORD + INDIVIDUAL DEMAND PASS
+ PAGE-BOUNDARY COHERENCE PASS
+ H1 / APPLICABLE TITLE PASS
+ ANALYTICAL SEO PRIORITY / BASIS PASS
+ CURRENT-SITE RECONCILIATION PASS
+ FULL PAGE-SPEC COVERAGE PASS
+ PHYSICAL CHANGE DELTA / READINESS PASS
+ ANALYTICAL TARGET-MODEL + SCANNABLE TREE PASS
+ TZ COMPACT-REGISTER + DETAILED-ACTION-CARDS PASS
+ CLIENT LANGUAGE PASS
+ XLSX USABILITY / PACKAGE QA PASS
+ BOTH PDF RENDER / RECIPIENT QA PASS
+ YANDEX-ONLY BOUNDARY PASS
+ PERSISTENCE / REMOTE READBACK PASS
```

Hard release failures:

```text
DELTA-ONLY CLIENT PACKAGE
TARGET MODEL DERIVED ONLY BY COPYING CURRENT URLS
KEEP/NO_CHANGE TARGET PAGES MISSING FROM PAGE SPECS
TARGET STRUCTURE NOT UNDERSTANDABLE WITHOUT CURRENT SITE
PRIMARY MAPPING REQUIRES ANOTHER SHEET TO SEE DEMAND
PAGE SPEC MIXES HETEROGENEOUS PRIMARY TASKS
OWN COVERAGE AND ELSEWHERE CONTRADICT WITHOUT EXPLANATION
MECHANICAL FULL-PAGE EXPANSION OF EVERY KEEP ROLE
```
