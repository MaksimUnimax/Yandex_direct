# Step 14A — current-site semantic reconciliation and final Step-14 closure

Date: 2026-09-02  
Job: `OKNO_MSK`  
Mode: `NO_BRIDGE`

## Purpose and method

Close the post-Run9 current-site discovery gap without repeating the full crawl. The canonical Step-14 rule was applied to every URL newly surfaced outside the frozen Step12/13/14 universe:

```text
NEW URL -> exactly one of
ARCHITECTURE_MATERIAL
NON_MATERIAL_WITH_REASON
OUT_OF_SCOPE_WITH_REASON

ARCHITECTURE_MATERIAL -> affected structural unit/query family
-> test frozen owner/boundary
-> update only affected decisions
```

The exact repaired Run10 Markdown source is identified by `STEP_14A_REPAIRED_REPORT_SOURCE_MANIFEST.json`, SHA-256 `1366c35f8ba45314d4453dba1271536f08bc2072e7292a1404bdc5bde17fe6b7`. Its 1.97 MB Markdown bytes are not copied into Git. The complete 2624-row semantic classification, material delta, QA and final state are Git-durable.

## Mechanical Run10 accounting

```text
UNIQUE_PUBLIC_URLS = 2683
OPENED_RUN10 = 1688
OPENED_RUN9_PRESERVED = 9
ERROR = 679
NOT_HTML = 307
PENDING = 0
PROCESSING = 0
SILENT_SKIP = 0
UNPROCESSED = 0
KNOWN_STEP12_13_14_YES = 59
CURRENT_MINUS_STEP12_13_14 = 2624
```

Checks: `1688 + 9 + 679 + 307 = 2683`; `59 + 2624 = 2683`.

## Complete 2624-row semantic reconciliation

```text
ARCHITECTURE_MATERIAL = 21
NON_MATERIAL_WITH_REASON = 1932
OUT_OF_SCOPE_WITH_REASON = 671
UNCLASSIFIED = 0
BLANK_REASON = 0
UNIQUE_PATHS = 2624
```

The row-level authority is the lossless sharded transport `STEP_14A_CURRENT_SITE_RECONCILIATION_TRANSPORT.json` plus ordered `STEP_14A_CURRENT_SITE_RECONCILIATION_B64_CHUNK_01.txt` … `CHUNK_09.txt`. Reassembly is concatenate -> base64-decode -> gunzip -> UTF-8 TSV. Decoded TSV: 354792 bytes, 2624 rows, SHA-256 `d7329636c7959dcb44f93f59699720e4945ee740ce94b88e3acc033fa457fc6a`. Reason meanings are in `STEP_14A_CLASSIFICATION_REASON_CODES.tsv`.

## Architecture-material delta

All 21 material URLs were manually reconciled against the frozen 168 structural units and 21 Step-13 query-family cases. Full row-level decisions are in `STEP_14A_ARCHITECTURE_DELTA.tsv`.

Primary/state changes:

- `OPEN_BALCONY_FINISHING` -> exact existing owner `/balkony-i-lodzhii/otdelka-balkonov`.
- `PRIVATE_HOUSE_PVC_WINDOWS_WOODEN_HOUSE` -> exact specialist `/okna-rehau/po-tipu-doma/okna-v-derevyannyj-dom`.
- sliding-only balcony intent -> `/balkony-i-lodzhii/razdvizhnye-okna-na-balkon`; explicit cold intent remains on `/balkony-i-lodzhii/holodnoe-osteklenie`.
- sliding veranda/terrace intent -> `/verandy/razdvizhnye-okna-na-verandu`; broad non-sliding outdoor glazing remains on `/verandy`.

Routing owner update:

- `GLASS_UNIT_PRODUCT_SELECTION` gains exact commercial hub `/okna-rehau/steklopakety-dlya-plastikovykh-okon`, with manufacturing/info pages as supporting evidence.

Same-task competitor/cannibalization candidates, with prior supported primaries retained and no destructive action asserted:

- `/okna-rehau/panoramnye-okna-rehau`
- `/okna-rehau/po-tipu-doma/okna-dlya-kottedzhej-i-zagorodnyh-domov`
- `/stati/sravnenie-profilej-rehau`

The other 13 material rows are narrower supporting/intersection updates (Provedal, cold-panoramic/French balcony, room-specific/private-house, size catalog, selection guides, glass-unit info/manufacturing, frameless/outdoor type-choice). They do not displace the broader owner outside their explicit modifier.

## Architecture-relevant ERROR resolution

Inside the 2624 current-minus universe, 676 rows had crawl status `ERROR`. Classification reduced these to 5 architecture-material errors. All 5 were independently confirmed live HTML on 2026-09-02:

- `/stati/steklopakety-osobennosti-i-vidy`
- `/stati/kakoj-profil-i-firma-luchshe`
- `/stati/vidy-i-tipy-ostekleniya-verandy-plyusy-i-minusy`
- `/okna-rehau/izgotovlenie-steklopaketov-na-zakaz`
- `/verandy/razdvizhnye-okna-na-verandu`

Therefore `MATERIAL_ERROR_TOTAL=5`, `RESOLVED=5`, `UNRESOLVED=0`. The remaining 671 error rows are explicitly non-material/out-of-scope and cannot alter accepted Search ownership under their recorded reason classes.

## Internal-link topology and safety

Run9 literal topology is preserved without rerun:

```text
CLASSIFIED = 15/15
AS_IS_PRESENT = 9
AS_IS_ABSENT_PLANNED = 6
BLOCKED_OR_UNVERIFIED = 0
```

Recommendation state remains separate from as-is state.

Safety:

```text
NEW_PAGE_CREATE_ACTIONS = 0
DESTRUCTIVE_ACTIONS = 0
MERGE_DELETE_REDIRECT_CANONICAL_ACTIONS = 0
PROVIDER_CALLS_STEP14 = 0
GENSEARCH_OR_ALICE_CALLS = 0
```

## Limitation and QA

Direct XML sitemap reconciliation was not obtained in the Run10 browser environment and is not rewritten as success. Operational completeness is accepted for the main-host recursive method because the durable queue closed at `PENDING=0`, `PROCESSING=0`, `SILENT_SKIP=0` and all 2624 newly surfaced URLs were classified. This is not a mathematical claim that no undiscoverable URL exists. GEO subdomains remain outside the current Moscow main-host freeze unless separately scoped.

QA: 2624/2624 classified; 21/21 material manually reconciled; 5/5 material errors resolved; deterministic 60-row bulk spot-check across 12 largest reason buckets PASS; topology 15/15 PASS. Machine authority: `STEP_14A_RECONCILIATION_QA_2026-09-02.json`.

## Final gate

```text
STEP_14A.1 RECURSIVE CURRENT-SITE DISCOVERY = COMPLETE
STEP_14A.2 REPAIRED REPORT / INTEGRITY = PASS
STEP_14A.3 NEW-URL SEMANTIC/SCOPE RECONCILIATION = PASS
STEP_14A.4 ARCHITECTURE-RELEVANT ERROR RESOLUTION = PASS
STEP_14 FINAL = PASS
STEP_15 EXECUTED = FALSE
STEP_15 NEXT LEGAL WORK = PRE-STEP METHOD RESEARCH/REVIEW ONLY
STEP_16 EXECUTED = FALSE
```

Step-14 PASS does not authorize a provider call.
