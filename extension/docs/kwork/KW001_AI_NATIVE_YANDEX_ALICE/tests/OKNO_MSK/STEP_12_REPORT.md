# Step 12 — Structural actions report

Date: 2026-08-31

## Status

`PASS_AFTER_FULL_STRUCTURAL_ACTION_AUDIT`

## Step goal

Convert the corrected Step-11 phrase/page evidence into a concrete site-structure action for every effective assigned task without automatically creating pages, inventing products/services, diagnosing cannibalization or using AI evidence early.

## Full roadmap

| Stage | Plain-language meaning | Status |
|---|---|---|
| 0 | Freeze what the client asked for | ✅ COMPLETE |
| 1 | Understand the site and what it sells/explains | ✅ COMPLETE |
| 2 | Plan how to collect real search demand | ✅ COMPLETE |
| 3/3R | Collect and repair the first demand dataset | ✅ COMPLETE / historical first pass superseded |
| 4 | Roughly separate useful directions from noise | ✅ COMPLETE |
| 5 | Collect missing demand directions | ✅ COMPLETE |
| 6/6A | Check seasonality and whether collection is sufficient | ✅ COMPLETE |
| 7 | Clean individual search phrases | ✅ COMPLETE AFTER CORRECTION |
| 8 | Freeze the set that goes into Search analysis | ✅ COMPLETE AFTER CORRECTION |
| 9 | Check selected phrases in ordinary Yandex Search | ✅ COMPLETE AFTER CORRECTIONS |
| 10 | Group phrases by the real task a person wants to solve | ✅ COMPLETE |
| 11 | Decide which existing page should answer each task and materialize every phrase | ✅ COMPLETE AFTER CORRECTION |
| 12 | Decide what pages to keep, strengthen, add, create or deliberately not create | ✅ COMPLETE / PASS AFTER FULL STRUCTURAL ACTION AUDIT |
| 13 | Check whether similar pages actually compete with each other in Search | ⬜ NOT STARTED |
| 14 | Freeze the classic-Search site structure | ⬜ NOT STARTED |
| 15 | Choose the cases where AI search can add useful evidence | ⬜ NOT STARTED |
| 16 | Collect selected AI-search evidence | ⬜ NOT STARTED |
| 17 | Compare ordinary Search and AI-search behaviour | ⬜ NOT STARTED |
| 18 | Decide what should be implemented first | ⬜ NOT STARTED |
| 19 | Build client-ready files | ⬜ NOT STARTED |
| 20 | Check the final work for contradictions and missing items | ⬜ NOT STARTED |
| 21 | Deliver and handle allowed revisions | ⬜ NOT STARTED |
| 22 | Close the job cleanly | ⬜ NOT STARTED |


## Accounting

```text
SOURCE_ACTIVE_PHRASES = 2332
ASSIGNED_PHRASES = 2313
SEARCH_REQUIRED = 19
ASSIGNED_CLUSTERS = 75/75
PHRASE_ACTION_MAP_ROWS = 2332
PHRASE_ROUTING_OVERRIDES_TO_KNOWN_EXISTING_CHILD/UTILITY_PAGES = 191
PAGE_ROLLUP_ROWS = 55
NEW_BRIDGE_REQUESTS = 0
NEW_BRIDGE_COST_RUB = 0.0
FINAL_GITHUB_READBACK = PASS
```

Cluster-level action counts:

```text
ADD_SECTION_OR_FAQ_TO_EXISTING = 9
EXPAND_EXISTING_PAGE = 8
KEEP_EXISTING_STRUCTURE = 29
NEW_COMMERCIAL_PAGE = 2
NEW_INFORMATIONAL_PAGE = 3
NO_STANDALONE_PAGE = 18
OUTSIDE_SCOPE_NO_ACTION = 6
```

## New pages justified now

