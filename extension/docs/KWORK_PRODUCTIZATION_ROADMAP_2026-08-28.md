# KWORK PRODUCTIZATION ROADMAP

Date: 2026-08-28
Status: **ACTIVE PRODUCTIZATION ROADMAP / NO PRODUCT BYTE CHANGE**
Branch: `roadmap/kwork-productization-2026-08-28`

## 1. Permanent worker model

```text
ChatGPT Plus
= analyst / research planner / semantic architect / decision-maker / client-artifact author / QA

Yandex Marketing Bridge
= controlled authenticated hands for provider acquisition, persistence, batching, policy, recovery and delivery

Human owner/operator
= authorization boundary / local operator / irreducible live actions / commercial owner
```

The goal is not to publish generic Kwork cards. Each Kwork must become a rehearsed product that this worker model can execute repeatedly with minimal improvisation.

## 2. Definition of IMPLEMENTED Kwork

A Kwork is `READY_TO_SELL` only after all of the following are complete:

```text
1. Market promise frozen
2. Exact service boundary frozen
3. Client intake defined
4. Full execution logic defined
5. Test-project set selected
6. At least one complete end-to-end dry run executed; normally two materially different test projects are preferred
7. Real Bridge/provider path exercised where required under normal safety/cost rules
8. Final client deliverables actually produced
9. Time / provider cost / operator actions measured
10. Failure cases and ambiguity handling recorded
11. Kwork title/description/price/options revised from observed execution truth
12. Portfolio/sample artifact prepared and clearly labeled as test/demo where applicable
13. Self-contained ChatGPT runbook written
14. New-context rehearsal proves the runbook is sufficient without relying on chat memory
15. Final owner review
```

Writing a card is not implementation. Existing technical tests are supporting evidence, not a substitute for a commercial end-to-end rehearsal.

## 3. Per-Kwork permanent artifact set

Every implemented Kwork receives a folder:

```text
extension/docs/kwork/<KW-ID>/
  PRODUCT_CARD.md
  TEST_PLAN.md
  TEST_RUN_<project>.md
  SAMPLE_DELIVERABLES.md
  ECONOMICS_AND_LIMITS.md
  RUNBOOK_FOR_CHATGPT.md
  FINAL_ACCEPTANCE.md
```

`RUNBOOK_FOR_CHATGPT.md` is created/frozen only after the real workflow has been exercised and corrected.

The runbook must allow ChatGPT in a clean new conversation to understand the order from the document alone.

## 4. Productization order

### WAVE A — works on current accepted Bridge capabilities

#### KW-001 — AI-Native Semantic Rebuild: Yandex + Alice AI

Working Kwork title:

`Пересоберу семантику сайта под Яндекс и Алису AI — обычный + генеративный поиск`

Starting test price: **7,500 RUB**

Current technical basis:

```text
Wordstat + Wordstat batch
ordinary Yandex Search
Search batch / TOP evidence
Webmaster where client access exists
Metrika where client access exists
Direct where relevant and available
official GenSearch
accepted O-001 comparative methodology
accepted GenSearch proxy validation
```

Important: O-001/blood_sand and GenSearch gates prove methodology/provider value. They do **not** by themselves prove the complete Kwork delivery flow. KW-001 therefore starts with a full commercial rehearsal from mock client brief to final workbook/report.

Status: **ACTIVE / FIRST TO IMPLEMENT**

#### KW-002 — Semantic core + page mapping

Working title:

`Соберу семантическое ядро под Яндекс до 500 запросов и распределю по страницам`

Starting test price: **3,000 RUB**

Core hands:

```text
Wordstat batch
ChatGPT cleanup / intent / grouping
page-job / target-page mapping
optional bounded ordinary Search evidence
artifact generation
```

Status: `QUEUED_AFTER_KW-001`

#### KW-003 — Yandex SERP clustering up to 500 keys

Working title:

`Кластеризую до 500 ключей по реальному ТОПу Яндекса и распределю по страницам`

Starting test price: **2,500 RUB**

Core hands:

```text
Search batch
ranked URL/domain evidence
TOP/domain projections
overlap evidence
ChatGPT clustering judgment
page mapping
client workbook
```

Status: `QUEUED_AFTER_KW-002`

