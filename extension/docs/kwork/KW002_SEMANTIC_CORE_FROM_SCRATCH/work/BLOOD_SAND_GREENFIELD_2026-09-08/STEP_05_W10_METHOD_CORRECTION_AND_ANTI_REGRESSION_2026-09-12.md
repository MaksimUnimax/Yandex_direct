# KW-002 Blood & Sand — Step05 method correction and anti-regression record

Date: 2026-09-12  
Status: **DOCUMENTATION CORRECTION MATERIALIZED / PROVIDER EXECUTION STILL NOT RELEASED**

Universal authority created by this correction:

`../../LEVEL2/STEP_05_TARGETED_EXPANSION_AND_PROVIDER_EXECUTION_GATE.md`

Current job boundary:

```text
STEP05_W10_V2_PRE_ACQUISITION = ACCEPTED
STEP05_FINAL = NOT COMPLETE
W10C001 = NOT EXECUTED
PROVIDER_EXECUTION_RELEASED = false
WORDSTAT_CALLS_ALLOWED_NOW = 0
STEP06_STARTED = false
```

This record exists because several material Step05 execution-contract defects were discovered after the W10 V2 pre-acquisition reconciliation had already passed. The reconciliation itself is not discarded; the defect is in the execution contract and in missing universal Step05 anti-regression rules.

---

## 1. What was already correct and remains accepted

The W10 V2 reconciliation correctly reduced the 13 Step04 queue rows to bounded outcomes rather than blindly issuing provider calls.

Accepted strengths preserved:

- prior durable evidence was reused where it already answered the question;
- owner/business facts were kept out of search-demand provider acquisition;
- duplicate reprobes were avoided;
- one genuinely unresolved provider candidate remained;
- no provider call occurred during W10 V2 reconciliation;
- no Step03A/Step03B/W09 Step04 mutation occurred;
- Step06 did not start.

Therefore this correction does **not** rebuild the 13-row reconciliation.

---

# 2. Defect — pre-acquisition PASS could be misread as final Step05 completion

## What was wrong

W10 V2 has a valid pre-acquisition acceptance, but one provider candidate remains unexecuted. Without explicit state separation, a later agent could report Step05 itself as complete.

## Why dangerous

Step06 could start while a material targeted-expansion branch remains unresolved.

## Correction

The universal Step05 authority now distinguishes:

```text
PRE_ACQUISITION_ACCEPTED
PROVIDER_EXECUTION_PENDING
RAW_PERSISTENCE_PENDING
NORMALIZATION_SANITATION_PENDING
RECONCILIATION_PENDING
STEP05_ACCEPTED
```

Current job remains:

```text
STEP05_FINAL_COMPLETE = false
STEP06_START_ALLOWED = false
```

---

# 3. Defect — old stop condition collapsed valid zero and technical failure

Historical W10 V2 candidate wording:

```text
stop on success, empty result, validation failure or provider failure
```

## What was wrong

This wording used the same apparent terminal semantics for fundamentally different outcomes.

A valid complete zero-row provider response can be bounded evidence. Validation/provider failure is not an answer to the semantic question.

## Correction

Current Step05 outcome contract must distinguish:

```text
SUCCESS_WITH_ROWS
SUCCESS_WITH_ZERO_ROWS
SUCCESS_BUT_EVIDENCE_INCOMPLETE
VALIDATION_FAILURE
PROVIDER_FAILURE
OUTCOME_UNKNOWN
```

Only complete valid provider responses can create provider evidence.

---

# 4. Defect — “no automatic retry” could be confused with negative evidence

## What was wrong

The old candidate correctly prohibited automatic retry, but did not explicitly separate the execution-safety meaning from semantic meaning.

## Why dangerous

A later executor could treat a failed/unknown request that is not automatically retried as if the demand question had been answered negatively.

## Correction

Permanent invariant now exists:

```text
NO_RETRY != NEGATIVE_EVIDENCE
```

For incomplete/failure/unknown outcomes:

```text
branch = UNRESOLVED
blind_retry = forbidden
negative_semantic_conclusion = forbidden
follow_up = requires separate reconciliation/release
```

---

# 5. Defect — requested depth 2000 existed before explicit Step05 depth proof

Historical candidate requested:

```text
requested_depth_if_bridge_supported = 2000
```

## What was wrong

The number was not accompanied in the candidate manifest by the full inherited depth-justification reasoning required by:

`../../LEVEL2/STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`

Provider maximum is not itself a semantic method.

## Current reasoning

W10C001 is a single bounded discovery question and the current plan allows at most one GetTop request before persistence/reconciliation. Plausible candidate depths are 500 / 1000 / 2000.

Reason to prefer 2000 **if the immediately pre-execution Bridge/provider recheck confirms that 2000 remains valid and cost behavior remains acceptable**:

- the question is discovery-oriented rather than exact-form validation;
- only one request is intended in the current round;
- shallower 500/1000 boundaries can hide lower-frequency qualified vocabulary and make a one-call diagnostic less informative;
- choosing 2000 maximizes observable vocabulary inside the already bounded one-request contract;
- a returned 2000-row boundary still does not prove semantic completeness.

