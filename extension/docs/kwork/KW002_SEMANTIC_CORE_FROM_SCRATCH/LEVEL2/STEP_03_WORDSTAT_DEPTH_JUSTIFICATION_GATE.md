# KW-002 — LEVEL 2 / STEP 03 WORDSTAT DEPTH JUSTIFICATION GATE

Updated: 2026-09-09  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED / MANDATORY BEFORE WORDSTAT ACQUISITION**

## 0. Purpose

This is the mandatory Level-2 gate for KW-002 Step 03 primary Wordstat acquisition.

It also governs later KW-002 Wordstat acquisition stages that inherit Step-03 acquisition semantics:

```text
STEP 05 = targeted expansion / coverage control
STEP 08 = competitor-derived Wordstat expansion
```

Concrete client values, seed phrases, selected depth, provider results, request IDs, row counts and costs belong only in `work/<JOB_ID>/`.

---

# 1. OWNER-LOCKED EXECUTION ORDER

Before the first material Wordstat provider request of Step 03 or any materially new acquisition revision, ChatGPT must first prove the required acquisition depth for the current job.

```text
ENTER STEP 03
→ DEFINE EXACT ACQUISITION QUESTION
→ RESEARCH CURRENT WORDSTAT / PROVIDER DEPTH CONTRACT
→ REVIEW CURRENT GREENFIELD INPUT + AVAILABLE EVIDENCE
→ COMPARE DEPTH OPTIONS
→ JUSTIFY REQUIRED DEPTH
→ SHOW OWNER PLAIN-LANGUAGE PROOF + CLICKABLE SOURCES + LIMITATIONS
→ DEPTH JUSTIFICATION GATE = PASS
→ ONLY THEN WORDSTAT PROVIDER EXECUTION
```

Until this gate passes:

```text
WORDSTAT_PROVIDER_EXECUTION_ALLOWED = false
```

Forbidden shortcuts:

```text
DEPTH CHOSEN FROM MEMORY = FAIL
PREVIOUS JOB DEPTH COPIED WITHOUT RESEARCH = FAIL
TECHNICAL BRIDGE TEST DEPTH = SEMANTIC ACQUISITION DEPTH = FAIL
PROVIDER MAXIMUM = AUTOMATIC PROOF OF TOTAL COVERAGE = FAIL
SMALLER DEPTH CHOSEN ONLY TO FIT CHAT / TRANSPORT LIMIT = FAIL
HTTP 200 / SUCCEEDED = DEPTH WAS ADEQUATE = FAIL
```

---

# 2. WHAT MUST BE PROVED

The Step-03 pre-provider depth justification must answer:

```text
1. What exact semantic-acquisition question is Step 03 resolving?
2. Is this broad greenfield discovery, a bounded diagnostic probe, a targeted gap check, or a technical capability test?
3. What current Wordstat/provider result-depth range and hard limits are documented now?
4. What provider fields/rows are returned at the selected depth?
5. What can remain unobserved beyond the provider result boundary?
6. What client/business vocabulary is known before search research?
7. What search vocabulary is still unknown because this is a greenfield job?
8. What candidate depths are plausible for the current seed/family class?
9. What material evidence would be lost at each shallower option?
10. Why is the selected depth sufficient for the declared first-pass question?
11. What truncation / saturation / coverage risk remains?
12. What condition triggers Step 05 or another targeted expansion?
13. What provider-request and cost effect follows from the decision?
```

A number such as `20`, `50`, `500`, `1000` or `2000` without this reasoning is not a valid method decision.

---

# 3. GREENFIELD BURDEN OF PROOF

KW-002 starts from a new-site condition unless the current job explicitly says otherwise.

Normally there is no existing owned query history or existing query→URL map to reveal the market vocabulary.

Therefore:

```text
NEW SITE
+ NO OWN SEARCH HISTORY
→ HIGH DISCOVERY BURDEN
```

This does not hard-code one universal depth number forever. It does mean that a shallow primary acquisition requires stronger positive justification because the job cannot rely on an existing site's historical query universe to compensate for missed discovery.

```text
GREENFIELD != NUM_PHRASES 20
GREENFIELD != SHALLOW PRIMARY ACQUISITION BY DEFAULT
CLIENT PRODUCT NAME != COMPLETE SEARCH VOCABULARY
SEED LIST != COMPLETE MARKET VOCABULARY
```

