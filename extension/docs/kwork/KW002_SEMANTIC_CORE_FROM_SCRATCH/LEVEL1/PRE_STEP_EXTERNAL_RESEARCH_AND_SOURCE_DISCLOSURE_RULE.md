# KW-002 — LEVEL 1 PRE-STEP EXTERNAL RESEARCH AND SOURCE DISCLOSURE RULE

Status: **ACTIVE / OWNER-LOCKED / REQUIRED**  
Owner instruction: 2026-09-09

## 1. Purpose

Before every major KW-002 roadmap step, the method must be checked against **fresh external internet sources relevant to that exact step**.

Internal project documentation controls execution, but it cannot be the only methodological justification.

```text
INTERNAL RUNBOOK = PROCESS AUTHORITY
INTERNAL RUNBOOK != INDEPENDENT METHOD PROOF
PAST WEB RESEARCH != AUTOMATICALLY FRESH ENOUGH FOR THE NEXT STEP
```

The owner must be able to open the cited sources directly and inspect what the method is based on.

## 2. Mandatory pre-step internet research

Before execution of every major step:

```text
1. define the exact methodological/provider questions of the step;
2. search the current internet for sources that answer those questions;
3. read the relevant source material, not only search-result snippets;
4. prefer current primary/official documentation where available;
5. add strong industry corroboration when the step contains analytical SEO methodology not fully defined by an official provider;
6. compare the sources with the proposed project method;
7. change/rework the method if external evidence exposes a defect;
8. persist the source-to-method trace in the step pre-step artifact;
9. show the source list with clickable links in the owner-facing chat BEFORE execution.
```

No provider request, Work execution or material step execution may begin before this disclosure is complete.

## 3. Source priority

Use the strongest source available for each claim:

```text
1. OFFICIAL PROVIDER / SEARCH ENGINE DOCUMENTATION
2. OFFICIAL PRODUCT / API / POLICY / PRICING DOCUMENTATION
3. PRIMARY TECHNICAL / STANDARDS SOURCES
4. HIGH-QUALITY INDUSTRY PRACTICE / SPECIALIST METHODOLOGY
5. PROJECT_TEST_VALIDATED EVIDENCE
6. ANALYST HEURISTIC — only when clearly labelled
```

Do not use a weak secondary article to override a current official provider contract.

Do not add irrelevant links merely to increase source count.

```text
NO UNIVERSAL MAGIC SOURCE COUNT
ENOUGH SOURCES = every material method question has adequate support or an explicit evidence gap
```

## 4. Mandatory owner-facing source disclosure

The pre-step chat report must contain a clearly visible section:

```text
ИСТОЧНИКИ / МАТЕРИАЛЫ, КОТОРЫЕ Я ИЗУЧИЛ ПЕРЕД ШАГОМ
```

For every source show:

```text
SOURCE TITLE
PUBLISHER / SOURCE CLASS
CLICKABLE URL
DATE/FRESHNESS CHECKED when material
WHAT EXACTLY THIS SOURCE SUPPORTS
HOW IT CHANGES / CONFIRMS THE CURRENT STEP METHOD
LIMITATION / WHAT IT DOES NOT PROVE, when relevant
```

A source name without a link is insufficient.

A raw list of URLs without explaining what each source supports is insufficient.

The owner must be able to click the links from chat and inspect the material directly.

## 5. Mandatory durable step artifact

Every major `work/<JOB_ID>/` pre-step artifact must include an external-source section or table with at least:

```text
source_id
source_title
publisher
source_class
url
checked_at
method_element_supported
exact_claim_supported
project_specific_application
claim_boundary
```

If the same source supports several material method elements, preserve that mapping rather than citing it once decoratively.

## 6. Freshness rule

For changing topics such as:

```text
provider/API capabilities
pricing
quotas/limits
search-engine features
AI-search behavior
laws/policies
product functionality
current SEO/search guidance
```

research must be refreshed before the material step.

Do not rely on a prior chat's internet check merely because the URL still exists.

Record the date the source was checked.

## 7. If no adequate external source exists

Still perform the search.

If no credible external source supports a material method element, write explicitly:

```text
NO ADEQUATE EXTERNAL SOURCE FOUND
SOURCE_CLASS = PROJECT_TEST_VALIDATED | ANALYST_HEURISTIC | OWNER_SCOPE_RULE
```

