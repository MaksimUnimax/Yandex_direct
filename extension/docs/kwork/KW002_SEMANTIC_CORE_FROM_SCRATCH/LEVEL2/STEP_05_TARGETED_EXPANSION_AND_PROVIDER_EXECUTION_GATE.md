# KW-002 — LEVEL 2 / STEP 05 TARGETED EXPANSION AND PROVIDER EXECUTION GATE

Status: **ACTIVE / UNIVERSAL / MANDATORY FOR STEP05 / ANTI-REGRESSION AUTHORITY**  
Created: 2026-09-12  
Applies to: every KW-002 job that reaches Step05 targeted expansion / coverage control.

Companion authorities:

- `STEP_RULES_INDEX.md`
- `STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`
- `STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`
- `../LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `../LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `../LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md`
- `../LEVEL1/WORK_HANDOFF_RULE.md`
- `../LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`

This file is universal. It MUST NOT contain current client names, product names, current query strings, current candidate IDs, current row counts or current provider request IDs. Those belong in `work/<JOB_ID>/`.

---

# 0. Purpose

Step05 exists to close **material search-vocabulary coverage gaps** revealed by earlier evidence without turning acquisition into recursive re-querying.

A valid Step05 does not merely ask whether another provider call is technically possible. It must prove that a new call has a bounded unresolved question, cannot already be answered from durable evidence, has incremental information value, has a safe execution/outcome contract, and will feed back through the existing normalization/sanitation pipeline before becoming accepted semantic evidence.

Hard invariants:

```text
PRE_ACQUISITION_ACCEPTED != STEP05_COMPLETE
PROVIDER_SUCCESS != SEMANTIC_ACCEPTANCE
NO_RETRY != NEGATIVE_EVIDENCE
PROVIDER_MAXIMUM != SEMANTIC_COMPLETENESS
BROAD EVIDENCE != QUALIFIED QUESTION ANSWER
TEMPORAL SNAPSHOT != PERMANENT TRUTH
RAW PROVIDER ROW != ACCEPTED SEMANTIC ROW
WORK != DEFAULT FOR SMALL DOCUMENTATION / GATE WORK
```

---

# 1. Step05 state model

Step05 MUST distinguish preparation, provider execution, persistence, downstream processing and final acceptance.

Minimum state model:

```text
STEP05_PRE_ACQUISITION_RECONCILIATION_PENDING
STEP05_PRE_ACQUISITION_ACCEPTED
STEP05_PROVIDER_EXECUTION_PENDING
STEP05_PROVIDER_RESULT_RECEIVED
STEP05_PROVIDER_EVIDENCE_PERSISTENCE_PENDING
STEP05_PROVIDER_EVIDENCE_PERSISTED
STEP05_NORMALIZATION_SANITATION_PENDING
STEP05_RECONCILIATION_PENDING
STEP05_ACCEPTED
```

Equivalent repository-specific names are allowed, but the distinctions are mandatory.

A pre-acquisition review cannot be represented as final Step05 completion while an unresolved provider candidate remains open.

Final Step05 acceptance requires every material Step05 branch to be one of:

```text
CLOSED_FOR_CURRENT_RESEARCH_SNAPSHOT
DEFERRED_TO_NAMED_LATER_STEP_WITH_REASON
ACQUIRED_PERSISTED_NORMALIZED_SANITIZED_RECONCILED
```

---

# 2. Mandatory candidate contract before any provider release

Every new Step05 provider candidate MUST record all of the following before execution:

```text
candidate identity
exact unresolved question
source gap / source hypothesis
why current durable evidence does not answer the question
scope difference from prior probes/evidence
expected incremental information gain
what SUCCESS_WITH_ROWS would change
what SUCCESS_WITH_ZERO_ROWS would change
what technical/incomplete failure would change (normally nothing semantically)
provider/query/operator choice and rationale
recall-vs-precision goal
morphology/exactness decision where applicable
region/device/provider scope
requested depth
depth justification
what shallower alternatives may miss
depth-boundary interpretation
maximum request count
current cost basis if cost is material
stop condition
no-blind-retry rule
raw persistence requirement
remote readback requirement
downstream normalization/sanitation path
reopen/escalation triggers
```

