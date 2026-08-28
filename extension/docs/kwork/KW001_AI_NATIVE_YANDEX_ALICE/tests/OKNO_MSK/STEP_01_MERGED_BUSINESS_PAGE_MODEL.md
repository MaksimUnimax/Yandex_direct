# KW-001 / OKNO-MSK — STEP 01 MERGED BUSINESS + PAGE-JOB MODEL

Date: 2026-08-28  
Status: **MERGED STEP-01 ANALYST MODEL / PRE-PROVIDER FREEZE CANDIDATE**

Depends on:

```text
TEST_ORDER.md
STEP_01_MERGED_SITE_INVENTORY.md
OPEN_QUESTIONS_FOR_CLIENT.md
STEP_01_MULTI_PASS_DISCOVERY_CROSSCHECK.md
```

## 1. Business model established from merged public evidence

The public site represents a glazing/window business with a purchase flow spanning product selection, measurement, price calculation, production/fulfilment, installation and aftercare.

Observed conversion model:

```text
search / direct visit / article / local landing
→ product, use-case or information page
→ compare / understand suitability / estimate price
→ calculator / call / callback / free measurement
→ quote / contract
→ production / delivery / installation
→ warranty / service / repair
```

This is broader than a simple `PVC windows` catalogue. The semantic model must therefore distinguish product selection, use-case choice, technical explanation, local purchase, service and trust jobs.

---

## 2. Merged business/search-job families

### B01 — broad PVC-window purchase

Observed assets:

```text
homepage broad commercial landing
REHAU category hub
price/calculator support
```

Jobs to test:

```text
buy plastic windows
plastic windows Moscow
windows with installation
windows from manufacturer
price / calculate windows
```

Open question: whether generic PVC purchase, branded REHAU purchase and manufacturer intent belong to one or several primary page jobs.

### B02 — REHAU brand/profile selection

Observed assets:

```text
REHAU hub
multiple specific profile pages
comparison/FAQ content
selection article support
```

Jobs to test:

```text
buy REHAU windows
choose REHAU profile
compare profile systems
specific profile purchase
heat/noise/budget/light selection
```

This family is explanation-heavy and is a likely later AI-evidence candidate, but AI is not selected until Search-only mapping is frozen.

### B03 — window configuration / application / design

Observed axes:

```text
opening/configuration
object/office type
French/floor-to-ceiling
stained-glass/decorative
coloured/design
```

Jobs to test: choose a finished construction by application/design rather than profile name.

### B04 — windows by house series

Observed hub plus multiple series pages.

Job to test:

```text
known building series → expected configuration/size/price starting point
```

Do not assume every series page deserves independent demand; use representative Wordstat/SERP evidence to validate the family and then avoid exploding the base package into every series.

### B05 — PVC/REHAU doors

Observed:

```text
doors hub
balcony doors
sliding doors
entrance doors
```

Jobs to test: buy/choose door by function, opening and thermal/security need.

### B06 — balcony/loggia broad glazing

Observed broad hub with warm/cold, finishing, price and multiple solution paths.

Jobs:

```text
glaze balcony/loggia
choose warm vs cold
estimate cost
make balcony usable
```

### B07 — balcony physical/engineering solutions

Observed:

```text
panoramic
opening mode
semicircular/geometry
roof
extension
second contour
```

Job: solve a physical/engineering constraint or visual/use-case requirement.

Need later evidence to determine which are independent search jobs vs supporting variants.

### B08 — balcony by house series

Observed at least one direct series-specific balcony landing.

Job: known house series + balcony/loggia glazing.

This is separate from the window-house-series family in content structure and must be tested separately before any consolidation recommendation.

### B09 — local/GEO purchase

Observed two public models:

```text
main-domain district landing
city subdomain landing
```

Jobs to test:

```text
windows/glazing in a Moscow district
windows in a Moscow-region city
```

The base test will validate the GEO model with a bounded representative set, not crawl/cluster every locality.

### B10 — veranda / terrace / gazebo / outbuilding glazing

Observed broad hub plus warm/cold and specific outbuilding pages.

Jobs:

```text
glaze veranda/terrace/gazebo
choose warm vs cold
choose year-round vs seasonal use
choose material
```

This family likely carries stronger explanation/suitability questions than generic purchase roots.

### B11 — aluminium / cold glazing

Observed material hub plus hinged/sliding subtypes.

Jobs:

```text
buy aluminium windows/glazing
choose Provedal/material system
choose sliding vs hinged
solve lightweight/cold glazing need
```

Open boundary: material-led aluminium intent vs object-led cold balcony/veranda intent.

### B12 — accessories / safety / customisation

Observed substantial pages for screens, blinds, hardware/security, lamination, handles and decorative options; glass-option family also surfaced.

Jobs:

```text
add insect protection
improve child/burglary safety
customise colour/design
choose glass/accessory option
```

Commercial-scope question: whether these are meaningful standalone acquisition directions or mainly supporting/upsell content.

### B13 — installation / finishing / aftercare

Observed distinct assets:

```text
installation
slopes finishing
warranty/service
extended warranty
repair
```

Jobs differ materially:

```text
order installation
understand installation quality/process
finish opening/slopes
obtain warranty support
repair existing windows
```

Standalone commercial relevance remains a client/evidence question.