Then explain the evidence gap and whether it requires:

```text
HOLD
CONTROLLED EXPERIMENT
PROVIDER CAPABILITY CHECK
OWNER DECISION
PROJECT-SPECIFIC HEURISTIC WITH CLAIM BOUNDARY
```

Never fabricate a source or silently present a heuristic as an external standard.

## 8. Provider-step special requirement

Before a step that uses Yandex Marketing Bridge or another provider, external research must verify all material applicable items such as:

```text
operation/method semantics
request/response fields
regions/devices/operators
limits/result depth/pagination
pricing/quota/cost
known capability boundaries
current provider documentation
```

The project must separately verify the Bridge's own current implementation/accepted capability from repository evidence.

```text
PROVIDER DOCS != BRIDGE CAPABILITY PROOF
BRIDGE TESTS != CURRENT PROVIDER DOCS
```

Both layers are required when material.

## 9. Analytical SEO-step special requirement

For analytical steps such as seed design, cleanup, intent, clustering, page ownership, internal linking, competitor expansion or AI-search reconciliation:

```text
OFFICIAL SEARCH-ENGINE GUIDANCE where relevant
+
HIGH-QUALITY INDUSTRY PRACTICE where official material does not fully define the analytical method
+
CURRENT PROJECT EVIDENCE
```

must be distinguished.

A third-party article may corroborate practice but must not be presented as an official Yandex rule.

## 10. Required pre-step chat order

Before execution, the owner-facing chat must show in this order or an equivalently complete structure:

```text
WHOLE KWORK GOAL
FULL ROADMAP
COMPLETED
REMAINING
CURRENT STEP GOAL
WHAT PROBLEM THE STEP SOLVES
REQUIRED OUTPUT
RELEVANT PRIOR ERRORS
NON-REPEAT CONTROLS
FRESH INTERNET RESEARCH
CLICKABLE SOURCE LIST + WHAT EACH SOURCE SUPPORTS
SOURCE→METHOD TRACE
METHOD / EXECUTION PLAN
BRIDGE/WORK GATE if applicable
PASS CONDITIONS
PLAIN-LANGUAGE WHY / WHAT / RESULT
```

Only after this is visible in chat:

```text
PRE_STEP_EXTERNAL_RESEARCH = PASS
SOURCE_DISCLOSURE_IN_CHAT = PASS
EXECUTION_ALLOWED = true
```

## 11. Failure conditions

The pre-step gate fails if any of the following applies:

```text
NO FRESH INTERNET RESEARCH FOR THE CURRENT MAJOR STEP
MATERIAL METHOD CLAIM HAS ONLY SELF-REFERENTIAL INTERNAL SUPPORT
SOURCE NAMES PROVIDED WITHOUT CLICKABLE LINKS
LINKS PROVIDED WITHOUT EXPLAINING WHAT THEY SUPPORT
STALE PROVIDER/PRICING/CAPABILITY CLAIM USED WITHOUT CURRENT CHECK
EXTERNAL SOURCE CLAIM EXCEEDS WHAT THE SOURCE ACTUALLY SUPPORTS
OWNER CANNOT INSPECT THE CITED BASIS FROM THE CHAT
```

Then:

```text
EXECUTION_ALLOWED = false
```

## 12. Relation to quality scoring

The universal quality score must penalize or fail `METHOD_AND_SOURCE_SUPPORT` when this rule was not followed.

A step cannot receive PASS merely because its downstream result happened to look plausible after skipping mandatory source research/disclosure.

## 13. Marker

```text
KW002_PRE_STEP_INTERNET_RESEARCH_REQUIRED = true
KW002_PRE_STEP_CLICKABLE_SOURCE_DISCLOSURE_REQUIRED = true
KW002_SOURCE_TO_METHOD_EXPLANATION_REQUIRED = true
KW002_STALE_WEB_RESEARCH_NOT_AUTOMATICALLY_REUSABLE = true
KW002_PROVIDER_STEP_CURRENT_OFFICIAL_DOCS_REQUIRED_WHEN_AVAILABLE = true
KW002_EXECUTION_BLOCKED_UNTIL_SOURCE_DISCLOSURE = true
```
