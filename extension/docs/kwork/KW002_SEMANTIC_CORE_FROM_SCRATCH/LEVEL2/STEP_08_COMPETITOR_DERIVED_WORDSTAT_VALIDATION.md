# KW-002 — LEVEL 2 / STEP 08 COMPETITOR-DERIVED WORDSTAT VALIDATION

Status: **ACTIVE / UNIVERSAL / MANDATORY FOR STEP08**  
Created: 2026-09-18  
Applies to: every KW-002 job that reaches competitor-derived demand validation.

Companion authorities:

- `STEP_RULES_INDEX.md`;
- `../LEVEL1/COMMON_RULES.md`;
- `../LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`;
- `../LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md`;
- `../LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`;
- `STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`;
- `STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`;
- `STEP_05_TARGETED_EXPANSION_AND_PROVIDER_EXECUTION_GATE.md`;
- `YANDEX_MARKETING_BRIDGE_PROVIDER_EXECUTION_GATE.md`.

This is a universal step rule. Client names, exact phrases, request IDs, counts,
costs, job IDs and current statuses belong in `work/<JOB_ID>/`.

---

## 0. Purpose and hard boundary

Step08 validates and expands genuinely new competitor-derived directions against
current Yandex demand evidence.

```text
COMPETITOR-DERIVED CANDIDATE != PRODUCTION KEYWORD
COMPETITOR PAGE TOPIC != PROVEN DEMAND
WORDSTAT DEMAND != FINAL RELEVANCE
WORDSTAT DEMAND != FINAL INTENT
WORDSTAT DEMAND != SERP CLUSTER
WORDSTAT DEMAND != PAGE
```

Step08 MUST NOT perform final intent, final clustering, query→page ownership,
site architecture, URL/H1/Title decisions or Step09+ finalization.

---

## 1. Entry gate

Step08 may enter preparation only when:

```text
CURRENT_REMOTE_BASE_FETCHED = true
STEP07_ACCEPTED = true
STEP07_ELIGIBLE_CANDIDATE_UNIVERSE_FROZEN = true
STEP07_RAW_PROVENANCE_IMMUTABLE = true
CURRENT_WORDSTAT_METHOD_RESEARCH = PASS
CURRENT_BRIDGE_CONTRACT_VERIFIED = true
CURRENT_WORDSTAT_DEPTH_GATE_READ = true
CURRENT_RAW_PERSISTENCE_GATE_READ = true
CURRENT_PROVIDER_EXECUTION_GATE_READ = true
```

If Step07 has a declared source limitation, that limitation remains explicit and
is not silently repaired or erased by Step08.

---

## 2. Step08 has two different phases

### Phase A — pre-acquisition reconciliation

Before any provider call:

```text
STEP07 ELIGIBLE CANDIDATES
-> RECONCILE AGAINST ALL CURRENT DURABLE DEMAND EVIDENCE
-> DEFINE OPEN INFORMATION QUESTIONS
-> REUSE EXACTLY MATCHING EVIDENCE
-> DESIGN ONLY GENUINELY NEW ACQUISITION QUESTIONS
-> BUILD DEPENDENCY-AWARE PROVIDER QUEUE
```

### Phase B — provider execution and evidence reconciliation

Only after Phase A is accepted:

```text
RELEASE ONE PERMITTED PROVIDER ACTION
-> RECEIVE ACTUAL RESULT
-> PERSIST COMPLETE RAW
-> REMOTE READBACK
-> RECONCILE
-> ONLY THEN NEXT PROVIDER ACTION
```

Preparation PASS does not equal provider execution PASS.

---

## 3. Reuse-first requirement

Every competitor-derived candidate must first be reconciled against durable
current-job evidence.

Classify evidence scope at least as:

```text
EXACT_QUESTION_ANSWERED
QUALIFIED_QUESTION_ANSWERED
RELATED_BUT_INSUFFICIENT
NO_DURABLE_EVIDENCE_FOUND
NOT_APPLICABLE
```

Hard rules:

```text
BROAD EVIDENCE != QUALIFIED QUESTION ANSWER
RELATED EVIDENCE != CLOSURE
SAME TEXT != AUTOMATIC SAME EVIDENCE QUESTION
```

Reuse requires a durable locator and a written scope-match explanation.

---

## 4. Acquisition-question identity

A provider seed exists to answer an explicit information question.

Every provider seed must have:

```text
acquisition_question_id
open_information_question
member_candidate_ids
incremental_information_gain
research_mode
operator_shape
depth
outcome_contract
release_state
```

Literal phrase uniqueness is not enough.

```text
UNIQUE PHRASE != UNIQUE INFORMATION QUESTION
```

---

## 5. Parent/child dependency rule

Before provider release, model whether a broader/parent probe can answer a
narrower child question.

Allowed release states:

```text
INITIAL_REQUIRED
INDEPENDENT_REQUIRED
CONDITIONAL_AFTER_PARENT
REUSE_EXISTING_EVIDENCE
HOLD
```

If a parent may answer a child:

```text
PARENT EXECUTES FIRST
-> COMPLETE RAW PERSISTENCE / READBACK
-> RECONCILE PARENT RESULT AGAINST CHILD QUESTION
-> CHILD STILL UNANSWERED?
   YES -> child may receive a later release
   NO  -> child is cancelled as unnecessary
```

A child must never be unconditionally pre-authorized merely because its literal
phrase differs.

For several seeds sharing one declared information question, Step08 must do one
of:

1. merge them into one sufficient probe;
2. document distinct operator/scope/referent information gain;
3. make narrower probes conditional on a parent.

---

## 6. Acquisition grouping is not SEO clustering

An acquisition group means only that one provider observation can answer a
shared demand question for multiple candidate identities.

It does NOT mean those candidates:

- share final intent;
- belong on one page;
- form one SEO cluster;
- are synonyms;
- should be merged as semantic identities.

Every candidate remains independently traceable.

---

## 7. Research modes and operators

Every provider probe must be classified as:

```text
DISCOVERY_RECALL_FIRST
PRECISION_VALIDATION
EXACT_FORM_TEST
COLLISION_DIAGNOSTIC
```

Operator shape follows the information question.

No universal shortcut such as:

```text
ALWAYS USE !
ALWAYS USE QUOTES
ALWAYS USE OR
NEVER USE OPERATORS
```

is allowed.

Grouped OR is allowed only when the grouped terms serve one coherent
information question and do not hide distinct referents.

---

## 8. Depth

Depth is governed by
`STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`.

Every provider seed or homogeneous execution class must record:

```text
candidate_depth_options
selected_depth
why selected
why alternatives rejected
boundary interpretation
cost/request effect
```

```text
PROVIDER MAXIMUM != SEMANTIC COMPLETENESS
DEPTH BOUNDARY HIT != MARKET SATURATION
```

---

## 9. Provider outcome contract

Before release, every seed must define:

```text
SUCCESS_WITH_ROWS
SUCCESS_WITH_ZERO_ROWS
SUCCESS_BUT_EVIDENCE_INCOMPLETE
VALIDATION_FAILURE
PROVIDER_FAILURE
OUTCOME_UNKNOWN
```

Hard rules:

```text
NO_RETRY != NEGATIVE EVIDENCE
ZERO ROWS != UNIVERSAL ZERO DEMAND
TECHNICAL FAILURE != SEMANTIC NEGATIVE
```

---

## 10. Provider execution

Execution uses the current accepted YMB contract.

For Manual mode:

```text
ONE STANDALONE CODE BLOCK
-> ONE BRIDGE COMMAND
-> OWNER/USER TRIGGERS YANDEX ACTION
-> ACTUAL *_RESULT_V1 REQUIRED
```

A printed command is preparation only.

Provider calls may never be inferred from expected results.

---

## 11. RAW persistence and downstream transformation

Every actual Wordstat response inherits
`STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md` in full:

```text
ACTUAL RESULT
-> COMPLETE RAW RESULT + ERROR TRUTH
-> RECEIPT / REQUEST PROVENANCE
-> REMOTE GITHUB READBACK
-> RECONCILIATION
-> ONLY THEN NEXT PROVIDER REQUEST
```

