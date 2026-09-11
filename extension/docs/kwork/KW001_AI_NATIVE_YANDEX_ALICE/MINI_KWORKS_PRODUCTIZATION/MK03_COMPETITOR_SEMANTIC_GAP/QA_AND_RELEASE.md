# MK03 — QA AND RELEASE

Status: **PHASE 4 PASS CANDIDATE / MANDATORY RELEASE GATES**

## 1. QA principle

MK03 release requires four independent classes of correctness:

```text
ANALYTICAL CORRECTNESS
+ ACCOUNTING / DETERMINISTIC CORRECTNESS
+ PHYSICAL ARTIFACT CORRECTNESS
+ RECIPIENT USEFULNESS
```

A green file-open check or green schema test alone is not release acceptance.

## 2. G0 — Scope and input gate

PASS requires:
- public client site identified;
- target region frozen;
- Yandex-only V1 boundary preserved;
- material business ambiguity either resolved from current public evidence or explicitly held;
- no hidden dependency on client-supplied competitor names.

FAIL if analysis proceeds from an unfrozen region/scope or invents business truth.

## 3. G1 — Current-site freshness gate

Any conclusion that a direction is missing from the client must use current-enough public-site evidence for that claim.

Hard failures:

```text
OLD ABSENCE AS CURRENT ABSENCE
SEARCH ABSENCE AS SITE ABSENCE
HISTORICAL INVENTORY USED WITHOUT RECONCILIATION WHEN CURRENT COVERAGE MATTERS
```

## 4. G2 — Organic competitor evidence gate

Every material domain called a Yandex organic Search competitor must trace to current/preserved-current regional Yandex Search evidence for an in-scope query family.

Hard failures:
- client hint promoted directly to organic competitor;
- business rivalry treated as Search evidence;
- ads/marketplace familiarity substituted for organic evidence;
- competitor counts without query-family evidence.

## 5. G3 — Competitor-page evidence gate

Material competitor pages used for seed acquisition must be public, evidence-bearing and traceable to the discovery process.

Hard failure:

```text
COMPETITOR PAGE TOPIC AS PROOF OF EXACT QUERY RANKING
```

A page may support a topic/seed hypothesis without supporting a Search visibility claim.

## 6. G4 — Seed/provenance gate

Every material competitor-derived seed/candidate preserves source lineage.

PASS requires:
- source competitor/page/topic reconstructable;
- seed state distinguishable from accepted keyword state;
- duplicate semantic identity can merge while new provenance survives.

Hard failures:

```text
COMPETITOR-DERIVED SEED = AUTOMATIC ACCEPTED KEYWORD
NEW PROVENANCE = AUTOMATIC NEW KEYWORD ID
LINEAGE LOST DURING DEDUPLICATION
```

## 7. G5 — Wordstat funnel gate

Wordstat acquisition must pass through normalization, sanitation and business-fit routing before final use.

PASS requires explicit reconciliation of raw occurrences into deterministic outcomes.

Hard failures:
- raw Wordstat appended directly to final analytical set;
- duplicate occurrences counted as independent keyword identities;
- Wordstat demand treated as proof of client fit, intent, page ownership or structural action;
- provider call with no named decision gap.

## 8. G6 — Selective Search confirmation gate

`SERP_COVERAGE_MODE = SELECTIVE_DECISION_SERP` must remain visible in data semantics.

For every exact query→competitor visibility claim, PASS requires current direct Search evidence or explicitly reusable preserved current evidence for that exact query/region.

Hard failures:
- unprobed candidate called Search-confirmed;
- a small tested subset generalized into a full domain keyword universe;
- page topic or Wordstat occurrence substituted for exact ranking evidence;
- no distinction between tested and untested rows.

## 9. G7 — Gap classification gate

Every material candidate must end in one explicit state equivalent to:

```text
CONFIRMED_GAP
ALREADY_COVERED
REJECT_OFF_SCOPE
HOLD_EVIDENCE
```

PASS requires:
- reason/evidence for the state;
- current client coverage evidence or uncertainty;
- deterministic duplicate collapse documented where applicable;
- no silent drops.

Hard failure: totals do not reconcile from acquisition/candidate authority to final states.

## 10. G8 — Opportunity-boundary gate

Every opportunity must be supported by the final gap/coverage state and must remain inside MK03 scope.

Hard failures:

```text
CONFIRMED_GAP → AUTOMATIC CREATE PAGE
COMPETITOR PAGE EXISTS → CLIENT MUST COPY PAGE
BOUNDED GAP NOTE → FULL TARGET ARCHITECTURE CLAIM
MK03 RESULT → IMPLEMENTATION-READY TZ WITHOUT DOWNSTREAM PRODUCT WORK
```

Positive `ALREADY_COVERED` / KEEP findings remain valid client value and must not be hidden merely because no physical change follows.

## 11. G9 — Evidence-type separation gate

Canonical authorities and recipient views must distinguish at minimum:

