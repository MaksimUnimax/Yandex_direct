# AI-NATIVE SEMANTIC REBUILD — OWN SERVICE OPPORTUNITY

Status: **STRATEGIC OFFER / EXPERIMENTAL PREMIUM HYPOTHESIS / COMPARATIVE GATE REQUIRED**  
Date: 2026-08-27  
Internal offer id: **O-001**

## 1. Client problem / offer

O-001 is our own product concept derived from the real `MaksimUnimax/blood_sand` research workflow. It is not a Kwork observation and must not be counted as an F-case in market-demand statistics.

Internal shorthand `ИИ-индексация` is acceptable, but client-facing language must not promise guaranteed indexing, ranking or citation.

Preferred client-facing formulations:

- `Пересборка семантического ядра под Яндекс + Алису AI`;
- `AI-native семантическое ядро: обычный поиск + генеративная выдача`;
- `Семантика для обычного и AI-поиска`.

The differentiator is not generic GEO/AEO formatting. It is an **evidence-first rebuild of semantic and page architecture using human demand + ordinary Search + observed AI-search evidence**.

## 2. Permanent worker model

```text
CLIENT
→ site / business / region / goals / access

CHATGPT PLUS
→ research plan
→ query selection
→ evidence interpretation
→ contamination detection
→ semantic cleanup/clustering
→ H/A/C/O reasoning
→ page-job decisions
→ architecture/recommendations
→ client artifacts
→ QA

YANDEX MARKETING BRIDGE
→ controlled data/action hands
→ Wordstat
→ ordinary Yandex Search
→ Webmaster
→ Metrika
→ Direct where useful
→ future GenSearch if gate justifies implementation

HUMAN OWNER/OPERATOR
→ authorization/access boundary
→ runs irreducible local/account actions
→ does not perform the SEO analysis instead of ChatGPT
```

The extension should productize acquisition, persistence, safety and repeatability. ChatGPT remains the reasoning layer.

## 3. Methodology inherited from blood_sand

The accepted strategy treats ordinary Yandex Search and AI answers as connected but distinct evidence surfaces.

Important provenance classes include:

```text
SEED
WORDSTAT
SERP_QUERY
ALICE_INPUT
ALICE_SOURCE
ALICE_FANOUT_OBSERVED
ALICE_FANOUT_INFERRED
WEBMASTER_SEARCH
WEBMASTER_ALICE
CUSTOMER_EVIDENCE
MARKETPLACE_EVIDENCE
```

Canonical flow:

```text
registry/input
→ raw evidence
→ normalized observations
→ evidence ledger
→ derived analysis
→ action/page-job decision
```

Priority reasons remain separate:

```text
H = Human demand
A = AI/Alice importance
C = Commercial value
O = Owned-asset value
```

Do not collapse them into an unexplained single number.

## 4. Why this can change ordinary semantic-core decisions

A normal semantic core asks:

> what do people search, how often, and how should those queries be grouped?

O-001 additionally asks:

> what job does ordinary Search solve, what job does AI solve, which sources/pages support the AI answer, what adjacent questions/refined queries appear, and what page architecture should compete in both systems without weakening commerce or truthfulness?

`blood_sand` already contains real cross-surface differences, including roots where ordinary Search is strongly transactional while consumer Alice evidence is explanation/meaning/suitability-first.

That is real evidence that the surfaces can differ. It is **not yet proof** that the premium method beats a strong ordinary SEO baseline. That incremental value must be established by the mandatory comparative gate.

## 5. Mandatory comparative proof

Canonical gate:

`extension/docs/AI_NATIVE_BLOOD_SAND_REQUIRED_COMPARATIVE_GATE.md`

Clean baseline manifest:

`extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_SOURCE_MANIFEST_2026-08-27.md`

Design:

```text
PASS A
= business/product + Wordstat + ordinary Search
= no Alice/AI evidence

freeze

PASS B
= same baseline
+ canonical AI/Alice evidence

compare action-level decisions
```

Valid verdicts:

```text
AI_NATIVE_COMPARATIVE_GATE_PASS
NO_PROVEN_UPLIFT
INVALID_BASELINE_LEAKAGE
INSUFFICIENT_CANONICAL_EVIDENCE
```

