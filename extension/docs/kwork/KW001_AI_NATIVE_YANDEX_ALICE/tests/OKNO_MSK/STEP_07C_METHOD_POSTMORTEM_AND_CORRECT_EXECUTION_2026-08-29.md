# KW-001 / OKNO-MSK — STEP 07C METHOD POSTMORTEM AND CORRECT EXECUTION

Date: 2026-08-29  
Status: **CURRENT-JOB METHOD POSTMORTEM / CORRECTION CANDIDATE READY / NOT FINAL ACCEPTANCE**

This document records what was done wrong in the Step-07 row-level cleanup, why it was wrong, how the failure was found, how it was corrected, and how this step must be approached next time.

It is intentionally written as a causal postmortem rather than an exception list.

---

# 1. What I did wrong

## Error A — I treated a negative filter as proof of positive relevance

Historical Step 07B effectively used this logic for many result rows:

```text
if phrase matches known exclusion -> EXCLUDE
else if phrase matches known boundary/review rule -> REVIEW
else -> KEEP
```

That means the practical meaning of KEEP became:

```text
I did not recognize a reason to reject it
```

instead of:

```text
I positively established that the phrase represents a relevant user need for this business/scope
```

This was the central semantic error.

### Consequence

Phrases could become KEEP simply because the dictionary did not know their failure class.

Observed examples included:

```text
1 установка пластиковых окон
6 6 с панорамными окнами
rehau окна 2
алюминиевые окна 2
rehau окна анадырский проезд д 47
rehau микролифт для окна
```

Later semantic QA exposed additional classes:

```text
окна rehau сайт
окна rehau официальный
окна rehau сравнение
окна rehau внутри на стекле конденсат починить
окна rehau провисли
окно пластиковое закрыто
квартира с панорамными окнами
панорамные окна лес
панорамные окна на море
панорамные окна как называются
ремонт сетки для пластиковых окон
демонтаж алюминиевых окон
французские окна название
французские окна это какие
окна в рассрочку без
```

The exact examples are symptoms. The real defect was the default-KEEP reasoning model.

---

## Error B — I allowed machine reconciliation to create false confidence in semantic correctness

The old pass could prove:

```text
all source rows accounted
exact duplicate arithmetic reconciled
all unique rows had a status
no rows silently disappeared
```

Those controls were useful and remain valid.

But I incorrectly allowed that structural correctness to support a semantic PASS.

### Why this was wrong

A table can contain every row and still attach a bad semantic decision to every row.

Therefore:

```text
ACCOUNTING PASS != SEMANTIC PASS
```

The old Step 07B proved bookkeeping completeness, not enough semantic correctness.

---

## Error C — I relied too heavily on literal dictionaries/string patterns

During the correction itself, QA exposed multiple examples where literal matching did not represent meaning robustly.

### Example 1 — Russian inflection

A positive test based on an `окн` literal did not correctly cover the actual form `окон` in a phrase such as:

```text
установка пластиковых окон
```

A known-good phrase was incorrectly at risk of REVIEW.

### Example 2 — word order

A rule intended to catch state/context queries did not initially catch:

```text
окно пластиковое закрыто
```

because the words appeared in a different order than expected.

### Example 3 — morphology of component terms

A component boundary rule recognized one form of `сетка`, but a query such as:

```text
ремонт сетки для пластиковых окон
```

could avoid the intended component review rule until the cause was generalized to the word root/class.

### Root problem

I was using strings as if they were semantics.

Literal rules are useful for deterministic/auditable support, but they cannot be trusted as the sole semantic decision mechanism.

---

## Error D — the first correction was still too easy to accept after one successful build

The first corrected candidate removed the default KEEP fallthrough and materially improved the table.

It would have been easy to stop there because:

```text
workflow = SUCCESS
all KEEP had POSITIVE_* reasons
basic QA passed
```

But manual review still found new failure classes:

```text
navigational/entity intent
technical information intent
real-estate/inspiration panoramic intent
component/hardware boundary intent
state/context fragments
comparison intent
demolition service boundary
DIY/repair fragments
```

### Root cause risk

A successful build can produce a coherent implementation of an incomplete semantic model.

Therefore build success itself cannot be a completion criterion.

---

