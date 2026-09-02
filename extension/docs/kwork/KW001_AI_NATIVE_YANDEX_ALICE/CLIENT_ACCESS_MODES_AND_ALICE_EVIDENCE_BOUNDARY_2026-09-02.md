# KW-001 — CLIENT ACCESS MODES AND ALICE EVIDENCE BOUNDARY

Date: 2026-09-02  
Status: **ACTIVE / UNIVERSAL / OWNER-REQUESTED CLARIFICATION**  
Parent authority: `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`  
Capability authority: `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_BRIDGE_CAPABILITY_UPDATE_2026-09-01.md`

## 0. Purpose

This addendum makes one distinction operationally explicit for every KW-001 job:

```text
ANALYSIS WITHOUT CLIENT-PRIVATE ACCESS
!=
ANALYSIS WITH DELEGATED CLIENT-PRIVATE ACCESS
```

and, specifically for Alice-related evidence:

```text
PUBLIC / CONSUMER ALICE OBSERVATION
!=
OFFICIAL GENSEARCH PROVIDER EVIDENCE
!=
CLIENT-OWNED WEBMASTER "ВИДИМОСТЬ САЙТА В АЛИСЕ AI"
```

The parent policy remains authoritative: the base Kwork must be sellable and executable without mandatory Yandex Webmaster access. Client-private evidence is an optional enhancement unless an explicitly sold/authorized enhanced scope says otherwise.

This file does not promote Step 16 to a validated permanent method. Step 16 remains subject to its own current pre-step research, source-to-method trace, owner review and provider authorization gate.

---

## 1. Evidence acquisition channels

Every material evidence item in an access-sensitive step must be assigned one acquisition channel before execution.

```text
PUBLIC_SURFACE
= public site / public Search / public Yandex surface that does not require rights to the client's property.

PROVIDER_OWN_CONTEXT
= Wordstat / Search / GenSearch / other governed provider evidence acquired through our own accepted provider/Bridge context; no rights to the client's property are implied.

CLIENT_PRIVATE_DELEGATED
= private first-party evidence read through access delegated to our own working account/login.

CLIENT_PRIVATE_OPERATOR_EXPORT
= sanitized private evidence gathered by an authorized operator/client and persisted for analysis without passing client credentials to ChatGPT/Codex/browser.

UNAVAILABLE
= the private evidence exists conceptually but is not available on this job.
```

Acquisition channel and requirement class are separate fields. A source can be `CLIENT_PRIVATE_DELEGATED` and still be only an optional enhancement.

Required requirement classes:

```text
NO_CLIENT_ACCESS_REQUIRED
OPTIONAL_CLIENT_PRIVATE_ENHANCEMENT
CLIENT_PRIVATE_REQUIRED_BY_EXPLICIT_ENHANCED_SCOPE
NOT_REQUIRED_FOR_CURRENT_STEP
```

Canonical rule:

```text
PRIVATE SOURCE EXISTS
!=
PRIVATE SOURCE IS REQUIRED
```

---

## 2. Alice / Yandex evidence matrix

| Evidence surface | Client/site-owner access required? | KW-001 evidence namespace | Base-package role | Claim boundary |
|---|---:|---|---|---|
| Public Alice AI answer observed in Yandex Search / other publicly reachable consumer surface | **No rights to the client's site property are required** | `CONSUMER_ALICE_*` | Supplementary only when the current validated step method explicitly calls for it | A dated observation of that consumer surface only; do not infer private Webmaster metrics or stable/permanent behavior |
| Official GenSearch provider/API evidence | **No client-site rights required** | `GEN_SEARCH_*` | Canonical no-private-access AI evidence route where the current roadmap/method authorizes it | GenSearch evidence only; never relabel as exact consumer Alice or owned Webmaster visibility |
| Yandex Webmaster — `Видимость сайта в Алисе AI` | **Yes: rights to the site/property are required** | `OWNED_WEBMASTER_ALICE_*` | Optional first-party enhancement in the base package | Only claims actually visible in the delegated property; do not infer it from public Alice or GenSearch |
| Private Webmaster query / URL / indexing / diagnostic evidence | **Yes, unless already available through a properly delegated/authenticated governed context** | `OWNED_WEBMASTER_*` | Optional enhancement for base scope; may be required only by explicit enhanced scope | Historical/private query, URL and performance claims require observed private evidence |
| Public Yandex Business / Maps card visible as an ordinary user | **No client admin access required** | `PUBLIC_YANDEX_BUSINESS_*` | Public business evidence when relevant | Public card state only; no claims about unpublished/admin configuration |
| Yandex Business admin/ownership/verification/unpublished settings | **Yes** | `OWNED_YANDEX_BUSINESS_*` | Optional/private unless a future validated step explicitly requires it | Admin/verification/settings claims require actual delegated/private evidence |
| Metrika / Direct private reports or account state | **Yes, or a separately governed delegated provider context** | `OWNED_METRIKA_*` / `OWNED_DIRECT_*` | Not automatically required by the base package | No traffic/campaign/account-state claims without observed private evidence |

