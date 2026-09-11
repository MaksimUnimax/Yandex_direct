# MK02 — QA AND RELEASE

Status: **ACTIVE / PHASE 7 MARKET-GRADE CORRECTION PASS / PHASE 8 ECONOMICS NEXT**

MK02 must not pass on one generic green status. Semantic correctness, target landing mapping, current-page reconciliation, target architecture, page-spec completeness, implementation readiness, recipient usability and persistence are independent gates.

Owner correction authorities:

- `PHASE_7_OWNER_PRODUCT_GAP_CORRECTION_2026-09-10.md`;
- `PHASE_7_OWNER_MARKET_GRADE_QUALITY_CORRECTION_2026-09-10.md`.

## G0 — Scope / Yandex-only gate

PASS only when delivered work matches the frozen existing-site MK02 order: site, region, included/excluded directions and known change constraints. Google and AI/Alice/Neuro are neither required nor implied. Competitor Step5A is absent from base.

## G1 — Acquisition / persistence gate

Verify executed Wordstat/Search/private-Yandex actions against their manifests. Every governed useful occurrence/observation is durably preserved with required provenance and provider limitations. Useful acquisition is saved/read back before later material acquisition.

## G2 — Semantic accounting gate

Reconcile raw occurrences → unique phrases → final semantic states. Silent row loss=0. Duplicate current phrase keys=0. Excluded/review rows remain explicitly represented.

## G3 — Semantic decision gate

Adversarially challenge KEEP/REVIEW/EXCLUDE decisions. No default KEEP, no frequency-only relevance decision, no association auto-keep. Uncertainty preserved.

## G4 — Semantic Search-evidence gate

Where ordinary Yandex Search is used for semantic resolution:

- exact query/region/surface/time recorded;
- raw/projection fidelity explicit;
- exact observation not generalized beyond evidence;
- controls vs dataset joins reconciled;
- Search absence never used as site absence.

If Search not required, state `NOT_REQUIRED` rather than inventing work.

## G5 — Clustering semantic gate

Check whole-phrase task coherence, current-domain profile, intent/result compatibility, member consistency, representative phrase validity and unresolved cases. No target cluster count. Corrected cluster/unit changes must rebuild all derived fields.

## G6 — Target landing-map accounting and role gate

Corrected Step10 is **target-first**. Verify:

```text
CURRENT ACCEPTED SEMANTIC ACTIVE KEYS == PHRASE→TARGET MAP KEYS
ACTIVE APPLICABLE PHRASES WITHOUT TARGET ROUTE / EXPLICIT UNRESOLVED STATE = 0
MATERIAL CLUSTERS WITHOUT TARGET LANDING SPEC = 0
LEGACY DOWNSTREAM-ONLY ACTIVATIONS = 0
SILENT ACTIVE DROPS = 0
```

For every active phrase preserve phrase → cluster/task → intended target landing-page key → target URL/route or explicit no-standalone/unresolved state.

For every material cluster preserve one intended primary landing-page specification with page purpose, intent, page type, representative demand, member count, parent/section and current-match state kept separately.

Client-visible mapping must distinguish intended target landing, current page match/current owner, exact phrase owner, family/structural-unit owner, supporting page and observed Search-relevant URL.

Hard failures:

```text
TARGET LANDING SPECS DERIVED ONLY BY COPYING CURRENT URLS = FAIL
CURRENT SITE INVENTORY USED AS THE TARGET MODEL ITSELF = FAIL
```

## G7 — Target landing/page-ownership coherence gate

Adversarially reopen broad/weak/mixed units, object-vs-component, commercial-vs-information/service/DIY, plausible lexical-only URLs and medium/low-confidence assignments. Representative query cannot substitute for full-member review.

Multiple materially different terminal tasks cannot be forced into one landing page merely because the current site already combines them.

## G8 — Structural-action evidence gate

Every material target landing spec receives an action state. Verify phrase count is not CREATE proof; current-content reuse precedes CREATE; old inventory absence is not current absence; no action proves itself; real-site-change state is explicit; KEEP/no-change pages remain in the register; NO_STANDALONE has an explicit owner/parent; corrections propagate atomically.

```text
SMALL ACTION DELTA IS ALLOWED
SMALL TARGET-PAGE DELIVERABLE CAUSED BY DROPPING KEEP/NO_CHANGE IS NOT
```

## G9 — Competing-page / cannibalization claim gate

Verify:

```text
RELATED PAGES LABELLED CANNIBALIZATION WITHOUT QUALIFYING EVIDENCE = 0
CURRENT SERP SNAPSHOT USED AS HISTORY = 0
HARM CLAIM WITHOUT HARM EVIDENCE = 0
DESTRUCTIVE REMEDIATION EXCEEDING EVIDENCE = 0
KNOWN FIRST-PARTY HISTORY SOURCE SILENTLY SKIPPED = 0
```

## G10 — Target architecture / current-site reconciliation gate

Correct order is mandatory:

```text
TARGET LANDING SPECS
→ TARGET PAGE REGISTRY
→ TARGET HIERARCHY / TREE
→ TARGET PAGE ROLES
→ CURRENT SITE DISCOVERY / RECONCILIATION
→ CURRENT→TARGET DELTA
```

Target structure must be understandable without opening the current website. Current literal internal links and recommended links remain separate. AI evidence is not used in Search-only architecture freeze.

Hard failures:

```text
TARGET ARCHITECTURE = CURRENT URL INVENTORY + SMALL DELTA = FAIL
TARGET TREE OMITTED BECAUSE CURRENT SITE IS ALREADY GOOD = FAIL
```

## G11 — Full page-spec + implementation-delta completeness gate

Step14 produces:

```text
A. FULL TARGET PAGE SPECIFICATION REGISTER
B. PHYSICAL CURRENT→TARGET IMPLEMENTATION DELTA
```

For every material target page require page/route, page type, parent/section, page purpose, one primary task/intent, primary query, member count, semantic scope, own coverage, support/elsewhere boundary, related pages, current match/state, target action, real-site-change state, implementation detail when resolved, acceptance/end state and uncertainty/clarification.

For every READY physical change also require resolved implementation mode, exact change, exact placement/context where material, dependencies, preservation and matching acceptance.

Hard failures:

```text
MATERIAL TARGET PAGE WITHOUT PAGE SPEC = FAIL
KEEP TARGET PAGE WITHOUT PAGE SPEC = FAIL
CHANGE-ONLY REGISTER PRESENTED AS THE FULL TZ = FAIL
```

## G12 — Priority / scheduling honesty gate

Analytical priority and production scheduling remain separate.

```text
UNKNOWN EFFORT TREATED LOW = 0
UNKNOWN OWNER TREATED ASSIGNABLE = 0
NUMBERING IMPLIED SCHEDULE WITHOUT CALIBRATION = 0
CLIENT BUSINESS IMPORTANCE INVENTED = 0
TIMELINE / CAPACITY INVENTED = 0
ANALYTICAL SEO PRIORITY PRESENTED AS IMPLEMENTATION ORDER = 0
```

## G13 — Client deliverable data / cross-view consistency gate

All promised logical client views must be materialized through the frozen physical package. Cross-reconcile semantic phrase view, cluster/task view, phrase→target landing view, cluster→target landing view, target page registry/structure view, current-site/current-match view, full page-spec view, current→target delta, readiness/keep/recheck views, narrative findings and TZ report.

Contradiction or missing promised view = FAIL.

Hard failure:

```text
DELTA-ONLY CLIENT PACKAGE = FAIL
```

## G14 — Recipient language / report quality gate

For Russian client artifacts:

- ordinary headings/statuses/reasons/instructions are Russian;
- internal IDs/files/QA enums/Stage/Step vocabulary do not leak;
- XLSX is scanned through visible cells and raw package XML/table metadata;
- client-text normalization is not bypassed;
- phrase→page, cluster→page and page→structure views explain WHAT/WHY/HOW;
- analytical PDF visibly shows the target model, not mainly counts;
- implementation/TZ PDF includes the complete target-page plan, not only READY changes;
- thousands of phrase rows stay in XLSX;
- no fixed page-count quality proxy;
- no empty filler/template symmetry.

## G15 — Physical / recipient / persistence gate

Physical package:

```text
1 XLSX
+ 1 ANALYTICAL PDF
+ 1 IMPLEMENTATION-TZ PDF
+ SHORT HANDOFF MESSAGE
```

Open final XLSX; render/inspect both exact final PDFs; verify no clipping/overlap/broken glyphs/unreadable tables/orphan headings; verify recipient can find a target page for an arbitrary phrase/cluster; verify KEEP remains useful; verify handoff, Yandex-only boundary, exact remote identities/hashes; local-only completion = FAIL.

## G16 — Market-grade mapping usability / information-density gate

This gate prevents a technically complete target-first package from becoming hard to use or mechanically repetitive.

### Phrase mapping

The primary phrase→target-page client view must expose the preserved Wordstat demand indicator on the same row as:

```text
PHRASE
CLUSTER / TASK
TARGET PAGE
TARGET URL / ROUTE
ACTION
```

