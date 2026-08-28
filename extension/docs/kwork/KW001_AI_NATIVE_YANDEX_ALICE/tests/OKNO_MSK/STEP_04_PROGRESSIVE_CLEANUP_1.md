# KW-001 / OKNO-MSK — STEP 04 PROGRESSIVE CLEANUP #1

Date: 2026-08-28  
Status: **ANALYTICAL CLEANUP COMPLETE / PRE-EXPANSION TRIAGE FROZEN**

Depends on:

```text
STEP_03_ACCEPTANCE.md
STEP_03_WORDSTAT_PASS1_EXECUTION_LOG.md
STEP_03_*_CHECKPOINT*.md
STEP_01_MERGED_BUSINESS_PAGE_MODEL.md
OPEN_QUESTIONS_FOR_CLIENT.md
../../WORKING_RUNBOOK_FOR_CHATGPT.md
```

## 1. Purpose

Perform the first semantic cleanup over Wordstat pass #1 without prematurely clustering, mapping pages, or deciding final client semantics.

The universal runbook requires only three states at this stage:

```text
KEEP
REJECT_OBVIOUS
REVIEW
```

This step is intentionally conservative. It removes only clearly unsupported noise and preserves uncertainty for later business/SERP evidence.

---

## 2. Governing rule

**RULE** — ambiguous phrases go to `REVIEW`, not to deletion.

**PURPOSE** — preserve potentially valuable demand until business truth or ordinary Yandex SERP evidence can resolve intent/page boundaries.

**EVIDENCE** — accepted KW-001 runbook; mock-order business questions for repair, accessories, finance, standalone installation and GEO remain partly unresolved.

**FAILURE IF IGNORED** — potentially valuable acquisition/service/support demand can disappear from the project merely because its commercial role is not yet known.

**REVIEW TRIGGER** — explicit client clarification or later SERP evidence resolving the ambiguity.

---

## 3. Classification meaning

### KEEP

Use when the phrase/vocabulary is clearly relevant to a provisionally active observed business family and the Moscow test scope.

`KEEP` means only:

```text
retain for the next semantic stages
```

It does **not** mean:

```text
separate page approved
primary keyword approved
high priority approved
final cluster approved
```

### REJECT_OBVIOUS

Use only for clear cases such as:

```text
wrong product / wrong semantic meaning
clearly unrelated association
wrong geography outside the frozen Moscow scope
job-seeker/employment intent
used/marketplace intent incompatible with the observed new-window business
exact duplicate / mechanical duplicate
```

### REVIEW

Use when relevance is plausible but one of these remains unresolved:

```text
client commercial priority
standalone-vs-bundled service role
accessory/upsell-vs-acquisition role
finance conversion-vs-acquisition role
informational-vs-commercial user job
possible separate page boundary
competitor/comparison usefulness
SERP intent ambiguity
```

---

## 4. Cross-pass cleanup rules applied

### Geography

Frozen test region is Moscow city (`213`). Therefore:

```text
Moscow / Moscow districts = KEEP or REVIEW by intent
Moscow Region towns / other Russian cities / foreign locations = REJECT_OBVIOUS for this mock order
```

This is a scope classification, not a statement that those locations lack demand or are invalid for the real business.

### Frequency

Low count alone is never a rejection reason.

Examples preserved:

```text
P-44 demand = real but modest
P-46 balcony demand = sparse but successful provider result
roofed-balcony demand = low but directly relevant
```

### Associations

Wordstat associations are vocabulary discovery evidence, not automatically retained semantics.

Relevant associations may become expansion candidates; unrelated associations are `REJECT_OBVIOUS`.

### Business-priority unknowns

Mock-order questions still unresolved:

```text
standalone installation priority = UNKNOWN
repair/service acquisition priority = UNKNOWN
accessories standalone priority = UNKNOWN
finance acquisition priority = UNKNOWN
```

