# blood_sand — AI-native Pass B

Date: 2026-08-27

```text
PASS_A_COMMIT = 9501af0da39c671f578f56bb56dad311f2d9c761
PASS_A_IMMUTABLE_BEFORE_AI_EXPOSURE = true
frozen_source_commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
fresh_provider_requests = 0
final_R3_opened_before_pass_b_freeze = false
```

## Evidence boundary

Baseline is the immutable Pass A at:

`extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md`

Added AI layer is canonical consumer-Alice evidence from the frozen `blood_sand` commit, principally:

- `marketing/research/R2_PRIMARY_SEARCH_ALICE_COMPARISON_2026-08-26.md`
- `marketing/research/R2_YANDEX_SERP_ALICE_FINAL_REPORT_2026-08-26.md`
- `marketing/data/normalized/alice/20260826T0734Z__pechat_velesa.csv`
- `marketing/data/normalized/alice/20260826__alatyr_obereg.csv`
- `marketing/data/normalized/alice/20260826__obereg_v_mashinu.csv`
- `marketing/data/normalized/alice/20260826__obereg_veles.csv`
- `marketing/data/normalized/alice/20260826__vegvizir.csv`
- `marketing/data/normalized/alice/20260826__podarok_muzhchine_v_mashinu.csv`
- `marketing/data/normalized/alice/20260826__podarok_muzhchine_v_mashinu__CONTEXT_CONTAMINATED.csv`

No fresh provider request was made. Final R3 opportunity artifacts were deliberately not opened before this Pass B was frozen.

## Interpretation model

H / A / C / O remain separate:

- `H` = human demand / ordinary Search evidence from Pass A.
- `A` = direct observed Alice answer/source/fan-out importance.
- `C` = commercial fit inferred only from known assortment/use-case boundaries; no owned-site revenue is claimed.
- `O` = owned-asset opportunity inferred only from repeat specialist-source participation; no Webmaster/Metrika performance is claimed.

No opaque combined score is used.

## AI-native decision register

| Unit | AI-native decision / priority | AI-native page job | Exact added AI signal | Change vs Pass A |
|---|---|---|---|---|
| A01 `славянские обереги` | KEEP / P0 | specialist commercial hub plus source-worthy explanatory/selection support | Alice is informational/explanatory while specialist independents repeatedly participate as sources | confidence/source-quality requirement increases; core architecture unchanged |
| A02 `печать велеса` | KEEP / P0 | commercial symbol-family landing, paired with A03 | Alice on the unmodified root is meaning/explanation-first; 17 captured sources include informational and independent commerce-content pages; observed fan-outs cover historical use, related Veles symbols and legends | split already found by Search; AI materially de-risks it but does not create a new split |
| A03 `печать велеса значение` | KEEP / P0 | dedicated meaning/use/history guide cross-linked to A02 | Alice base-root answer itself emphasizes forms, symbolism, historical/ritual use, bear-vs-wolf distinctions, wearing caveats and modern use | content specification becomes more explicit; decision unchanged |
| A04 `оберег велес` | **KEEP / P1** | **Veles-family selection/explanation guide with commercial modules for stocked forms; separate commercial category only if assortment depth supports it** | Alice directly presents multiple Veles forms (bull-head, bear paw, wolf paw), task-based suitability/selection and 3 product cards; sources include `slavyarmarka.ru`, `slavyanskieoberegi.ru`, `veles.bz`, `ruyan-master.ru` | **material: INVESTIGATE → KEEP for a supporting family selection job; avoids requiring assortment breadth before any standalone owned job exists** |
| A05 `алатырь оберег` | KEEP / P1 | **hybrid content-commerce family page with substantial meaning/mythology/suitability block; separate meaning URL still conditional on Search demand** | Alice answer is explicitly meaning/mythology/suitability-first; 18 exact source URLs were captured, heavily including informational and independent commerce-content sources | **material PAGE_JOB_CHANGE: thin commercial-first page is insufficient; explanatory source-worthiness becomes required work** |
| A06 `оберег чур / сварог` | INVESTIGATE / P2 | candidate child families | no direct canonical Alice observation in the inspected set changes the evidence boundary | NO_CHANGE |
| A07 lower-volume named Slavic symbols | INVESTIGATE / P2-P3 | absorb in Slavic hub until evidence/assortment supports split | no direct canonical Alice evidence inspected for these units | NO_CHANGE |
| A08 `вегвизир` | KEEP / P0 | specialist commercial/entity family landing paired with A09 | both embedded and standalone Alice are history/meaning-first; answer explicitly corrects the common Viking-age framing and cites reference + specialist commerce-content sources | architecture unchanged; factual-source requirement strengthened |
| A09 `вегвизир значение` | **KEEP / P0** | **launch-critical history/meaning guide with explicit provenance/correction layer** | Alice on the high-demand base root itself prioritizes Huld manuscript 1860, non-Viking-age correction, etymology, purpose and scientific caveat; 11 exact embedded sources captured | **material PRIORITY_CHANGE: P1 → P0 because AI importance is high on the base root, not only on an explicit meaning modifier** |
| A10 `шлем ужаса оберег` | KEEP / P1 | commercial family page with history/meaning support | adjacent Alice evidence distinguishes Ægishjálmur from Vegvísir, but there is not enough direct Alice evidence here to justify another URL | NO_CHANGE at architecture level |
| A11 `валькнут / гунгнир` | INVESTIGATE / P3 | product/hub support only | insufficient direct added AI evidence | NO_CHANGE |
| A12 automotive protection (`оберег/амулет/талисман в машину`) | KEEP / P0 | hybrid choice/use-case commerce category with selection, placement/safety and product modules | Alice is hybrid choice/use-case + shopping and injects 7 directly orderable products; source set mixes specialist commerce-content, marketplaces, public information and media | confidence and implementation detail increase; Pass A already required choice support |
| A13 mirror-pendant form factor | KEEP / P1 | form-factor commercial category, separate from protection job | canonical R2 records Alice as broad decor/form-factor shopping with direct products, reinforcing commodity breadth | NO_CHANGE; contamination/competition risk reinforced |
| A14 exact symbol+car tails | REJECT standalone / P3 | absorb into stronger symbol/automotive pages | AI evidence does not justify thin intersection pages | NO_CHANGE |
| A15 specific automotive-theme tails | INVESTIGATE / P2-P3 | facets/sections/product pages | no direct AI evidence sufficient for standalone split | NO_CHANGE |
| A16 zodiac broad roots | REJECT core commercial target / P2 | only a future guide if real zodiac assortment exists | Alice is sign-by-sign selection with stones/colors/symbols central; no direct product-card section; narrower `оберег по знаку зодиака` still did not clean the stones/jewelry contamination | NO_CHANGE but strongly de-risked |
| A17 zodiac tails | INVESTIGATE / P3 | exact products/support only | broad Alice contamination does not validate tail architecture | NO_CHANGE |
| A18 generic automotive gifts | REJECT core pendant landing / P2 | no dedicated pendant gift-category page | clean Alice rerun centers practical accessories/comfort/electronics/car care and has no organic amulet/pendant/symbol category; prior contaminated run explicitly injected Vegvisir/Veles/runic suggestions because it referenced earlier amulet queries and is marked `EXCLUDED_FROM_PRIMARY` | **material CONTAMINATION_CORRECTION: prevents a false gift expansion caused by conversational carry-over; baseline rejection remains** |
| A19 specialist independent-site opportunity | KEEP / P0 | **owned specialist asset must be both commerce-capable and citation/source-worthy, with explanatory pages/modules designed as first-class assets** | Alice source panels repeatedly include specialist content-commerce domains for Pechat Velesa, Alatyr, Veles family, Vegvisir and automotive protection | **material SOURCE_GAP_FOUND: ranking alone is not sufficient; source-worthiness changes required content work** |
| A20 mobile-first execution | KEEP / P0 | cross-cutting mobile requirement | no Alice evidence changes device evidence | NO_CHANGE |