- `PANORAMIC_WINDOWS_COMMERCIAL` → **PROPOSED_NEW:/panoramnye-okna/** — Panoramic windows are a large, stable commercial task across house/terrace/general purchase queries, and no general commercial panoramic owner exists. Create one useful broad commercial page that explains product options, materials, opening, sizing, price factors and routes object-specific balcony/veranda cases to their pages.
- `WINDOW_HARDWARE_INFO` → **PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/** — Create one substantial guide to window hardware: what it is, types, major brands, how to choose, compare, maintain and lubricate it. The 41-phrase set represents a stable explanatory/selection task and no broad owner exists.
- `WINDOW_INSTALLATION_DIY_INFO` → **PROPOSED_NEW:/stati/ustanovka-plastikovyh-okon-svoimi-rukami/** — Create a comprehensive DIY installation guide covering preparation, gaps, dismantling, fixing, sealing, common errors and when professional installation is safer. The 36 phrases form a stable standalone how-to task.
- `WINDOW_REPAIR_DIY_INFO` → **PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/** — Create a comprehensive DIY diagnostics/adjustment/repair guide for common PVC-window problems. The set has a stable self-help task and no broad current owner.
- `WINDOW_REPLACEMENT_SERVICE` → **PROPOSED_NEW:/uslugi/zamena-okon/** — Replacement is a distinct end-to-end service task: remove old window, prepare opening, install new window and finish/hand over. The current installation page covers parts of this workflow but has no replacement-specific landing.

No page was created merely because Step 11 had `NO_SUITABLE_EXISTING_PAGE`; each new-page row has a distinct task and explicit useful-content rationale.

## Existing structure discovered during full phrase review

Step 12 does not blindly inherit the broad Step-11 owner when a more specific **already existing and previously read** child/utility page clearly matches the phrase. The phrase-level map therefore routes supported subsets to current pages such as credit/instalments, calculator, private-house windows, P-44, aluminium sliding/hinged, panoramic balcony, warm/cold veranda, PVC-door subtypes, REHAU model pages and specific accessory pages.

This is a structural routing refinement based only on already persisted first-party discovery evidence; it does not claim those URLs are proven Yandex ranking URLs.

## Deliberately no standalone page

- `BALCONY_GLAZING_PROVIDER_REVIEWS_INFO` — A first-party seller cannot truthfully become a neutral ranking/review page for competing balcony-glazing providers; no standalone target should be created for this generic reputation task.
- `GLAZING_DIY_INFO` — The small set mixes balcony and veranda DIY and different technologies; one generic DIY-glazing page would be too broad and thin. Specific DIY guidance can be attached to the relevant object pages or future coherent guides.
- `GLAZING_PERMISSION_INFO` — The phrases mix balcony permission, French-window redevelopment, boiler-room window requirements and hardware standards; they do not form one useful standalone legal page.
- `MOSQUITO_NET_REPAIR_SERVICE` — Repair of mosquito nets is not verified as a current offered service; do not create a commercial repair page from demand alone.
- `OPEN_BALCONY_FINISHING` — The current site explicitly does not offer interior balcony finishing without glazing; creating a landing would contradict the public offer.
- `OUTDOOR_GLAZING_REVIEWS_INFO` — One generic veranda-glazing review query does not justify a standalone first-party review page.
- `OUTDOOR_GLAZING_SPECIALIZED_INFO` — Frameless glazing, liquid glass and polycarbonate thickness are different techniques/material questions; the three phrases do not support one coherent standalone document.
- `PVC_DOOR_REPAIR_SERVICE` — PVC-door repair is not verified as a current offered service; do not publish a service landing based only on query demand.
- `PVC_DOOR_REPLACEMENT_SERVICE` — PVC-door replacement is not verified as a standalone current service; three phrases alone do not override that business-evidence gap.
- `ROOF_WINDOWS_COMMERCIAL` — Mansard/roof-window product availability is not verified on the site; do not create a commercial page from two phrases.
- `SOFT_WINDOWS_COMMERCIAL` — Soft/flexible-window product availability is not verified and the only phrase is ambiguous; no standalone commercial page.
- `TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL` — Timber-aluminium products are not verified as part of the current offer; do not create a commercial family page until the product is confirmed.
- `WINDOWSILL_REPAIR_SERVICE` — Repair/restoration of windowsills is not verified as a standalone offered service; current assets cover sills and finishing but not this exact service.
- `WINDOW_HARDWARE_SHOPPING` — The cluster is a broad aftermarket/third-party hardware catalog task; the target site is not verified as a general parts marketplace. Do not create a massive hardware-store landing.
- `WINDOW_PRODUCT_REVIEWS_INFO` — Generic product/model reviews and ratings are not one truthful first-party review asset. Do not create a page that pretends neutral third-party review coverage; rating-only phrases can route to the existing comparison article.
- `WINDOW_PRODUCT_VIDEO_INFO` — Two generic “video” phrases do not justify a standalone page; useful videos should live on the relevant PVC/aluminium product pages or portfolio.
- `WINDOW_PROVIDER_REVIEWS_INFO` — Generic ratings/reviews of installers and repair providers require neutral comparative evidence; a first-party company site should not create a self-authored ranking page.
- `WOOD_WINDOWS_COMMERCIAL` — Wooden-window products are not verified as a current offer and the five phrases are partly mixed with plastic windows in wooden houses; no standalone wooden-window commercial page.

## Step-13 handoff

The following structural areas require later Search-conflict checking, but **no cannibalization verdict is made here**:

- `ALUMINIUM_WINDOWS_COMMERCIAL` — https://okno-msk.ru/alyuminievye-okna/
- `BALCONY_GLAZING_GENERAL` — https://okno-msk.ru/balkony-i-lodzhii/
- `OUTDOOR_STRUCTURE_GLAZING` — https://okno-msk.ru/verandy/
- `PANORAMIC_WINDOWS_COMMERCIAL` — PROPOSED_NEW:/panoramnye-okna/
- `PVC_WINDOWS_COMMERCIAL` — https://okno-msk.ru/okna-rehau/
- `REHAU_WINDOWS_COMMERCIAL` — https://okno-msk.ru/okna-rehau/
- `WINDOWS_COMMERCIAL_GENERAL` — https://okno-msk.ru/
- `WINDOW_REPLACEMENT_SERVICE` — PROPOSED_NEW:/uslugi/zamena-okon/
- `WINDOW_SELECTION_INFO` — https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna/

`SPLIT_EXISTING_PAGE = 0` and `MERGE_STRUCTURALLY_REDUNDANT_PAGES = 0` at this step because current evidence did not justify a structural split/merge without relying on the search-conflict question reserved for Step 13. Empty action categories are accepted; they are not populated for symmetry.

## Search-required handoff

All 19 unresolved phrases remain `DEFER_UNRESOLVED` with no page action.

## ПРОСТЫМИ СЛОВАМИ — ИТОГ

### Зачем делали этот шаг

Чтобы превратить список поисковых фраз и страниц в **понятный план того, что менять на сайте**, а не просто собирать данные.

### Что фактически сделали

Для каждой темы просмотрели все относящиеся к ней фразы и решили: оставить нынешнюю страницу, усилить её, добавить нужный блок, сделать действительно новую страницу или сознательно не создавать страницу. Там, где на сайте уже есть более точная страница — например про рассрочку, конкретный тип двери или конкретную модель окна — фразы направлены туда, а не в слишком общую страницу.

### Что получили и что это даёт дальше

Получили полный черновик карты изменений сайта: какие нынешние страницы сохраняем, что в них дополняем, какие новые страницы действительно оправданы и какие идеи отвергаем. Следующий шаг будет отдельно проверять, не мешают ли похожие страницы друг другу в поиске; на этом шаге такой вывод специально не делался.
