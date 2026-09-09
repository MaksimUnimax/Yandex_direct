# MK01 — CLIENT INPUT CONTRACT

Status: **FROZEN FOR MK01 PRODUCTIZATION / CARD WORDING PENDING REHEARSAL**

Working Kwork title:

**«Семантическое ядро для сайта: сбор, чистка и кластеризация»**

This file defines what the client must provide before MK01 starts, what is optional, what must never be requested as a base requirement, and how missing/contradictory inputs are handled.

Concrete client values belong in the current Level-2 order record. This file contains only the reusable contract.

---

## 1. Base-mode eligibility

Current validated MK01 base mode is for an **existing public website**.

Required eligibility:

```text
PUBLIC WEBSITE EXISTS = true
PUBLIC SITE CAN BE READ = true
ONE PRIMARY REGION CAN BE NAMED = true
CLIENT CAN DEFINE/CONFIRM THE BUSINESS SCOPE = true
```

If the website does not yet exist, do not silently simulate an existing-site model. That is a different from-scratch/greenfield product and requires its own validated method.

If the site is temporarily inaccessible, the provider/analysis phase does not start until the public business/site model can be established or the product scope is explicitly changed.

---

## 2. Required client inputs before start

The client must provide or explicitly confirm the following.

### R1. Exact public website URL

Required value:

```text
https://example.ru/
```

Why required:

- confirm the business actually represented on the site;
- understand product/service vocabulary;
- avoid collecting demand for things the business does not offer;
- build the current domain profile used during cleaning and clustering.

The URL is an input, not proof that the first discovered page inventory is complete forever.

### R2. Primary promotion / demand region

Examples of the type of answer expected:

- Москва;
- Москва и Московская область;
- Санкт-Петербург;
- Россия;
- another clearly named region.

Why required:

Yandex Wordstat demand must be collected/reported under an explicit regional scope. The analyst must not silently choose a region because it seems obvious from a domain name or address.

Initial MK01 base productization assumes **one primary region**. Multi-region pricing/limits are not silently included and will be frozen later if offered.

### R3. What products/services/directions must be included

Client provides either:

- a short list of the commercial directions to research; or
- confirmation that the public site's current offer is the intended base scope, plus any corrections.

Examples of answer form:

```text
INCLUDE:
- service/product A
- service/product B
- service/product C
```

Why required:

A public page can exist without being a current commercial priority or even without accurately reflecting the client's intended scope. Search demand does not define the business by itself.

### R4. Explicit exclusions

Client states what must not enter the semantic core even if related demand exists.

Examples of exclusion types:

- products/services no longer sold;
- wholesale vs retail boundaries;
- DIY/instructional demand not served by the business;
- geographic areas not served;
- jobs/education/support topics outside the offer;
- brands/materials/categories intentionally excluded.

If there are no known exclusions, the client may explicitly answer `NONE`.

### R5. Short business / conversion confirmation

Client confirms in plain language what the site is trying to sell/do and what the main user action is.

Example answer form:

```text
BUSINESS:
We sell/install ...

PRIMARY CLIENT ACTION:
request a quote / call / order / book / submit a form / other
```

This does not need to be a marketing brief. Its purpose is to prevent semantic decisions from drifting away from the real commercial job.

---

## 3. Inputs that are useful but OPTIONAL

None of the following may block purchase or base execution when absent.

### O1. Existing semantic core / keyword list

Optional formats may include XLSX/CSV/table/text.

Use:

- coverage comparison;
- vocabulary hints;
- identifying known priorities or historical grouping.

Boundary:

```text
CLIENT KEYWORD LIST != VERIFIED YANDEX DEMAND
CLIENT KEYWORD LIST != AUTOMATIC KEEP
CLIENT CLUSTER != AUTOMATIC FINAL CLUSTER
```

Every phrase that enters the governed MK01 result must still satisfy the current Yandex evidence/method rules.

### O2. Known site sections/categories/pages

Useful as orientation but not required because the method reads the current public site.

Boundary:

```text
CLIENT PAGE LIST != COMPLETE CURRENT SITE PROOF
OLDER INVENTORY != CURRENT SITE TRUTH
```

### O3. Competitor list

Optional only.

In MK01 base scope, competitor-derived expansion is excluded. A client-supplied competitor can be recorded as context, but does not trigger a hidden competitor audit or Step5A research.

Deep competitor semantic-gap work belongs to MK03 or a future explicitly priced add-on.

### O4. Internal commercial priorities

Useful examples:

- high-margin directions;
- directions with spare capacity;
- priority services/products;
- directions temporarily paused.

These may help explain/report the semantic result but are not required to prove basic public business relevance.

Boundary:

```text
PUBLIC BUSINESS RELEVANCE != INTERNAL BUSINESS PRIORITY
MISSING INTERNAL PRIORITY != SEMANTIC EVIDENCE ROUTE
```

### O5. Yandex Webmaster access

**Optional. Not required to buy MK01 and not required to execute its base scope.**

Client-facing meaning:

> Доступ к Яндекс Вебмастеру не обязателен. Если доступ уже есть и его использование оправдано конкретной проверкой, он может быть применён как дополнительный источник данных Яндекса, но базовый результат строится без обязательного доступа к кабинету.

Do not ask for the client's Yandex password.

If future delegated access is used, it follows the universal `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` and least-privilege procedure.

### O6. Yandex Metrika / Direct data

Optional enhancement only when separately available, authorized and useful. Not a base requirement.

