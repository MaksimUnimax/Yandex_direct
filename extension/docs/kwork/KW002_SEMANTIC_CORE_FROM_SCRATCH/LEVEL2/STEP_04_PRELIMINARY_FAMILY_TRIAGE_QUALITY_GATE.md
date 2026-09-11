# KW-002 — LEVEL 2 STEP 04 PRELIMINARY FAMILY TRIAGE QUALITY GATE

Status: **ACTIVE / UNIVERSAL / REQUIRED FOR ANY KW-002 SITE**

Companion authorities:

- `../LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`
- `../LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `../LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`

## 1. Purpose

Step04 creates a **preliminary map of demand/topic/task families** from the sanitized semantic universe so later expansion, detailed relevance review and SERP clustering know where evidence is strong, ambiguous, heterogeneous or missing.

Step04 is deliberately not final SEO clustering.

```text
PRELIMINARY FAMILY != FINAL INTENT
PRELIMINARY FAMILY != SERP CLUSTER
PRELIMINARY FAMILY != QUERY->PAGE OWNERSHIP
PRELIMINARY FAMILY != SITE IA
```

## 2. Input contract

Step04 reads:

```text
SANITIZED KEEP-CANDIDATE identities
+ HOLD/AMBIGUOUS identities where family context is useful
+ complete lineage/provenance locators
+ frozen business/scope facts
```

High-confidence excluded history remains available for accounting/audit but is not silently re-triaged as active demand.

RAW occurrences are audit/provenance evidence, not the semantic unit the analyst must independently classify one by one.

## 3. Why this step exists

A normalized/sanitized pool can still contain thousands of phrases with:

- multiple user-task directions;
- broad topical groups;
- ambiguous referents;
- hidden missing subtopics;
- business facts that need clarification;
- coverage gaps caused by initial seed choice.

Step04 makes those structures visible before expensive downstream stages.

## 4. Universal failure mechanisms this step must prevent

### 4.1 First-match precedence bias

Root cause:

A broad topic rule executes before a more informative action/task/object signal.

Control:

```text
BROAD TOPIC CONTEXT MUST NOT ERASE MORE INFORMATIVE EXPLICIT TASK
```

Collect simultaneous signals where practical or apply an explicit specificity/precedence contract.

### 4.2 Closed taxonomy / generic fallback bias

Root cause:

The classifier assumes all meaningful tasks are already represented. New coherent task patterns fall into a generic bucket.

Control:

Large generic families must receive independent heterogeneity/task discovery. Repeated explicit action patterns require at least a preliminary marker or new family when materially coherent.

### 4.3 Lexical shortcut bias

Root cause:

Prefixes/stems/substrings are used as semantic proof.

Control:

Bound lexical evidence and regression-test sibling lexemes/collisions.

### 4.4 Producer validates itself

Root cause:

The same rules create families and then pass only their own count/schema tests.

Control:

Use a second independent diagnostic that does not simply replay the production classifier.

### 4.5 Family label mistaken for final page decision

Root cause:

A coherent preliminary label looks like a ready SEO cluster.

Control:

Every family authority must mark intent/page status as NOT FINAL and preserve the later SERP evidence requirement.

## 5. Family representation

A family should preserve separate dimensions where useful:

```text
primary topic/context
primary user-task hypothesis
business relevance confidence
family coherence confidence
ambiguity class
final intent status = NOT_FINAL at Step04
SERP cluster status = NOT_STARTED at Step04
coverage state
later evidence needed
```

Do not force one scalar label to carry all semantic dimensions.

## 6. Allowed preliminary outcomes

Generic states may include:

```text
STRONG_BUSINESS_SUPPORT
PLAUSIBLE_BUSINESS_SUPPORT
MIXED_OR_AMBIGUOUS
COLLISION_OR_FOREIGN_REFERENT_REVIEW
RESIDUAL_QUARANTINE
COVERAGE_GAP_HYPOTHESIS
OWNER_FACT_REQUIRED
LATER_SERP_OR_INTENT_EVIDENCE_REQUIRED
```

The exact family taxonomy is job-derived; it is NOT universal and must not be hard-coded in Level2.

## 7. Independent family-coherence diagnostic

For materially large or rule-heavy family triage, Step04 must challenge the production taxonomy using at least one independent method that is not equivalent to the ordered classifier.

Possible diagnostics:

```text
term/co-occurrence analysis
TF-IDF topic decomposition
semantic embeddings
cross-family centroid/similarity checks
stratified manual review
explicit-task signal census
rare-subtopic discovery
```

Diagnostic results are warnings/evidence, not final page clustering.

No single clustering metric becomes ground truth.

## 8. Large-family requirement

Large generic, residual or ambiguity families must receive explicit heterogeneity review.

For each such family ask:

```text
Does it contain repeated coherent user actions/tasks hidden by the current taxonomy?
Does a broad context rule suppress a stronger signal?
Are there foreign-referent collision subgroups?
Is the family deliberately heterogeneous/quarantined, or accidentally so?
Could downstream code misread it as one final intent/page?
```

## 9. Occurrence-level reproducibility

Every active semantic identity receives exactly one preliminary primary family/task state for accounting, while secondary signals may be stored as metadata.

Publish deterministic lineage:

```text
raw occurrence
-> normalized identity
-> upstream sanitation state/reason
-> Step04 primary family
-> assignment reason
-> secondary signals / ambiguity / later evidence
```

Required:

```text
RAW_LINEAGE_LOSS = 0
UNASSIGNED_ACTIVE_IDENTITIES = 0
DUPLICATE_PRIMARY_ASSIGNMENTS = 0
OCCURRENCE_ACCOUNTING_RECONCILES = true
```

## 10. Sanitation feedback

If Step04 finds a systematic row class that appears mis-sanitized upstream:

- record a feedback class;
- do not silently mutate the upstream Step03B authority inside Step04;
- distinguish “family-routing defect” from “upstream sanitation defect”.

Step04 may expose an issue without claiming authority to rewrite the earlier step.

## 11. Coverage-gap / expansion queue

A Step04 coverage gap is a hypothesis, not provider authorization.

Every gap must state:

```text
what business/search direction appears missing
what current evidence exists
what exact uncertainty remains
whether the missing fact is a CLIENT/OWNER FACT or SEARCH-DEMAND question
what evidence route could resolve it
```

Before any later provider call, reconcile the gap against all durable acquisition history.

```text
LOCAL FAMILY GAP != NEW PROVIDER CALL AUTHORIZATION
```

## 12. Queue safety classes

A later queue gate should distinguish generically:

```text
VALID_INCREMENTAL_SEARCH_GAP
OWNER_FACT_FIRST
EXISTING_EVIDENCE_REUSE
DUPLICATE_OR_LOW_INFORMATION_PROBE
DEFER_TO_LATER_INTENT_OR_SERP
```

No fixed counts are universal.

## 13. Full-volume correction rule

If independent audit finds a systematic family defect:

```text
known bad rows = regression oracle
NOT patch list
```

Correction must:

```text
identify root cause
fix underlying rule/taxonomy/precedence
rerun complete affected semantic universe
rematerialize family/queue/feedback authorities
run old + new regressions
run independent post-correction diagnostic
```

## 14. QA

Minimum hard gates:

```text
FULL_ACTIVE_HOLD_UNIVERSE_PROCESSED = true
RAW_LINEAGE_LOSS = 0
PRELIMINARY_FAMILY_NOT_FINAL_CLUSTER = true
EXPLICIT_TASK_HIDDEN_BY_BROAD_TOPIC = 0
KNOWN_LEXICAL_COLLISIONS = 0
REPEATED_COHERENT_TASK_HIDDEN_IN_GENERIC = 0
LARGE_FAMILY_HETEROGENEITY_AUDIT = PASS
INDEPENDENT_FAMILY_DIAGNOSTIC = PASS
COVERAGE_GAP_REQUIRES_LATER_RECONCILIATION = true
OWNER_FACT_GAP_NOT_LABELLED_SEARCH_GAP = true
UPSTREAM_STATE_MUTATIONS_INSIDE_STEP04 = 0 unless a separately authorized upstream correction is the task
KNOWN_FAILURE_REGRESSION_MATRIX = PASS
```

## 15. Output

Step04 produces generic authority classes equivalent to:

```text
PRELIMINARY_FAMILY_AUTHORITY
OCCURRENCE_TO_FAMILY_LEDGER
TARGETED_EXPANSION_QUEUE
SANITATION_FEEDBACK_REGISTER
FAMILY_COHERENCE / BOUNDARY QA
KNOWN_FAILURE_REGRESSION_MATRIX
```

Exact filenames and taxonomy IDs are job-specific.

## 16. PASS

Step04 may PASS only if:

```text
METHOD_BOUNDARY = PASS
FULL_VOLUME_ACCOUNTING = PASS
FAMILY_BOUNDARY_QA = PASS
INDEPENDENT_DIAGNOSTIC = PASS
KNOWN_FAILURE_REGRESSIONS = PASS
OPEN_CRITICAL_RULE_DEFECTS = 0
QUEUE_SAFETY = PASS
REMOTE_READBACK = PASS for durable outputs
```

A high self-score never overrides a failed semantic regression.
