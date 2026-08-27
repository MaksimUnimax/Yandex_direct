# AI-native blood_sand comparative gate — final comparison

Date: 2026-08-27

## Authority / anti-leakage

```text
blood_sand_commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
pass_a_commit = 9501af0da39c671f578f56bb56dad311f2d9c761
pass_b_commit = d0cad99be1c1cf70ad06d3cf7bf28495daab58b8
pass_b_manifest_commit = 752fc2846c54698578718374ffac506942628408
fresh_provider_requests = 0
```

Canonical gate:

`extension/docs/AI_NATIVE_BLOOD_SAND_REQUIRED_COMPARATIVE_GATE.md`

Original Pass A manifest:

`extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_SOURCE_MANIFEST_2026-08-27.md`

Actual valid Pass A execution authority:

`extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_SEALED_BASELINE_PACKET_2026-08-27.md`

Pass B manifest:

`extension/tests/AI_NATIVE_BLOOD_SAND_PASS_B_SOURCE_MANIFEST_2026-08-27.md`

### Manifest erratum

The first clean-chat attempt failed closed because the original baseline manifest admitted documents that themselves contained AI/Alice-derived text. No Pass A was written in that failed attempt.

The defect was corrected by creating an explicit sealed Alice-free packet containing only neutral assortment framing, measured Wordstat observations and ordinary Yandex Search observations. A completely new clean chat then read only the hardened handoff + sealed packet and froze Pass A with:

```text
extra_source_opened = false
fresh_provider_requests = 0
```

Therefore the valid baseline is the sealed packet + Pass A commit `9501af0d...`, not the failed first attempt.

Pass B was frozen before final R3/opportunity artifacts were opened. Final R3 was used only afterward as an external consistency check.

## Decision-level comparison