## Error E — I initially patched some symptoms before fully generalizing the cause

During correction, some failures first appeared as individual phrases.

The wrong response would have been:

```text
add phrase to exception list
rerun
move on
```

Instead, the QA process had to ask what broader class produced the failure.

Examples:

```text
`окно пластиковое закрыто` -> state/context class, not one exact phrase
`ремонт сетки ...` -> component/accessory morphology class, not one exact phrase
`окна rehau официальный` -> navigational/entity class
`окна rehau сравнение` -> comparison class
`...конденсат починить` / `...провисли` -> repair/diagnostic class inside a product family
```

This is now an explicit non-repeat rule: fix the cause/class where defensible, not only the observed example.

---

## Error F — I had to separate cleanup from later Search/page decisions more aggressively

Some phrases are plausibly relevant to the business but cannot be safely accepted into KEEP without resolving intent/business/page boundaries.

Examples of classes:

```text
components/accessories
fittings brands
DIY/procedural questions
technical information
brand/material comparisons
demolition
panoramic architecture/inspiration/real-estate contexts
some repair sub-intents
```

The wrong choices would be either:

```text
accept them as KEEP because they mention windows
```

or:

```text
exclude them because they are not obviously commercial
```

The correct Step-07 state is often REVIEW because ordinary Search and later business/page evidence are the proper tools for resolving them.

---

# 2. Why these errors happened

The central causal chain was:

```text
large row set
→ desire for deterministic scalable processing
→ negative dictionaries / pattern rules
→ arithmetic reconciliation succeeded
→ successful technical output looked complete
→ absence of a known negative signal was allowed to become KEEP
→ hidden semantic false positives remained
```

In other words:

```text
I optimized first for deterministic processing and auditability
but did not initially impose a strong enough positive-evidence definition for semantic acceptance.
```

The old approach answered:

```text
Can I account for and label every row?
```

but the real Step-07 question is:

```text
Is each retained row positively defensible as relevant at this stage,
or should uncertainty remain explicit?
```

Both questions matter. I incorrectly treated the first as sufficient for the second.

---

# 3. How I corrected it

## Correction 1 — KEEP is now a positive state

The corrected rule is:

```text
KEEP -> explicit POSITIVE_* reason required
NO POSITIVE EVIDENCE -> not KEEP
UNCERTAIN BUT PLAUSIBLY RELEVANT -> REVIEW
CLEARLY WRONG -> reason-separated EXCLUDE_*
```

The build explicitly asserts:

```text
keep_requires_positive_reason = true
default_keep_fallthrough = false
```

Historical REVIEW/EXCLUDE rows were not promoted upward during this correction, which prevented the repair from inventing new optimistic acceptance.

---

## Correction 2 — preserve accounting layer, replace semantic decision layer

The trustworthy parts of old Step 07B were not discarded:

```text
source occurrence preservation
exact phrase accounting
provenance
reconciliation
```

The defective semantic acceptance logic was replaced.

This distinction matters because a postmortem should repair the broken layer, not erase valid evidence merely because the overall step had a defect.

---

## Correction 3 — two independent QA gates

The corrected step uses:

```text
A. ACCOUNTING / PROVENANCE QA
B. SEMANTIC QA
```

Semantic QA contains both:

```text
MUST_KEEP
MUST_NOT_KEEP
```

This matters because a correction that only tests false positives can over-clean the corpus and destroy genuinely relevant phrases.

---

## Correction 4 — repeated semantic saturation passes

The corrected candidate was not accepted after the first technically successful build.

The review loop was:

```text
build candidate
→ inspect materially different phrase families
→ find new error class
→ identify root cause/class
→ add/correct class-level rule
→ add adversarial QA control
→ rerun whole corpus
→ repeat
```

Four semantic saturation passes were performed.

The QA itself stopped multiple intermediate builds, including for real morphology/order defects.

---

## Correction 5 — uncertainty moved to REVIEW rather than hidden

Historical output:

```text
KEEP = 1760
REVIEW = 749
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 31
```

Current correction candidate:

```text
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
```

Transitions from historical KEEP:

```text
KEEP -> KEEP = 1388
KEEP -> REVIEW = 369
KEEP -> EXCLUDE_MECHANICAL = 3
```

This is not interpreted as `369 bad keywords discovered`.

