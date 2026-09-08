# KW-002 Blood & Sand — ALLOWED INPUTS AND SEALED SOURCES

Status: **FROZEN PRE-EXECUTION SOURCE BOUNDARY / CLIENT INPUT MATERIALIZED / ROADMAP OWNER REVIEW PENDING**

## 1. Purpose

The Blood & Sand rehearsal must prove that KW-002 can build a semantic core and site architecture from scratch. Existing project research therefore cannot be used as hidden analytical input.

## 2. Canonical client-supplied authorities

```text
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md
CLIENT_SUPPLIED_PRODUCT_CATALOG.csv
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
CLIENT_SUPPLIED_OUT_OF_SCOPE_SELLER_LINES.csv
```

These are treated as client/order inputs, not SEO conclusions.

## 3. Exact marketplace source artifacts admitted for the clean rehearsal

### Source A — Wildberries current seller cards

```text
repository = MaksimUnimax/blood_sand
source path = marketing/data/normalized/marketplace/wildberries/20260908__wb__cards-list__fresh-current108-identities.csv
source class = CLIENT_SUPPLIED_MARKETPLACE_LISTING_IDENTITIES
observed rows = 108
client-declared in-scope rows = 88
client-declared out-of-scope rows = 20
```

Allowed use:

```text
nmID / listing identity
SKU/barcode identity
exact current listing title
client-declared scope membership
```

The source is a mechanically normalized identity list from the current seller-card collection. Its SEO/analytical interpretation is forbidden at intake.

### Source B — Ozon product/listing identities

```text
repository = MaksimUnimax/blood_sand
source path = marketing/data/raw/marketplace/ozon/20260811T1025Z__ozon__stocks-current__all.json
source class = CLIENT_SUPPLIED_RAW_MARKETPLACE_CATALOG
returned product/listing rows = 76
```

Allowed fields/uses:

```text
product_id
marketplace SKU identity
offer_id / product title
presence of a product/listing identity in the supplied catalog
```

Stock quantities/reserved quantities may remain in the raw source but are not SEO-demand or SEO-priority evidence.

## 4. Intake accounting

```text
WB target listing rows = 88
Ozon listing rows = 76
Total admitted in-scope marketplace listing rows before reconciliation = 164
Cross-platform unique-product count = NOT YET DETERMINED
```

The catalog may contain duplicates, variants, repeated symbols and cross-platform representations. Step 01 must resolve the factual product/variant model where needed.

```text
LISTING ROW != UNIQUE PRODUCT
SAME TITLE != AUTOMATIC SAME VARIANT
PRODUCT TITLE != SEARCH QUERY
PRODUCT EXISTS != SEO PRIORITY
```

## 5. Allowed before final KW-002 freeze

Allowed source classes:

```text
A. KW-002 Level 1 documentation;
B. KW-002 Level 2 step documentation;
C. this job manifest/flow/source files;
D. the canonical client-supplied files in Section 2;
E. the exact marketplace source artifacts in Section 3;
F. current external methodology sources explicitly approved for the current step;
G. fresh Wordstat/Search/AI-search evidence acquired during this KW-002 job under its own provenance;
H. fresh public competitor pages discovered by this KW-002 job through current Yandex Search when the relevant Level-2 step authorizes them.
```

## 6. Default deny for all other Blood & Sand project materials

Before final freeze:

```text
DEFAULT BLOOD_SAND REPOSITORY ACCESS = DENY
EXCEPTION = exact source(s) explicitly whitelisted in this file
```

Do not use other files merely because they contain convenient product names or summaries.

## 7. Sealed / prohibited before final freeze

Do not open or use as execution inputs any prior Blood & Sand analytical artifacts containing conclusions from earlier research, including equivalents of:

```text
prior Wordstat reports/tables
prior Wordstat seed lists
prior query/opportunity maps
prior Search/SERP research
prior Alice/AI research
prior competitor analysis
prior buyer-research conclusions
prior SEO priorities
prior cluster/page decisions
prior IA/Page Jobs
prior semantic recommendations
prior conclusions copied into another repository/test
prior normalized/derived/ledger data that encodes analytical decisions
```

Exception: the exact WB current identity file in Section 3 is admitted only for its listing identity/title fields; no external conclusions attached to it may be imported.

## 8. Raw/current business facts vs old analysis

Allowed:

```text
brand/business description supplied in CLIENT_SUPPLIED_BRIEF.md
client-declared product scope
exact product/listing title
product/listing/SKU identity
marketplace sales-channel fact
region/business operations supplied by owner
```

Not allowed before final freeze:

```text
"this product family is SEO priority"
"this query is strong/weak"
"this is a competitor"
"this should be a separate page"
"Alice wants a hybrid page"
"this cluster was previously accepted"
"this old demand number should be reused"
```

Those are analytical conclusions and must be re-earned.

## 9. Clean-context requirement

Any clean new conversation or ChatGPT Work execution used for this rehearsal receives a whitelist of allowed paths/files.

```text
DEFAULT = DENY OLD BLOOD_SAND RESEARCH
```

If a needed business fact is missing from the current admitted product inputs, obtain it from a new client statement or newly admitted raw/current source rather than opening an old mixed research artifact.

## 10. After final freeze

Only after Step 20 has frozen the new KW-002 result may prior Blood & Sand research be opened for a separate regression comparison.

The comparison must record that the prior work was opened after the new result freeze and must not silently rewrite the already frozen baseline.

## 11. Current source-freeze markers

```text
CLIENT_BRIEF_MATERIALIZED = true
CLIENT_ASSORTMENT_MANIFEST_MATERIALIZED = true
WB_SOURCE_ROWS_OBSERVED = 108
WB_IN_SCOPE_ROWS_ADMITTED = 88
WB_OUT_OF_SCOPE_ROWS_DECLARED = 20
OZON_ROWS_ADMITTED = 76
IN_SCOPE_LISTING_ROWS_BEFORE_RECONCILIATION = 164
CROSS_PLATFORM_UNIQUE_PRODUCT_COUNT = NOT_YET_DETERMINED
OLD_BLOOD_SAND_ANALYTICAL_INPUTS_ALLOWED = 0
WORDSTAT_PRIOR_INPUTS_ALLOWED = 0
SEARCH_PRIOR_INPUTS_ALLOWED = 0
ALICE_PRIOR_INPUTS_ALLOWED = 0
COMPETITOR_PRIOR_INPUTS_ALLOWED = 0
OLD_CLUSTER_OR_IA_INPUTS_ALLOWED = 0
```
