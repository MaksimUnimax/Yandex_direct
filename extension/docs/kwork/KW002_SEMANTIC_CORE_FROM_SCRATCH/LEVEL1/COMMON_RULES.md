# KW-002 — LEVEL 1 COMMON RULES INDEX

Status: **ACTIVE / OWNER-AUTHORIZED / OWNER-LOCKED**

This file is the Level-1 entry point for KW-002.

## 0. Canonical inheritance rule

The previously shortened KW-002 common-rule scaffold is **not sufficient by itself**.

Canonical inherited universal authority:

`INHERITED_KW001_UNIVERSAL_RULES.md`

It contains the actual reusable rules transferred from KW-001, including their purpose, failure class/root cause and pass boundary.

```text
DO NOT REDUCE AN INHERITED RULE TO A FILE REFERENCE OR ONE-LINE LABEL.
DO NOT RE-INVENT A RULE THAT KW-001 HAS ALREADY EARNED/CORRECTED.
DO NOT APPLY A KW-001 JOB-SPECIFIC VALUE AS A KW-002 UNIVERSAL RULE.
```

For KW-002 documentation hierarchy:

```text
LEVEL 1 = general universal Kwork rules
LEVEL 2 = universal rules/method for concrete roadmap steps
work/<JOB_ID>/ = concrete order data/evidence/status/artifacts
```

The older KW-001 terminology that called current-job workspace `Level 2` is not used as KW-002 documentation terminology.

---

# 1. Mandatory Level-1 authorities

Before every major KW-002 step read:

```text
1. INHERITED_KW001_UNIVERSAL_RULES.md
2. RESULT_QUALITY_SCORING_RULE.md
3. METHOD_SOURCE_AND_EVIDENCE_RULES.md
4. CLIENT_INTAKE_AND_SCOPE_RULE.md when client/scope facts are material
5. JOB_DATA_SEPARATION_AND_LIFECYCLE.md
6. WORK_HANDOFF_RULE.md when large-data risk exists
7. current Level-2 step method
8. current work/<JOB_ID>/ manifest/flow/evidence
```

The inherited and owner-added Level-1 authority includes, at minimum:

```text
GOAL-FIRST BEFORE METHOD/EXECUTION
FULL ROADMAP BEFORE/AFTER EVERY MAJOR STEP
COMPLETED + REMAINING STATUS TRUTH
PLAIN-LANGUAGE WHY/WHAT/RESULT SUMMARY
FRESH REREAD OF PRIOR ERRORS + NON-REPEAT CONTROLS
METHOD ORIGIN CLASSIFICATION
SOURCE→METHOD TRACEABILITY
RESEARCH→EXECUTION SCHEMA
INFORMATION-GAIN JUSTIFICATION FOR NEW PROVIDER CALLS
QUALITY > PROVIDER-COST MINIMIZATION
EXPLICIT BRIDGE SERVICE/MODE BEFORE COMMANDS
PROVIDER SUCCESS != PROJECT COMPLETION
COMPLETE RETURNED EVIDENCE PERSISTENCE + READBACK BEFORE NEXT PROVIDER ACTION
OWNER ANALYTICAL OBJECTION != AUTOMATIC METHOD REVERSAL
PERMANENT METHOD OWNER-LOCK
JOB DATA MUST NOT CONTAMINATE UNIVERSAL RULES
MATERIAL AUTHORITY MUTATION INVALIDATES DEPENDENT PASS
UNCERTAINTY CONTINUITY
CONCRETE STEP MUST EMBED ITS OWN GATES
END-OF-STEP QUANTITATIVE ACCOUNTING
MANDATORY 10-POINT RESULT QUALITY SCORE
QUALITY_SCORE >= 9/10 + ALL HARD GATES FOR PASS
LATE REVIEW MAY INVALIDATE AN OLD PASS/SCORE
NEXT_STEP_ALLOWED EXPLICIT DECISION
JOB CLOSE ONLY AFTER HANDOFF/REVISIONS/PENDING ACTIONS CLOSED
```

---

# 2. KW-002 product identity

