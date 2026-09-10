# MK02 — CLIENT INPUT CONTRACT

Status: **PHASE 2 CLIENT INPUT CONTRACT DEFINED / REHEARSAL VALIDATION PENDING**

Working product identity:

**«Семантическое ядро + SEO-структура сайта + ТЗ на доработку»**

This contract defines what must be known before MK02 starts, what is optional, what can block only individual implementation recommendations, and what must never be invented.

## 1. Base-mode eligibility

Current MK02 V1 is designed for an **existing public website**.

Required eligibility:

```text
PUBLIC WEBSITE EXISTS = true
PUBLIC SITE CAN BE READ = true
ONE PRIMARY REGION CAN BE NAMED = true
CLIENT CAN CONFIRM BUSINESS SCOPE = true
CLIENT CAN STATE KNOWN STRUCTURAL/BUSINESS CONSTRAINTS OR EXPLICITLY STATE NONE KNOWN = true
```

A greenfield/no-site project is not silently processed as existing-site MK02.

## 2. Required client inputs before semantic acquisition

### R1. Exact public website URL

Why required:

- current business/site vocabulary;
- page ownership;
- current-vs-target architecture comparison;
- current literal internal-link/topology checks;
- implementation-location context.

### R2. Primary Yandex region

The analyst must not infer the commercial region from domain, address or intuition.

Base V1 assumes one primary region until Phase 8 proves/prices otherwise.

### R3. Included products/services/business directions

Client provides a short list or explicitly confirms that the current public offer is the intended research scope, with corrections.

A public page can exist without being a current business priority; demand cannot define the business by itself.

### R4. Explicit exclusions

Client states what must not be included even if related search demand exists, for example:

- services/products not sold;
- unsupported geography;
- B2B/B2C boundary;
- brands/materials/categories intentionally excluded;
- DIY/information tasks not wanted as acquisition targets;
- discontinued or temporary offerings.

If none are known, the client explicitly confirms `NONE KNOWN`.

### R5. Business purpose / primary client action

Plain-language confirmation of what the site sells/does and what the visitor should normally do: order, request quote, book, call, submit form, buy, etc.

This is required because a technically truthful topic is not automatically a desirable standalone page or user path.

### R6. Known site-change constraints / protected elements

The client must state known material restrictions, if any, before architecture decisions are finalized.

Examples:

- URLs that cannot be changed for business/technical reasons;
- mandatory legal/service pages;
- product categories that must remain separate;
- forms/calculators/pricing blocks that must remain available;
- pages controlled by another system/team;
- navigation constraints;
- planned redesign/migration already approved;
- contractual/brand restrictions.

If no restrictions are known, client may state `NONE KNOWN`.

Important:

```text
NO CONSTRAINTS REPORTED
!= PROOF THAT NO TECHNICAL CONSTRAINTS EXIST
```

Unknown implementation constraints are preserved as uncertainty when material.

## 3. Optional but useful client inputs

### O1. Existing semantic core

Useful for vocabulary/coverage comparison only.

```text
CLIENT SEMANTIC CORE != VERIFIED CURRENT YANDEX DEMAND
CLIENT CLUSTER != FINAL MK02 CLUSTER
CLIENT PAGE MAPPING != CURRENT OWNER AUTHORITY
```

MK02 includes its own semantic research in base scope.

### O2. Existing SEO structure / sitemap / page map

Useful for reconciliation, but current public discovery still governs current-site claims.

```text
CLIENT PAGE LIST != COMPLETE CURRENT SITE PROOF
OLD SITEMAP != CURRENT HTML TOPOLOGY
```

### O3. Known competitors

Optional context only. Base MK02 does not silently activate competitor-derived Step5A expansion or a full competitor audit.

### O4. Yandex Webmaster delegated access

Optional in base-public mode.

It may materially strengthen query×URL/history diagnosis where available and explicitly used, but its absence does not block the whole base MK02.

If historical first-party evidence is unavailable:

- current public page/Search evidence may still support bounded architecture decisions;
- strong historical harmful-cannibalization claims remain unavailable;
- affected destructive decisions stay bounded/deferred where history is required.

Do not request the client's account password.

### O5. Yandex Metrika data

Optional. Useful only if separately authorized and relevant to business/measurement calibration.

Not required to decide basic semantic/page architecture.

### O6. CMS/platform/technical stack

Useful examples:

- WordPress;
- Bitrix;
- Tilda;
- custom CMS;
- headless framework;
- unknown.

Not a universal pre-start blocker. However, a READY task whose exact mechanism depends on platform-specific facts cannot invent them. It must either remain technology-neutral where sufficient or move to clarification.

### O7. Developer/implementer constraints and estimates

Optional for implementation specification; required only for a stronger implementation schedule/order if that is separately promised.

Useful fields:

- responsible role/team;
- effort estimate;
- deployment limitations;
- capacity/timeline;
- release process.

Without these:

```text
IMPLEMENTATION SPEC MAY BE READY
IMPLEMENTATION SCHEDULE MAY NOT BE CLAIMED READY
```

### O8. Client business priority / margin / capacity

Optional.

Public business relevance may support analytical importance, but it is not a substitute for client-confirmed margin, lead value or internal priority.

## 4. Inputs not required in base scope

The client is not required to provide:

- Yandex account password;
- Google account access;
- Google Search Console;
- Google Analytics;
- Google Keyword Planner/Ads exports;
- Yandex Direct access;
- Metrika access;
- hosting/server password;
- source-code repository access;
- CMS administrator password.

If optional private Yandex evidence is justified, use delegated least-privilege access under the parent KW-001 policy, never shared passwords/tokens.

## 5. Google data policy

MK02 is Yandex-only.

Google-origin keyword/page information may be accepted as unverified contextual input, but it cannot be represented as Yandex demand/Search evidence without passing the Yandex method.

```text
GOOGLE DATA != YANDEX EVIDENCE
```

Final architecture/TZ claims must not mix Google rankings/frequency into Yandex conclusions.

## 6. Pre-start Level-2 order record

Before provider acquisition, persist at minimum:

```text
site_url
site_state = existing_public_site
primary_region
business_description
primary_conversion_goal
included_directions
excluded_directions
known_site_change_constraints
protected_pages_or_elements
existing_semantic_core_state
existing_structure_or_sitemap_state
competitors_supplied_state
private_yandex_access_state
cms_platform_state
implementer_constraints_state
client_business_priority_state
product = MK02
requested_result = semantic core + page ownership + target architecture + evidence-supported implementation specifications
frozen_timestamp
unresolved_client_questions
```

## 7. Missing-input behavior

### Missing/inaccessible public site

```text
MK02 BASE START = BLOCKED
```

Because current-page ownership and current topology cannot be truthfully evaluated.

### Missing region

```text
WORDSTAT ACQUISITION = BLOCKED
```

### Unclear business scope

Do not collect unlimited adjacent demand or let current page inventory define the business silently.

### Known structural restriction unclear

If it can affect a material architecture action, the action cannot be finalized until clarified or explicitly preserved as pending.

### No existing semantic core

Not a blocker. MK02 includes collection.

### No competitor list

Not a blocker. Competitor expansion is outside base.

### No Webmaster/Metrika/Direct access

Not a blocker for base-public mode.

### No CMS/platform information

Not a blocker for evidence-backed platform-neutral tasks. A task requiring platform-specific implementation detail becomes `PENDING_TECHNICAL_DETAIL` or equivalent until resolved.

### No developer effort/owner/capacity estimate

Does not block implementation-specification readiness when the change itself is fully specified. It blocks any stronger claim of a production-ready schedule/order that depends on those inputs.

### Contradictory client vs public-site facts

Do not silently choose the convenient version.

Record the conflict, distinguish public observable fact from business policy, and keep affected architecture/action claims pending until the material contradiction is resolved.

## 8. Business-detail gate for READY actions

Company-specific claims such as exact service inclusions/exclusions, warranty, installation sequence, materials, delivery/service boundaries or mandatory preparation require direct business evidence.

If missing:

```text
READY = FORBIDDEN
→ CONCRETE CLIENT CLARIFICATION
→ WHAT BECOMES READY AFTER ANSWER
```

This directly prevents the earlier failure where a generic installation topic was over-promoted to a company-specific ready implementation block without evidence.

## 9. Revision boundary after start

Material scope change includes:

- different primary region;
- new business direction outside frozen scope;
- domain/site replacement;
- transition to greenfield/rebuild mode;
- addition of competitor semantic gap research;
- addition of Google;
- addition of AI/Alice/Neuro;
- demand for exhaustive historical cannibalization diagnosis;
- demand for implementation itself rather than specifications;
- major protected-site constraints revealed after architecture freeze.

A material revision is logged; affected evidence/analysis is rerun only where necessary. Existing valid evidence is not erased or blindly recollected.

## 10. Client-facing input wording draft

> Для начала работы пришлите ссылку на действующий сайт, основной регион продвижения, список направлений/услуг, которые нужно учитывать, и то, что точно не входит в работу. Коротко напишите, что продаёт сайт и какое действие должен совершать клиент. Также заранее укажите известные ограничения на изменение структуры: какие страницы, URL, формы, калькуляторы или разделы обязательно нужно сохранить, если такие ограничения есть. Если есть старое семантическое ядро, sitemap/структура, доступ к Яндекс Вебмастеру или информация о CMS — можно приложить, но для базового старта это необязательно. Пароли от аккаунтов не нужны. Работа выполняется по Яндексу; Google в базовый продукт не входит.

## 11. Phase-2 PASS gate

MK02 may enter normal acquisition/analysis only when:

```text
PUBLIC_SITE_URL_CONFIRMED = true
PUBLIC_SITE_READABLE = true
PRIMARY_REGION_CONFIRMED = true
BUSINESS/CONVERSION_JOB_CONFIRMED = true
INCLUDED_DIRECTIONS_CONFIRMED = true
EXCLUSIONS_CONFIRMED_OR_NONE = true
KNOWN_SITE_CHANGE_CONSTRAINTS_CONFIRMED_OR_NONE_KNOWN = true
YANDEX_ONLY_SCOPE_ACKNOWLEDGED = true
NO_REQUIRED_GOOGLE_INPUTS = true
NO_PASSWORD/SECRET_DEPENDENCY = true
ORDER_FREEZE_PERSISTED = true
```

Optional private/technical/implementation inputs change only the claim modes they actually govern; they are not silently assumed.