### Alice answer in plain operational terms

```text
TO SEE WHAT ALICE PUBLICLY ANSWERS
-> WE DO NOT NEED THE SITE OWNER'S WEBMASTER CABINET.

TO SEE THE SITE'S PRIVATE "ВИДИМОСТЬ САЙТА В АЛИСЕ AI" STATISTICS IN WEBMASTER
-> WE DO NEED RIGHTS TO THAT SITE/PROPERTY.

TO RUN THE BASE STEP-16 GENSEARCH ROUTE
-> CLIENT WEBMASTER ACCESS IS NOT REQUIRED;
-> PROVIDER AUTHORIZATION / COST / PERSISTENCE GATES STILL APPLY.
```

The client does not give us their password. If private Webmaster evidence is used, the preferred procedure remains delegation to our own Yandex ID with the least privilege required, normally `Просмотр / VIEW`, under the parent policy.

---

## 3. Current official Alice-access fact boundary

Current official Yandex documentation checked on 2026-09-02 states that:

- the Webmaster tool `Видимость сайта в Алисе AI` shows site representation/mentions in Alice AI answers in Search and example queries/sites;
- to view that site's statistics, the site must be added to Yandex Webmaster and rights to it must be confirmed/delegated;
- Yandex Webmaster role `Просмотр` can view site information without editing it;
- only a verified `Владелец` can manage other users' access;
- a delegated user enters Webmaster under their own Yandex ID and adds the site/property; the client password is not required.

Official references:

- `https://yandex.ru/support/webmaster/ru/service/alice-answers`
- `https://yandex.ru/support/webmaster/ru/service/rights-management`
- `https://yandex.ru/support/webmaster/ru/service/rights`
- `https://yandex.ru/support/webmaster/ru/alice`

These facts describe access/surface boundaries, not a permanent Step-16 analytical method.

---

## 4. Mandatory access/evidence precheck

Before every access-sensitive step, and before any provider/private acquisition, persist a job-level matrix containing at least:

```text
EVIDENCE_ITEM
EVIDENCE_SURFACE
ACQUISITION_CHANNEL
REQUIREMENT_CLASS
CURRENT_ACCESS_STATE
CURRENT_CAPABILITY_STATE
BASE_PATH_WITHOUT_CLIENT_ACCESS
ENHANCED_PATH_WITH_CLIENT_ACCESS
CLAIM_BOUNDARY
FALLBACK_ROUTE
BLOCKING_STATE
ARTIFACT_TARGET
```

No material evidence item may silently disappear because private access is unavailable.

For each unavailable private item choose exactly one:

```text
OPTIONAL_UNAVAILABLE__BASE_PATH_CONTINUES
CLIENT_REQUEST_REQUIRED__EXPLICIT_ENHANCED_SCOPE
NOT_REQUIRED_FOR_CURRENT_STEP
```

Canonical rule:

```text
CLIENT_PRIVATE_DATA_UNAVAILABLE
-> NARROW ONLY THE CLAIMS THAT DEPEND ON IT
-> DO NOT DOWNGRADE OR BLOCK UNRELATED PUBLIC/PROVIDER ANALYSIS
```

---

## 5. No-access mode

When client-private access is unavailable:

```text
BASE_PUBLIC_EVIDENCE_MODE = true
PUBLIC_SURFACE EVIDENCE = ALLOWED
PROVIDER_OWN_CONTEXT EVIDENCE = ALLOWED WHEN ITS OWN GATE AUTHORIZES IT
CLIENT_PRIVATE CLAIMS = FORBIDDEN UNLESS OPERATOR-PROVIDED SANITIZED EVIDENCE EXISTS
CLIENT_PRIVATE ABSENCE = NOT A PROCESS FAILURE
```

