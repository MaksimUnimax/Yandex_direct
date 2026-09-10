# MK02 — QA AND RELEASE

Status: **ACTIVE / PHASE 7 CORRECTIVE REWORK REQUIRED / PHASE 8 BLOCKED**

MK02 must not pass on one generic green status. Semantic correctness, target landing mapping, current-page reconciliation, target architecture, page-spec completeness, implementation readiness, recipient usability and persistence are independent gates.

Owner correction authority: `PHASE_7_OWNER_PRODUCT_GAP_CORRECTION_2026-09-10.md`.

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

Client-visible mapping must distinguish:

```text
INTENDED TARGET LANDING
CURRENT PAGE MATCH / CURRENT OWNER
EXACT PHRASE OWNER
FAMILY / STRUCTURAL-UNIT OWNER
SUPPORTING PAGE
OBSERVED SEARCH-RELEVANT URL
```

Hard failure:

```text
TARGET LANDING SPECS DERIVED ONLY BY COPYING CURRENT URLS = FAIL
CURRENT SITE INVENTORY USED AS THE TARGET MODEL ITSELF = FAIL
```

## G7 — Target landing/page-ownership coherence gate

Adversarially reopen broad/weak/mixed units, object-vs-component, commercial-vs-information/service/DIY, plausible lexical-only URLs and medium/low-confidence assignments. Representative query cannot substitute for full-member review.

Also verify cluster granularity is suitable for one landing-page role. Multiple materially different intents/tasks cannot be forced into one landing page merely because the current site already combines them.

## G8 — Structural-action evidence gate

Every material target landing spec receives an action state. Verify:

- phrase count not used as CREATE proof;
- current-content reuse checked before CREATE;
- old inventory absence not used as current absence;
- owner-goal evidence source visible internally;
- no action proves itself;
- rejected/outside units do not strand salvageable in-scope phrases;
- real-site-change state = YES/NO/UNRESOLVED;
- `KEEP / NO_CHANGE` target pages remain in the target page register;
- `NO_STANDALONE` tasks have an explicit parent/owner route;
- material upstream corrections propagated atomically.

Known regression checks do not replace independent global-coherence review.

Permanent rule:

```text
SMALL ACTION DELTA IS ALLOWED
SMALL TARGET-PAGE DELIVERABLE CAUSED BY DROPPING KEEP/NO_CHANGE IS NOT
```

## G9 — Competing-page / cannibalization claim gate

Execution mode must be explicit. Verify:

```text
RELATED PAGES LABELLED CANNIBALIZATION WITHOUT QUALIFYING EVIDENCE = 0
CURRENT SERP SNAPSHOT USED AS HISTORY = 0
HARM CLAIM WITHOUT HARM EVIDENCE = 0
DESTRUCTIVE REMEDIATION EXCEEDING EVIDENCE = 0
KNOWN FIRST-PARTY HISTORY SOURCE SILENTLY SKIPPED = 0
```

Base-public mode may pass without private history only with bounded historical/harm claims.

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

Verify:

- target page registry complete for all material target landing specs;
- target hierarchy/parent route present for all material target pages;
- target structure understandable without opening the current website;
- independent current site discovery performed where completeness is material;
- upstream known list does not prove its own completeness;
- current URL universe materialized;
- newly discovered relevant pages reconciled;
- current literal internal-link state separated from recommended links;
- target architecture separated from current topology;
- current match state present for every target page;
- sitemap presence not used as HTML reachability proof;
- unsupported destructive action from new discovery=0;
- AI evidence used in Search-only freeze=0.

Hard failures:

```text
TARGET ARCHITECTURE = CURRENT URL INVENTORY + SMALL DELTA = FAIL
TARGET TREE OMITTED BECAUSE CURRENT SITE IS ALREADY GOOD = FAIL
```

## G11 — Full page-spec + implementation-delta completeness gate

Step14 produces two linked outputs:

```text
A. FULL TARGET PAGE SPECIFICATION REGISTER
B. PHYSICAL CURRENT→TARGET IMPLEMENTATION DELTA
```

For every material target page require equivalent client meaning for:

```text
TARGET PAGE / URL OR ROUTE
PAGE TYPE
PARENT / SECTION
PAGE PURPOSE
PRIMARY TASK / INTENT
PRIMARY / REPRESENTATIVE QUERY
MEMBER PHRASE COUNT
SEMANTIC SCOPE / CLUSTER
WHAT THE PAGE SHOULD COVER
BOUNDARY / WHAT BELONGS ELSEWHERE WHEN MATERIAL
SUPPORTING / CHILD / RELATED PAGES WHEN MATERIAL
CURRENT MATCH / STATE
ACTION = CREATE | OPTIMIZE | ROUTE | KEEP | NO_STANDALONE | RECHECK
REAL SITE CHANGE = YES | NO | UNRESOLVED
IMPLEMENTATION DETAIL IF CHANGE IS REAL AND RESOLVED
ACCEPTANCE / TARGET END STATE
UNCERTAINTY / CLARIFICATION IF REQUIRED
```

For every item claimed READY physical change, also require:

```text
IMPLEMENTATION MODE DECLARED = true
REAL SITE CHANGE STATE RESOLVED = true
AS-IS STATE PRESENT WHEN MATERIAL = true
EVIDENCE MEANING PRESENT = true
EXACT CHANGE PRESENT = true
EXACT LOCATION / CONTEXT PRESENT WHEN REQUIRED = true
TO-BE STATE PRESENT = true
DEPENDENCIES PRESENT/NA = true
PRESERVATION REQUIREMENTS PRESENT/NA = true
ACCEPTANCE CHECK MATCHES CHANGE = true
```

