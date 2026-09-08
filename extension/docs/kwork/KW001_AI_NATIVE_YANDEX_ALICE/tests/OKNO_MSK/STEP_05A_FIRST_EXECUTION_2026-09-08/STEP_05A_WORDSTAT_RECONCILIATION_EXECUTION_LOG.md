# Step 5A.5 Wordstat reconciliation execution log

## 2026-09-08 — baseline

- Remote branch fetched and read at `e733d4051e5a0704d60370b14326fd1bc23a655a`.
- Handoff, Level-1 candidate method, Step 5A execution authorities, 14 raw envelopes, current Stage-5 semantic master and canonical-unit authority read.
- Protected client release baseline preserved.

## 2026-09-08 — material block 1

- Normalized 14/14 seed executions.
- Extracted 21/21 direct result rows and 139/139 associations.
- Preserved `EMPTY_PROVIDER_RESULT` and `TOTALCOUNT_ONLY` distinctions.
- Persisted competitor-page → seed → raw Wordstat lineage without provider calls.

Remote readback: PASS at remote commit `48d6689a53ff4b21144213a4c1feb7016ab7ef42`.

## 2026-09-08 — material block 2

- Reconciled all 160 returned rows against current semantic authority or an explicit noise/scope/hold boundary.
- Kept 56 already-covered rows, 51 irrelevant-noise rows, 26 off-scope rows and 7 HOLD rows out of the Search package.
- Preserved 20 phrase occurrences across 8 genuinely new returned-phrase families.
- Added one separately evidenced `totalCount`-only direction (`окна для старого фонда`) without inventing a phrase row.
- Materialized exactly 9 deduplicated ordinary-Yandex-Search requirements for Main ChatGPT.

Remote readback: pending commit/push.
