# KW-002 Blood & Sand — canonical Step03B correction handoff

Date: 2026-09-11  
Repository: `MaksimUnimax/Yandex_direct`  
Branch audited: `roadmap/kwork-productization-2026-08-28`  
Live remote authority audited: `a0d662851c2f26d7a219ec7efb7d7e37e640dce3`  
Job: `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

## 1. Required action

`FULL STEP03B REPROCESS`

This is a deterministic, rule-only reclassification of all **24,576** accepted Step03A normalized identities. It does not require Step03A reprocessing, new Wordstat/Search/GenSearch calls, Step05 evidence, or changes to the 25,979-row RAW universe.

Do not patch only the examples in this document. Apply the corrected rule order and exception logic to the full universe, then regenerate every Step03B-dependent derivative and reconcile Step04. The full row-level audit authority is:

`KW002_STEP03A_03B_INDEPENDENT_FULL_VOLUME_AUDIT_OVERLAY_2026-09-11.tsv`

## 2. Frozen input authority

- `STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv`: 24,576 identities.
- `STEP_03A_NORMALIZATION_LEDGER_2026-09-11.tsv`: 25,979 RAW occurrences.
- Frozen client brief, assortment manifest, and 76-row Ozon catalog.
- No prior sealed Blood & Sand research.
- Corrected Step04 family authority may be used only as context and reconciliation evidence, never as the sole classifier.

## 3. Defective rule classes

| Current rule/reason | Defect | Replacement rule |
|---|---|---|
| `EXCLUDE_EXPLICIT_ASTROLOGY_INFORMATION` | Runs before sufficient zodiac-product collision handling; stone/object/commercial variants are destroyed. | Exclude only explicit astrology tasks. Product + zodiac without an explicit information task is KEEP; object/commercial zodiac demand is KEEP; unresolved stone/zodiac ambiguity is HOLD. |
| `EXCLUDE_EXPLICIT_FOREIGN_ENTITY` | `футбол\w*` matches `футболка`; generic team/entity language is treated as explicit. | Token-bound sport patterns; clothing becomes an unrelated-product decision; generic team/entity collision becomes HOLD unless a foreign referent is explicit. |
| `EXCLUDE_EXPLICIT_GAME` | Generic `игра`, `мод\w*`, `id` and model-like stems are accepted as conclusive. | Named game or explicit in-game task = EXCLUDE; generic game/model token without the referent = HOLD. |
| `EXCLUDE_EXPLICIT_MEDIA` | Generic `читать`, `слушать`, `смотреть`, `скачать`, `серия` fire without enough media evidence. | Explicit work/episode/digital-consumption context = EXCLUDE; bare media action with a business product term = HOLD; title/product collisions remain HOLD unless digital-media context is explicit. |
| `EXCLUDE_EXPLICIT_ORGANIZATION` | `банк\w*` and ordered rule execution mislabel bank-card and Yandex/Dzen contexts. | Require an explicit organization referent; route physical non-client products to unrelated-product; retain unresolved platform/title collisions in HOLD. |
| `EXCLUDE_EXPLICIT_PLACE` | `купить.*дом|дом.*купить` confuses “оберег дома купить” with real estate; product marketplace queries are removed. | Exact real-estate constructions = EXCLUDE; supported product + purchase/marketplace/geo context = KEEP; unresolved place/product collision = HOLD. |
| `EXCLUDE_EXPLICIT_VEHICLE_OR_MODEL` | Vehicle brand logic precedes frozen catalog collision checks; “Звезда Лады” and a supported car-use query collide. | Explicit Chery Amulet/Renault Talisman model or part = EXCLUDE; frozen “Звезда Лады” collision = HOLD/KEEP by object/commerce; supported product explicitly for a car = KEEP. |
| `EXCLUDE_LEXICAL_GARBAGE` | Prefix `четк*` also captures possible singular/typo forms related to `чётки`. | Exclude explicit adjective/adverb morphology (`чётко`, `чёткий`, etc.); route possible rosary form/typo to HOLD. |
| KEEP fallback | Any recognized product token is kept after an incomplete blacklist, so unrecognized games, car parts and digital-media phrases survive. | Positive business recognition must still pass independent explicit foreign-context guards. Extend named-game, vehicle-part and digital-media evidence; otherwise HOLD, not blind KEEP. |
| HOLD policy | Clearly supported zodiac-product/object phrases remain HOLD; clearly foreign game/media/entity cases also remain HOLD. | Resolve only where frozen product evidence or explicit foreign context is conclusive; preserve all remaining uncertainty as HOLD/SERP_REQUIRED_LATER. |

## 4. Full-volume blast radius

Normalized identities requiring a state transition: **1,710 / 24,576**.  
RAW occurrences carried by those identities: **1,761 / 25,979**.

| Current state | Corrected KEEP | Corrected HOLD | Corrected EXCLUDE | Row total |
|---|---:|---:|---:|---:|
| KEEP | 4,788 | 207 | 79 | 5,074 |
| HOLD | 298 | 12,084 | 368 | 12,750 |
| EXCLUDE | 14 | 744 | 5,994 | 6,752 |
| Corrected total | 5,100 | 13,035 | 6,441 | 24,576 |

Raw-occurrence transition totals:

| Current state | Corrected KEEP | Corrected HOLD | Corrected EXCLUDE | Occurrence total |
|---|---:|---:|---:|---:|
| KEEP | 4,945 | 211 | 80 | 5,236 |
| HOLD | 304 | 12,828 | 368 | 13,500 |
| EXCLUDE | 14 | 784 | 6,445 | 7,243 |
| Corrected total | 5,263 | 13,823 | 6,893 | 25,979 |

## 5. Mandatory representative regression cases

These are tests, not row-specific patches.

- KEEP after correction: `оберег дома купить`; `четки в машину знак lada`; `звезда лада купить`; `кулон дева знак зодиака с камнем`.
- HOLD after correction: `амулет читать`; `серия амулет`; `талисман команды`; `звезда лада значение`; possible `четка` morphology.
- EXCLUDE after correction: `hollow knight амулеты`; `датчик температуры амулет`; explicit Chery Amulet parts; explicit film/book/chapter/game queries.
- Remain HOLD/SERP_REQUIRED_LATER: mixed product-versus-information, title-versus-product, catalog-name-versus-entity and ambiguous zodiac/stone cases without decisive evidence.

## 6. Required regenerated outputs

1. Step03B sanitized candidate pool.
2. Step03B excluded register.
3. Step03B HOLD/ambiguous register (or the combined authority with explicit state).
4. Step03B QA and reason-count table.
5. Data funnel and reconciliation-ready summary.
6. Step04 occurrence/family reconciliation against the reprocessed Step03B state.

Step03A authorities must remain byte-identical.

## 7. Required QA after reprocessing

- Input normalized identities = 24,576.
- Input RAW lineage = 25,979; unique occurrence IDs = 25,979.
- State partition is exhaustive and mutually exclusive.
- State totals sum to 24,576; raw-occurrence totals sum to 25,979.
- No frequency-based exclusion.
- No single ambiguous token is sufficient for exclusion.
- All 14 `EXCLUDE -> KEEP`, 744 `EXCLUDE -> HOLD`, 207 `KEEP -> HOLD`, 79 `KEEP -> EXCLUDE`, 298 `HOLD -> KEEP`, and 368 `HOLD -> EXCLUDE` regression rows match the accepted correction overlay, unless a documented Main ChatGPT adjudication supersedes a row.
- Each reason code reports normalized and RAW counts and bounded examples.
- False-exclusion regression suite includes astrology, media, place/home, vehicle/catalog and lexical collision cases.
- False-keep regression suite includes missed game names, vehicle parts and explicit digital-media contexts.
- `RAW_LINEAGE_LOSS = 0`.
- No Step05 evidence or provider calls used.

## 8. Stop condition

After producing the corrected Step03B authorities and the Step04 reconciliation receipt, stop for Main ChatGPT return QA. Do not start Step05.

REPROCESS_SCOPE = FULL_STEP03B_REPROCESS  
STEP03A_REPROCESS = false  
PROVIDER_CALLS_REQUIRED = 0  
STEP04_RECONCILIATION_REQUIRED = true  
STEP05_ALLOWED = false
