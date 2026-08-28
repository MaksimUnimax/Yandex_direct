# KW-001 / OKNO-MSK — STEP 01 MULTI-PASS DISCOVERY CROSS-CHECK

Date: 2026-08-28
Status: TEST-DERIVED METHOD EVIDENCE
Site: https://okno-msk.ru/

## 1. Purpose

Compare three independent public-site discovery passes before semantic/provider work:

```text
PASS A = ChatGPT public-web pass
PASS B = Codex in ChatGPT Work
PASS C = Codex desktop/app pass supplied by owner
```

The goal is not to choose a winner. The goal is to determine whether different discovery surfaces expose materially different page families or evidence quality and therefore whether KW-001 Step 1 needs a stronger acquisition contract.

No Wordstat, ordinary Yandex Search API, Search batch or GenSearch evidence is used in this comparison.

---

## 2. Coverage summary

### PASS A — ChatGPT public web

Observed in the accepted Step-01 inventory:

```text
representative pages actually reviewed = 18
major business families = covered
commercial hubs = covered
product subtype = covered
service = covered
information guide = covered
trust/company = covered
conversion utility = covered
GEO district page = observed/read
GEO city subdomain = observed/read
```

Distinctive finds included:

```text
/balkony-i-lodzhii/rajony/osteklenie-balkonov-v-mitino/
https://balashiha.okno-msk.ru/
/balkony-i-lodzhii/osteklenie-lodzhii-vtorym-konturom/
.../ceriya-doma-p-46/
/uslugi/ustanovka-okon/
/o-kompanii/proizvodstvo/
/calculator/
/stati/kak-vybrat-plastikovye-okna/
```

Strength: independent search-visible discovery found GEO/subdomain and selected weakly exposed/specialized pages.

Weakness: smaller actually-read set; fewer repeated-template representatives than the Work pass.

### PASS B — Codex Work

Reported:

```text
pages_opened_total = 56
unique_page_families = 12
footer_checked = true
internal_link_expansion_performed = true
DISCOVERY_SATURATION_REACHED = true
```

It directly reviewed a much deeper set of:

```text
REHAU profile models
house-series pages
doors subtypes
balcony geometry/construction pages
warm/cold veranda pages
aluminium opening types
service/warranty/repair/finance pages
accessories/customisation
article hub + multiple articles
trust/contact pages
```

Strength: by far the strongest deep representative reading of internal page families and repeated templates.

Important limitation recorded by that pass:

```text
Work Cloud Browser itself did not expose a usable live DOM and timed out;
subsequent inventory used a read-only first-party page-view surface.
```

Most important miss:

```text
no GEO landing family or public subdomain was found through checked internal navigation
```

That conflicts with PASS A factual discovery of both a district landing and a Balashikha subdomain. Therefore `internal-navigation saturation` was not equal to `public-site universe saturation`.

### PASS C — Codex desktop/app

Reported:

```text
pages_opened_total = 5
unique_page_families = 16 observed/inferred
footer_checked = true
internal_link_expansion_performed = true
DISCOVERY_SATURATION_REACHED = false
```

Only these five URLs were actually opened/read:

```text
/
/okna-rehau/
/dveri-rehau/
/balkony-i-lodzhii/
/verandy/
```

The pass nevertheless extracted a useful navigation taxonomy including:

```text
REHAU profiles
number-of-sashes axis
object/room axis
house-series axis
balcony glazing modes
balcony geometry
balcony finishing
accessories
services
prices/utilities
trust/company
articles/actions/news
```

Strength: header/footer/catalog link discovery exposed important segmentation axes quickly, especially `number of sashes` and the explicit navigation-level taxonomy.

Weakness: browser timeouts prevented validation of most child pages. Therefore child-page statements from this pass are `DISCOVERED_LINK/INFERRED_FAMILY`, not equivalent to `OPENED_AND_READ` evidence.

It correctly refused to claim saturation.

---

## 3. Agreement across all passes

All three independently support the same high-level business model:

```text
PVC / REHAU windows
PVC doors
balcony/loggia glazing
veranda/gazebo/terrace glazing
aluminium glazing
measurement/calculation/order conversion
supporting service/trust/information layers
```

All three also independently show that the site segments demand on multiple orthogonal axes rather than one simple product hierarchy.

This agreement increases confidence that the basic business/page-family model is not an artifact of one acquisition surface.

---

## 4. Material differences for KW-001

### D1 — GEO architecture was missed by both Codex reports but found by ChatGPT web

PASS A directly observed:

```text
main-domain district landing
+ city subdomain landing
```

PASS B explicitly reported no geo/subdomain family through internal navigation.
PASS C reported no subdomain and did not reach geo pages.

Decision:

```text
INTERNAL_NAVIGATION_ONLY_DISCOVERY = INSUFFICIENT FOR COMPLEX EXISTING SITES
```

