# KW-002 — INHERITED UNIVERSAL STEP RULES FROM KW-001

Status: **ACTIVE / UNIVERSAL / COMPANION TO STEP_RULES_INDEX**

Purpose: preserve reusable failure controls learned in KW-001 without importing any existing-site-specific assumption or any current-job value into KW-002.

Documentation hierarchy:

```text
LEVEL1 = universal cross-step rules/root causes
LEVEL2 = universal roadmap step methods
work/<JOB_ID>/ = concrete client/order facts, evidence, counts, IDs and status
```

This file contains only reusable rules, WHY they exist, failure mechanisms and PASS boundaries.

---

# STEP 00 — scope freeze

## Rule
Freeze business, geography, offer boundary, exclusions, commercial goal, promised outputs, allowed inputs and sealed/prohibited prior research before evidence acquisition.

## Why
If the definition of the order changes during research, downstream results can be internally consistent but answer a different problem.

## Failure blocked

```text
EVOLVING ANALYSIS CHANGED ORIGINAL SUCCESS CRITERION
```

## PASS
Frozen brief exists before analysis; later corrections are versioned as explicit authority changes.

---

# STEP 01 — business / offer model

## Rule
Build a factual neutral model of what the business actually sells/provides before inventing acquisition vocabulary or SEO structure.

## Why
Client vocabulary is evidence about the offer, not proof of how users search or how pages should be structured.

## Failure blocked

```text
CLIENT/ANALYST TAXONOMY WAS TREATED AS SEARCH TAXONOMY
UNSUPPORTED OFFER FACTS WERE INVENTED
```

## PASS
Every material offer direction traces to an approved business fact; unknowns remain explicit.

---

# STEP 02 — seed / acquisition plan

## Rule
Every seed is a measurement probe with a named information purpose.

```text
SEED != FINAL KEYWORD
SEED != FINAL PAGE
CLIENT TAXONOMY != AUTOMATIC ACQUISITION TAXONOMY
```

## Why
A broad/ambiguous phrase can be useful for discovery without being suitable as final semantic truth.

## Failure blocked

```text
MEASUREMENT INSTRUMENT WAS TREATED AS FINAL OBJECT
```

## PASS
Every seed has source lineage, information question, ambiguity/refinement logic and incremental discovery purpose.

Dedicated current gate: `STEP_02_SEED_ACQUISITION_QUALITY_GATE.md`.

---

# STEP 03 — primary Wordstat acquisition

## Rule
For every authorized provider item:

```text
JUSTIFY DEPTH
→ EXECUTE
→ RECEIVE COMPLETE RESULT
→ DURABLY SAVE COMPLETE REQUIRED BODY
→ READBACK
→ COUNT/FIELD/PROVENANCE RECONCILIATION
→ ONLY THEN NEXT ITEM
```

## Why
Provider/transport success does not preserve semantic evidence or prove sufficient acquisition depth.

## Failure blocked

```text
HTTP/STATUS SUCCESS WAS TREATED AS COMPLETE DATA ACQUISITION
TECHNICAL TEST DEPTH WAS TREATED AS SEMANTIC COVERAGE
```

## PASS
All returned evidence required by the step is durably preserved and current depth is methodologically justified.

Dedicated gates:
- `STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`
- `STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`

---

# STEP 03A — normalization / deduplication

## Rule
Create a normalized analytical identity layer without destroying RAW provenance or merging uncertain meanings.

## Why
Aggressive row reduction can erase meaningful morphology, punctuation, order or occurrence lineage.

## Failure blocked

```text
DEDUPLICATION OPTIMIZED ROW COUNT INSTEAD OF SEMANTIC IDENTITY
```

## PASS
RAW lineage loss = 0; exact/implicit merge decisions are explainable and uncertain variants remain separate/HOLD.

---

# STEP 03B — conservative sanitation

## Rule
Use bounded context/referent evidence for high-confidence exclusions; preserve material ambiguity.

