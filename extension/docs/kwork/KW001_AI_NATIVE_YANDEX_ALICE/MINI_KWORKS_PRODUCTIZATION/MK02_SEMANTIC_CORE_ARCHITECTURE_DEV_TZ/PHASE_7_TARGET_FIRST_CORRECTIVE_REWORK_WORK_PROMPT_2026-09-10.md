# MK02 — PHASE 7 TARGET-FIRST CORRECTIVE REWORK — WORK EXECUTION PROMPT

You are continuing the existing Kwork / Yandex Marketing Bridge productization work.

THIS IS NOT A NEW PROJECT.
THIS IS NOT A NEW MARKET RESEARCH TASK.
THIS IS NOT PHASE 8.
THIS IS A SUBSTANTIVE CORRECTIVE REWORK OF MK02 PHASES 5–7 AFTER OWNER PRODUCT-RECIPIENT REVIEW FOUND A PRODUCT-GAP.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Product root:
`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/MINI_KWORKS_PRODUCTIZATION/MK02_SEMANTIC_CORE_ARCHITECTURE_DEV_TZ`

Level-2 rehearsal root:
`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/MINI_KWORKS_PRODUCTIZATION/MK02_SEMANTIC_CORE_ARCHITECTURE_DEV_TZ/tests/OKNO_MSK`

## 0. FIRST READ / LIVE STATE

Before editing anything:

1. Read the live branch HEAD from GitHub.
2. Read in full:
   - `../MINI_KWORK_DEVELOPMENT_PROTOCOL.md`
   - `PRODUCT_ROADMAP.md`
   - `PRODUCT_SCOPE.md`
   - `PHASE_7_OWNER_PRODUCT_GAP_CORRECTION_2026-09-10.md`
   - `STEP_RULES_INDEX.md`
   - `steps/STEP_09_TASK_FIRST_CLUSTERING.md`
   - `steps/STEP_10_PAGE_OWNERSHIP_MAPPING.md`
   - `steps/STEP_11_STRUCTURAL_ACTION_DIAGNOSIS.md`
   - `steps/STEP_12_COMPETING_PAGE_SAFETY.md`
   - `steps/STEP_13_SEARCH_ONLY_ARCHITECTURE_FREEZE.md`
   - `steps/STEP_14_IMPLEMENTATION_SPECIFICATION.md`
   - `steps/STEP_15_CLIENT_MATERIALIZATION_QA.md`
   - `DELIVERABLE_SPEC.md`
   - `QA_AND_RELEASE.md`
   - `ERRORS_AND_LESSONS.md`
   - `GENERAL_RULES.md`
   - `PRODUCT_PACKAGING.md`
   - latest Phase-5/6/7 OKNO_MSK authorities, machine QA, recipient QA and remote readback receipts.
3. Reconcile the live HEAD with the handoff. Preserve unrelated concurrent work. No force push.

Do not continue if you have not read the corrected target-first rules.

## 1. DEFECT BEING CORRECTED

The previous client package was physically valid but under-delivered the sold MK02 value.

Old effective path:

```text
CURRENT SITE PAGES
→ CURRENT OWNERSHIP
→ SMALL CURRENT→TARGET DELTA
→ A FEW IMPLEMENTATION TASKS
```

This caused a mature site such as OKNO_MSK to produce a client-facing result that looked like a small site audit even though MK02 sells:

```text
SEMANTIC CORE
+ PHRASE→PAGE MAPPING
+ CLUSTER→LANDING PAGE MAPPING
+ TARGET SEO STRUCTURE
+ PAGE-BY-PAGE SPECIFICATION
+ IMPLEMENTATION DELTA
```

The correction is **not** to pretend OKNO_MSK has no pages or no current routing.

Correct mode:

```text
REAL CURRENT SITE = AS-IS EVIDENCE
CURRENT ROUTING = NOT PRE-ACCEPTED AS TARGET ANSWER
TARGET LANDING MODEL = INDEPENDENTLY DERIVED FROM ACCEPTED SEMANTICS / USER TASKS
THEN TARGET MODEL IS RECONCILED WITH CURRENT SITE
```

## 2. DATA BOUNDARY

Reuse preserved accepted OKNO_MSK evidence.