| Unit | Baseline evidence / intent | Pass A decision / priority / page job | AI-native evidence / intent | Pass B decision / priority / page job | delta_type | Commercial / architecture impact | Confidence | material_delta |
|---|---|---|---|---|---|---|---|---|
| A01 `славянские обереги` | high precise demand; Search commercial/category-first; specialist independents strong | KEEP / P0 / specialist commercial hub with info support | Alice is more explanatory and also uses specialist sources | KEEP / P0 / same hub, but explanatory/source-worthy support becomes explicit | SOURCE_GAP_FOUND | content bar rises, architecture unchanged | high | no |
| A02 `печать велеса` | Search strongly transactional/platform-heavy | KEEP / P0 / commercial family page | Alice on the same broad root is meaning/history/use-first; 17 captured sources; fan-outs on historical use, related symbols, legends | KEEP / P0 / commercial page paired with meaning guide | CONFIDENCE_CHANGE | validates split and required cross-linking | high | no |
| A03 `печать велеса значение` | explicit meaning Search is clearly separate | KEEP / P0 / dedicated meaning guide | base-root Alice independently emphasizes forms, symbolism, history, use and caveats | KEEP / P0 / dedicated meaning/use/history guide | CONFIDENCE_CHANGE | stronger content specification, no new URL decision | high | no |
| A04 `оберег велес` | commercial Search strong but commercial category depends on real assortment breadth | INVESTIGATE / P1 / candidate Veles commercial category or merge with Pechat | Alice directly observes a multi-form Veles selection/suitability job (bull-head, bear paw, wolf paw) plus 3 products and specialist sources | **KEEP / P1 / Veles-family selection/explanation guide; commercial category remains conditional on assortment** | **NEW_SUPPORTING_JOB + KEEP_REJECT_CHANGE** | **creates an actionable owned job even before SKU depth proves a separate commercial category** | high | **yes** |
| A05 `алатырь оберег` | Search commercial-first + meaning support | KEEP / P1 / commercial family page, concise meaning support | Alice is meaning/mythology/suitability-first; 18 exact sources include many information/content-commerce pages | **KEEP / P1 / hybrid content-commerce page with substantial explanatory block** | **OTHER_TRACEABLE_CHANGE / PAGE_JOB_CHANGE** | **meaning/suitability becomes required work, not optional short copy** | high | **yes** |
| A06 `оберег чур / сварог` | demand exists; exact Search not measured in packet | INVESTIGATE / P2 | no direct added AI evidence used | INVESTIGATE / P2 | NO_CHANGE | none | medium-low | no |
| A07 lower-volume Slavic symbols | low/moderate demand; no direct Search | INVESTIGATE / P2-P3 / absorb in hub | no direct added AI evidence used | INVESTIGATE / P2-P3 | NO_CHANGE | none | medium | no |
| A08 `вегвизир` | high precise demand; Search mixed entity + commerce | KEEP / P0 / commercial/entity family paired with meaning guide | Alice is strongly history/meaning/correction-first on broad root; reference + specialist commerce-content sources | KEEP / P0 / same pair with strict provenance/accuracy requirement | SOURCE_GAP_FOUND | truth/source-quality bar rises | high | no |
| A09 `вегвизир значение` | meaning Search overwhelmingly informational | KEEP / P1 / meaning/history guide | broad high-demand `вегвизир` itself triggers Alice history/meaning/correction-first behavior, including Huld 1860 and non-Viking-age correction | **KEEP / P0 / launch-critical provenance-rich history/meaning guide** | **PRIORITY_CHANGE** | **guide moves into first-launch work rather than secondary support** | high | **yes** |
| A10 `шлем ужаса оберег` | coherent commercial named-symbol SERP | KEEP / P1 / commercial page with meaning support | adjacent Alice evidence distinguishes Ægishjálmur, but direct Alice usefulness on exact root remains unmeasured | KEEP / P1 | NO_CHANGE | prevents over-claiming AI priority | medium-high | no |
| A11 `валькнут / гунгнир` | very low measured demand | INVESTIGATE / P3 | insufficient AI evidence | INVESTIGATE / P3 | NO_CHANGE | none | medium | no |
| A12 automotive protection | Search mixed choice/use-case + commerce; real demand | KEEP / P0 / protection/use-case category with choice support | Alice is hybrid choice/use-case + shopping and injects 7 products; source set includes specialist commerce-content and marketplaces | KEEP / P0 / hybrid choice-commerce category with placement/safety/product modules | CONFIDENCE_CHANGE | implementation detail and confidence improve; baseline already had correct job | high | no |
| A13 mirror-pendant form factor | Search near-pure form-factor transaction, platform-heavy | KEEP / P1 / separate form-factor category | Alice remains broad decor/form-factor shopping with products | KEEP / P1 | NO_CHANGE | confirms commodity pressure and separation from protection job | high | no |
| A14 symbol+car exact tails | volumes ~4-5 | REJECT standalone / P3 | no AI evidence justifies thin pages | REJECT standalone / P3 | NO_CHANGE | avoids page proliferation | high | no |
| A15 specific automotive-theme tails | small/historical demand; under-measured | INVESTIGATE / P2-P3 | no decisive AI evidence | INVESTIGATE / P2-P3 | NO_CHANGE | none | medium | no |
| A16 broad zodiac | 3,422 broad → 21 quoted; Search stones/jewelry/guide contaminated | REJECT core commercial / P2 | Alice is sign-by-sign stones/colors/symbols selection; narrower root also remains contaminated | REJECT core commercial / P2 | CONFIDENCE_CHANGE | prevents treating broad demand as direct pendant opportunity | high | no |
| A17 zodiac tails | limited tails; parent contaminated | INVESTIGATE / P3 | no decisive clean tail AI evidence | INVESTIGATE / P3 | NO_CHANGE | none | medium | no |
| A18 generic automotive gifts | real demand, but Search practical-gift dominant and pendant weak-fit | REJECT core pendant landing / P2 | clean Alice has practical accessories/comfort/electronics/car-care and no organic pendant category; old run explicitly injected runic/Veles suggestions because prior amulet context and is `EXCLUDED_FROM_PRIMARY` | REJECT core pendant landing / P2 | **CONTAMINATION_CORRECTION** | **prevents a false gift-page expansion that contaminated AI evidence would have encouraged** | high | **yes (de-risking)** |
| A19 specialist independent opportunity | Search repeatedly rewards specialist independent pages | KEEP / P0 / specialist site with commercial + meaning assets | Alice repeatedly uses specialist commerce-content pages as answer sources across Pechat, Alatyr, Veles, Vegvisir and automotive protection | **KEEP / P0 / specialist owned asset must be explicitly citation/source-worthy as well as commerce-capable** | **SOURCE_GAP_FOUND** | **changes required content work from ranking-only to source-quality explanatory assets** | high | **yes** |
| A20 mobile-first execution | Wordstat/device evidence strongly mobile-first | KEEP / P0 | Alice adds no valid device evidence | KEEP / P0 | NO_CHANGE | device decision remains evidence-pure | high | no |

## Material deltas that establish incremental value

### 1. Veles-family job — new supporting action

Ordinary SEO could only say "investigate a broader Veles category if SKU depth supports it." Direct Alice evidence shows that users can receive a Veles-family chooser/explanation covering multiple forms and suitability before shopping. That makes a standalone **selection/explanation asset** actionable even while the commercial category remains conditional.

This is a real page-job change, not a cosmetic rewrite.

### 2. Alatyr — commercial page becomes hybrid content-commerce work

