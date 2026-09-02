# KW-001 — mandatory Codex current-site discovery and topology gate addendum

Date: 2026-09-02
Status: **ACTIVE / UNIVERSAL PROCESS ADDENDUM / OWNER-APPROVED / OWNER-LOCKED**
Authority: latest explicit owner instruction; supplements `RULES_ARCHITECTURE.md`, `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`, and step-specific methods.

## Purpose

This addendum prevents a known-page recheck from being mistaken for complete current-site discovery and prevents live endpoint checks from being mistaken for proof that an internal link actually exists in HTML.

Canonical non-equivalences:

```text
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
UPSTREAM_INPUT_UNIVERSE != CURRENT_SITE_UNIVERSE
SOURCE_LIVE + TARGET_LIVE != EDGE_IMPLEMENTED
SEMANTIC_LINK_RECOMMENDATION != CURRENT_AS_IS_LINK
LOCAL_BRANCH_NAME_MATCH != REMOTE_STATE_CURRENT
FILE_NOT_FOUND_IN_STALE_LOCAL_CLONE != FILE_ABSENT_FROM_CANONICAL_BRANCH
```

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

ChatGPT MUST require a deterministic Codex/code run before the step may close as complete.

Canonical rule:

```text
SITE_COMPLETENESS_OR_TOPOLOGY_MATERIAL = true
-> CODEX_DETERMINISTIC_DISCOVERY_RUN_REQUIRED = true
-> CODEX_OUTPUT_PERSISTED_IN_GITHUB = true
-> GITHUB_READBACK_REQUIRED = true
-> ANALYTICAL_RECONCILIATION_REQUIRED = true
-> ONLY THEN STEP_PASS_MAY_BE_CONSIDERED
```

ChatGPT's own web reads are an independent semantic/current-content validation layer. They are NOT sufficient evidence of full URL-universe completeness when a deterministic crawl can test that claim.

## Mandatory repository synchronization before Codex authority read

A Codex run must first prove that the local checkout reflects the current canonical remote authority.

Why this exists:

A 2026-09-02 Step-14A attempt was correctly fail-closed by Codex because required files were missing locally. However, the local checkout was at `bd5766a6498577176aaf8d0210a80c670cde4c39` while the canonical remote branch had already advanced to `2407b5fca3b969bd0559619e422951b8d276ddfc`, where the required files existed. The prompt had said only to use the existing branch and had not required a fetch/remote-state comparison first.

The incorrect implication was:

```text
CORRECT LOCAL BRANCH NAME
-> LOCAL CHECKOUT IS CURRENT
-> FILE MISSING LOCALLY
-> FILE MISSING FROM CANONICAL AUTHORITY
```

This is invalid.

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

If local-only commits exist, they must not be destroyed merely to synchronize. Destructive reset, force-push or silent discard is not authorized. Use a safety backup and fail closed on unresolved conflicts.

Canonical rule:

```text
DETERMINISTIC_RUN + STALE_INPUTS != VALID_REPRODUCIBLE_EVIDENCE

REMOTE_FETCH_COMPLETE = true
LOCAL_VS_REMOTE_STATE_RECORDED = true
SAFE_SYNC_COMPLETE = true
-> MANDATORY_AUTHORITY_READ MAY BEGIN
```

The Codex completion report must preserve:

```text
LOCAL_HEAD_BEFORE_SYNC
REMOTE_HEAD_AFTER_FETCH
SYNC_MODE
LOCAL_HEAD_AFTER_SYNC
WORKTREE_CLEAN_OR_PRESERVED_STATE
```

## Required Codex responsibilities

The Codex/code layer must, as applicable to the site and step:

1. discover public URLs from the homepage crawl and normal HTML links;
2. use public sitemap(s) as an additional discovery source, not as the sole source;
3. normalize and deduplicate URLs while preserving evidence of discovery origin;
4. fetch/recheck discovered public HTML pages with bounded retries and explicit failure states;
5. extract literal internal `<a href>` edges from fetched HTML;
6. persist source URL, target URL, anchor text when available, link evidence/provenance, and fetch state;
7. calculate or persist crawl depth/reachability sufficient for the current analytical goal;
8. identify sitemap-only, crawl-only, orphan-candidate, redirect, failed and broken-internal-edge cases when observable;
9. reconcile newly discovered URLs against the upstream architecture/input universe;
10. verify every step-required planned internal edge against literal current HTML and classify it separately from the recommendation;
11. write machine-readable outputs and a human-readable report into the current job workspace;
12. run deterministic QA and leave the job fail-closed on material coverage gaps.

## Separation of responsibilities

```text
CODEX / DETERMINISTIC CODE
= discovery completeness, HTML extraction, link graph, mechanical reconciliation, repeatable QA

CHATGPT ANALYTICAL LAYER
= semantic relevance, user intent, page responsibility, architecture materiality, affected-unit reopen decisions, claim boundaries

OWNER
= authorization and any scope/cost/site-mutation decision
```

Codex output must not silently make semantic ownership decisions or authorize new pages, redirects, canonicals, merges, deletion, provider spending, or site mutation.

## Required current-vs-target states

Current topology and recommended architecture must be stored separately.

For planned internal-link actions, at minimum distinguish:

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
-> if non-material: persist with reason and keep freeze unchanged
```

No relevant discovered URL may be silently ignored.

## Fail-closed acceptance

A step depending on site completeness/topology MUST NOT close as PASS when any of these is true:

```text
required Codex run not executed;
Codex outputs not persisted/read back;
material crawl/discovery coverage gap unexplained;
new relevant discovered URL not reconciled;
required planned internal edge not classified from literal HTML evidence;
current topology and target recommendation conflated;
mechanical QA has unresolved blockers;
repository synchronization not proved before authority read.
```

## Non-repeat lesson

The error that triggered this rule was caused by treating a recheck of known upstream URLs as proof of the full current-site universe, and by treating live source/target endpoints plus semantic fit as proof of literal link implementation. A later blocked Codex attempt exposed a second process defect: the prompt relied on a branch name without proving that the local clone had fetched the current remote authority. The controls are therefore not "check more pages manually" or "retry Codex"; the controls are **mandatory deterministic discovery/topology evidence plus mandatory repository synchronization before the read-first gate**.
