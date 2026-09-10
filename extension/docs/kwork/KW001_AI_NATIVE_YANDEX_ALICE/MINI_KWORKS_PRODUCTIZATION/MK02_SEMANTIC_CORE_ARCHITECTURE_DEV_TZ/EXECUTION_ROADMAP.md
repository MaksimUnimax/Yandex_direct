# MK02 — AUTONOMOUS EXECUTION ROADMAP

Status: **LEVEL-1 METHOD / DATA REHEARSAL NOT STARTED**

Product working identity:

**«Семантическое ядро + SEO-структура сайта + ТЗ на доработку»**

This roadmap is the standalone execution sequence for a real MK02 order. It does not require the executor to reconstruct the full KW-001 roadmap from memory. `STEP_RULES_INDEX.md` and `steps/*.md` contain the step-level contracts.

## 0. Global execution boundaries

```text
SEARCH ECOSYSTEM = YANDEX ONLY
SITE MODE = EXISTING PUBLIC WEBSITE
SEMANTIC COLLECTION = INCLUDED
COMPETITOR STEP5A = EXCLUDED FROM BASE
AI / ALICE / NEURO = EXCLUDED
GOOGLE = EXCLUDED
IMPLEMENTATION ITSELF = EXCLUDED
PRODUCTION SCHEDULE = NOT PROMISED WITHOUT REAL CALIBRATION
```

A new provider request is made only for a named information gap that can change an accepted decision. Useful acquisition is persisted/read back before another material acquisition interaction.

## 1. Pre-start gate

Before Step00, confirm base eligibility:

- public site exists and is readable;
- one primary Yandex region can be confirmed;
- client can define/confirm business directions/exclusions;
- client states known material structural/change constraints or `NONE KNOWN`;
- Yandex-only scope accepted;
- no password/secret dependency.

If not, do not silently downgrade evidence requirements.

---

## STEP 00 — Freeze order, business scope and known site-change constraints

Purpose: lock the sold task before data acquisition.

Required result:

```text
SITE
REGION
BUSINESS / CONVERSION JOB
INCLUDED DIRECTIONS
EXCLUSIONS
KNOWN PROTECTED URLS / FORMS / CALCULATORS / SECTIONS OR NONE KNOWN
OPTIONAL INPUT AVAILABILITY
UNRESOLVED CLIENT QUESTIONS
```

Do not let later demand evidence rewrite client scope automatically.

Gate: `steps/STEP_00_ORDER_SCOPE_FREEZE.md` PASS.

---

## STEP 01 — Build current site/business model

Purpose: understand what the current public site actually offers and what page vocabulary/roles exist.

Use a current timestamped discovery/profile. Do not claim whole-site completeness from one route.

Output: scoped business/page model + initial current URL evidence + freshness limitations.

Gate: `steps/STEP_01_CURRENT_SITE_BUSINESS_MODEL.md` PASS.

---

## STEP 02 — Plan bounded Yandex Wordstat acquisition

Purpose: turn frozen business directions into acquisition probes without pre-approving keywords/pages.

```text
SEED != FINAL KEYWORD
SITE TAXONOMY != FINAL SEMANTIC / ARCHITECTURE TAXONOMY
```

Output: probe manifest + parameters + stop/cost/persistence plan.

Gate: Step02 PASS.

---

## STEP 03 — Acquire and persist Yandex demand evidence

Purpose: collect complete governed Wordstat occurrence data and make it durable.

Required order:

```text
REQUEST
→ COMPLETE USEFUL RESPONSE
→ SAVE COMPLETE OCCURRENCE/PROVENANCE
→ READBACK / RECONCILE
→ ONLY THEN NEXT MATERIAL REQUEST
```

Output: durable occurrence/demand/provenance layer.

Gate: Step03 PASS.

---

## STEP 04 — Conservative first triage

Purpose: remove only obvious noise/out-of-scope families and identify real collection gaps.

Do not finalize relevance from family membership/frequency.

Output: triage states + preserved uncertainty + named Step05 gaps.

Gate: Step04 PASS.

---

## STEP 05 — Targeted second acquisition, only if justified

