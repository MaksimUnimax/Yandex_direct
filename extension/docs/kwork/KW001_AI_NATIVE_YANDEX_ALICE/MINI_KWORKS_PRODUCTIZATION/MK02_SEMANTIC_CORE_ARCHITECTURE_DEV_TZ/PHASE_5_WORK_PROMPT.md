# MK02 — PHASE 5 WORK EXECUTION HANDOFF

Use the following as the execution contract for Work mode.

---

Ты продолжаешь активную работу по проекту Kwork / Yandex Marketing Bridge.

ЭТО НЕ НОВЫЙ ПРОЕКТ И НЕ НОВОЕ ИССЛЕДОВАНИЕ.

THIS IS AN EXECUTION TASK.

Твоя задача — выполнить **PHASE 5 — OKNO_MSK MK02-ONLY REHEARSAL** для второго мини-кворка:

**«Семантическое ядро + SEO-структура сайта + ТЗ на доработку»**

так, как если бы клиент OKNO_MSK купил **ТОЛЬКО MK02**, без полного KW-001, без MK03, без MK04 как отдельного продукта, без MK06 и без Google.

Не останавливайся на анализе.
Не пиши только план.
Не делай review-only report.
Нужно выполнить фактическую data projection/reconciliation, материализовать MK02-only authorities и candidate recipient views, прогнать QA, сохранить результаты в GitHub, делать commits по материальным блокам и выполнить remote readback.

======================================================================
0. REPOSITORY / BRANCH / CONCURRENCY
======================================================================

Repository:

MaksimUnimax/Yandex_direct

Branch:

roadmap/kwork-productization-2026-08-28

Перед любой записью:

1. Прочитай live remote branch HEAD.
2. Работай поверх актуального HEAD.
3. Не делай force push.
4. Если ветка сдвинулась параллельно — перечитай новый HEAD и накладывай только свои MK02-файлы поверх актуального дерева.
5. Не затирай KW002 или другую параллельную работу.
6. После каждого законченного материального блока: save → commit → push/ref update → remote readback.

Последний подтверждённый методический HEAD на момент handoff:

`4c8c66c41ef8d288089b6f43999eedb4a0dc05a9`

Но не считай его гарантированно текущим — сначала прочитай live HEAD.

======================================================================
1. WORKSPACES
======================================================================

Level-1 parent methodology:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE`

MK02 Level-1 product method:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/MINI_KWORKS_PRODUCTIZATION/MK02_SEMANTIC_CORE_ARCHITECTURE_DEV_TZ`

Source pilot job:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK`

MK01 standalone rehearsal reference, semantic foundation only:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/MINI_KWORKS_PRODUCTIZATION/MK01_SEMANTIC_CORE_CLUSTERING/tests/OKNO_MSK`

MK02 rehearsal workspace to create/use:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/MINI_KWORKS_PRODUCTIZATION/MK02_SEMANTIC_CORE_ARCHITECTURE_DEV_TZ/tests/OKNO_MSK`

======================================================================
2. READ THE MK02 METHOD COMPLETELY BEFORE DATA
======================================================================

Before touching OKNO_MSK datasets, fully read current remote versions of:

- `PRODUCT_ROADMAP.md`
- `MARKET_REALITY_2026-09-10.md`
- `PRODUCT_SCOPE.md`
- `CLIENT_INPUT_CONTRACT.md`
- `GENERAL_RULES.md`
- `ERRORS_AND_LESSONS.md`
- `STEP_RULES_INDEX.md`
- every file in `steps/`
- `EXECUTION_ROADMAP.md`
- `DELIVERABLE_SPEC.md`
- `QA_AND_RELEASE.md`
- `METHOD_CONSISTENCY_AUDIT_2026-09-10.md`
- `METHOD_REMOTE_READBACK_2026-09-10.md`

Also read the exact parent KW-001 authorities referenced by MK02, especially current versions of:

- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`
- `STEP_11_PAGE_OWNERSHIP_METHOD.md`
- `STEP_12_STRUCTURAL_ACTION_METHOD.md` + named companion gates
- `STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`
- `STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE_METHOD.md` + named discovery/reliability/sync addenda
- `STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md`
- `STEP_18_EXECUTION_TICKET_COMPLETENESS_GATE.md`
- `STEP_19_CLIENT_DELIVERABLE_PACKAGING_METHOD.md`
- `STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_GATE.md` and applicable supplemental gates

