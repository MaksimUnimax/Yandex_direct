# KW-001 — STEP 12 STRUCTURAL ACTION METHOD

Updated: 2026-09-03  
Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-AUTHORIZED**  
Scope: decide what an existing site should keep as structural owner, strengthen, expand, route, split, merge, create, or deliberately not create after phrase-level page responsibility has been established.  
Boundary: Step12 makes structural/content-routing recommendations. Historical competition/harm diagnosis belongs to Step13; final Search architecture freeze belongs to Step14.

Companion authorities:

- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`
- `STEP_12_EVIDENCE_INDEPENDENCE_AND_CURRENT_CONTENT_VALIDATION.md`
- `STEP_12_GLOBAL_COHERENCE_REVALIDATION_GATE.md`
- `STEP_12_THIRD_AUDIT_EXECUTION_ORDER_CLARIFICATION.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`
- `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`

Concrete client/test domains, URLs, phrases, products, counts, defect IDs and correction results belong in Level-2 job evidence.

---

## 1. Step purpose

Step12 converts the accepted semantic/page-responsibility evidence into a practical answer:

> What should change in the site structure/content relationships, what should remain as-is structurally, what should be deferred, and why?

A label such as `KEEP`, `EXPAND`, `ROUTE` or `CREATE` is not enough. Every material action must be caused by evidence.

Canonical chain:

```text
EXACT PHRASES / USER NEEDS
→ COHERENT TERMINAL USER TASK
→ CURRENT BUSINESS TRUTH + OWNER GOAL
→ CURRENT SITE / CURRENT CONTENT
→ DEMAND + SEARCH EVIDENCE WHEN MATERIAL
→ COMPARE STRUCTURAL ALTERNATIVES
→ ACTION
→ IMPLEMENTATION RELATIONSHIPS
→ INDEPENDENT QA
```

---

## 2. External method grounding

### Official Yandex

- user need / targeting: https://yandex.ru/support/webmaster/ru/recommendations/targeting
- site structure: https://yandex.ru/support/webmaster/ru/recommendations/site-structure
- presentation / logical splitting: https://yandex.ru/support/webmaster/ru/recommendations/presentation
- low-value/low-demand pages: https://yandex.ru/support/webmaster/ru/site-indexing/low-demand
- useful content: https://yandex.ru/support/webmaster/ru/threat/useless-content
- duplicates: https://yandex.ru/support/webmaster/ru/robot-workings/double

These support user-task fit, logical page structure, useful distinct content and avoiding unnecessary duplicate/thin pages.

### Industry corroboration

- Semrush Keyword Mapping: https://www.semrush.com/blog/keyword-mapping/
- Semrush Content Gap Analysis: https://www.semrush.com/blog/content-gap-analysis/
- Semrush Content Audit: https://www.semrush.com/blog/content-audit/
- Semrush Content Strategy: https://www.semrush.com/blog/content-marketing-strategy-guide/
- Ahrefs Keyword Mapping: https://ahrefs.com/blog/keyword-mapping/
- Ahrefs Keyword Clustering: https://ahrefs.com/blog/keyword-clustering/
- Ahrefs Keyword Strategy: https://ahrefs.com/blog/keyword-strategy/
- Ahrefs Internal Links: https://ahrefs.com/blog/internal-links-for-seo/
- Rush Analytics structure/clustering/relevant URLs: https://www.rush-analytics.ru/faq/

These support current-page reuse, intent/task grouping, demand/business potential, Search-result evidence when boundary is disputed, and contextual internal linking.

External sources do not prescribe the exact KW-001 action labels or a universal page-count threshold.

---

## 3. Permanent failure history — failure, root cause, correction

Do not reduce these to a checklist. The causal lesson is what prevents recurrence.

### M12-01 — lexical phrase overrides replaced explicit structural units

**Failure:** individual phrases were routed by matching tokens/substrings instead of an auditable user-task unit.

**Root cause:**

```text
STRONG LEXICAL CLUE
WAS TREATED AS
FINAL TASK/PAGE AUTHORITY
```

**Control:** group materially different phrases into explicit structural subunits; materialize member phrases, user task, candidate page and evidence before routing.

---

### M12-02 — seeing every phrase was mistaken for proving unit coherence

**Failure:** mixed user tasks survived even though all member phrases were visible to the analyst.

**Root cause:**

```text
PHRASE-LEVEL VISIBILITY
WAS TREATED AS
PHRASE-LEVEL FALSIFICATION
```

**Control:** explicitly test whether every member shares the same object, terminal result, intent, lifecycle stage and expected page role. Split or defer incompatible members before choosing a page action.

---

### M12-03 — phrase count was treated as demand and new-page justification

**Failure:** a large vocabulary cluster could receive strong CREATE logic without a dedicated demand/Search evidence matrix.

**Root cause:**

```text
NUMBER OF VARIANTS
WAS USED AS A PROXY FOR
REAL SEARCH DEMAND / STANDALONE PAGE VALUE
```

**Control:** phrase count is coverage only. Use real demand evidence and Search boundary evidence when it can change the standalone-page decision.

---

### M12-04 — confidence defaulted high instead of being earned

**Failure:** a default confidence value could survive unless manually downgraded.

**Root cause:**

```text
NO ERROR TRIGGERED
WAS TREATED AS
HIGH EVIDENCE STRENGTH
```

**Control:** derive confidence from visible evidence dimensions and downgrade reasons. No default HIGH.

---

### M12-05 — QA certified desired state rather than underlying evidence

**Failure:** hard-coded booleans/counts or action-consistency checks produced a clean QA result without recomputing the real-world claim.

**Root cause:**

```text
SCHEMA / INVARIANT CONSISTENCY
WAS TREATED AS
INDEPENDENT EVIDENCE VALIDATION
```

**Control:** every QA fact must be computed from data, verified from provenance/receipts or supported by an explicit review ledger. A verifier must be capable of rejecting the generated action.

---

### M12-06 — downstream competing-page candidates were manually curated

**Failure:** a hand-selected list could miss less obvious adjacent/overlapping page pairs.

**Root cause:**

```text
ANALYST MEMORY / OBVIOUS EXAMPLES
WERE TREATED AS
COMPLETE ROUTING-GRAPH UNIVERSE
```

**Control:** derive Step13 candidate pairs from the complete final current routing graph.

---

### M12-07 — proposed page URL was mistaken for implementation-ready architecture

**Failure:** a CREATE/SPLIT recommendation could have a slug but no clear parent, inbound path, support links or navigation role.

**Root cause:**

```text
PAGE IDENTITY
WAS TREATED AS
SITE-ARCHITECTURE PLACEMENT
```

**Control:** every accepted new/split page needs hierarchy and link relationships.

---

### M12-08 — NO_STANDALONE_PAGE was treated as end of analysis

**Failure:** useful subtasks could remain without a destination after rejecting a standalone page.

**Root cause:**

```text
"DO NOT CREATE THIS URL"
WAS TREATED AS
"THIS USER NEED IS RESOLVED"
```

**Control:** route useful subtasks to current pages/sections, create explicit later-evaluation units, or defer with a named reason.

---

### M12-09 — rejected/outside unit state stranded salvageable in-scope phrases

**Failure:** a correct cluster-level rejection was applied to every member even when some phrases represented valid in-scope tasks elsewhere.

**Root cause:**

```text
UNIT-LEVEL VERDICT
WAS TREATED AS
MEMBER-LEVEL VERDICT WITHOUT SALVAGE REVIEW
```

**Control:** every rejected/outside/no-page family receives phrase/subunit salvage and contradiction review.

---

### M12-10 — provisional downstream dependency was hidden by final-looking action confidence

**Failure:** a structural action remained presented as final while a named Step13 boundary check could still change it.

**Root cause:**

```text
ROADMAP BOUNDARY WAS DOCUMENTED
BUT DID NOT MECHANICALLY CHANGE
ACTION MATURITY / CLAIM WORDING
```

**Control:** explicit status such as `FINAL_WITHIN_STEP12_EVIDENCE`, `PROVISIONAL_PENDING_DOWNSTREAM_CHECK`, or `DEFERRED_PENDING_MISSING_EVIDENCE`.

---

### M12-11 — upstream historical state was treated as stronger than later contradictory evidence

**Failure:** an older OUTSIDE/no-page/absence decision could survive despite newer verified current-site evidence.

**Root cause:**

```text
PROVENANCE / PREVIOUS ACCEPTANCE
WAS MISTAKEN FOR
IMMUTABLE CORRECTNESS
```

**Control:** preserve the old state historically but create an explicit correction overlay when newer material evidence contradicts it.

---

### M12-12 — old inventory absence was treated as current site absence

**Failure:** CREATE could survive because no owner appeared in an upstream inventory, even though a current equivalent page existed.

**Root cause:**

```text
OLD NEGATIVE EVIDENCE
WAS TREATED AS
CURRENT NEGATIVE EXISTENCE PROOF
```

**Control:** every surviving CREATE passes a fresh current-site existence/content-reuse audit immediately before acceptance. One false CREATE triggers re-audit of all CREATE candidates in the same run.

---

### M12-13 — business truth/expertise was mistaken for owner strategic goal

**Failure:** a high-demand topic could be recommended because the business can truthfully discuss it even when the proposed content format may work against the owner's commercial/user outcome.

**Root cause:**

```text
CAN TRUTHFULLY TALK ABOUT TOPIC
WAS TREATED AS
SHOULD ATTRACT / ENABLE THIS USER TASK IN THIS FORMAT
```

**Control:** record owner goal, desired user outcome, business potential, content role, counterproductive-to-core-offer state and evidence source. Unknown material policy => defer/owner-policy required.

---

### M12-14 — no single owner was promoted to a content gap

**Failure:** distributed current content or a strong existing high-level article could be overlooked and a new broad page proposed.

**Root cause:**

```text
NO SINGLE EXACT OWNER
WAS TREATED AS
NO CURRENT CONTENT COVERAGE
```

**Control:** mandatory current-content reuse audit across relevant articles/hubs/children/services before informational CREATE.

---

### M12-15 — action label substituted for diagnosis

**Failure:** `EXPAND` or `SECTION` implicitly stood in for why the page was deficient.

**Root cause:**

```text
PRESCRIPTION
WAS TREATED AS
DIAGNOSIS
```

**Control:** separate structural-gap and content-enhancement diagnoses before action selection.

---

### M12-16 — structural KEEP was allowed to sound like “no optimization needed”

**Failure:** correct structural ownership could be overread as proof of good performance/content completeness.

**Root cause:**

```text
CORRECT URL ROLE
WAS TREATED AS
GOOD PAGE PERFORMANCE / COMPLETE OPTIMIZATION
```

**Control:** `KEEP_STRUCTURAL_OWNER` is separate from performance/optimization state. Missing private analytics limits the claim.

---

### M12-17 — intended target and observed Search-selected URL were compressed together

**Failure:** analyst recommendation and observed Search behavior became hard to distinguish.

**Root cause:**

```text
DESIRED OWNER
WAS TREATED AS
OBSERVED SEARCH OWNER
```

**Control:** preserve `INTENDED_TARGET_URL` separately from `CURRENT_SEARCH_RELEVANT_URL` and its evidence state.

---

### M12-18 — broad intent hid material Search result type/format/angle

**Failure:** “informational/commercial” was sometimes too coarse to resolve a disputed page boundary.

**Root cause:**

```text
BROAD INTENT CLASS
WAS TREATED AS
FULL SEARCH-PRESENTATION EVIDENCE
```

**Control:** when material, preserve content type, format and angle separately; write `NOT_SEPARATELY_OBSERVED` rather than infer missing dimensions.

---

### M12-19 — owner-goal inference strength was hidden

**Failure:** a public-site inference could look equivalent to an explicit client instruction.

**Root cause:**

```text
PLAUSIBLE BUSINESS INFERENCE
WAS PRESENTED TOO CLOSE TO
CLIENT-CONFIRMED POLICY
```

**Control:** preserve owner-goal evidence source such as client-stated, analytics-observed, sales/support, public-site explicit, public-site inferred or unknown.

---

### M12-20 — internal linking was treated as a routing-graph afterthought

**Failure:** a page relation could become an IMPLEMENT link without independent source-context and target-fit evidence.

**Root cause:**

```text
SEMANTIC/ROUTING EDGE
WAS TREATED AS
CURRENT CONTEXTUAL LINK OPPORTUNITY
```

**Control:** current source context + current target fit + user-next-step usefulness are required before IMPLEMENT.

---

### M12-21 — later evidence did not automatically reopen all members of a contradicted unit

**Failure:** once a unit ID existed, later evidence could narrow/contradict the boundary while only the triggering phrase was reconsidered.

**Root cause:**

```text
STRUCTURAL UNIT ID
BECAME A SELF-SEALING ASSUMPTION
```

**Control:** material later contradiction reopens all members; run the global-coherence gate and rebuild affected downstream outputs.

---

### M12-22 — action explanation was allowed to prove the action

**Failure:** generated gap/evidence fields could paraphrase the chosen action and then satisfy QA.

**Root cause:**

```text
DECISION GENERATOR
GENERATED ITS OWN CAUSAL JUSTIFICATION
```

**Control:** `ACTION MUST NEVER BE AN EVIDENCE SOURCE FOR ITSELF`; obey the evidence-independence companion gate.

---

### M12-23 — known regression set reaching zero was mistaken for global correctness

**Failure:** exact known corrections passed while unknown mixed-unit defects remained outside that regression set.

**Root cause:**

```text
KNOWN DEFECTS FIXED
WAS TREATED AS
FAILURE UNIVERSE EXHAUSTED
```

**Control:** independent global coherence review must be capable of discovering new defect classes.

---

### M12-24 — downstream artifacts could remain accepted after upstream mutation

**Failure:** a corrected semantic/unit boundary could invalidate page actions/links/pair graphs while historical downstream PASS remained visible.

**Root cause:**

```text
HISTORICAL DOWNSTREAM PASS
WAS NOT DEPENDENCY-INVALIDATED BY
MATERIAL UPSTREAM CHANGE
```

**Control:** compute impact set, rebuild affected outputs, then independently verify rebuilt state before restoring PASS.

---

## 4. Structural gap vs content enhancement

Keep these separate:

```text
STRUCTURAL_GAP_STATE =
  NONE
  TOPIC_GAP
  INTENT_GAP
  MIXED_STRUCTURAL_GAP
  STRUCTURAL_EVIDENCE_INSUFFICIENT