Therefore these families are not deleted, but their standalone commercial role remains `REVIEW` until later evidence/clarification.

---

# 5. Seed-family cleanup ledger

## S01 — `пластиковые окна`

Primary state: **KEEP**

KEEP directions:

```text
broad PVC purchase
Moscow purchase
price / installation / turnkey
REHAU/profile vocabulary
balcony/application vocabulary
manufacturer/factory vocabulary
selection/review vocabulary
```

REVIEW directions:

```text
repair/regulation
accessories
DIY/how-to
```

REJECT_OBVIOUS:

```text
used / marketplace demand
clearly unrelated associations
wrong-region variants
```

Reason: broad root remains the main demand-discovery family but contains multiple later boundaries.

---

## S02 — `окна rehau`

Primary state: **KEEP**

KEEP:

```text
REHAU purchase / Moscow / price / installation
Grazio / Blitz / Delight / Intelio vocabulary
60/70/80-mm selection vocabulary
brand/profile selection
```

REVIEW:

```text
REHAU vs Veka/KBE/Melke/Kaleva comparisons
repair/accessory tails
official/dealer/manufacturer boundary
```

REJECT_OBVIOUS:

```text
wrong-region and unrelated associations
```

No specific REHAU model receives a separate-page decision here.

---

## S03 — `французские окна`

Primary state: **KEEP + REVIEW MIXED**

KEEP:

```text
French/floor-to-ceiling windows
balcony/loggia application
private-house application
panoramic/sliding interpretation
purchase / price / Moscow / installation
replacement of balcony block where window meaning is clear
```

REVIEW:

```text
curtains/blinds/accessory formulations tied to French windows
design/explanation formulations with unclear commercial vs informational job
```

REJECT_OBVIOUS:

```text
language/translation meanings
clearly non-window uses of “French”
unrelated associations
```

Important result: the seed is semantically contaminated but still useful; contamination is not provider failure.

---

## S04 — `окна п 44`

Primary state: **KEEP**

Retain the real house-series vocabulary including:

```text
окно п 44
дом п 44 окна
размеры окон п 44
окна серии п 44
пластиковые окна п 44
```

No separate P-44 landing decision is made. Later SERP must decide whether this is:

```text
independent house-series cluster
broader house-series ownership
supporting long-tail only
```

Low frequency is explicitly not a rejection reason.

---

## S05 — `пластиковые двери`

Primary state: **KEEP**

KEEP:

```text
PVC doors broad purchase
entrance doors
balcony doors
sliding doors
with/without glass
Moscow / price / installation
```

REVIEW:

```text
repair/regulation
hardware/fittings
```

REJECT_OBVIOUS:

```text
used/marketplace demand
wrong-region/unrelated noise
```

Later SERP must decide hub vs subtype boundaries.

---

## S06 — `остекление балконов`

Primary state: **KEEP**

KEEP:

```text
balcony/loggia glazing broad
Moscow / price / turnkey
warm glazing
cold glazing
aluminium glazing
PVC glazing
panoramic glazing
sliding glazing
frameless glazing
finishing / insulation bundle
house-series vocabulary
roof / extension / physical-solution vocabulary
```

REVIEW:

```text
DIY
permissions/legal questions
repair/replacement adjacency
individual engineering variants as separate jobs
```

REJECT_OBVIOUS:

```text
wrong-region / unrelated noise
```

This is a high-complexity boundary family; cleanup does not flatten it into one future page.

---

## S07 — `остекление балкона с крышей`

Primary state: **KEEP**

KEEP:

```text
остекление балкона с крышей
price
Moscow
Khrushchev / building-context formulation
last-floor formulation
```

REJECT_OBVIOUS:

```text
roofing/aerator and other unrelated associations
unrelated bath/curtain/etc associations
```

Low totalCount (`48`) is retained as a real engineering subfamily, not rejected for volume alone.

---