KW-002 builds a semantic core and planned site architecture **from scratch** for modern Yandex.

```text
FROM SCRATCH
= no existing semantic core required
= no existing final site structure required
= client guesses do not become search truth
```

The method considers:

```text
ordinary Yandex organic Search
+
Yandex generative search/answers including Alice AI evidence where decision-relevant
```

AI-search evidence is evidence about how modern Yandex answers/frames user tasks and what source/page types it uses. It is **not** asking a conversational assistant how SEO should be done.

---

# 3. No universal keyword-count cap

There is no permanent rule `MAX_FINAL_KEYWORDS = 500`.

```text
RAW CANDIDATES = as many as evidence collection legitimately produces inside frozen business/scope
FINAL CORE = all retained phrases that survive the method and belong to the sold/frozen order scope
BRIDGE BATCH LIMIT = execution chunk only
```

Forbidden:

```text
truncate a valid family because one batch is full
pad a weak niche to hit a sales number
sample a large dataset and call it complete
```

When complete large-data processing is unsafe in ordinary chat, apply `WORK_HANDOFF_RULE.md`.

---

# 4. Evidence classes must remain separate

For material claims distinguish:

```text
CLIENT FACT
PROVIDER OBSERVATION
CURRENT SEARCH OBSERVATION
PUBLIC COMPETITOR-PAGE OBSERVATION
AI-SEARCH OBSERVATION
PROJECT DERIVATION / ANALYST JUDGMENT
UNKNOWN / HOLD
```

Never convert one class into another.

Examples:

```text
competitor page topic != proven demand
Wordstat phrase != business relevance
competitor visible for one query != full competitor keyword universe
SERP overlap != automatic same-page decision
AI answer topic != automatic new SEO page
```

---

# 5. Search-only baseline before AI-search reconciliation

KW-002 must first be capable of showing what ordinary Yandex Search evidence alone produces.

```text
SEARCH-ONLY SEMANTIC/PAGE ARCHITECTURE
→ FREEZE
→ AI-SEARCH EVIDENCE
→ COMPARISON
→ CHANGE | ENRICH | DE_RISK | NO_CHANGE | HOLD
```

AI evidence must not retroactively contaminate the baseline.

A supported `NO_CHANGE` is a valid result; do not force a split/new page/content requirement just to manufacture AI value.

---

# 6. Client-facing output rule

Final artifacts must tell the client, in ordinary language:

```text
what was researched
what demand was found
what was removed and why
how queries were grouped
which page should answer which group
what site structure follows
what competitor evidence added
what ordinary Yandex Search showed
what AI-search evidence changed/confirmed/did not prove
what remains uncertain
```

Internal IDs/protocol/status vocabulary is secondary traceability, not the client narrative.

---

# 7. Fail-closed truthfulness

If a material decision lacks evidence:

```text
DO NOT GUESS
→ HOLD / REVIEW / SEARCH_REQUIRED / EVIDENCE_REQUIRED / DEFERRED
```

Output completeness must not erase truthful uncertainty.

---

# 8. Mandatory 10-point result quality scoring

Canonical authority:

`RESULT_QUALITY_SCORING_RULE.md`

After every major step/rework/deliverable, score the result on a 0–10 scale and explain the lost points.

```text
PASS REQUIRES QUALITY_SCORE >= 9.0 / 10
AND ALL HARD PASS GATES
AND NO OPEN CRITICAL DEFECT
```

A later external/owner/recipient review may invalidate an earlier PASS and require rescoring/rework.

The score must be shown both in durable QA/state and in the owner-facing chat summary.

---

## Marker

```text
KW002_LEVEL1_CANONICAL_INHERITED_RULE_AUTHORITY = INHERITED_KW001_UNIVERSAL_RULES.md
KW002_RESULT_QUALITY_SCORE_AUTHORITY = RESULT_QUALITY_SCORING_RULE.md
KW002_SHORT_RULE_SUMMARY_DOES_NOT_REPLACE_INHERITED_RULES = true
KW002_LEVEL1_OWNER_LOCKED = true
```
