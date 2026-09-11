# MINI-KWORK DEVELOPMENT PROTOCOL

Status: **OWNER-APPROVED / SERIES-LEVEL / MANDATORY / PRODUCTIZATION-ONLY**  
Applies to: **MK01–MK07 and any future versioned mini-kwork in this series**  
Owner approval: **2026-09-10**  
Owner large-artifact transport amendment: **2026-09-11**

Cross-Kwork large-artifact publication authority:

`../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

## 0. What this document governs

This document governs **how a mini-kwork is designed, extracted, validated, rehearsed and frozen as a commercial product**.

It is NOT a client-job execution step and must not be confused with the rules inside an already built mini-kwork.

Canonical separation:

```text
PRODUCTIZATION CONTROL PLANE
= SERIES_ROADMAP.md
+ MINI_KWORK_DEVELOPMENT_PROTOCOL.md

PRODUCT EXECUTION PLANE
= MKxx/PRODUCT_SCOPE.md
+ MKxx/CLIENT_INPUT_CONTRACT.md
+ MKxx/GENERAL_RULES.md
+ MKxx/STEP_RULES_INDEX.md
+ MKxx/steps/*.md
+ MKxx/EXECUTION_ROADMAP.md
+ MKxx/DELIVERABLE_SPEC.md
+ MKxx/QA_AND_RELEASE.md

DATA / EVIDENCE PLANE
= parent KW-001 Level-2 jobs
+ MKxx/tests/<CASE_ID>/
+ preserved provider/search/site evidence

MARKET / EXTERNAL REFERENCE PLANE
= current marketplace evidence
+ current official Yandex / industry methodology sources

CROSS-KWORK TRANSPORT PLANE
= ../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md
```

Hard rule:

```text
PRODUCTIZATION RULE != CLIENT EXECUTION RULE
LEVEL-2 EXAMPLE != LEVEL-1 METHOD
WORK EXECUTOR != PRODUCT ARCHITECT
ARTIFACT GENERATION != ARTIFACT TRANSPORT
```

## 1. Mandatory entry gate before work on any mini-kwork

Before designing or continuing MK02–MK07, or reopening a frozen MK01 version, read in this order:

1. `MINI_KWORK_DEVELOPMENT_PROTOCOL.md` — this document;
2. `../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md` — mandatory cross-Kwork transport rule whenever Work/file persistence is material;
3. `SERIES_ROADMAP.md` — current product identity, boundaries and cursor;
4. `YANDEX_ONLY_SCOPE.md` — cross-product ecosystem boundary;
5. the selected `MKxx/PRODUCT_ROADMAP.md`;
6. only then the source KW-001 authorities required by that product.

Do not start from a remembered Step number, an old client file or a Work result.

The selected mini-kwork must be named explicitly before detailed method work starts.

## 2. Source of mini-kwork identity

The source of the seven product concepts and their high-level boundaries is `SERIES_ROADMAP.md`.

For the selected mini-kwork freeze:

- what exact client result is sold;
- what is not sold;
- which neighbouring mini-kworks must remain outside scope;
- the supported operating mode, such as existing-site vs greenfield;
- Yandex-only boundary;
- whether full new semantic acquisition is included or an input is expected.

A mini-kwork is not a shortened marketing description of full KW-001. It is a standalone product with its own input contract, method, roadmap, evidence boundary, deliverable and Definition of Done.

## 3. Method source — extract from current proven KW-001, do not redesign from memory

The main method source is the **current accepted KW-001 methodology**.

For every selected mini-kwork:

1. identify which KW-001 steps/gates are causally necessary for the sold result;
2. identify which steps are unnecessary;
3. identify which steps belong to another mini-kwork;
4. read the current/latest accepted authority for every included step;
5. preserve later corrections and owner-directed gates;
6. materialize the needed logic inside the mini-kwork so it can run autonomously.

Forbidden shortcut:

```text
"USE KW-001 STEP N"
```

as the complete mini-kwork rule.

Required extraction includes, where applicable:

```text
PURPOSE
WHY THE STEP EXISTS
INPUTS
REQUIRED EVIDENCE
METHOD / EXECUTION ORDER
OUTPUTS
SOURCE KW-001 AUTHORITY
KNOWN FAILURE CLASSES
ROOT CAUSES / FALSE ASSUMPTIONS
CORRECTED METHOD
NON-REPEAT CONTROLS
CLAIM BOUNDARIES
UNKNOWN / BLOCKER BEHAVIOR
PASS GATE
CLIENT-FACING MEANING
```

## 4. Current authority wins over historical convenience

When KW-001 has multiple historical files for the same subject, do not select an authority because its filename is familiar or because it was used in an earlier report.

Use the latest accepted/canonical authority and declared correction precedence.

If a later QA, owner review, post-release correction or accepted overlay changed the method, the mini-kwork inherits the corrected state and the failure lesson that caused it.

```text
HISTORICAL FILE EXISTS != CURRENT METHOD AUTHORITY
EARLIER PASS != LATER CORRECTION INVALID
```

## 5. How OKNO_MSK and other Level-2 evidence may be used

OKNO_MSK is the principal rehearsal/reference case for this series, but it is **Level-2 evidence**, not a universal rule source by itself.

Promote only the reusable lesson:

```text
CONCRETE FAILURE
→ ROOT CAUSE
→ GENERAL NON-REPEAT CONTROL
```

Keep case-specific values in Level 2:

- domain and URL;
- exact phrase;
- row/action/query ID;
- current count;
- client-specific business fact;
- concrete page owner;
- concrete action verdict;
- provider receipt;
- test commit/hash.

Do not turn an OKNO_MSK-specific answer into a rule for an unrelated site.

## 6. Failure extraction is mandatory, not optional cleanup

For every included KW-001 stage, extract the real failure history relevant to the mini-kwork.

Each failure carried into `ERRORS_AND_LESSONS.md` should preserve:

```text
WHAT FAILED
WHY IT FAILED
FALSE ASSUMPTION / ROOT CAUSE
CORRECTED RULE
WHERE THE RULE IS ENFORCED
REGRESSION / PASS CONDITION
```

Owner-identified recipient/report failures are method inputs when they can recur in the selected mini-kwork.

Canonical closure rule:

```text
ONE BAD EXAMPLE FIXED != FAILURE CLASS CLOSED
```

## 7. Mandatory Level-1 file architecture

Before data rehearsal, the mini-kwork Level-1 method must contain at minimum:

```text
PRODUCT_ROADMAP.md
PRODUCT_SCOPE.md
CLIENT_INPUT_CONTRACT.md
GENERAL_RULES.md
ERRORS_AND_LESSONS.md
STEP_RULES_INDEX.md
steps/STEP_XX_*.md for every local step
EXECUTION_ROADMAP.md
DELIVERABLE_SPEC.md
QA_AND_RELEASE.md
```

Additional product-specific method files are allowed when genuinely needed.

Later productization phases may add:

```text
MARKET_REALITY_*.md
PRODUCT_PACKAGING.md
CLIENT_HANDOFF_TEMPLATE.md
pricing/economics authorities
KWORK_CARD.md
PORTFOLIO_ASSET_SPEC.md
freeze/readback receipts
```

Do not create empty ceremonial files just to imitate another product.

## 8. Two rule levels inside every mini-kwork

### Rule Level A — `GENERAL_RULES.md`

Cross-step invariants that govern the whole mini-kwork.

Examples include evidence discipline, uncertainty preservation, Yandex-only scope, current-site freshness, data persistence, correction propagation, recipient usability and boundaries between analytical and physical actions.

### Rule Level B — `steps/STEP_XX_*.md`

Specific execution rule for one local step.

Every local step must have its own purpose, input/evidence requirements, method, output, known failures, non-repeat controls, blockers and PASS gate.

```text
GENERAL RULE != SUBSTITUTE FOR STEP METHOD
STEP METHOD != PERMISSION TO IGNORE GENERAL RULES
```

## 9. Product boundaries are frozen before data work

Before Phase 5, explicitly define neighbouring-product boundaries.

Examples:

- MK01 ends at semantic core + clustering;
- MK02 adds ownership/architecture/evidence-supported implementation specifications, but not Step5A competitor expansion or AI;
- MK03 owns competitor-derived semantic-gap acquisition;
- MK04 owns dedicated query/page/intents/cannibalization work from an existing semantic input unless otherwise versioned;
- MK05 converts pre-existing accepted decisions into implementation-ready tasks and must not silently rerun a full research product;
- MK06 owns Yandex Search↔Alice/Neuro/AEO diagnostic work;
- MK07 is the full applicable complex.

No mini-kwork may silently give away a neighbouring product because the evidence happens to exist in the parent pilot.

## 10. Yandex-only is a series authority

All mini-kworks obey `YANDEX_ONLY_SCOPE.md`.

Google evidence/capabilities are excluded unless a future separately researched, tested and owner-approved product/version explicitly changes that rule.

Do not infer Google conclusions from Yandex evidence.

## 11. External references have separate roles

Do not mix commercial market evidence with methodological evidence.

### Market / commercial research

Use fresh Kwork, FL.ru and other legitimate current market evidence to establish:

- whether a comparable product exists;
- how the market describes it;
- typical composition;
- observed prices/budgets;
- important differences from our product.

A nearby analogue must not be labelled an exact analogue if it is not one.

### Methodology research

Use current official Yandex materials and high-quality relevant industry sources to validate method requirements when fresh research is required.

```text
MARKET ANALOGUE != METHOD AUTHORITY
METHOD ARTICLE != OUR FINAL PRICE
```

## 12. Traceability of new product rules

A material new rule must have an identifiable origin, for example:

```text
CURRENT KW-001 METHOD
KW-001 FAILURE / CORRECTION
OWNER REVIEW
OFFICIAL YANDEX SOURCE
CURRENT EXTERNAL METHOD RESEARCH
REHEARSAL-DISCOVERED METHOD DEFECT
```

Do not add a strong rule only because it “sounds right”.

## 13. Build an autonomous roadmap before touching large data

After scope, input contract, general rules, failures and per-step rules are materialized, build `EXECUTION_ROADMAP.md`.

A new executor must be able to run the selected product without reconstructing the full KW-001 project from memory.

The roadmap must make clear:

- execution sequence;
- conditional steps;
- provider/evidence boundaries;
- stop gates;
- product exclusions;
- which outputs feed which later steps;
- what constitutes final PASS.

## 14. Mandatory method consistency audit

Before Phase 5, cross-reconcile at minimum:

```text
PRODUCT_SCOPE
CLIENT_INPUT_CONTRACT
GENERAL_RULES
ERRORS_AND_LESSONS
STEP_RULES_INDEX
ALL PER-STEP RULES
EXECUTION_ROADMAP
DELIVERABLE_SPEC
QA_AND_RELEASE
```

Check that all files agree on:

- sold product identity;
- included/excluded stages;
- Yandex-only boundary;
- supported operating mode;
- uncertainty states;
- action/readiness semantics;
- neighbouring mini-kwork boundaries;
- client result;
- provider-call rules;
- QA meaning.

Known cross-file contradictions must be zero before large-data rehearsal begins.

## 15. No large-data work before method PASS

Phases 0–4 are **Level-1 productization work**.

During those phases do not perform the large OKNO_MSK mini-kwork projection, mass row transforms, new cluster rebuilds or final test deliverable generation.

```text
PHASES 0–4 = METHOD / RULES / ROADMAP
PHASE 5 = LARGE-DATA REHEARSAL
```

## 16. Phase 5 large-data rehearsal is handed to Work

After the method package passes its consistency audit and is committed/read back, prepare a dedicated `PHASE_5_WORK_PROMPT.md` or equivalent execution handoff.

Work receives a **closed execution contract**, not a request to invent the product.

Work must first read the entire current mini-kwork Level-1 method and only then touch the Level-2 data.

Work is used for the large dataset/reconciliation workload because it can carry the substantial multi-file execution through to completion.

Every Phase-5 Work prompt that can produce material files must also freeze the publication transport policy from `../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`:

```text
ARTIFACT_PUBLICATION_POLICY = NATIVE_GIT_IF_ALREADY_AUTHENTICATED | OWNER_RELAY_IF_MORE_EFFICIENT
LARGE_ARTIFACT_MODEL_TRANSPORT = FORBIDDEN_BY_DEFAULT
OWNER_RELAY_ALLOWED = true
REMOTE_READBACK_REQUIRED = true
```

## 17. Work role boundary

Canonical role split:

```text
CHAT / OWNER-CONTROLLED PRODUCTIZATION
= product architecture
+ scope
+ method extraction
+ rules
+ roadmap
+ product boundaries
+ pre-data consistency audit

WORK
= execute the already designed method on large Level-2 data
+ materialize data authorities
+ run reconciliation / QA
+ produce candidate recipient views
+ measure workload
+ report proven method defects
+ prepare efficient artifact handoff/publication when large files are produced
```

Work must not silently redesign product identity, remove required steps, add neighbouring-product scope or weaken evidence gates for convenience.

## 18. What Work must do when it finds a real method defect

A genuine rehearsal-discovered Level-1 defect is not ignored and is not patched only in OKNO_MSK.

Required sequence:

```text
NAME FAILURE CLASS
→ EXPLAIN ROOT CAUSE / FALSE ASSUMPTION
→ UPDATE LEVEL-1 ERROR LEDGER
→ UPDATE GENERAL/PER-STEP/DELIVERABLE/QA AUTHORITY AS NEEDED
→ IDENTIFY FULL LEVEL-2 IMPACT SET
→ REBUILD AFFECTED OUTPUTS
→ RERUN REGRESSION
→ PUBLISH USING APPROVED TRANSPORT
→ REMOTE READBACK
```

Only then may the affected gate return to PASS.

## 19. Rehearsal means “client bought only this mini-kwork”

Phase 5 must project OKNO_MSK as though the client bought only the selected mini-kwork.

Do not hand the full KW-001 result back under a smaller product label.

When downstream pilot artifacts contain evidence/results from excluded stages, perform a contamination audit sufficient to answer whether those excluded stages changed the current mini-kwork result.

```text
REMOVING EXCLUDED ROWS != CAUSAL CONTAMINATION AUDIT COMPLETE
```

Check downstream effects on clusters, page owners, architecture, actions, links, AI decisions, reports or other relevant outputs depending on the product.

## 20. Reuse preserved evidence before any new provider call

A rehearsal normally uses preserved evidence.

Before any new provider call:

1. search current preserved project evidence;
2. identify the exact information gap;
3. show which product decision requires it;
4. confirm the call is allowed by the rehearsal contract;
5. persist/read back useful evidence before the next material acquisition.

If evidence is genuinely unavailable and new collection is not authorized, preserve the correct `UNKNOWN / REVIEW / SEARCH_REQUIRED / HOLD / PENDING_*` state instead of inventing certainty.

## 21. Work checkpoint persistence discipline — mandatory in every Work handoff

Long Work execution must not exist only in Work memory, local scratch state or the conversation until the final answer.

Every prompt/handoff that delegates substantial data processing, reconciliation, corrective rework, report generation or other long multi-file execution to Work **MUST explicitly contain a checkpoint-persistence section**. This is part of the execution contract, not an optional operational suggestion.

Checkpointing is **semantic-block based, not clock based**:

```text
DO NOT COMMIT EVERY MINUTE
DO NOT COMMIT EVERY ROW
DO NOT WAIT UNTIL THE ENTIRE TASK IS FINISHED

PERSIST WHEN A MEANINGFUL, INTERNALLY CONSISTENT BLOCK IS COMPLETE
AND CAN BE SAFELY RESUMED FROM THAT STATE
```

Examples of suitable material boundaries depend on the product and may include:

```text
INPUT / SOURCE AUTHORITY AUDIT COMPLETE
→ CORE DATA AUTHORITY OR ONE SELF-CONTAINED DATA LAYER COMPLETE
→ MAPPING / CLUSTER / OWNERSHIP LAYER COMPLETE
→ DOWNSTREAM ACTION / RECONCILIATION LAYER COMPLETE
→ CLIENT WORKBOOK OR REPORT SOURCE COMPLETE
→ PHYSICAL ARTIFACT + QA COMPLETE
→ FINAL STATE / READBACK COMPLETE
```

A completed block must not remain only as prose in Work's dialogue. Persist the actual reusable result: machine-readable authority, source/generator change, structured checkpoint state, report source, QA receipt or other material artifact appropriate to the block.

For every completed material block:

```text
SAVE MATERIAL OUTPUTS
→ RECORD CURRENT CURSOR / WHAT IS COMPLETE / WHAT REMAINS
→ LOCAL QA
→ CHOOSE APPROVED PUBLICATION TRANSPORT
→ PUBLISH VIA NATIVE AUTHENTICATED GIT IF ALREADY RELIABLE
   OR OWNER-RELAY WEB UPLOAD WHEN MORE EFFICIENT
→ REMOTE READBACK OF THE MATERIAL STATE
→ CONTINUE FROM THAT REMOTE-RECOVERABLE CHECKPOINT
```

The old assumption that Work itself must always obtain Git credentials and push every large checkpoint is explicitly superseded.

```text
WORK SELF-PUSH REQUIRED FOR EVERY ARTIFACT = false
REMOTE-RECOVERABLE CHECKPOINT REQUIRED = true
```

If owner relay is selected:

```text
WORK FREEZES + QA'S EXACT ARTIFACT SET
→ PROVIDES DOWNLOADABLE FILES / OPTIONAL ZIP
→ PROVIDES DIRECT GITHUB UPLOAD PAGE FOR TARGET BRANCH/DIRECTORY
→ OWNER UPLOADS THROUGH NORMAL AUTHENTICATED WEB UI
→ OWNER CONFIRMS
→ WORK / MAIN CHATGPT VERIFIES REMOTE IDENTITY + QA
```

For repository publication, ZIP may be used as a transport/download container, but if the repository expects individual files Work must clearly tell the owner to extract the ZIP and upload the contained files rather than committing the ZIP itself.

Large file bytes must not be routed through model text merely because direct Git authentication failed.

Forbidden by default:

```text
BASE64 LARGE ARTIFACT
GIANT CHAT PASTE
MANY CONNECTOR CHUNKS
FULL-FILE RECONSTRUCTION THROUGH TOOL ARGUMENTS
REGENERATE VALID ARTIFACT ONLY TO SOLVE PUBLICATION AUTH
```

If one semantic block itself is too large to complete safely in a single Work session, create a **resumable partial checkpoint at a deterministic boundary** (for example, a completed batch/tranche or generated intermediate authority) and mark it explicitly:

```text
IN_PROGRESS / PARTIAL / NOT_FINAL_AUTHORITY
```

Such a partial checkpoint must record enough state to resume without reconstructing progress from conversation memory, including where material:

```text
SOURCE COMMIT / AUTHORITY IDS
LAST COMPLETED KEY / BATCH / CURSOR
COMPLETED OUTPUT PATHS
ROW / ENTITY ACCOUNTING SO FAR
KNOWN FAILURES / OPEN ITEMS
NEXT RESUME ACTION
```

A partial checkpoint must never be mislabeled PASS or final authority merely because it was published.

Hard non-repeat rules:

```text
HOURS OF COMPLETED WORK ONLY IN DIALOGUE = FAIL
MEANINGFUL COMPLETED BLOCK NOT DURABLY SAVED = FAIL
FINAL-ONLY PERSISTENCE STRATEGY FOR LONG WORK = FAIL
CHECKPOINT PUBLISHED != FINAL PASS
GIT AUTH FAILURE != RECOMPUTE COMPLETED ARTIFACT
LARGE ARTIFACT MODEL-BYTE TRANSPORT BY DEFAULT = FAIL
REMOTE-RECOVERABLE STATE > CONVERSATION-ONLY STATE
```

No force push. Preserve concurrent unrelated work. Publication boundaries must reflect meaningful recoverable progress rather than artificial commit spam.

## 21A. Owner-relay is a normal mini-kwork transport method

Canonical authority:

`../../KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

Owner relay may be used for:

```text
large TSV/CSV/JSON authorities
XLSX workbooks
DOCX/PDF reports
ZIP/evidence bundles
client deliverables
intermediate large-data checkpoints
other material files where direct Git transport is inefficient
```

Work must not spend substantial time/tokens repeatedly debugging Git authentication when the same exact artifacts can be handed to the owner for normal browser upload and then verified remotely.

Owner relay changes only the **transport actor**. It does not move analytical responsibility to the owner.

```text
OWNER RELAYS BYTES
WORK / MAIN CHATGPT OWNS METHOD + QA + REMOTE VERIFICATION
```

## 22. Phase 5 must measure workload, not set price

Work rehearsal must record real workload/volume metrics needed for commercial packaging, including whatever is material for the product:

- data rows/entities;
- manual review volume;
- Search/provider demand;
- site/page evidence volume;
- actions/cases/work packages;
- readiness/uncertainty counts;
- document/client-view sizes;
- bottlenecks.

Do not freeze final price, limits or delivery time inside Phase 5 unless the product roadmap explicitly says otherwise.

## 23. Logical deliverable before physical package

Before rehearsal, define **what the client must be able to understand/use**, not an arbitrary file count or page count.

Phase 5–6 may then determine the best physical split based on real data and recipient tasks.

```text
LOGICAL CLIENT NEED
→ REAL REHEARSAL DATA
→ PHYSICAL PACKAGE DECISION
```

Do not force every mini-kwork into the same XLSX/PDF/DOCX structure merely because another mini-kwork used it.

## 24. Client reports must answer the sold product

Permanent lesson inherited from MK01 and KW-001 recipient reviews:

```text
CLIENT REPORT != EXECUTION PROTOCOL
CORRECT COUNTS + CLEAN LAYOUT != RECIPIENT VALUE
```

An analytical client report must explain **what the research showed**.

An implementation client document must explain **what to do, why, where, how, what remains to clarify and how to check the result**.

Internal provider chronology, QA history and repository state must not become the client narrative.

## 25. Owner review follows Work rehearsal

Work Phase 5 PASS is not final product acceptance.

After Work returns:

1. review the rehearsal/result as the product owner/recipient;
2. inspect discovered method defects;
3. inspect candidate client views;
4. decide the final Phase-6 physical client package;
5. rerun/extend product QA where needed.

```text
WORK QA PASS != OWNER PRODUCT ACCEPTANCE
```

## 26. Pricing/package freeze comes after real workload evidence

Only after rehearsal and owner review should Phase 8 freeze:

- base price;
- base limits;
- add-ons;
- delivery target;
- revision boundary;
- provider-cost boundary;
- large-order/custom-quote threshold.

Use both measured rehearsal workload and refreshed market evidence.

## 27. Kwork card follows the proven product

The card is written from the accepted product, not the other way around.

It must agree with current:

```text
PRODUCT_SCOPE
CLIENT_INPUT_CONTRACT
DELIVERABLE / PACKAGING
PRICE / LIMITS
QA / CLAIM BOUNDARIES
```

Do not change the method merely to make a more attractive card claim.

## 28. Visuals are late-stage product assets

Cover/portfolio visuals come after method, rehearsal, client package, QA, economics and card copy are substantively ready.

Visuals must use real or safely anonymized validated product evidence and must never invent rows, metrics, counts or screenshots that look like real client results.

A visual cannot compensate for an unfinished product.

## 29. Owner-accepted freeze before moving the series cursor

When a mini-kwork is accepted, create/fix an explicit freeze state containing the accepted version of:

- product scope;
- method;
- client package;
- price/limits when frozen;
- Kwork card when frozen;
- known deferred publication/visual items;
- accepted hashes/commits/readback where relevant.

A frozen product is not casually edited while building the next product.

Reopen only for:

```text
PROVEN DEFECT
or
EXPLICIT NEW VERSION
```

Then move `SERIES_ROADMAP.md` cursor to the next mini-kwork.

## 30. Canonical series development formula

```text
SERIES PRODUCT DEFINITION
→ READ THIS DEVELOPMENT PROTOCOL
→ READ CROSS-KWORK LARGE-ARTIFACT PUBLICATION RULE
→ SELECT ONE MINI-KWORK
→ FREEZE PRODUCT PROMISE / BOUNDARIES
→ FRESH MARKET CHECK
→ CLIENT INPUT CONTRACT
→ EXTRACT CURRENT PROVEN KW-001 METHOD
→ EXTRACT RELEVANT FAILURES / CORRECTIONS
→ BUILD GENERAL RULES
→ BUILD PER-STEP RULES
→ BUILD AUTONOMOUS ROADMAP
→ DEFINE LOGICAL DELIVERABLE + QA
→ CROSS-CHECK LEVEL-1 METHOD
→ COMMIT + REMOTE READBACK

→ HAND LARGE-DATA EXECUTION TO WORK
→ WORK READS COMPLETE LEVEL-1 METHOD
→ WORK PROMPT INCLUDES SEMANTIC-BLOCK CHECKPOINT PERSISTENCE
→ WORK PROMPT FREEZES ARTIFACT PUBLICATION POLICY
→ OKNO_MSK MINI-KWORK-ONLY REHEARSAL
→ DURABLE CHECKPOINT AFTER EACH COMPLETED MATERIAL BLOCK
→ USE NATIVE GIT OR OWNER-RELAY PUBLICATION, WHICHEVER IS RELIABLE/EFFICIENT
→ REMOTE READBACK AFTER EACH MATERIAL PUBLICATION
→ CONTAMINATION AUDIT WHERE NEEDED
→ DATA / DECISION AUTHORITIES
→ INDEPENDENT QA + RECIPIENT REVIEW
→ WORKLOAD METRICS
→ METHOD-DEFECT PROPAGATION IF FOUND
→ REMOTE-VERIFIED PUBLICATION

→ OWNER REVIEW
→ FINAL CLIENT PACKAGE
→ PRICE / LIMITS
→ KWORK CARD
→ VISUALS
→ OWNER FREEZE
→ NEXT MINI-KWORK
```

## 31. Anti-confusion markers

These markers are mandatory mental/readback checks whenever a new mini-kwork starts:

```text
THIS FILE = HOW TO BUILD THE PRODUCT
MKxx/GENERAL_RULES = HOW TO RUN THAT PRODUCT ACROSS STEPS
MKxx/steps/*.md = HOW TO RUN A PARTICULAR STEP
OKNO_MSK = TEST DATA / EVIDENCE, NOT UNIVERSAL METHOD
KW-001 = SOURCE METHOD, NOT AUTOMATIC MINI-KWORK SCOPE
WORK = LARGE-DATA EXECUTOR, NOT PRODUCT ARCHITECT
OWNER RELAY = APPROVED FILE TRANSPORT, NOT ANALYTICAL DELEGATION
LARGE ARTIFACT MODEL BYTE TRANSPORT = FORBIDDEN BY DEFAULT
REMOTE READBACK = REQUIRED AFTER OWNER UPLOAD
MARKET SOURCES = COMMERCIAL EVIDENCE, NOT AUTOMATIC METHOD AUTHORITY
METHOD SOURCES = METHOD SUPPORT, NOT AUTOMATIC PRICE AUTHORITY
```

If these roles become ambiguous, stop productization at the current Level-1 phase and reconcile the authority roles before data execution.
