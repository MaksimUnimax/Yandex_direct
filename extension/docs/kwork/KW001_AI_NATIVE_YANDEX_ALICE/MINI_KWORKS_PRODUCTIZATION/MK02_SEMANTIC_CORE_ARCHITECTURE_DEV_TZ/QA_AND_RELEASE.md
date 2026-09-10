# MK02 — QA AND RELEASE

Status: **ACTIVE / PHASE 7 PRODUCT-RECIPIENT QA PASS / PHASE 8 ECONOMICS NEXT**

MK02 must not pass on one generic green status. Semantic correctness, page ownership, architecture, implementation readiness, recipient usability and persistence are independent gates.

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

## G6 — Page-ownership accounting and role gate

Verify:

```text
CURRENT ACTIVE APPLICABLE PHRASES == FINAL OWNERSHIP ROWS
CURRENT ACCEPTED SEMANTIC ACTIVE KEYS == OWNERSHIP MAP KEYS
LEGACY DOWNSTREAM-ONLY ACTIVATIONS = 0
SILENT ACTIVE DROPS = 0
OWNER_EXISTING_WITH_BLANK_TARGET = 0
OWNER_EXISTING_WITHOUT_CURRENT_PAGE_EVIDENCE = 0
UNRESOLVED_WITH_FABRICATED_TARGET = 0
```

Client-visible mapping must distinguish exact phrase owner, family/structural-unit owner, supporting page and observed Search-relevant URL when materially different.

The current accepted semantic product authority, not an older downstream `ASSIGNED`/working flag, defines `CURRENT ACTIVE APPLICABLE PHRASES`.

## G7 — Page-ownership coherence gate

Adversarially reopen broad/weak/mixed units, object-vs-component, commercial-vs-information/service/DIY, plausible lexical-only URLs and medium/low-confidence assignments. Representative query cannot substitute for full-member review.

## G8 — Structural-action evidence gate

Every material action must have independent diagnosis/evidence. Verify:

- phrase count not used as CREATE proof;
- current-content reuse checked before CREATE;
- old inventory absence not used as current absence;
- owner-goal evidence source visible internally;
- no action proves itself;
- rejected/outside units do not strand salvageable in-scope phrases;
- real-site-change state = YES/NO/UNRESOLVED;
- material upstream corrections propagated atomically.

Known regression checks do not replace independent global-coherence review.

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

## G10 — Current-site topology / target-architecture gate

When architecture completeness is material:

- independent current site discovery performed;
- upstream known list does not prove its own completeness;
- current URL universe materialized;
- newly discovered relevant pages reconciled;
- current literal internal-link state separated from recommended links;
- target architecture separated from current topology;
- sitemap presence not used as HTML reachability proof;
- unsupported destructive action from new discovery=0;
- AI evidence used in Search-only freeze=0.

## G11 — Implementation-spec completeness gate

For every item claimed READY:

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

Hard failures:

- analytical route labelled READY;
- link READY without required placement/context;
- ambiguous “before X or Y” placement;
- analysis left to implementer;
- READY placeholder/TODO;
- filename/ID-only client evidence;
- generic cloned step blocks.

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

All promised logical client views from `DELIVERABLE_SPEC.md` must be materialized through the Phase-6 frozen physical package. Verify one current authority feeds all views and no stale historical owner/action appears in a polished file.

Cross-reconcile:

```text
SEMANTIC VIEW
OWNERSHIP VIEW
CURRENT ARCHITECTURE VIEW
TARGET ARCHITECTURE VIEW
ACTION VIEW
READY / CLARIFICATION / NO-CHANGE / HOLD VIEWS
NARRATIVE FINDINGS
IMPLEMENTATION REPORT
```

Contradiction between views = FAIL.

## G14 — Recipient language / report quality gate

For Russian client artifacts:

- ordinary headings/statuses/reasons/instructions are Russian;
- internal action IDs/filenames/QA IDs/Stage/Step/enums do not leak;
- final XLSX is scanned both through visible cells and raw package XML/table metadata;
- client-text normalization is not bypassed by a secondary generator path;
- document identity is result/purpose, not recipient profession;
- topic→page and page→page tables explain WHAT/WHY/HOW;
- analytical report answers “what did research show?”;
- implementation report is action-first and answers what/why/where/how/clarify/check;
- no generic defensive prohibition section;
- no provider/owner-failure/quarantine narration;
- no fixed page-count quality proxy;
- no empty TOC/filler/template symmetry.

This gate explicitly covers owner-identified Report №02 failures A–U.

## G15 — Physical / recipient / persistence gate

Phase 6 has frozen the base MK02 V1 client package as:

```text
1 XLSX
+ 1 ANALYTICAL PDF
+ 1 IMPLEMENTATION-TZ PDF
+ SHORT HANDOFF MESSAGE (NOT A FILE)
```

Phase 7 must therefore:

- open the final XLSX and verify its workbook structure/usability;
- render and inspect **both** final PDFs independently from the exact post-correction delivery bytes;
- parse/extract and client-language-scan both PDFs, but do not treat parse/hash success as a substitute for rendering;
- verify no clipping/overlap/broken glyphs/unreadable tables/orphan headings or broken page flow;
- verify the analytical PDF independently answers “what did the research show?”;
- verify the implementation-TZ PDF independently answers what/why/where/how/clarify/check;
- verify an uninvolved recipient can identify current vs target architecture, READY vs clarification/no-change and use the implementation tasks;
- verify the short handoff message names exactly the real three files and points to the correct starting order;
- verify the Yandex-only boundary in each client-facing file;
- verify no stale 7-READY state survives in any polished view;
- persist text/binary artifacts as tooling allows;
- verify exact remote identities/hashes/readback honestly;
- treat local-only completion as FAIL.

DOCX is not a mandatory base client file. If an internal DOCX is used as a PDF-generation intermediate, it must not create a second contradictory client authority.

## Report-stage no-new-research gate

This applies across G13–G15:

```text
REPORT MATERIALIZATION != NEW PROJECT RESEARCH
```

If report generation exposes missing implementation evidence, classify the item pending/clarification. Do not silently launch site recrawls, new Wordstat/Search or new object classification solely to make a report look more READY unless a separately authorized research/revalidation block is opened.

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

## Current Phase-7/8 boundary

```text
PHASE 5 OKNO_MSK REHEARSAL = PASS
PHASE 6 CLIENT PACKAGE OWNER REVIEW = PASS
PHASE 7 PRODUCT / RECIPIENT QA = PASS / 2026-09-10
PHYSICAL PACKAGE = XLSX + ANALYTICAL_PDF + IMPLEMENTATION_TZ_PDF + HANDOFF_MESSAGE
PHASE 7 PROVIDER CALLS = 0
PHASE 5 DATA AUTHORITIES MODIFIED IN PHASE 7 = 0
NEXT_ACTION = PHASE_8_MK02_PRICE_LIMITS_ECONOMICS
```

G13–G15 are PASS for the validated Phase-7 package. Phase 8 price/limits is the next gate; Phase 9 card and Phase 10 visuals remain pending.
