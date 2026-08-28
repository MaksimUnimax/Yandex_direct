# KW-001 / OKNO-MSK — STEP 02 SEED / QUERY PLAN

Date: 2026-08-28  
Status: **FROZEN PRE-WORDSTAT PLAN**

Depends on:

```text
TEST_ORDER.md
STEP_01_ACCEPTANCE.md
STEP_01_MERGED_SITE_INVENTORY.md
STEP_01_MERGED_BUSINESS_PAGE_MODEL.md
OPEN_QUESTIONS_FOR_CLIENT.md
../../WORKING_RUNBOOK_FOR_CHATGPT.md
```

No Wordstat, ordinary Search or GenSearch evidence was opened while creating this plan.

---

## 1. Purpose of Step 02

Step 02 converts the merged factual site/business model into a bounded first Wordstat acquisition manifest.

It does **not** attempt to write the semantic core manually.

```text
STEP 01
= what the business/site appears to contain

STEP 02
= which starting search phrases will be used to discover actual Yandex demand

STEP 03+
= provider evidence, cleanup and controlled expansion
```

### Rule

**RULE** — freeze the first seed manifest before opening Wordstat results.  
**PURPOSE** — prevent hindsight-driven seed selection where the analyst keeps adding phrases only because attractive provider results were already seen.  
**EVIDENCE** — project working runbook requires pre-provider freeze and iterative, auditable expansion.  
**FAILURE IF IGNORED** — request count, coverage and economics become impossible to audit; the resulting core can be cherry-picked around observed results.  
**REVIEW TRIGGER** — later test evidence may change the commercial seed-count default, but each individual order still requires a pre-provider manifest.

---

## 2. Frozen provider assumptions for first pass

```text
method = WORDSTAT_API_V1.getTop via accepted durable batch hand
region_label = Moscow
region_id = RESOLVE/VERIFY AT STEP-03 PREFLIGHT; DO NOT GUESS IN THIS FILE
devices = DEVICE_ALL
operators = NONE for discovery pass
numPhrases_per_seed = 200
pass_1_seed_count = 18
pass_1_max_provider_requests = 18
theoretical_raw_row_ceiling_before_cross-seed_duplicates = 3600
```

### Why broad phrases / no exact operators in pass #1

**RULE** — first pass uses broad discovery phrases without exact-frequency operators.  
**PURPOSE** — expose synonyms, modifiers, subtopics and user wording rather than measuring only the literal seed form.  
**FAILURE IF IGNORED** — an exact-first workflow can miss the vocabulary needed to build the semantic universe.  
**REVIEW TRIGGER** — exact/operator-based measurements may be added later for a specifically sold exact-frequency task; they are not the purpose of this pass.

### Why `200` phrases per seed

`200` is a **provisional productization setting**, not an industry standard.

**PURPOSE** — balance discovery breadth against analyst review volume. With 18 seeds the theoretical ceiling is 3,600 raw rows before cross-seed duplication, which is large enough to expose vocabulary but bounded enough for progressive cleanup and a second targeted pass.  
**FAILURE IF IGNORED** — setting 2,000 for every seed could create up to 36,000 raw rows in the first pass, making the 7,500 RUB base rehearsal operationally unrealistic before we have measured marginal value. Setting the count too low may hide useful subfamilies.  
**REVIEW TRIGGER** — after this test record how many of the 200 slots were useful, duplicated or noisy; revise the default for the next test if evidence supports it.

---

## 3. Frozen first-pass seed manifest

