# KW-001 — Step 14 Search-only architecture freeze method

Date: 2026-09-02
Status: **APPROVED / ACTIVE AFTER POST-RUN DISCOVERY-TOPOLOGY CORRECTION / OWNER-APPROVED**
Stage: Step 14 — Search-only architecture freeze

## 1. Step purpose

Step 14 freezes the classic-Search architecture before any AI/Alice/GenSearch evidence is introduced.

The purpose is NOT merely to copy Step 12 structural actions and Step 13 competing-page decisions into one table. The step must establish a reproducible baseline of:

```text
A. TARGET SEARCH ARCHITECTURE
   which current page owns which search/user task;
   which pages support that owner;
   which structural actions remain supported;
   which internal links are recommended;
   which unresolved items remain unresolved.

B. CURRENT AS-IS PUBLIC SITE TOPOLOGY
   which relevant public pages actually exist now;
   which pages are discoverable now;
   which literal internal HTML links actually exist now;
   how important pages are reachable;
   whether newly discovered pages materially alter the frozen model.
```

The two layers must be reconciled but must never be conflated.

Canonical rule:

```text
TARGET_SEARCH_ARCHITECTURE != CURRENT_AS_IS_TOPOLOGY
```

A Step-14 PASS means the Search-only baseline is semantically coherent AND has been reconciled against a deterministic current-site discovery/topology pass.

---

# 2. Why this method exists

The first OKNO_MSK Step-14 execution produced a strong semantic freeze but exposed a material methodological defect after external audit.

The original execution did these things correctly:

```text
reconciled 2332 active phrases;
preserved 2313 assignments and 19 unresolved rows;
consumed 168 Step-12 structural units;
consumed 199 Step-13 effective page pairs and 21 query-family cases;
rechecked 59 known implementation-relevant URLs;
kept unsupported new-page and destructive actions at zero;
preserved historical/harm claim boundaries;
carried 58 link-action rows with 15 recommended IMPLEMENT edges.
```

However, the method made two invalid inferential jumps.

## Error 1 — known URL recheck was treated as complete current-site discovery

The execution derived the current URL universe from Step 12/13/14 inputs and rechecked all of those known URLs.

The logical chain was:

```text
UPSTREAM ARCHITECTURE ACCEPTED
-> avoid speculative scope expansion
-> derive implementation-critical URLs from upstream artifacts
-> reread all known URLs
-> all known URLs are current/live
-> infer current architecture coverage is sufficient
```

The first four operations were reasonable. The last inference was not.

Why it was wrong:

```text
KNOWN_URL_RECHECK != CURRENT_SITE_DISCOVERY
UPSTREAM_INPUT_UNIVERSE != CURRENT_SITE_UNIVERSE
```

A page absent from upstream inputs cannot fail a known-URL recheck because it is never tested. Therefore a 59/59 live result proves only that the 59 selected URLs are live; it does not prove that all architecture-relevant current pages were discovered.

The error was not "too few manual page reads". The error was using a closed upstream list to prove the completeness of the universe from which that list had been derived.

The non-repeat control is independent deterministic discovery.

## Error 2 — live endpoints plus semantic fit were treated as proof that a link was implemented

The first freeze preserved 15 Step-12 recommended internal-link edges and revalidated source URL, target URL and semantic/role compatibility.

The logical chain was:

```text
recommended edge survives Step 12
-> source exists now
-> target exists now
-> source/target roles remain compatible
-> infer current implementation is verified
```

Again, the first four observations may justify keeping the recommendation. They do NOT prove literal current HTML implementation.

Canonical rule:

```text
SOURCE_LIVE + TARGET_LIVE + SEMANTIC_FIT != EDGE_IMPLEMENTED
SEMANTIC_LINK_RECOMMENDATION != CURRENT_AS_IS_LINK
```

A literal current edge requires evidence from fetched HTML, normally an actual same-site `<a href>` from source to target after URL normalization.

The non-repeat control is a deterministic HTML link graph and separate recommendation/as-is fields.

