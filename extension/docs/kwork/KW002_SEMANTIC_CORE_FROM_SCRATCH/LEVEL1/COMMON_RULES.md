# KW-002 — LEVEL 1 COMMON RULES

Status: **ACTIVE / OWNER-AUTHORIZED SCAFFOLD**

Level 1 contains only universal cross-step rules for KW-002. It does not contain current client facts or step-specific execution detail.

## 1. Product identity

KW-002 is a from-scratch semantic-core and planned-site-architecture product for modern Yandex search.

```text
FROM SCRATCH
= do not require an existing semantic core
= do not require an existing final page structure
= do not treat client guesses as search truth
```

The method considers both:

```text
ordinary Yandex organic Search
+
Yandex generative search/answers including Alice AI evidence where decision-relevant
```

AI-search evidence is used to understand user-task orientation, source/page types and whether Search-only page decisions should be changed, enriched or de-risked. It is not an instruction to ask a conversational assistant for SEO advice.

## 2. No artificial keyword-count cap

There is no permanent product rule such as `MAX_FINAL_KEYWORDS = 500`.

The order freezes its own scope. Technical provider batch sizes are execution chunks only.

Forbidden:

```text
truncate a valid semantic family only because a batch limit was reached
pad a weak niche to reach a sales number
sample a large dataset and present the sample as the full result
```

## 3. Evidence before conclusion

For every material claim distinguish:

```text
CLIENT FACT
PROVIDER OBSERVATION
CURRENT SEARCH OBSERVATION
PUBLIC COMPETITOR-PAGE OBSERVATION
AI-SEARCH OBSERVATION
PROJECT DERIVATION / ANALYST JUDGMENT
UNKNOWN / HOLD
```

Never convert one evidence class into another.

Examples:

```text
competitor page contains topic X != people search for X
Wordstat returns phrase X != X belongs to client business
competitor ranks for query Q != every phrase on competitor page ranks
Search overlap != automatic same-page decision
AI answer contains topic X != X requires a new SEO page
```

## 4. Before every major step

Required sequence:

```text
1. state whole-job goal and current step goal;
2. state what has already been completed and what remains;
3. read Level 1 rules;
4. read the current Level 2 step method;
5. read current work/<JOB_ID>/ manifest/flow/evidence;
6. review relevant external methodology when the step requires it;
7. identify inherited KW-001 rules and whether adaptation is required;
8. self-audit for missing evidence, false assumptions and prior-job contamination;
9. explain plainly WHY / WHAT / EXPECTED RESULT to owner;
10. obtain owner authorization when the step gate requires it;
11. execute only that authorized step;
12. preserve the complete result;
13. read back / QA / update job flow;
14. report what changed and what comes next.
```

## 5. Do not automatically agree with owner analytical objections

Owner decisions on scope, authorization, real business facts and commercial priorities are binding.

But an analytical objection must still be checked against evidence before changing the method/result.

```text
OWNER OBJECTION
→ restate disputed point
→ distinguish evidence from assumption
→ recheck method + evidence + external sources
→ classify REAL DEFECT / COMMUNICATION DEFECT / UNCERTAINTY / NO DEFECT
→ change only when justified
```

This rule is inherited from KW-001 `DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md`.

## 6. Bridge state must be explicit before operator commands

Before every Yandex Marketing Bridge command state:

```text
ACTIVE SERVICE
EXECUTION MODE
MATERIAL ADDITIONAL STATE
EXPECTED PROVIDER REQUEST COUNT / BILLABLE STATUS when relevant
```

Do not rely on previous dialogue context to imply the mode.

## 7. Provider success is not project completion

A provider item/step is complete only when:

```text
provider outcome known
+ complete required result preserved
+ count/field/provenance truth verified
+ persisted result readable for next step
```

`HTTP 200`, `SUCCEEDED`, request count or cost record alone is insufficient.

If preservation fails, the next provider item and next analytical step are blocked until recovery.

Inherited from KW-001 evidence-persistence discipline.

## 8. Universal rules, step rules and job data are separate

```text
LEVEL 1 = common reusable rules
LEVEL 2 = reusable step methods
work/<JOB_ID>/ = concrete job truth
```

A job-specific incident may justify proposing a reusable correction, but concrete client names, queries, URLs, counts, request IDs and current-job outcomes must not become permanent Level 1/Level 2 inputs.

Permanent change requires explicit owner authorization.

## 9. Large-data rule

If complete analysis cannot be performed reliably in the ordinary chat context because the dataset is large, the solution is not sampling or truncation.

Use the dedicated `WORK_HANDOFF_RULE.md`.

## 10. Search-only causal freeze before AI-search reconciliation

The method must be able to show what ordinary Search evidence alone would have produced before AI-search evidence is allowed to change the result.

```text
SEARCH-ONLY BASELINE FIRST
→ freeze
→ AI-search evidence
→ compare
→ CHANGE / ENRICH / DE_RISK / NO_CHANGE / HOLD
```

This prevents AI-search evidence from retroactively contaminating the baseline and allows the client/productization test to show whether it added decision value.

## 11. No forced AI delta

A valid outcome is `NO_CHANGE`.

Never create a new page, split a cluster or exaggerate a content requirement merely to prove that Alice AI "changed something".

## 12. Client-facing language

Final client artifacts must explain:

```text
what we researched
why it matters
what we found
how phrases were grouped
which page should answer which demand
what structure is recommended
what ordinary Search showed
what AI-search evidence changed or confirmed
what remains uncertain
```

Internal step IDs, provider protocol names and QA jargon are traceability details, not the main client narrative.

## 13. Stop/hold discipline

If a material conclusion lacks evidence:

```text
DO NOT GUESS
→ HOLD / REVIEW / EVIDENCE_REQUIRED
```

A smaller truthful core is better than a larger invented core.
