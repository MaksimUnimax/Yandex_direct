# KW-002 Blood & Sand — ALLOWED INPUTS AND SEALED SOURCES

Status: **FROZEN / Ozon-ONLY ASSORTMENT AUTHORITY / CLEAN BASELINE ACTIVE**

## 1. Purpose

KW-002 must build the semantic core and planned site architecture from scratch without importing prior Blood & Sand analytical conclusions.

## 2. Canonical client-supplied authorities

Allowed client-input files:

```text
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
```

Job-control files are also allowed:

```text
JOB_MANIFEST.md
JOB_FLOW.md
STEP_00_SCOPE_AND_SOURCE_FREEZE_2026-09-08.md
current Step-01 pre-step/work handoff authority
```

## 3. Exact authoritative assortment source

```text
repository = MaksimUnimax/blood_sand
path = marketing/data/raw/marketplace/ozon/20260811T1025Z__ozon__stocks-current__all.json
source class = CLIENT_SUPPLIED_RAW_MARKETPLACE_CATALOG
rows = 76
```

Allowed product/business fields:

```text
product_id
marketplace SKU
exact offer_id / product title
presence of product/listing identity
raw stock fields only as source facts, not SEO-demand or priority evidence
```

## 4. Wildberries correction

Latest owner instruction supersedes the earlier intake design:

```text
WB PRODUCT CATALOG = NOT ALLOWED FOR STEP 01 OR STEP 02
WB SALES CHANNEL FACT = ALLOWED AS CLIENT BUSINESS FACT
```

Previously created files:

```text
CLIENT_SUPPLIED_PRODUCT_CATALOG.csv
CLIENT_SUPPLIED_OUT_OF_SCOPE_SELLER_LINES.csv
```

remain only for historical correction traceability. They are not current evidence inputs.

## 5. Current accounting

```text
AUTHORITATIVE ASSORTMENT SOURCES = 1
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ALLOWED = 0
STEP 01 INPUT ROWS = 76
CROSS_PLATFORM JOIN = NOT APPLICABLE
```

## 6. Allowed source classes before final KW-002 freeze

```text
A. KW-002 Level 1 documentation;
B. relevant KW-002 Level 2 step documentation;
C. current job workspace/control files;
D. the three canonical client-input authorities in Section 2;
E. the exact Ozon raw source in Section 3;
F. current external methodology sources explicitly approved for the current step;
G. fresh Wordstat/Search/AI-search evidence acquired inside KW-002 under its own provenance;
H. fresh public competitor pages discovered by this KW-002 job when the relevant Level-2 step authorizes them.
```

## 7. Default deny for other Blood & Sand materials

```text
DEFAULT BLOOD_SAND REPOSITORY ACCESS = DENY
EXCEPTION = exact whitelisted source(s) above
```

Forbidden before final freeze include prior:

```text
Wordstat reports/tables/seeds
Search/SERP research
Alice/AI research
opportunity maps
competitor analysis
buyer-research conclusions
SEO priorities
cluster/page/IA/Page Job decisions
semantic recommendations
normalized/derived analytical ledgers
WB catalog identity files for Step 01/02 after the owner correction
```

## 8. Raw business facts vs analysis

Allowed:

```text
brand/business description
Ozon product_id / SKU / exact title
Ozon product identity in the supplied catalog
marketplace-channel fact
region/business operations supplied by owner
```

Not allowed as inherited truth:

```text
"this family is SEO priority"
"this query is strong/weak"
"this is a search competitor"
"this requires a separate page"
"Alice wants a hybrid page"
"this old cluster was accepted"
"reuse this old demand number"
```

## 9. Clean Work context

Any ChatGPT Work handoff receives only the exact whitelist stated in its prompt/manifest. Work may not browse old Blood & Sand research or WB product inputs merely because they exist.

## 10. After final freeze

Prior Blood & Sand research may be opened only after Step 20 for a separately recorded regression comparison.

## 11. Current markers

```text
CLIENT_BRIEF_MATERIALIZED = true
CLIENT_ASSORTMENT_MANIFEST_MATERIALIZED = true
OZON_ROWS_ADMITTED = 76
WB_ROWS_ADMITTED_TO_STEP01 = 0
STEP01_INPUT_ROWS = 76
CROSS_PLATFORM_RECONCILIATION_REQUIRED = false
OLD_BLOOD_SAND_ANALYTICAL_INPUTS_ALLOWED = 0
WORDSTAT_PRIOR_INPUTS_ALLOWED = 0
SEARCH_PRIOR_INPUTS_ALLOWED = 0
ALICE_PRIOR_INPUTS_ALLOWED = 0
COMPETITOR_PRIOR_INPUTS_ALLOWED = 0
OLD_CLUSTER_OR_IA_INPUTS_ALLOWED = 0
```