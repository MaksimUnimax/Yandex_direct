# KW-001 — STEP METHOD REVIEW AND LESSONS LEDGER

Date updated: 2026-08-29  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file contains permanent, owner-approved KW-001 methodology lessons and corrections accumulated so far.

It is part of Layer A/B permanent methodology as defined by `RULES_ARCHITECTURE.md` and is **not** a per-job execution log.

## Owner-lock rule

This file does **not** update automatically after each job step.

During a concrete job ChatGPT may discover a possible reusable lesson, but without explicit owner instruction it may only:

```text
report the finding;
show evidence/sources;
propose a permanent change;
wait for owner instruction.
```

Only explicit owner authorization allows adding/removing/changing a permanent lesson here.

Concrete client/job words, URLs, provider results, matrices, page decisions and job histories must not be copied into this file.

## Mandatory read

Before every major step ChatGPT must read this file as part of the stable universal method, but must not mutate it unless explicitly authorized by the owner.

## Mandatory causal-use rule

This ledger is not a list of actions to repeat mechanically.

Before applying a lesson to a new step ChatGPT must be able to explain:

```text
WHAT FAILED BEFORE
WHY IT FAILED
WHAT FALSE ASSUMPTION / PROCESS GAP CAUSED IT
HOW THE APPROVED CONTROL BLOCKS THAT CAUSE
WHY THAT CAUSE IS RELEVANT TO THE CURRENT STEP
WHETHER CURRENT EXTERNAL RESEARCH STILL SUPPORTS THE METHOD
```

If this causal explanation cannot be produced, method validation has not happened.

Canonical rule:

```text
RULE_RECALL_WITHOUT_CAUSAL_UNDERSTANDING != METHOD_VALIDATION
```

## Required structure for every validated step entry

Each step entry should preserve, where applicable:

```text
STEP PURPOSE
APPROVED METHOD
WHY THIS METHOD
KNOWN ERROR(S)
ROOT CAUSE
CORRECTED METHOD
NON-REPEAT CONTROLS
METHOD ORIGIN / EXTERNAL SUPPORT
PASS GATE
STATUS
```

A future step with no validated methodology must be marked `UNVALIDATED` and researched before execution rather than inferred mechanically from neighbouring steps.

---

# OWNER-APPROVED STEP METHODOLOGY LESSONS

## Step 0 — order / scope freeze

### Step purpose

Freeze what the client actually asked for before evidence gathering starts, so later data cannot silently rewrite the order.

### Approved method

- Freeze business, region, goal, scope, known exclusions and requested outputs before provider evidence.
- Later findings may change recommendations but must not silently rewrite the original brief.

### Why this method

Without a frozen starting state, later evidence can be interpreted against a moving target and the analysis can appear internally consistent while no longer answering the original client task.

### Known error / failure prevented

Do not let later evidence retroactively redefine the order so the analysis appears cleaner than it really was.

### Method origin

`PROJECT_TEST_VALIDATED + ANALYST_DISCIPLINE`.

### Pass gate

The brief/scope is explicit enough that a later analyst can distinguish original client constraints from later evidence-led recommendations.

Status: **APPROVED / ACTIVE**.

---

## Step 1 — existing-site discovery and business/page model

### Step purpose

Build a factual model of the existing business/site before using search-demand evidence to recommend page changes.

### Approved method

- For a non-trivial existing site, combine deep internal architecture discovery with an independent public/search-visible discovery channel.
- Preserve evidence states: opened/read is stronger than discovered-link or inferred-template evidence.
- Merge complementary passes rather than selecting one report and discarding the other.
- Site architecture is factual/business discovery input; it does not prove that every current page deserves its own SEO target.

### Why this method

One discovery channel can miss public pages, templates, content families or business signals. Cross-channel discovery reduces the chance that the later semantic model is built on an incomplete picture of the actual site.

### Known error

A single discovery pass was treated as if it represented the whole site.

### Root cause

Discovery success was confused with discovery completeness.

### Corrected method / non-repeat control

A single discovery pass must not be treated as complete for a non-trivial site unless completeness is demonstrated and recorded. Use an independent second discovery channel and preserve the evidence strength of each finding.

### Method origin

`PROJECT_TEST_VALIDATED + INDUSTRY_REASONING`.