```text
CLEAR OFF-TOPIC -> EXCLUDE
DIRECT BUSINESS-SUPPORTED -> KEEP CANDIDATE
AMBIGUOUS -> HOLD
```

## Why
Substring, prefix, single-token and positive-business fallbacks can systematically misclassify homonyms/foreign contexts.

## Failure blocked

```text
TOKEN MATCH WAS TREATED AS REFERENT/INTENT PROOF
BINARY CLEAN OUTPUT DESTROYED UNCERTAINTY
```

## PASS
Every state has deterministic reason/provenance and independent semantic QA finds no blocking systematic defect.

---

# STEP 04 — preliminary family/topic/task triage

## Rule
Create preliminary demand families and user-task hypotheses from sanitized candidates while preserving ambiguity and explicitly separating topic context from stronger task signals.

```text
PRELIMINARY FAMILY != FINAL INTENT
PRELIMINARY FAMILY != SERP CLUSTER
PRELIMINARY FAMILY != PAGE
```

## Why
Ordered lexical taxonomies can hide tasks, overfit to predefined labels, or look deceptively like final clusters.

## Failure blocked

```text
FIRST-MATCH PRECEDENCE ERASED STRONGER TASK
GENERIC FALLBACK HID UNMODELLED TASK
PRODUCER VALIDATED ONLY ITS OWN TAXONOMY
```

## PASS
Full semantic universe is reproducibly mapped; independent family-coherence diagnostics pass; no final page/intent claims are made.

Dedicated gate: `STEP_04_PRELIMINARY_FAMILY_TRIAGE_QUALITY_GATE.md`.

---

# STEP 05 — targeted expansion / coverage control

## Rule
Run second acquisition only for a named unresolved search-demand question after reconciliation against all durable evidence.

## Why
Local apparent gaps can duplicate earlier evidence or actually be owner/business fact gaps.

## Failure blocked

```text
RECURSIVE KEYWORD COLLECTION WITHOUT INFORMATION GAIN
OWNER FACT SENT TO SEARCH PROVIDER
DUPLICATE PROVIDER ACQUISITION
```

## PASS
Every provider-ready probe has incremental information gain, negative-result value, stop condition and no equivalent prior evidence.

---

# STEP 06 — current Search competitor discovery

## Rule
Search competitors come from current SERP recurrence across representative retained demand, not client labels.

```text
BUSINESS RIVAL != SEARCH COMPETITOR
```

## PASS
Every selected search competitor has current SERP discovery lineage.

---

# STEP 07 — competitor semantic expansion

## Rule
Use current SERP-discovered competitor pages to generate candidate missed topics/seeds with URL/topic lineage.

```text
COMPETITOR PAGE TOPIC != PROVEN DEMAND
COMPETITOR-DERIVED SEED != FINAL KEYWORD
```

## PASS
Every candidate has discoverable source lineage and remains a hypothesis until demand evidence.

---

# STEP 08 — competitor-derived Wordstat expansion

## Rule
Return genuinely new competitor-derived topics to the same provider/persistence/normalization/sanitation pipeline before union.

## PASS
Only sanitized new demand evidence enters the candidate universe.

---

# STEP 09 — candidate semantic master freeze

## Rule
Freeze one auditable candidate universe with complete source/demand/provenance/state fields before expensive row-level judgment.

## Failure blocked

```text
FREEZE BOUNDARY SILENTLY LOST DEMAND/PROVENANCE
```

## PASS
Active/HOLD/reserve/excluded history remain distinct and traceable.

---

# STEP 10 — nuanced row relevance / task / intent / priority

## Rule
No default KEEP. Require positive business-fit evidence; preserve uncertainty; prioritize by business/task/coverage and demand, not frequency alone.

## PASS
Every candidate has explicit relevance/task/intent/priority reasoning or HOLD.

---

# STEP 11 — Search-stage semantic freeze

## Rule
Freeze the exact delivery/Search-selected set with deterministic joins to all prior evidence.

