# blood_sand — clean Pass A ordinary-search baseline

Date: 2026-08-27

```text
PASS_A_CONTEXT = CLEAN_SEALED_PACKET_ONLY
sealed_packet_path = extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_SEALED_BASELINE_PACKET_2026-08-27.md
frozen_source_commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
extra_source_opened = false
fresh_provider_requests = 0
```

## Read inventory

```text
extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_CLEAN_CHAT_HANDOFF_2026-08-27.md
extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_SEALED_BASELINE_PACKET_2026-08-27.md
```

No other repository file, repository search, external web source, prior-conversation evidence, personal context, or fresh provider response was used.

## Baseline method

This Pass A uses only measured Wordstat demand and ordinary Yandex Search composition frozen in the sealed packet. Decisions are based on three factors together: measured demand precision, observed ordinary-Search intent/composition, and direct fit to the stated assortment of symbolic pendants/amulets including an automotive use case.

Priority scale:

- `P0` — architecture-defining target that should anchor the first semantic/page structure.
- `P1` — strong supporting target with clear demand/intent and credible independent-site fit.
- `P2` — valid but conditional target; evidence or assortment depth is insufficient for an unconditional standalone page.
- `P3` — weak/low-volume target or a term best absorbed into a stronger page.

`REJECT` below means reject as a standalone SEO page target in this baseline. It does not forbid natural use of the phrase on a relevant stronger page.

## Decision register

### A01

```text
unit_id = A01
root_or_cluster = славянские обереги
baseline_evidence = broad 25,737; quoted 2,987; ordinary Search is commercial/category-first; marketplaces are #1/#3 but specialist independent sites occupy most of Top-10 and one specialist domain ranks multiple URLs.
intent = broad commercial category with informational support
 decision = KEEP
priority = P0
page_job = specialist commercial category / hub for Slavic amulets, with navigation into named symbol families and supporting meaning content
split_merge = keep as umbrella category; do not split solely by broad demand; child symbol pages require their own evidence and assortment fit
confidence = high
missing_evidence = exact current assortment breadth by Slavic family; conversion data; page-level competition strength beyond observed Top-10
contamination_or_fit_notes = broad but highly relevant to stated assortment; specialist-independent visibility is unusually strong, so this is a primary independent-site opportunity rather than a marketplace-only battle
```

### A02

```text
unit_id = A02
root_or_cluster = печать велеса
baseline_evidence = broad 3,330; quoted 802; 8/10 primary results are marketplaces/trading platforms, but a specialist independent page ranks #2; one editorial meaning result ranks #7.
intent = product/transactional symbol-family intent
 decision = KEEP
priority = P0
page_job = commercial symbol/product-family landing for Печать Велеса
split_merge = keep primary commercial root on its own commercial job; split explicit meaning intent to A03
confidence = high
missing_evidence = assortment depth inside the Печать Велеса family; whether one canonical product or several variants should be indexed separately
contamination_or_fit_notes = strong direct fit and meaningful phrase demand; marketplace pressure is high, but specialist #2 proves an independent specialist page can compete
```

### A03

```text
unit_id = A03
root_or_cluster = печать велеса значение
baseline_evidence = ordinary Search is meaning-first/hybrid; rank #1 is a specialist meaning page, #2 an editorial meaning article, with multiple specialist product pages ranking through explicit meaning sections; materially different from marketplace-heavy primary печать велеса SERP.
intent = informational meaning / interpretation
 decision = KEEP
priority = P0
page_job = dedicated meaning/guide page supporting the commercial Печать Велеса page
split_merge = SPLIT from A02 because observed Search composition and user job are materially different; cross-link both directions
confidence = high
missing_evidence = direct Wordstat volume for the exact meaning phrase was not supplied
contamination_or_fit_notes = explicit meaning modifier removes the main transactional ambiguity; separate intent is supported by ordinary Search, not inferred from wording alone
```

### A04

```text
unit_id = A04
root_or_cluster = оберег велес
baseline_evidence = broad 1,507; commercial-first Search with stronger niche-independent representation than печать велеса; informational and hybrid meaning/product results are also visible.
intent = commercial Veles-family intent broader than the exact Печать Велеса product name
 decision = INVESTIGATE
priority = P1
page_job = candidate Veles-family commercial category, or secondary semantic cluster on A02 if the real assortment does not contain multiple materially distinct Veles products
split_merge = do not automatically merge with печать велеса; decide from assortment breadth because the observed root is broader, while Search supports specialist commerce
confidence = medium-high
missing_evidence = exact Veles-family assortment and whether users encounter multiple distinct Veles symbols/products on the site
contamination_or_fit_notes = good specialist-site opportunity, but the packet does not establish enough assortment structure to justify a separate Veles category over a strong Печать Велеса family page
```

