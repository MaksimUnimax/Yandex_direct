# STEP 04 — triage QA — 2026-09-10

Status: **PASS**

## Gate and source accounting

```text
STEP04_OWNER_GATE = PASS
CANONICAL_PRIMARY_MANIFEST_ROWS = 79
UNIQUE_RUN_ORDERS = 79
RUN_ORDER_RANGE = 1..79
INPUT_PRIMARY_PROBES_ACCOUNTED = 79/79
CURRENT_FEED_FORWARD_SOURCE_RESOLVED = 79/79
CURRENT_SOURCE_CARRIERS_READ = PASS
RAW_TREE_FILES_BYTE_READ = 96
RAW_TREE_BYTES_READ = 2136069
RAW_TREE_PATH_NUL_BYTES_SHA256 = 37735e106341fac56eef48f2fb0068d2b9a1c6ee561e2fc97eb61cfa72d7d293
CURRENT_RESULTS_OCCURRENCES_PROCESSED = 24722
CURRENT_ASSOCIATION_OCCURRENCES_PROCESSED = 1257
CURRENT_TOTAL_OCCURRENCES_PROCESSED = 25979
CURRENT_EMPTY_RUN_ORDERS = 49,50,51,57,66,67,70
CURRENT_EMPTY_RUN_COUNT = 7
SILENT_SOURCE_DROPS = 0
OCCURRENCE_ASSIGNMENT_DUPLICATES = 0
```

Every current occurrence was assigned exactly once to one preliminary family. The source-occurrence counts in the family table reconcile to **25979**. The seven empty current outcomes are represented as separate coverage-gap rows, so they are not silently lost.

The complete RAW tree was byte-read. Eleven compressed re-query envelopes were reconstructed and integrity-checked according to their accepted manifest; ten of them are current feed-forward sources. Historical broken gzip bundles were not used as current gates or substitutes. Run orders 32–48 and 50–51 use the replacement mapping from `STEP_03_RAW_RECOVERY_PROGRESS_2026-09-09.json`; run 49 uses its independent readable carrier.

## Output checks

```text
FAMILY_ROW_COUNT = 32
FAMILY_ROWS_WITH_REASON_CODE = 100%
FAMILY_ROWS_WITH_REASON_TEXT = 100%
FAMILY_ROWS_WITH_PROVENANCE = 100%
FAMILY_OCCURRENCE_SUM = 25979
FAMILY_RUN_ORDER_UNION = 1..79
TARGETED_EXPANSION_QUEUE_ROW_COUNT = 17
QUEUE_ROWS_WITH_REQUIRED_FIELDS = 100%
OWNER_CLARIFICATION_REQUIRED_COUNT = 6
FUTURE_PROVIDER_EVIDENCE_REQUIRED_COUNT = 15
```

Counts by `triage_state`:

```text
strong in-scope = 3
plausible in-scope = 4
mixed/ambiguous = 9
obvious out-of-scope = 9
coverage gap / requires expansion = 7
```

## Adversarial boundary checks

```text
LOW_FREQUENCY_ONLY_REJECTIONS = 0
FORCED_AMBIGUITY_DECISIONS = 0
SEALED_SOURCE_VIOLATIONS = 0
NEW_PROVIDER_CALLS = 0
FINAL_ROW_CLEANUP_PERFORMED = false
FINAL_CLUSTERING_PERFORMED = false
PAGE_DESIGN_PERFORMED = false
STEP05_STARTED = false
```

The `obvious out-of-scope` rows require explicit semantic context such as a vehicle model/part, named game/franchise, media format/title, place/organization/person, industrial AUMA equipment, non-product religious practice, astrology task, or non-product morphology. Frequency was not used in any reason code or decision. Short names and unclear associations remain visible as `mixed/ambiguous`.

## Unresolved evidence defects

- Current sources for run orders **49, 50, 51, 57, 66, 67 and 70** contain no observed rows. They are coverage gaps, not negative demand conclusions.
- The 76 Ozon titles do not state physical form, material, dimensions, or substantiated symbolic effects for most products.
- Ом/Аум, Гунгнир/Копьё Одина, Алатырь, Триглав, Ратиборец, Знич, Громовик, Белобог, Чернобог and Мара have observed competing meanings.
- Zodiac wording is dominated by explicit astrology contexts; the product form is not stated by the client input.
- `чётки` is mixed by provider morphology with `чётко/чёткий`.
- The physical representation of the catalog title `Молитва Иоанн Златоуст` is not stated.

These defects are materialized in the expansion queue. Resolving them would be Step05 or a client-fact request, neither of which was executed here.