Known historical Phase-5 counts for reconciliation only:

```text
SEMANTIC UNIVERSE = 2840
WORKING = 2185
REVIEW = 187
EXCLUDED = 468
```

Do not change these merely to make a nicer document.

Do not perform new Wordstat, Yandex Search, Alice/Neuro/GenSearch, Google or competitor-provider calls just because the package is being rebuilt.

If the corrected target-first transformation exposes a concrete evidence gap, preserve an unresolved/recheck state. A new provider call requires a separately justified/authorized research block.

Step5A competitor-derived expansion remains excluded.
Google remains excluded.
AI/Alice/Neuro remain excluded.

## 3. CORE EXECUTION — TARGET-FIRST MAPPING

Use the accepted working phrases and task/intent clusters as input.

### 3.1 Phrase-level target map

Materialize one row for every active working phrase:

```text
phrase_key
phrase
cluster/task key
cluster/task human name
intent / user task
target_landing_page_key
target route state
target URL if resolved after proper reconciliation
current page match kept separately
uncertainty / reason
```

Every working phrase must have exactly one target landing route or an explicit unresolved/no-standalone state. Silent drops = 0.

Do not assign target landing pages merely by copying current URLs.

### 3.2 Cluster→landing-page map

Materialize one row for every material cluster/task:

```text
cluster/task key
human cluster/task name
primary / representative query
member phrase count
intent / user task
intended landing-page key
page purpose
page type
intended parent / section
provisional target route before current-site reconciliation
supporting/child relation where material
current match state kept separately
uncertainty / evidence boundary
```

The landing-page unit is driven by task/intent and expected page role, not by current-site URL convenience.

Do not force one page per phrase.
Do not force one page per cluster if evidence supports a no-standalone/parent route.
Do not force a target page count.

### 3.3 Target page registry / target SEO hierarchy

From the independent landing model, build the target page registry and a human-readable hierarchy/tree.

For every material target page preserve:

```text
target_page_key
page purpose
page type
primary task / intent
primary / representative query
member phrase count
semantic scope / cluster keys
target route / URL state
parent / section
child/supporting relationships when material
```

Only after this target registry/hierarchy exists, reconcile it against the actual current site.

## 4. CURRENT-SITE RECONCILIATION

Use the real current OKNO_MSK public-site inventory/evidence already preserved by the project, refreshed only if the current method/evidence freshness rule actually requires a site read and it can be done without prohibited provider research.

For each target page classify an equivalent state:

```text
EXISTING_MATCH
EXISTING_NEEDS_OPTIMIZATION
EXISTING_RELATIONSHIP_CHANGE
NEW_PAGE_CANDIDATE
NO_STANDALONE_PAGE_ROUTE_TO_PARENT
UNRESOLVED
```

A current page may become the accepted target URL after the target role has independently been defined and the page is shown to fit it.

Do not fabricate a new page when a current page adequately owns the target task.
Do not fabricate an exact new slug when the route is not sufficiently resolved; use a provisional route/page key and explicit uncertainty.

## 5. ACTION STATE FOR EVERY TARGET PAGE

Every material target landing/page spec must receive an action state:

```text
CREATE
OPTIMIZE / STRENGTHEN
ROUTE / INTERNAL-LINK CHANGE
KEEP / LOCK AS TARGET OWNER
NO_STANDALONE — INCLUDE IN NAMED PARENT/OWNER
RECHECK / NEEDS EVIDENCE
```

Also preserve:

```text
REAL SITE CHANGE REQUIRED = YES | NO | UNRESOLVED
```

Critical rule:

```text
KEEP / NO_CHANGE != DROP FROM DELIVERABLE
```

A page that already matches the target must still have a complete page specification.

## 6. FULL PAGE-BY-PAGE TARGET SPECIFICATION

Materialize one specification for every material target page.

Required client meaning:

```text
Target page / URL or route
Page type
Parent / section
Page purpose
Primary user task / intent
Primary / representative query
Member phrase count
Semantic scope / cluster
What this page should cover
What belongs elsewhere / what should not become a separate page when material
Supporting / child / related pages when material
Current URL match / current state
Target action = CREATE | OPTIMIZE | ROUTE | KEEP | NO_STANDALONE | RECHECK
Real site change = YES | NO | UNRESOLVED
Implementation detail if a real change is resolved
Acceptance / target end state
Uncertainty / exact clarification if needed
```