CONTENT_ENHANCEMENT_STATE =
  NONE
  QUALITY_GAP
  ORIGINALITY_GAP
  CONTENT_EVIDENCE_INSUFFICIENT
  NOT_ASSESSED
```

A content-quality gap does not create a new URL boundary by itself.

---

## 5. Correct Step12 execution order

This is the canonical reusable order.

### Stage 1 — whole-job/step gate

State whole goal, full roadmap, completed/remaining work, Step12 goal/output, known failure classes/root causes and non-repeat controls. Complete current method research/trace and owner-facing plain-language summary. Obtain authorization where required.

### Stage 2 — freeze accepted upstream phrase-level inputs

Read current accepted phrase map, ownership/corrections/unresolved state, demand evidence and Search evidence. Preserve exact IDs/provenance.

### Stage 3 — define owner/business goal evidence

Record best available goal and desired user outcome. Label inference strength; do not invent client policy.

### Stage 4 — materialize every phrase and challenge semantic coherence

No hidden lexical overrides. Every active phrase belongs to one explicit final structural unit or a named unresolved state.

### Stage 5 — fresh current-site/current-content discovery

Apply `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`. Reconcile newly discovered material pages and distributed content coverage.

### Stage 6 — diagnose structural/content gap before prescribing action

Record structural gap and content enhancement states from independent current evidence.

### Stage 7 — evaluate business truth and business potential

Confirm the business can fulfil the promised product/service/content task and that the content role aligns with the best available owner goal evidence.

### Stage 8 — attach real demand evidence

Use actual acquired demand/frequency/search evidence. Phrase count remains coverage only.

### Stage 9 — attach Search boundary evidence when material

Separate intended target from observed relevant URL; preserve content type/format/angle when actually observed and relevant.

### Stage 10 — compare alternatives before CREATE

Mandatory default comparison path:

```text
KEEP STRUCTURAL OWNER
→ EXPAND EXISTING PAGE
→ ADD SECTION / FAQ
→ ROUTE TO EXISTING SPECIALIST / CHILD
→ REFRAME / CONSOLIDATE CURRENT CONTENT
→ ONLY THEN EVALUATE CREATE
```

This is not a ban on CREATE. It proves CREATE fills a remaining gap.

### Stage 11 — repeat fresh CREATE gate immediately before acceptance

Every surviving CREATE must prove:

```text
CURRENT EXISTENCE CHECK
+ CURRENT CONTENT REUSE AUDIT
+ DISTINCT USER TASK
+ REAL DEMAND
+ BUSINESS TRUTH / GOAL FIT
+ SEARCH BOUNDARY WHEN MATERIAL
+ NO CURRENT EQUIVALENT
+ IMPLEMENTABLE HIERARCHY
```

One false CREATE => re-audit all current CREATE candidates.

### Stage 12 — choose action and evidence-derived confidence/maturity

No default HIGH. Unresolved material evidence/dependency remains visible.

### Stage 13 — materialize implementation relationships

New/split pages: parent, inbound path, outbound/support path, commercial handoff where relevant, navigation/breadcrumb role.

Existing-page relationships: internal-link action only when source context + target fit + user usefulness are current and independently validated.

### Stage 14 — materialize complete phrase→unit→page/action map

Every current active phrase is accounted exactly once in the final structural decision universe or explicit unresolved/deferred state.

### Stage 15 — derive complete Step13 candidate pair universe

Derive from the final routing graph. Do not diagnose harmful cannibalization in Step12.

### Stage 16 — independent global coherence + evidence QA

Apply the companion gates. The verifier must attempt to falsify actions, not confirm their schema.

### Stage 17 — persist diagnostics and outputs before final gate

Save failure diagnostics safely, then final outputs, then GitHub readback.

### Stage 18 — plain-language end report

Explain why the step was done, what structurally changes, what was rejected/deferred, what remains provisional and what the next stage may do.

---

## 6. Correct action semantics

### KEEP_STRUCTURAL_OWNER

Current page is the correct structural owner. Does not mean no content/performance optimization is needed.

### EXPAND_EXISTING_PAGE

Owner is correct but independently observed same-task content needs remain materially under-covered.

### ADD_SECTION_OR_FAQ_TO_EXISTING

A subordinate question/task belongs on the current owner and lacks a justified standalone URL boundary.

### ROUTE_TO_EXISTING_PAGE_AS_SUBTASK

A useful subtask should be served by an existing specialist/child/supporting page. Material routes require implementation relationship evidence.

### NEW_COMMERCIAL_PAGE / NEW_INFORMATIONAL_PAGE

Allowed only after the fresh existence/reuse/business/demand/Search/hierarchy gates prove a real standalone remaining gap.

### SPLIT_EXISTING_PAGE

Allowed when current content combines large independent terminal tasks that require distinct page responsibility.

### MERGE_STRUCTURALLY_REDUNDANT_PAGES

Allowed as a structural candidate only when pages are genuinely redundant for the same task and one can replace the other without losing distinct value. Search harm remains Step13 evidence.

### NO_STANDALONE_PAGE

Means only “do not create a separate URL for this unit”; still route useful subtasks or explicitly defer them.

### OUTSIDE_SCOPE_NO_ACTION

Requires scope/business/task evidence and a salvage pass for useful in-scope members.

### DEFER_PENDING_EVIDENCE

Use when the necessary business, policy, current-content, Search or other evidence is insufficient. Name the missing evidence and recheck trigger.

---

## 7. Evidence-derived confidence model

Expose equivalent dimensions:

```text
TASK_COHERENCE
BUSINESS_TRUTH
OWNER_GOAL_ALIGNMENT
OWNER_GOAL_EVIDENCE_SOURCE
BUSINESS_POTENTIAL
CONTENT_ROLE
FRESH_SITE_CHECK
EXISTING_CONTENT_REUSE
STRUCTURAL_GAP_STATE
CONTENT_ENHANCEMENT_STATE
CURRENT_PAGE_FIT
DEMAND_SUPPORT
SEARCH_BOUNDARY_SUPPORT
RELEVANT_URL_MATCH_STATE
HIERARCHY_CLARITY
PERFORMANCE_EVIDENCE_STATE
DOWNSTREAM_DEPENDENCY_STATE
```

Confidence must be derived from them with visible downgrade reasons.

```text
UNVERIFIED BUSINESS TRUTH -> cannot become high-confidence commercial CREATE
WEAK TASK COHERENCE -> cannot become high-confidence structural action
MATERIAL SEARCH BOUNDARY UNKNOWN -> provisional when Search can change boundary
UNKNOWN OWNER POLICY -> no final policy-sensitive action
```

No universal numeric threshold is required.

---

## 8. Required artifacts

Current-job filenames may vary, but equivalent outputs should exist:

```text
STRUCTURAL UNITS / CORRECTIONS
STRUCTURAL ACTIONS
NEW-PAGE EVIDENCE
PHRASE ACTION MAP
PAGE ACTION ROLLUP
HIERARCHY / RELATIONSHIP PLAN
INTERNAL-LINK ACTION LEDGER
NEXT-STEP CANDIDATE PAIRS
SEARCH REQUIRED HANDOFF
QA REVIEW LEDGER
QA JSON
REPORT
CURRENT STATE / JOB FLOW UPDATE
```

Historical artifacts remain traceable; corrections do not rewrite history silently.

---

## 9. QA model

### Accounting

```text
ALL CURRENT ACTIVE PHRASES ACCOUNTED
NO DUPLICATE FINAL PHRASE ROWS
NO SILENT DROPS
EVERY ASSIGNED PHRASE HAS ONE FINAL UNIT
UNRESOLVED PHRASES HAVE EXPLICIT NON-FINAL STATE
```

### Structural/action evidence

```text
HIDDEN LEXICAL OVERRIDES = 0
MIXED UNITS LEFT UNCORRECTED = 0
NEW PAGE WITHOUT FRESH EXISTENCE/REUSE GATE = 0
NEW PAGE WITHOUT DEMAND/BUSINESS EVIDENCE REQUIRED BY CLAIM = 0
DEFAULT HIGH CONFIDENCE = false
ACTION WITHOUT EVIDENCE DIMENSIONS = 0
UNSUPPORTED SPLIT/MERGE = 0
USEFUL PHRASES STRANDED BY NO_STANDALONE/OUTSIDE = 0
IMPLEMENTABLE ACTION WITHOUT PRIMARY DESTINATION = 0
```

### Evidence independence

```text
ACTION USED AS ITS OWN EVIDENCE = 0
QUALITY GAP WITHOUT CURRENT PAGE + MISSING NEED = 0
LINK IMPLEMENT WITHOUT CURRENT SOURCE CONTEXT = 0
LINK IMPLEMENT WITHOUT CURRENT TARGET FIT = 0
SELF-ASSERTED QA PASS FIELDS = 0
KNOWN-REGRESSION-ZERO USED AS GLOBAL COHERENCE PROOF = 0
```

### Step boundaries

```text
PREMATURE CANNIBALIZATION/HARM VERDICT = 0
PREMATURE SEARCH-ARCHITECTURE FREEZE = 0
AI EVIDENCE USED EARLY = 0
```

### Correction/reopen

```text
MATERIAL UPSTREAM CHANGE WITHOUT DOWNSTREAM IMPACT TRACE = 0
AFFECTED DOWNSTREAM PASS REUSED WITHOUT REBUILD/PROOF = 0
FINAL GITHUB READBACK = PASS
```

---

## 10. Pass gate

Step12 may pass only when the current job's declared expected totals reconcile and all material gates above pass.

Do not hard-code rehearsal-specific counts in this permanent method.

Canonical boundary:

```text
STEP12_COMPLETE
-> STEP13 MAY BECOME NEXT ALLOWED STAGE