---

# 3. Root cause — why the first method allowed the error

The defect came from an interaction between two otherwise valid controls.

The method correctly tried to prevent:

```text
speculative new pages;
unsupported redirects/canonicals/merges/deletions;
uncontrolled scope expansion;
reopening already validated upstream work without evidence.
```

But the anti-speculation control was applied too broadly.

Instead of saying:

```text
DO NOT CREATE OR CHANGE ARCHITECTURE WITHOUT EVIDENCE
```

the execution effectively behaved as if:

```text
DO NOT LOOK BEYOND THE UPSTREAM URL UNIVERSE UNLESS A KNOWN UNIT FAILS
```

Those are not equivalent.

The first rule is correct. The second creates selection bias.

Similarly, the link QA correctly wanted to preserve only relevant source/target relationships, but it lacked a field separating:

```text
SHOULD EXIST
from
DOES EXIST NOW
```

Because the schema did not force that distinction, a semantic recommendation could pass a QA designed around endpoint existence and be reported too strongly.

A further process regression made the error avoidable: earlier Step 11 work had already used Codex discovery/profile artifacts (`STEP_11_CODEX_DISCOVERED_URLS.tsv`, `STEP_11_CODEX_PAGE_PROFILE_LEDGER.tsv`, and a Codex current-page refresh report), but the Step-14 method did not explicitly require reviewing/reusing that deterministic discovery pattern before claiming current-site completeness.

Therefore the permanent lesson is causal, not merely procedural:

```text
IF ACCEPTANCE CLAIMS COMPLETENESS OR TOPOLOGY,
THEN EVIDENCE MUST BE GENERATED BY A METHOD CAPABLE OF TESTING COMPLETENESS OR TOPOLOGY.

A CLOSED LIST CANNOT PROVE ITS OWN COMPLETENESS.
ENDPOINT EXISTENCE CANNOT PROVE AN EDGE.
```

---

# 4. Approved method

## Phase A — load upstream semantic authorities

Load and reconcile the accepted outputs from Steps 8–13 that materially govern Search architecture, including current job counts, ownership, structural actions, unresolved boundaries, competing-page corrections and internal-link recommendations.

Do not silently resurrect superseded intermediate actions.

Required principle:

```text
LATEST ACCEPTED UPSTREAM STATE = INPUT BASELINE
NOT = CURRENT-SITE COMPLETENESS PROOF
```

## Phase B — run independent deterministic current-site discovery through Codex/code

When Step 14 acceptance depends on public-site completeness/topology, a deterministic Codex/code run is mandatory.

Why Codex/code is required:

The task is mechanical and enumerable: crawl, fetch, parse HTML, normalize URLs, extract hrefs, calculate graph properties and reconcile sets. Manual web reads are useful for semantic interpretation but are not a defensible completeness mechanism for a site-scale graph when code can enumerate it.

Codex/code must discover from at least:

```text
1. homepage / normal same-site HTML crawl;
2. public sitemap(s) as an additional discovery source;
3. any already-known accepted current URLs needed to seed/reconcile the crawl.
```

Sitemap is a discovery supplement, not a substitute for crawl reachability.

The run must preserve discovery origin so a URL can be classified as:

```text
CRAWL_DISCOVERED
SITEMAP_DISCOVERED
KNOWN_UPSTREAM
or combinations of these.
```

## Phase C — build current as-is topology

For fetched public HTML pages, extract normalized same-site literal `<a href>` edges.

Persist, where available:

```text
source_url
target_url
anchor_text
source_fetch_state
target_fetch_state
redirect/final_url evidence
discovery provenance
crawl depth / reachability
incoming internal link count
outgoing internal link count
```

Identify observable cases such as:

```text
crawl-only URL
sitemap-only URL
orphan candidate
broken internal target
redirected internal target
unreachable/fetch-failed page
```

Do not convert a fetch failure into an absence claim without an explicit bounded retry/failure state.