Full individual phrase membership remains in XLSX. Do not dump 2185 phrase rows into PDF.

## 7. REQUIRED LEVEL-2 AUTHORITIES

Create versioned corrected authorities under the OKNO_MSK test root. Use clear names equivalent to:

```text
TARGET_FIRST_PHRASE_LANDING_MAP_2026-09-10.tsv
TARGET_FIRST_CLUSTER_LANDING_MAP_2026-09-10.tsv
TARGET_PAGE_REGISTRY_2026-09-10.tsv
TARGET_ARCHITECTURE_HIERARCHY_2026-09-10.tsv or .md
CURRENT_TARGET_RECONCILIATION_2026-09-10.tsv
TARGET_PAGE_SPEC_REGISTER_2026-09-10.tsv
CURRENT_TARGET_CHANGE_DELTA_2026-09-10.tsv
```

Exact filenames may follow existing repository conventions, but the logical authorities must exist separately and be joined by stable keys.

Do not overwrite historical Phase-7 evidence as though it never existed. Preserve history and mark superseded client content explicitly.

## 8. REBUILD THE CLIENT XLSX

Create a corrected client workbook from the corrected authorities.

Mandatory easily discoverable client views/sheets equivalent to:

```text
1. Начните здесь
2. Все запросы
3. Кластеры / задачи
4. Рассадка запросов по страницам
5. Посадочные страницы / кластер→страница
6. Целевая структура сайта
7. ТЗ по страницам / спецификации страниц
8. Изменения сайта / current→target delta
9. Проверить / уточнить / отложено
10. Связи страниц where material
```

Keep useful existing supporting sheets if they add recipient value. Do not preserve a fixed sheet count merely for regression aesthetics.

Required workbook behavior:

- filterable tables;
- frozen headers where useful;
- readable widths/wrapping;
- no internal Stage/Step/action-enum jargon in ordinary client display;
- no formula errors;
- no stale current-site-first mapping presented as target truth;
- visible explanation of WHAT / WHY / HOW for mapping/structure sheets.

## 9. REBUILD ANALYTICAL PDF

The analytical PDF must no longer be mainly a statistical summary.

Its purpose is to show the client the **target semantic/site model**.

Required content:

1. What site/region and Yandex demand were studied.
2. Semantic-core totals and limitations, briefly.
3. Main user-task/demand directions.
4. How queries were grouped into landing-page tasks.
5. The target landing-page map at useful human scale.
6. Target page registry summary.
7. Target SEO hierarchy/tree or hierarchical table.
8. Representative examples: cluster → target page.
9. Current-vs-target reconciliation summary.
10. Counts/classes of EXISTING_MATCH / OPTIMIZE / CREATE candidate / NO_STANDALONE / RECHECK as actually derived.
11. Important KEEP/no-change findings as evidence that the current site matches the designed target, not as absence of work.
12. Where the complete phrase-level mapping lives in XLSX.
13. Boundaries/uncertainty.

Do not invent a page-count target. Make it as long as needed for useful recipient comprehension.

## 10. REBUILD TZ PDF

The second PDF must become a **page-by-page target specification / site-improvement TZ**, not a short list of a few physical changes.

It must let the recipient understand for every material target page, directly or through a complete register plus grouped detailed specifications:

```text
what page this is
what demand / cluster lands there
what user task it serves
where it sits in the target structure
what target/current URL applies
whether it already exists/matches
CREATE / OPTIMIZE / ROUTE / KEEP / NO_STANDALONE / RECHECK
what must change, if anything
what the target end state is
how a real change is accepted
what exact clarification is needed if unresolved
```

KEEP pages remain visible.
NO_STANDALONE tasks must name the parent/owner page.
Physical change tickets are a subset of the full page specification.

Do not paste thousands of phrases into the PDF.

## 11. GENERATOR / VALIDATOR CORRECTION

Do not hand-patch only final binaries.

Update the workbook/report generators and validators so a future MK02 execution automatically produces/requires:

```text
phrase→target map
cluster→landing map
target page registry/hierarchy
page-spec register including KEEP/no-change
delta as subset
```

