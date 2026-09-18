# KW-002 / BLOOD & SAND — STEP07 POST-ACCEPTANCE METHOD + COVERAGE DEFECT RECORD

Status: **HISTORICAL / SUPERSEDED AS CURRENT GATE**
Date: 2026-09-18
Historical role: records the defect that superseded the earlier `STEP07 = PASS_ACCEPTED` conclusion.
Current resolution: access-state correction passed; ranking-query source recovery failed legitimately in both Work and Codex Windows; the universal methodology now permits a declared external-source recall limitation instead of permanent roadmap deadlock.
Current acceptance authority: `STEP07_RANKING_QUERY_SOURCE_LIMITATION_ACCEPTANCE_2026-09-18.md`.

## 1. Why this record exists

Step07 was formally accepted after R2 wrapper correction, but a later independent external-method audit re-opened the step.
The audit found one concrete execution/QA defect and one method-design defect that were not covered by the previous PASS gates.

Previous accepted corpus is preserved as historical evidence:

```text
CANDIDATE_IDENTITIES = 2172
PROVENANCE_ROWS = 3948
SOURCE_URLS = 1976
AUTHORIZED_COMPETITORS = 32
STEP08_ELIGIBLE_AT_R2 = 794
```

No current evidence indicates that the five R2 semantic corrections or the immutable raw wording/source context should be rolled back.

## 2. Defect A — Ozon access-state / coverage accounting was false

Current published coverage row for `S07A002 / ozon.ru` states:

```text
discovered_urls = 27
eligible_urls = 27
inspected_urls = 26
inaccessible_urls = 0
redirected_terminal_urls = 1
candidate_yield_urls = 0
no_candidate_urls = 26
terminal_coverage_status = COMPLETE
```

The later independent audit inspected the canonical browser-recovery evidence rather than trusting the summary ledger.
It found that the 27 Ozon evidence records contained target block/error content rather than substantive Ozon page content.
Representative evidence included connection/VPN-style block text for `S07U000025` and the same class of target-block content across the Ozon set.

Therefore the old semantic claim was invalid:

```text
ACCESSIBLE + INSPECTED_NO_CANDIDATE
```

because the target semantic page was not actually obtained.

Correct direction:

```text
BLOCK / ERROR / ACCESS FAILURE EVIDENCE
-> applicable inaccessible/error/unresolved state
-> NOT INSPECTED_NO_CANDIDATE
```

### Root cause A

The rule already prohibited converting inaccessible/error pages into `INSPECTED_NO_CANDIDATE`, but execution and return QA validated schema, keys and count reconciliation without validating the semantic meaning of each `INSPECTED_*` state against stored page evidence.

```text
COUNTS_RECONCILE != ACCESS_CLASSIFICATION_PROVEN
PRODUCER TERMINAL LABEL != SELF-CERTIFYING EVIDENCE
```

This was an execution + QA design failure: the existing rule was correct, but the acceptance gate did not independently content-check the access classification.

## 3. Defect B — Step07 method had a competitor-recall blind spot

The old Step07 method primarily mined visible public competitor page content: titles, taxonomy, product names, headings, use cases, labels and contextual text.
This is valid, but it is not sufficient to claim complete competitor semantic discovery.

A competitor page can rank for a search query whose exact wording does not occur visibly on the page.
If Step07 never discovers that query, Step08 cannot validate it, because Wordstat only tests candidates that entered the Step08 queue.

```text
NOT DISCOVERED IN STEP07
-> NOT PRESENT IN STEP08 INPUT
-> STEP08 CANNOT REPAIR THE RECALL OMISSION
```

### Root cause B

The Level2 Step07 contract did not require a second organic ranking-query discovery lane.
The method therefore allowed a page-text-only execution to appear complete.
The prior pre-step/return QA did not challenge this missing discovery channel before acceptance.

This is a method-specification failure, not a bad-row patch.

## 4. Permanent correction already applied to universal rules

On 2026-09-18 the live universal Step07 rule was amended to require:

```text
LANE A = PAGE_SURFACE_DISCOVERY
LANE B = ORGANIC_RANKING_QUERY_DISCOVERY
```