The current long-running conversation has already consumed Alice-derived conclusions. Therefore a clean Pass A must be generated in a genuinely isolated context, not fabricated here.

## 6. Current market position

Generic GEO/AEO offers already exist. The quick market review surfaced audits, FAQ/content advice, AI-oriented page formatting and mass AI-content offers.

The review did not surface an exact equivalent of our full evidence chain:

```text
Wordstat
+ direct Yandex SERP
+ observed AI answer/source/refined-query evidence
+ observed-vs-inferred provenance
+ evidence ledger
+ H/A/C/O
+ page-job architecture
+ post-launch measurement
```

This is a differentiation signal, not proof that nobody else offers similar work anywhere.

## 7. Current capability after Phase 5 closure

Phase 5 Direct is now **PASS / CLOSED**.

| Layer | Status | Worker |
|---|---|---|
| Site/business analysis | YES | ChatGPT |
| Seed/query strategy | YES | ChatGPT |
| Wordstat human demand | YES | Bridge |
| Dynamics/region/device where exposed | YES | Bridge + ChatGPT |
| Ordinary regional Yandex SERP | YES | Bridge |
| Competitor/source/page-type analysis | YES bounded | ChatGPT |
| Semantic cleanup/clustering | YES | ChatGPT |
| Page-job/target-page architecture | YES bounded | ChatGPT |
| XLSX/CSV/PDF/DOCX deliverables | YES | ChatGPT artifact layer |
| Ordinary Webmaster query evidence | YES | Bridge |
| Metrika behavior/conversion | YES where data exists | Bridge + ChatGPT |
| Direct read data | YES where advertiser data exists | Bridge |
| Structured official AI-search provider path exists | YES, researched | Yandex GenSearch |
| GenSearch implemented in current Bridge | NO | gated future hand |
| Consumer-Alice equivalence to GenSearch proven | NO | validation required |
| Webmaster Alice visibility in current Bridge | NO | future official/import hand |

## 8. Critical new feasibility finding — official GenSearch

The preferred repeatable AI-search acquisition path is now official Yandex Search API GenSearch rather than default consumer-Alice DOM scraping.

Official endpoint:

```text
POST https://searchapi.api.cloud.yandex.net/v2/gen/search
```

Useful response evidence currently includes:

```text
message.content
sources[].url
sources[].title
sources[].used
searchQueries[].text
searchQueries[].reqId
hints[]
answer status flags
```

Provider research:

`extension/docs/AI_NATIVE_YANDEX_GENSEARCH_PROVIDER_RESEARCH_2026-08-27.md`

Product implication:

```text
existing Search provider family
├── ordinary /v2/web/search   [implemented]
└── generative /v2/gen/search [official path found, not implemented]
```

Do not create a separate credential-consolidation project. GenSearch belongs to the Search/Yandex Cloud credential family; Webmaster/Metrika/Direct remain independent.

## 9. Provenance caution — GenSearch is not automatically consumer Alice

Do not silently translate GenSearch evidence into consumer-Alice evidence.

Future normalized provenance should use labels such as:

```text
GEN_SEARCH_INPUT
GEN_SEARCH_ANSWER
GEN_SEARCH_SOURCE
GEN_SEARCH_SOURCE_USED
GEN_SEARCH_QUERY_OBSERVED
```

Do not automatically call `searchQueries[]`:

```text
ALICE_FANOUT_OBSERVED
```

A bounded comparison against the canonical `blood_sand` consumer-Alice observations is required after the broader methodology gate justifies the engineering priority.

## 10. Economics / test-set design

Official Yandex pricing snapshot recorded on 2026-08-27:

```text
generative synchronous Search API = 5,080 RUB / 1,000 requests incl. VAT
≈ 5.08 RUB/request
```

Therefore O-001 should not run every keyword through GenSearch.

Correct model:

```text
large Wordstat set
→ ChatGPT cleans/clusters
→ ordinary Search resolves many questions
→ ChatGPT selects small decision-relevant AI test set
→ GenSearch only for material AI-specific uncertainty
```

