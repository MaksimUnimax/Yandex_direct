# MK02 STEP 10 — CURRENT PAGE OWNERSHIP / PHRASE→PAGE MAPPING

## PURPOSE
Decide which current public page truthfully owns each accepted user-task cluster and materialize one ownership row for every applicable active phrase.

## WHY THIS STEP EXISTS
A coherent semantic cluster does not automatically identify a page. A similarly named URL, one representative query or a Search-visible URL can appear convincing while serving a materially different user task. Cluster-level decisions also hide phrase-level exceptions if no full map is built.

## INPUTS
Step09 cluster contracts and the exact active phrase set from the **current accepted semantic product authority**; current public-site/page evidence; current business scope; unresolved semantic/Search handoff; saved Search/Webmaster evidence where legitimately applicable. Historical downstream assignment flags are enrichment/provenance only and cannot define the active input set.

## REQUIRED EVIDENCE
For each material candidate page: current URL, current page purpose/task, title/H1 or equivalent visible evidence, product/service/information role, important inclusions/exclusions, parent/child/support relation when material, discovery/read provenance. For broad or weak units, full member phrases must be reviewable.

## METHOD
First derive the exact active phrase key set from the current accepted semantic product state. Join older ownership/action evidence onto those keys without importing an older `ASSIGNED`/working flag as activation authority. Then start from that phrase ledger, not the cluster summary alone. Build plausible candidate pages for every effective task/unit. Audit broad/weak/mixed units member-by-member before accepting ownership. Use current page purpose and expected user outcome; URL/title tokens are candidate-discovery clues only. Use Search only where it resolves a real task/page expectation boundary; Search absence never proves site absence. Assign an equivalent state:

```text
OWNER_EXISTING
NO_SUITABLE_EXISTING_PAGE
OWNER_UNRESOLVED_EVIDENCE_REQUIRED
OUTSIDE_SCOPE_NO_TARGET_OWNERSHIP
```

Then materialize a complete phrase→page map. Preserve separately:

```text
EXACT PHRASE OWNER
FAMILY / STRUCTURAL-UNIT OWNER
SUPPORTING PAGE(S)
OBSERVED SEARCH-RELEVANT URL when actually evidenced
```

These roles must never be silently compressed into one `main URL` field.

## OUTPUTS
Current page candidate ledger; unit ownership ledger; complete phrase→page map; explicit unresolved/no-page rows; supporting-page relationships; ownership QA/readback.

## SOURCE KW-001 AUTHORITY
`STEP_11_PAGE_OWNERSHIP_METHOD.md`; `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`; corrected post-release owner/supporting-page lessons.

## KNOWN FAILURE CLASSES
M11-01..M11-07; QF001-style exact-owner/family-owner/supporting-page contradiction; M12-17 intended target vs observed Search URL compression.

## ROOT CAUSES
Cluster labels, lexical similarity, output completeness and observed Search behavior were allowed to substitute for full member/task/current-page evidence.

## NON-REPEAT CONTROLS
Current-semantic-state activation filter before every historical join; phrase-level input/accounting; candidate ledger; full-member coherence review for risky units; current page read required for `OWNER_EXISTING`; explicit role separation; unresolved state allowed; save/readback before further acquisition.

## CLAIM BOUNDARIES
```text
LEXICAL URL MATCH != OWNER
SEARCH-RANKING URL != AUTOMATIC OWNER
SEARCH ABSENCE != SITE ABSENCE
NO_SUITABLE_EXISTING_PAGE != CREATE
CLUSTER OWNER != COMPLETE PHRASE MAP
REPRESENTATIVE QUERY != WHOLE-CLUSTER EVIDENCE
```

Step10 does not decide CREATE/SPLIT/MERGE or prove cannibalization.

## UNKNOWN / BLOCKER BEHAVIOR
If current page evidence or cluster coherence is insufficient, assign unresolved/no-suitable state honestly. No target URL is fabricated merely to complete a table.

