# KW-002 / BLOOD & SAND — STEP07 EXECUTION QA

Date: 2026-09-17  
Action: `ACTUAL_STEP07`  
Work start remote HEAD: `fd2440b9a71816a1454d96a12f6631102b363629`  
Pre-publication remote HEAD: `00230d7f1a8f83bb2aebfcbad89b896b122879d5`  
Overall hard QA: **FAIL / INCOMPLETE**  
Step result: **INCOMPLETE**

## 1. Executive result

All contracted files and rows were produced, all discovered URLs reached a
governed terminal state, and the ledgers are mechanically coherent. Step07 is
nevertheless **INCOMPLETE**: 751 eligible URLs could not be legitimately
inspected, and only 1 of 32 authorized competitors yielded inspectable
candidate-bearing pages. Terminal accounting is not a substitute for semantic
coverage. No bypass, sampling fallback or narrative PASS was used.

The branch advanced during execution. The new authority changed the Work/Main
role boundary and required handoff set from seven files to six; it did not
change competitor membership, input hashes, output CSV schema, claim boundary
or extraction method. Packaging was paused, the new execution-only prompt blob
`3070c6e9e5e75bcc510f04aa09f76d119f69770f` was read and verified, outputs were
regenerated against `00230d7f…`, and the obsolete Work rule-read ledger was
excluded from the handoff as the current release explicitly requires.

```text
AUTHORIZED_COMPETITORS = 32
SOURCE_URL_ROWS = 1976
INSPECTED_URLS = 24
EXCLUDED_URLS = 1201
INACCESSIBLE_URLS = 751
UNRESOLVED_URLS = 0
ERROR_URLS = 0
CANDIDATE_YIELD_URLS = 24
NO_CANDIDATE_URLS = 0
RAW_OCCURRENCES_RETAINED = 1119
EXPLICIT_DERIVED_OCCURRENCES = 298
PROVENANCE_ROWS = 1417
CANDIDATE_IDENTITIES = 686
```

## 2. Reconciliation totals

| Reconciliation status | Rows |
|---|---:|
| `ALREADY_PRESENT` | 10 |
| `NEW_CANDIDATE` | 400 |
| `NORMALIZED_DUPLICATE` | 0 |
| `POSSIBLE_VARIANT` | 3 |
| `OUT_OF_SCOPE` | 207 |
| `AMBIGUOUS` | 66 |

Step08 routing remains declarative only:

| Route | Rows |
|---|---:|
| `ELIGIBLE_NEW_CANDIDATE` | 400 |
| `ELIGIBLE_POSSIBLE_VARIANT` | 3 |
| `AUDIT_ONLY_ALREADY_PRESENT` | 10 |
| `AUDIT_ONLY_DUPLICATE` | 0 |
| `EXCLUDED_OUT_OF_SCOPE` | 207 |
| `HOLD_AMBIGUOUS` | 66 |

No candidate is claimed as proven demand.

## 3. URL terminal totals

| Inspection status | URLs |
|---|---:|
| `EXCLUDED_OUT_OF_SCOPE` | 1201 |
| `INACCESSIBLE_CAPTCHA_OR_ANTI_BOT` | 12 |
| `INACCESSIBLE_ROBOTS` | 178 |
| `INACCESSIBLE_TIMEOUT_OR_NETWORK` | 561 |
| `INSPECTED_CANDIDATE_YIELD` | 24 |

Coverage ledger terminal statuses:

- `COMPLETE_WITH_INACCESSIBLE_EVIDENCE`: 32

## 4. All 32 competitor coverage rows

| Authority | Canonical site | Discovered | Inspected | Excluded | Inaccessible | Unresolved | Candidate identities | Terminal status |
|---|---|---:|---:|---:|---:|---:|---:|---|
| S07A001 | wildberries.ru | 23 | 0 | 0 | 23 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A002 | ozon.ru | 27 | 0 | 0 | 27 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A003 | market.yandex.ru | 23 | 0 | 3 | 20 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A004 | livemaster.ru | 11 | 0 | 0 | 11 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A005 | avito.ru | 10 | 0 | 2 | 8 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A006 | aliexpress.ru | 2 | 0 | 0 | 2 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A007 | joom.ru | 2 | 0 | 0 | 2 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A008 | ru.wikipedia.org | 20 | 0 | 3 | 17 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A009 | ru.ruwiki.ru | 10 | 0 | 2 | 8 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A010 | kartaslov.ru | 1766 | 24 | 1190 | 552 | 0 | 686 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A011 | ru.wiktionary.org | 5 | 0 | 1 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A012 | znanierussia.ru | 3 | 0 | 0 | 3 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A013 | sibpodkova.ru | 4 | 0 | 0 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A014 | artvaza.ru | 13 | 0 | 0 | 13 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A015 | radugakamnya.ru | 4 | 0 | 0 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A016 | tet-estet.ru | 3 | 0 | 0 | 3 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A017 | sokolov.ru | 2 | 0 | 0 | 2 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A018 | slavyanskieoberegi.ru | 4 | 0 | 0 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A019 | happywitch.ru | 4 | 0 | 0 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A020 | simvolroda.ru | 2 | 0 | 0 | 2 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A021 | oum.ru | 8 | 0 | 0 | 8 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A022 | azbyka.ru | 4 | 0 | 0 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A023 | foma.ru | 2 | 0 | 0 | 2 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A024 | pravoslavie.ru | 1 | 0 | 0 | 1 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A025 | pravmir.ru | 1 | 0 | 0 | 1 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A026 | actro.online | 4 | 0 | 0 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A027 | goroskop365.ru | 4 | 0 | 0 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A028 | elarus.ru | 3 | 0 | 0 | 3 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A029 | lunaro.ru | 3 | 0 | 0 | 3 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A030 | runarium.ru | 3 | 0 | 0 | 3 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A031 | xn--80aejvmu5h.xn--80aswg | 4 | 0 | 0 | 4 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |
| S07A032 | blog.beregy.ru | 1 | 0 | 0 | 1 | 0 | 0 | COMPLETE_WITH_INACCESSIBLE_EVIDENCE |

