# KW-001 — AI-Native Semantic Rebuild: implementation plan

Updated: 2026-09-08  
Status: **ACTIVE / COMMERCIAL END-TO-END REHEARSAL REQUIRED / UNIVERSAL PRODUCT PLAN**

This is the permanent productization plan. Concrete rehearsal/client names, domains, case-specific results and current job progress belong in Level2.

## 1. Working Kwork

Title:

`Пересоберу семантику сайта под Яндекс и Алису AI — обычный + генеративный поиск`

### 1.1 Canonical product goal — DO NOT REFRAME

**Цель кворка: пересобрать и проверить поисковое/семантическое ядро сайта ПОД АЛИСУ, то есть под современную выдачу Яндекса, где часть поискового ответа формируется Алисой, при одновременном сохранении корректности для обычной выдачи Яндекса.**

Это не `обычное SEO + дополнительная проверка Алисы` и не `обычный аудит сайта, после которого несколько запросов посмотрели в Алисе`.

Коммерческий смысл продукта:

```text
НОВАЯ ПОИСКОВАЯ РЕАЛЬНОСТЬ
= обычная выдача Яндекса + выдача/ответы Алисы как часть поискового опыта

ЦЕЛЬ КВОРКА
= пересобрать / перепроверить ядро сайта под эту новую реальность

ОБЯЗАТЕЛЬНЫЙ РЕЗУЛЬТАТ ИССЛЕДОВАНИЯ
= понять, как собранный спрос и его распределение по страницам соответствуют ОБЫЧНОЙ ВЫДАЧЕ И ВЫДАЧЕ АЛИСЫ,
  и какие изменения нужны именно с учётом Алисы

ВОЗМОЖНЫЙ И НОРМАЛЬНЫЙ ВЫВОД
= существующее ядро и структура уже в целом хорошо подходят под обе выдачи;
  тогда полная переделка не требуется, а внедряются только доказанные точечные изменения
```

Критически важно различать **цель кворка** и **результат конкретного исследования**:

```text
ЦЕЛЬ КВОРКА = ЯДРО ПОД АЛИСУ / ПОД НОВОЕ ВРЕМЯ ПОИСКА

РЕЗУЛЬТАТ КОНКРЕТНОГО САЙТА МОЖЕТ БЫТЬ =
УЖЕ ХОРОШО СООТВЕТСТВУЕТ И ОБЫЧНОЙ ВЫДАЧЕ, И ВЫДАЧЕ АЛИСЫ;
ПОЛНАЯ ПЕРЕСБОРКА СУЩЕСТВУЮЩЕЙ СТРУКТУРЫ НЕ НУЖНА;
НУЖНЫ ТОЧЕЧНЫЕ УЛУЧШЕНИЯ
```

Alice must therefore never be described in customer-facing positioning as merely `additional`, `optional`, `after the main SEO work`, or a minor post-check. Bounded/selective Alice checks are an **execution method** for making the Alice-native semantic decision efficiently; they do not downgrade Alice from the **core commercial objective**.

Initial test price:

`7,500 RUB`

Initial delivery target:

`4–5 days`

This price/scope is provisional until sufficiently different end-to-end rehearsals measure real work time, operator burden and provider cost.

## 2. What the product must be able to do

The reusable product capability must support:

```text
business/site understanding
human-demand evidence from Yandex Wordstat
competitor-derived semantic discovery from real Yandex-search competitors
Wordstat expansion of genuinely new competitor-derived topics/seeds
current Yandex query → competitor domain/URL visibility evidence
ordinary Yandex Search evidence
Alice / GenSearch evidence sufficient to evaluate the core for the new Yandex search experience
semantic cleanup/grouping
Search-vs-Alice comparison
page-job decisions
source/competitor observations
prioritized recommendations
client workbook/report
```

The competitor layer is a bounded semantic-coverage mechanism, not a deep competitor SEO audit. It must remain executable without a mandatory third-party reverse-domain database. External reverse-domain data may be optional enrichment only when independently available/authorized.