Hard failures include analytical route labelled READY, ambiguous placement, analysis left to implementer, placeholders, generic cloned steps, and additionally:

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
```

Implementation specification may be ready while production sequence remains pending calibration.

## G13 — Client deliverable data / cross-view consistency gate

All promised logical client views must be materialized through the frozen physical package. Cross-reconcile:

```text
SEMANTIC PHRASE VIEW
CLUSTER / TASK VIEW
PHRASE→TARGET LANDING VIEW
CLUSTER→TARGET LANDING VIEW
TARGET PAGE REGISTRY / STRUCTURE VIEW
CURRENT SITE / CURRENT MATCH VIEW
FULL PAGE-SPEC VIEW
CURRENT→TARGET ACTION DELTA
READY / CLARIFICATION / KEEP / NO-STANDALONE / RECHECK VIEWS
NARRATIVE FINDINGS
IMPLEMENTATION/TZ REPORT
```

Contradiction or missing promised view = FAIL.

Hard failure:

```text
DELTA-ONLY CLIENT PACKAGE = FAIL
```

## G14 — Recipient language / report quality gate

For Russian client artifacts:

- ordinary headings/statuses/reasons/instructions are Russian;
- internal action IDs/filenames/QA IDs/Stage/Step/enums do not leak;
- final XLSX is scanned both through visible cells and raw package XML/table metadata;
- client-text normalization is not bypassed by a secondary generator path;
- document identity is result/purpose, not recipient profession;
- phrase→page, cluster→page and page→structure views explain WHAT/WHY/HOW;
- analytical PDF visibly shows the target site/page model, not mainly counts;
- analytical PDF includes a target hierarchy/tree or equivalent hierarchical table;
- implementation/TZ PDF visibly includes the full target-page plan/page specifications, not only READY changes;
- thousands of phrase rows remain in XLSX rather than being dumped into PDF;
- no generic defensive prohibition section;
- no provider/owner-failure/quarantine narration;
- no fixed page-count quality proxy;
- no empty TOC/filler/template symmetry.

## G15 — Physical / recipient / persistence gate

The physical package remains:

```text
1 XLSX
+ 1 ANALYTICAL PDF
+ 1 IMPLEMENTATION-TZ PDF
+ SHORT HANDOFF MESSAGE (NOT A FILE)
```

Phase-7 corrective QA must:

- open the final XLSX and verify the mandatory mapping/target-structure/page-spec views are usable;
- render and inspect **both** final PDFs independently from the exact post-correction delivery bytes;
- parse/extract and client-language-scan both PDFs, without treating parse/hash as render QA;
- verify no clipping/overlap/broken glyphs/unreadable tables/orphan headings or broken page flow;
- verify the analytical PDF independently answers: what demand exists, how it clusters, where it should land, and what the target structure is;
- verify the TZ PDF independently answers for each material target page: what it is, what lands there, where it sits, current match, action and target end state;
- verify an uninvolved recipient can locate the target page for an arbitrary working phrase and an arbitrary material cluster;
- verify KEEP/no-change pages remain useful visible specifications;
- verify the short handoff message names exactly the real three files and points to the correct starting order;
- verify the Yandex-only boundary in each client-facing file;
- persist text/binary artifacts as tooling allows;
- verify exact remote identities/hashes/readback honestly;
- treat local-only completion as FAIL.

DOCX is not a mandatory base client file.

## Report-stage no-new-research gate

```text
REPORT MATERIALIZATION != NEW PROJECT RESEARCH
```

The corrective rework must reuse preserved OKNO_MSK evidence unless a concrete newly identified information gap actually requires a separately authorized research/revalidation block. Do not make provider calls merely to make the new reports look richer.

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

One patched example is not closure.

## Release classes

```text
METHOD_READY
= scope + input contract + general rules + failure ledger + step rules + execution roadmap + logical deliverable + QA contracts complete and read back

REHEARSAL_PASS
= MK02-only OKNO_MSK projection completed under current Level-1 method + applicable G0–G15 PASS

PRODUCT_PACKAGE_READY
= rehearsal + physical client package + recipient review + price/limits + card copy accepted

PUBLISHED
= owner published product + published scope/price captured/read back
```

## Current boundary after owner product-gap finding

```text
PHASE 5 ORIGINAL OKNO_MSK REHEARSAL = HISTORICAL PASS UNDER SUPERSEDED CURRENT-SITE-FIRST CLIENT MODEL
PHASE 6 ORIGINAL PACKAGE DECISION = PHYSICAL SPLIT RETAINED
PHASE 7 ORIGINAL PHYSICAL QA = HISTORICAL PASS FOR SUPERSEDED CONTENT MODEL
OWNER PRODUCT-GAP FINDING 2026-09-10 = SUBSTANTIVE METHOD / DELIVERABLE FAIL
CURRENT STATE = PHASE 7 CORRECTIVE REWORK REQUIRED
TARGET-FIRST METHOD RULES = UPDATED
PHASE 8 PRICE/LIMITS/ECONOMICS = BLOCKED
NEXT_ACTION = REBUILD OKNO_MSK TARGET-FIRST LANDING MAP / TARGET PAGE REGISTRY / PAGE SPECS / XLSX / TWO PDF + QA + REMOTE READBACK
```