## Phase D — reconcile discovered URLs against the frozen semantic model

Every newly discovered URL not represented in the upstream architecture must receive an analytical classification:

```text
ARCHITECTURE_MATERIAL
NON_MATERIAL_WITH_REASON
OUT_OF_SCOPE_WITH_REASON
```

Why:

Discovery tells us that a page exists; it does not tell us whether it changes Search ownership.

Codex must not silently decide semantic ownership.

If `ARCHITECTURE_MATERIAL`:

```text
reopen only affected structural unit(s), query-family case(s), ownership boundary and link decisions;
preserve unaffected units;
rerun local QA;
do not silently create a new page/action merely because a current page was discovered.
```

If non-material or out of scope, preserve the URL and reason. Do not silently ignore it.

## Phase E — verify planned internal-link edges against literal HTML

For every required/recommended Step-14 internal edge, store two separate dimensions:

```text
RECOMMENDATION_STATE
AS_IS_TOPOLOGY_STATE
```

Minimum as-is states:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

Interpretation:

`AS_IS_PRESENT`
= literal normalized current `<a href>` evidence exists on the fetched source page.

`AS_IS_ABSENT_PLANNED`
= recommendation remains valid, source/target exist and are semantically compatible, but literal current edge is absent.

`BLOCKED_OR_UNVERIFIED`
= current HTML evidence is insufficient because fetch/parser/redirect/other material evidence is unresolved.

`NOT_APPLICABLE`
= no current edge is required for the accepted recommendation/state.

Never report `AS_IS_ABSENT_PLANNED` as implemented.

## Phase F — preserve unresolved and destructive-action boundaries

Unresolved phrases/items must remain traceable.

No silent assignment.
No silent drop.

New current-site discovery alone does not authorize:

```text
NEW PAGE
DELETE
MERGE
301/308 REDIRECT
CANONICAL CONSOLIDATION
```

Those require their own qualifying evidence and affected-unit analysis.

## Phase G — independent semantic spot checks by ChatGPT

After Codex outputs are persisted, ChatGPT must independently read a sample of material pages/edges, especially:

```text
newly discovered architecture-material pages;
changed ownership candidates;
edges classified AS_IS_PRESENT that matter to acceptance;
blocked/failure cases;
mandatory specialist pages from prior corrections.
```

Purpose:

```text
CODE CAN PROVE ENUMERATION/HTML EVIDENCE;
CODE CANNOT BY ITSELF PROVE SEMANTIC RESPONSIBILITY.
```

The analytical layer validates meaning; it does not replace the crawl.

## Phase H — GitHub persistence and readback

All Codex outputs required for acceptance must be committed in the job workspace and read back before final analysis/PASS.

Chat transcript is not durable evidence.

---

# 5. Required outputs

For a completeness/topology-material Step 14 job, the method must produce equivalent machine-readable artifacts for:

```text
CURRENT DISCOVERED URL UNIVERSE
CURRENT INTERNAL LINK GRAPH
CURRENT PAGE / FETCH PROFILE LEDGER
UPSTREAM-vs-CURRENT URL RECONCILIATION
REQUIRED/PLANNED EDGE VERIFICATION
UNRESOLVED / BOUNDARY LEDGER
FINAL SEARCH-ONLY SEMANTIC ARCHITECTURE FREEZE
QA
REPORT
ACCEPTANCE
CURRENT STATE
```

Exact filenames may vary by job, but the evidence classes may not be omitted.

---

# 6. Codex gate

Canonical step-specific rule:

```text
STEP14_SITE_COMPLETENESS_OR_TOPOLOGY_MATERIAL = true
-> STEP14_CODEX_DETERMINISTIC_DISCOVERY_REQUIRED = true
-> STEP14_CODEX_OUTPUTS_COMMITTED = true
-> STEP14_GITHUB_READBACK = PASS
-> STEP14_NEW_URL_RECONCILIATION_COMPLETE = true
-> STEP14_REQUIRED_EDGE_LITERAL_HTML_CLASSIFICATION_COMPLETE = true
-> ONLY THEN STEP14_FINAL_PASS_MAY_BE_CONSIDERED
```