This is a job-specific methodological justification, not a universal “always request 2000” rule.

Current state:

```text
REQUESTED_DEPTH = 2000_PENDING_IMMEDIATE_PROVIDER_BRIDGE_RECHECK
DEPTH_GATE_FINAL_RELEASE = PENDING
```

---

# 6. Defect — depth boundary lacked an explicit state

## What was wrong

A 2000-row return could later be misread as “all vocabulary collected”.

## Correction

If returned row count reaches the requested depth boundary:

```text
DEPTH_BOUNDARY_REACHED = true
SEMANTIC_UNIVERSE_COMPLETE = false
```

This state must survive downstream reconciliation.

---

# 7. Defect — `Аум` versus `!Аум` operator decision was not explicitly justified

## Current evidence boundary

The unresolved question is not “what is the exact-form frequency of the word Аум?”.

It is whether the distinct Cyrillic form `Аум` has current **physical-product-qualified discovery vocabulary** when constrained by product-class terms.

Current candidate phrase:

```text
(амулет|оберег|талисман) Аум
```

## Fresh official provider facts checked 2026-09-12

Yandex Wordstat documentation currently states that Wordstat supports operators including `!`, `+`, quotes, brackets, parentheses and `|` on Top/Regions views, and that an ordinary word/phrase query is evaluated with possible word forms. Official documentation also describes `!` as an operator that can preserve/fix word forms in contexts where word-form preservation is required.

Sources:

- https://yandex.com/support2/wordstat/ru/content/faq
- https://yandex.com/support2/wordstat/ru/
- https://yandex.com/support2/wordstat/en/content/stop-slova

## Corrected operator decision

Retain the bare form `Аум` for the current candidate rather than automatically switching to `!Аум`.

Reason:

```text
CURRENT QUESTION = DISCOVERY / RECALL-FIRST
PRODUCT-CLASS QUALIFIERS ALREADY NARROW CONTEXT
MORPHOLOGICAL VARIANTS MAY CONTAIN USEFUL PRODUCT VOCABULARY
PREMATURE ! FIXATION MAY REDUCE RECALL
```

This does not mean `!` is wrong in general.

Reconsideration trigger:

```text
if current provider evidence or a later controlled diagnostic shows that unwanted morphology/form collisions materially dominate and prevent the bounded question from being answered
```

Any such follow-up would require a separate release; it is not automatically authorized.

---

# 8. Defect — broad prior evidence could be overread as proof against qualified demand

Current prior evidence includes a broad `Аум` acquisition branch and a separately qualified `Ом` branch.

## What was wrong

Broad evidence around `Аум` contains collision space but does not itself answer the narrower physical-product-qualified `Аум` question.

## Correct claim boundary

```text
BROAD_AUM_EVIDENCE_DOES_NOT_ANSWER_QUALIFIED_AUM_PRODUCT_QUESTION
```

Forbidden claim:

```text
BROAD_AUM_COLLISIONS => QUALIFIED_PRODUCT_DEMAND_ABSENT
```

This scope distinction is the reason W10C001 can still have incremental information gain without duplicating earlier evidence.

---

# 9. Defect — time-bounded demand evidence could be described too permanently

## What was wrong

Terms such as `PERMANENT`, `PERMANENT_STOP`, `NEVER_REPROBE` are too strong for a temporal search-demand snapshot unless they refer narrowly to current-round execution authorization rather than to market truth.

## Correction

Use bounded language:

```text
CLOSED_FOR_CURRENT_RESEARCH_SNAPSHOT
IDENTICAL_REPLAY_NOT_AUTHORIZED_IN_CURRENT_ROUND
```

Possible reopen triggers:

- material client/business scope change;
- material assortment change;
- new owner evidence;
- planned future refresh/revision;
- evidence freshness expiry;
- material provider/method change;
- upstream authority invalidation.

A reopen trigger requires new reconciliation and does not itself authorize a provider call.

---

# 10. Defect — accepted review lessons were chat-only

## What was wrong

The post-W10 audit identified the defects above, but they were not yet in durable GitHub methodology.

## Why dangerous

A new chat/agent could read the repository and repeat the same execution-contract errors.

## Correction

The reusable mechanisms are now materialized in:

`../../LEVEL2/STEP_05_TARGETED_EXPANSION_AND_PROVIDER_EXECUTION_GATE.md`

This file records the current job-specific occurrence and correction.

---

# 11. Defect — current provider facts could be reused from historical values

The old manifest contains a historical estimated-cost field and a provider-depth assumption.

## Correction

Before execution release, recheck:

```text
CURRENT_REMOTE_HEAD
CURRENT_BRIDGE_WORDSTAT_SCHEMA
CURRENT_OFFICIAL_PROVIDER_LIMITS
CURRENT_OFFICIAL_PROVIDER_PRICE IF MATERIAL
```

Historical cost values remain historical evidence only.

