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