For Step 16 specifically, subject to Step-16 method research and provider authorization:

```text
BASE AI ACQUISITION PATH = OFFICIAL GENSEARCH
OWNED_WEBMASTER_ALICE_VISIBILITY = OPTIONAL_UNAVAILABLE
CONSUMER_ALICE OBSERVATION = SEPARATE SURFACE; USE ONLY IF THE VALIDATED METHOD JUSTIFIES IT
```

A public consumer-Alice observation may never be used as a substitute for a claim about the site's private Webmaster Alice visibility dashboard.

---

## 6. With-access mode

When usable client-private access becomes available:

```text
1. identify the exact private evidence item and decision it can affect;
2. if this is the first real-access job, freeze the WITHOUT_ACCESS baseline first;
3. use delegated access under our own account/login; never request client passwords, cookies, 2FA or tokens;
4. persist private-derived evidence in a separate namespace/artifact family;
5. keep public/GenSearch/consumer-Alice/owned-Webmaster evidence separate;
6. rerun only affected decision layers;
7. classify the access delta as CHANGE / DE_RISK / NEW_FINDING / NO_CHANGE / INSUFFICIENT_TO_COMPARE;
8. only then consider changing universal method, package wording, pricing or access policy.
```

Access does not automatically authorize Bridge/provider calls. Capability, provider-cost, persistence and step-authorization gates still apply independently.

Canonical separation:

```text
ACCOUNT ACCESS != TOOL CAPABILITY
TOOL CAPABILITY != STEP AUTHORIZATION
STEP AUTHORIZATION != PROVIDER CALL AUTHORIZATION
```

---

## 7. Client request rule

Do not ask the client for access merely because a private dashboard exists.

Ask for delegated access only when:

```text
A. the current validated method identifies a concrete decision that private evidence can materially change/de-risk;
OR
B. the client bought/authorized an enhanced scope that requires that private evidence;
OR
C. the first-real-access controlled comparison has been explicitly activated.
```

Otherwise:

```text
NO CLIENT ACCESS REQUEST
-> COMPLETE BASE MODE
-> DISCLOSE PRIVATE EVIDENCE NOT OBSERVED
```

---

## 8. Required reporting language

Every final report that used mixed access modes must distinguish:

```text
WHAT WE COULD OBSERVE WITHOUT CLIENT ACCESS
WHAT WE OBSERVED THROUGH OUR OWN PROVIDER/BRIDGE CONTEXT
WHAT WE OBSERVED THROUGH CLIENT-DELEGATED PRIVATE ACCESS
WHAT WAS NOT AVAILABLE
WHICH CLAIMS ARE THEREFORE BOUNDED
WHETHER PRIVATE ACCESS CHANGED ANY DECISION
```

Forbidden compression:

```text
"checked Alice"
```

when multiple surfaces were involved.

Use explicit labels such as:

```text
public consumer Alice observation
GenSearch provider observation
owned Webmaster Alice-visibility observation
```

---

## 9. Non-repeat controls

```text
KW001_CLIENT_ACCESS_MODE_MUST_BE_EXPLICIT = true
KW001_PUBLIC_PROVIDER_PRIVATE_EVIDENCE_MUST_NOT_BE_MERGED = true
KW001_PUBLIC_ALICE_DOES_NOT_REQUIRE_SITE_OWNER_WEBMASTER_ACCESS = true
KW001_OWNED_WEBMASTER_ALICE_VISIBILITY_REQUIRES_SITE_RIGHTS = true
KW001_GENSEARCH_BASE_PATH_DOES_NOT_REQUIRE_CLIENT_WEBMASTER_ACCESS = true
KW001_NO_ACCESS_NARROWS_ONLY_DEPENDENT_CLAIMS = true
KW001_PRIVATE_DASHBOARD_EXISTENCE_DOES_NOT_CREATE_ACCESS_REQUIREMENT = true
KW001_CLIENT_CREDENTIAL_SHARING_FORBIDDEN = true
KW001_FIRST_REAL_ACCESS_BASELINE_FREEZE_REQUIRED = true
KW001_ACCESS_CAPABILITY_AUTHORIZATION_ARE_SEPARATE_GATES = true
```