No private-data absence may be reframed as product failure.

---

## 4. Google data policy

MK01 is Yandex-only.

The client is **not asked** to provide:

- Google Ads / AdWords exports;
- Google Keyword Planner data;
- Google Search Console;
- Google Analytics;
- Google Trends;
- Google SERP exports.

If the client voluntarily supplies a keyword list originally built from Google tools, it may be used only as an **unverified vocabulary hint/input candidate**.

Canonical rule:

```text
GOOGLE-ORIGIN PHRASE
!= VERIFIED YANDEX DEMAND
!= AUTOMATIC MK01 KEEP
```

Before such a phrase is represented as Yandex demand in the MK01 result, it must pass the same approved Yandex validation/acquisition rules as any other candidate.

The final deliverable must not mix Google frequency with Yandex frequency.

---

## 5. What the client must NOT send

Do not request or accept as normal workflow input:

- Yandex account password;
- Google account password;
- raw session cookies;
- OAuth refresh/access tokens pasted into chat/documents;
- API secrets;
- server/hosting passwords that are not required for the public-site analysis;
- personal credentials of employees.

If optional private Yandex access is ever justified, use delegated access under the approved least-privilege procedure rather than password sharing.

---

## 6. Pre-start order freeze record

Before the first paid/provider acquisition for a client, create a Level-2 order record containing at minimum:

```text
site_url
site_state = existing_public_site
primary_region
business_description
primary_conversion_goal
included_directions
excluded_directions
base_package = MK01
requested_output = MK01 canonical deliverable
existing_semantic_core = PROVIDED | NONE
competitors_supplied = PROVIDED | NONE
private_yandex_access_state = AVAILABLE | UNAVAILABLE | UNKNOWN | NOT_REQUESTED
frozen_timestamp
unresolved_client_questions
```

The frozen record protects the order from being silently rewritten after the analyst sees demand evidence.

---

## 7. Missing-input behavior

### Missing URL / no public site

```text
BASE MK01 START = BLOCKED
```

Reason: current MK01 has been productized from an existing-site workflow. Do not invent the missing business/site evidence.

### Missing primary region

```text
WORDSTAT ACQUISITION = BLOCKED UNTIL REGION IS CONFIRMED
```

Do not silently infer the region.

### Unclear included business directions

Do not acquire unlimited adjacent demand.

Action:

```text
FREEZE CONFIRMED SCOPE
+ MARK UNCLEAR DIRECTIONS
+ OBTAIN CLIENT CONFIRMATION BEFORE MATERIAL EXPANSION
```

If a small ambiguity can safely remain outside the base scope, record it as excluded/pending rather than inventing client intent.

### No exclusions supplied

Allowed only when the client explicitly confirms `NONE KNOWN`. The analyst still excludes objectively out-of-scope/noise demand under the method.

### No existing semantic core

Not a blocker. MK01 is designed to collect the semantic core.

### No competitor list

Not a blocker. Competitor expansion is not part of base MK01.

### No Yandex Webmaster/Metrika/Direct access

Not a blocker. Proceed in public/provider base mode.

### Client supplies contradictory business facts

Do not choose the convenient version silently.

Record:

```text
CONFLICTING INPUT
-> identify conflict
-> use current public evidence only for facts it can actually prove
-> request/record client clarification for business facts that only the client can resolve
-> keep affected semantic decisions HOLD/REVIEW when material
```

---

## 8. Revision boundary after start

After `TEST/CLIENT ORDER FROZEN`, the following are potential scope-changing revisions:

- changing the primary region;
- adding a new product/service family not present in the frozen order;
- removing a major previously included direction after acquisition;
- switching to another website/domain;
- changing the product from existing-site to greenfield;
- requesting competitor gap analysis;
- requesting page architecture/ownership/TZ/AI analysis.

A material revision must be logged and only affected acquisition/analysis rerun where justified. Previously acquired provider evidence remains historical evidence; it is not erased or blindly recollected.

---

## 9. Client-facing “what I need from you” draft

The final Kwork card wording will be polished only after the rehearsal, but the required meaning is now frozen:

> Для начала работы пришлите ссылку на действующий сайт, основной регион продвижения и коротко укажите, какие товары/услуги нужно включить в семантику и что точно не нужно собирать. Также напишите, какое основное действие должен совершать клиент на сайте — заказать, оставить заявку, позвонить и т. п. Если у вас уже есть список запросов или старое семантическое ядро, можете приложить — это необязательно. Доступ к Яндекс Вебмастеру, Метрике или Директу для базовой работы не требуется. Google Ads, Keyword Planner и другие данные Google в этот кворк не входят.

---

## 10. Client-input PASS gate

MK01 may enter provider acquisition only when:

```text
PUBLIC_SITE_URL_CONFIRMED = true
PUBLIC_SITE_READABLE = true
PRIMARY_REGION_CONFIRMED = true
INCLUDED_DIRECTIONS_CONFIRMED = true
EXCLUSIONS_CONFIRMED_OR_NONE = true
BUSINESS/CONVERSION_JOB_CONFIRMED = true
YANDEX_ONLY_SCOPE_ACKNOWLEDGED = true
NO_REQUIRED_GOOGLE_INPUTS = true
NO_REQUIRED_PRIVATE_YANDEX_ACCESS = true
NO_PASSWORD/SECRET_DEPENDENCY = true
ORDER_FREEZE_PERSISTED = true
```

If a required field is unresolved, the affected start gate fails; the method does not fill the gap by assumption.