Ordinary Search supports commerce and some meaning support. Alice answers the unmodified root as mythology/meaning/suitability-first and draws on 18 captured sources. Therefore substantive explanatory/source-worthy content becomes a required component of the Alatyr owned asset.

The gate does **not** force a separate meaning URL because exact Search demand for that modifier was not measured.

### 3. Vegvisir — meaning/history priority moves P1 → P0

Pass A correctly discovered the meaning split, but treated it as secondary support. Alice makes historical explanation/correction the dominant job for the broad, high-demand root itself. That materially changes launch sequencing and content-quality requirements.

### 4. Context contamination control prevents a wrong action

The contaminated gift run explicitly injected runic/Veles suggestions due prior conversation. The clean rerun removes them. If provenance had been ignored, AI evidence could have falsely promoted the generic gift branch. Preserving context contamination therefore materially de-risks architecture.

### 5. Specialist source gap changes owned-site work

Search proved specialist sites can rank. Alice adds evidence that specialist commerce-content pages can be selected as sources. The premium method therefore adds a concrete requirement: explanatory pages/modules must be designed as credible standalone sources, not merely SEO landing copy.

## Important `NO_CHANGE` findings

The added AI layer did **not** overturn several strong ordinary-SEO decisions:

- Pechat Velesa commercial-vs-meaning split was already discoverable from Search.
- Automotive protection vs mirror-form-factor separation was already discoverable from Search.
- Zodiac rejection was already strongly supported by precision + Search contamination.
- Generic gift weak-fit was already visible in Search; clean Alice confirms it.
- Low-volume symbol+car tails still do not justify thin pages.
- Mobile-first execution remains based on Wordstat/device evidence, not Alice.

This matters: the comparative result is not based on claiming that AI evidence changes every cluster.

## Post-freeze R3 consistency check

After Pass B was frozen, `marketing/research/R3_OPPORTUNITY_MAP_FINAL_2026-08-26.md` was opened as an external reference.

It is broadly consistent with the independent comparison:

- Pechat Velesa, Slavic category, automotive protection, Alatyr and Vegvisir are strong opportunities.
- Broad zodiac and generic gift remain deprioritized/rejected as primary acquisition lanes.
- Broader Veles remains structurally distinct from Pechat Velesa but its commercial-category boundary depends on actual SKU hierarchy.
- R3 separately emphasizes historically rigorous Vegvisir content.

The apparent Veles difference is not a contradiction: Pass B authorizes a supporting chooser/explanation job; it does not assert an unconditional separate commercial category.

## Acceptance criteria

1. Pass A truly frozen before AI exposure — **PASS** (`9501af0d...`).
2. Same non-AI evidence base — **PASS**; Pass B starts from immutable Pass A.
3. Material deltas traceable to added evidence — **PASS**.
4. At least one material action-level change or de-risking — **PASS**; A04, A05, A09, A18, A19.
5. AI-native recommendations do not knowingly weaken SEO/user usefulness/truth/commercial role — **PASS**.
6. Observed evidence vs inference separated — **PASS**.
7. `NO_CHANGE` cases explicitly listed — **PASS**.

# Final verdict

```text
AI_NATIVE_COMPARATIVE_GATE_PASS
```

The experiment supports the narrow claim that, on this real project dataset, adding direct canonical consumer-Alice evidence to a strong Wordstat + ordinary Search baseline produced material actionable improvements/de-risking in page-job scope, launch priority, source-quality requirements and contamination control.

It does **not** prove traffic/revenue uplift, guaranteed Alice citation/indexing, permanent reproducibility, or that every semantic-core project needs AI evidence.

## Limitations

- one project/niche dataset;
- consumer-Alice observations are snapshots and not guaranteed stable;
- `A`, `C`, and `O` are not substitutes for owned-site conversion/revenue/behavior data;
- several Alice source panels lacked exact URLs or completeness confirmation and were kept as such;
- no fresh provider request was made for this comparative gate;
- the first Pass A attempt exposed a flawed manifest and failed closed; the valid second attempt used the superseding sealed packet;
- GenSearch equivalence to consumer Alice remains unproven.

## Next product decision

The broader methodology gate now authorizes the bounded provider-proxy subcheck defined in the canonical gate:

```text
canonical consumer Alice observations
vs
Yandex Search API GenSearch observations on a small representative set
```

The objective is to test answer job, source overlap/types, refined-query themes and whether any material decision implication changes.

**Do not yet claim GenSearch == consumer Alice.**

If the bounded proxy check is sufficiently aligned for the product purpose, promote a repeatable GenSearch evidence hand in Yandex Marketing Bridge. If it materially diverges, keep provenance separate and either retain a consumer-Alice validation surface or narrow the product claim.