### Pass gate

The merged business/page model is cross-checked, evidence states are explicit, and unresolved discovery gaps are recorded instead of inferred away.

Status: **APPROVED / ACTIVE**.

---

## Step 2 — seed/query plan

### Step purpose

Create bounded acquisition probes that expose search-demand vocabulary without predetermining the final semantic core from the existing site structure.

### Approved method

- A seed is an acquisition probe, not a final semantic-core keyword.
- Do not mirror every existing URL into one seed; use bounded representative roots so provider evidence can challenge current site taxonomy.
- Every second-pass expansion must have an explicit reason/information purpose.
- Numerical request/row caps used for rehearsal economics are project controls, not industry standards.

### Why this method

Seeds are measurement instruments. Treating them as final targets causes the acquisition plan to reproduce analyst assumptions or the current URL tree rather than reveal actual demand.

### Known error

Seed relevance was confused with final keyword/page relevance.

### Root cause

The acquisition probe itself was treated as the object being selected for the final semantic set.

### Corrected method / non-repeat control

Always explain what uncertainty each seed is probing and never defend/reject it based on intuition alone when measurement is the purpose of the probe.

### Method origin

`PROJECT_TEST_VALIDATED + ANALYST_HEURISTIC`.

### Pass gate

Every seed has a declared acquisition purpose and no seed is treated as final semantic/page evidence solely because it was selected for provider acquisition.

Status: **APPROVED / ACTIVE**.

---

## Step 3 — Wordstat provider acquisition

### Step purpose

Collect a complete reusable demand-evidence dataset that later semantic work can audit and reproduce.

### Approved method

- Freeze the manifest before provider execution.
- Preserve exact phrase, region, device, provider request identity, cost and outcome state.
- `SEED != FINAL KEYWORD`.
- `RAW WORDSTAT != CLIENT SEMANTIC CORE`.
- Wordstat associations are similar-query vocabulary evidence, not automatically accepted semantic-core phrases.
- A successful sparse response is not a provider failure and not proof of zero demand.
- `OUTCOME_UNKNOWN` must never be blindly replayed.
- Before every YMB command explicitly state active service and execution mode.
- Replay safety is determined by provider-execution truth and accepted recovery policy, not UI appearance.

### Why this method

The step exists to preserve data for later reasoning, not to accumulate successful API statuses. If complete returned evidence is missing, later cleanup and expansion cannot be audited even when every provider call technically succeeded.

### Owner-approved correction — provider execution is not collection completion

The goal of Step 3 is to **collect a complete reusable dataset**, not to execute a target number of API requests.

A Step-3 provider item is complete only when the complete result required by the step has been preserved and verified before the next provider item is allowed.

Mandatory per-item sequence:

```text
DEFINE WHAT MUST BE COLLECTED
→ EXECUTE ONE PROVIDER ITEM
→ RECEIVE PROVIDER RESULT
→ PRESERVE THE COMPLETE REQUIRED RESULT
→ VERIFY PRESERVED COUNTS/FIELDS AGAINST PROVIDER TRUTH
→ CONFIRM THE SAVED RESULT IS READABLE/USABLE
→ ONLY THEN ALLOW THE NEXT PROVIDER ITEM
```

The following do **not** prove Step-3 completion by themselves:

```text
HTTP 200
status = OK
request_executed = true
item_status = SUCCEEDED
batch succeeded count
provider request count
cost recorded
representative examples
summary/checkpoint without complete returned rows
```

If the provider returns a result set and only representative examples are preserved, that item is **INCOMPLETE FOR THE PROJECT** even though the API request succeeded.

If the current item is incomplete:

```text
CURRENT_ITEM = INCOMPLETE
NEXT_PROVIDER_ITEM = BLOCKED
STEP_3 = NOT_COMPLETE
NEXT_ANALYTICAL_STEP = BLOCKED
```

For Wordstat `getTop`, preservation must explicitly account for the complete returned arrays required by the concrete step, including `results[]` and `associations[]` when those arrays are part of the acquisition objective. `totalCount` is demand/frequency evidence and must not be confused with the number of returned rows saved.

### Error that caused this correction