No complete candidate contract = no provider execution release.

---

# 3. Failure F05-01 — local gap duplicates durable evidence

## Failure mechanism

A family/queue gap is declared locally and immediately converted into a new provider probe without reconciling the question against all existing durable acquisition evidence.

## Why dangerous

The project spends requests/cost on a question already answered under another seed, operator shape, earlier step or durable historical acquisition.

## Wrong pattern

```text
LOCAL GAP LABEL -> NEW PROVIDER CALL
```

## Correct rule

```text
LOCAL GAP HYPOTHESIS
-> FULL DURABLE EVIDENCE RECONCILIATION
-> INFORMATION-GAIN TEST
-> ONLY THEN NEW CANDIDATE
```

## Detection / PASS

```text
EQUIVALENT_EXISTING_EVIDENCE_NOT_CHECKED = 0
PROBE_LITERAL_DUPLICATES = 0
PROBE_SEMANTIC_DUPLICATES_WITHOUT_SCOPE_GAIN = 0
INCREMENTAL_INFORMATION_GAIN_EXPLICIT = true
```

---

# 4. Failure F05-02 — owner/business fact sent to demand provider

## Failure mechanism

Search-demand evidence is asked to prove inventory, service availability, geography, product properties, legal claims or another fact whose authority belongs to the client/business.

## Why dangerous

Search behavior cannot create business truth.

## Correct rule

```text
SEARCH DEMAND EVIDENCE != CLIENT / OWNER FACT
```

Owner-fact gaps remain owner/business-evidence questions. They do not become provider candidates merely because Step05 wants closure.

## PASS

```text
OWNER_FACT_GATED_SENT_TO_PROVIDER = 0
UNSUPPORTED_BUSINESS_FACT_INFERRED_FROM_DEMAND = 0
```

---

# 5. Failure F05-03 — pre-acquisition acceptance misrepresented as Step05 completion

## Failure mechanism

Reconciliation/preparation passes, but unresolved provider candidates are still not executed or reconciled; the step is nevertheless called COMPLETE/PASS.

## Why dangerous

Later steps inherit false completeness and may skip unresolved vocabulary branches.

## Correct rule

Use the Step05 state model in section 1. A preparation gate can be PASS while Step05 remains open.

## PASS

```text
UNRESOLVED_PROVIDER_CANDIDATES > 0
=> STEP05_FINAL_COMPLETE = false
```

---

# 6. Failure F05-04 — zero-result and technical failure collapsed into one semantic stop state

## Failure mechanism

A valid provider response with zero rows is treated as equivalent to validation failure, provider/network failure, malformed/incomplete evidence or unknown request outcome.

## Why dangerous

Only a valid complete response answers the bounded measurement question. A technical failure contains no negative semantic evidence.

## Mandatory outcome model

Every executed candidate must resolve to a state at least equivalent to:

```text
SUCCESS_WITH_ROWS
SUCCESS_WITH_ZERO_ROWS
SUCCESS_BUT_EVIDENCE_INCOMPLETE
VALIDATION_FAILURE
PROVIDER_FAILURE
OUTCOME_UNKNOWN
```

Additional transport-specific states may exist, but they cannot erase these semantic distinctions.

## Interpretation

```text
SUCCESS_WITH_ROWS
-> usable provider evidence after persistence/readback

SUCCESS_WITH_ZERO_ROWS
-> bounded negative observation for current request scope/snapshot

SUCCESS_BUT_EVIDENCE_INCOMPLETE
-> branch remains unresolved

VALIDATION_FAILURE
-> branch remains unresolved

PROVIDER_FAILURE
-> branch remains unresolved

OUTCOME_UNKNOWN
-> branch remains unresolved and blind retry forbidden
```

## PASS

```text
TECHNICAL_FAILURE_MAPPED_TO_NEGATIVE_SEMANTIC_EVIDENCE = 0
UNKNOWN_OUTCOME_MAPPED_TO_NEGATIVE_SEMANTIC_EVIDENCE = 0
```

---

# 7. Failure F05-05 — no-retry rule treated as negative evidence

## Failure mechanism

An execution-safety rule saying “do not retry automatically” is interpreted as if the semantic question has been answered negatively.