```text
OBSERVED CURRENT SEARCH FACT
PUBLIC PAGE FACT
WORDSTAT DEMAND FACT
NORMALIZATION / ROUTING ASSIGNMENT
ANALYTICAL CONCLUSION
STRUCTURAL OPPORTUNITY RECOMMENDATION
BUSINESS FACT
UNKNOWN / HOLD
```

FAIL if an inference or recommendation is written as a provider observation.

## 12. G10 — No-silent-drop/accounting gate

All material acquired rows/candidates must be count/accounting-reconciled.

A valid conceptual reconciliation is:

```text
DISCOVERED / ACQUIRED MATERIAL
= PRESERVED UNIQUE IDENTITIES
+ DETERMINISTIC DUPLICATE COLLAPSES WITH LINEAGE
+ ALREADY COVERED
+ REJECTED / OFF-SCOPE
+ HOLD / EVIDENCE REQUIRED
```

Exact Level-2 schemas may vary, but unexplained disappearance is forbidden.

## 13. G11 — Cross-view consistency gate

Canonical data, XLSX and PDF must agree on all material decision fields:
- competitor identity/type;
- evidence-bearing page;
- candidate identity/provenance;
- Wordstat state;
- Search-tested state;
- client coverage state;
- final gap state;
- opportunity or HOLD reason.

FAIL if a summary/PDF silently upgrades or changes a canonical row decision.

## 14. G12 — XLSX physical QA gate

For the exact final workbook:
- inspect intended sheets and visible client cells;
- inspect headers, filters, freeze panes, widths and usability;
- validate formulas/references where present;
- inspect workbook XML/table metadata when needed;
- detect hidden critical information, accidental internal fields, broken tables, duplicated headers or unusable widths;
- rerun after any final workbook change.

No universal fixed sheet count, row count or competitor count may be used as a fake regression gate.

## 15. G13 — PDF physical QA gate

For the exact final PDF:
- parse/extract text sufficiently to detect omissions/truncation;
- render every exact final page;
- visually inspect every rendered page;
- reject clipping, overlap, unreadable tables, blank/missing pages, broken fonts and layout defects;
- rerender if final bytes change.

No universal fixed PDF page count is required.

## 16. G14 — Recipient task gate

Without repository knowledge, the final package must let the client answer arbitrary material questions such as:

1. Which Yandex organic competitor was observed and from which search family?
2. Which competitor page exposed a selected candidate direction?
3. Was an exact query→competitor relation actually Search-tested?
4. What did Wordstat support for that direction?
5. Is the direction already covered, a confirmed gap, off-scope or held?
6. What bounded opportunity follows?
7. What uncertainty remains and what evidence would resolve it?

Counts-only or presentation-only files fail this gate.

## 17. G15 — Client-language gate

Ordinary client-facing material must not require knowledge of:
- repository paths;
- Step/Stage numbers;
- internal QA codes;
- commit hashes;
- raw state-machine language.

Necessary evidence/provenance remains inspectable in client-readable terms.

## 18. G16 — Source/generator propagation gate

When an artifact defect is found:

```text
FIX CANONICAL SOURCE / GENERATOR / METHOD
→ REGENERATE
→ RERUN ANALYTICAL + PHYSICAL QA
```

Hand-patching only the final PDF/XLSX is not method closure.

## 19. G17 — Persistence and publication gate

Every material completed block follows:

```text
SAVE
→ LOCAL QA
→ COMMIT / APPROVED PUBLICATION TRANSPORT
→ REMOTE READBACK
```

Phase-5 Work execution must use semantic-block checkpointing and the cross-Kwork artifact transport authority.

## 20. Provider-call accounting

Release receipt must state at least:
- number/type of new Search calls;
- number/type of new Wordstat calls;
- which evidence was reused;
- any calls blocked/not made and why.

A provider call with no named decision gap is a QA defect.

## 21. Hard release failures

Any one of the following blocks release:

```text
BUSINESS RIVAL PRESENTED AS ORGANIC SEARCH COMPETITOR WITHOUT SEARCH EVIDENCE
PAGE TOPIC PRESENTED AS EXACT RANKING EVIDENCE
RAW WORDSTAT COPIED INTO FINAL ACCEPTED SET
UNPROBED QUERY PRESENTED AS SEARCH-CONFIRMED
NEW PROVENANCE DUPLICATED AS NEW KEYWORD ID
CONFIRMED GAP AUTO-CONVERTED TO CREATE PAGE
OLD CLIENT-SITE ABSENCE USED AS CURRENT FACT
SILENT DROPS / UNRECONCILED COUNTS
COUNTS-ONLY CLIENT PACKAGE
XLSX/PDF NOT PHYSICALLY INSPECTED
FINAL ARTIFACT CHANGED AFTER QA WITHOUT RECHECK
REMOTE READBACK MISSING
```

## 22. Release receipt

A final Phase-5/Phase-7 style receipt must record:
- Level-2 authority paths;
- generator/source paths where applicable;
- QA gate results;
- provider-call accounting;
- exact release artifact paths;
- SHA256 for client binaries where produced;
- Git commit(s);
- remote readback result;
- unresolved HOLD items;
- next allowed productization action.

PASS may be declared only when all applicable gates are green and unresolved uncertainty is honestly preserved rather than hidden.