It means 369 old KEEP decisions did not meet the stronger positive-evidence standard and are now explicitly deferred for later evidence instead of being presented as certain.

---

## Correction 6 — non-exact duplicates are surfaced, not silently merged

The correction additionally found candidate non-exact duplicate groups using conservative lexical similarity.

They were not automatically merged.

Reason:

```text
lexical similarity != proven same user intent/page ownership
```

Those candidates can be resolved later with stronger semantic/Search evidence.

---

# 4. How Step 07 must be done correctly next time

The following is the required reasoning procedure. It is not a mechanical command list.

## Stage 1 — understand the real goal before touching the rows

First answer:

```text
What does Step 07 need to prove?
What does KEEP mean positively for this frozen business/scope?
Which decisions belong to later Search/page stages rather than cleanup?
```

If KEEP cannot be defined positively before implementation, do not build the classifier yet.

### Why

Without a positive acceptance definition, the pipeline naturally drifts back to `not rejected = retained`.

---

## Stage 2 — research current external methodology for this exact step

Before implementation, search current materials about:

```text
semantic-core cleanup
keyword/search intent
relevance vs business fit
query grouping/duplicates
when SERP evidence is needed
risks of volume-based deletion
```

Use direct sources and state what they support versus what remains project-specific.

Current sources used in this correction:

- Yandex Wordstat: https://yandex.ru/support2/wordstat/ru/interface/new
- Yandex Webmaster targeting/user needs: https://yandex.ru/support/webmaster/en/recommendations/targeting
- Topvisor cleanup methodology: https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/
- Rush Analytics clustering preparation: https://www.rush-analytics.ru/blog/chto-takoe-klasterizacziya-zaprosov
- Ahrefs keyword intent: https://ahrefs.com/blog/keyword-intent/
- Ahrefs clustering: https://ahrefs.com/blog/keyword-clustering/
- Ahrefs keyword mapping: https://ahrefs.com/blog/keyword-mapping/
- Semrush keyword clustering: https://www.semrush.com/blog/keyword-clustering/

### Why

Project rules and scripts are not independent evidence of their own correctness. External methodology must be used to challenge the planned procedure before execution.

---

## Stage 3 — preserve complete source accounting separately from semantic decisions

Create/verify:

```text
source occurrence ledger
exact normalization key
unique exact phrase record
source -> unique phrase mapping
provenance
```

### Why

This ensures semantic correction never destroys acquisition evidence and allows every later decision to be traced back to source data.

---

## Stage 4 — use deterministic rules only where they are actually safe

Safe deterministic operations can include:

```text
exact duplicate accounting
obvious malformed/mechanical noise
explicitly frozen out-of-scope geography where unambiguous
clearly unrelated product/domain intent
```

But deterministic absence of a negative signal is not evidence for KEEP.

### Why

Deterministic filters are strong when the condition itself is explicit; they are weak when completeness of the rule dictionary is unknown.

---

## Stage 5 — require positive evidence for KEEP

Each KEEP must answer:

```text
What user need is expressed?
Why is that need relevant to the accepted business/site scope?
Why is this not merely an unresolved adjacent/technical/navigation/DIY/page-boundary case?
```

Store an explicit positive reason.

### Why

A positive reason makes retention auditable and prevents silent default acceptance.

---

## Stage 6 — use REVIEW as evidence preservation, not as failure

Use REVIEW when:

```text
phrase may be useful/relevant
but intent, business priority, service boundary, page boundary or Search behaviour is not sufficiently established
```

### Why

Step 07 should not guess conclusions that later ordinary Search is specifically intended to resolve.

---

## Stage 7 — do not auto-merge non-exact duplicates

Exact normalized duplicates can be accounted for deterministically.

For spelling/transliteration/token-order/light morphology variants:

```text
surface candidate group
preserve both phrases/provenance
wait for stronger intent/page evidence before merge
```

### Why

Two strings can be close while representing different search tasks, modifiers or page needs.

---

## Stage 8 — adversarial semantic QA

Build QA from both directions.

### MUST_KEEP controls

Use undeniable core cases across major accepted business families.

Purpose:

```text
catch over-cleaning / false negatives
```

### MUST_NOT_KEEP controls

Use known risk classes:

```text
malformed fragments
navigation/entity
technical info
DIY/procedural
components/accessories
brand/material comparisons
state/context fragments
real-estate/inspiration
unproved service boundaries
repair diagnostics inside product families
```

Purpose:

```text
catch false-positive KEEP decisions
```

### Why

A classifier can be consistently wrong while still being deterministic. Adversarial controls test semantics rather than implementation consistency.

---

## Stage 9 — fix the class, not only the phrase

When QA finds a bad decision:

```text
1. identify the general cause;
2. search the corpus for related cases;
3. design the narrowest defensible class-level correction;
4. test whether it harms known-good phrases;
5. rerun the complete corpus;
6. add the discovered failure class to permanent QA.
```

### Why

An exact exception fixes one symptom and leaves the same causal bug elsewhere.

---

## Stage 10 — continue review until error-class discovery saturates

Do not stop because one build succeeds.

Review materially different families after each correction.

Stop only when additional passes are no longer exposing material **new classes** of failure and all declared QA controls pass.

### Why

The goal is not to prove there are zero arguable phrases. The goal is to stop known systematic decision errors from hiding behind technical success.

---

## Stage 11 — acceptance must state remaining limits

A Step-07 PASS must not claim:

```text
final page ownership
final clustering
final architecture
all REVIEW resolved
all non-exact duplicates resolved
SERP evidence already known
```

### Why

Those are later stages. Keeping boundaries explicit prevents cleanup from silently swallowing the rest of the workflow.

---

# 5. Mandatory non-repeat gate for Step 07

Before Step 07 may pass next time:

```text
ALL_SOURCE_OCCURRENCES_ACCOUNTED = true
ALL_UNIQUE_EXACT_PHRASES_CLASSIFIED = true
UNCLASSIFIED = 0
DEFAULT_KEEP_FALLTHROUGH = false
EVERY_KEEP_HAS_POSITIVE_REASON = true
UNCERTAIN_PLAUSIBLE_CASES_CAN_REMAIN_REVIEW = true
LOW_FREQUENCY_ONLY_EXCLUSIONS = 0
ASSOCIATION_AUTO_KEEP = false
NONEXACT_DUPLICATES_AUTO_MERGED = 0
ARITHMETIC_QA = PASS
PROVENANCE_QA = PASS
SEMANTIC_MUST_KEEP_QA = PASS
SEMANTIC_MUST_NOT_KEEP_QA = PASS
KNOWN_PREVIOUS_ERROR_CLASSES_RECHECKED = true
QA_FAILURES_FIXED_AT_CAUSE_LEVEL_WHERE_DEFENSIBLE = true
WHOLE_CORPUS_RERUN_AFTER_RULE_CHANGE = true
LATER_SEARCH_PAGE_DECISIONS_NOT_PRETENDED_COMPLETE = true
```

Technical equivalents are acceptable only if they prove the same concepts.

---

# 6. Current corrected candidate status

Current candidate evidence:

```text
source occurrences = 2965
exact phrase keys = 2840
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
builder QA failures = 0
expanded semantic QA failures = 0
semantic saturation passes = 4
provider requests during correction = 0
provider cost during correction = 0 RUB
```

This document does **not** convert the candidate into final acceptance.

Current truth remains:

```text
CORRECTION_CANDIDATE_READY = true
OWNER_REVIEW_PENDING = true
ROW_LEVEL_CLEANUP_FINAL_ACCEPTANCE = false
NEXT_STEP_ALLOWED = false
```

---

# 7. The lesson to carry forward

The central lesson is not:

```text
remember these exact 72 QA phrases
```

It is:

```text
understand what KEEP is supposed to prove;
separate accounting truth from semantic truth;
search current external methodology before the step;
use rules as evidence aids, not as substitutes for meaning;
prefer explicit REVIEW to false certainty;
when QA finds a failure, understand the causal class and rerun the whole set;
never accept an analytical step merely because the script/workflow succeeded.
```

Canonical non-repeat statement:

```text
DO_NOT_MECHANICALLY_REPEAT_STEP_07_RULES
UNDERSTAND_THE_PRIOR_FAILURE_CAUSE_FIRST
THEN_APPLY_CURRENT_EVIDENCE_AND_METHOD
```
