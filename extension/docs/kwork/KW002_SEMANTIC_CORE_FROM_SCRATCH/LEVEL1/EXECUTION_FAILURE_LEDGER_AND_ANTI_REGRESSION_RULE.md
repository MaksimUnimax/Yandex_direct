# KW-002 — UNIVERSAL EXECUTION FAILURE LEDGER AND ANTI-REGRESSION RULE

Status: **OWNER-MANDATED / ACTIVE / UNIVERSAL / MUST BE READ BEFORE EVERY LATER STEP**
Decision date: 2026-09-11
Applies to: all KW-002 jobs and every Main ChatGPT / Work execution pass.

Companion architecture authority:

`ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`

## 1. Purpose

This file stores **universal failure mechanisms**, their root causes and reusable anti-regression gates.

Concrete client names, product names, family IDs, query IDs, request IDs, row counts and job-specific examples belong in `work/<JOB_ID>/` failure ledgers and audit evidence.

Hard distinction:

```text
UNIVERSAL FAILURE CLASS = mechanism that can recur on another site
JOB FAILURE RECORD = proof that the mechanism occurred in one execution
```

A known failure class without an explicit regression gate means the current step is not ready for PASS.

---

## F00 — source/scope authority drift

### Root cause

Execution starts before the authoritative source set, business boundary or purchased scope is frozen, or a later scope change is treated as an additive note instead of an invalidating authority mutation.

### Why it fails

Downstream work can be internally consistent while answering the wrong business/scope question.

### Universal rule

```text
MATERIAL INPUT AUTHORITY CHANGE
-> identify every dependent artifact
-> invalidate affected PASS states
-> rebuild/reconcile from the new authority
-> only then continue
```

### Gates

```text
ACTIVE_INPUT_SOURCE_SET == CURRENT_OWNER_APPROVED_SOURCE_SET
SUPERSEDED_INPUT_USED_AS_CURRENT = 0
DEPENDENT_PASS_AFTER_MATERIAL_INPUT_CHANGE_WITHOUT_RECHECK = 0
```

---

## F01 — business/accounting completeness mistaken for search completeness

### Root cause

A model covers every catalog/service row, so execution assumes search-discovery coverage is also complete.

### Why it fails

Client taxonomy describes inventory/services; users may search with synonyms, use cases, problems, attributes, colloquial language and ambiguous names that the client never uses.

### Universal rule

```text
BUSINESS_LINEAGE_COVERAGE != SEARCH_DISCOVERY_COVERAGE
```

### Gates

```text
MATERIAL_BUSINESS_DIRECTION_WITHOUT_DISCOVERY_ROUTE = 0
HIGH_AMBIGUITY_ROUTE_WITHOUT_REFINEMENT_OR_CONTROL = 0
SEARCH_QUALITY_QA = PASS
```

---

## F02 — seed/probe treated as final keyword or truth

### Root cause

The acquisition instrument is promoted into the final semantic object merely because it was selected for provider execution.

### Why it fails

A broad or ambiguous seed may be excellent for discovery while being unsuitable as a final keyword, intent label or page target.

### Universal rule

```text
SEED != FINAL KEYWORD
SEED != FINAL INTENT
SEED != FINAL PAGE
```

### Gates

```text
SEED_WITHOUT_NAMED_INFORMATION_PURPOSE = 0
SEED_SELECTION_USED_AS_FINAL_RELEVANCE_PROOF = 0
```

---

## F03 — provider success mistaken for durable project completion

### Root cause

Transport/API success, visible chat output, HTTP success or terminal provider state is treated as sufficient evidence persistence.

### Why it fails

The next context cannot reproduce facts that were not durably persisted with provenance; summaries/counts cannot reconstruct lost rows.

### Universal rule

```text
PROVIDER_SUCCESS != DURABLE FEED_FORWARD COMPLETION
```

Required order:

```text
receive complete result
-> persist complete required body
-> persist request/provenance identity
-> remote readback
-> row/count/field reconciliation
-> only then next provider action
```

### Gates

```text
TERMINAL_PROVIDER_ITEMS = AUTHORIZED_PROVIDER_ITEMS
DURABLE_LOSSLESS_ITEMS = AUTHORIZED_PROVIDER_ITEMS
REMOTE_READBACK = PASS
CHAT_ONLY_RAW_EVIDENCE = 0
```