Trigger: a named unresolved coverage gap from Step04 can materially affect downstream decisions.

No automatic recursion. No competitor-derived Step5A work in base MK02.

Output: union-compatible additional evidence + explicit stop decision.

If not required, record `NOT_REQUIRED` with reason.

Gate: Step05 applicable state PASS.

---

## STEP 06 — Row-level semantic cleanup

Purpose: every governed unique phrase gets an explicit semantic/business state and reason.

Hard rules:

```text
NO DEFAULT KEEP
LOW FREQUENCY != IRRELEVANT
HIGH FREQUENCY != RELEVANT
ASSOCIATION != BUSINESS FIT
```

Output: current row-level semantic authority + uncertainty + exact accounting.

Gate: semantic QA PASS.

---

## STEP 07 — Freeze semantic universe / routes

Purpose: create one current deterministic pre-Search authority for downstream work.

Preserve active, Search-required, deferred and excluded states with complete demand/provenance joins.

Output: frozen semantic universe + route ledger.

Gate: Step07 PASS/readback.

---

## STEP 08 — Targeted ordinary Yandex Search for unresolved semantic boundaries

Run only when a named question can change semantic/task classification.

Persist exact query/region/time/surface/result evidence. Do not generalize one exact query to an untested family.

Output: bounded Search decisions + remaining unresolved cases.

If no Search needed, record `NOT_REQUIRED`.

Gate: Step08 applicable state PASS.

---

## STEP 09 — Task/intent-first clustering

Purpose: produce stable user-task units suitable for page ownership.

```text
WHOLE USER TASK FIRST
LEXICAL OVERLAP SECONDARY
NO TARGET CLUSTER COUNT
```

Output: cluster contracts + assignments + task/intent/business-fit + semantic QA.

Gate: Step09 PASS.

---

## STEP 10 — Current page ownership / complete phrase→page map

Purpose: determine which **current** page truthfully owns each accepted task and preserve this for every applicable active phrase.

Required distinctions:

```text
EXACT PHRASE OWNER
!= FAMILY OWNER
!= SUPPORTING PAGE
!= OBSERVED SEARCH-RELEVANT URL
```

`NO_SUITABLE_EXISTING_PAGE` is allowed and does not authorize CREATE.

Output: candidate ledger + ownership ledger + complete phrase→page map + unresolved handoff.

Gate: ownership accounting/coherence/current-page QA PASS.

---

## STEP 11 — Structural/content-routing action diagnosis

Purpose: decide whether actual site change is needed and which structural alternative is supported.

Required chain:

```text
USER TASK / DEMAND
+ CURRENT OWNER / CONTENT
+ BUSINESS GOAL EVIDENCE
+ SEARCH EVIDENCE WHEN MATERIAL
+ ALTERNATIVE COMPARISON
→ DIAGNOSIS
→ ACTION / NO-CHANGE / DEFER
```

Before CREATE, run current existence/content-reuse audit. Action may not prove itself.

Output: structural/action authority + no-change + unresolved + dependency relationships.

Gate: all M12 controls/global coherence PASS.

---

## STEP 12 — Competing-page safety diagnosis

Purpose: prevent false cannibalization and unsafe destructive action.

Base MK02 default mode:

```text
BASE_PUBLIC_EVIDENCE_MODE
```

Stronger first-party-history mode is used only when separately available/required by the claim.

Hard boundaries:

```text
RELATED PAGES != CANNIBALIZATION
CURRENT SERP OVERLAP != HISTORICAL COMPETITION
HISTORICAL COMPETITION != PROVEN HARM
```

Output: related-page/case verdicts + claim level + bounded action implications.

Gate: no historical/harm/destructive overclaim.

---

## STEP 13 — Reconcile target Search architecture with actual current topology

Purpose: independently verify current site pages/links so the target architecture is not based only on a closed upstream list.

Maintain:

```text
TARGET SEARCH ARCHITECTURE
CURRENT AS-IS TOPOLOGY
```

Independently discover current relevant pages when completeness is material. Preserve literal current internal-link evidence separately from recommended links.

Newly discovered material pages reopen affected decisions only.