A site can contain commercially material public page families that are weakly linked, absent from checked navigation, or exposed mainly through search-visible URLs.

### D2 — Work produced the deepest validated internal-family inventory

PASS B opened 56 pages and validated many family representatives that PASS A sampled only lightly and PASS C merely inferred from navigation.

Decision:

For large repeated families, a systematic browser/page-reader pass materially improves confidence about:

```text
actual page job
template differences
CTA/content differences
whether a family is real vs navigation-label inference
```

### D3 — Desktop/app pass exposed navigation axes despite low page-read coverage

PASS C highlighted `number of sashes` and explicit object/type subdivisions early, even though it could not open their children reliably.

Decision:

Navigation taxonomy itself is useful evidence for seed planning, but must carry a lower evidence status until representative child URLs are read.

### D4 — `found URL` and `read URL` must be separate evidence states

The passes demonstrate four distinct states:

```text
OPENED_READ
DISCOVERED_LINK_ONLY
INFERRED_TEMPLATE_FAMILY
UNVERIFIED_OR_INACCESSIBLE
```

Treating them as one state creates false confidence.

### D5 — Saturation needs a cross-channel definition

PASS B could honestly reach saturation within its navigation/page-view surface while still missing a real GEO/subdomain family found by PASS A.

Decision:

`DISCOVERY_SATURATION_REACHED` may only be claimed for KW-001 after the required discovery channels are cross-checked, not merely after one crawler/browser stops finding new internal families.

---

## 5. New Step-01 discovery contract derived from this test

For an existing site with non-trivial architecture, KW-001 should use at least two complementary public discovery paths:

### CHANNEL A — internal architecture discovery

Use navigation, footer, breadcrumbs, internal links and systematic representative page reading to discover:

```text
catalog taxonomy
repeated families
page templates
page jobs
service/trust/content branches
```

### CHANNEL B — independent public URL discovery

Use independent public/search-visible discovery to look specifically for:

```text
GEO pages
subdomains
weakly linked landing pages
specialized use-case pages
public families not exposed in the sampled menu/footer tree
```

Sitemap may be used only as a public URL-discovery aid when the order scope allows it; it is not a technical SEO audit finding.

### Optional CHANNEL C — alternate browser/runtime

Use an alternate Work/local browser only when A or B cannot reliably read representative pages. It is a recovery/coverage tool, not automatically a superior authority.

### Evidence status required per URL/family

Every discovered item should be tagged:

```text
OPENED_READ
DISCOVERED_LINK_ONLY
INFERRED_TEMPLATE_FAMILY
UNVERIFIED_OR_INACCESSIBLE
```

### New saturation condition

KW-001 may mark site discovery saturated only when:

```text
CHANNEL A no longer reveals new material family/axis/job
AND
CHANNEL B no longer reveals new material family/axis/job
AND
representative pages of every material family are OPENED_READ where technically possible
AND
remaining unresolved/inaccessible families are explicitly listed
```

For a very small/simple site, one channel may be enough only if it demonstrably exposes the complete public structure; this must be recorded rather than assumed.

---

## 6. Merged OKNO-MSK factual model additions

Compared with the original 18-page ChatGPT inventory, the multi-pass merge strengthens Step 01 with additional explicit axes/families:

```text
REHAU windows by number of sashes
REHAU windows by object/room
multiple REHAU profile-template representatives
broader house-series family
multiple balcony geometry/construction templates
balcony finishing as its own service/use-case branch
accessory/customisation family
repair/warranty/finance service branches
article hub + repeated editorial family
price/finance/conversion branches
```

The original PASS A contributions that must be retained because the Codex passes missed them include:

```text
main-domain district GEO family
city subdomain GEO model
second-contour balcony solution
standalone installation page
production/trust hybrid
```

No semantic merge/delete/new-page decision follows from this inventory alone.

---

## 7. Step-01 productization verdict

```text
THREE_PASS_HIGH_LEVEL_BUSINESS_AGREEMENT = PASS
WORK_DEEP_INTERNAL_FAMILY_COVERAGE = STRONGEST
CHATGPT_SEARCH_VISIBLE_GEO_DISCOVERY = MATERIAL_UNIQUE_VALUE
DESKTOP_NAVIGATION_TAXONOMY = USEFUL_BUT_PARTIALLY_UNVERIFIED
SINGLE_SURFACE_DISCOVERY = REJECTED_AS_DEFAULT
READ_VS_DISCOVERED_EVIDENCE_STATUS = REQUIRED
CROSS_CHANNEL_SATURATION = REQUIRED
```

The important product lesson is not that every future order needs three agents. It is that the KW-001 method must combine complementary discovery channels and preserve evidence quality. A deeper reader and an independent public-URL discovery path are more valuable than repeatedly running the same navigation crawl.

No provider work should begin until the merged Step-01 model and seed scope are frozen.