The workflow may use a bounded diagnostic/control sample rather than bulk-running every phrase through Alice. This is an efficiency and evidence-design choice only. It must never be presented as meaning that Alice is secondary to the product.

Optional account evidence such as Webmaster/Metrika/Direct may be used only when actually available and governed by `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`. It must not be silently required for the base-package promise.

## 3. Explicit non-promises

Never promise:

```text
guaranteed Alice inclusion/citation
guaranteed AI visibility
guaranteed Yandex position
guaranteed traffic/leads/revenue
GenSearch == consumer Alice
source order == ranking
AI evidence must always change the SEO decision
competitor page topic == competitor ranks for that exact query
complete enumeration of every organic keyword of a competitor without evidence that supports that scope
```

A valid outcome may be `NO_CHANGE`: Alice evidence can confirm that the existing semantic/page decision is already suitable for the new search experience.

A valid competitor-expansion outcome may also be that the second independent competitor route adds little or no material in-scope demand. The method must report that truth rather than force artificial additions.

## 4. Rehearsal diversity requirement

Before READY_TO_SELL, execute at least two materially different test orders.

Preferred generic profiles:

### Test A — commercial catalog / product family

```text
multiple related product/category intents
existing public pages
meaning/selection/compatibility questions where AI could plausibly differ from transactional Search
observable Yandex demand
```

Purpose: stress commercial vs explanatory/hybrid page-job decisions.

### Test B — service or mixed information-commerce business

```text
clear commercial conversion goal
informational questions around the service/product
existing public competitor/source landscape
observable Yandex demand
```

Purpose: demonstrate that the method is not overfit to one domain, vocabulary or site architecture.

`STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md` has completed its required project-test validation and is now a permanent approved KW-001 method. Future varied rehearsals must continue to exercise it as regression/portability/economics evidence, but permanent Step5A promotion no longer depends on another first-execution gate.

Any prior project/test may remain historical regression evidence in Git history/Level2, but no concrete test identity is a permanent method input.

## 5. Mock-client order freeze

Before analysing each test site, create a Level2 test-order record containing:

```text
site URL
business description
region
client goal
base package purchased
known pages/categories
known exclusions
competitors supplied or NONE
requested output
assumed client questions
frozen timestamp
private-access state
```

Do not alter the brief after seeing provider evidence merely to make the result look better. Any real revision is logged as a client revision.

Client-supplied competitors are hints. The workflow must still distinguish business rivals from the domains that actually compete in current Yandex results for the researched demand.

## 6. End-to-end rehearsal sequence

The active detailed step order is governed by `STEP_RULES_INDEX.md` and current step-method authorities. This section states the product-level intent, not a competing roadmap.

### Intake / scope

Freeze offer, audience, conversion jobs, regions, existing page roles, exclusions and unresolved client questions.

### Demand acquisition

Use bounded seed/probe logic, acquire Wordstat evidence under Bridge durability rules, preserve complete required results and account cost.

### Step5A — competitor semantic expansion

Use `STEP_05A_COMPETITOR_SEMANTIC_EXPANSION_METHOD.md`.

Step5A is an **APPROVED / ACTIVE permanent acquisition-coverage stage** in the default KW-001 roadmap. Execute it after initial Wordstat acquisition/targeted expansion and before final semantic cleanup/freeze. If a required evidence route is genuinely unavailable, preserve the blocker explicitly rather than silently skipping the stage.

This stage is an **additional acquisition/coverage loop**, not a substitute for the original demand collection and not a full competitor audit.

Canonical product-level flow:

```text
initial acquired semantic set
→ current Yandex Search on representative in-scope query families
→ identify real recurring organic competitors
→ inspect evidence-bearing competitor URLs/pages for missed topics/seeds
→ compare those topics with already acquired demand
→ genuinely new competitor-derived seeds go to Wordstat
→ preserve every returned occurrence under the same union-compatible acquisition model as Step3/Step5
→ current Yandex Search rechecks material new candidate queries/families
→ business/scope fit + Wordstat demand + current Search evidence drive ADD / ALREADY_COVERED / REJECT / HOLD
→ confirmed additions merge into the same semantic pipeline before final cleanup/freeze
```

Critical boundaries:

```text
COMPETITOR PAGE TOPIC != EXACT QUERY RANKING
COMPETITOR RANKING != AUTOMATIC KEYWORD ACCEPTANCE
COMPETITOR-DERIVED SEED != FINAL KEYWORD
COMPETITOR EXPANSION != DEEP COMPETITOR SEO AUDIT
TESTED QUERY VISIBILITY != FULL COMPETITOR KEYWORD UNIVERSE
```

External reverse-domain databases/exports are optional enrichment only. They must not become a silent base-package dependency.

### Ordinary Search baseline

Acquire current Search evidence only for decision-relevant roots/boundaries and preserve exact provenance.

Search calls used inside Step5A for competitor discovery/confirmation have a different acquisition purpose and do not remove the later requirement to obtain the ordinary Search evidence required by downstream semantic/page decisions.

### Search-only semantic/page architecture

Before Alice evidence can influence the result:

```text
clean/group demand, including confirmed competitor-derived additions
resolve user tasks
map current page ownership
build evidence-backed structural/content actions
check competing-page boundaries within evidence mode
freeze Search-only architecture against current-site evidence
```

This Search-only freeze is a **causal-control method**, not the commercial end-goal. The sold goal remains the semantic-core decision under the combined modern Yandex environment, including Alice.

### Alice diagnostic design and acquisition

Select a bounded diagnostic/control set under the current Step15 method, acquire the preserved Alice/GenSearch evidence under the current Step16 gate, then compare ordinary Search and Alice under Step17 claim limits.

Do not bulk-run the semantic core through Alice merely because the provider is available. The bounded set must still be sufficient to answer the sold question: **does the semantic/page architecture remain appropriate when Alice is part of the search experience, and what must change if it does not?**

### Step18 — prioritization and implementation readiness

Use `STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md`.

The product must preserve two distinct layers:

```text
IDEAL_ANALYTICAL_PRIORITY
= evidence-based importance/order from demand, user task, public business relevance, Search opportunity, risk, evidence, dependencies and uncertainty.

EXPECTED_IMPLEMENTATION_PRIORITY
= real execution order after owner, effort, capacity, delivery window, client business importance and measurement readiness are calibrated when the deliverable requires an implementation-ready roadmap.
```

Canonical boundary:

```text
IDEAL_ANALYTICAL_PRIORITY != IMPLEMENTATION_READY_ORDER
```

Do not collapse human demand, Alice diagnostic value, commercial/business value, evidence confidence or implementation effort into an unexplained magic score.

If owner/effort/capacity/business-priority inputs are unavailable and the sold scope is analytical recommendations, preserve `PENDING_CALIBRATION` rather than fabricate them.

### Client deliverables

The rehearsal must actually produce the sellable artifacts, not merely describe them.

Minimum base-package artifact classes:

```text
1. semantic/page map workbook
2. Search-vs-Alice gap matrix
3. competitor/source map including competitor-derived semantic gaps and their evidence state
4. prioritized action plan
5. methodology/limitations sheet
6. final client delivery message
```

The competitor/source view must explain in recipient language:

```text
which domains were treated as real search competitors and why
which additional topics/seeds came from competitor evidence
which new Wordstat demand was found
which tested competitor/query relationships were actually confirmed in current Yandex results
which candidates were added / already covered / rejected / held
which downstream cluster/page decisions changed because of that evidence
```

Confirmed competitor-derived phrases must also exist in the common semantic core; they may not live only in a separate competitor worksheet.

Where an implementation-ready roadmap is promised, add calibrated work packages, ownership, effort/capacity, delivery waves and measurement plan.