Recipient must be able to filter one target page and sort its routed phrases by demand without joining another sheet.

### Page keyword targeting

For every material page spec:

```text
PRIMARY QUERY + INDIVIDUAL WORDSTAT INDICATOR = present
TOP SECONDARY QUERIES + INDIVIDUAL WORDSTAT EACH = present where available
TOTAL ROUTED PHRASE COUNT = present
```

Normally 5–10 distinct useful secondary queries where available. No invented summed page-volume metric.

### Page-role boundary coherence

```text
EXPLICIT PRIMARY PAGE JOB COUNT = 1
UNEXPLAINED HETEROGENEOUS TERMINAL TASKS IN PRIMARY FIELD = 0
NORMALIZED OWN-COVERAGE ∩ NORMALIZED ELSEWHERE = ∅
```

Support/mention/link topics are a separate layer from own coverage and elsewhere/named-owner topics.

### H1 / Title / analytical priority

```text
MATERIAL PAGE SPECS WITHOUT RECOMMENDED H1 = 0
CREATE/OPTIMIZE WITHOUT TITLE DIRECTION OR EXPLICIT EVIDENCE BLOCKER = 0
ANALYTICAL SEO PRIORITY WITHOUT BASIS = 0
```

Title is not fabricated for KEEP pages merely for symmetry. Description is not silently added to base scope.

### Analytical PDF architecture visibility

A wide hierarchy table alone cannot satisfy the architecture-visibility test. The final analytical PDF must contain a directly scannable target tree/indented hierarchy/branch representation that exposes major sections and parent→child relationships.

### TZ PDF compression

All target pages must remain present in a complete compact register. Detailed cards must focus on CREATE / OPTIMIZE / ROUTE / RECHECK and material KEEP exceptions.

Hard failure:

```text
MECHANICAL ONE-FULL-PAGE-PER-KEEP WITH NO ADDITIONAL INFORMATION = FAIL
KEEP MISSING FROM COMPLETE REGISTER = FAIL
LONGER PDF USED AS QUALITY PROXY = FAIL
```

### Recipient tests

Using only the client package, an uninvolved recipient must be able to:

1. sort phrases of one target page by Wordstat demand directly in the mapping sheet;
2. identify primary + secondary queries and individual demand for a page;
3. identify one primary page job and distinguish own/support/elsewhere topics;
4. see recommended H1 and applicable Title direction/blocker;
5. understand architecture from a scannable tree/branch view;
6. see all KEEP roles without reading dozens of repetitive full-page cards;
7. distinguish analytical SEO priority from implementation schedule.

Any applicable failure = G16 FAIL.

## Report-stage no-new-research gate

```text
REPORT MATERIALIZATION != NEW PROJECT RESEARCH
```

Use preserved OKNO_MSK evidence unless a concrete newly identified information gap actually requires a separately authorized research/revalidation block. Do not make provider calls merely to enrich presentation.

## Failure handling

Any substantive FAIL:

```text
CLASSIFY FAILURE
→ IDENTIFY ROOT CAUSE
→ UPDATE GENERAL/PER-STEP RULE WHEN METHOD DEFECT EXISTS
→ IDENTIFY FULL IMPACT SET
→ REBUILD AFFECTED AUTHORITIES / CLIENT VIEWS
→ RUN REGRESSION + INDEPENDENT QA
→ SAVE / COMMIT / REMOTE READBACK
```

## Release classes

```text
METHOD_READY
REHEARSAL_PASS
PRODUCT_PACKAGE_READY
PUBLISHED
```

## Current boundary after second owner quality review

```text
TARGET-FIRST DATA REHEARSAL = PRESERVED
FIRST TARGET-FIRST CLIENT PACKAGE = HISTORICAL PASS UNDER SUPERSEDED QUALITY GATE
OWNER MARKET-GRADE QUALITY FINDING 2026-09-10 = SUBSTANTIVE CLIENT-PACKAGE / PAGE-SPEC FAIL
CURRENT STATE = PHASE 7 MARKET-GRADE CLIENT QUALITY CORRECTION PASS / CLOSED
G16 MACHINE QA = 58/58 PASS
FINAL RECIPIENT QA = 10/10 PASS
FINAL CLIENT PACKAGE = 1 XLSX + 2 PDF / VERSIONED MARKET-GRADE DIRECTORY
PHASE 8 PRICE/LIMITS/ECONOMICS = CURRENT / NOT YET EXECUTED
NEXT_ACTION = EXECUTE_PHASE_8_MK02_PRICE_LIMITS_ECONOMICS
```
