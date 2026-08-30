# KW-001 — EVIDENCE QUALITY AND PROVIDER COST POLICY

Date: 2026-08-30  
Status: **ACTIVE / UNIVERSAL / OWNER-DIRECTED / OWNER-LOCKED**

## Purpose

This policy governs provider-evidence economics for KW-001 real and rehearsal orders.

It exists because the commercial product is sold for analytical result quality. Provider/API/Search/Webmaster costs are part of delivery cost and must not be minimized in a way that weakens evidence, increases analyst uncertainty, or wastes delivery time.

---

## Core rule

```text
RESULT_QUALITY > PROVIDER_COST_MINIMIZATION
DELIVERY_TIME > PROVIDER_COST_MINIMIZATION
EVIDENCE_RELIABILITY > PROVIDER_COST_MINIMIZATION
```

Provider cost is a business/economics variable, not the primary analytical objective.

```text
PROVIDER_COST = COST_OF_GOODS / DELIVERY COST
```

It must be measured, reconciled, and incorporated into Kwork economics/pricing.

It must **not** be used as a default reason to avoid a materially better direct evidence source.

---

## Direct-provider evidence rule

When a direct Yandex source can answer the analytical question more authoritatively than agent inference or indirect observation, use the direct Yandex source as a normal evidence route rather than reserving it only for a late ambiguity escalation.

Examples:

```text
Yandex Webmaster query<->URL data
= direct owned evidence of how Yandex associates site pages with queries

regional ordinary Yandex Search / SERP
= direct current evidence of what Yandex ranks for a query and what result/page types coexist

Wordstat
= direct Yandex human-demand evidence
```

For provider-observable questions:

```text
DIRECT_PROVIDER_EVIDENCE > AGENT_INFERENCE
```

This does not mean provider data replaces first-party page reading for questions about actual page content, offer, CTA, scope, or user task.

```text
PROVIDER_SEARCH_BEHAVIOR != PAGE_CONTENT
PAGE_READ != PROVIDER_SEARCH_BEHAVIOR
```

Use both when both dimensions are material.

---

## Quality/time rule

Do not implement a workflow whose main objective is to minimize the number of provider calls.

A new provider request is justified when it materially improves one or more of:

```text
evidence coverage
freshness
confidence
directness of evidence
boundary resolution
error detection
execution speed / analyst time
client-result quality
```

A previously collected result may be reused, but reuse is not a reason to suppress a new direct request when the new request would materially improve the decision.

```text
EXISTING_EVIDENCE != NEW_EVIDENCE_FORBIDDEN
```

---

## What still must be avoided

This policy is not permission for blind or redundant provider traffic.

Do not issue requests that are materially duplicative and have no credible information value.

```text
MORE_REQUESTS != BETTER_METHOD
```

The correct question before a provider batch is:

```text
WILL THIS EVIDENCE MATERIALLY IMPROVE QUALITY, COVERAGE, FRESHNESS, CONFIDENCE, OR TIME?
```

not:

```text
CAN WE AVOID PAYING FOR THIS REQUEST?
```

---

## Cost accounting

All paid/provider execution must still preserve:

```text
planned requests
executed requests
successful / failed / outcome-unknown requests
unit or estimated cost where available
total provider cost
replay/recovery cost
reason for material additional evidence
```

The economic lesson belongs in product pricing and margin measurement.

Analytical quality must not be silently degraded to protect a provisional package price.

If reliable execution economics show the current product price cannot absorb the evidence level required for a high-quality result, fix the **price/package**, not the evidence standard.

---

## Tool-role consequence

For public-page research:

```text
Codex / Work / public web
= page discovery, extraction, rendered inspection, actual content/task/CTA evidence

Yandex Webmaster / ordinary Yandex Search / other direct Yandex provider surfaces
= Yandex-observed search behavior and provider truth
```

They are complementary evidence systems, not substitutes selected primarily by cost.

---

## Failure if ignored

If ChatGPT optimizes provider spend before result quality, the service can produce:

```text
under-sampled Search evidence
false page ownership
missed page conflicts
stale conclusions
avoidable manual analysis
slow delivery
false certainty from agent inference
weaker client recommendations
```

---

## Review trigger

Review this policy only if the owner changes the product economics or explicitly introduces a package with a hard evidence/cost ceiling.

Until then:

```text
QUALITY_TIME_FIRST_PROVIDER_POLICY = ACTIVE
PROVIDER_COST_MINIMIZATION_AS_PRIMARY_GOAL = FORBIDDEN
DIRECT_PROVIDER_EVIDENCE_EARLY_WHEN_MATERIAL = REQUIRED
PROVIDER_COST_ACCOUNTING = REQUIRED
```