---

## F03A — destructive normalization / deduplication

### Root cause

Normalization optimizes row reduction instead of semantic identity and provenance preservation.

### Why it fails

Digits, punctuation, word order or morphology may change referent/intent. Merging uncertain variants destroys evidence and makes later correction impossible.

### Universal rule

- normalize conservatively;
- exact duplicate collapse is analytical, not evidence deletion;
- implicit duplicates require high-confidence equivalence;
- uncertain equivalence remains separate/HOLD;
- RAW text and lineage stay recoverable.

### Gates

```text
RAW_LINEAGE_LOSS = 0
UNEXPLAINED_IMPLICIT_COLLAPSE = 0
ORIGINAL_TEXT_RECOVERABLE = true
```

---

## F03B-1 — unsafe lexical shortcut / substring-prefix overreach

### Root cause

Short prefixes, stems, substrings or regex fragments are used as semantic proof because they are convenient implementation shortcuts.

### Why it fails

Different lexemes can share characters; a token can have multiple referents; lexical resemblance does not prove user intent.

### Universal rule

```text
STRING PREFIX SIMILARITY != SAME LEXEME
SAME LEXEME != SAME REFERENT
TOKEN MATCH != USER INTENT
```

Use bounded tokens, verified morphology or explicit contextual evidence. Broad stems may be discovery signals but cannot be destructive proof unless collision safety is demonstrated.

### Gates

```text
UNBOUNDED_STEM_USED_AS_DESTRUCTIVE_PROOF = 0
KNOWN_PREFIX_COLLISION_REGRESSIONS = PASS
AMBIGUOUS_COLLISION_FORCED_TO_FINAL_STATE = 0
```

---

## F03B-2 — positive business vocabulary overrides explicit foreign context

### Root cause

The classifier assumes that presence of a product/business token is stronger than evidence of a foreign referent.

### Why it fails

The same word can occur in games, media, vehicle models/parts, people, places, organizations or unsupported products.

### Universal rule

```text
POSITIVE BUSINESS TOKEN
DOES NOT OVERRIDE
EXPLICIT FOREIGN CONTEXT
```

If business and foreign interpretations both remain plausible, use HOLD rather than forced KEEP/EXCLUDE.

### Gates

```text
FOREIGN_CONTEXT_GUARDS = PASS
BUSINESS_TOKEN_ONLY_KEEP_WITH_CONTRADICTING_CONTEXT = 0
```

---

## F03B-3 — mechanical/accounting QA mistaken for semantic QA

### Root cause

The same producer verifies its own counts/schema and a high self-score is treated as proof that semantic rules are correct.

### Why it fails

A deterministic system can be perfectly reproducible and consistently wrong.

### Universal rule

```text
ACCOUNTING_QA != SEMANTIC_QA
SELF_SCORE != INDEPENDENT ACCEPTANCE
```

High-volume semantic steps require adversarial checks using a method that is not equivalent to the production classifier.

### Gates

```text
MECHANICAL_ACCOUNTING = PASS
INDEPENDENT_SEMANTIC_DIAGNOSTIC = PASS where applicable
OPEN_CRITICAL_SEMANTIC_DEFECTS = 0
```

---

## F03B-4 — uncertainty destroyed prematurely

### Root cause

The pipeline is optimized for a clean binary output too early, so ambiguous rows are forced into KEEP or EXCLUDE before enough evidence exists.

### Why it fails

Early lexical evidence cannot reliably resolve mixed referents, user tasks or SERP intent.

### Universal rule

```text
CLEAR OFF-TOPIC -> EXCLUDE
DIRECT BUSINESS-SUPPORTED -> KEEP CANDIDATE
MATERIAL AMBIGUITY -> HOLD / LATER EVIDENCE
```

Frequency or commercial delivery caps never resolve semantic ambiguity.

### Gates

```text
LOW_FREQUENCY_ONLY_EXCLUSIONS = 0
HIGH_FREQUENCY_ONLY_KEEPS = 0
AMBIGUOUS_SILENT_EXCLUSIONS = 0
DELIVERY_CAP_USED_AS_RELEVANCE_RULE = false
```

