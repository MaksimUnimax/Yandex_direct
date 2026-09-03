# KW-001 — Step 14 native-tool-first discovery correction

Date: 2026-09-02  
Updated: 2026-09-03  
Status: **ACTIVE / STEP-14-SPECIFIC / UNIVERSAL / OWNER-REQUIRED**

## Purpose

When Step 14 needs independent current-site discovery, choose the strongest already-available native evidence tool before building custom collection infrastructure.

## Failure and root cause

A prior controlled execution correctly required independent deterministic discovery, but then assumed that this automatically required a new custom crawler. Work drifted from collecting evidence into building and debugging collection infrastructure.

```text
DETERMINISTIC PASS REQUIRED != CUSTOM CRAWLER REQUIRED
```

Root cause:

```text
"manual analyst reading is not completeness proof"
WAS OVERGENERALIZED INTO
"only a custom crawler can provide acceptable independent evidence"
```

The missing question was:

```text
WHAT CURRENT NATIVE TOOL CAN OBSERVE THE REQUIRED FACT DIRECTLY, REPRODUCIBLY AND WITH SUFFICIENT COVERAGE?
```

Concrete domains, paths, counts and incident data belong in Level-2 evidence, not this permanent rule.

## Corrected method

Before selecting a collection implementation:

1. define the exact factual observation required;
2. inspect current native tool capabilities in the execution environment;
3. choose the simplest reproducible tool that can meet coverage, output and termination requirements;
4. introduce custom code only for a named capability gap.

When a native browser is sufficient, it may be used to:

```text
open <CURRENT_SITE_URL>;
inspect current navigation and public pages;
follow same-site links systematically;
record URL/final URL/title/H1/discovery provenance as applicable;
verify <CURRENT_REQUIRED_EDGE_SET> against literal current page/DOM evidence;
use sitemap(s) as an additional discovery route;
reconcile discovered URLs with accepted upstream URLs;
persist outputs for semantic review.
```

Code remains valid as a narrow helper for normalization, deduplication, joins, counts, artifact formatting or a mechanical operation the native browser cannot reliably perform.

If the native tool cannot meet the required completeness, scale or repeatability, a qualified code/crawler path may be used under the deterministic execution reliability gate.

## Evidence boundary

Discovery evidence does not itself authorize semantic or structural changes.

The collection layer must not automatically:

```text
create pages;
change semantic/page ownership;
merge or delete pages;
set redirects/canonicals;
change accepted upstream decisions;
execute downstream analytical stages.
```

Semantic reconciliation remains an analytical responsibility after evidence persistence.

## Non-repeat sequence

```text
WHAT FACT MUST BE OBSERVED?
-> WHAT NATIVE TOOL CAN OBSERVE IT?
-> DOES IT MEET COVERAGE / REPEATABILITY / TERMINATION NEEDS?
-> WHAT NAMED GAP, IF ANY, REQUIRES CUSTOM CODE?
```

Do not build infrastructure merely because the evidence requirement is deterministic.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## Markers

```text
KW001_STEP14_TOOL_CAPABILITY_FIRST_DISCOVERY_ACTIVE = true
KW001_STEP14_CUSTOM_CRAWLER_NOT_REQUIRED_BY_DEFAULT = true
KW001_STEP14_NATIVE_CAPABILITY_BEFORE_CUSTOM_COLLECTION_CODE = true
```
