# KW-001 / OKNO-MSK — BUSINESS AND PAGE MODEL

Date: 2026-08-28
Status: STEP 01 ANALYST MODEL
Depends on: TEST_ORDER.md, SITE_PAGE_INVENTORY.md

## 1. Business model understood from public site

The business is not merely a seller of standard PVC windows. The public offer is a vertically integrated glazing/installation business with its own-production positioning and multiple product/service families.

Core commercial model observed:

```text
traffic / inquiry
→ product or glazing need
→ configuration / consultation / calculator
→ free measurement
→ quote / contract
→ manufacture
→ delivery
→ installation
→ warranty/service
```

Primary conversion actions across the site are:

```text
calculate price
request free measurement
request callback / submit contact
order window/door/glazing/installation
```

The site states that the company manufactures and installs plastic and aluminium window systems, presents itself as an official REHAU partner, and exposes own-production/trust evidence.

## 2. Commercial families

### C1 — Plastic / REHAU windows

Observed hierarchy:

```text
broad plastic windows in Moscow
→ REHAU family
→ profile systems (Blitz, Thermo, Grazio, Delight, Intelio, etc.)
→ object/use-case variants (apartment, house, office, panoramic, coloured, etc.)
→ accessories / glazing / configuration choices
```

Primary user jobs likely include:

```text
buy windows
compare profiles
choose profile for heat/noise/light/budget
estimate price
understand configuration
find manufacturer/installer
```

### C2 — REHAU / PVC doors

Observed hierarchy:

```text
doors hub
→ balcony doors
→ sliding doors
→ entrance doors
→ configurations / glazing / thresholds / fittings
```

Primary jobs:

```text
buy door
choose door type
configure safety / insulation / glazing
estimate price
```

### C3 — Balconies and loggias

This is the most internally segmented commercial family.

Observed segmentation dimensions include:

```text
warm vs cold glazing
shape / geometry
house series
district / locality
special technology (e.g. second contour, removal, panoramic, roof)
finishing / improvement
material/profile
```

Primary jobs likely include:

```text
choose warm/cold solution
choose configuration by balcony geometry
solve a building-specific constraint
solve a location-specific purchase need
turn balcony into usable space
combine glazing + finishing
estimate project cost
```

This family should receive the strongest later page-boundary testing because many different axes can produce superficially similar commercial pages.

### C4 — Verandas / terraces / gazebos

Observed hub combines several structures and then splits at least by warm/cold glazing.

Primary jobs:

```text
glaze seasonal vs year-round space
choose PVC vs aluminium
choose warm vs cold solution
understand suitability / condensation / heat / protection trade-offs
estimate cost
```

This is a strong candidate for AI evidence because the purchase decision is explanation-heavy.

### C5 — Aluminium windows / cold glazing

Observed product-material family:

```text
aluminium windows
→ Provedal profiles
→ sliding / casement
→ applications: balcony, veranda, gazebo, large/light structures
```

Primary jobs:

```text
choose aluminium instead of PVC
understand cold glazing limits
choose opening/profile
buy lightweight / lower-cost glazing
```

This creates a semantic architecture question: should the user arrive through a material page (`алюминиевые окна`) or an object/use-case page (`холодное остекление балкона/веранды`), and which jobs deserve separate assets.

### C6 — Installation / service

The installation page has independent commercial language and price information, not only support text.

Potential jobs:

```text
order installation separately
understand installation process / ГОСТ / scope
compare installation quality/price
prepare for installation
```

Whether standalone installation is strategically important cannot be inferred solely from the public page and is a client question.

## 3. Supporting asset families

### S1 — Selection / educational content

The site already contains substantive informational pages such as `Как выбрать пластиковые окна`, plus comparisons and FAQs embedded into commercial pages.

Therefore the AI-native service should not default to the generic recommendation `add FAQ / write article`.

Instead we must determine:

```text
which explanatory jobs already have an owned asset
whether the asset is the right page type for the observed Search/AI job
whether commercial pages duplicate or complement that information
whether AI source-worthiness requires strengthening existing assets rather than creating new URLs
```

### S2 — Trust / authority / source-worthiness

Observed assets:

```text
company page
production page
certification/partner claims
warranty/service
work examples/reviews
process from consultation to installation
```

These are potentially important for AI source-worthiness and commercial trust, but they are not assumed to be search landing pages for broad commercial roots.

### S3 — Conversion utilities

The calculator is an independent page/job:

```text
user wants to estimate / compare price before measurement
```