For broad primary discovery, if the job selects a depth materially below the current provider maximum, the job-specific report must state:

```text
what evidence is intentionally not being requested
why that omitted evidence is unlikely to change the current acquisition decision
how the missing-coverage risk will be detected later
```

If this cannot be defended, the shallow depth fails the gate.

---

# 4. TECHNICAL PROBE IS NOT SEMANTIC COMPLETENESS

A small depth may be used for a technical/capability check, for example:

```text
OPERATOR_BEHAVIOR_PROBE
TRANSPORT_ACCEPTANCE_PROBE
BRIDGE_CAPABILITY_PROBE
```

But that request must be labelled as such and must explicitly state:

```text
THIS REQUEST DOES NOT SATISFY STEP-03 SEMANTIC ACQUISITION COMPLETENESS
```

A successful small test proves only the tested technical behavior.

It does not prove that the same depth is sufficient for the greenfield semantic-core acquisition.

---

# 5. DEPTH IS A COVERAGE DECISION, NOT A MAGIC CONSTANT

The selected depth must follow the information question.

Typical logic:

```text
BOUNDED TECHNICAL / DIAGNOSTIC QUESTION
→ bounded depth may be justified

BROAD PRIMARY GREENFIELD DISCOVERY
→ deep acquisition is normally required unless current evidence proves a smaller depth is sufficient

RESULT REACHES PROVIDER DEPTH BOUNDARY
OR
NEW MATERIAL MASKS / VOCABULARY BRANCHES APPEAR
OR
STEP 04 FINDS A NAMED COVERAGE GAP
→ STEP 05 TARGETED EXPANSION

COMPETITOR RESEARCH FINDS GENUINELY NEW DEMAND DIRECTION
→ STEP 08 WORDSTAT EXPANSION UNDER THIS SAME DEPTH GATE
```

```text
FIRST GETTOP LAYER != COMPLETE MARKET UNIVERSE
PROVIDER MAXIMUM != PROOF OF SEMANTIC SATURATION
```

---

# 6. FRESH EXTERNAL RESEARCH REQUIRED

Before each material Step-03 execution or materially new acquisition revision, perform fresh current research specifically about acquisition depth and provider limits.

Priority:

```text
1. official Yandex Wordstat / Search API documentation
2. official Yandex Wordstat operator / product documentation
3. current high-quality SEO collection / deep-parsing methodology
4. controlled Bridge capability evidence only for tool behavior
5. analyst heuristic only when explicitly marked
```

The job-specific source trace must be:

```text
METHOD ELEMENT
→ SOURCE
→ WHAT EXACTLY SOURCE SUPPORTS
→ CURRENT GREENFIELD INTERPRETATION
→ SELECTED DEPTH / EXECUTABLE ACTION
```

Current baseline references that must be revalidated rather than copied blindly include:

```text
https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop
https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-gettop
https://yandex.ru/support2/wordstat/ru/
https://yandex.ru/support2/wordstat/ru/content/operators
```

Industry deep/recursive collection sources may corroborate the method but do not override the current official provider contract.

---

# 7. REQUIRED JOB-SPECIFIC ARTIFACT

Before the first material provider request, `work/<JOB_ID>/` must contain a depth decision record equivalent to:

```text
STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_<DATE>.md
```

For a restarted/revised acquisition after a material transport/provider/method change, create a new revision rather than silently reusing the old depth note.

Minimum fields:

```text
STEP / ACQUISITION REVISION
JOB MODE = GREENFIELD / explicitly declared alternative
EXACT ACQUISITION QUESTION
SEED / FAMILY CLASS
CURRENT PROVIDER DEPTH LIMIT
CANDIDATE DEPTH OPTIONS
SELECTED DEPTH
WHY SELECTED
WHY SHALLOWER DEPTH IS OR IS NOT SUFFICIENT
KNOWN COVERAGE / TRUNCATION LIMITATION
STEP-05 / STEP-08 EXPANSION TRIGGER
EXPECTED REQUEST COUNT
EXPECTED COST EFFECT
FRESH SOURCES + CLICKABLE LINKS
OWNER-FACING EXPLANATION DELIVERED
DEPTH_GATE_VERDICT
```

---

# 8. OWNER-FACING PROOF IS MANDATORY