This preserves both economics and evidence quality.

## 11. Exact service workflow

```text
1. Intake
   site + region + products/services + goals + existing semantic core + optional competitors.

2. Business/site model
   ChatGPT maps offer, audience, exclusions, current pages and conversion jobs.

3. Human-demand layer
   Bridge Wordstat acquires bounded evidence.
   ChatGPT cleans and constructs candidate clusters.

4. Ordinary Search layer
   ChatGPT chooses decision-relevant roots/secondaries.
   Bridge Search measures target-region Yandex SERPs.
   ChatGPT classifies page/source composition and user job.

5. AI test-set design
   ChatGPT selects only queries whose AI evidence can change/de-risk a real decision.

6. AI-search observation
   future preferred production hand: official GenSearch.
   consumer Alice observations remain a validation/reference surface where necessary.

7. Evidence merge
   preserve source provenance; never mix observed and inferred fan-out.

8. Decision analysis
   H / A / C / O kept separate;
   compare ordinary Search job vs AI job;
   identify source/content gaps and commercial fit.

9. Semantic/page rebuild
   ChatGPT chooses existing page / new page / FAQ / comparison / guide / product fact / reject.
   Resolve cannibalization and role conflicts.

10. Client deliverables
   semantic workbook;
   Search-vs-AI intent-gap matrix;
   source/competitor map;
   page architecture;
   prioritized actions;
   methodology/evidence notes;
   optional content briefs.

11. Post-launch validation
   Webmaster ordinary search;
   AI visibility/SoV when a stable acquisition/import path is available;
   Metrika behavior/conversion;
   revise recommendations when evidence contradicts the initial hypothesis.
```

## 12. Recommended client artifact

Suggested core fields:

```text
query
cluster
human-demand evidence
ordinary Search job
ordinary leading source/page types
AI evidence provenance
AI job
AI source domains/pages
refined/fan-out query evidence
H
A
C
O
current page
recommended page job
action
priority
confidence
notes
```

The valuable deliverable is not only the keyword list, but the traceable reason for the architecture/action.

## 13. Product position relative to Phase 6

Do not replace the mass-market Semantic Core Builder with O-001.

Tiered architecture:

```text
BASE
Semantic Core Builder
= Wordstat + ordinary Search where useful
+ ChatGPT cleanup/grouping/page mapping

PREMIUM CANDIDATE
AI-Native Semantic Rebuild
= BASE
+ selected AI-search evidence
+ Search-vs-AI job gaps
+ source competition
+ H/A/C/O
+ AI-aware page jobs
+ post-launch AI visibility measurement when available
```

Phase 6 may proceed now because it productizes the shared market-proven hands. AI-specific engineering waits for comparative proof.

## 14. Commercial boundaries

Never promise:

- guaranteed Alice/AI indexing;
- guaranteed source inclusion;
- guaranteed SoV/ranking growth;
- guaranteed traffic/sales;
- that one AI response is permanently reproducible;
- that GenSearch exactly equals consumer Alice;
- that source array order is a ranking;
- that high Wordstat demand implies high AI importance;
- that high AI importance automatically requires a new page.

Promise only:

- declared evidence collection methodology;
- transparent semantic/page decisions based on captured evidence;
- concrete recommended actions;
- before/after measurement where data exists;
- revision when new evidence contradicts the hypothesis.

## 15. Current verdict

```text
strategic/service hypothesis = YES / STRONG
market differentiation signal = STRONG
premium incremental decision value = UNPROVEN until comparative gate
current base data primitives = MOSTLY AVAILABLE
repeatable official AI-search path = FOUND (GenSearch)
GenSearch implementation = NOT YET AUTHORIZED
current commercial position = EXPERIMENTAL PREMIUM HYPOTHESIS
```

Next AI-specific decision:

```text
clean independent blood_sand Pass A
→ freeze
→ Pass B
→ compare
→ if material uplift: validate GenSearch vs canonical Alice and promote implementation
→ if no uplift: keep AI-specific hand lower priority
```

Meanwhile Phase 6 Semantic Core / batch orchestration continues independently.