It also exposes product configuration logic (profile, glazing, dimensions, opening type), which can inform semantic expansion but should not be confused with organic Search demand evidence.

### S4 — Geographic landings

Two geographic architectures are visible:

```text
main-domain district URLs (e.g. balcony glazing in Mitino)
city subdomains (e.g. Balashikha)
```

We cannot judge whether these should be consolidated, expanded or left alone until demand/SERP evidence is acquired.

## 4. Existing page-job types

The site already supports most of the page-job classes that KW-001 may recommend:

```text
BROAD_COMMERCIAL
CATEGORY_HUB
PRODUCT_PROFILE
USE_CASE_SOLUTION
SERVICE
LOCAL_GEO
SELECTION_GUIDE
TRUST_SOURCE
CONVERSION_UTILITY
HYBRID_CONTENT_COMMERCE
```

This makes the site a useful test because KW-001 must improve/reassign an already complex architecture rather than merely invent missing page types.

## 5. Main semantic/page-boundary questions for later evidence

These are the questions Step 02+ should answer. They are not conclusions yet.

### Q1 — Who owns the broad `пластиковые окна` job?

Potential conflict:

```text
homepage
vs
/okna-rehau/
```

Need Wordstat + ordinary SERP evidence to separate generic PVC purchase, REHAU-brand purchase and manufacturer intent.

### Q2 — Profile product page vs comparison/selection page

Potential split:

```text
REHAU category comparison
specific profile page (Thermo etc.)
how-to-choose informational article
```

Need Search and selective AI evidence around `какие окна выбрать`, `какой профиль rehau выбрать`, `rehau thermo vs ...`, noise/heat/budget questions.

### Q3 — Balcony segmentation

Need to determine which axes represent real independent user jobs:

```text
warm/cold
type/shape
house series
district
special glazing technology
finishing
```

Do not assume every existing URL is justified or unjustified.

### Q4 — Aluminium vs cold-glazing use case

Potential architecture overlap:

```text
/alyuminievye-okna/
vs
cold veranda pages
vs
cold balcony pages
```

Need to know whether users search by material, by object or by desired temperature/use scenario.

### Q5 — Veranda vs terrace vs gazebo

The hub combines these entities while children split warm/cold. Need demand/SERP evidence on whether object type is more important than glazing mode.

### Q6 — Manufacturer intent

Own-production messaging is present on broad pages and a dedicated production page. Need to check whether `окна от производителя`, `завод пластиковых окон`, etc. form distinct search/page jobs.

### Q7 — Geographic strategy

Need evidence for:

```text
Moscow broad landing
Moscow district pages
Moscow-region city subdomains
```

Base KW-001 test should not attempt to optimize every locality; it should inspect geography as one architecture family and keep the test bounded.

## 6. Primary directions selected for base-package semantic test

The Step-01 exit gate requires a bounded 10–15 direction set. Proposed set for Step 02:

```text
D01 plastic windows / windows in Moscow
D02 REHAU windows / profile-family selection
D03 REHAU Thermo / profile-specific purchase-selection
D04 PVC / REHAU doors
D05 balcony doors
D06 balcony & loggia glazing broad
D07 warm balcony glazing
D08 cold balcony glazing / aluminium use
D09 special balcony glazing (second contour as representative special solution)
D10 house-series balcony glazing (P-46 as representative)
D11 veranda / terrace / gazebo glazing broad
D12 warm vs cold veranda glazing
D13 aluminium windows / Provedal material-led demand
D14 window installation service
D15 how to choose windows / profile-selection informational job
```

Geographic landings remain a cross-cutting evidence dimension rather than consuming a separate full semantic direction in the first base-package run. We will still use them when Search results show locality-specific page jobs.

## 7. What Step 01 does NOT conclude

No conclusion has yet been made about:

```text
keyword frequency
which URL should rank for which query
cannibalization
which pages should be deleted/merged/created
competitor strength
SERP similarity
AI answer orientation
AI source inclusion
commercial priority
```

Those require the next evidence layers.

## 8. Step-01 analyst conclusion

The site is suitable for KW-001 Test A because it contains:

```text
mature commercial architecture
multiple related product families
high-overlap semantic boundaries
selection-heavy products
existing informational/source assets
multiple geographic models
clear conversion actions
```

The strongest expected value of the AI-native layer is not `creating AI pages`. It is testing whether selection/explanation/source-worthiness jobs require different page scope or priority than ordinary commercial Search suggests.
