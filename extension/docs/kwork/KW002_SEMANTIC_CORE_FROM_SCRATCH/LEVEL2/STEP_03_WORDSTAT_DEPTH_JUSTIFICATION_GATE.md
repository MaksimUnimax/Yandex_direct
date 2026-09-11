# KW-002 — LEVEL 2 / STEP 03 WORDSTAT DEPTH JUSTIFICATION GATE

Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED / MANDATORY BEFORE MATERIAL WORDSTAT ACQUISITION**
Applies to: any KW-002 site/job using Wordstat in Step03 and inherited later acquisition stages.

Companion universal authorities:

- `../LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`
- `../LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`

## 0. Purpose

This gate prevents arbitrary provider-depth selection.

Step03 must prove that its selected Wordstat result depth is appropriate for the **current acquisition question**, rather than copying a number from a technical test, a prior job, a provider maximum, memory or chat convenience.

The same logic also governs materially new Wordstat acquisition in later steps such as targeted expansion and competitor-derived expansion.

Concrete client values, selected depth, exact seeds, request IDs, row counts and costs belong only in `work/<JOB_ID>/`.

---

## 1. Universal root cause this gate prevents

### Failure mechanism — technical/provider parameter mistaken for semantic coverage decision

A provider exposes a configurable result depth and hard maximum. It is easy to choose:

- a small value because a transport/capability test succeeded;
- a convenient value because it fits chat/context;
- the maximum because “more is safer”;
- a prior-job value because it worked before.

All four shortcuts are methodologically invalid.

### Why it fails

Provider depth controls **what evidence is observable**, not whether the market has been semantically saturated. Different acquisition questions have different information needs.

```text
TECHNICAL SUCCESS != SEMANTIC COVERAGE
PROVIDER MAXIMUM != PROOF OF MARKET COMPLETENESS
PREVIOUS JOB DEPTH != CURRENT JOB DEPTH JUSTIFICATION
CHAT CONVENIENCE != EVIDENCE METHOD
```

### Universal anti-regression rule

Depth is selected from the declared information question, expected vocabulary uncertainty, provider contract and explicit truncation/saturation risk.

---

## 2. Mandatory execution order

Before the first material Wordstat request of Step03 or any materially new acquisition revision:

```text
DEFINE EXACT ACQUISITION QUESTION
→ RESEARCH CURRENT WORDSTAT/PROVIDER DEPTH CONTRACT
→ REVIEW CURRENT FROZEN BUSINESS INPUT + EXISTING EVIDENCE
→ COMPARE PLAUSIBLE DEPTH OPTIONS
→ STATE WHAT EACH OPTION MAY MISS
→ JUSTIFY SELECTED DEPTH
→ STATE EXPANSION/TRUNCATION TRIGGERS
→ DISCLOSE SOURCES + LIMITATIONS TO OWNER
→ DEPTH GATE PASS
→ ONLY THEN EXECUTE PROVIDER
```

Until PASS:

```text
WORDSTAT_PROVIDER_EXECUTION_ALLOWED = false
```

---

## 3. What must be proved

The job-specific depth record must answer:

```text
1. What exact acquisition question is being resolved?
2. Is this broad discovery, bounded diagnostic, targeted gap check, or technical test?
3. What current provider depth range/hard limits are documented now?
4. What fields/rows are returned at the selected depth?
5. What may remain unobserved beyond the returned boundary?
6. What business vocabulary is known before search research?
7. What search vocabulary remains unknown?
8. What candidate depths are plausible for this query/seed class?
9. What material evidence may be lost at each shallower option?
10. Why is the selected depth sufficient for this declared question?
11. What truncation/saturation risk remains?
12. What condition triggers targeted expansion?
13. What request-count/cost consequence follows?
```

A number without this reasoning is not a valid method decision.

---

## 4. Discovery burden depends on evidence state, not client niche

For a greenfield site or any business with little/no owned search history:

```text
LOW OWN SEARCH HISTORY
+ UNKNOWN MARKET VOCABULARY
→ HIGHER DISCOVERY BURDEN
```

For a bounded diagnostic question with already narrow evidence needs, shallower depth may be appropriate.

No fixed universal depth is encoded.

If a broad discovery stage chooses materially less than the provider's available depth, the job-specific record must explain:

```text
what evidence is intentionally not requested
why omission is unlikely to change the current decision
how missed-coverage risk will be detected later
```

If that cannot be defended, the selected depth fails.

---

## 5. Technical probe is not semantic completeness

A small request may be used to test:

```text
OPERATOR BEHAVIOR
TRANSPORT ACCEPTANCE
BRIDGE CAPABILITY
SCHEMA/PARSER COMPATIBILITY
```

Such a request must be labelled as a technical/diagnostic probe and cannot satisfy broad semantic-acquisition completeness by itself.

Required statement:

```text
TECHNICAL_PROBE_COMPLETED = true
SEMANTIC_ACQUISITION_COMPLETENESS_PROVED_BY_THIS_PROBE = false
```

unless the acquisition question itself was explicitly only the bounded technical diagnostic.

---

## 6. Depth is a coverage decision, not a magic constant

Generic logic:

```text
BOUNDED DIAGNOSTIC QUESTION
→ bounded depth may be justified

BROAD PRIMARY DISCOVERY
→ deeper acquisition normally requires consideration

RESULT REACHES DEPTH BOUNDARY
OR
NEW MATERIAL VOCABULARY BRANCHES APPEAR
OR
LATER FAMILY TRIAGE FINDS A NAMED GAP
→ TARGETED EXPANSION CANDIDATE
```

Even a maximum-depth response may not represent the complete semantic market universe.

---

## 7. Fresh external research required

Before each material acquisition revision, re-check current provider behavior/limits.

Priority:

```text
1. official Yandex Wordstat/Search API documentation
2. official Wordstat operator/product documentation
3. current high-quality collection methodology
4. controlled Bridge evidence for tool behavior only
5. analyst heuristic, explicitly marked
```

Baseline references to revalidate:

- https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop
- https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-gettop
- https://yandex.ru/support2/wordstat/ru/
- https://yandex.ru/support2/wordstat/ru/content/operators

Job-specific source trace:

```text
METHOD ELEMENT
→ SOURCE
→ WHAT SOURCE SUPPORTS
→ CURRENT JOB INTERPRETATION
→ SELECTED DEPTH / ACTION
```

---

## 8. Required job-specific artifact

Before the first material request, `work/<JOB_ID>/` must contain a depth decision record, e.g.:

`STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_<DATE>.md`

Minimum fields:

```text
STEP / ACQUISITION REVISION
JOB MODE
EXACT ACQUISITION QUESTION
SEED/FAMILY CLASS
CURRENT PROVIDER DEPTH LIMIT
CANDIDATE DEPTH OPTIONS
SELECTED DEPTH
WHY SELECTED
WHY SHALLOWER/DEEPER OPTIONS WERE REJECTED
KNOWN COVERAGE/TRUNCATION LIMITATION
EXPANSION TRIGGER
EXPECTED REQUEST COUNT
EXPECTED COST EFFECT
FRESH SOURCES
OWNER-FACING EXPLANATION DELIVERED
DEPTH_GATE_VERDICT
```

A materially revised acquisition creates a new revision instead of silently reusing the old note.

---

## 9. Owner-facing proof

Before material provider execution, explain in plain language:

```text
what depth is proposed
why the current information question needs it
why smaller/larger alternatives were rejected
what sources support the provider assumptions
what remains unobserved
what later expansion may still be required
```

This explanation is job-specific and belongs in the current execution conversation/job evidence, not in Level2.

---

## 10. Large-data boundary

Acquisition depth must never be reduced merely because the result is inconvenient for ordinary chat.

```text
LARGE RESULT != LOWER EVIDENCE DEPTH
```

If justified depth produces large output:

```text
KEEP JUSTIFIED DEPTH
→ PERSIST COMPLETE RAW
→ USE WORK/LARGE-DATA PIPELINE FOR TRANSFORMATION
```

---

## 11. PASS / FAIL

PASS requires:

```text
EXACT_INFORMATION_QUESTION_DEFINED = true
CURRENT_EXTERNAL_DEPTH_RESEARCH = PASS
OFFICIAL_PROVIDER_LIMITS_RECHECKED = true
DISCOVERY_BURDEN_EXPLICIT = true
CANDIDATE_DEPTH_OPTIONS_COMPARED = true
SELECTED_DEPTH_EXPLICIT = true
ALTERNATIVE_DEPTH_RISKS_EXPLICIT = true
COVERAGE_TRUNCATION_BOUNDARY_EXPLICIT = true
TARGETED_EXPANSION_TRIGGER_EXPLICIT = true
REQUEST_COST_EFFECT_EXPLICIT = true
SOURCE_TO_DEPTH_TRACE_COMPLETE = true
OWNER_FACING_DEPTH_PROOF_DELIVERED = true
TECHNICAL_PROBE_NOT_MISLABELLED_AS_SEMANTIC_COMPLETENESS = true
LARGE_DATA_NOT_USED_AS_REASON_TO_REDUCE_DEPTH = true
JOB_SPECIFIC_VALUES_IN_LEVEL2 = 0
```

Only then:

```text
STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE = PASS
WORDSTAT_PROVIDER_EXECUTION_ALLOWED = true
```

Otherwise provider execution remains blocked.

---

## 12. Plain-language universal rule

Before collecting Wordstat, first prove:

> How deep must this specific acquisition question be measured now so that we do not deliberately discard material vocabulary or waste collection volume without information gain?