## Why dangerous

No-retry protects against duplicate billing/double execution when request outcome is uncertain. It says nothing about demand.

## Universal invariant

```text
NO_RETRY != NEGATIVE_EVIDENCE
```

If outcome is failed, unknown or incomplete:

```text
DO NOT BLIND-RETRY
DO NOT CLOSE QUESTION AS NEGATIVE
KEEP BRANCH UNRESOLVED
REQUIRE NEW RECONCILIATION / RELEASE BEFORE ANY FOLLOW-UP
```

## PASS

```text
NO_RETRY_USED_AS_SEMANTIC_CLOSURE = 0
```

---

# 8. Failure F05-06 — provider maximum used as depth justification

## Failure mechanism

The requested depth is chosen because it is the provider maximum, because it was used before, or because “more is safer”.

## Why dangerous

Provider depth is an observation boundary, not proof of market completeness. Different questions require different depths.

## Correct rule

Every materially new Step05 Wordstat acquisition inherits:

`STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`

Required Step05 depth reasoning:

```text
exact information question
candidate depth options
what shallower options may miss
why selected depth is proportionate
request/cost consequence
what boundary saturation would mean
what would trigger another separately released investigation
```

## PASS

```text
SELECTED_DEPTH_JUSTIFIED_BY_INFORMATION_QUESTION = true
PROVIDER_MAXIMUM_USED_AS_SOLE_JUSTIFICATION = false
```

---

# 9. Failure F05-07 — depth boundary misread as semantic completeness

## Failure mechanism

The provider returns exactly the requested depth and the project reports that the semantic universe is complete.

## Why dangerous

The result may be truncated at the chosen boundary.

## Required state

Use an explicit state such as:

```text
DEPTH_BOUNDARY_REACHED
```

when returned result count reaches the requested acquisition boundary and the provider contract does not prove saturation beyond it.

## Universal invariant

```text
RETURNED_ROWS == REQUESTED_DEPTH
!=
SEMANTIC_UNIVERSE_COMPLETE
```

## PASS

```text
BOUNDARY_HIT_HAS_EXPLICIT_TRUNCATION_INTERPRETATION = true
```

---

# 10. Failure F05-08 — query operator / morphology decision left implicit

## Failure mechanism

An operator, morphology fixation, exactness constraint or phrase shape is added/removed because it appears more precise, without tying the choice to the research question.

## Why dangerous

The operator changes recall/precision and therefore changes what evidence is observable.

## Correct rule

For every materially meaningful operator choice record:

```text
research goal
recall requirement
precision requirement
known collision/noise risk
whether morphological variants are wanted
why selected operator shape fits the question
what result pattern would trigger reconsideration
```

No universal operator is correct for all Step05 questions.

General heuristic:

```text
DISCOVERY QUESTION -> often recall-first
VALIDATION / EXACT-FORM QUESTION -> may require greater precision
```

This is a heuristic, not provider truth. The job-specific decision must be explicit.

## PASS

```text
MATERIAL_OPERATOR_CHOICE_WITHOUT_RATIONALE = 0
```

---

# 11. Failure F05-09 — broad evidence used to close a narrower qualified question

## Failure mechanism

Evidence for a broad token/topic is used to prove presence or absence of a more qualified commercial/product/use-case question.

## Why dangerous

Scope mismatch is hidden. Broad evidence may be dominated by informational, cultural, media, entity or other unrelated uses while the qualified question remains unanswered.

## Correct rule

Evidence closes a Step05 question only if the evidence scope actually answers that question.

When scopes differ, use a conclusion equivalent to:

```text
EXISTING_EVIDENCE_DOES_NOT_ANSWER_THIS_QUALIFIED_QUESTION
```

## PASS

```text
BROAD_EVIDENCE_USED_AS_NEGATIVE_PROOF_FOR_NARROWER_QUESTION = 0
```

---

# 12. Failure F05-10 — temporal evidence described as permanent truth

## Failure mechanism

A demand/provider observation is labelled `PERMANENTLY_CLOSED`, `NEVER_REPROBE`, `PERMANENT_NEGATIVE` or equivalent even though demand, assortment, geography, provider behavior and evidence freshness can change.