A controlled KW-001 rehearsal executed a multi-item Wordstat pass and recorded successful provider outcomes, but many item checkpoints preserved only counts and representative examples rather than the complete returned phrase rows. The batch was then incorrectly accepted as complete and downstream analysis proceeded without a complete reusable acquisition dataset.

### Root cause

```text
technical success was treated as the goal
instead of verifying whether the actual data-collection goal had been achieved
```

### Failure prevented

Without this correction:

```text
a provider batch can look complete while the dataset needed by the client task is missing;
subsequent cleanup can operate on examples instead of all collected phrases;
expansion choices can be made from incomplete evidence;
several later steps can become invalid and require rework;
operator time and provider cost can be wasted;
request-count progress can replace actual project progress.
```

### Required Step-3 completion report

At the end of a Step-3 collection pass, the report must reconcile at minimum:

```text
provider items planned
provider items attempted
provider items actually executed
provider items with known outcomes
results rows returned
association rows returned where applicable
rows saved
rows verified
items incomplete
outcome_unknown
provider cost
```

### Non-repeat controls / pass gate

If the relevant counts do not reconcile, Step 3 cannot pass. The next provider item is blocked until the current required result is completely saved and verified.

### Method origin

`OFFICIAL provider semantics + PROJECT_TEST_VALIDATED + OWNER-APPROVED PROCESS CORRECTION`.

Status: **APPROVED / ACTIVE**.

---

## Step 4 — first post-Wordstat triage / cleanup preparation

### Step purpose

Separate obvious noise/scope problems from potentially useful demand and identify unresolved families before true row-level semantic cleanup.

### Approved rules

- Do not treat raw Wordstat output as a ready semantic core.
- Preserve ambiguous potentially valuable demand for later business/SERP resolution rather than deleting it prematurely.
- Wordstat associations are vocabulary/expansion evidence, not automatically accepted keywords.
- Do not make final cluster/page decisions before ordinary SERP evidence when page-boundary uncertainty remains.
- Business-priority unknowns must remain unresolved rather than being silently promoted or deleted.

### Why this method

Early triage should reduce obvious noise without destroying evidence needed for later intent/page decisions. It is preparation for row-level cleanup, not a substitute for it.

### Approved correction A — family-level triage is not full cleanup

Do not call a family/pattern review `complete semantic cleanup`.

Before final semantic-core freeze, row-level retained/excluded provenance must exist for the phrases used in the workflow.

### Root cause of correction A

A higher-level pattern/family decision was incorrectly treated as if every underlying phrase had been individually accounted for.

### Approved correction B — separate exclusion reasons

Use distinct states/reasons such as:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

A semantically valid phrase outside the frozen client scope is not the same thing as irrelevant demand.

### Approved correction C — frequency rule

Canonical rule:

```text
LOW_FREQUENCY_ALONE != PROOF_OF_IRRELEVANCE
```

Frequency may still contribute later to prioritization/page decisions together with relevance, business value, cluster/topic size and SERP evidence.

### Approved correction D — association confidence

A high-count broad association may justify an acquisition probe without becoming a strong semantic candidate.

Use probe confidence/status concepts such as:

```text
EXPANSION_PROBE_READY
EXPANSION_PROBE_AMBIGUOUS
EXPANSION_PROBE_REVIEW
```

### External support already checked when owner approved this correction

Official Yandex Wordstat GetTop:
- https://aistudio.yandex.ru/docs/ru/search-api/api-ref/Wordstat/getTop

External corroboration:
- https://www.semrush.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-intent/

Exact internal status names remain project-specific mechanics, not claimed industry standards.

### Non-repeat controls / pass gate

Do not claim full cleanup from family-level evidence. Preserve ambiguous rows. Keep scope/irrelevance/mechanical reasons separated. Do not use volume or association status as automatic acceptance/rejection proof.

### Method origin

`OFFICIAL + INDUSTRY_PRACTICE + ANALYST_HEURISTIC (owner-approved correction)`.

Status: **APPROVED / ACTIVE**.

---

## Step 5 — targeted Wordstat expansion pass #2

### Step purpose

Use a bounded second acquisition pass only where the first pass left a material demand-coverage uncertainty.

Status: **NOT YET UNIVERSALLY VALIDATED BY EXECUTION**.

### Current stable pre-step questions