### B14 — finance / price / calculation

Observed:

```text
credit/instalments
price page
multiple calculator routes
```

Jobs:

```text
understand budget
calculate preliminary price
compare configurations
pay by instalments
```

These are conversion/decision-support jobs and may map to utilities rather than normal commercial category pages.

### B15 — informational selection / explanation

Observed article hub plus multiple guides.

Jobs include:

```text
how to choose windows
understand glazing types
understand panoramic glazing
choose coloured windows
understand glass units
plan balcony finishing
understand micro-ventilation
```

Critical rule for later AI analysis: before recommending a new explanatory asset, first test whether an existing article/commercial page already serves the observed job.

### B16 — trust / manufacturer/source-worthiness

Observed:

```text
company
production
reviews
contacts
warranty/process evidence
```

Jobs:

```text
verify supplier
verify manufacturer/production claim
assess trust, process and guarantees
```

These may support both conversion and source-worthiness but are not automatically primary landing pages for commercial roots.

---

## 3. Page-job taxonomy frozen after merged discovery

```text
BROAD_COMMERCIAL
CATEGORY_HUB
PRODUCT_PROFILE
USE_CASE_SOLUTION
HOUSE_SERIES_SOLUTION
LOCAL_GEO
SERVICE
AFTERCARE_REPAIR
ACCESSORY_CUSTOMISATION
INFORMATION_GUIDE
TRUST_SOURCE
CONVERSION_UTILITY
HYBRID_CONTENT_COMMERCE
```

No SEO correctness is implied by the site's current use of these jobs. They are factual/analytical classes for later mapping.

---

## 4. Boundary queue for Wordstat + Search stages

Priority boundary questions:

### Q01 — broad PVC vs REHAU branded hub

Need to separate generic purchase, brand purchase, price and manufacturer intents.

### Q02 — REHAU category/comparison vs specific profile vs selection guide

Need to determine where commercial selection ends and explanatory/brand-model jobs become distinct.

### Q03 — window design/use-case pages

Need evidence for French/panoramic/coloured/stained-glass/object-specific boundaries.

### Q04 — house-series windows

Need representative demand + SERP evidence before treating the repeated family as broadly justified.

### Q05 — doors hub vs individual door types

Need to validate balcony/sliding/entrance page ownership.

### Q06 — balcony broad vs thermal/engineering/geometry branches

Highest-complexity boundary family; likely requires multiple representative Search clusters.

### Q07 — balcony house-series vs generic balcony/geometry pages

Need to know whether series is an independent entry job or merely a variant of generic glazing.

### Q08 — GEO district vs city/subdomain strategy

Need bounded representative demand/SERP evidence, not a full locality audit.

### Q09 — veranda object type vs warm/cold regime

Need to test whether users and Yandex primarily segment by object (`veranda/terrace/gazebo`) or use scenario (`warm/cold/year-round`).

### Q10 — aluminium material vs cold-glazing use case

Need to avoid mapping material and object intents mechanically to the same page.

### Q11 — accessory/security/customisation standalone demand

Need to determine which accessory families deserve independent acquisition pages vs supporting roles.

### Q12 — installation/repair/warranty

Need to separate acquisition service from aftercare/support jobs.

### Q13 — price/calculator/finance ownership

Need to determine whether query jobs map to price pages, calculator utilities or broad commercial pages.

### Q14 — commercial selection content vs article layer

Need Search evidence first, then selective AI evidence where explanation/source-worthiness can change/de-risk architecture.

### Q15 — manufacturer/trust intent

Need to test whether `from manufacturer/factory/production` is an independent search landing job or a trust attribute of broad commercial pages.

---

## 5. What changed relative to the first 18-page model

The first model correctly identified the main commercial families, GEO existence, special balcony solutions, installation, production and informational content.

The merged model materially expands/strengthens:

```text
profile-model depth
window design/use-case axis
window-house-series family
door subtype depth
balcony geometry/engineering family
accessory/customisation/security family
repair/warranty/aftercare family
finance/instalment job
larger editorial family
price/calculator distinction
```

Therefore the original fixed 15-direction seed list must not be used unchanged. Step 02 must be rebuilt from this merged family model while keeping provider acquisition bounded.

---

## 6. Mock-client assumptions retained

From the frozen test order/open questions:

```text
primary_region = Moscow
B2C residential = primary focus
all visible product families = provisionally active
standalone installation strategic priority = UNKNOWN
GEO architecture = existing and open to evidence-led recommendation
new pages allowed when justified
merge/reassignment recommendations allowed when justified
Webmaster/Metrika/Direct unavailable for base rehearsal
```

No public discovery result may silently change these assumptions. A change later is a mock client revision.

---

## 7. Step-01 analyst freeze

```text
MERGED_BUSINESS_MODEL_READY = true
MERGED_PAGE_JOB_TAXONOMY_READY = true
BOUNDARY_QUEUE_READY = true
OLD_15_DIRECTION_PLAN_REQUIRES_REBUILD = true
WORDSTAT_REQUESTS = 0
SEARCH_REQUESTS = 0
GENSEARCH_REQUESTS = 0
```

Next action: create/freeze `STEP_02_SEED_QUERY_PLAN.md` from the merged model before any Wordstat request.