## Why dangerous

A time-bounded research snapshot is converted into an eternal semantic claim.

## Correct state language

Prefer bounded states such as:

```text
CLOSED_FOR_CURRENT_RESEARCH_SNAPSHOT
IDENTICAL_REPLAY_NOT_AUTHORIZED_IN_CURRENT_ROUND
```

## Mandatory reopen triggers

Every snapshot closure must define applicable triggers such as:

```text
material scope change
material assortment/business-fact change
new owner evidence
planned future refresh/revision
material evidence-freshness expiry
provider/method change
upstream authority invalidation
```

A trigger permits reconsideration; it does not automatically authorize a provider call.

## PASS

```text
UNJUSTIFIED_PERMANENT_TEMPORAL_CLOSURE = 0
REOPEN_TRIGGER_MODEL_PRESENT = true
```

---

# 13. Failure F05-11 — audit correction remains chat-only

## Failure mechanism

A review identifies a material methodology/execution defect, the conversation acknowledges it, but the correction never reaches durable repository authority.

## Why dangerous

The lesson disappears on agent/chat handoff and can be repeated in the next job.

## Correct rule

```text
MATERIAL_ACCEPTED_STEP05_CORRECTION
-> UNIVERSAL RULE IF GENERALIZABLE
-> JOB INCIDENT RECORD IF JOB-SPECIFIC
-> CURRENT EXECUTION CONTRACT RECONCILIATION
-> REMOTE READBACK
```

## PASS

```text
MATERIAL_ACCEPTED_STEP05_CORRECTION_CHAT_ONLY = 0
```

---

# 14. Failure F05-12 — stale provider schema / limits / pricing reused as current

## Failure mechanism

A prior provider schema, technical limit, price or Bridge contract is copied into a new execution gate without current verification.

## Why dangerous

Provider and Bridge contracts can change; a historical recorded value is not necessarily current truth.

## Correct rule before execution release

```text
FETCH CURRENT REMOTE BASE
RECHECK CURRENT BRIDGE REQUEST SCHEMA
RECHECK CURRENT OFFICIAL PROVIDER LIMITS
RECHECK CURRENT OFFICIAL PRICE IF COST IS MATERIAL
SEPARATE HISTORICAL VALUES FROM CURRENT VERIFIED VALUES
```

Current verification belongs in the job-specific execution release/source trace, not hard-coded permanently into this universal file.

## PASS

```text
STALE_PROVIDER_FACT_USED_AS_CURRENT_WITHOUT_RECHECK = 0
```

---

# 15. Failure F05-13 — provider response treated as accepted semantic output

## Failure mechanism

New provider rows are injected directly into family/semantic/final authorities because acquisition succeeded.

## Why dangerous

Raw rows have not passed identity normalization, duplicate handling, collision handling, sanitation or uncertainty preservation.

## Correct pipeline

For Wordstat-based Step05 expansion:

```text
PROVIDER RESPONSE
-> COMPLETE RAW PERSISTENCE
-> REMOTE READBACK
-> STEP03A-COMPATIBLE NORMALIZATION
-> STEP03B-COMPATIBLE SANITATION
-> UNION / RECONCILIATION
-> STEP05 ACCEPTANCE
```

Do not mutate accepted upstream authorities in place. Materialize the appropriate additive/revision lineage.

## PASS

```text
RAW_PROVIDER_ROW_DIRECT_TO_ACCEPTED_SEMANTIC_AUTHORITY = 0
```

---

# 16. Failure F05-14 — next provider call before current RAW durability

## Failure mechanism

The current provider response is visible/technically successful and execution moves to another call before complete RAW is persisted and read back.

## Correct rule

Step05 inherits `STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md` in full.

```text
NO NEXT PROVIDER REQUEST
UNTIL
COMPLETE CURRENT RAW + PROVENANCE + REMOTE READBACK = PASS
```

HTTP/provider success alone is not a persistence gate.

## PASS

```text
NEXT_PROVIDER_CALL_BEFORE_CURRENT_RAW_READBACK = 0
```

---

# 17. Failure F05-15 — new probe without information-gain contract

## Failure mechanism

A new probe exists because a gap “looks interesting” but the project has not stated what decision a positive, zero, incomplete or failed outcome changes.