## S08 — `остекление балкона п 46`

Primary state: **KEEP / PAGE BOUNDARY REVIEW**

Provider result was successful with `totalCount=19` and no detailed results array.

Interpretation:

```text
real measured family != zero demand
successful sparse payload != provider error
```

Retain the phrase as evidence for the balcony-house-series family; later SERP decides whether it is independent or supporting semantics.

---

## S09 — `пластиковые окна митино`

Primary state: **KEEP**

KEEP:

```text
пластиковые окна в митино
local address/purchase formulation where commercial intent is plausible
```

REVIEW:

```text
ремонт пластиковых окон в митино
```

because repair acquisition priority remains unknown.

REJECT_OBVIOUS:

```text
unrelated Mitinskaya-street / weather / people / transfer / other association noise
```

This validates a real Moscow-district demand family but does not prove that every district deserves a separate landing.

---

## S10 — `остекление веранды`

Primary state: **KEEP**

KEEP:

```text
veranda glazing
veranda + terrace
price
aluminium
sliding
cold / warm
frameless
panoramic
private house / dacha
turnkey
```

REVIEW:

```text
gillotine glazing
soft/flexible glazing
polycarbonate
wooden glazing
other material/system variants whose client offer is not yet verified at semantic level
```

REJECT_OBVIOUS:

```text
Ekaterinburg / SPb / Voronezh / Novosibirsk / other out-of-scope GEO
clearly unrelated associations
```

Object (`veranda/terrace`) vs regime/material (`warm/cold/aluminium`) remains a later SERP boundary question.

---

## S11 — `алюминиевые окна`

Primary state: **KEEP**

KEEP:

```text
aluminium windows broad
sliding
Moscow / buy / price
balcony / loggia
veranda / terrace
warm / cold
panoramic
Provedal / Alutech / Schüco vocabulary
manufacture / installation
```

REVIEW:

```text
repair
hardware/fittings
screens/accessories
PVC-vs-aluminium comparison
brand/system boundaries
```

REJECT_OBVIOUS:

```text
metallurgy/alloy meanings
used/marketplace demand
clearly unrelated associations
wrong-region variants
```

Material-led intent vs object-led cold-glazing intent remains unresolved.

---

## S12 — `аксессуары для пластиковых окон`

Primary state: **REVIEW**

Literal root is relevant to an observed accessory family but standalone acquisition priority is unknown.

Observed evidence:

```text
аксессуары для пластиковых окон = 29
оконная фурнитура association = 1458
```

Therefore:

```text
literal accessory vocabulary = REVIEW
оконная фурнитура = expansion candidate / NEW_VOCABULARY
```

Do not reject the family merely because the literal seed is small.

---

## S13 — `установка пластиковых окон`

Primary state: **KEEP + REVIEW SPLIT**

KEEP where installation is clearly bundled with the client's window purchase flow:

```text
windows with installation
price with installation
Moscow with installation
turnkey
manufacturer + installation
```

REVIEW:

```text
standalone installation service
DIY installation/instructions
slopes / sills / screens as separate service jobs
```

REJECT_OBVIOUS:

```text
job-seeker / монтажник employment intent
wrong-region noise
```

Observed association `монтаж окон = 5019` is a strong `NEW_VOCABULARY` expansion candidate.

---

## S14 — `ремонт пластиковых окон`

Primary state: **REVIEW**

The family is clearly real and matches observed site assets, but mock-client acquisition priority is explicitly unknown.

Retain for later evidence:

```text
repair broad
Moscow repair
price / inexpensive
repair + regulation
master/callout
urgent repair
mechanism/hardware
replacement of glazing unit
Moscow district/service GEO
```

REJECT_OBVIOUS:

```text
other-city GEO outside Moscow
marketplace noise
clearly unrelated meanings
```

Do not promote or delete the family before client/business resolution.

---

## S15 — `цены на пластиковые окна`