### A05

```text
unit_id = A05
root_or_cluster = алатырь оберег
baseline_evidence = broad 1,878; commercial-first Search with visible meaning/support layer; a specialist independent site appears in Top-5; marketplace #1 contained a project-brand Alatyr car-amulet product with 593 ratings at capture.
intent = commercial symbol-family intent with secondary meaning demand
 decision = KEEP
priority = P1
page_job = commercial Alatyr symbol/product-family page; include concise meaning support and consider a separate guide only after exact meaning demand is measured
split_merge = standalone symbol family; do not create a separate meaning page from current evidence alone
confidence = high for commercial page, medium for separate support page
missing_evidence = exact meaning-query demand/SERP; current independent-site assortment depth for Alatyr
contamination_or_fit_notes = direct product fit is strong and ordinary Search admits specialist independents; marketplace brand visibility is evidence of product-market fit, not independent-site ranking
```

### A06

```text
unit_id = A06
root_or_cluster = оберег чур / сварог оберег
baseline_evidence = measured broad demand 903 and 761 respectively; no ordinary-Search composition for these exact roots is included in the sealed packet.
intent = likely named-symbol commercial/informational mix, unresolved by allowed evidence
 decision = INVESTIGATE
priority = P2
page_job = candidate symbol-family commercial pages only if assortment depth and ordinary Search confirm a commercial page job
split_merge = keep as candidate child families under A01; no forced standalone split yet
confidence = medium-low
missing_evidence = exact SERPs, phrase precision, assortment depth, direct business fit by symbol
contamination_or_fit_notes = demand is large enough to investigate, but Pass A must not infer page type from volume alone
```

### A07

```text
unit_id = A07
root_or_cluster = Перун / Звезда Лады / Триглав / Молвинец / Мара / Громовик
baseline_evidence = measured broad demand ranges from 130 down to 43; no exact ordinary-Search composition is included for these roots.
intent = named-symbol demand, unresolved page job
 decision = INVESTIGATE
priority = P2-P3
page_job = absorb initially into the Slavic hub and relevant product inventory; promote to dedicated family pages only when assortment and Search intent justify them
split_merge = MERGE into A01 architecture by default; split only with additional evidence
confidence = medium
missing_evidence = exact SERPs, quoted demand, assortment breadth, conversion/business value
contamination_or_fit_notes = low-to-moderate measured demand does not justify page proliferation by itself
```

### A08

```text
unit_id = A08
root_or_cluster = вегвизир
baseline_evidence = broad 5,938; quoted 1,541; Top-10 is 7 commercial/platform + 3 informational/reference; commercial demand is strong even without a purchase modifier.
intent = mixed entity + commerce
 decision = KEEP
priority = P0
page_job = specialist commercial Vegvisir symbol/product-family landing with concise entity context
split_merge = keep commercial/entity root as a standalone family job; split explicit meaning intent to A09
confidence = high
missing_evidence = actual Vegvisir assortment depth and conversion data
contamination_or_fit_notes = large precise demand and mixed commerce make this a strong family opportunity; falling year-over-year dynamics reduce urgency slightly but do not invalidate the target
```

### A09

```text
unit_id = A09
root_or_cluster = вегвизир значение
baseline_evidence = ordinary Search is overwhelmingly definition/history/meaning material; rank #1 is a specialist editorial page; this is sharply different from mixed-commercial вегвизир.
intent = clean informational definition/history/meaning
 decision = KEEP
priority = P1
page_job = dedicated meaning/history guide supporting A08
split_merge = SPLIT from A08; cross-link to commercial family page rather than forcing one hybrid page to satisfy two clearly different SERPs
confidence = high
missing_evidence = exact demand volume for the meaning variant
contamination_or_fit_notes = separate page job is justified by Search composition even without supplied Wordstat volume
```

### A10