The MK02 Level-1 method is the execution authority. Do not redesign it merely because another arrangement seems convenient.

If the rehearsal exposes a real method defect, document the defect/root cause, fix the relevant Level-1 authority, identify the full impact set and rerun regression before PASS.

======================================================================
3. ABSOLUTE PRODUCT BOUNDARY
======================================================================

MK02 base sells:

```text
YANDEX DEMAND
→ CLEAN SEMANTIC CORE / TASK CLUSTERS
→ CURRENT PAGE OWNERSHIP / PHRASE→PAGE MAP
→ STRUCTURAL ACTION DIAGNOSIS
→ COMPETING-PAGE SAFETY WHERE MATERIAL
→ TARGET SEARCH ARCHITECTURE RECONCILED WITH CURRENT SITE
→ EVIDENCE-SUPPORTED IMPLEMENTATION SPECIFICATIONS
```

MK02 base does NOT include:

- Google Ads / Google Keyword Planner;
- Google Search / Google Search Console / Google SEO;
- AI / Alice / Yandex Neuro / GenSearch / AEO;
- competitor-derived Step5A semantic expansion;
- a standalone full historical harmful-cannibalization audit as MK04;
- website coding/implementation itself;
- copywriting full final page texts;
- full technical SEO audit unrelated to the structural findings;
- fabricated production schedule;
- guaranteed rankings/traffic/leads/revenue.

Do not leak full KW-001 or another mini-kwork into MK02 output.

======================================================================
4. PROVIDER / EXTERNAL-CALL BOUNDARY
======================================================================

**DEFAULT: NEW PROVIDER CALLS = 0.**

Do not call/re-run:

- Wordstat;
- ordinary Yandex Search;
- Webmaster;
- Metrika;
- Direct;
- Alice / GenSearch / Neuro;
- Google;
- external SEO provider APIs.

Use preserved OKNO_MSK evidence.

This is a rehearsal of the already researched pilot, not a fresh client run.

If a current MK02 method requirement cannot be satisfied from preserved evidence, do not invent it and do not silently make a new provider call. Record the exact evidence gap and the affected claim/readiness state.

======================================================================
5. CRITICAL MK02-BASE SEMANTIC SOURCE RULE
======================================================================

MK02 base excludes competitor Step5A.

The accepted MK01-only semantic rehearsal established the native pre-Step5A universe:

```text
SOURCE UNIQUE PHRASES = 2840
WORKING CORE = 2185
REVIEW / UNCERTAIN = 187
EXCLUDED = 468
TOTAL GROUPS = 59
WORKING GROUPS = 54
OUTSIDE GROUPS = 5
```