## Material AI-native changes

### B-D1 — Veles-family supporting job becomes actionable

Pass A could not justify a standalone `оберег велес` job without knowing assortment breadth. Alice directly observes a multi-form selection/suitability task and light shopping for the same root. That creates an owned **selection/explanation guide job** even when a deep product category is not yet justified.

This is not a claim that a separate commercial category must exist. The material change is that the owned site should have a Veles-family explanatory/selection asset rather than merely waiting for assortment proof.

### B-D2 — Alatyr commercial page requires source-worthy explanation

Pass A supported a commercial Alatyr page and only concise meaning support. Alice answers the unmodified root as meaning/mythology/suitability-first and draws from a large mixed informational/content-commerce source set. A product-family page that omits substantive explanation would satisfy Search commerce but underserve the observed AI job.

The revised job is hybrid content-commerce. A separate meaning URL remains conditional to avoid inventing cannibalizing architecture without Search-demand evidence.

### B-D3 — Vegvisir meaning/history work moves to launch-critical priority

Pass A already found a clean meaning split. Alice independently makes meaning/history/correction the dominant job on the broad high-demand `вегвизир` root itself. Therefore the A09 guide is promoted from P1 to P0. The extra work is also qualitative: historical provenance and explicit correction of the common Viking-age framing are required to be source-worthy and truthful.

### B-D4 — Contaminated AI context is proven dangerous and excluded

The old `подарок мужчине в машину` run says it injected Vegvisir/Veles/runic pendant suggestions because of prior amulet queries. The clean rerun removes that branch and returns broad practical gift selection. The contaminated record is explicitly `EXCLUDED_FROM_PRIMARY`.

The correct AI-native action is therefore **not** to reverse Pass A's gift rejection. This is a material de-risking result: provenance/context controls prevent a false architecture expansion.

### B-D5 — Specialist source-worthiness becomes an explicit owned-site requirement

Ordinary Search already proved specialist sites can rank. Alice adds a different observation: specialist commerce-content pages are repeatedly used as answer sources. This changes the work specification from "build specialist pages that can rank" to "build specialist pages that can both satisfy commerce and stand as factual explanatory sources".

## Cases where AI evidence does not change the action

AI evidence does **not** justify rewriting every baseline decision. Important `NO_CHANGE` cases include:

- `печать велеса` commercial-vs-meaning split: already found by ordinary Search;
- automotive protection vs mirror-form-factor split: already found by ordinary Search;
- zodiac commercial rejection: already supported by Wordstat precision + Search contamination;
- generic gift rejection: clean Alice confirms rather than reverses it;
- low-volume symbol-car intersection pages: no AI evidence justifies thin pages;
- mobile-first execution: Wordstat/device evidence remains the basis.

## Pass B freeze statement

```text
PASS_B_FROZEN = true
PASS_A_USED_IMMUTABLY = 9501af0da39c671f578f56bb56dad311f2d9c761
fresh_provider_requests = 0
final_R3_opened_before_pass_b_freeze = false
observed_vs_inferred_separated = true
```