---

## F04-1 — aggregate family counts without row/occurrence reproducibility

### Root cause

Only summaries are materialized because aggregate reconciliation appears sufficient.

### Why it fails

A later audit cannot prove which exact identity/occurrence produced a family total or reproduce rule changes.

### Universal rule

Every family-triage pass must publish deterministic mapping:

```text
occurrence_identity
-> normalized_identity
-> upstream state
-> preliminary family/task state
-> assignment reason
```

### Gates

```text
OCCURRENCE_LEDGER_ROWS = TOTAL_OCCURRENCES
UNIQUE_OCCURRENCE_IDS = TOTAL_OCCURRENCES
UNASSIGNED_OCCURRENCE_IDS = 0
UNEXPECTED_DUPLICATE_OCCURRENCE_IDS = 0
FAMILY_COUNT_RECONCILIATION = PASS
```

---

## F04-2 — representative examples patched instead of the underlying rule

### Root cause

Known bad rows are treated as the correction target rather than evidence of a systematic producer defect.

### Why it fails

Sibling rows affected by the same rule remain wrong, and the apparent fix does not generalize.

### Universal rule

```text
REPRESENTATIVE DEFECT EXAMPLE != PATCH TARGET
REPRESENTATIVE DEFECT EXAMPLE = REGRESSION TEST FOR A RULE FAILURE
```

Correction order:

```text
identify mechanism
-> define blast radius
-> fix producer/rule
-> rerun complete affected universe
-> regression-test known examples
-> report sibling changes
```

### Gates

```text
RULE_LEVEL_FIX_DOCUMENTED = true
FULL_AFFECTED_UNIVERSE_REPROCESSED = true
KNOWN_DEFECT_EXAMPLES_PASS = true
MANUAL_KNOWN_ROW_PATCH_ONLY = false
```

---

## F04-3 — upstream authority changes not propagated downstream

### Root cause

A downstream PASS is treated as immutable even when its semantic input authority materially changes.

### Why it fails

Family, queue, clustering or page decisions can remain logically based on superseded states.

### Universal rule

```text
MATERIAL_UPSTREAM_CHANGE
-> downstream dependency reconciliation
-> invalidate affected conclusions
-> semantic rerun where needed
-> re-accept before continuing
```

### Gates

```text
AFFECTED_DOWNSTREAM_ARTIFACTS_IDENTIFIED = true
STALE_DOWNSTREAM_AUTHORITY_USED = 0
MAIN_RETURN_QA_AFTER_REQUIRED_RERUN = PASS
```

---

## F04-4 — first-match rule ordering erases a more informative explicit task

### Root cause

A classifier uses ordered early returns. A broad topic/context rule fires before a more specific action, object or user-task signal.

### Why it fails

Natural-language queries are multidimensional. Topic, referent, action, commercial modifier and content/task type can coexist. First rule wins is an implementation artifact, not a semantic principle.

### Universal rule

```text
BROAD TOPIC CONTEXT MUST NOT ERASE A MORE INFORMATIVE EXPLICIT USER TASK
```

Before terminal assignment, collect materially relevant signals or use an explicit specificity/precedence contract. Preserve secondary context as metadata.

### Gates

```text
EXPLICIT_TASK_HIDDEN_BY_BROADER_TOPIC = 0
RULE_PRECEDENCE_CONTRACT = PRESENT
SIMULTANEOUS_SIGNAL_REGRESSION = PASS
FINAL_INTENT_INFERRED_PREMATURELY = false
```

---

## F04-5 — generic fallback hides an unmodelled coherent user task

### Root cause

The taxonomy is treated as closed. Anything that does not match known branches falls into a generic family, even when the phrase contains a repeated coherent action/task not represented in the taxonomy.

### Why it fails

The classifier confirms its own ontology instead of discovering missing dimensions in the data.

### Universal rule

```text
GENERIC FALLBACK != PROOF OF UNQUALIFIED USER TASK
```

Large generic families require independent heterogeneity/task discovery. Repeated explicit actions must become at least a preliminary task marker/family when materially coherent.

### Gates

```text
LARGE_GENERIC_FAMILY_HETEROGENEITY_AUDIT = PASS
REPEATED_EXPLICIT_TASK_PATTERN_HIDDEN_IN_GENERIC = 0
UNKNOWN_TASK_DISCOVERY_ROUTE = PRESENT
```