```text
unit_id = A10
root_or_cluster = шлем ужаса оберег
baseline_evidence = broad 474; Search is commerce-heavy with Wildberries #1, Ozon #2, specialist content/commerce #3, plus Market/Livemaster and supporting history/meaning material.
intent = commercial-first named-symbol intent with secondary informational layer
 decision = KEEP
priority = P1
page_job = commercial symbol-family page with meaningful history/meaning support inside the page
split_merge = standalone family if stocked; do not split a separate meaning page yet because the supplied evidence shows a secondary, not dominant, meaning layer
confidence = high
missing_evidence = assortment availability/depth and explicit meaning-query SERP/demand
contamination_or_fit_notes = specialist content/commerce ranking #3 indicates a realistic independent-site route despite marketplace pressure
```

### A11

```text
unit_id = A11
root_or_cluster = валькнут амулет / гунгнир амулет
baseline_evidence = broad demand 70 and 17; no ordinary-Search composition supplied.
intent = low-volume named-symbol commercial intent, unresolved
 decision = INVESTIGATE
priority = P3
page_job = product-level or family content only if the assortment contains exact products; otherwise absorb into a Norse/symbol hub
split_merge = no standalone SEO family page by default
confidence = medium
missing_evidence = SERPs, quoted demand, product availability, margin/business value
contamination_or_fit_notes = exact demand is too small to justify standalone architecture without stronger assortment or conversion evidence
```

### A12

```text
unit_id = A12
root_or_cluster = оберег в машину / амулет в машину / талисман в машину
baseline_evidence = оберег в машину 1,405 broad / 96 quoted; амулет в машину 404; талисман в машину 177; оберег в машину Search is mixed commercial + choice/use-case across many protection traditions; амулет в машину is commercial/use-case with marketplace pressure but independent content/commerce also appears; demand rose materially through Jul 2026.
intent = automotive protection/use-case commercial + selection
 decision = KEEP
priority = P0
page_job = automotive protection/use-case category that helps users choose an amulet/obereg for the car across relevant stocked symbols
split_merge = MERGE close protection synonyms into one use-case cluster; SPLIT from mirror-pendant form-factor A13
confidence = high
missing_evidence = exact overlap/cannibalization across the three synonym SERPs; detailed assortment coverage beyond symbolic pendants/amulets
contamination_or_fit_notes = broader than any one symbol, but directly aligned to the stated automotive use case; independent pages appear, so this is not a pure platform-only battle
```

### A13

```text
unit_id = A13
root_or_cluster = подвеска на зеркало в машину
baseline_evidence = broad 1,074; quoted 266; all 10 observed Top-10 results are commercial marketplace/platform/catalog pages; results span toys, JDM, religious symbols, gifts, handmade items and amulets.
intent = near-pure transactional form-factor/product intent
 decision = KEEP
priority = P1
page_job = form-factor commercial category for mirror pendants, limited to actual stocked products and written as a product-format page rather than a protection guide
split_merge = SPLIT from A12 because Search is pure transaction/form-factor while A12 is mixed protection/use-case; cross-link where products overlap
confidence = high
missing_evidence = independent-site ranking feasibility beyond the observed all-platform Top-10 and exact assortment breadth in non-protection pendant styles
contamination_or_fit_notes = high lexical fit to a hanging pendant form, but semantic scope is much broader than amulets; this is a tougher platform battle than A12 and should not define the whole automotive architecture
```

### A14

```text
unit_id = A14
root_or_cluster = exact symbol + car tails (печать велеса в машину; вегвизир в машину; инь ян в машину; similar low-volume symbol-car wording)
baseline_evidence = печать велеса в машину 5; вегвизир в машину 4; инь ян в машину 5; stronger generic automotive clusters are orders of magnitude larger.
intent = highly specific product/use-case tail
 decision = REJECT
priority = P3
page_job = no standalone SEO landing; use naturally on the relevant symbol product/family page and/or A12/A13 where the exact product fits
split_merge = ABSORB into stronger symbol and automotive clusters; do not create thin intersection pages
confidence = high
missing_evidence = none required to reject standalone pages at present; product-level conversion could later justify merchandising, not necessarily SEO pages
contamination_or_fit_notes = exact wording is too small to support separate indexable intersections; stronger parent clusters carry the demand
```

### A15