```text
Does each proposed probe add information rather than duplicate pass #1?
Is the phrase a semantic target or only an acquisition probe?
What exact uncertainty will its provider result resolve?
Is the business family actually in scope or still client-unknown?
Is a broad association being over-promoted merely because of count?
Can the uncertainty be resolved more appropriately by later SERP evidence instead?
```

### Why these controls exist

A second acquisition pass can easily become recursive keyword collection with no decision value. Each probe therefore needs a declared information gain and must not be justified merely by volume or lexical adjacency.

A concrete job's exact Step-5 probe manifest belongs in that job workspace and does not belong here.

---

## Step 7 — row-level semantic cleanup

### Step purpose

Transform the complete acquired phrase universe into an auditable phrase-level decision set in which every source occurrence is accounted for and every unique phrase is explicitly classified without pretending that unresolved intent/page questions are already solved.

This step answers:

```text
Is this phrase clearly relevant enough to remain in the working semantic set now?
Is it clearly irrelevant / outside scope / mechanical noise?
Or is it genuinely uncertain and therefore REVIEW?
```

It does **not** decide final page ownership, final clustering, cannibalization or final Search architecture.

### Approved method

1. Preserve every source occurrence and provenance before semantic decisions.
2. Use conservative exact normalization for exact duplicate accounting; do not use stemming/lemmatization/word reordering as automatic merge proof.
3. Maintain one auditable decision record per exact normalized phrase.
4. Use explicit decision states:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

5. `KEEP` requires **positive semantic/business evidence**. It must never mean merely `no exclusion rule matched`.
6. A potentially relevant phrase without sufficient positive evidence goes to `REVIEW`, not automatically to KEEP and not silently to exclusion.
7. Low frequency alone never proves irrelevance.
8. Association-only evidence never auto-promotes a phrase to KEEP.
9. Non-exact lexical duplicates are surfaced as candidates and are not automatically merged without stronger intent/page evidence.
10. Run arithmetic/provenance QA **and** semantic QA. Arithmetic success alone cannot pass semantic cleanup.
11. Semantic QA must include adversarial MUST_KEEP and MUST_NOT_KEEP cases across the main phrase families and known failure classes.
12. If semantic QA finds a new class of false decisions, fix the **cause/class**, rerun the whole decision set, and repeat until additional review is no longer producing material new failure classes.
13. Do not self-accept the result merely because the classifier/script runs successfully; the acceptance must reflect the declared semantic goal and remaining uncertainty.

### Why this method

Semantic cleanup is a relevance/intent decision problem, not a string-filtering problem.

A deterministic prefilter is useful for obvious cases, but a negative dictionary cannot prove positive relevance. Therefore absence of a rejection signal cannot logically serve as evidence for KEEP.

Likewise, exact accounting proves that no rows disappeared, but it does not prove the decisions attached to those rows are semantically correct.

The method intentionally prefers REVIEW over false certainty because later ordinary Search evidence can resolve mixed intent/page boundaries more safely than an aggressive cleanup heuristic.

### Known error 1 — family-level triage was previously overstated as complete cleanup

What was wrong:

A higher-level family/pattern pass was described as if all phrases had been semantically cleaned.

Root cause:

```text
coverage of categories was confused with row-level decision completeness
```

Correction:

Require full phrase-level accounting and explicit decision provenance before Step 7 can even be evaluated.

Non-repeat control:

```text
SOURCE_OCCURRENCES_RECONCILE = true
UNIQUE_PHRASES_RECONCILE = true
UNCLASSIFIED = 0
```

### Known error 2 — default KEEP fallthrough

What was wrong:

A classifier allowed phrases that matched no known exclusion/review rule to fall through into KEEP.

This created the false logic:

```text
NOT KNOWN BAD -> KEEP
```

instead of the required logic:

```text
POSITIVE RELEVANCE / BUSINESS FIT ESTABLISHED -> KEEP
UNCERTAIN -> REVIEW
CLEARLY WRONG -> EXCLUDE_*
```

Root cause:

The method was built primarily as a negative filter. Dictionary completeness was implicitly treated as if it proved semantic correctness.

Why this is dangerous:

Any phrase class missing from the negative dictionaries becomes a false KEEP even when its intent is navigational, DIY, technical, architectural, real-estate, component-specific, malformed or otherwise unresolved.

Corrected method:

```text
DEFAULT_KEEP_FALLTHROUGH = false
KEEP_REQUIRES_POSITIVE_REASON = true
UNCERTAINTY_DEFAULT = REVIEW
```

Every KEEP must have an explicit positive reason tied to a known business/content family or another positively established relevant user need.

### Known error 3 — machine/accounting QA was mistaken for semantic QA

What was wrong:

The earlier pipeline could reconcile all rows, exact duplicates and statuses while still making poor relevance decisions.

Root cause:

```text
structural correctness was treated as analytical correctness
```

Correction:

Step 7 requires two independent gates:

```text
A. ACCOUNTING / PROVENANCE QA
B. SEMANTIC DECISION QA
```

Both must pass.

### Known error 4 — brittle literal dictionaries / morphology and word order

What was wrong:

Literal substring rules missed inflected forms or reordered phrase forms. A semantic class could therefore change only because the words appeared in a different grammatical form/order.

Root cause:

String matching was allowed to stand in for semantic understanding.

Correction:

Use literal/rule logic only as an auditable aid, then adversarially test morphological/order variants. When QA finds a miss, fix the semantic class or normalization logic rather than adding only the single observed phrase whenever a broader causal rule exists.

Non-repeat control:

Semantic QA must deliberately include inflection and word-order variants for known risk classes.

### Known error 5 — isolated patching instead of causal correction

What was wrong:

When an individual false decision appears, it is tempting to add that exact phrase to an exception list and move on.

Root cause:

The symptom is easier to patch than identifying the general class of requests that produced it.

Corrected method:

For every semantic QA failure ask:

```text
What general intent/class caused this?
What other phrases can fail for the same reason?
Can the correction be expressed as a defensible class-level rule?
Will this rule create false negatives elsewhere?
What positive controls prove core queries still remain KEEP?
```

Then rerun the entire corpus.

Canonical rule:

```text
FIX_CAUSE_NOT_ONLY_EXAMPLE = true
```

### Known error 6 — non-exact duplicates can be over-merged

What was wrong/risk:

Spelling, transliteration, token-order or light morphological similarity can look like duplicate semantics without proving identical intent/page ownership.

Root cause:

Lexical similarity can be confused with search-task equivalence.

Corrected method:

Exact normalization may deduplicate exact phrase keys conservatively. Non-exact duplicates are only candidate groups until later intent/SERP evidence supports merging.

### Known error 7 — semantic cleanup can accidentally decide later-stage questions

Risk:

A cleanup classifier can begin deciding page architecture, final clustering, commercial priority or cannibalization simply because the phrase appears related.

Root cause:

The boundary between relevance cleanup and Search/page validation becomes blurred.

Corrected method:

If the phrase is plausibly relevant but final intent/page/business boundary needs evidence, keep it in REVIEW. Do not force later-stage decisions into Step 7.

### Required reasoning sequence before executing Step 7

ChatGPT must understand and explain this sequence before authorization:

```text
1. WHAT EXACT SOURCE UNIVERSE MUST BE ACCOUNTED FOR?
2. WHAT DOES KEEP MEAN POSITIVELY IN THIS BUSINESS/SCOPE?
3. WHICH DECISIONS CAN BE SAFE DETERMINISTIC EXCLUSIONS?
4. WHICH INTENT/SCOPE/PAGE BOUNDARIES MUST REMAIN REVIEW?
5. WHAT NORMALIZATION IS SAFE FOR EXACT ACCOUNTING?
6. WHAT NON-EXACT SIMILARITY MUST NOT BE AUTO-MERGED?
7. WHAT KNOWN ERROR CLASSES MUST THE SEMANTIC QA ATTACK?
8. WHAT POSITIVE CONTROL CASES PROTECT AGAINST OVER-CLEANING?
9. HOW WILL WE KNOW THE QA HAS STOPPED FINDING MATERIAL NEW FAILURE CLASSES?
10. WHAT REMAINS FOR ORDINARY Search AFTER THIS STEP?
```

If ChatGPT cannot explain why each decision/gate exists, Step 7 is not ready to run.

### External support checked for this lesson

Official/current search-demand and user-need guidance:
- https://yandex.ru/support2/wordstat/ru/interface/new
- https://yandex.ru/support/webmaster/en/recommendations/targeting