#### KW-004 — Yandex niche + competitor opportunity analysis

Working title:

`Проанализирую нишу и конкурентов в Яндексе: спрос, ТОП и точки роста`

Starting test price: **5,000 RUB**

Core hands:

```text
Wordstat
ordinary Search / Search batch
public competitor/site review
selected GenSearch only when decision-relevant
ChatGPT opportunity / priority analysis
client action plan
```

Status: `QUEUED_AFTER_KW-003`

### WAVE B — commercially promising, but current Bridge slice is insufficient

These Kworks are not allowed to be advertised as fully supported until the required capability gate passes.

#### KW-005 — Full Yandex Direct + Metrika audit

Target starting price after implementation: **6,000 RUB**

Missing hands to research/implement include, where official APIs permit:

```text
Direct search-query evidence
placement/network evidence
richer campaign/strategy evidence
performance dimensions below campaign where needed
ad/UTM evidence required by the final audit contract
Metrika goals/conversions
traffic-source/campaign dimensions
UTM dimensions
revenue/e-commerce evidence where available
```

Status: `REQUIRES_PRODUCT_GAP_WORK`

#### KW-006 — Recurring Yandex Direct optimization / analyst loop

Target starting price after implementation: **12,000 RUB/month** for a tightly bounded first package.

First safe model should remain:

```text
Bridge collects evidence
→ ChatGPT produces explicit change plan
→ owner/client applies approved changes
→ Bridge re-measures
→ ChatGPT compares outcome
```

Do not require Direct write automation for the first sellable version.

Depends on KW-005 read-evidence expansion.

Status: `REQUIRES_PRODUCT_GAP_WORK`

#### KW-007 — Exact-frequency enrichment for 5k–10k keywords

Target starting price after implementation/economics validation: **4,000 RUB**

Need official provider-contract research and proof of exact-frequency semantics/economics at scale. Reuse existing durable batch infrastructure if the provider path is valid.

Status: `REQUIRES_PROVIDER_CONTRACT_RESEARCH`

#### KW-008 — Competitor keyword-gap analysis from client export

Target starting price: **4,500 RUB**

Preferred first implementation is importer-first rather than new paid provider integration:

```text
client CSV/XLSX export
→ normalize competitor / keyword / URL / position / frequency fields
→ ChatGPT gap analysis
→ clustering / target-page mapping
→ prioritized client artifact
```

Status: `REQUIRES_IMPORT_WORKFLOW`

## 5. Explicitly out of this roadmap

```text
Google provider development = deferred / separate future decision
technical SEO / crawler audit = excluded by owner decision
more Alice/GenSearch plumbing without a newly proven gap = not authorized
```

## 6. Sequential execution rule

Only one Kwork is active for productization at a time.

```text
KW-001 complete + FINAL_ACCEPTANCE
→ KW-002
→ KW-003
→ KW-004
→ reassess real market/test evidence
→ then begin Wave B capability work in priority order
```

Do not start Wave-B engineering merely because it is listed here. First complete the current-capability offers and learn from their real execution.

## 7. Test-project philosophy

A test project must be treated like a real client order:

```text
synthetic/mock brief written before analysis
scope and price-equivalent package fixed before work
inputs frozen
provider requests accounted
all assumptions marked
client deliverables actually built
final delivery message written
revision scenario tested
```

Whenever practical, use materially different public/test sites so the procedure is not overfit to one niche.

A prior project may be reused as regression evidence, but previous knowledge must not silently replace the current test order's recorded inputs.

## 8. Final acceptance question for every Kwork

Before `READY_TO_SELL`, answer YES to all:

```text
Can ChatGPT execute the job from the runbook in a clean context?
Does Bridge provide every promised external fact/evidence surface?
Are owner actions explicit and minimal?
Is every deliverable actually producible?
Are price/scope consistent with measured effort and provider cost?
Are non-guarantees and unsupported claims excluded?
Do we know what to do when evidence is missing/ambiguous?
Can a real order be started without redesigning the methodology?
```

If any answer is NO, the Kwork remains `NOT_READY_TO_SELL`.

## 9. Current next action

```text
ACTIVE = KW-001 AI-Native Semantic Rebuild
NEXT = create KW-001 implementation package, freeze test-order protocol, select test projects, then run the first complete rehearsal
```
