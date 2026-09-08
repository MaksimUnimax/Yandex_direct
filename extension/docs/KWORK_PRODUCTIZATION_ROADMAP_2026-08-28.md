# KWORK PRODUCTIZATION ROADMAP

Date: 2026-08-28
Updated: 2026-09-08
Status: **ACTIVE PRODUCTIZATION ROADMAP / OWNER-DIRECTED KW002 SWITCH**
Branch: `roadmap/kwork-productization-2026-08-28`

## 1. Permanent worker model

```text
ChatGPT Plus
= analyst / research planner / semantic architect / decision-maker / client-artifact author / QA

Yandex Marketing Bridge
= controlled authenticated hands for provider acquisition, persistence, batching, policy, recovery and delivery

ChatGPT Work
= large-data execution environment used only under the owner-approved Work handoff rule and owner-supplied prompt

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

## 3. Per-Kwork documentation architecture

Every implemented Kwork must keep three distinct stores:

```text
LEVEL 1 = universal cross-step rules for the Kwork
LEVEL 2 = universal rules/methods for individual roadmap steps
work/<JOB_ID>/ = concrete client/test order data, evidence, status and deliverables
```

Concrete job data must not be copied into Level 1 or Level 2 as permanent inputs. Reusable lessons may be promoted only after owner authorization and after case-specific values are removed/parameterized.

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
public competitor-page review as a semantic-discovery source
competitor-derived Wordstat expansion
current Yandex query → competitor domain/URL visibility evidence
Webmaster where client access exists
Metrika where client access exists
Direct where relevant and available
official GenSearch
accepted O-001 comparative methodology
accepted GenSearch proxy validation
```

KW-001 includes a required competitor semantic expansion layer before final semantic cleanup/freeze.

Current state:

```text
technical rehearsal evidence exists
Step5A technical validation = PASS
owner review / final commercial productization = still open
READY_TO_SELL = false
```

Status: **PAUSED_AT_OWNER_REVIEW / NOT COMPLETE / NOT READY_TO_SELL**

Owner decision on 2026-09-08 explicitly pauses KW-001 productization so that KW-002 can be developed and rehearsed on a clean greenfield commercial-catalog case. This is a sequencing override, not a claim that KW-001 passed final acceptance.

#### KW-002 — Greenfield semantic core + clustering + site architecture

Working title:

`Соберу с нуля семантическое ядро и структуру сайта под современный Яндекс — обычная выдача + Алиса AI`

Core commercial goal:

```text
client business / assortment / region
→ discover real Yandex demand from scratch
→ expand coverage through real Yandex-search competitors
→ clean and classify demand
→ acquire current ordinary Yandex SERP evidence
→ cluster by user task + intent + SERP similarity
→ assign one primary page owner for each retained cluster
→ freeze Search-only site architecture
→ use bounded AI-search evidence to test whether the modern Yandex generative experience changes, enriches or de-risks page-job decisions
→ reconcile Search + AI-search evidence
→ produce final semantic core + query-to-page map + site structure + Page Jobs + client-ready artifacts
```

Important wording boundary:

```text
AI-SEARCH EVIDENCE != ASKING ALICE FOR SEO ADVICE
```

The product studies how Yandex Search and Yandex generative answers represent user tasks and source/page types. It does not treat a conversational assistant as an SEO consultant.

No universal final-keyword cap is defined. Scope is frozen per order. Provider/job batch limits are technical chunk sizes only and may require multiple batches; they are not a product-level semantic limit.

Core hands:

```text
Wordstat batch
ordinary Search batch / TOP evidence
TOP/domain overlap projections
public competitor-page semantic discovery
competitor-derived Wordstat expansion
ChatGPT cleanup / intent / user-task analysis / clustering judgment
page ownership / query-to-page mapping
Search-only IA freeze
bounded GenSearch / AI-search evidence when decision-relevant
Search-vs-AI reconciliation
artifact generation
ChatGPT Work for large datasets under the owner-approved handoff rule
```

Test case selected:

```text
Blood & Sand = clean greenfield commercial-catalog rehearsal
prior Blood & Sand SEO research = SEALED / not an execution input
only minimum client-like business facts + raw current assortment inputs are allowed before final freeze
```