## PASS
No retained row lacks complete upstream traceability; valid outside-scope rows remain reserve.

---

# STEP 12 — current Search evidence

## Rule
Persist exact-query/current-region SERP evidence for the governed Search-stage set under the active coverage policy.

## PASS
Required Search coverage is complete or missing evidence is explicit; no silent sampling claim.

---

# STEP 13 — task-first + SERP-backed clustering

## Rule
Cluster by user task/intent and current SERP behavior; semantic similarity assists but does not replace judgment.

## Failure blocked

```text
LEXICAL FAMILY WAS TREATED AS FINAL PAGE CLUSTER
```

## PASS
Merge/split boundaries are evidence-backed and mixed/uncertain clusters remain explicit.

---

# STEP 14 — query→page ownership + Search-only IA

## Rule
Assign final Search clusters to one governed planned page/job and freeze Search-only architecture before AI evidence.

## PASS
Every retained cluster has explicit primary ownership or HOLD; no unproved duplicate page jobs.

---

# STEP 15 — AI diagnostic case selection

## Rule
Select AI-search cases for decision value, not arbitrary representativeness.

## PASS
Every case has named uncertainty/information gain and control boundary.

---

# STEP 16 — AI evidence acquisition

## Rule
Preserve raw AI/search evidence and keep provider/source claim boundaries explicit.

## PASS
Evidence is complete enough for declared diagnostic questions; one response is not treated as stable universal truth.

---

# STEP 17 — Search-vs-AI reconciliation

## Rule
Preserve frozen Search baseline and classify AI effect explicitly:

```text
CHANGE | ENRICH | DE_RISK | NO_CHANGE | HOLD
```

## PASS
Every change has causal evidence; NO_CHANGE is valid.

---

# STEP 18 — final architecture authority

## Rule
One current canonical truth feeds final semantic core, page ownership, IA, Page Jobs and internal links.

## PASS
No contradictory downstream artifact survives a canonical change.

---

# STEP 19 — client deliverables

## Rule
One internal truth feeds all recipient views; client language/usability is separate from internal traceability.

## PASS
Every promised artifact is complete and understandable without decoding internal IDs.

---

# STEP 20 — final QA / recipient acceptance

## Rule
Artifact existence/package QA does not replace exact-file analytical/recipient QA.

## PASS
Data correctness, consistency, readability and recipient usability all pass.

---

# STEP 21 — revision rehearsal / productization measurement

## Rule
Revisions reprocess only materially affected dependencies; universal method promotion requires root-cause generalization, not one-job copying.

## PASS
Impact boundary is explicit and unaffected evidence is preserved.

---

# STEP 22 — close

## Rule
Close only after deliverables, publication/readback, revisions and pending actions are complete.

## PASS
No blocking pending state remains.

---

# Cross-step inherited rules

```text
GOAL BEFORE EXECUTION
FULL ROADMAP VISIBILITY
FRESH ERROR/LESSON REREAD
FRESH EXTERNAL METHOD RESEARCH
SOURCE→METHOD TRACE
INFORMATION GAIN BEFORE PROVIDER CALL
QUALITY > TRIVIAL PROVIDER COST SAVING
PROVIDER SUCCESS != PROJECT COMPLETION
COMPLETE DURABLE EVIDENCE BEFORE NEXT PROVIDER ACTION
UNCERTAINTY REMAINS EXPLICIT
MATERIAL UPSTREAM CHANGE INVALIDATES AFFECTED DOWNSTREAM PASS
LARGE DATA MUST NOT BE SAMPLED FOR CONTEXT CONVENIENCE
WORK OUTPUT REQUIRES INDEPENDENT RETURN QA
SEARCH-ONLY BASELINE BEFORE AI DELTA
DO NOT FORCE AI DELTA
ONE CANONICAL TRUTH FEEDS CLIENT ARTIFACTS
JOB DATA MUST NOT CONTAMINATE UNIVERSAL METHOD
```