Pre-Step5A semantic authority previously proved for MK01:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv`

Known later integrated universe:

```text
2840 + 16 Step5A competitor additions = 2856
```

For MK02 base:

```text
STEP5A COMPETITOR ADDITIONS IN SEMANTIC INPUT = 0
```

Do not simply use the 2856 integrated core as MK02 base semantic authority.

However, later downstream full-KW001 artifacts may contain useful independent current-page/Search/topology evidence collected after Step5A. Such evidence may be reused only when its factual meaning is independent of the competitor-derived additions and it legitimately applies to the 2840-native scope.

======================================================================
6. STEP5A CAUSAL CONTAMINATION AUDIT — MANDATORY
======================================================================

Removing 16 rows is not enough by itself.

Later ownership/structural/architecture/action decisions may have been created or modified because Step5A added new phrases/topics.

Before treating downstream full-KW001 results as MK02 base truth, build:

`STEP5A_DOWNSTREAM_CONTAMINATION_AUDIT.md`

For every reused downstream authority/class determine:

1. Was the decision/action already supported by native 2840 evidence?
2. Did Step5A introduce the only evidence for that task/unit/action?
3. Did Step5A change a cluster/unit boundary, owner, create/split/merge action, internal-link relation, competing-page case or implementation task?
4. Is later evidence independent and reusable for native phrases even though collected after Step5A?
5. What must be excluded/rederived for a true MK02-base result?

Required rule:

```text
LATE ARTIFACT DATE != STEP5A CONTAMINATION
BUT
STEP5A-CAUSED DECISION != MK02 BASE DECISION
```

If an action depends materially on Step5A competitor additions, it cannot remain in base MK02 unless the same action is independently re-proved from allowed native evidence.

======================================================================
7. SOURCE AUTHORITY AUDIT
======================================================================

Create:

`SOURCE_AUTHORITY_AUDIT.md`

Record the exact preserved sources used for:

- semantic universe;
- row-level semantic decisions;
- clustering;
- ordinary Search evidence;
- page ownership;
- current page reads;
- structural actions;
- competing-page evidence;
- current-site discovery/topology;
- internal-link state;
- implementation readiness;
- client action authority.

For every source state whether it is:

```text
PRIMARY AUTHORITY
CURRENT ACCEPTED OVERLAY
REUSABLE INDEPENDENT EVIDENCE
CROSS-CHECK ONLY
SUPERSEDED / FORBIDDEN
STEP5A-CONTAMINATED FOR MK02 BASE
```

Do not choose authority by filename/date alone. Check content, precedence and later corrections.

======================================================================
8. MOCK CLIENT ORDER — MK02 ONLY
======================================================================

Create:

`MOCK_CLIENT_ORDER.md`

Project the real OKNO_MSK business/site context into `CLIENT_INPUT_CONTRACT.md` as if the client bought only MK02.

Record:

- existing public site;
- primary region;
- business/conversion purpose;
- included directions;
- exclusions;
- known structural constraints from preserved client/business evidence only;
- optional Webmaster/Metrika/Direct state;
- Yandex-only boundary;
- what MK02 is expected to deliver;
- what is not ordered.

Do not invent client-protected pages/constraints if preserved evidence does not establish them. Use `NONE KNOWN FROM PRESERVED INPUT` / explicit unknown where appropriate.

======================================================================
9. EXECUTE LOCAL MK02 STEPS 00–15 FROM PRESERVED EVIDENCE
======================================================================

Create and maintain:

`REHEARSAL_EXECUTION_LOG.md`

For every MK02 step 00–15 record:

- input;
- exact source authority/evidence;
- operation performed;
- output artifact;
- row/entity accounting;
- uncertainty/limitation;
- QA state.

Do not write only “already completed in KW-001”. Show which preserved artifact proves/reconstructs the MK02-only result.

======================================================================
10. STEPS 00–09 — SEMANTIC FOUNDATION
======================================================================

Use the accepted 2840 native semantic universe and preserved evidence to reproduce/confirm the semantic foundation without Step5A.

You may reuse the accepted MK01 rehearsal as a consistency reference, but the MK02 execution log must still prove its own inputs and joins.

Required native invariants unless a real method defect disproves them:

```text
UNIQUE PHRASES = 2840
WORKING CORE = 2185
REVIEW / UNCERTAIN = 187
EXCLUDED = 468
TOTAL GROUPS = 59
WORKING GROUPS = 54
OUTSIDE GROUPS = 5
STEP5A SEMANTIC CONTAMINATION = 0
```

Do not modify accepted MK01 data merely to make downstream MK02 easier.

======================================================================
11. STEP 10 — PAGE OWNERSHIP / COMPLETE PHRASE→PAGE MAP
======================================================================

Build a true MK02-base ownership authority from allowed evidence.

Required distinctions:

```text
EXACT PHRASE OWNER
FAMILY / STRUCTURAL-UNIT OWNER
SUPPORTING PAGE(S)
OBSERVED SEARCH-RELEVANT URL when directly evidenced
```

Do not compress these into one ambiguous URL.

Required states include equivalents:

```text
OWNER_EXISTING
NO_SUITABLE_EXISTING_PAGE
OWNER_UNRESOLVED_EVIDENCE_REQUIRED
OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP
```

Materialize one ownership row for every applicable active phrase.

Expected dataset classes may include:

- task/unit candidate page ledger;
- unit ownership ledger;
- complete phrase→page map;
- unresolved/no-page handoff;
- owner/supporting-page relation ledger.

Do not fabricate targets for unresolved rows.

======================================================================
12. STEP 11 — STRUCTURAL / CONTENT-ROUTING ACTIONS
======================================================================

From accepted MK02-base ownership and current evidence, derive supported structural actions.

For each material task/unit distinguish:

```text
STRUCTURAL GAP
CONTENT ENHANCEMENT GAP
REAL SITE CHANGE REQUIRED = YES | NO | UNRESOLVED
ACTION / NO-CHANGE / DEFER
```

Before CREATE:

- verify current page existence/current content reuse from preserved current-site evidence;
- do not treat old inventory absence as current absence;
- compare alternatives;
- preserve owner-goal evidence source;
- salvage in-scope member phrases from rejected/outside units.

Action cannot be its own evidence.

No unsupported CREATE/SPLIT/MERGE/destructive action.

======================================================================
13. STEP 12 — COMPETING-PAGE SAFETY
======================================================================

Default rehearsal/product mode:

`BASE_PUBLIC_EVIDENCE_MODE`

Use preserved first-party history only if it already exists and can legitimately support the case. Do not acquire new private history.

Keep separate:

```text
NORMAL DISTINCT TASKS
NORMAL PARENT/CHILD
NORMAL PRIMARY/SUPPORTING
CURRENT OWNERSHIP/MULTI-URL SIGNAL
HISTORICAL COMPETITION when actually supported
HARMFUL IMPACT only when actually supported
EVIDENCE INSUFFICIENT
```

Hard rules:

```text
RELATED PAGES != CANNIBALIZATION
CURRENT SERP OVERLAP != HISTORICAL COMPETITION
HISTORICAL COMPETITION != PROVEN HARM
```

Any Step11 destructive action requiring unavailable stronger evidence must be downgraded/deferred.

======================================================================
14. STEP 13 — CURRENT-vs-TARGET SEARCH ARCHITECTURE
======================================================================

Reconstruct from preserved evidence:

A. target Search architecture;
B. current as-is public site topology.

Do not let the upstream known URL list prove its own completeness.

For rehearsal, use preserved independent site-discovery/topology evidence from the full pilot when available; record its snapshot date/freshness limitation rather than making fresh site calls.

Preserve separately:

- current discovered relevant URL universe;
- current page/fetch states;
- literal current internal links;
- recommended/planned relations;
- newly discovered material pages from preserved evidence;
- upstream-vs-current reconciliation;
- current-vs-target delta.

```text
SOURCE LIVE + TARGET LIVE + SEMANTIC FIT != LINK IMPLEMENTED
```

No AI evidence in target Search architecture.

======================================================================
15. STEP 14 — IMPLEMENTATION SPECIFICATIONS
======================================================================

Build canonical work packages only after architecture is reconciled.

Required final states include equivalents:

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

Every READY item must have, where applicable:

```text
PAGE / OBJECT
WHY CHANGE IS NEEDED
AS-IS CURRENT STATE
EVIDENCE MEANING
EVIDENCE LOCATOR
IMPLEMENTATION MODE
EXACT CHANGE
EXACT LOCATION / CONTEXT
TO-BE STATE
DEPENDENCIES
PRESERVATION / DO-NOT-BREAK REQUIREMENT
ACCEPTANCE CHECK
```

Implementer must not be left to perform research/classification that belongs to MK02.

Forbidden READY examples:

- “place before X or Y”;
- “choose appropriate category”;
- “decide which items belong to filter”;
- generic cloned step list;
- placeholder/TODO/date;
- filename-only evidence;
- semantic mapping row presented as website change.

Keep implementation specification separate from production scheduling.

Do not invent owner, effort, capacity, timeline, business priority or expected uplift.

======================================================================
16. REPORT №02 OWNER FAILURE CLASSES A–U — MANDATORY REGRESSION
======================================================================

Before client candidate output, read the current MK02 `ERRORS_AND_LESSONS.md` and parent canonical Report №02 gate.

Explicitly test all owner failure classes A–U, including:

- internal traceability leakage;
- cloned generic implementation steps;
- ambiguous placement labelled ready;
- analysis left to implementer;
- READY placeholders;
- numbering mistaken for schedule;
- duplicate visible page/link pairs;
- missing material methodology source;
- temporal fact transferred to wrong object;
- report materialization becoming new research;
- internal process narration;
- negative pseudo-actions;
- obvious UI/browser filler;
- duplicated instructions;
- empty TOC/furniture;
- orphan field headings;
- profession-branded document identity;
- unexplained topic→page tables;
- unexplained page-pair tables;
- standalone defensive preservation section;
- implementation report dominated by research framing.

Failure count must be reported, not assumed zero.

======================================================================
17. STEP 15 — MATERIALIZE LOGICAL CLIENT VIEWS
======================================================================

Use `DELIVERABLE_SPEC.md` as the logical delivery contract.

Do not simply copy the full KW-001 client reports.

Materialize client-facing candidate views sufficient to test Phase 5/prepare Phase 6 for:

1. scope/how to use;
2. semantic core;
3. task/cluster map;
4. phrase/task→page ownership map;
5. exact owner/family owner/supporting distinctions;
6. current architecture/topology;
7. target Search architecture;
8. current→target delta/action map;
9. READY implementation specifications;
10. clarifications/checks;
11. mapping/no-change/HOLD items;
12. page-to-page relationships;
13. analytical explanation — what did research show?;
14. implementation explanation — what to do/why/where/how/clarify/check?;
15. acceptance/measurement interface where evidence supports it.

**Do not freeze a final commercial file split or arbitrary page count simply because a template is convenient.**

Phase 5 should determine and record the most usable physical package candidate for Phase 6 based on actual data volume and recipient task.

======================================================================
18. CLIENT REPORT / ANALYTICAL VALUE RULE
======================================================================

MK02 inherits the corrected MK01 rule:

```text
CLIENT ANALYTICAL REPORT != EXECUTION PROTOCOL
CORRECT COUNTS + CLEAN LAYOUT != RECIPIENT VALUE
```

The analytical layer must explain material findings about:

- demand/task structure;
- page ownership/coverage;
- current-vs-target architecture;
- important KEEP/no-change results;
- material unresolved boundaries;
- why major actions exist.

The implementation layer must be action-first.

Do not make either layer a chronology of provider calls/stages/QA.

======================================================================
19. QA — RUN G0–G15
======================================================================

Fully execute `QA_AND_RELEASE.md`.

Create:

`QA_REPORT.md`

with one PASS/FAIL line and evidence for every gate G0–G15.

Where possible, add independent machine validation for:

- row/set accounting;
- ownership coverage;
- owner-role distinctions;
- unresolved target blank-state invariants;
- structural-action evidence fields;
- Step5A contamination;
- current-vs-target URL/edge reconciliation;
- READY ticket required fields;
- duplicate visible action/link pairs;
- client-visible internal-token leakage;
- placeholders;
- cross-view contradictions.

Do not let the generator validate only its own output assumptions. Independent validator must be capable of failing.

If a gate FAILS, fix root cause and rerun affected gates before Phase 5 PASS.

======================================================================
20. RECIPIENT REVIEW
======================================================================

Create:

`RECIPIENT_REVIEW.md`

An uninvolved recipient must be able to explain from candidate client views:

- what was researched;
- which demand/groups are relevant;
- what page owns each material topic;
- difference between exact owner/family owner/supporting page;
- current site vs target architecture;
- what actually changes on site;
- what is READY now;
- what needs a concrete clarification/check;
- what is mapping/no-change/HOLD;
- how to verify implemented changes;
- what MK02 does not include.

Recipient review is separate from machine QA.

======================================================================
21. REHEARSAL METRICS FOR FUTURE PHASE 8
======================================================================

Create:

`REHEARSAL_METRICS.md`

Measure actual work volume, including at minimum:

- semantic source/working/review/excluded rows;
- working clusters;
- active phrase→page mapping rows;
- ownership units/tasks;
- current pages reviewed;
- current URLs/topology nodes/edges processed from preserved evidence;
- ownership candidate comparisons;
- structural action count by class;
- CREATE/SPLIT/MERGE/KEEP/NO_CHANGE/DEFER counts;
- competing-page cases;
- Search evidence reused;
- private-history evidence reused or unavailable;
- target architecture units/pages/relations;
- current-vs-target deltas;
- implementation work packages;
- READY / business-detail / technical-detail / placement-detail / recheck / mapping-only / no-change / HOLD counts;
- action-specific implementation detail workload;
- candidate client view/sheet/report sizes;
- manual analytical review bottlenecks;
- which real new-client provider calls would normally be needed;
- provider calls during rehearsal = 0.

Do NOT assign final price or commercial limits in Phase 5.

======================================================================
22. METHOD-DEFECT HANDLING
======================================================================

If rehearsal finds a real MK02 Level-1 defect:

1. name the failure class;
2. explain root cause/false assumption;
3. update `ERRORS_AND_LESSONS.md`;
4. update `GENERAL_RULES.md` and/or affected `steps/*.md`;
5. update `DELIVERABLE_SPEC.md` / `QA_AND_RELEASE.md` if needed;
6. identify the full Level-2 impact set;
7. rebuild affected outputs;
8. rerun regression;
9. commit/read back.

Do not make silent ad hoc exceptions for OKNO_MSK.

======================================================================
23. REQUIRED PHASE-5 REHEARSAL ARTIFACTS
======================================================================

At minimum create in MK02 `tests/OKNO_MSK/`:

```text
MOCK_CLIENT_ORDER.md
SOURCE_AUTHORITY_AUDIT.md
STEP5A_DOWNSTREAM_CONTAMINATION_AUDIT.md
REHEARSAL_EXECUTION_LOG.md
TEST_RESULT.md
QA_REPORT.md
RECIPIENT_REVIEW.md
REHEARSAL_METRICS.md
REMOTE_READBACK_RECEIPT.md
```

Plus structured data authorities as required for:

```text
SEMANTIC FOUNDATION / JOIN MANIFEST
PAGE OWNERSHIP
PHRASE→PAGE MAP
STRUCTURAL ACTIONS
COMPETING-PAGE CASES
CURRENT SITE TOPOLOGY
TARGET SEARCH ARCHITECTURE
CURRENT-vs-TARGET DELTA
IMPLEMENTATION WORK PACKAGES
CLARIFICATIONS / NO-CHANGE / HOLD
CLIENT CANDIDATE VIEWS
```

Use TSV/CSV/JSON/XLSX/DOCX/PDF only where the current data/use-case justifies them.

======================================================================
24. COMMIT BOUNDARIES
======================================================================

Do not accumulate all Phase 5 progress in memory/local workspace.

Recommended material commit boundaries:

A. `docs(mk02): establish OKNO_MSK source and Step5A contamination authority`

After:
- mock order;
- source-authority audit;
- Step5A downstream contamination audit.

B. `data(mk02): materialize OKNO_MSK ownership and architecture rehearsal`

After:
- steps 00–13 data authorities;
- phrase→page map;
- structural actions;
- competing-page cases;
- current/target architecture.

C. `data(mk02): materialize OKNO_MSK implementation work packages`

After:
- Step14 work packages;
- READY/pending/no-change/HOLD reconciliation;
- implementation acceptance.

D. `qa(mk02): validate OKNO_MSK MK02-only rehearsal`

After:
- G0–G15;
- independent validator;
- recipient review;
- rehearsal metrics;
- any Level-1 method corrections.

E. `docs(mk02): finalize phase 5 rehearsal readback`

After:
- roadmap state update;
- final remote readback receipt.

Commit wording may adapt to actual content. Do not create empty commits.

======================================================================
25. PHASE 5 STOP BOUNDARY
======================================================================

Do not continue into final product pricing/card/visuals.

Phase 5 ends when the data rehearsal, candidate client views, QA and metrics are complete.

Do NOT mark these as complete yet:

- Phase 6 final client packaging/product standard;
- Phase 8 final price/limits;
- Phase 9 Kwork card;
- Phase 10 visuals.

Those happen after owner review of the MK02 rehearsal.

======================================================================
26. FINAL RESPONSE FORMAT
======================================================================

Return a factual execution report containing:

- starting live remote HEAD;
- final live remote HEAD;
- commits made;
- exact 2840-native semantic authority used;
- Step5A contamination audit result;
- semantic counts;
- page-ownership row count and state counts;
- exact owner/family owner/supporting-page reconciliation result;
- current pages/topology evidence count;
- structural action counts by class;
- competing-page case counts and evidence modes;
- target architecture counts;
- current-vs-target delta counts;
- implementation work-package counts by READY/pending/mapping/no-change/HOLD state;
- provider calls during rehearsal;
- G0–G15 result;
- independent QA counts;
- recipient review result;
- method defects found/corrected;
- candidate physical client package recommendation for Phase 6, without falsely freezing it;
- rehearsal metrics for Phase 8;
- final remote readback result;
- exact NEXT_ACTION.

Do not return only a plan. Return the completed Phase 5 result.