```text
unit_id = A15
root_or_cluster = славянский оберег в машину / герб россии в машину / спаси и сохрани в машину / православный оберег в машину
baseline_evidence = historical 72 / 55 / 48 / 22 respectively; no exact SERP evidence supplied for these tails.
intent = specific automotive protection/theme variants
 decision = INVESTIGATE
priority = P2-P3
page_job = secondary facets/sections or exact product pages where inventory exists; not standalone category pages by default
split_merge = absorb under A12 or the relevant symbol/tradition family unless future Search and assortment evidence supports a distinct category
confidence = medium-high
missing_evidence = exact SERPs, current demand for historical signal, assortment depth by tradition/theme
contamination_or_fit_notes = more demand than the 4-5-volume symbol tails, but still too weak and under-evidenced to justify separate SEO architecture now
```

### A16

```text
unit_id = A16
root_or_cluster = талисман знак зодиака / оберег по знаку зодиака
baseline_evidence = талисман знак зодиака 3,422 broad but only 21 quoted; its Top-10 is about 6 informational/guide vs 4 commercial and stones/jewelry are a major neighboring intent; оберег по знаку зодиака 710 and its Search still contains multiple stones/minerals selection pages plus marketplaces.
intent = guide/selection-first with substantial stones/jewelry contamination
 decision = REJECT
priority = P2
page_job = reject as a dedicated commercial category target for the current symbolic-pendant baseline; only revisit as a guide/selection concept if the actual assortment has credible zodiac coverage
split_merge = do not merge this broad contaminated demand into core symbol or automotive category volume; keep outside the core commercial architecture
confidence = high for commercial rejection, medium for future editorial opportunity
missing_evidence = actual zodiac assortment, exact product-match coverage, conversion evidence for zodiac selection
contamination_or_fit_notes = broad volume materially overstates direct demand; the 3,422 → 21 precision gap is the strongest contamination warning in the packet
```

### A17

```text
unit_id = A17
root_or_cluster = знак зодиака в машину / талисман знака зодиака близнецы
baseline_evidence = broad 149 and 160; parent zodiac intent is contaminated and guide/selection-first; no exact SERPs for these tails are supplied.
intent = zodiac-specific long-tail commercial/selection intent
 decision = INVESTIGATE
priority = P3
page_job = product/collection support only if exact matching zodiac inventory exists; no standalone SEO pages by default
split_merge = absorb under a future validated zodiac guide/category or exact product pages, not into A12 merely because a car modifier exists
confidence = medium
missing_evidence = exact SERPs, quoted demand, actual zodiac assortment
contamination_or_fit_notes = parent-cluster contamination prevents treating these figures as clean direct pendant demand
```

### A18

```text
unit_id = A18
root_or_cluster = подарок мужчине в машину / подарок автомобилисту
baseline_evidence = 1,070 current signal and historical 1,192; Search is overwhelmingly shopping/gift, dominated by practical automotive kits, car-care products, holders and general accessories; pendant appears only as one option, not the dominant answer; closest pendant-specific observed child is only 7.
intent = generic automotive gift shopping/ideas
 decision = REJECT
priority = P2
page_job = no dedicated commercial gift-category landing for the symbolic pendant assortment; possible supporting editorial inclusion only if broader gift merchandising is developed
split_merge = keep outside core automotive-amulet category; do not inflate A12/A13 with generic gift volume
confidence = high
missing_evidence = broader gift assortment, conversion evidence, whether the site will intentionally merchandise non-pendant automotive gifts
contamination_or_fit_notes = real demand but weak direct assortment fit; generic demand is dominated by practical goods, so volume alone would create a mismatched page
```

### A19

```text
unit_id = A19
root_or_cluster = specialist independent-site opportunity
baseline_evidence = independent specialist sites dominate much of славянские обереги Top-10; a specialist ranks #2 for печать велеса; specialist sites are visibly competitive for алатырь оберег and оберег велес; specialist editorial ranks #1 for both печать велеса значение and вегвизир значение; specialist content/commerce ranks #3 for шлем ужаса оберег. In contrast, подвеска на зеркало в машину is an all-platform Top-10.
intent = architecture-level opportunity assessment
 decision = KEEP
priority = P0
page_job = build the independent site around specialist symbol/category expertise plus separate meaning/support pages where Search clearly asks for them; use pure form-factor/platform battles as secondary acquisition surfaces, not as the sole architecture
split_merge = prioritize A01/A02/A03/A04/A05/A08/A09/A10/A12; treat A13 as separate but less defensible specialist terrain
confidence = high
missing_evidence = domain authority, backlink profile, technical SEO baseline, conversion economics
contamination_or_fit_notes = ordinary Search repeatedly rewards specialist independents in symbol and meaning clusters, which is the strongest baseline evidence for an independent-site strategy
```