Primary state: **KEEP**

KEEP:

```text
broad price
Moscow price
price with installation
balcony/dacha/kitchen application price
replacement price
size-specific price
calculator/calculate-price vocabulary
```

REVIEW:

```text
accessory price tails
repair/replacement-component price tails
```

REJECT_OBVIOUS:

```text
Ozon / Wildberries / Avito marketplace intent
out-of-scope cities/regions
unrelated association noise
```

A price page is not approved here; ownership may later be broad commercial page, price page or calculator utility.

---

## S16 — `окна в рассрочку`

Primary state: **REVIEW**

Commercial demand is real:

```text
окна в рассрочку = 507
пластиковые окна в рассрочку = 212
Москва = 129
без банка = 38
установка = 28
REHAU = 26
```

However finance acquisition priority remains `UNKNOWN` in the mock order.

Therefore retain the family for later business/SERP evidence without approving a standalone finance landing.

REJECT_OBVIOUS:

```text
out-of-scope GEO
unrelated associations
```

---

## S17 — `как выбрать пластиковые окна`

Primary state: **KEEP**

KEEP:

```text
how to choose PVC windows
how to choose correctly
apartment
private house
profile selection
glazing-unit selection
quality/recommendations
```

REVIEW:

```text
curtains/blinds
seals
screens
other accessory-selection tails
```

REJECT_OBVIOUS:

```text
lyrics/wordplay
mattress and unrelated “how to choose” associations
other non-window meanings
```

This confirms a real informational-selection job, but later Search/AI stages must decide existing-guide ownership and whether any new content is justified.

---

## S18 — `пластиковые окна от производителя`

Primary state: **KEEP**

KEEP:

```text
manufacturer/factory commercial root
Moscow
price
installation
buy/order
turnkey
REHAU + manufacturer
trust/official-site wording
```

REVIEW:

```text
manufacturer-vs-broad-commercial ownership
trust/source page vs sales landing role
```

REJECT_OBVIOUS for this Moscow mock order:

```text
Naro-Fominsk / Chekhov / Domodedovo / Lyubertsy / other Moscow-Region towns
SPb / Ekaterinburg / other cities
unrelated association noise
```

This is retained as a real trust-commercial demand family; separate landing status remains unresolved.

---

# 6. First-pass retained semantic families

After obvious-noise removal, the following families remain alive for later stages:

```text
F01 broad PVC purchase
F02 REHAU brand/profile
F03 French / panoramic / floor-to-ceiling
F04 windows by house series
F05 PVC doors
F06 balcony/loggia broad glazing
F07 balcony physical/engineering solutions
F08 balcony by house series
F09 Moscow GEO/district demand
F10 veranda/terrace/outbuilding glazing
F11 aluminium windows/glazing
F12 accessories/fittings — REVIEW commercial role
F13 installation/turnkey — bundled KEEP, standalone REVIEW
F14 repair/regulation — REVIEW commercial role
F15 price/calculation
F16 instalment/finance — REVIEW commercial role
F17 informational selection/explanation
F18 manufacturer/factory/trust-commercial
```

No family is removed solely because demand is small.

---

# 7. Obvious rejection taxonomy frozen

The first cleanup identified repeatable rejection classes:

```text
R01 wrong-region GEO outside Moscow test scope
R02 unrelated semantic meaning
R03 unrelated Wordstat association
R04 marketplace/used-goods intent incompatible with new-window business
R05 employment/job-seeker intent
R06 exact/mechanical duplicate
```

These can be applied mechanically in later workbook cleanup while retaining the raw source row/provenance.

---

# 8. Review queue frozen

The following questions must survive into later stages rather than being deleted:

```text
V01 standalone installation vs bundled installation
V02 repair/service acquisition vs aftercare
V03 accessories/fittings standalone acquisition vs upsell/support
V04 finance/instalments standalone acquisition vs conversion support
V05 Moscow GEO landing value and boundary
V06 house-series independent page value
V07 French vs panoramic vs balcony/use-case intent
V08 veranda/terrace object vs material/regime segmentation
V09 aluminium material intent vs cold-glazing object intent
V10 price page vs calculator vs broad commercial ownership
V11 manufacturer intent as landing job vs trust modifier
V12 selection guide vs commercial-page explanatory layer
V13 competitor/comparison terms as useful content vs non-target demand
V14 DIY/how-to technical terms as supporting content vs non-commercial distraction
```

---

# 9. Expansion candidate pool from pass #1

This is a candidate pool only. Step 04 does **not** execute or freeze the second Wordstat batch.

## Strong candidates

| Candidate | Reason | Evidence role |
|---|---|---|
| `оконная фурнитура` | `NEW_VOCABULARY` | literal accessory seed was only 29 while association was 1458 |
| `монтаж окон` | `NEW_VOCABULARY` | installation pass surfaced association around 5019 |
| `панорамные окна` | `NEW_VOCABULARY` + `DISTINCT_USER_JOB` | French/balcony evidence repeatedly surfaced panoramic/floor-to-ceiling language |
| `остекление террасы` | `KNOWN_SUBFAMILY_GAP` | veranda pass repeatedly surfaced terrace as a co-equal object term |
| `балкон с выносом` | `KNOWN_SUBFAMILY_GAP` | broad balcony pass surfaced extension/removal engineering language; B07 exists on site |
| `панорамное остекление балкона` | `KNOWN_SUBFAMILY_GAP` | broad balcony pass produced material panoramic demand; B07 boundary unresolved |
| `окна для частного дома` | `DISTINCT_USER_JOB` | French/selection passes surfaced private-house selection/use-case language |

## Review candidates — do not promote automatically

| Candidate | Reason | Why still REVIEW |
|---|---|---|
| `регулировка окон пвх` | `PROBLEM_SOLUTION_WORDING` | repair acquisition priority unknown |
| `москитные сетки на пластиковые окна` | `KNOWN_SUBFAMILY_GAP` | accessory standalone priority unknown |
| `окна пвх` | `NEW_VOCABULARY` | likely synonymically redundant with broad `пластиковые окна`; expansion must add information, not volume |
| `стеклопакет` | `NEW_PRODUCT_VOCABULARY` | very large association, but standalone product/business boundary not established |
| `оконный завод` | `NEW_VOCABULARY` | manufacturer/trust intent may be a modifier rather than independent acquisition job |

Pass #2 selection must use the already frozen reasons from Step 02 and respect the bounded second-pass cap; redundancy is a valid reason not to run a candidate.

---

# 10. What Step 04 explicitly did not do

```text
no new Wordstat requests
no Search requests
no GenSearch requests
no final frequency threshold
no final semantic-core freeze
no final cluster assignment
no page mapping
no cannibalization decision
no separate-page decision
no second-pass seed freeze
```

---

# 11. Step-04 completion gate

```text
all 18 pass-1 seed families reviewed = PASS
KEEP / REJECT_OBVIOUS / REVIEW semantics applied = PASS
low frequency used as sole rejection reason = false
wrong-region/noise taxonomy recorded = PASS
business-unknown families preserved as REVIEW = PASS
retained family universe frozen = PASS
review queue frozen = PASS
second-pass candidate pool produced with reasons = PASS
provider requests made in Step 04 = 0
SEARCH requests made in Step 04 = 0
GENSEARCH requests made in Step 04 = 0
final page/cluster decisions made = false
```

Markers:

```text
KW001_OKNO_MSK_STEP_04_PROGRESSIVE_CLEANUP_1_COMPLETE = true
KW001_OKNO_MSK_STEP_04_PASS2_CANDIDATE_POOL_READY = true
KW001_OKNO_MSK_FINAL_SEMANTIC_CORE_FROZEN = false
```