Fresh source review in this documentation pass confirmed that official Yandex materials currently describe Wordstat Top queries as recent query statistics and confirm supported operator families, but this documentation pass does **not** promote any historical price to current execution authority.

A current official Yandex Cloud announcement from April 2026 stated a GetTop rate of 20 RUB per 1000 requests for the May 2026 GA launch, but the execution gate must still recheck the then-current pricing page immediately before a billable call rather than treating that announcement as permanent current pricing.

Source:

- https://yandex.cloud/en/blog/digest-april-2026

---

# 12. Defect — successful provider response could be treated as accepted Step05 rows

## Correction

Any future W10C001 rows must follow:

```text
COMPLETE RAW
-> REMOTE READBACK
-> STEP03A-COMPATIBLE NORMALIZATION
-> STEP03B-COMPATIBLE SANITATION
-> RECONCILIATION / UNION
-> STEP05 FINAL DECISION
```

No raw provider row may enter final semantic/family/page authority directly.

---

# 13. Defect — next provider call before current RAW durability

The existing universal RAW-persistence rule already covers Step05 and remains authoritative:

`../../LEVEL2/STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`

Current Step05 contract restates the hard control:

```text
NO NEXT WORDSTAT CALL
UNTIL
COMPLETE CURRENT RAW + PROVENANCE + GITHUB REMOTE READBACK = PASS
```

---

# 14. Defect — valid zero could be overclaimed as universal zero demand

## Correction

A valid zero result can close only the bounded current question/snapshot:

```text
provider + phrase/operator + region/device + current snapshot + current bounded question
```

It does not prove universal market absence.

Required interpretation:

```text
SUCCESS_WITH_ZERO_ROWS
-> CLOSED_FOR_CURRENT_RESEARCH_SNAPSHOT may be allowed
-> UNIVERSAL_ZERO_DEMAND_CLAIM = false
```

---

# 15. Process mistake — Work must not be used for this bounded documentation/gate correction

This correction is small methodology/documentation work and one-candidate gate logic. It does not require large-data transformation.

Correct role boundary:

```text
MAIN CHATGPT / NORMAL REPO EDITING
= bounded methodology, documentation, gate and one/few-candidate work

WORK
= large-data / full-volume transformation when the Level1 trigger is actually met
```

If a future provider response creates a large full-volume normalization/sanitation workload that ordinary chat cannot process without sampling/truncation, then Work may become appropriate for that transformation. Work is not used merely because Step05 exists.

---

# 16. Current corrected W10C001 pre-release contract

```text
candidate = W10C001
status = NOT_EXECUTED
question = distinct Cyrillic Аум physical-product-qualified discovery vocabulary
phrase = (амулет|оберег|талисман) Аум
operator_mode = DISCOVERY_RECALL_FIRST / NO_MORPHOLOGY_FIXATION
prior_broad_evidence_closure = DOES_NOT_ANSWER_QUALIFIED_QUESTION
requested_depth = 2000_PENDING_IMMEDIATE_RECHECK
max_requests_current_round = 1
provider_execution_released = false
wordstat_calls_allowed_now = 0
```

Outcome contract:

| outcome | semantic effect | execution effect |
|---|---|---|
| `SUCCESS_WITH_ROWS` | bounded positive evidence | persist full RAW/readback; 03A/03B; reconcile |
| `SUCCESS_WITH_ZERO_ROWS` | bounded zero observation; no universal-zero claim | persist/readback; current snapshot branch may close |
| `SUCCESS_BUT_EVIDENCE_INCOMPLETE` | no closure | persist what was returned; branch unresolved; new release required |
| `VALIDATION_FAILURE` | no semantic answer | preserve failure evidence; branch unresolved; corrected release required |
| `PROVIDER_FAILURE` | no semantic answer | preserve failure evidence; branch unresolved; new release required |
| `OUTCOME_UNKNOWN` | no semantic answer; duplicate-execution risk | preserve receipt; blind retry forbidden; separate recovery/release required |

Depth-boundary contract:

```text
returned_rows == requested_depth
=> DEPTH_BOUNDARY_REACHED = true
=> SEMANTIC_UNIVERSE_COMPLETE = false
```

---

# 17. Current PASS / HOLD verdict

```text
STEP05_W10_V2_RECONCILIATION = ACCEPTED
STEP05_METHOD_CORRECTION = MATERIALIZED
W10C001_CONTRACT = CORRECTED_FOR_DOCUMENTATION
W10C001_PROVIDER_RELEASE = HOLD
WORDSTAT_CALLS_IN_THIS_CORRECTION = 0
SEARCH_CALLS_IN_THIS_CORRECTION = 0
GENSEARCH_CALLS_IN_THIS_CORRECTION = 0
STEP06 = NOT_STARTED
```

Remaining next action:

```text
SEPARATE STEP05 FIRST-PROVIDER EXECUTION RELEASE
AFTER:
- current HEAD recheck,
- current Bridge Wordstat schema recheck,
- current official provider limit/price recheck,
- exact release readback.
```

Do not start Step06 before Step05 is actually closed.