If Codex cannot execute or its output is incomplete:

```text
STEP14_OVERALL = BLOCKED_OR_REOPENED
```

Do not substitute additional manual page reads and then claim equivalent completeness.

---

# 7. External method origin / why the controls are justified

The method must be refreshed with current sources at execution time, but the corrected structure is based on these durable principles:

## Yandex site structure

Yandex recommends clear link structure and ordinary HTML links to documents and notes that discovery/indexing depends on site link structure; sitemap may assist discovery.

Method consequence:

```text
current architecture must include actual reachability/link evidence, not only endpoint existence.
```

Current reference:
`https://yandex.ru/support/webmaster/ru/recommendations/site-structure`

## Yandex duplicate/canonical and redirect guidance

Canonical and redirects have qualifying purposes; thematic overlap alone is not sufficient evidence for destructive consolidation.

Method consequence:

```text
new discovery or overlap does not auto-authorize redirect/canonical/merge/delete.
```

References:
`https://yandex.ru/support/webmaster/ru/robot-workings/canonical`
`https://www.yandex.ru/support/webmaster/ru/recommendations/changing-site-structure`

## Crawl-based industry practice

Modern technical/site-architecture auditing uses crawled pages, incoming/outgoing internal links and crawl depth as separate evidence dimensions.

Method consequence:

```text
URL_LIVE != TOPOLOGY_VERIFIED
```

Current references used in the 2026-09-02 correction:
`https://www.semrush.com/kb/543-site-audit-crawled-pages`
`https://ahrefs.com/blog/internal-links-for-seo/`

## Codex role

Codex is used here as a repository/code execution layer for deterministic enumeration and QA, not as an SEO authority. The SEO/architecture rules come from search-engine/industry/current-job evidence; Codex makes the mechanical evidence reproducible.

---

# 8. Source-to-method trace

```text
Yandex clear HTML link/reachability guidance
-> literal current link graph required for as-is topology claims

Yandex sitemap/discovery guidance
-> sitemap used as additional discovery channel, not sole proof of reachability

Yandex canonical/redirect guidance
-> no destructive action from mere overlap/new discovery

crawl-based industry architecture practice
-> incoming/outgoing links + crawl depth + discovered URL universe are separate evidence dimensions

OKNO_MSK post-run audit
-> known-only recheck missed completeness risk and link-schema conflated recommendation with implementation

Step-11 Codex precedent in this project
-> deterministic discovery was already feasible and project-compatible

explicit owner instruction 2026-09-02
-> Codex run is mandatory when Step-14 completeness/topology is material
```

---

# 9. Known errors and non-repeat controls

## E14-01 — closed-list completeness fallacy

Error:
known upstream URLs were reread and the resulting live set was treated as sufficient current-site coverage.

Root cause:
anti-speculation/scope-preservation was confused with discovery completeness.

Control:
independent Codex/code discovery before PASS.

## E14-02 — endpoint evidence conflated with edge evidence

Error:
live source + live target + semantic fit was reported too close to implemented current link.

Root cause:
recommendation state and as-is topology state were not separate required fields.

Control:
literal HTML edge extraction + dual-state schema.

## E14-03 — available deterministic precedent not promoted into the step gate

Error:
Step 11 already had Codex-discovered URL/profile artifacts, but Step 14 did not require reviewing/reusing a deterministic site-discovery pattern.

Root cause:
pre-step review focused on Step-14 sources and immediate Step-12/13 outputs but did not ask whether earlier project stages had a stronger evidence-acquisition mechanism for the same factual claim.

Control:
before designing a step evidence mechanism, inspect relevant prior job artifacts/tools for an existing stronger deterministic acquisition pattern.

Canonical question:

```text
IS THERE ALREADY A MORE COMPLETE / REPRODUCIBLE PROJECT TOOL OR PRIOR-STAGE EVIDENCE MECHANISM FOR THIS CLAIM?
```