## Why dangerous

Step05 becomes open-ended exploratory spending rather than bounded coverage control.

## Correct rule

Every provider candidate must answer:

```text
WHAT EXACT QUESTION IS OPEN?
WHY CAN EXISTING EVIDENCE NOT ANSWER IT?
WHAT WOULD POSITIVE EVIDENCE CHANGE?
WHAT WOULD A VALID ZERO CHANGE?
WHAT WOULD TECHNICAL FAILURE CHANGE? (normally no semantic conclusion)
WHAT IS THE REQUEST/DEPTH/COST BOUND?
WHAT IS THE STOP CONDITION?
WHAT IS THE PERSISTENCE/DOWNSTREAM PATH?
```

## PASS

```text
PROVIDER_CANDIDATE_WITHOUT_INFORMATION_GAIN_CONTRACT = 0
```

---

# 18. Failure F05-16 — valid zero result overclaimed

## Failure mechanism

A valid zero-row response is converted into “there is no market demand”.

## Why dangerous

The observation is bounded by provider, query/operator shape, region, device, time/snapshot and request scope.

## Correct interpretation

`SUCCESS_WITH_ZERO_ROWS` may close only the current bounded question/snapshot when evidence is complete.

It does NOT prove universal absence of demand.

Required closure shape:

```text
ZERO_RESULT_SCOPE = provider + query/operator + region/device + current snapshot + bounded question
CLOSURE = CLOSED_FOR_CURRENT_RESEARCH_SNAPSHOT
UNIVERSAL_ZERO_DEMAND_CLAIM = false
```

## PASS

```text
ZERO_RESULT_OVERCLAIM = 0
```

---

# 19. Failure F05-17 — Work used when no large-data trigger exists

## Failure mechanism

A small methodology correction, gate review, one/few candidate reconciliation or simple documentation task is handed to Work merely because Work exists in the process.

## Why dangerous

It adds unnecessary handoff state, base-drift risk and execution complexity and violates the intended role boundary.

## Universal rule

```text
WORK = LARGE-DATA / FULL-VOLUME TRANSFORMATION TOOL WHEN TRIGGERED BY SCALE
WORK != DEFAULT STEP05 DOCUMENTATION EDITOR
WORK != DEFAULT ONE-CANDIDATE GATE REVIEWER
```

Use Main ChatGPT / ordinary repository editing for bounded documentation, gate and small-candidate work.

Use Work only when the applicable Level1 Work trigger is actually met, for example when provider output or full-volume reconciliation is too large/risky for ordinary chat without sampling/truncation.

Large data must never be sampled merely to avoid Work.

## PASS

```text
WORK_HANDOFF_WITHOUT_LARGE_DATA_OR_EXPLICIT_APPLICABLE_TRIGGER = 0
LARGE_DATA_SAMPLED_TO_AVOID_WORK = 0
```

---

# 20. Provider outcome contract

Every job-specific Step05 execution release MUST define the outcome mapping before the call.

Minimum matrix:

| provider outcome | semantic meaning | branch state | automatic retry |
|---|---|---|---|
| `SUCCESS_WITH_ROWS` | positive bounded provider evidence | persist/readback, then 03A/03B | no automatic replay |
| `SUCCESS_WITH_ZERO_ROWS` | valid bounded zero observation | snapshot closure may be possible | no automatic replay |
| `SUCCESS_BUT_EVIDENCE_INCOMPLETE` | provider responded but evidence not sufficient/complete | unresolved | forbidden until new release |
| `VALIDATION_FAILURE` | request contract invalid/not accepted | unresolved | forbidden until corrected release |
| `PROVIDER_FAILURE` | provider did not answer bounded semantic question | unresolved | forbidden until new release |
| `OUTCOME_UNKNOWN` | execution may or may not have occurred | unresolved; duplicate-execution risk | blind retry forbidden |

Hard rule:

```text
TECHNICAL FAILURE DOES NOT BECOME NEGATIVE DEMAND EVIDENCE
```

---

# 21. Query/operator decision gate

Before a provider call, the job-specific release must state whether the request is primarily:

```text
DISCOVERY / RECALL-FIRST
PRECISION VALIDATION
EXACT-FORM TEST
COLLISION DIAGNOSTIC
```

Then justify operators/morphology accordingly.

Required fields:

```text
operator shape
what is fixed/not fixed
expected recall effect
expected precision effect
known collision risk
why this fits current unresolved question
reconsideration trigger
```

The method MUST NOT encode a universal “always use !” or “never use !” rule.

---

# 22. Temporal closure / reopen model

A Step05 branch may be closed for the current research snapshot when evidence is sufficient for the bounded question.

Closure does not mean permanent truth.

Recommended generic fields:

```text
closure_state
closure_scope
closure_evidence
closure_date/snapshot
identical_replay_allowed_current_round = false
reopen_triggers[]
```

A reopen trigger sends the question back through reconciliation/information-gain review. It does not automatically issue a provider request.

---

# 23. Fresh external/provider research before release

Before a material provider execution release, current job evidence must refresh relevant provider facts.

Authority order:

```text
1. official provider documentation
2. current Bridge code/protocol for local execution contract
3. high-quality external methodology for questions official docs do not answer
4. project heuristic, explicitly labelled
```

Baseline provider references to re-check when relevant:

- https://yandex.com/support2/wordstat/ru/
- https://yandex.com/support2/wordstat/ru/content/faq
- https://yandex.com/support2/wordstat/ru/content/api-wordstat
- current Yandex Cloud / Yandex Search API Wordstat documentation and pricing pages

Current official Wordstat documentation supports that Top/Regions views accept operators including `!`, `+`, quotes, brackets, parentheses and `|`, and that Top queries represent recent query statistics. Exact current API/Bridge limits and prices must still be revalidated immediately before execution rather than frozen in Level2.

---

# 24. Required job-specific artifacts

Before the first Step05 provider execution, the active job must have durable authority for:

```text
Step05 pre-acquisition reconciliation
provider candidate manifest
fresh source/provider/Bridge trace
candidate depth justification
operator/recall-precision decision
outcome matrix
execution release
raw persistence target / receipt path
reopen/stop logic
```

After execution:

```text
complete RAW result
receipt/provenance
remote readback
03A-compatible normalization result
03B-compatible sanitation result
Step05 reconciliation/closure record
```

---

# 25. Step05 final PASS

Step05 may be accepted only when all applicable conditions pass:

```text
ALL_GAP_ROWS_RECONCILED = true
DUPLICATE_REPROBES = 0
OWNER_FACT_PROVIDER_BYPASSES = 0
ALL_NEW_PROVIDER_CANDIDATES_HAVE_INFORMATION_GAIN_CONTRACT = true
DEPTH_JUSTIFICATION = PASS where provider acquisition exists
OPERATOR_DECISION_EXPLICIT = true where material
OUTCOME_CONTRACT_DEFINED_BEFORE_EXECUTION = true
NO_RETRY_SEPARATED_FROM_EVIDENCE_MEANING = true
ZERO_RESULT_SCOPE_BOUNDED = true
DEPTH_BOUNDARY_HANDLED = true where applicable
COMPLETE_RAW_PERSISTENCE_AND_READBACK = PASS for every executed request
NEW_ROWS_PASS_03A_03B_BEFORE_UNION = true
TEMPORAL_CLOSURES_HAVE_REOPEN_TRIGGERS = true
MATERIAL_REVIEW_CORRECTIONS_DURABLE = true
WORK_USED_ONLY_WHEN_APPLICABLE_TRIGGER_EXISTS = true
OPEN_CRITICAL_STEP05_DEFECTS = 0
```

If an execution-ready candidate remains unresolved/unexecuted:

```text
STEP05_PRE_ACQUISITION_MAY_BE_ACCEPTED
STEP05_FINAL_COMPLETE = false
STEP06_START_ALLOWED = false
```

---

# 26. Plain-language universal rule

Before Step05 spends another provider request, prove all of this:

> We know exactly what remains unknown; old evidence really does not answer it; the new query shape and depth are justified; we know what every possible provider outcome means; technical failure cannot be mistaken for “no demand”; the full result will be durably saved before any next call; and any new rows will return through normalization/sanitation before they become accepted semantic evidence.