## 5. Hard QA

| # | Invariant | Result | Evidence |
|---:|---|---|---|
| 1 | `SCHEMA_ENUM_REQUIRED_FIELD_COMPLIANCE` | **PASS** | All four CSVs match the frozen field order/types/enums; no violations |
| 2 | `PRIMARY_KEYS_UNIQUE` | **PASS** | candidates=686/686; urls=1976/1976; provenance=1417/1417 |
| 3 | `CANDIDATE_KEYS_UNIQUE` | **PASS** | unique comparison keys=686; rows=686 |
| 4 | `URL_AUTHORITY_CANONICAL_UNIQUENESS` | **PASS** | unique authority/canonical pairs=1976; rows=1976 |
| 5 | `ONLY_AUTHORIZED_COMPETITORS_USED` | **PASS** | All authority IDs resolve to S07A001..S07A032 and canonical sites match the frozen authority. |
| 6 | `ALL_AUTHORIZED_COMPETITORS_ACCOUNTED` | **PASS** | coverage authorities=32; expected=32 |
| 7 | `ALL_FOREIGN_KEYS_RESOLVE` | **PASS** | No unresolved parent/candidate/source URL references |
| 8 | `DETERMINISTIC_SORT_AND_IDS` | **PASS** | sort=True; sequential ID universes=True |
| 9 | `DISCOVERED_URL_TERMINAL_RECONCILIATION` | **PASS** | All 32 per-competitor equalities reconcile |
| 10 | `INACCESSIBLE_BLOCKED_SURFACES_EXPLICIT` | **PASS** | inaccessible=751; by status={"INACCESSIBLE_CAPTCHA_OR_ANTI_BOT": 12, "INACCESSIBLE_ROBOTS": 178, "INACCESSIBLE_TIMEOUT_OR_NETWORK": 561} |
| 11 | `NO_UNRESOLVED_OR_ERROR_URLS` | **PASS** | unresolved=0; error=0 |
| 12 | `CANDIDATE_SOURCE_COUNTS_EQUAL_PROVENANCE` | **PASS** | Candidate/domain/URL/occurrence counts and URL occurrence counts reconcile |
| 13 | `EVERY_CANDIDATE_HAS_PROVENANCE` | **PASS** | candidates=686; candidates with provenance=686 |
| 14 | `RAW_WORDING_AND_OCCURRENCES_PRESERVED` | **PASS** | raw=1119; final original occurrences=1119; exact multiset equality=True |
| 15 | `EVERY_TRANSFORMATION_RECORDED` | **PASS** | provenance=1417; derived=298 |
| 16 | `NO_DUPLICATE_OCCURRENCE_SILENTLY_DISCARDED` | **PASS** | Complete raw occurrence multiset retained before 298 explicit derived occurrences. |
| 17 | `MULTI_SOURCE_PROVENANCE_PRESERVED` | **PASS** | multi-domain candidates observed=0; all occurrence provenance retained (only one competitor yielded inspectable candidate pages). |
| 18 | `RECONCILIATION_AND_STEP08_ROUTE_VALID` | **PASS** | Every summary has exactly one governed status and matching later route. |
| 19 | `DEMAND_NOT_ASSERTED` | **PASS** | All candidate rows explicitly remain unvalidated. |
| 20 | `NO_FINAL_INTENT_OR_CLUSTER_DECISIONS` | **PASS** | Final intent and cluster fields retain Step07 stop-state enums. |
| 21 | `NO_PAGE_URL_H1_TITLE_DECISIONS` | **PASS** | No output schema contains page-ownership, target URL, H1 or Title decision fields. |
| 22 | `NO_STEP08_EXECUTION` | **PASS** | Step08 was not invoked; step08_route is a future routing label only. |
| 23 | `NEW_PROVIDER_CALLS_ZERO` | **PASS** | Execution log: Wordstat=0; Yandex Search=0; AI Search/GenSearch=0. |
| 24 | `NO_ARBITRARY_SAMPLE_OR_TOP_N` | **PASS** | No page cap used; complete discovered frontier has 1976 terminal rows. Inaccessibility is recorded, not replaced by a sample. |
| 25 | `ACCEPTED_UPSTREAM_FILES_UNCHANGED` | **PASS** | seven authority/schema SHA-256 values unchanged=True |
| 26 | `CURRENT_RELEASE_PROMPT_IDENTITY` | **PASS** | prompt blob=3070c6e9e5e75bcc510f04aa09f76d119f69770f; expected=3070c6e9e5e75bcc510f04aa09f76d119f69770f; six-file execution-only release verified=True |
| 27 | `COMPLETE_BOUNDED_COMPETITOR_UNIVERSE_PROCESSED` | **FAIL** | inspectable-page domains=1/32; inspected URLs=24; inaccessible URLs=751; terminally accounted does not equal semantically inspected. |
| 28 | `EXECUTION_COMPLETENESS_DEMONSTRABLE` | **FAIL** | Step07 remains INCOMPLETE because legitimate inaccessible evidence prevents truthful full-volume semantic coverage. |

