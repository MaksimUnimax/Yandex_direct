# KW-002 — ROADMAP AND METHOD GENERALIZATION RULE

Status: **OWNER-MANDATED / UNIVERSAL / ACTIVE**
Decision date: 2026-09-11
Applies to: every KW-002 job, every Level-1 rule, every Level-2 roadmap/method file, every Main ChatGPT/Work handoff.

## 1. Core architecture

KW-002 documentation has three non-interchangeable layers:

```text
LEVEL1 = universal product/process rules and universal root causes
LEVEL2 = universal roadmap steps and step methods for ANY eligible site/business
work/<JOB_ID>/ = concrete client facts, examples, IDs, counts, evidence, statuses and corrections
```

A future analyst must be able to execute Level1+Level2 on a completely unrelated site without knowing the job that first produced a lesson.

## 2. Universal-roadmap test

Every Level-2 step must pass this test:

> If all client names, product names, family IDs, row counts, request IDs and historical project details are removed, does the step still explain WHY it exists, WHAT evidence it consumes, HOW it operates, WHAT it creates and WHAT PASS means?

If no, the Level-2 document is contaminated by job-specific material and must be rewritten.

## 3. What belongs in Level 1

Allowed:

- universal root cause of a failure class;
- universal anti-regression principle;
- generic data/evidence boundaries;
- universal lifecycle/publication/QA rules;
- reusable gates that apply independent of niche.

Forbidden as rule definitions:

- concrete client/site/brand/product names;
- current-job family/queue IDs;
- current-job row counts;
- one project's exact defect examples as if they define the rule;
- current job status or owner approval.

Concrete examples may be referenced only as historical evidence in `work/<JOB_ID>/`.

## 4. What belongs in Level 2

Each roadmap step must define generically:

```text
PURPOSE
WHY THIS STEP EXISTS
INPUT DATA LAYER
ENTRY GATES
METHOD
ROOT-CAUSE FAILURE CLASSES IT MUST PREVENT
OUTPUT DATA LAYER / ARTIFACTS
FULL-VOLUME / ACCOUNTING REQUIREMENTS
SEMANTIC / METHODOLOGICAL QA
PASS / FAIL / HOLD
NEXT-STEP CONTRACT
```

Level 2 must never define a step by one site's taxonomy.

Forbidden:

```text
"for this site, family X..."
"because Blood & Sand had..."
"76 rows means..."
"PSF014 must..."
"this owner approved current execution..."
```

Those are job-root statements.

## 5. What belongs in work/<JOB_ID>/

Allowed and required:

- frozen client/business facts;
- exact assortment/service data;
- job-specific examples of a universal failure;
- concrete affected row counts;
- current family IDs and query IDs;
- provider request IDs;
- owner approvals for this execution;
- current cursor/status;
- audit overlays and correction evidence.

Job-root evidence may strengthen or reveal a universal lesson. It must not silently mutate the universal roadmap.

## 6. Generalizing a discovered defect

When a concrete job exposes an error:

```text
OBSERVED EXAMPLE
→ identify underlying mechanism/root cause
→ formulate niche-independent failure class
→ define universal prevention/detection gate in Level1
→ map that gate to every applicable Level2 step
→ keep concrete example/counts in work/<JOB_ID>/
→ rerun affected job data under corrected rule
```

Forbidden:

```text
EXAMPLE -> universal special-case patch
CURRENT FAMILY ID -> permanent methodology
CURRENT CLIENT VOCABULARY -> universal lexical rule
```

## 7. Roadmap stability vs method improvement

A concrete job may reveal that a roadmap step needs a stronger gate or an additional universally necessary sub-stage.

Before changing the roadmap, prove:

```text
PROBLEM IS CLASS-GENERAL
NOT merely current-client-specific
AND
NEW/CHANGED STEP HAS A REUSABLE INPUT→METHOD→OUTPUT CONTRACT
```

If the need exists only for one client, keep it as a job-specific branch/gate inside `work/<JOB_ID>/`; do not modify the global roadmap.

## 8. Mandatory regression gate

Before accepting any change under `LEVEL1/` or `LEVEL2/`:

```text
JOB_SPECIFIC_CLIENT_NAMES_IN_RULE_BODY = 0
JOB_SPECIFIC_FAMILY_OR_QUEUE_IDS_IN_RULE_BODY = 0
JOB_SPECIFIC_ROW_COUNTS_USED_AS_UNIVERSAL_THRESHOLDS = 0
CURRENT_JOB_STATUS_IN_LEVEL2 = 0
CURRENT_JOB_OWNER_EXECUTION_APPROVAL_IN_LEVEL2 = 0
UNIVERSAL_ROOT_CAUSE_EXPLICIT = true where lesson-derived
WHY_METHOD_WORKS_OR_FAILURE_OCCURS_EXPLICIT = true
ANY_SITE_EXECUTABILITY_TEST = PASS
```

Historical references inside clearly marked provenance notes are allowed only when they do not define the rule and preferably remain in job-root.

## 9. Interaction with failure ledgers

Canonical separation:

```text
LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md
= universal failure mechanisms + generic gates

work/<JOB_ID>/...FAILURE_LEDGER...
= concrete incidents, counts, examples, affected artifacts
```

A job-specific ledger may add evidence but may not weaken or replace the universal cause.

## 10. PASS policy

A KW-002 roadmap/method revision can be accepted only if:

```text
UNIVERSALITY = PASS
LAYER_SEPARATION = PASS
ROOT_CAUSE_EXPLICIT = PASS
ANY_SITE_EXECUTABILITY = PASS
JOB_EVIDENCE_PRESERVED_SEPARATELY = PASS
```