New provider rows then return through:

```text
STEP03A-COMPATIBLE NORMALIZATION
-> STEP03B-COMPATIBLE SANITATION
-> STEP08 CANDIDATE RECONCILIATION
```

RAW provider rows never enter accepted semantic authority directly.

---

## 12. Dynamic queue reconciliation

A provider queue is not permanently immutable once new evidence arrives.

After a parent/wave/bounded execution unit produces new durable evidence:

```text
NEW EVIDENCE
-> RECHECK PENDING INFORMATION QUESTIONS
-> CANCEL QUESTIONS NOW ANSWERED
-> KEEP ONLY STILL-JUSTIFIED REQUESTS
-> RELEASE NEXT WAVE
```

Do not execute a stale child queue merely because it was prepared earlier.

---

## 13. Large-data rule

If complete candidate/evidence reconciliation is too large for ordinary chat:

```text
LARGE DATA
!= SAMPLE IT
!= FIRST N
!= SUMMARY IN PLACE OF ANALYSIS

-> COMPLETE BOUNDED UNIT IN CHATGPT WORK
```

Work executes the frozen contract; Main Chat owns method, release and
acceptance.

---

## 14. Required outputs

Before provider execution, the job must materialize:

```text
candidate pre-acquisition reconciliation
existing-evidence reuse register
acquisition-question register
provider seed manifest
parent/child dependency + release-state mapping
known-failure regression matrix
pre-acquisition QA
execution release
```

After provider execution:

```text
complete RAW provider results
receipts/provenance
remote readback evidence
normalization/sanitation outputs
Step08 reconciliation/closure
```

---

## 15. Pre-acquisition PASS

PASS requires:

```text
FULL_ELIGIBLE_CANDIDATE_ACCOUNTING = PASS
SILENT_SKIP = 0
REUSE_ROWS_WITHOUT_DURABLE_LOCATOR = 0
BROAD_EVIDENCE_USED_TO_CLOSE_NARROWER_QUESTION = 0
PROVIDER_SEEDS_WITHOUT_INFORMATION_GAIN = 0
PROVIDER_SEEDS_WITHOUT_ACQUISITION_QUESTION_ID = 0
DUPLICATE_INFORMATION_QUESTIONS_WITHOUT_MERGE_OR_JUSTIFICATION = 0
UNCONDITIONAL_CHILD_PROBES_WHERE_PARENT_MAY_ANSWER = 0
CONDITIONAL_CHILD_WITHOUT_TRIGGER = 0
PROVIDER_SEEDS_WITHOUT_OPERATOR_RATIONALE = 0
PROVIDER_SEEDS_WITHOUT_DEPTH_RATIONALE = 0
PROVIDER_SEEDS_WITHOUT_OUTCOME_CONTRACT = 0
PROVIDER_EXECUTION_RELEASED_PREMATURELY = 0
KNOWN_FAILURE_REGRESSION_MATRIX = PASS
```

---

## 16. Final Step08 PASS

Step08 is complete only when all released provider work is terminal and:

```text
ALL_EXECUTED_RESULTS_PERSISTED_AND_READ_BACK = true
OUTCOME_UNKNOWN_UNRESOLVED = 0
ALL_NEW_ROWS_NORMALIZED_AND_SANITIZED = true
CANDIDATE_RECONCILIATION_COMPLETE = true
PENDING_CONDITIONAL_CHILDREN_RESOLVED_OR_GOVERNED = true
VALID_PENDING_PROVIDER_QUESTIONS = 0
OPEN_CRITICAL_STEP08_DEFECTS = 0
```

Only then may Step09 preparation begin.

---

## 17. Plain-language universal rule

Do not buy a new Wordstat request merely because a competitor produced a new
phrase. First prove that old evidence does not already answer the question.
Then ask the broadest safe question that can answer it. If that broad answer may
make narrower questions unnecessary, run it first and decide on the children
only after the result is safely stored and reconciled.