STEP12_COMPLETE
!= STEP13 EXECUTED
!= HARMFUL CANNIBALIZATION PROVEN
!= FINAL SEARCH ARCHITECTURE FROZEN
```

If evidence cannot resolve a material structural boundary, preserve a provisional/deferred state instead of fabricating PASS.

---

## 11. Permanent non-repeat markers

```text
KW001_STEP12_METHOD_ACTIVE = true
KW001_STEP12_JOB_SPECIFIC_RESULTS_FORBIDDEN_IN_PERMANENT_METHOD = true
KW001_STEP12_HIDDEN_LEXICAL_OVERRIDES_FORBIDDEN = true
KW001_STEP12_STRUCTURAL_UNITS_REQUIRED = true
KW001_STEP12_GLOBAL_COHERENCE_REVALIDATION_REQUIRED_AFTER_MATERIAL_CONTRADICTION = true
KW001_STEP12_PHRASE_COUNT_NOT_EQUAL_DEMAND = true
KW001_STEP12_NEW_PAGE_FRESHNESS_AND_REUSE_GATE_REQUIRED = true
KW001_STEP12_OWNER_GOAL_EVIDENCE_SOURCE_REQUIRED = true
KW001_STEP12_CONFIDENCE_MUST_BE_EVIDENCE_DERIVED = true
KW001_STEP12_QA_MUST_BE_INDEPENDENTLY_DERIVED = true
KW001_STEP12_ACTION_CANNOT_PROVE_ITSELF = true
KW001_STEP12_STRUCTURAL_OWNER_NOT_EQUAL_PERFORMANCE_STATE = true
KW001_STEP12_INTENDED_TARGET_NOT_EQUAL_OBSERVED_SEARCH_URL = true
KW001_STEP12_INTERNAL_LINK_IMPLEMENT_REQUIRES_CURRENT_SOURCE_AND_TARGET_VALIDATION = true
KW001_STEP12_NO_STANDALONE_REQUIRES_SUBTASK_RESOLUTION = true
KW001_STEP12_UPSTREAM_STATE_CAN_BE_FALSIFIED_BY_LATER_MATERIAL_EVIDENCE = true
KW001_STEP12_DOWNSTREAM_INVALIDATION_REQUIRED_AFTER_MATERIAL_UPSTREAM_CHANGE = true
KW001_STEP12_STEP13_CANDIDATE_UNIVERSE_MUST_BE_DERIVED = true
KW001_STEP12_DIAGNOSTICS_PERSIST_BEFORE_FINAL_GATE = true
```

## ПРОСТЫМИ СЛОВАМИ

Step12 нужен, чтобы из очищенных запросов и назначенных страниц сделать честный план изменений сайта. Сначала проверяем, что люди действительно хотят одного и того же результата, затем смотрим, что бизнес реально предлагает и что уже есть на текущем сайте, после этого учитываем реальный спрос и Search только там, где они меняют решение. Новую страницу создаём последней альтернативой, а не первой. Любое действие затем проверяется независимо — выбранное решение не имеет права само служить доказательством собственной правильности.