Status: **ACTIVE / OWNER-DIRECTED FIRST IMPLEMENTATION**

#### KW-003 — Yandex SERP clustering

Working title:

`Кластеризую ключи по реальному ТОПу Яндекса и распределю по страницам`

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

KW-003 remains a separately sellable standalone clustering product. The fact that KW-002 uses SERP evidence internally does not eliminate KW-003 as an independent service for clients who already have a keyword set.

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

KW-004 remains a separate, broader niche/competitor opportunity product. The bounded competitor-semantic loop inside KW-002 exists to improve semantic coverage and does not silently import a full competitor SEO audit.

Status: `QUEUED_AFTER_KW-003`

### WAVE B — commercially promising, but current Bridge slice is insufficient

#### KW-005 — Full Yandex Direct + Metrika audit
Status: `REQUIRES_PRODUCT_GAP_WORK`

#### KW-006 — Recurring Yandex Direct optimization / analyst loop
Status: `REQUIRES_PRODUCT_GAP_WORK`

#### KW-007 — Exact-frequency enrichment for large keyword sets
Status: `REQUIRES_PROVIDER_CONTRACT_RESEARCH`

#### KW-008 — Competitor keyword-gap analysis from client export
Status: `REQUIRES_IMPORT_WORKFLOW`

## 5. Explicitly out of this roadmap

```text
Google provider development = deferred / separate future decision
technical SEO / crawler audit = excluded by owner decision
mandatory paid reverse-domain competitor provider for KW-002 = not authorized
artificial universal keyword-count cap for KW-002 = forbidden
```

## 6. Active sequencing rule

Normally only one Kwork is active for productization at a time.

Current owner-directed sequence:

```text
KW-001 = PAUSED_AT_OWNER_REVIEW
KW-002 = ACTIVE
→ complete KW-002 documentation + Blood & Sand greenfield rehearsal + deliverables + revision + productization measurement + owner review
→ then owner decides whether to return to KW-001 finalization or continue to KW-003
```

This override must remain explicit so a paused Kwork is never misreported as complete.

## 7. Test-project philosophy

A test project must be treated like a real client order:

```text
mock/client-like brief written before analysis
scope frozen before work
inputs frozen
prior research sealed when the goal is a from-scratch rehearsal
provider requests accounted
all assumptions marked
client deliverables actually built
final delivery message written
revision scenario tested
```

A prior project may be reused as a test business, but previous analytical conclusions must not silently replace the current test order's recorded inputs.

## 8. Large-data Work rule

When a step requires large-table processing or complete multi-file analysis that cannot be handled reliably in the ordinary chat context, ChatGPT must not sample, truncate or compress the job merely to fit the conversation.

Instead:

```text
identify the exact large-data execution unit
→ freeze allowed input paths and prohibited sources
→ use the owner-supplied canonical ChatGPT Work prompt
→ execute the large-data unit in Work
→ return the produced artifacts/results
→ independently verify counts/provenance/QA in the main workflow
→ persist/read back before continuing
```

The owner supplies and controls the canonical Work prompt. ChatGPT must not invent a replacement prompt once the owner has supplied the canonical one.

## 9. Final acceptance question for every Kwork

Before `READY_TO_SELL`, answer YES to all:

```text
Can ChatGPT execute the job from the runbook in a clean context?
Does Bridge provide every promised external fact/evidence surface?
Can large-data steps be handed to Work without losing source/provenance/QA requirements?
Are owner actions explicit and minimal?
Is every deliverable actually producible?
Are price/scope consistent with measured effort and provider cost?
Are non-guarantees and unsupported claims excluded?
Do we know what to do when evidence is missing/ambiguous?
Can a real order be started without redesigning the methodology?
```

If any answer is NO, the Kwork remains `NOT_READY_TO_SELL`.

## 10. Current next action

```text
ACTIVE = KW-002 Greenfield Semantic Core + Site Architecture
TEST = Blood & Sand
NEXT = materialize KW-002 Level 1 common rules + Level 2 step methods + isolated Blood & Sand work/<JOB_ID>/ manifest/flow, then begin Step 0 only after owner review of the prepared roadmap
```