| ID | Business family | Seed phrase | Why this seed exists | What it is intended to discover/test |
|---|---|---|---|---|
| S01 | B01 broad PVC-window purchase | `пластиковые окна` | broadest core commercial root | generic purchase vocabulary, installation/price/manufacturer modifiers, alternative wording |
| S02 | B02 REHAU brand/profile selection | `окна rehau` | branded family is materially distinct in the current site architecture | brand demand, profile/model wording, buy/price/compare modifiers |
| S03 | B03 window application/design | `французские окна` | representative design/application landing from Step 01 | floor-to-ceiling/panoramic/design wording and whether the job expands beyond a single label |
| S04 | B04 windows by house series | `окна п 44` | bounded representative of the repeated house-series family; not an attempt to query every series | whether house-series-specific window demand exists and what modifiers users apply |
| S05 | B05 PVC/REHAU doors | `пластиковые двери` | broad door-family root | balcony/entrance/sliding/use-case vocabulary and commercial modifiers |
| S06 | B06 balcony/loggia broad glazing | `остекление балконов` | highest-complexity broad balcony root | warm/cold, loggia, price, finishing, material, geometry and other demand branches |
| S07 | B07 balcony engineering solution | `остекление балкона с крышей` | representative physical/engineering job distinct from broad glazing | roof/engineering/project modifiers and related structural solution vocabulary |
| S08 | B08 balcony by house series | `остекление балкона п 46` | representative of a direct balcony-series landing; intentionally separate from S04 | whether series-specific balcony intent exists as its own demand job |
| S09 | B09 local/GEO purchase | `пластиковые окна митино` | bounded representative of Moscow-district GEO demand; primary test region remains Moscow | locality modifiers and whether district-specific purchase demand is observable |
| S10 | B10 veranda/terrace/gazebo glazing | `остекление веранды` | broad outbuilding glazing root | veranda/terrace/gazebo, warm/cold, seasonal/year-round, material vocabulary |
| S11 | B11 aluminium/cold glazing | `алюминиевые окна` | material-led family exists independently of object-led cold glazing | aluminium/Provedal/opening/use-case vocabulary and commercial demand |
| S12 | B12 accessories/safety/customisation | `аксессуары для пластиковых окон` | bounded umbrella seed for a large supporting commercial family | which accessory classes appear as independent search demand and which modifiers dominate |
| S13 | B13 installation acquisition | `установка пластиковых окон` | installation can be a separate acquisition job and must not be inferred from product demand alone | standalone installation/process/price/GOST-related demand |
| S14 | B13 repair/aftercare acquisition | `ремонт пластиковых окон` | repair is a materially different post-purchase service job from installation | repair/adjustment/replacement/service vocabulary |
| S15 | B14 price/calculation | `цены на пластиковые окна` | direct budget/comparison job | price/cost/calculation/configuration modifiers and whether calculator-style wording emerges |
| S16 | B14 finance | `окна в рассрочку` | financing is not guaranteed to emerge from generic price demand and has a dedicated page job | instalment/credit/payment wording and standalone acquisition value |
| S17 | B15 informational selection | `как выбрать пластиковые окна` | existing informational selection layer must be tested against real human demand | profile/glass/hardware/noise/heat/selection questions and explanatory vocabulary |
| S18 | B16 manufacturer/trust intent | `пластиковые окна от производителя` | manufacturer intent may be a separate landing job or only a trust modifier | manufacturer/factory/production/direct-price vocabulary |

---

## 4. What is deliberately NOT seeded separately in pass #1

The following Step-01 entities are **not** interpreted as absent or unimportant. They are deliberately withheld from first-pass direct seeding to keep acquisition bounded:

```text
individual REHAU model names beyond the branded umbrella
all French/coloured/stained-glass/design variants
all house series
all balcony geometries
panoramic / extension / second-contour variants
all districts/cities/subdomains
warm and cold veranda as separate first-pass seeds
sliding vs hinged aluminium
individual accessories/security products
warranty / extended warranty
slopes finishing
calculator as a literal utility query
all article topics
```

### Purpose

The first pass is designed to discover vocabulary and measure whether the umbrella roots expose these branches. The second pass exists specifically to add targeted seeds where the first pass or the frozen site model shows a material gap.

### Failure if ignored

Seeding every known URL label immediately would make the semantic core mirror the site's existing architecture instead of testing whether users actually formulate demand that way. It would also inflate provider requests before marginal value is known.

---

## 5. Pass #2 expansion rules — reasons must be explicit

No second-pass seed may be added merely because it sounds useful.

Every added seed must carry one or more reason codes:

