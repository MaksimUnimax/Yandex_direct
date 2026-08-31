# KW-001 / OKNO-MSK — Step 11 Codex current page refresh

Date: 2026-08-30

This is an acquisition/extraction pass only. It makes no `CREATE`, `MERGE`, `SPLIT`, `DELETE`, `KEEP`, `EXPAND`, page-ownership, or cannibalization decision.

## Method and evidence boundary

The rendered homepage was opened first. Its visible main navigation, mega-menu, footer, internal commercial links and CTAs were read, then material current URLs were opened in a browser and their rendered title, H1, headings, primary copy, CTA and final URL were recorded. Step-01 was used only afterwards as a reconciliation baseline. No Wordstat, Search API, GenSearch, Webmaster or other paid Yandex provider API was called.

## Quantitative reconciliation

```text
TOTAL_URLS_DISCOVERED = 67
OPENED_READ_COUNT = 61
DISCOVERED_LINK_ONLY_COUNT = 5
INFERRED_TEMPLATE_FAMILY_COUNT = 0
UNVERIFIED_OR_INACCESSIBLE_COUNT = 1
OLD_STEP01_URLS_RECONFIRMED = 54
NEW_URLS_NOT_IN_STEP01 = 15
OLD_STEP01_URLS_NOT_RECONFIRMED = 10
```

`UNVERIFIED_OR_INACCESSIBLE_COUNT` is `https://okno-msk.ru/robots.txt`: the in-app browser was blocked by its client policy, so it was not used as discovery evidence. It is not a content page.

The counts distinguish *current page reading* from link discovery. The URL TSV is the complete reported acquisition set; the profile ledger concentrates the material pages for current Step-11 candidate work and records the actual rendered evidence, rather than treating a slug as page purpose.

## Step-01 comparison

Reconfirmed material families include REHAU/PVC windows and profile models, PVC doors, aluminium/Provedal, balcony warm/cold/engineering/finishing variants, verandas, installation/repair/slopes, price and calculator utilities, accessories, editorial pages, company/trust assets, and the Mitino district GEO page.

New current discoveries not represented in the Step-01 union include the `rehau-delight` and `rehau-delight-decor` profile pages, current house-type/accessory hubs, rendered balcony calculator URL, window/door calculators, measurement URL, winter-garden and summer-kitchen children, and several accessory children.

The historical city-subdomain example `https://balashiha.okno-msk.ru/` no longer exposes a Balashikha landing: the current browser navigation finished at `https://okno-msk.ru/`. It is therefore a redirect observation, not evidence for a live subdomain family. The historical source did not establish the full GEO universe, so this does not prove that no other subdomains exist.

The following Step-01 pages/families were not reconfirmed in this bounded current pass and must not be treated as current-page reads: the exact `balkon-polukruglyj`, second-contour, P-46 balcony-series, `rehau-intellio-80` deep content, several individual house-series pages, `rehau-thermo-design` deep content, `stati/kak-vybrat-cvetnoe-plastikovoe-okno`, `uslugi/kredit-i-rassrochka`, `uslugi/rasshirennaya-garantiya`, and `o-kompanii/proizvodstvo`. Some were visible as current links or sibling template paths but were not assigned `OPENED_READ` solely for that reason.

## New material page families

- Current separate REHAU profile family now visibly includes Delight Design and Delight Decor alongside the previously known models.
- Current calculator/estimate family has distinct window, balcony and door entry paths; balcony calculation rendered parameter steps, while the window price/calculator surfaces showed a loading placeholder.
- Current accessory hierarchy exposes a broader selection of security, child-lock, glass, handle, windowsill, drip-cap and lamination pages.

## Material unread or ambiguous pages

- Accessory links: `grebenki-i-zamki`, `detskie-zamki`, `energosberegayuschie-steklopakety`.
- Potential panoramic sibling: `balkony-i-lodzhii/osteklenie-ot-pola-do-potolka/`.
- Outdoor child: `verandy/holodnoe-osteklenie-besedok/`.
- Any further city-subdomain family beyond the historical Balashikha example remains unenumerated by this pass.

## Pages requiring rendered/browser inspection in ChatGPT Work

- `https://okno-msk.ru/ceny/` and `https://okno-msk.ru/kalkulyator-okon-rehau/`: the rendered main content says `Calculator is loading`; inspect loaded controls, available profile/product combinations and final conversion route.
- `https://okno-msk.ru/kalkulyator-ostekleniya-balkona/` and balcony pages containing its embedded calculator: inspect state changes, option dependencies, calculated total and post-calculation CTA.
- `https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/ruchki-na-okna/`: the page mixes purchasable handles with a DIY replacement section; inspect hierarchy/tabs and prominent rendered CTA before any task-to-page conclusion.
- `https://okno-msk.ru/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/` and `https://okno-msk.ru/okna-rehau/francuzskie-okna/`: inspect rendered comparison blocks and CTA to distinguish commercial task boundaries from the panoramic editorial page.
- GEO district/subdomain templates: inspect visible location switching, hidden menus and canonical/redirect behaviour, especially before declaring the public GEO family exhausted.
