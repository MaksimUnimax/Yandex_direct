# STEP 5A WORDSTAT ACQUISITION SUMMARY — 2026-09-08

## Status

Step 5A.4 provider acquisition is complete.

- Bridge: `yandex-marketing-bridge v0.1.4`
- Service: `wordstat`
- Method: `getTop`
- Region: `213`
- Device: `DEVICE_ALL`
- Requested phrases per seed: `200`
- Job: `kw001-okno-msk-step05a-wordstat-gap-20260908`
- Seeds: `14`
- Succeeded: `14`
- Failed terminal: `0`
- Outcome unknown: `0`
- Pending: `0`
- Requests started: `14`
- Final job status: `COMPLETED`
- Final next safe action: `NONE`
- Final estimated acquisition cost: `0.28 RUB`

## Raw evidence authority

The complete provider envelopes are persisted in this directory:

- `STEP_05A_WORDSTAT_BATCH_START_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_01_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_02_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_03_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_04_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_05_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_06_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_07_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_08_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_09_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_10_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_11_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_12_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_13_RAW.json`
- `STEP_05A_WORDSTAT_ITEM_14_RAW.json`

Raw provider payloads are the authority. This summary is only an acquisition index and must not replace row-level evidence.

## Seed-level acquisition index

| # | Seed | Provider result shape observed | totalCount observed | Direct `results` rows visible in returned envelope |
|---:|---|---|---:|---:|
| 1 | остекление балкона П-46 | non-empty provider result | 17 | see raw item 01 |
| 2 | остекление балкона с выносом по полу | `{}` | n/a | 0 |
| 3 | гидроизоляция открытого балкона | `results + associations + totalCount` | 95 | 7 |
| 4 | солнцезащитный стеклопакет | `results + associations + totalCount` | 28 | 5 |
| 5 | многофункциональный стеклопакет | `results + associations + totalCount` | 11 | 2 |
| 6 | ударопрочный стеклопакет | `results + associations + totalCount` | 8 | 1 |
| 7 | Provedal C640 или P400 | `{}` | n/a | 0 |
| 8 | окна для старого фонда | `totalCount only` | 5 | 0 |
| 9 | окна для квартиры под аренду | `{}` | n/a | 0 |
| 10 | балкон под офис | `results + associations + totalCount` | 7 | 1 |
| 11 | балкон-кладовая | `results + associations + totalCount` | 3 | 1 |
| 12 | фальш-крыша на балкон | `{}` | n/a | 0 |
| 13 | шумоизоляция крыши балкона | `results + associations + totalCount` | 22 | 3 |
| 14 | армирование оконного профиля | `results + associations + totalCount` | 5 | 1 |

## Important interpretation boundary

1. `result = {}` is preserved as an empty provider result. It is **not** silently converted to numeric zero demand.
2. `totalCount` without returned `results` rows is not expanded or reconstructed.
3. Associations are discovery evidence only. They are not accepted semantic phrases merely because Wordstat returned them.
4. No Wordstat observation by itself determines Search intent, landing-page ownership, split/merge, or page creation.
5. Competitor-page evidence created the seed; Wordstat only validates/discovers demand around that seed.
6. Any materially new phrase/direction surviving Step 5A.5 must still go through ordinary Yandex Search validation in Step 5A.6 before final `ADD_TO_PIPELINE`.

## Step 5A.5 input contract

Work must use the 14 raw item envelopes above, together with the existing Step 5A page-evidence/seed-reconciliation authorities and current OKNO_MSK semantic authority, to:

- extract all actual `results` rows and relevant associations without inventing missing rows;
- preserve exact lineage `competitor page -> candidate seed -> Wordstat seed -> returned phrase`;
- classify provider noise/off-scope phrases;
- reconcile all returned phrases against the existing semantic core;
- distinguish genuinely new material directions from exact/close existing coverage;
- deduplicate surviving new directions;
- produce the exact bounded ordinary-Yandex-Search recheck package for Main ChatGPT;
- leave all provider execution to Main ChatGPT / Yandex Bridge;
- do not mutate client deliverables;
- do not promote Step 5A to permanent Level-1 methodology based on this execution alone.

## Current transition

`STEP_5A_4_WORDSTAT_ACQUISITION = COMPLETE`

`NEXT_ACTION = WORK_STEP_5A_5_WORDSTAT_CLEAN_RECONCILE_AND_MATERIALIZE_SEARCH_RECHECK_PACKAGE`
