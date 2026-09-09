# KW-001 — STEP 3 WORDSTAT ACQUISITION DEPTH JUSTIFICATION GATE

Updated: 2026-09-09  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED / MANDATORY BEFORE WORDSTAT ACQUISITION**

## 0. Authority and scope

This gate is the permanent Step-3 rule for deciding Wordstat acquisition depth in KW-001.

Canonical current methodology numbering:

```text
STEP 2 = seed / acquisition probe plan
STEP 3 = Wordstat/provider acquisition
```

The older `WORKING_RUNBOOK_FOR_CHATGPT.md` uses the legacy label `STEP 4 — Wordstat pass #1`. That legacy section is governed by this gate whenever it performs Wordstat acquisition.

This rule also governs later KW-001 Wordstat acquisition routes that inherit Step-3 acquisition semantics, including Step 3R recovery, Step 5 targeted second acquisition and the Wordstat sub-stage of Step 5A competitor semantic expansion.

Concrete client domains, phrases, counts, selected depth values and current provider receipts belong in the current job/test workspace, not in this universal rule.

---

# 1. OWNER-LOCKED RULE

Before the first material Wordstat provider request of an acquisition step or materially new acquisition revision, ChatGPT must first prove what acquisition depth is required for the current task.

```text
ENTER WORDSTAT ACQUISITION STEP
→ DEFINE THE EXACT INFORMATION QUESTION
→ RESEARCH CURRENT EXTERNAL METHOD / PROVIDER LIMITS
→ COMPARE DEPTH OPTIONS AGAINST CURRENT JOB EVIDENCE
→ JUSTIFY THE REQUIRED DEPTH
→ SHOW THE OWNER THE EVIDENCE + CLICKABLE SOURCES + LIMITATIONS
→ DEPTH JUSTIFICATION GATE = PASS
→ ONLY THEN PROVIDER EXECUTION MAY BEGIN
```

```text
DEPTH CHOSEN FROM MEMORY = FAIL
OLD TEST PAYLOAD SIZE = METHOD RULE = FAIL
TECHNICAL CAPABILITY TEST DEPTH = SEO ACQUISITION DEPTH = FAIL
PROVIDER MAXIMUM = AUTOMATIC PROOF OF SUFFICIENT COVERAGE = FAIL
HTTP 200 / SUCCEEDED = DEPTH WAS ADEQUATE = FAIL
```

Until this gate passes:

```text
WORDSTAT_PROVIDER_EXECUTION_ALLOWED = false
```

---

# 2. WHAT "PROVE THE DEPTH" MEANS

The pre-provider depth justification must explicitly answer all of the following.

```text
1. What exact acquisition question are we resolving?
2. Is this a broad discovery acquisition, a bounded diagnostic probe, a targeted gap check, or a technical capability test?
3. What current Wordstat/provider depth range and result limits are documented now?
4. What does the provider return at the selected depth, and what can remain unobserved beyond that boundary?
5. What existing first-party/search evidence already exists for this site?
6. Does Yandex Webmaster or other allowed owned evidence materially reduce the discovery burden for this particular family?
7. What are the plausible depth options for this task?
8. What evidence would be lost at each shallower option?
9. Why is the selected depth sufficient for the declared question?
10. What truncation/coverage risk remains after the selected depth?
11. What trigger will cause targeted/recursive/deeper acquisition later?
12. What provider-request and cost effect follows from the decision?
```

A number without this reasoning is not a method decision.

---

# 3. EXISTING-SITE KW-001 BOUNDARY

KW-001 usually operates on an existing site. That does **not** create a universal shallow Wordstat depth.

Existing-site evidence may include, when allowed and available:

```text
current public pages / URL families
existing semantic core
current query→URL relationships
Yandex Webmaster query/page evidence
other current first-party search evidence
```

This evidence can make some Wordstat probes narrower because the job may already know part of the vocabulary/search universe.

But:

```text
EXISTING SITE != NUM_PHRASES 20
EXISTING SITE != SHALLOW WORDSTAT BY DEFAULT
KNOWN SITE VOCABULARY != COMPLETE MARKET VOCABULARY
WEBMASTER QUERY HISTORY != PROOF THAT MISSED DEMAND DOES NOT EXIST
```

For a materially important broad family, missed-demand search or semantic-gap acquisition, a shallow result cap must not be used merely because the site already exists.

If a depth materially below the current provider maximum is chosen for a broad acquisition, the job-specific depth report must provide positive evidence that the narrower depth is sufficient for the declared information question and must state what it is intentionally not attempting to discover.

---

# 4. TECHNICAL PROBE VS SEMANTIC ACQUISITION

Small depths are allowed for a bounded technical or capability check when the purpose is transport/operator/runtime validation rather than semantic coverage.

Such a request must be labelled, for example:

```text
TECHNICAL_CAPABILITY_PROBE
OPERATOR_BEHAVIOR_PROBE
TRANSPORT_ACCEPTANCE_PROBE
```

And it must explicitly state:

```text
THIS REQUEST DOES NOT SATISFY SEMANTIC ACQUISITION COMPLETENESS
```

A previous owner-live Bridge test using a small payload can prove lifecycle/transport behavior. It cannot be reused as proof that the same depth is sufficient for a client semantic-core acquisition.

---

# 5. DEPTH IS COVERAGE-DRIVEN, NOT A MAGIC CONSTANT

KW-001 does not freeze one universal `numPhrases` value for every request.

The selected depth depends on the current information question and current external/provider evidence.

Possible patterns include:

```text
NARROW DIAGNOSTIC QUESTION
→ bounded depth may be justified

BROAD IMPORTANT FAMILY / MISSED-DEMAND DISCOVERY
→ deep acquisition is normally required unless current evidence proves otherwise

RETURNED RESULT REACHES PROVIDER DEPTH BOUNDARY
OR
NEW MATERIAL MASKS / VOCABULARY BRANCHES APPEAR
OR
COVERAGE REVIEW FINDS A NAMED GAP
→ targeted second acquisition / deeper branch review
```

```text
FIRST LAYER DEPTH != TOTAL MARKET COMPLETENESS
```

The provider maximum is a collection boundary, not a claim that all possible demand has been enumerated.

---

# 6. FRESH EXTERNAL RESEARCH IS MANDATORY

Before each material Step-3 execution or materially new acquisition revision, re-check current external sources.

Priority:

```text
1. official Yandex Wordstat / Search API documentation
2. official Yandex Webmaster documentation when existing-site owned-query evidence is relevant
3. current high-quality SEO collection methodology / tooling documentation
4. controlled project evidence for Bridge capability only
5. analyst heuristic only when explicitly labelled
```

The job-specific report must preserve:

```text
METHOD ELEMENT
→ SOURCE
→ WHAT EXACTLY THE SOURCE SUPPORTS
→ CURRENT JOB-SPECIFIC INTERPRETATION
→ SELECTED DEPTH / EXECUTABLE ACTION
```

Current baseline references that should be revalidated rather than blindly copied include:

```text
https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop
https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-gettop
https://yandex.ru/support2/wordstat/ru/
https://yandex.ru/support2/wordstat/ru/content/operators
https://yandex.ru/support/webmaster/ru/service/popular-queries
```

Industry sources may corroborate deep/recursive collection practice, but they do not override current official provider contracts.

---

# 7. REQUIRED JOB-SPECIFIC ARTIFACT

Before provider execution, the current job/test workspace must materialize a depth decision record equivalent to:

```text
WORDSTAT_DEPTH_JUSTIFICATION_<DATE>.md
```

It must contain at minimum:

```text
STEP / ACQUISITION REVISION
JOB MODE = EXISTING_SITE / other explicitly declared mode
EXACT QUESTION
SEED / FAMILY CLASS
CURRENT PROVIDER DEPTH LIMIT
CANDIDATE DEPTH OPTIONS
EXISTING FIRST-PARTY / WEBMASTER EVIDENCE AVAILABLE
SELECTED DEPTH
WHY SELECTED
WHY SHALLOWER DEPTH IS OR IS NOT SUFFICIENT
KNOWN COVERAGE / TRUNCATION LIMITATION
SECOND-ACQUISITION TRIGGER
EXPECTED REQUEST COUNT
EXPECTED COST EFFECT
FRESH SOURCES + CLICKABLE LINKS
OWNER-FACING EXPLANATION DELIVERED
DEPTH_GATE_VERDICT
```

---

# 8. OWNER-FACING DISCLOSURE IS PART OF THE GATE

The depth proof is not allowed to exist only in an internal file.

Before the first material provider request, ChatGPT must explain to the owner in plain language:

```text
what depth is proposed
why this depth is required for this exact task
why a smaller depth would or would not be safe
what evidence/source supports the decision
what provider limit remains
what additional acquisition may still be required later
```

Clickable source links must be included.

```text
INTERNAL DEPTH NOTE ONLY = FAIL
OWNER-FACING PROOF MISSING = FAIL
```

---

# 9. PASS / FAIL GATE

PASS requires:

```text
EXACT_INFORMATION_QUESTION_DEFINED = true
CURRENT_EXTERNAL_DEPTH_RESEARCH = PASS
OFFICIAL_PROVIDER_LIMITS_RECHECKED = true
EXISTING_SITE_FIRST_PARTY_EVIDENCE_CONSIDERED_WHEN_AVAILABLE = true
CANDIDATE_DEPTH_OPTIONS_COMPARED = true
SELECTED_DEPTH_EXPLICIT = true
SHALLOWER_DEPTH_RISK_EXPLICIT = true
COVERAGE_TRUNCATION_BOUNDARY_EXPLICIT = true
SECOND_ACQUISITION_TRIGGER_EXPLICIT = true
REQUEST_COST_EFFECT_EXPLICIT = true
SOURCE_TO_DEPTH_TRACE_COMPLETE = true
OWNER_FACING_DEPTH_PROOF_DELIVERED = true
TECHNICAL_PROBE_NOT_MISLABELLED_AS_SEMANTIC_COMPLETENESS = true
```

Only then:

```text
WORDSTAT_DEPTH_JUSTIFICATION_GATE = PASS
WORDSTAT_PROVIDER_EXECUTION_ALLOWED = true
```

Any missing hard condition means:

```text
WORDSTAT_DEPTH_JUSTIFICATION_GATE = FAIL / HOLD
WORDSTAT_PROVIDER_EXECUTION_ALLOWED = false
```

---

# 10. NON-REPEAT LESSON

### WHAT FAILED BEFORE

A small Wordstat response depth used in Bridge owner-live acceptance could be discussed too close to a reusable SEO acquisition depth.

### WHY

```text
TRANSPORT TEST CONFIGURATION
WAS CONFUSED WITH
SEMANTIC-COVERAGE METHODOLOGY
```

### NON-REPEAT CONTROL

Never inherit a depth number from a technical test or a previous client job. Prove the current depth before the current acquisition.

### HOW TO VERIFY

Before provider execution, inspect the current job-specific depth-justification artifact and owner-facing source disclosure. If either is missing, execution is blocked.

---

# 11. PLAIN-LANGUAGE RULE

Before Wordstat collection starts, first answer one question convincingly:

> **How deep do we need to collect Wordstat for this exact job so that we do not knowingly throw away material search demand?**

Only after that answer is supported by current sources, current site evidence and an explicit coverage boundary may the collection begin.