### Final QA

Check at minimum:

```text
Kwork goal remains explicit: semantic core under Alice / modern Yandex search
Alice is not reframed as an optional/additional afterthought
competitor semantic expansion executed or explicitly blocked with evidence before semantic freeze
competitor page topic is never presented as exact-query ranking without Search evidence
no claim of full competitor keyword-universe coverage without a supporting reverse-domain/index evidence route
external reverse-domain provider is not silently required for the base package
competitor-derived Wordstat rows preserve complete Step3/Step5-compatible provenance
confirmed competitor additions are merged into the common core rather than isolated in a decorative worksheet
no invented provider facts
provider region/scope/provenance correct
no GenSearch==consumer-Alice overclaim
no guaranteed outcomes
no orphan important task
no unsupported new-page/destructive recommendation
no current-site completeness claim from a closed old list
no implementation-ready claim without required calibration
no accounting batch presented as an executable work item
client can understand next actions without reading raw evidence
files open and reconcile
```

### Economics / operator burden

Measure:

```text
ChatGPT work stages / approximate effort
initial provider requests + estimated cost
additional Step5A Search/Wordstat requests + estimated cost
competitor public-page review burden
owner/operator actions required
elapsed wall-clock constraints
revision-sensitive stages
implementation-calibration burden where included
```

Use observations to confirm/revise package price, scope and limits. Step5A must be measured specifically because it is an approved additional coverage layer and may materially affect the 7,500 RUB / 4–5 day provisional economics.

### Simulated client revision

Every test must include one realistic revision such as product/service scope correction, changed priority, geography clarification or rejection of a proposed action.

Re-run only affected reasoning/evidence where justified. Prove the workflow can revise without replaying unrelated paid provider work or rewriting history.

## 7. Test evidence files

For each accepted test project create equivalent Level2 artifacts:

```text
TEST_ORDER_<id>.md
TEST_EXECUTION_<id>.md
TEST_DELIVERABLE_INDEX_<id>.md
TEST_ECONOMICS_<id>.md
TEST_REVISION_<id>.md
```

When Step5A is executed, its competitor discovery, page evidence, derived seeds, Wordstat occurrences, query-visibility checks and merge reconciliation must also be durably represented in Level2 evidence. They may be separate files or equivalent sections/tables as long as lineage and counts are auditable.

Never store credentials/secrets.

## 8. Card finalization after tests

Only after accepted varied test runs freeze:

```text
final Kwork title
final description
exact base-package limits
exact required client inputs
final delivery time
final base price
add-on menu
portfolio/demo screenshots/artifacts
FAQ
non-guarantee language
```

Marketing copy must be derived from observed workflow truth and must preserve the Alice-native commercial objective.

The final card may mention competitor-semantic checking only at the depth actually validated in rehearsals. It must not market the narrow Step5A layer as a full competitor SEO audit or as complete reverse-domain keyword recovery.

## 9. Final autonomous runbook

The final runbook must satisfy `extension/docs/KWORK_RUNBOOK_STANDARD_2026-08-28.md`, current Level1 rules and a clean-context rehearsal.

The runbook must include Step5A in the executable order and preserve its claim boundaries before `KW001_CLEAN_CONTEXT_RUNBOOK_REHEARSAL_PASS` can pass.

## 10. Product acceptance markers

```text
KW001_TEST_A_END_TO_END_PASS
KW001_TEST_B_END_TO_END_PASS
KW001_COMPETITOR_SEMANTIC_EXPANSION_REHEARSAL_PASS
KW001_DELIVERABLE_SET_PASS
KW001_REVISION_FLOW_PASS
KW001_ECONOMICS_RECORDED
KW001_FINAL_CARD_FROZEN
KW001_CLEAN_CONTEXT_RUNBOOK_REHEARSAL_PASS
KW001_READY_TO_SELL
```

All are required before READY_TO_SELL.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.