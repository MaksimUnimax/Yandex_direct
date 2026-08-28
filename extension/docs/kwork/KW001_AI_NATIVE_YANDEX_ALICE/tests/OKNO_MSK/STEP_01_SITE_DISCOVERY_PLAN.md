# KW-001 / OKNO-MSK — STEP 01 SITE DISCOVERY PLAN

Date: 2026-08-28
Status: ACTIVE
Depends on: TEST_ORDER.md

## Purpose

Build a content/business inventory sufficient for semantic/page-job analysis. This is NOT a technical SEO audit and does not authorize crawler/technical promises.

## Required acquisition fields

For each representative internal page collect:

```text
url
page_title
h1
breadcrumbs / section path
page_family
primary offer or information job
visible products/services
major subtopics
primary CTA
important internal links / child families
notes
```

Do not collect technical-audit fields as part of KW-001 base work.

## Discovery sources

Preferred order:

1. Current ChatGPT public-web access for indexed public pages and search-visible structure.
2. ChatGPT Work Cloud Browser / Codex only if a representative page family, dynamic navigation or page content cannot be acquired reliably from current web access.
3. Local Codex/browser only if Work is insufficient.

The goal is to minimize operator effort while still producing a trustworthy content inventory.

## Known top-level business/page families from initial public reconnaissance

Treat these only as discovery hypotheses until representative pages are reviewed:

```text
A. Plastic / REHAU windows
B. REHAU doors
C. Balconies and loggias
D. Verandas / terrace glazing
E. Aluminium windows / glazing
F. Installation and related services
G. Prices / calculator / promotions / conversion pages
H. Company / production / trust/support pages
I. Local/geographic landing families on subdomains
```

Observed examples include nested balcony/loggia variants, exterior/interior finishing, house-series pages, 6-meter balcony pages, and cold veranda glazing.

## Representative-page strategy

KW-001 does not require reading every page before forming the business model. First acquire representative pages from each major family and enough child pages to identify repeated page jobs.

Suggested first representative set:

```text
homepage
1 general REHAU/windows family page
1 specific profile/product page
1 doors family page
1 balconies/loggias hub
2–4 materially different balcony child pages
1 veranda family/child page
1 aluminium-windows page
installation/service page
production/company page
prices/calculator page if content-readable
1–2 local/subdomain landing examples
```

Expand only when the representative set reveals a new page/job family that affects semantic architecture.

## Step-01 outputs

Produce:

```text
SITE_PAGE_INVENTORY.md
BUSINESS_AND_PAGE_MODEL.md
OPEN_QUESTIONS_FOR_CLIENT.md
```

The inventory must distinguish:

```text
commercial landing
category/hub
product/profile page
service page
informational/support page
local/geographic landing
mixed/hybrid page
unknown/review
```

## Exit gate

Step 01 passes when ChatGPT can state, with page examples:

```text
what the business sells
which commercial families exist
which page-job families already exist
where obvious page-family overlap may need later evidence
what important business ambiguity still requires client clarification
which 10–15 primary directions should enter the base-package semantic test
```

No Wordstat/Search/GenSearch provider acquisition before this gate is recorded.