Hard failures:

- `COMPLETE_BOUNDED_COMPETITOR_UNIVERSE_PROCESSED` — inspectable-page domains=1/32; inspected URLs=24; inaccessible URLs=751; terminally accounted does not equal semantically inspected.
- `EXECUTION_COMPLETENESS_DEMONSTRABLE` — Step07 remains INCOMPLETE because legitimate inaccessible evidence prevents truthful full-volume semantic coverage.

The failure is substantive coverage, not schema or reconciliation corruption.
The 32 competitors are accounted for, but most public taxonomies could not be
enumerated/inspected from this execution environment without prohibited bypass.

## 6. Method authority boundary

Main Chat's accepted release record already contains the fresh external-method
review. Work did not rerun that governance/research step under the corrected
execution-only role boundary. The frozen Step07 method was executed unchanged;
external methodology was not used as demand evidence or to add competitors.

## 7. Methodological problem discovered

Public-source access was not sufficient for full-volume semantic extraction:

- 178 URLs terminated as robots-unavailable/disallowed evidence;
- 12 terminated as CAPTCHA/anti-bot evidence;
- 561 terminated as timeout/network evidence;
- only 24 pages on `kartaslov.ru` yielded inspectable content;
- 1,201 discovered URLs were explicitly excluded as unrelated branches;
- no unresolved or internal-error rows remain, but inaccessibility itself blocks
  a truthful Step07 completion claim.

The network/robots terminal evidence is snapshot-bounded. It does not prove the
sites are permanently unavailable. A later authorized retry must start from
current authority and the existing ledgers, must not bypass controls, and must
not treat this run as a representative sample.

## 8. Universal quality score

| Dimension | Score | Basis |
|---|---:|---|
| GOAL_AND_OUTPUT_COMPLETENESS | 7/10 | All seven deliverables are materialized, but the substantive Step07 universe is incomplete. |
| METHOD_AND_SOURCE_SUPPORT | 9/10 | Current project authority plus fresh official methodology sources were applied. |
| INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY | 10/10 | Authority hashes, raw wording, URL lineage and many-to-many occurrence evidence reconcile. |
| COVERAGE_AND_COMPLETENESS | 2/10 | All terminal states are recorded, but only one competitor yielded inspectable candidate pages. |
| ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES | 9/10 | Candidates remain demand-unvalidated; no final intent, cluster or page decisions were made. |
| ADVERSARIAL_QA_QUALITY | 9/10 | Independent schema, enum, FK, count, raw-preservation, sorting and authority-hash checks were run. |
| PERSISTENCE_READBACK_AND_REPRODUCIBILITY | 9/10 | Deterministic IDs, complete ledgers and a frozen handoff package support readback. |
| OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE | 9/10 | Single-directory seven-file handoff and explicit failure evidence are owner-usable. |
| INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY | 8/10 | No paid/search provider calls; inaccessible evidence stopped unsafe bypass attempts. |
| DOWNSTREAM_READINESS | 2/10 | The data contract is valid, but Step08 must not start until missing Step07 coverage is resolved or accepted by authority. |

```text
QUALITY_TOTAL = 74 / 100
QUALITY_SCORE = 7.4 / 10
HARD_FAILURE_OVERRIDE = true
```

The score does not override the incomplete-coverage hard failure.

## 9. Stop boundaries and operational assertions

```text
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_OR_GENSEARCH_CALLS = 0

STEP07 = INCOMPLETE
STEP08_STARTED = false

FINAL_INTENT_DECISIONS = NONE
FINAL_CLUSTER_DECISIONS = NONE
FINAL_PAGE_DECISIONS = NONE

ACCEPTED_UPSTREAM_FILES_CHANGED = 0
STALE_BASE_MUTABLE_STATE_FILE_OVERWRITE = 0
WORK_GITHUB_COMMIT_PUSH_PR = false
```