### A20

```text
unit_id = A20
root_or_cluster = mobile-first execution constraint across core roots
baseline_evidence = representative device split: славянские обереги PHONE 22,563 / DESKTOP 2,869; оберег в машину PHONE 1,297 / DESKTOP 100.
intent = cross-cutting delivery constraint, not a new keyword target
 decision = KEEP
priority = P0
page_job = all P0/P1 pages must make category comprehension, product selection, meaning summary, internal navigation and commercial CTA work on mobile first
split_merge = no additional SEO page; apply across retained architecture
confidence = high
missing_evidence = device conversion rates and mobile UX analytics
contamination_or_fit_notes = device evidence changes execution priority, not semantic clustering
```

## Resolved baseline tensions

1. **`печать велеса` vs `печать велеса значение`: split.** The primary root is strongly transactional/platform-heavy; the explicit meaning variant is meaning-first/hybrid with specialist editorial leaders. They should cross-link but have different page jobs.

2. **Named symbol families are not handled by volume alone.** `вегвизир` earns a commercial family page and a separate meaning guide because both precise demand and Search composition support the split. `шлем ужаса оберег` earns a commercial family page with embedded support. `алатырь оберег` earns a commercial family page. Lower-volume or under-observed families remain candidates rather than automatic pages.

3. **Automotive protection/use-case vs mirror-pendant form factor: split.** `оберег/амулет/талисман в машину` form one protection/use-case cluster with mixed commercial/choice intent; `подвеска на зеркало в машину` is a broader, near-pure transactional form-factor cluster. One page would blur materially different Search jobs.

4. **Zodiac broad demand is not accepted as core direct demand.** The 3,422 → 21 broad-to-quoted collapse and stones/jewelry-heavy guide SERPs make a commercial zodiac category unsafe without stronger assortment evidence. Generic zodiac commercial targeting is rejected in this baseline.

5. **Generic automotive gift demand is rejected as a standalone commercial target.** Demand exists, but ordinary Search expects practical gifts and general accessories more than symbolic pendants.

6. **Independent-site opportunity is strongest in specialist symbol/category and meaning surfaces.** `славянские обереги`, Veles/Alatyr-related specialist commerce, Vegvisir, and meaning pages repeatedly show specialist independents in competitive positions. `подвеска на зеркало в машину` is much closer to a platform battle and should be secondary.

7. **Low-volume exact `symbol + car` intersections are absorbed, not split.** `печать велеса в машину` (5), `вегвизир в машину` (4), `инь ян в машину` (5) do not justify thin standalone pages when far stronger symbol and automotive parent clusters exist.

## Proposed first-pass architecture implied by Pass A

```text
P0  /slavyanskie-oberegi/                         specialist commercial hub
P0  /pechat-velesa/                               commercial symbol/family
P0  /pechat-velesa/znachenie/                     separate meaning guide
P0  /vegvizir/                                    commercial symbol/family
P1  /vegvizir/znachenie/                          separate meaning guide
P1  /alatyr-obereg/                               commercial symbol/family
P1  /shlem-uzhasa/                                commercial symbol/family with embedded support
P0  /oberegi-v-mashinu/                           automotive protection/use-case category
P1  /podveski-na-zerkalo-v-mashinu/               separate form-factor commercial category
P1? /oberegi-velesa/                              conditional on actual Veles assortment breadth
```

The paths above are semantic jobs, not a requirement for exact URL spelling. Lower-volume symbol families should remain children of the hub/product inventory until their own Search composition and assortment depth justify dedicated indexable family pages.

## Final baseline conclusion

The strongest ordinary-SEO baseline is not a single broad marketplace-style catalog. It is a specialist independent architecture combining: (a) a strong Slavic commercial hub, (b) evidence-backed named-symbol commercial families, (c) separate meaning pages only where ordinary Search demonstrates a materially distinct informational surface, and (d) a dedicated automotive protection/use-case category separated from the broader mirror-pendant form-factor transaction.

High broad demand is explicitly discounted where precision or fit is weak. Zodiac and generic automotive gift roots must not be allowed to inflate the core opportunity. Exact `symbol + car` tails should be absorbed into stronger parent clusters rather than multiplied into thin pages.