---

## F04-6 — hand-built taxonomy accepted without independent discovery-oriented challenge

### Root cause

The same lexical taxonomy both produces families and defines the tests used to validate them.

### Why it fails

Missing families or misplaced rows outside the predefined vocabulary can remain invisible.

### Universal rule

For high-volume preliminary semantic grouping, add an independent diagnostic that does not simply replay ordered production rules. Examples include term/co-occurrence analysis, semantic embeddings, topic decomposition, cross-family centroid/similarity diagnostics or stratified human review. Diagnostic output is not final SERP clustering.

### Gates

```text
INDEPENDENT_FAMILY_COHERENCE_DIAGNOSTIC = PASS
LARGE_FAMILIES_CHALLENGED_FOR_HIDDEN_SUBTASKS = true
DIAGNOSTIC_NOT_MISUSED_AS_FINAL_SERP_CLUSTERING = true
```

---

## F05-1 — coverage-gap queue duplicates already durable evidence

### Root cause

A local family-level gap is declared without reconciling it against the full prior acquisition/evidence history.

### Why it fails

The pipeline can spend provider calls re-measuring a question already answered under another seed, earlier step or historical durable request.

### Universal rule

```text
LOCAL COVERAGE GAP HYPOTHESIS
MUST BE RECONCILED AGAINST
ALL CURRENT DURABLE EVIDENCE
BEFORE PROVIDER AUTHORIZATION
```

A new probe must have explicit incremental information gain and a negative-result value.

### Gates

```text
PROVIDER_READY_QUEUE_WITH_EQUIVALENT_EXISTING_EVIDENCE = 0
PROBE_LITERAL_DUPLICATES = 0
PROBE_SEMANTIC_DUPLICATES_WITHOUT_OPERATOR_OR_SCOPE_GAIN = 0
INCREMENTAL_INFORMATION_GAIN_EXPLICIT = true
```

---

## F05-2 — owner/business fact gap sent to a search provider

### Root cause

The pipeline asks demand/search evidence to establish inventory, product form, service availability, legal/claim boundaries or another fact only the client/business can authoritatively provide.

### Why it fails

Search behavior cannot turn an unknown business fact into truth.

### Universal rule

```text
SEARCH DEMAND EVIDENCE != CLIENT BUSINESS FACT
```

### Gates

```text
OWNER_FACT_GATED_SENT_TO_PROVIDER = 0
UNSUPPORTED_INVENTORY_OR_CLAIM_INFERENCE = 0
```

---

## F06+ — final clustering/page decisions made from preliminary lexical families

### Root cause

Early topical grouping is mistaken for page-level SEO clustering because the labels look coherent.

### Why it fails

One topical family can contain multiple user intents/pages, while lexically different queries can share the same SERP/user task.

### Universal rule

```text
PRELIMINARY FAMILY != FINAL SEO CLUSTER
TERM SIMILARITY != QUERY->PAGE OWNERSHIP
```

Final page-level decisions require governed later evidence, including user task/intent and current SERP overlap where the roadmap specifies it.

### Gates

```text
PRELIMINARY_FAMILY_USED_AS_FINAL_PAGE_CLUSTER = 0
FINAL_PAGE_OWNERSHIP_BEFORE_SERP_STAGE = 0
```

---

## Universal anti-regression procedure

Every later step must materialize a known-failure regression matrix containing at least:

```text
failure_class
root_cause_relevant_to_current_step
regression_test
result
blocking_if_fail
```

Before execution:

```text
READ THIS FILE
-> identify applicable failure mechanisms
-> map them to current step gates
-> add novel job-specific examples only in work/<JOB_ID>/
-> execute
```

## PASS policy

A step may be accepted only if:

```text
METHOD_RULES = PASS
FULL_VOLUME_ACCOUNTING = PASS where applicable
SEMANTIC_QA = PASS where applicable
KNOWN_FAILURE_REGRESSION_MATRIX = PASS
PERSISTENCE_AND_REMOTE_READBACK = PASS where applicable
OPEN_CRITICAL_DEFECTS = 0
```

Quality scores never override a failed hard gate.