Add regression capable of rejecting:

```text
CURRENT-SITE-FIRST MAP WITHOUT TARGET MODEL
DELTA-ONLY CLIENT PACKAGE
KEEP/NO_CHANGE TARGET PAGES DROPPED
NO-STANDALONE WITHOUT OWNER/PARENT
TARGET ARCHITECTURE = CURRENT URL INVENTORY + DELTA
PDF WITH COUNTS BUT NO TARGET MODEL
TZ PDF WITH ONLY READY CHANGE TICKETS
```

Do not encode fragile hard-coded cell positions, page counts or fixed number of target pages/sheets.

## 12. METHODOLOGY PROPAGATION

The core corrected per-step rules are already being materialized by the main chat.

During corrective execution, verify consistency of:

```text
PRODUCT_SCOPE.md
STEP_RULES_INDEX.md
steps/STEP_10...
steps/STEP_11...
steps/STEP_13...
steps/STEP_14...
steps/STEP_15...
DELIVERABLE_SPEC.md
QA_AND_RELEASE.md
PRODUCT_ROADMAP.md
PRODUCT_PACKAGING.md
ERRORS_AND_LESSONS.md
GENERAL_RULES.md
SERIES_ROADMAP.md
```

If any still say or imply:

```text
MK02 = current-page audit + TZ only on changes
```

correct them to the target-first/full-page-spec model.

Add the reusable failure class to `ERRORS_AND_LESSONS.md` and the cross-step non-repeat rule to `GENERAL_RULES.md` if not already present.

Do not modify unrelated mini-kworks except a necessary series cursor/status line.

## 13. QA / RECIPIENT TESTS

At minimum prove:

```text
WORKING PHRASES == PHRASE→TARGET ROWS OR EXPLICIT ROUTE ACCOUNTING
SILENT WORKING PHRASE DROPS = 0
MATERIAL CLUSTERS WITHOUT TARGET LANDING SPEC = 0
MATERIAL TARGET PAGES WITHOUT PAGE SPEC = 0
KEEP TARGET PAGES WITHOUT PAGE SPEC = 0
NO-STANDALONE WITHOUT NAMED PARENT/OWNER = 0
TARGET ARCHITECTURE DERIVED ONLY BY COPYING CURRENT URLS = 0
PHYSICAL CHANGE TICKETS ⊆ FULL PAGE-SPEC REGISTER
```

Recipient test using only final client files:

1. Pick an arbitrary working phrase: can recipient find its target landing page?
2. Pick an arbitrary material cluster: can recipient find its landing page and understand why?
3. Can recipient understand the full target structure without opening the live site?
4. Can recipient see which target pages already exist/match vs need optimization/create/route/recheck?
5. Can recipient understand the target role of a KEEP page?
6. Can recipient execute every READY physical change without doing the analyst's work again?

Any failure of 1–5 = product package FAIL.

## 14. PHYSICAL FILE QA

For final XLSX:

- open/read workbook;
- scan visible client cells;
- scan raw XLSX package XML/table metadata for internal-token leakage;
- formula-error scan;
- usability/layout inspection.

For both PDFs:

- inspect exact final bytes;
- parse/text scan;
- render every final page;
- inspect clipping, overlap, broken glyphs, unreadable tables, orphan headings and broken page flow;
- re-render after every material PDF correction.

Do not certify final bytes using an earlier render.

## 15. PERSISTENCE / SEMANTIC CHECKPOINTS / COMMITS / READBACK

This is a long Work execution. Do **not** keep completed work only in Work memory, local scratch files or the conversation until the end.

Checkpointing is based on **completed meaningful blocks**, not on time:

```text
DO NOT COMMIT EVERY MINUTE
DO NOT COMMIT EVERY ROW
DO NOT ACCUMULATE HOURS OF FINISHED WORK ONLY IN THE DIALOGUE

WHEN A MEANINGFUL BLOCK IS COMPLETE AND INTERNALLY CONSISTENT,
SAVE IT DURABLY BEFORE STARTING THE NEXT LARGE BLOCK
```

For this corrective task, suitable checkpoint boundaries include, as they become complete:

```text
1. SOURCE / INPUT RECONCILIATION COMPLETE
2. PHRASE→TARGET + CLUSTER→LANDING AUTHORITIES COMPLETE
3. TARGET PAGE REGISTRY + TARGET HIERARCHY COMPLETE
4. CURRENT↔TARGET RECONCILIATION + PAGE-SPEC REGISTER COMPLETE
5. GENERATORS / VALIDATORS CORRECTED
6. CLIENT XLSX COMPLETE + ITS QA COMPLETE
7. ANALYTICAL PDF COMPLETE + FINAL-BYTE QA COMPLETE
8. TZ PDF COMPLETE + FINAL-BYTE QA COMPLETE
9. METHODOLOGY / STATE RECONCILIATION COMPLETE
10. FINAL REMOTE READBACK / RECEIPT COMPLETE
```

These are examples of semantic boundaries, not a requirement to manufacture exactly ten commits. Combine adjacent blocks when they are naturally one coherent unit; split a block only when it is genuinely too large to hold safely until completion.

For every completed material block:

```text
SAVE ACTUAL REUSABLE OUTPUTS
→ RECORD WHAT IS COMPLETE / WHAT REMAINS
→ COMMIT WITH A DESCRIPTIVE CHECKPOINT MESSAGE
→ PUSH / SAFE REF UPDATE
→ REMOTE READBACK
→ ONLY THEN CONTINUE THE NEXT LARGE BLOCK
```

Do not treat a prose status message as persistence. The actual TSV/JSON/MD/generator/client-source/QA material that represents the completed work must be durably saved.

If a single block is too large and interruption/hanging would destroy substantial progress, persist a deterministic resumable partial checkpoint. Mark it explicitly:

```text
IN_PROGRESS
PARTIAL
NOT_FINAL_AUTHORITY
```

Such a checkpoint must include enough state to resume without reconstructing work from dialogue memory, where material:

```text
SOURCE COMMIT / AUTHORITY IDS
LAST COMPLETED KEY / BATCH / CURSOR
COMPLETED OUTPUT PATHS
ROW / ENTITY ACCOUNTING SO FAR
OPEN ITEMS / KNOWN FAILURES
EXACT NEXT RESUME ACTION
```

A partial checkpoint may be committed and pushed for recovery, but it must not be called PASS/final authority.

Hard failures:

```text
HOURS OF COMPLETED WORK ONLY IN DIALOGUE = FAIL
MEANINGFUL COMPLETED BLOCK NOT PUSHED = FAIL
FINAL-ONLY COMMIT STRATEGY FOR THIS LONG TASK = FAIL
CHECKPOINT COMMIT != FINAL PASS
```

Before every material write, account for live branch concurrency.
No force push.
Preserve concurrent unrelated work.

At the end:

1. push/commit all corrected authorities/generators/client artifacts/QA/state docs;
2. perform remote GitHub readback;
3. verify exact blob identities for text authorities and exact SHA-256 for final XLSX/PDF binaries;
4. create a final versioned remote-readback receipt;
5. verify final branch HEAD after the receipt commit;
6. report exact final HEAD and artifact identities.

## 16. PHASE BOUNDARY

DO NOT START PHASE 8.
DO NOT WRITE THE KWORK CARD.
DO NOT GENERATE COVER/VISUALS.
DO NOT PRICE THE PRODUCT.

This task ends only when:

```text
TARGET-FIRST AUTHORITIES COMPLETE
+ CLIENT XLSX REBUILT
+ ANALYTICAL PDF REBUILT
+ PAGE-SPEC/TZ PDF REBUILT
+ GENERATORS/VALIDATORS CORRECTED
+ MACHINE QA PASS
+ RECIPIENT QA PASS
+ FINAL-BYTE PHYSICAL QA PASS
+ METHODOLOGY/STATE CONSISTENCY PASS
+ COMMIT/PUSH/REMOTE READBACK PASS
```

Then set:

```text
PHASE 7 TARGET-FIRST CORRECTIVE REWORK = PASS
NEXT_ACTION = PHASE_8_MK02_PRICE_LIMITS_ECONOMICS
```

Do not stop at analysis, a plan, or a defect report. Execute the full corrective data projection, materialization, QA, persistence and remote readback.