```text
NEW_VOCABULARY
= pass #1 reveals a meaningful synonym/term not covered by current seeds

DISTINCT_USER_JOB
= provider evidence shows a different purchase/selection/problem job

KNOWN_SUBFAMILY_GAP
= a Step-01 material family is not represented in pass #1 top results, so absence cannot safely be inferred

BUSINESS_CRITICAL_GAP
= mock/real client says a commercially important offer requires direct measurement

AMBIGUOUS_MEANING
= broad root mixes meanings and a narrower seed is required to isolate the client's job

GEO_REPRESENTATIVE_GAP
= bounded GEO model requires another representative to distinguish locality types

SERIES_TEMPLATE_GAP
= one representative series is insufficient to know whether the repeated family is generalizable
```

### Provisional pass-2 budget

```text
pass_2_seed_list = NOT YET FROZEN
pass_2_max_additional_seeds_without_scope_revision = 12
combined provisional Wordstat getTop request ceiling = 30
```

This is a productization budget, not a permanent commercial promise. Step 03/04 results must justify every additional request.

---

## 6. Stop rules for Wordstat expansion

Stop adding seeds when one or more of the following is true:

```text
new seeds mainly reproduce phrases/families already present
new phrases are predominantly irrelevant to the business
remaining known site subfamilies have no material business/page-job reason to be measured separately
request budget is reached
the next seed has no specific decision or discovery gap attached
```

Do **not** stop merely because one broad seed failed to surface a Step-01 material family. That is exactly what `KNOWN_SUBFAMILY_GAP` is for.

### Purpose

**PURPOSE** — achieve discovery saturation by marginal information gain, not by arbitrary recursive scraping or premature false negatives.

---

## 7. Geography rule for this rehearsal

Frozen mock order says:

```text
primary_region = Moscow
```

Therefore:

```text
S09 uses a Moscow district as the bounded GEO representative.
Moscow-region city/subdomain demand is NOT expanded in the base pass unless the mock order is formally revised.
```

The existence of public city subdomains remains part of Step-01 architecture evidence, but it does not silently broaden the commercial region.

### Purpose

Prevent site discovery from silently changing the client brief from `Moscow` to `Moscow + all Moscow Region cities`.

---

## 8. Device rule

Pass #1 uses:

```text
DEVICE_ALL
```

No desktop/mobile split is justified yet.

### Purpose

The current service needs total human-demand discovery first. Device segmentation adds provider/analysis complexity and should only be introduced if a later business decision depends on it.

---

## 9. Required Step-03 evidence record per seed

When Wordstat pass #1 is executed, every seed must preserve at minimum:

```text
seed_id
seed_phrase
business_family
normalized provider command
region label + resolved provider region id
device
operators
numPhrases requested
request_id
request executed truth
provider outcome
raw result reference / payload
returned row count
cost/request ledger truth
started/completed timestamps
```

ChatGPT then records:

```text
unique phrases after mechanical exact dedupe
obvious reject count
review count
new vocabulary
new user-job candidates
known Step-01 subfamilies still missing
pass-2 recommendation + reason code
```

---

## 10. What Step 02 does NOT decide

No conclusion is made here about:

```text
actual Wordstat demand
frequency level
final keywords
final clusters
SERP similarity
which existing page owns a query
cannibalization
new/merge/delete page decisions
AI-search importance
commercial priority
```

Those require later evidence.

---

## 11. Step-02 freeze

```text
seed_manifest_frozen = true
first_pass_seed_count = 18
first_pass_max_requests = 18
numPhrases_per_seed = 200 provisional
region = Moscow; provider ID must be verified before execution
device = DEVICE_ALL
operators = NONE
pass_2_reason_codes_frozen = true
pass_2_max_additional_seeds_without_revision = 12
Wordstat requests before Step-02 freeze = 0
Search requests before Step-02 freeze = 0
GenSearch requests before Step-02 freeze = 0
```

Acceptance marker candidate:

```text
KW001_OKNO_MSK_STEP_02_SEED_PLAN_FROZEN = true
```