Output: current URL universe, as-is link graph, target architecture, current-vs-target delta, final Search-only architecture freeze.

Gate: Step13 full topology/reconciliation PASS.

---

## STEP 14 — Build implementation specifications

Purpose: turn supported architecture/action authority into work an implementer can actually execute.

First canonicalize/de-duplicate real changes. Then distinguish:

```text
READY_IMPLEMENTATION_SPEC
PENDING_BUSINESS_DETAIL
PENDING_TECHNICAL_DETAIL
PENDING_PLACEMENT_OR_CONTEXT
RECHECK_ONLY
SEMANTIC_MAPPING_ONLY
NO_SITE_CHANGE
HOLD
```

READY requires applicable:

```text
PAGE / OBJECT
WHY
AS-IS
EVIDENCE MEANING
IMPLEMENTATION MODE
EXACT CHANGE
EXACT LOCATION / CONTEXT WHEN MATERIAL
TO-BE
DEPENDENCIES
PRESERVATION REQUIREMENTS
ACCEPTANCE CHECK
```

Do not invent owner/effort/capacity/timing. Analytical priority may be provided separately; numbering does not imply schedule.

Output: work-package/action authority + clarification/no-change/HOLD + analytical priority + acceptance criteria.

Gate: Step14 readiness QA PASS.

---

## STEP 15 — Materialize client package / final QA / readback

Purpose: turn current accepted authorities into recipient-ready views without new hidden research.

Logical package must let the client understand:

- semantic core/clusters;
- query/task→current page map;
- family owner/supporting pages where material;
- current-vs-target architecture;
- supported real site changes;
- READY implementation tasks;
- clarification/recheck/HOLD/no-site-change results;
- page relationships;
- why decisions were made;
- how to verify implementation;
- product limitations.

Two separate recipient jobs must be satisfied:

```text
ANALYTICAL EXPLANATION = WHAT DID THE RESEARCH SHOW?
IMPLEMENTATION REPORT = WHAT TO DO / WHY / WHERE / HOW / WHAT TO CLARIFY / HOW TO CHECK?
```

Physical XLSX/DOCX/PDF split is finalized after MK02 OKNO_MSK rehearsal. Do not predeclare an arbitrary page count/file structure as a quality metric.

Report materialization may not launch new project research merely to make a pending item look READY.

Gate: data + analytical + implementation + physical + recipient + persistence/readback QA PASS.

---

## 16. Correction propagation rule

Any material upstream correction after a later step has started requires:

```text
IDENTIFY IMPACT SET
→ INVALIDATE AFFECTED DOWNSTREAM PASS
→ REBUILD AFFECTED DERIVED FIELDS / ACTIONS / CLIENT VIEWS
→ INDEPENDENT QA
→ RESTORE PASS ONLY AFTER READBACK
```

No ID-only/local patch.

## 17. Provider/data-work rule for current productization stage

This Level-1 roadmap is built without processing OKNO_MSK data.

```text
METHOD BUILD = NOW
OKNO_MSK DATA REHEARSAL = PHASE 5 / WORK MODE
```

The Work execution prompt must use this roadmap as authority and must not redesign the method while processing data unless a real defect is found and recorded.

## 18. Autonomous Definition of Done for a future real MK02 order

```text
ORDER/SCOPE PASS
+ YANDEX DEMAND PERSISTED
+ SEMANTIC CORE QA PASS
+ CLUSTER QA PASS
+ PHRASE→PAGE OWNERSHIP COMPLETE
+ STRUCTURAL ACTION EVIDENCE PASS
+ COMPETING-PAGE CLAIMS BOUNDED
+ CURRENT SITE TOPOLOGY RECONCILED
+ TARGET SEARCH ARCHITECTURE FROZEN
+ IMPLEMENTATION SPECIFICATIONS READY WHERE EVIDENCE SUFFICIENT
+ PENDING / NO-CHANGE / HOLD EXPLICIT ELSEWHERE
+ CLIENT PACKAGE MATERIALIZED
+ RECIPIENT QA PASS
+ REMOTE READBACK PASS
= MK02 DELIVERY PASS
```