If yes, either use it or document why it is unsuitable.

---

# 10. Pass gate

A completeness/topology-material Step 14 may pass only when all applicable conditions are true:

```text
UPSTREAM_ACCOUNTING_RECONCILED = true
CODEX_RUN_EXECUTED = true
CODEX_OUTPUTS_PERSISTED = true
GITHUB_READBACK = PASS
CURRENT_DISCOVERED_URL_UNIVERSE_MATERIALIZED = true
DISCOVERY_ORIGINS_PRESERVED = true
NEWLY_DISCOVERED_URLS_RECONCILED = true
UNEXPLAINED_RELEVANT_DISCOVERED_URLS = 0
CURRENT_LITERAL_INTERNAL_LINK_GRAPH_MATERIALIZED = true
REQUIRED_PLANNED_EDGES_AS_IS_CLASSIFIED = 100%
CURRENT_TOPOLOGY_SEPARATE_FROM_TARGET_RECOMMENDATION = true
MATERIAL_AFFECTED_UNITS_REOPENED_AND_RECHECKED = true when applicable
SILENT_UNRESOLVED_ASSIGNMENT = 0
SILENT_UNRESOLVED_DROP = 0
UNSUPPORTED_NEW_PAGE_ACTION = 0
UNSUPPORTED_DESTRUCTIVE_ACTION = 0
HISTORICAL/HARM CLAIM_BOUNDARIES_PRESERVED = true
AI_GENSEARCH_USED = 0 before Search-only freeze
QA_BLOCKERS = 0
```

If any material condition fails:

```text
STEP14_FINAL_PASS = false
```

The semantic freeze may remain provisionally preserved while topology/discovery is reopened, but the overall step is not complete.

---

# 11. Current OKNO_MSK consequence

The first semantic Step-14 output remains a provisional baseline, but overall Step 14 is reopened pending mandatory Step 14A Codex discovery/topology correction.

Current state until that correction is accepted:

```text
STEP14_SEMANTIC_FREEZE = PROVISIONAL_PASS_PRESERVED
STEP14_CURRENT_SITE_COMPLETENESS = REOPENED
STEP14_AS_IS_TOPOLOGY = REOPENED
STEP14_OVERALL = REOPENED_PENDING_CODEX_RUN
STEP15_EXECUTION = BLOCKED
```

Job-specific authority:
`tests/OKNO_MSK/STEP_14A_CODEX_DISCOVERY_TOPOLOGY_CORRECTION_AND_GATE_2026-09-02.md`

Universal process addendum:
`RULES_ARCHITECTURE_CODEX_SITE_DISCOVERY_GATE_ADDENDUM_2026-09-02.md`

---

Markers:

```text
KW001_STEP14_METHOD_APPROVED_AFTER_DISCOVERY_TOPOLOGY_CORRECTION = true
KW001_STEP14_KNOWN_URL_RECHECK_NOT_EQUAL_SITE_DISCOVERY = true
KW001_STEP14_UPSTREAM_UNIVERSE_NOT_EQUAL_CURRENT_SITE_UNIVERSE = true
KW001_STEP14_ENDPOINTS_LIVE_NOT_EQUAL_EDGE_IMPLEMENTED = true
KW001_STEP14_TARGET_ARCHITECTURE_SEPARATE_FROM_AS_IS_TOPOLOGY = true
KW001_STEP14_CODEX_DISCOVERY_REQUIRED_WHEN_COMPLETENESS_MATERIAL = true
KW001_STEP14_LITERAL_HTML_EDGE_VERIFICATION_REQUIRED = true
KW001_STEP14_NEW_URL_AFFECTED_UNIT_REOPEN_REQUIRED = true
KW001_STEP14_PREVIOUS_PROJECT_DISCOVERY_TOOL_REVIEW_REQUIRED = true
KW001_STEP14_FINAL_PASS_BLOCKED_WITHOUT_CODEX_READBACK = true
```
