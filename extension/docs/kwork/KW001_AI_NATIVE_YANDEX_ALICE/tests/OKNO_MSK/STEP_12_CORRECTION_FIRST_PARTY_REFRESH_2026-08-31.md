# Step 12 correction — current first-party page refresh

Date: 2026-08-31
Scope: targeted first-party verification triggered by D12-12. This is not a new broad site crawl.

## Blinds page

URL:
`https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/zhalyuzi/`

Current public-page observations from direct first-party read:

- H1: `Жалюзи на пластиковые окна`;
- visible price starts from 600 ₽/m²;
- explicit product/types visible: horizontal blinds, vertical blinds, Isolite Isotra, pleated/plisse;
- text says company staff help users choose blinds and users can place an order;
- the purchase workflow explicitly shows consultation → measurement → contract → delivery → installation;
- the page therefore directly supports at least **selection + purchase + installation** of window blinds;
- the page does **not** by this read prove a standalone blinds-repair service;
- the page also does not by itself prove that every phrase containing generic curtains/roller curtains should be treated as the same sold product. Those remain separately reviewed rather than automatically rescued.

## Why this matters to Step 12

The historical `OUTSIDE_CURTAINS_BLINDS` state was too broad. Current first-party evidence directly contradicts treating all blinds demand as outside the business.

Correct structural interpretation:

```text
BLINDS SELECTION / SHOPPING
-> verified in-scope current product page

BLINDS INSTALLATION
-> verified as part of current page/order workflow

BLINDS REPAIR
-> not verified by this page read; keep deferred pending business truth

GENERIC CURTAINS / SHUTTERS / ROLLER-CURTAIN WORDING
-> do not automatically equate to the verified blinds offer without additional page/product evidence
```

This record supports D12-12 correction and must be read together with:

```text
STEP_12_CORRECTION_DEFECT_LEDGER.tsv
STEP_12_NO_PAGE_OUTSIDE_SALVAGE_REVIEW_V4.tsv
STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V4.tsv
```

Evidence source class: `FIRST_PARTY_CURRENT_WEB`.
