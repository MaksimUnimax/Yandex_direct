# Current-site freshness and existence gate

Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL / OWNER-REQUESTED**

## Plain-language purpose

Websites change while an analysis is in progress. A page inventory collected earlier is a snapshot, not permanent truth. Before recommending a new page, deleting/merging pages, diagnosing overlap, or freezing the final architecture, the analyst must verify what exists **now**.

A prior controlled execution proved why this matters: a previously accepted inventory omitted current pages that already served tasks later treated as missing. The later structural step therefore proposed new pages that would have duplicated live pages.

### Root cause

```text
OLDER DISCOVERY SNAPSHOT
WAS TREATED AS
CURRENT NEGATIVE EXISTENCE PROOF
```

The correct control is fresh current-site discovery whenever a material decision depends on an existence/absence claim.

Concrete site identity, missed URLs, products and correction counts remain Level-2 incident evidence.

Hard rule:

```text
OLD_INVENTORY = HISTORICAL EVIDENCE
OLD_INVENTORY != CURRENT SITE TRUTH
NOT_FOUND_EARLIER != ABSENT_NOW
```

## Why negative existence claims require stronger evidence

"Page X exists" can be proven by opening the current page.

"No suitable page exists anywhere on the current site" is a much broader claim. It requires systematic discovery because the page may be:

- deeper in navigation;
- under a different slug;
- named by a synonym;
- nested under another product/service/object family;
- absent from an older inventory;
- newly published after the earlier discovery pass.

Therefore:

```text
POSITIVE EXISTENCE CLAIM -> OPEN/READ CURRENT PAGE
NEGATIVE EXISTENCE CLAIM -> MULTI-ROUTE CURRENT DISCOVERY + OPEN/READ PLAUSIBLE CANDIDATES
```

## Tool-selection rule

### ChatGPT public web is sufficient when

- the candidate set is small and named;
- exact pages/topics can be searched directly;
- the task is to verify content/CTA/business role of specific first-party pages;
- a positive existence claim can be proven by opening the page.

### Codex/browser pass is required or preferred when

- discovery is broad across a large site;
- the analyst needs to make a material negative claim that no suitable page exists;
- deep template families/navigation must be enumerated;
- many candidate units must be checked efficiently;
- search-engine discovery alone may miss weakly exposed pages.

For large-site negative existence claims, preferred pattern:

```text
CODEX/BROWSER BROAD DISCOVERY
+ CHATGPT TARGETED CURRENT PAGE READ/CROSS-CHECK
+ DURABLE GITHUB INVENTORY/READBACK
```

If Codex/browser is unavailable, use at least two independent current discovery routes, for example current navigation/HTML sitemap/site search + external site-restricted web discovery. If coverage is still incomplete, do not assert absence as HIGH confidence: record an explicit deferred/absence-not-proven state.

## Required evidence fields

Every material current-page check must preserve:

```text
check_timestamp
source_channel
query/discovery_route
candidate_url
final_url
page_opened_read = true/false
title
h1
visible_user_task
commercial/informational role
CTA or conversion role when relevant
material inclusions/exclusions
freshness limitation
```

Negative existence evidence additionally records:

```text
discovery_routes_used
synonyms/slugs checked
navigation/sitemap family checked
plausible_candidates_opened
coverage_limitations
absence_confidence
```

## Step applicability

### Step 1 — baseline site/business inventory

Perform the broadest discovery pass. Use multiple channels when the site is large. Timestamp the inventory and mark it explicitly as a baseline snapshot.

Why: Step 1 creates the reusable site model, but later steps must not treat it as timeless.

### Step 11 — page ownership

Refresh plausible owner candidates. `NO_SUITABLE_EXISTING_PAGE` requires explicit negative-current-site evidence, not merely absence from Step 1.

Why: page ownership is a claim about the current public site.

### Step 12 — structural actions

Immediately before every `NEW_*` / CREATE recommendation, perform a fresh current-site existence check and existing-content reuse audit. Re-check current existing targets used by material keep/expand/section/route decisions when their content role is central to the recommendation.

Why: a false CREATE can manufacture a duplicate/competition problem that did not exist before the analysis.

### Step 13 — overlap/cannibalization diagnosis

Before diagnosing a page pair, verify both URLs still exist and their current content/tasks have not materially changed since Step 12.

Why: overlap diagnosis on stale pages is invalid.

### Step 14 — Search architecture freeze

Re-read every final page affected by CREATE/SPLIT/MERGE/major ownership changes and verify final URLs before freezing the architecture.

Why: the frozen architecture must describe the live site plus accepted proposed changes, not an earlier snapshot.

### Step 20 — final QA / client deliverable

Run a lightweight current-URL/final-role recheck for every implementation-critical URL in the client output.

Why: the client should not receive recommendations based on pages that moved, disappeared, or changed role during the project.

## Non-repeat controls

```text
CREATE_WITHOUT_FRESH_CURRENT_SITE_CHECK = FAIL
NO_SUITABLE_EXISTING_PAGE_WITHOUT_NEGATIVE_DISCOVERY_EVIDENCE = FAIL
OLD_SITE_INVENTORY_USED_AS_SOLE_ABSENCE_PROOF = FAIL
MATERIAL_NEGATIVE_EXISTENCE_CLAIM_FROM_ONE_WEAK_DISCOVERY_CHANNEL = FAIL
FINAL_ARCHITECTURE_FREEZE_WITHOUT_CURRENT_URL_RECHECK = FAIL
```

## Durability

Any Codex/browser or web discovery that materially changes an action must be saved to the canonical GitHub workspace immediately and read back before the next material acquisition/decision batch.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