The depth decision is not allowed to remain only inside the repository.

Before the first material Wordstat provider request, ChatGPT must explain to the owner in plain language:

```text
what depth is proposed
why this exact greenfield task needs it
why a smaller depth would or would not be safe
which current sources support that decision
what provider/result boundary remains
what later expansion may still be needed
```

Clickable source links are required.

```text
INTERNAL DEPTH NOTE ONLY = FAIL
OWNER-FACING DEPTH PROOF MISSING = FAIL
```

---

# 9. CHATGPT WORK / LARGE-DATA BOUNDARY

Acquisition depth must never be reduced merely because the complete returned dataset is inconvenient for ordinary-chat context.

```text
LARGE RESULT
!= LOWER EVIDENCE DEPTH
```

If the selected methodologically justified depth creates a large full-row dataset:

```text
KEEP THE DEPTH
→ PERSIST COMPLETE RAW RESULT
→ USE LEVEL1 WORK HANDOFF WHEN FULL UNION / ROW-LEVEL PROCESSING RISKS CHAT TRUNCATION
```

Do not trade evidence completeness for chat convenience.

---

# 10. PASS / FAIL GATE

PASS requires:

```text
EXACT_INFORMATION_QUESTION_DEFINED = true
CURRENT_EXTERNAL_DEPTH_RESEARCH = PASS
OFFICIAL_PROVIDER_LIMITS_RECHECKED = true
GREENFIELD_DISCOVERY_BURDEN_EXPLICIT = true
CANDIDATE_DEPTH_OPTIONS_COMPARED = true
SELECTED_DEPTH_EXPLICIT = true
SHALLOWER_DEPTH_RISK_EXPLICIT = true
COVERAGE_TRUNCATION_BOUNDARY_EXPLICIT = true
TARGETED_EXPANSION_TRIGGER_EXPLICIT = true
REQUEST_COST_EFFECT_EXPLICIT = true
SOURCE_TO_DEPTH_TRACE_COMPLETE = true
OWNER_FACING_DEPTH_PROOF_DELIVERED = true
TECHNICAL_PROBE_NOT_MISLABELLED_AS_SEMANTIC_COMPLETENESS = true
LARGE_DATA_NOT_USED_AS_REASON_TO_REDUCE_DEPTH = true
```

Only then:

```text
STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE = PASS
WORDSTAT_PROVIDER_EXECUTION_ALLOWED = true
```

Otherwise:

```text
STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE = FAIL / HOLD
WORDSTAT_PROVIDER_EXECUTION_ALLOWED = false
```

---

# 11. CURRENT BLOOD & SAND REHEARSAL APPLICATION

This universal rule applies to the current `BLOOD_SAND_GREENFIELD_2026-09-08` job for any new Step-03 acquisition revision after the current Bridge transport blocker is repaired.

The historical blocked Step-03 V1 remains historical evidence and is not retroactively rewritten.

Before a new acquisition revision begins:

```text
RESEARCH CURRENT DEPTH METHOD AGAIN
→ MATERIALIZE NEW JOB-SPECIFIC DEPTH JUSTIFICATION
→ SHOW OWNER THE PROOF + SOURCES
→ PASS THIS GATE
→ ONLY THEN START NEW WORDSTAT PROVIDER LINEAGE
```

---

# 12. NON-REPEAT LESSON

### WHAT FAILED BEFORE

A small Wordstat depth used for Bridge owner-live/capability testing could be discussed as if it might be a sufficient semantic-acquisition depth.

### WHY

```text
TECHNICAL TEST PAYLOAD
WAS CONFUSED WITH
SEMANTIC DISCOVERY COVERAGE
```

### NON-REPEAT CONTROL

Never inherit acquisition depth from a Bridge acceptance test, a previous job or memory. Prove the depth at Step 03 before provider execution.

### HOW TO VERIFY

No material Wordstat acquisition request is allowed unless the current job has both:

```text
CURRENT DEPTH JUSTIFICATION ARTIFACT
+ OWNER-FACING SOURCE-BACKED DEPTH PROOF
```

---

# 13. PLAIN-LANGUAGE RULE

Before collecting Wordstat for a new site, first prove:

> **How deep do we need to collect this market now so that we do not deliberately throw away material vocabulary before we have even discovered it?**

Only after that proof may Step 03 execute provider requests.