and full-volume access-state content validation:

```text
EVERY_INSPECTED_STATE_HAS_TARGET_CONTENT_EVIDENCE = true
BLOCK_OR_ERROR_EVIDENCE_MISCLASSIFIED_AS_INSPECTED = 0
```

Related permanent failure classes were added to the Level1 failure ledger as `F07-1` and `F07-2`.

## 5. Correct Step07 method from now on

Future Step07 execution must run in this order:

```text
1. Freeze Step06-authorized search competitors.
2. Freeze host/path scope and complete URL frontier.
3. Mine the complete bounded public page surface.
4. Validate every access/inspection terminal state against actual stored evidence content.
5. Independently acquire the allowed Yandex-oriented organic ranking-query portfolio for materially relevant authorized competitors.
6. Preserve ranking-query source/snapshot/query/ranking-URL provenance.
7. Reconcile page-derived and ranking-query-derived candidates against the accepted upstream universe.
8. Preserve single-source and multi-source evidence without treating multiplicity as demand proof.
9. Report source concentration and recall limitations explicitly.
10. Run full-volume mechanical + semantic + access-state QA.
11. Stop before Wordstat demand validation, final intent, clustering or page design.
```

Hard boundaries remain:

```text
COMPETITOR PAGE TOPIC != PROVEN DEMAND
COMPETITOR RANKING QUERY != PROVEN DEMAND
STEP07 DISCOVERS
STEP08 VALIDATES DEMAND
```

## 6. Current correction scope

Do NOT restart Step06.
Do NOT discard the accepted 2172-candidate / 3948-provenance corpus.
Do NOT make new Ozon browser/provider calls merely to prove the already-recorded access-state defect.
Do NOT start Step08.

Required correction work:

1. full-volume validation of all 1976 URL terminal states against available browser/page evidence;
2. correct Ozon and any sibling misclassifications found by that full-volume validation;
3. recompute 32-row competitor coverage truth;
4. run the new organic ranking-query discovery lane over the full authorized competitor universe under the current release contract;
5. reconcile any newly discovered queries into Step07 candidates without demand claims;
6. recompute Step08-eligible queue;
7. publish full-volume QA + handoff manifest;
8. Main Chat return-QA and remote readback before Step08 can be released.

## 7. Why this correction is a Work task

The correction touches a 1976-row URL ledger, browser/page evidence, 32 competitors, candidate reconciliation and potentially a new ranking-query evidence universe.
Ordinary-chat sampling would violate the active Level1 Work rule.

```text
LARGE DATA != SAMPLE IT
LARGE DATA != TRUNCATE IT
LARGE DATA -> COMPLETE BOUNDED EXECUTION IN CHATGPT WORK
```

## 8. External methodology basis used by the independent audit

- Yandex Webmaster — query selection / market analysis: https://yandex.ru/support/webmaster/ru/service/queries-selection
- Semrush — competitor keywords: https://www.semrush.com/blog/competitor-keywords/
- Semrush — Keyword Gap: https://www.semrush.com/kb/28-keyword-gap
- Ahrefs — Content Gap: https://help.ahrefs.com/en/articles/9025740-how-to-use-content-gap-to-find-keyword-ideas-from-competitor-websites
- Serpstat — Keyword Gap: https://help.serpstat.com/en/articles/14437160-keyword-gap
- Keys.so — Yandex/Google competitor semantics: https://www.keys.so/ru

## 9. Historical gate at the time this defect record was current

```text
STEP07 = CORRECTION_REQUIRED
STEP08 = BLOCKED
WORDSTAT_CALLS_ALLOWED_NOW = 0
YANDEX_SEARCH_PROVIDER_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
NEXT = STEP07_POST_ACCEPTANCE_FULL_VOLUME_CORRECTION_IN_WORK
```

This gate is historical. It was later superseded after the access-state correction passed and two independent source-recovery attempts established that no legitimate approved Yandex organic domain/URL→query source was accessible in the available execution environments. See `STEP07_RANKING_QUERY_SOURCE_LIMITATION_ACCEPTANCE_2026-09-18.md` and the current state pointer.