External industry methodology used to challenge the project method:
- https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/
- https://www.rush-analytics.ru/blog/chto-takoe-klasterizacziya-zaprosov
- https://ahrefs.com/blog/keyword-intent/
- https://ahrefs.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://www.semrush.com/blog/keyword-clustering/

No external authority mandates the exact five internal statuses or one exact normalization recipe. Those remain project-specific, owner-approved controls.

### Mandatory non-repeat controls

Before Step 7 can pass:

```text
ALL_SOURCE_OCCURRENCES_ACCOUNTED = true
ALL_UNIQUE_EXACT_PHRASES_CLASSIFIED = true
UNCLASSIFIED = 0
DEFAULT_KEEP_FALLTHROUGH = false
EVERY_KEEP_HAS_POSITIVE_REASON = true
LOW_FREQUENCY_ONLY_EXCLUSIONS = 0
ASSOCIATION_AUTO_KEEP = false
NONEXACT_DUPLICATES_AUTO_MERGED = 0
ARITHMETIC_QA = PASS
PROVENANCE_QA = PASS
SEMANTIC_QA = PASS
KNOWN_FALSE_KEEP_CLASSES_TESTED = true
CORE_MUST_KEEP_CONTROLS_TESTED = true
NEW_QA_FAILURE_CLASS -> FIX_CAUSE + RERUN_WHOLE_SET
```

### Pass gate

Step 7 is complete only when:

```text
1. the entire declared source universe reconciles;
2. every unique exact phrase has an explicit decision and reason;
3. KEEP is based on positive evidence, never default fallthrough;
4. uncertain relevant demand is preserved as REVIEW;
5. safe exclusions remain reason-separated;
6. non-exact candidates are not silently merged;
7. adversarial semantic QA passes without known material failure classes being ignored;
8. the result remains explicitly separate from final clustering/page ownership/Search validation;
9. the current job acceptance record documents remaining limitations;
10. NEXT_STEP_ALLOWED is based on this analytical gate, not script/workflow success.
```

### Method origin

`OFFICIAL + INDUSTRY_PRACTICE + PROJECT_TEST_VALIDATED + OWNER-APPROVED PROCESS CORRECTION`.

Status: **APPROVED / ACTIVE**.

---

# Permanent-update policy

If a future job reveals a potential universal lesson:

```text
1. report it to the owner in the step report;
2. provide evidence and source support;
3. do not edit this file;
4. wait for explicit owner instruction;
5. only then update the permanent universal method if instructed.
```

Markers:

```text
KW001_PERMANENT_LESSONS_LEDGER_ACTIVE = true
KW001_PERMANENT_LESSONS_OWNER_LOCKED = true
KW001_NO_AUTOMATIC_LESSON_PROMOTION = true
KW001_RULE_RECALL_WITHOUT_CAUSAL_UNDERSTANDING_INVALID = true
KW001_STEP3_PROVIDER_EXECUTION_NOT_COLLECTION_COMPLETION = true
KW001_STEP3_NEXT_ITEM_BLOCKED_UNTIL_COMPLETE_RESULT_VERIFIED = true
KW001_STEP3_COMPLETION_COUNTS_MUST_RECONCILE = true
KW001_FAMILY_TRIAGE_NOT_EQUAL_FULL_CLEANUP = true
KW001_SCOPE_EXCLUSION_SEPARATE_FROM_IRRELEVANCE = true
KW001_LOW_FREQUENCY_ALONE_NOT_IRRELEVANCE_PROOF = true
KW001_ASSOCIATION_IS_PROBE_NOT_ACCEPTED_KEYWORD = true
KW001_STEP7_DEFAULT_KEEP_FALLTHROUGH_FORBIDDEN = true
KW001_STEP7_KEEP_REQUIRES_POSITIVE_REASON = true
KW001_STEP7_UNCERTAINTY_DEFAULT_REVIEW = true
KW001_STEP7_ARITHMETIC_QA_NOT_SEMANTIC_QA = true
KW001_STEP7_FIX_CAUSE_NOT_ONLY_EXAMPLE = true
KW001_STEP7_NONEXACT_DUPLICATES_NOT_AUTO_MERGED = true
KW001_STEP7_SEMANTIC_QA_REQUIRED = true
```