## PASS GATE
Current accepted semantic active keys reconcile exactly to ownership map keys; legacy downstream flags activate zero non-active phrases; silent drops=0; unknown unit IDs=0; `OWNER_EXISTING` always has current page evidence and target; unresolved/Search-required rows have no fabricated target; exact owner/family owner/supporting roles are distinguishable; no Step11/12 action/harm verdict leaked prematurely.

## CLIENT-FACING MEANING
«Для каждой темы и запроса показываем, какая существующая страница должна быть основной, какие страницы могут только дополнять тему и где подходящей страницы пока действительно нет или решение ещё требует проверки.»

---

## OWNER CORRECTION 2026-09-10 — TARGET-FIRST LANDING MAP IS MANDATORY

The current-site-first wording above is insufficient for the sold MK02 result and is superseded where it conflicts with this correction.

MK02 must not begin page responsibility by accepting the current site as the answer. Step10 must first design the **intended landing responsibility** from the accepted semantic/task clusters, and only then reconcile that intended responsibility with current public pages.

Mandatory two-level output:

```text
LEVEL 1 — EVERY ACTIVE PHRASE
phrase → cluster/task → intended landing-page key → intended target URL/page state

LEVEL 2 — EVERY MATERIAL CLUSTER/TASK
cluster/task → one intended primary landing page → page type → parent/section → supporting-page role
```

For every active phrase, the target-routing field must resolve to one of:

```text
TARGET_EXISTING_PAGE_CANDIDATE
TARGET_NEW_PAGE_CANDIDATE
TARGET_WITHIN_PARENT_NO_STANDALONE_PAGE
TARGET_UNRESOLVED_EVIDENCE_REQUIRED
OUTSIDE_SCOPE_NO_TARGET
```

`TARGET_NEW_PAGE_CANDIDATE` is only a target-design candidate at Step10; it is not permission to CREATE. Step11–13 must still test reuse, current-site reality and structural evidence.

For every material cluster/task, materialize a target landing-page specification with at least:

```text
TARGET PAGE KEY
HUMAN PAGE PURPOSE
PRIMARY USER TASK / INTENT
PAGE TYPE
PRIMARY / REPRESENTATIVE QUERY
MEMBER PHRASE COUNT
INTENDED PARENT / SECTION
INTENDED TARGET URL OR PROVISIONAL ROUTE
SUPPORTING PAGE RELATIONSHIPS WHEN MATERIAL
CURRENT PAGE CANDIDATE / MATCH STATE kept separately
```

Permanent distinctions:

```text
INTENDED TARGET LANDING != CURRENT PAGE THAT HAPPENS TO EXIST
PHRASE→TARGET MAP != CLUSTER→LANDING MAP
CURRENT SITE INVENTORY != TARGET INFORMATION ARCHITECTURE
GOOD CURRENT SITE != PERMISSION TO OMIT TARGET MAPPING
NO PHYSICAL CHANGE != NO DELIVERABLE VALUE
```

The current site is evidence for reconciliation, reuse and safety; it is not allowed to predefine the target map before target routing has been independently materialized.

Additional PASS requirements:

```text
ACTIVE PHRASES WITHOUT TARGET ROUTE/EXPLICIT UNRESOLVED STATE = 0
MATERIAL CLUSTERS WITHOUT TARGET LANDING SPEC = 0
TARGET LANDING SPECS DERIVED ONLY BY COPYING CURRENT URLS = FAIL
CURRENT OWNER MATCH MUST BE A LATER RECONCILIATION FIELD, NOT THE TARGET DESIGN ITSELF
```

Correct client-facing meaning after this correction:

«Для каждого рабочего запроса показываем, к какой теме он относится и на какую целевую посадочную страницу должен вести. Для каждой темы отдельно проектируем основную посадочную страницу и её место в структуре, а затем проверяем, есть ли на текущем сайте подходящая страница, нужно ли её доработать или требуется другое решение.»