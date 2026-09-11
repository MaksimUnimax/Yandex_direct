# KW-002 — LEVEL 2 UNIVERSAL STEP RULES INDEX

Status: **ACTIVE / UNIVERSAL ROADMAP / EXECUTABLE FOR ANY ELIGIBLE SITE OR BUSINESS**

Product: from-scratch semantic core + Yandex-grounded planned site architecture + later AI-search reconciliation.

Canonical architecture authorities:

- `../LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`
- `../LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `../LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`
- `../LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md`

This file defines the roadmap. It contains no current client/site facts, current job counts, family IDs, query IDs, owner execution status or project-specific examples.

## Global data flow

```text
FROZEN BUSINESS/SCOPE
→ BUSINESS/OFFER MODEL
→ SEED/PROBE MAP
→ PRIMARY RAW ACQUISITION
→ NORMALIZED UNIQUE POOL
→ CONSERVATIVELY SANITIZED CANDIDATES + HOLD
→ PRELIMINARY FAMILY/TASK MAP
→ TARGETED COVERAGE EXPANSION
→ CURRENT SEARCH COMPETITOR DISCOVERY
→ COMPETITOR-DERIVED EXPANSION
→ CANDIDATE SEMANTIC MASTER
→ ROW-LEVEL RELEVANCE / USER TASK / INTENT / PRIORITY
→ SEARCH-STAGE SEMANTIC FREEZE
→ CURRENT YANDEX SERP EVIDENCE
→ SERP + TASK-FIRST CLUSTERING
→ QUERY→PAGE OWNERSHIP + SEARCH-ONLY IA
→ AI-SEARCH DIAGNOSTIC CASE SELECTION
→ AI-SEARCH EVIDENCE
→ SEARCH-vs-AI RECONCILIATION
→ FINAL CORE + IA + PAGE JOBS + INTERNAL LINKS
→ CLIENT DELIVERABLES
→ FINAL QA / RECIPIENT ACCEPTANCE
→ REVISION REHEARSAL / PRODUCTIZATION MEASUREMENT
→ JOB CLOSE
```

Hard rule:

```text
ROADMAP STEP != CURRENT JOB SPECIAL CASE
```

A job may have HOLD/rework branches, but the permanent step exists because the need is reusable across sites.

---

# STEP 00 — freeze order, scope, sources and delivery promise

## Why

Analysis cannot be judged if the business question, source authority or promised output is allowed to drift during research.

## Input

Client/owner facts and permitted raw source material only.

## Method

Freeze:

```text
business description
products/services/offer boundary
region/geography
commercial goal
important exclusions
site state
allowed input sources
sealed/prohibited sources
purchased delivery scope/cap
```

## Root causes prevented

- source/scope authority drift;
- prior research contaminating a from-scratch baseline;
- later evidence silently rewriting the original order.

## Output

Frozen brief, source whitelist, delivery scope/cap, job manifest.

## PASS

No unresolved ambiguity that would materially change what market/business is being researched or what must be delivered.

---

# STEP 01 — factual business / offer / assortment model

## Why

Search research must start from what the business can actually sell/provide, not from an analyst-invented SEO taxonomy.

## Input

Frozen client/business facts and approved assortment/service sources.

## Method

Build a neutral model of:

```text
offers/products/services
families/categories where factually supported
attributes/forms where factually supported
use cases/problems where factually supported
commercial actions
known exclusions
unknown/ambiguous business facts
```

## Root causes prevented

- analyst invention presented as client truth;
- business accounting mistaken for search taxonomy;
- incomplete offer lineage into acquisition planning.

## Output

Business/offer model + ambiguity/unknown ledger where needed.

## PASS

Every material business direction can trace to an approved fact source; unsupported attributes/claims are explicit UNKNOWN rather than invented.

---

# STEP 02 — seed / acquisition probe design

Dedicated universal gate:

`STEP_02_SEED_ACQUISITION_QUALITY_GATE.md`

## Why

The project needs measurement probes that can discover market vocabulary, not a fake final keyword list copied from client labels.

## Input

Business/offer model.

## Method

Build a bounded, purpose-labelled set of discovery probes across relevant dimensions such as head terms, synonyms, use cases, problems, attributes/forms, commercial modifiers, exact names and qualified refinements.

## Root causes prevented

- business lineage coverage mistaken for search-discovery quality;
- ambiguous bare names accepted without refinement;
- client taxonomy copied into acquisition taxonomy;
- request cost/convenience overriding information gain.

## Output

Seed/probe map + deterministic primary acquisition manifest.

## PASS

Business lineage coverage and search-probe quality coverage both pass; every probe has a named information purpose and ambiguity/refinement logic.

---

# STEP 03 — primary Wordstat acquisition

Dedicated universal gates:

- `STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`
- `STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`

## Why

Acquire current Yandex demand evidence losslessly before semantic selection begins.

## Input

Primary acquisition manifest + current provider contract/depth decision.

## Method

For every authorized request:

```text
justify depth
→ execute
→ receive complete result
→ persist complete RAW result
→ persist request/provenance
→ remote readback
→ reconcile rows/fields/status
→ only then next request
```

## Root causes prevented

- technical/provider success mistaken for semantic completeness;
- arbitrary depth selection;
- visible chat output mistaken for durable evidence;
- raw duplicates/noise deleted before analysis.

## Output

Lossless RAW occurrence evidence + acquisition/receipt manifest.

## PASS

Every authorized item has a known terminal outcome and complete durable feed-forward required by the method.

---

# STEP 03A — normalization and safe deduplication

## Why

The raw occurrence universe is too repetitive/noisy for efficient semantic analysis but must remain fully traceable.

## Input

Complete RAW occurrence pool.

## Method

Conservative normalization:

```text
preserve RAW text
normalize case/whitespace conservatively
create stable normalized identity
collapse exact duplicates analytically
preserve every occurrence lineage
only merge implicit variants when equivalence is high-confidence
otherwise keep separate/HOLD
```

## Root causes prevented

- destructive normalization;
- provenance loss;
- deduplication optimized for row reduction instead of semantic identity.

## Output

Normalized unique pool + normalization ledger.

## PASS

RAW lineage loss = 0; every normalized row traces to RAW; uncertain implicit equivalence is not silently collapsed.

---

# STEP 03B — conservative high-confidence sanitation

## Why

Remove obvious foreign/noise cases before expensive semantic work while preserving unresolved ambiguity.

## Input

Normalized unique pool + frozen business scope.

## Method

```text
CLEAR OFF-TOPIC -> EXCLUDE with reason
DIRECT BUSINESS-SUPPORTED -> KEEP CANDIDATE
MATERIAL AMBIGUITY -> HOLD
```

Use bounded context/referent rules; do not let frequency, delivery cap, broad stems or a single business token decide semantics.

## Root causes prevented

- prefix/substring overreach;
- positive business token overriding explicit foreign context;
- ambiguity destroyed too early;
- mechanical QA mistaken for semantic QA.

## Output

Sanitized candidate pool + excluded register + HOLD register + semantic QA.

## PASS

Every normalized identity has a deterministic state/reason and RAW lineage; independent semantic QA finds no blocking systematic defect.

---

# STEP 04 — preliminary family / topic / task triage

Dedicated universal gate:

`STEP_04_PRELIMINARY_FAMILY_TRIAGE_QUALITY_GATE.md`

## Why

Reveal the structure, ambiguity and missing areas of the sanitized demand universe before detailed row-level intent and SERP work.

## Input

KEEP candidates + relevant HOLD identities + lineage + frozen business facts.

## Method

Create preliminary family/task hypotheses while keeping topic, explicit task, ambiguity and business support distinct.

Mandatory independent family-coherence challenge for materially large/rule-heavy data.

## Root causes prevented

- first-match rule order erasing stronger task signals;
- closed taxonomy/generic fallback hiding new coherent tasks;
- lexical shortcut bias;
- family label mistaken for final SEO cluster/page;
- producer validating only its own taxonomy.

## Output

Preliminary family authority + occurrence mapping + expansion-gap queue + sanitation feedback + independent coherence/boundary QA.

## PASS

Full active/HOLD universe accounted; no blocking family-rule defects; preliminary families explicitly remain non-final for intent/SERP/page ownership.

---

# STEP 05 — targeted expansion / coverage control

## Why

Close material search-vocabulary gaps revealed by earlier evidence without turning acquisition into endless recursion.

## Input

Step04 gap hypotheses + all prior durable acquisition evidence + unresolved owner/business facts.

## Method

For each proposed expansion:

```text
name exact unresolved question
→ reconcile against all existing evidence
→ separate OWNER FACT from SEARCH DEMAND question
→ prove incremental information gain
→ define negative-result value and stop condition
→ authorize only genuinely new probe
```

All new provider results immediately pass through Step03A/03B before union.

## Root causes prevented

- duplicate acquisition of already durable evidence;
- owner/business facts sent to a search provider;
- recursive expansion without information gain.

## Output

New RAW evidence where justified + normalized/sanitized additions + updated coverage state.

## PASS

No provider-ready probe duplicates current evidence; owner-fact gaps are not searched as if demand could prove inventory/business truth.

---

# STEP 06 — current Yandex organic competitor discovery

## Why

Find pages/domains that actually compete in current search results for retained demand directions.

## Input

Representative retained semantic families/queries.

## Method

Collect current ordinary Yandex SERP evidence and record recurring domains/URLs/result types across materially different query families.

```text
BUSINESS RIVAL != SEARCH COMPETITOR
```

## Output

Search competitor registry with current Yandex discovery lineage.

## PASS

Every selected semantic competitor has current SERP evidence; no competitor is included solely because the client named it.

---

# STEP 07 — competitor semantic expansion

## Why

Discover vocabulary/topics missed by client/analyst starting language.

## Input

Current search competitor registry + relevant public competitor pages.

## Method

Extract only evidence-bearing missed topics/use cases/naming directions, each with source URL and discovery lineage.

## Output

Competitor-derived candidate seed/topic register.

## PASS

No competitor page topic is treated as proven demand or automatically accepted keyword.

---

# STEP 08 — competitor-derived Wordstat expansion

## Why

Test whether genuinely new competitor-derived topics correspond to current Yandex demand.

## Input

Genuinely new competitor-derived seed candidates.

## Method

Use Step03 acquisition/persistence/depth rules, then immediate Step03A/03B normalization/sanitation.

## Output

New demand evidence with decisions such as new demand / already covered / no useful demand / out-of-scope / HOLD.

## PASS

Only sanitized new evidence joins the candidate universe; no raw competitor-derived data bypasses normalization/sanitation.

---

# STEP 09 — candidate semantic master + reserve freeze

## Why

Create one auditable post-acquisition candidate universe before expensive row-level judgments.

## Input

All normalized/sanitized primary + targeted + competitor-derived evidence.

## Method

Freeze distinct sets:

```text
ACTIVE_CANDIDATES
HOLD_AMBIGUOUS
VALID_RESERVE_CANDIDATES
AUTO_EXCLUDED_HISTORY
```

Preserve all demand/provenance/source fields.

## Output

Candidate semantic master + reserve set.

## PASS

No candidate exists merely due to duplicate provider occurrence; no provenance/demand field is silently lost at freeze boundary.

---

# STEP 10 — nuanced row-level relevance, user task, intent and priority

## Why

Perform expensive semantic judgment only on the cleaned candidate universe.

## Input

Candidate semantic master.

## Method

Each row receives governed decisions for:

```text
KEEP / REJECT / HOLD
relevance reason
user task/job
intent or mixed intent
commercial/informational role
business-fit state
ambiguity/evidence need
priority tier
redundancy/canonicality
family coverage role
```

Frequency is one factor, never the sole priority/relevance rule.

## Output

Cleaned prioritized semantic master.

## PASS

No default KEEP; positive in-scope evidence exists; uncertainty remains explicit; row-level QA is independently checked where needed.

---

# STEP 11 — delivery-scope selection + Search-stage semantic freeze

## Why

Select the exact governed set that will receive expensive current SERP evidence and may enter final delivery.

## Input

Cleaned prioritized semantic master + purchased scope/cap.

## Method

Coverage-aware selection using business fit, task/intent, demand, redundancy, cluster coverage and rankability evidence where available.

Reserve valid rows outside scope rather than deleting them.

## Output

Search-stage selected set + valid reserve.

## PASS

Selection respects purchased cap without padding/truncating relevance and preserves important business/task breadth.

---

# STEP 12 — current ordinary Yandex Search evidence acquisition

## Why

Final SEO clustering/page ownership must be grounded in current actual SERP behavior, not lexical similarity alone.

## Input

Search-stage selected set.

## Method

Use the product's active SERP coverage mode and persist required ranked result evidence with region/time/provenance.

## Output

Current SERP evidence authority for every required selected query.

## PASS

Coverage accounting satisfies the frozen product mode; missing/failed observations remain explicit.

---

# STEP 13 — SERP + user-task-first clustering

## Why

Determine which queries can realistically be satisfied by the same page versus requiring separate page intents.

## Input

Search-stage semantic rows + current SERP evidence + Step10 user-task/intent judgments.

## Method

Combine:

```text
user task / intent
SERP overlap / result-type behavior
semantic meaning
business/page usefulness
```

No universal fixed overlap threshold is assumed unless separately validated.

## Output

Final Search-backed semantic clusters with merge/split rationale and HOLDs.

## PASS

Cluster boundaries are evidence-backed and not derived from preliminary Step04 families alone.

---

# STEP 14 — query→page ownership + Search-only information architecture

## Why

Turn Search-backed clusters into a non-cannibalizing planned site structure.

## Input

Step13 final Search clusters + business offer model.

## Method

Assign each cluster to an existing/planned page job, define page type and parent/child IA relationship, resolve overlap/cannibalization.

## Output

Search-only query→page map + planned IA freeze.

## PASS

Every retained cluster has one governed primary ownership decision or explicit HOLD; no duplicate page purpose is created without evidence.

---

# STEP 15 — AI-search diagnostic case selection

## Why

AI-search evidence is expensive and should test decisions where generative answers may materially change/enrich/de-risk the Search-only architecture.

## Input

Frozen Search-only semantic/page architecture.

## Method

Select representative high-value cases based on uncertainty, page-type risk, informational/commercial boundary or architecture sensitivity.

## Output

AI-search diagnostic manifest with exact question each case must resolve.

## PASS

Every case has expected information gain; AI-search is not used as generic SEO advice.

---

# STEP 16 — AI-search evidence acquisition

## Why

Observe how current Yandex generative answers frame selected user tasks and what source/page types are used.

## Input

AI diagnostic manifest.

## Method

Acquire/persist governed AI-search evidence with full provenance and claim boundaries.

## Output

AI-search evidence authority for selected cases.

## PASS

Evidence is complete enough for its declared comparison question; no unsupported conclusions are inferred from absent/partial outputs.

---

# STEP 17 — Search-vs-AI reconciliation

## Why

Determine whether AI evidence changes, enriches, de-risks or leaves unchanged the Search-only decision.

## Input

Frozen Search-only architecture + AI evidence.

## Method

For each diagnostic case classify:

```text
CHANGE
ENRICH
DE_RISK
NO_CHANGE
HOLD
```

AI evidence must not retroactively contaminate the Search-only baseline.

## Output

Reconciliation ledger with causal chain from baseline to any change.

## PASS

Every architecture/content change has explicit AI causal evidence; supported NO_CHANGE is accepted as valid outcome.

---

# STEP 18 — final semantic core + final IA + Page Jobs + internal-link model

## Why

Materialize the final governed implementation authority after Search and AI reconciliation.

## Input

Final clusters, query→page ownership, Search-only IA, accepted AI deltas.

## Method

Freeze final delivered core, page jobs, IA, ownership and internal-link relationships within purchased scope.

## Output

Final semantic master + architecture/page-job/internal-link authorities.

## PASS

All final rows/pages are traceable to business facts + demand + required Search evidence; AI changes are separately causal and bounded.

---

# STEP 19 — client deliverables

## Why

Translate internal evidence into usable client artifacts without leaking unnecessary internal jargon.

## Input

Accepted final authorities.

## Method

Produce client-facing semantic core, planned structure and implementation/report artifacts required by the sold scope.

## Output

Client deliverables.

## PASS

Recipient can understand what to implement, why, and what remains uncertain; internal IDs are supporting traceability, not the narrative.

---

# STEP 20 — final QA / recipient acceptance

## Why

A technically generated deliverable is not complete until recipient usability and exact-file QA pass.

## Input

Client deliverables + internal final authorities.

## Method

Run exact-file QA, accounting, traceability, contradiction checks, readability/usability tests and recipient review.

## Output

Final QA verdict + correction ledger if needed.

## PASS

All blocking defects closed; deliverables match internal truth and sold scope.

---

# STEP 21 — revision rehearsal / productization measurement

## Why

The product must be repeatable as a Kwork service, not just successful once.

## Input

Completed job + recipient/owner feedback + execution metrics.

## Method

Measure time, provider usage, Work handoffs, revision causes, failure classes, artifact quality and reusable process improvements.

Promote only class-general lessons through `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`.

## Output

Revision/productization measurement + proposed universal improvements or job-specific notes.

## PASS

Universal changes are justified by root cause/generalization, not copied from one client example.

---

# STEP 22 — job close

## Why

Prevent “almost finished” jobs with unresolved publication, review, revision or evidence states.

## Input

Accepted deliverables, QA, publication/readback and revision state.

## Method

Close all pending actions, persist final cursor/manifest, verify remote recoverability and handoff.

## Output

Closed job state.

## PASS

```text
OPEN_BLOCKING_ACTIONS = 0
FINAL_ARTIFACTS_PUBLISHED_AND_READ_BACK = true
FINAL_STATUS_TRUTH = COMPLETE
```

---

# Global PASS rule for roadmap execution

Every major step must also satisfy applicable Level1 failure regressions.

```text
METHOD = PASS
FULL_VOLUME_ACCOUNTING = PASS where applicable
SEMANTIC_QA = PASS where applicable
KNOWN_FAILURE_REGRESSION_MATRIX = PASS
PERSISTENCE/REMOTE_READBACK = PASS where applicable
OPEN_CRITICAL_DEFECTS = 0
```

A quality score cannot override a failed hard gate.
