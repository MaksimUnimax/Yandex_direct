# OKNO_MSK — Step 5A.5 Wordstat reconciliation report

Date: 2026-09-08  
Status: **ANALYST QA PASS / OWNER REVIEW PENDING / METHOD NOT PROMOTED**

## 1. Completed scope

All 14 preserved Wordstat executions and every actually returned direct/association row were normalized, joined back to competitor-page evidence and reconciled against the current completed OKNO_MSK semantic authority. No provider was called. The result is a bounded ordinary-Yandex-Search requirement package for Main ChatGPT; it is not an accepted keyword/page/action decision.

## 2. Provider accounting

```text
SEEDS_ACCOUNTED = 14 / 14
DIRECT_WORDSTAT_ROWS_EXTRACTED = 21
ASSOCIATION_ROWS_EXTRACTED = 139
TOTAL_RETURNED_PHRASE_ROWS = 160
RESULT_ROWS_ASSOCIATIONS_TOTALCOUNT = 8
TOTALCOUNT_ONLY = 2
EMPTY_PROVIDER_RESULT = 4
FABRICATED_ROWS = 0
FABRICATED_ZERO_DEMAND = 0
```

`result={}` remains an empty provider result, not numeric zero. `totalCount`-only responses remain aggregate observations without invented phrase rows.

## 3. Row-level reconciliation

```text
ALREADY_COVERED_EXACT_OR_CLOSE = 56
POTENTIALLY_NEW_SEARCH_RECHECK = 20
OFF_SCOPE_BUSINESS = 26
NOISE_IRRELEVANT = 51
HOLD_EVIDENCE = 7
DEDUPLICATED_NEW_SEARCH_DIRECTIONS = 9
FINAL_SEARCH_RECHECK_CALLS_REQUIRED = 9
```

Associations were assessed independently. High counts did not override relevance, business scope or existing semantic coverage.

## 4. Exact Search recheck package

| Priority | Exact query | Wordstat source state | Why Search is required |
|---:|---|---|---|
| 1 | **гидроизоляция для открытого балкона** | returned phrase row(s) | Resolve current intent, competitor visibility and page type before any merge decision. |
| 2 | **солнцезащитный стеклопакет** | returned phrase row(s) | Resolve current intent, competitor visibility and page type before any merge decision. |
| 3 | **многофункциональный стеклопакет что это** | returned phrase row(s) | Resolve current intent, competitor visibility and page type before any merge decision. |
| 4 | **ударопрочный стеклопакет** | returned phrase row(s) | Resolve current intent, competitor visibility and page type before any merge decision. |
| 5 | **окна для старого фонда** | totalCount-only | Resolve current intent, competitor visibility and page type before any merge decision. |
| 6 | **балконы под офис** | returned phrase row(s) | Resolve current intent, competitor visibility and page type before any merge decision. |
| 7 | **кладовая на балконе** | returned phrase row(s) | Resolve current intent, competitor visibility and page type before any merge decision. |
| 8 | **шумоизоляция на крышу балкона** | returned phrase row(s) | Resolve current intent, competitor visibility and page type before any merge decision. |
| 9 | **армирование оконного профиля** | returned phrase row(s) | Resolve current intent, competitor visibility and page type before any merge decision. |

The P-46 seed is not repeated in this Search package: its exact query already has preserved Q62 Search evidence and Wordstat returned only `totalCount=17`, not phrase rows. The four `result={}` seeds remain explicit `HOLD_EVIDENCE`; absence of rows is not converted into zero demand.

## 5. Causality and decision boundary

```text
COMPETITOR PAGE EVIDENCE
→ CANDIDATE SEED
→ PRESERVED WORDSTAT ENVELOPE
→ ACTUALLY RETURNED PHRASE / TOTALCOUNT-ONLY STATE
→ CURRENT SEMANTIC RECONCILIATION
→ SEARCH REQUIREMENT
```

This lineage does not claim that a competitor ranks for a Wordstat-returned phrase. Wordstat does not establish intent, page ownership, split/merge, page creation or implementation.

## 6. Protection and provider accounting

```text
NEW_YANDEX_SEARCH_CALLS = 0
NEW_WORDSTAT_CALLS = 0
NEW_ALICE_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_WEBMASTER_CALLS = 0
NEW_METRIKA_CALLS = 0
NEW_DIRECT_CALLS = 0
CLIENT_DELIVERABLES_MODIFIED = false
LEVEL1_METHOD_PROMOTED = false
```

## 7. Next action

`MAIN_CHATGPT_STEP_5A_6_EXECUTE_ONLY_THE_MATERIALIZED_SEARCH_RECHECK_PACKAGE_VIA_YANDEX_BRIDGE`
