# KW-001 — mandatory Codex current-site discovery and topology gate addendum

Date: 2026-09-02  
Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL PROCESS ADDENDUM / OWNER-APPROVED / OWNER-LOCKED**  
Authority: latest explicit owner instruction; supplements `RULES_ARCHITECTURE.md`, `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`, and step-specific methods.

## Purpose

This addendum prevents a known-page recheck from being mistaken for complete current-site discovery, prevents live endpoint checks from being mistaken for proof that an internal link actually exists, and prevents stale local repository state from being mistaken for canonical project authority.

Canonical non-equivalences:

```text
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
UPSTREAM_INPUT_UNIVERSE != CURRENT_SITE_UNIVERSE
SOURCE_LIVE + TARGET_LIVE != EDGE_IMPLEMENTED
SEMANTIC_LINK_RECOMMENDATION != CURRENT_AS_IS_LINK
LOCAL_BRANCH_NAME_MATCH != REMOTE_STATE_CURRENT
FILE_NOT_FOUND_IN_STALE_LOCAL_CLONE != FILE_ABSENT_FROM_CANONICAL_BRANCH
```

## Why this rule exists

Prior controlled executions exposed three reusable failure classes:

1. a closed list of already-known URLs was rechecked and then treated as proof that no material current page had been missed;
2. source/target endpoint liveness plus semantic compatibility was treated too close to proof that a literal current HTML edge existed;
3. a Codex run read a correctly named but stale local branch and treated locally missing authority files as if they were absent from the canonical remote state.

### Root causes

```text
CLOSED INPUT SET WAS ALLOWED TO PROVE ITS OWN COMPLETENESS
SEMANTIC RECOMMENDATION STATE WAS NOT SEPARATED FROM AS-IS TOPOLOGY STATE
BRANCH NAME IDENTITY WAS MISTAKEN FOR CURRENT REMOTE STATE
```

Concrete domains, commit SHAs, file paths, counts and run states remain job-specific evidence and are not part of this universal rule.

## Mandatory gate

For every major step whose acceptance depends materially on any of the following:

```text
complete or near-complete public page discovery;
current public-site architecture;
current internal-link topology;
current crawl reachability;
orphan or sitemap-only detection;
exact current source->target link existence;
reconciliation of planned architecture against the actual site;
```

ChatGPT MUST require a deterministic Codex/code or other approved enumerable run before the step may close as complete when such a run is feasible and required by the current method.

```text
SITE_COMPLETENESS_OR_TOPOLOGY_MATERIAL = true
-> DETERMINISTIC_DISCOVERY_RUN_REQUIRED = true
-> OUTPUT_PERSISTED_IN_GITHUB = true
-> GITHUB_READBACK_REQUIRED = true
-> ANALYTICAL_RECONCILIATION_REQUIRED = true
-> ONLY THEN STEP_PASS MAY BE CONSIDERED
```

Manual web reads are a semantic/current-content validation layer. They are not sufficient proof of site-scale completeness when a deterministic mechanism can test that claim.

## Mandatory repository synchronization before authority read

A Codex run must first prove that the local checkout reflects the current canonical remote authority.

Before reading mandatory authorities or reporting a required file as absent, Codex must:

```text
record local branch + local HEAD + worktree state;
fetch the exact canonical remote branch;
record refreshed remote HEAD;
compare local vs remote ancestry/divergence;
preserve local-only work before synchronization;
synchronize safely;
only then perform the read-first/file-existence gate.
```

If local-only commits exist, they must not be destroyed merely to synchronize. Destructive reset, force-push or silent discard is not authorized. Use a safety backup and the evidence-conflict preservation rule where applicable.

```text
DETERMINISTIC_RUN + STALE_INPUTS != VALID_REPRODUCIBLE_EVIDENCE

REMOTE_FETCH_COMPLETE = true
LOCAL_VS_REMOTE_STATE_RECORDED = true
SAFE_SYNC_COMPLETE = true
-> MANDATORY_AUTHORITY_READ MAY BEGIN
```

The completion report must preserve equivalent fields:

```text
LOCAL_HEAD_BEFORE_SYNC
REMOTE_HEAD_AFTER_FETCH
LOCAL_REMOTE_RELATIONSHIP
SYNC_MODE
LOCAL_HEAD_AFTER_SYNC
WORKTREE_CLEAN_OR_PRESERVED_STATE
CONFLICT_COUNT / CLASSIFICATION when applicable
```

## Required deterministic responsibilities

The deterministic collection layer must, as applicable to the current site and step:

1. discover public URLs from normal same-site HTML navigation/crawl;
2. use public sitemap(s) as an additional discovery source, not as the sole proof of reachability;
3. normalize and deduplicate URLs while preserving discovery origin;
4. fetch/recheck discovered public HTML pages with bounded retries and explicit failure states;
5. extract literal internal `<a href>` edges from fetched HTML;
6. preserve source URL, target URL, anchor text when available, link evidence/provenance and fetch state;
7. calculate/preserve crawl depth or reachability sufficient for the current analytical goal;
8. identify sitemap-only, crawl-only, orphan-candidate, redirect, failed and broken-internal-edge cases when observable;
9. reconcile newly discovered URLs against the upstream architecture/input universe;
10. verify every step-required planned internal edge against literal current HTML and classify it separately from the recommendation;
11. write machine-readable outputs and a human-readable report into the current job workspace;
12. run deterministic QA and leave the job fail-closed on material coverage gaps.

## Separation of responsibilities

```text
DETERMINISTIC CODE / BROWSER AUTOMATION
= discovery completeness, HTML extraction, link graph, mechanical reconciliation, repeatable QA

CHATGPT ANALYTICAL LAYER
= semantic relevance, user intent, page responsibility, architecture materiality, affected-unit reopen decisions, claim boundaries

OWNER
= authorization and scope/cost/site-mutation decisions
```

The deterministic layer must not silently make semantic ownership decisions or authorize new pages, redirects, canonicals, merges, deletion, provider spending or site mutation.

## Required current-vs-target states

Current topology and recommended architecture must be stored separately.

For planned internal-link actions, distinguish at minimum:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

A recommendation may remain valid when `AS_IS_ABSENT_PLANNED`; it must not be reported as a currently implemented edge.

## Reopen policy

A newly discovered URL does not automatically invalidate the entire upstream architecture.

```text
NEWLY_DISCOVERED_URL
-> semantic relevance review
-> if architecture-material: reopen only affected unit(s)/case(s)
-> if non-material: persist with reason and keep unaffected decisions unchanged
```

No relevant discovered URL may be silently ignored.

## Fail-closed acceptance

A step depending on site completeness/topology MUST NOT close as PASS when any applicable condition below is true:

```text
required deterministic run not executed;
outputs not persisted/read back;
material discovery coverage gap unexplained;
new relevant discovered URL not reconciled;
required planned internal edge not classified from literal HTML evidence;
current topology and target recommendation conflated;
mechanical QA has unresolved blockers;
repository synchronization not proved before authority read.
```

## Permanent lesson

The controls are not “check more pages manually” or “retry the runner”. They are:

```text
INDEPENDENT ENUMERABLE DISCOVERY
+ LITERAL TOPOLOGY EVIDENCE
+ CURRENT REMOTE AUTHORITY
+ SAFE REPOSITORY SYNCHRONIZATION
+ SEMANTIC RECONCILIATION
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
