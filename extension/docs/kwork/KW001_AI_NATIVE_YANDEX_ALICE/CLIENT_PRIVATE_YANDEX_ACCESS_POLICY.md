# KW-001 — CLIENT PRIVATE YANDEX ACCESS POLICY

Date: 2026-09-01  
Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This is a Layer-A universal operating rule for KW-001.

It governs client-owned private Yandex data, especially Yandex Webmaster access, in the sellable base Kwork and in all future test/client jobs.

Owner decision that created this rule:

```text
THE BASE KWORK MUST BE SELLABLE AND EXECUTABLE WITHOUT MANDATORY YANDEX WEBMASTER ACCESS.
CLIENT PRIVATE DATA IS OPTIONAL ENHANCEMENT, NOT A PURCHASE BLOCKER.
THE FIRST REAL JOB THAT PROVIDES WEBMASTER ACCESS MUST BE USED FOR A CONTROLLED WITH-ACCESS VS WITHOUT-ACCESS COMPARISON.
ONLY AFTER THAT COMPARISON MAY WE CLAIM HOW MATERIAL THE ACCESS IS TO QUALITY, CHANGE THE PACKAGE POLICY, OR DESIGN THE FINAL WEBMASTER BRIDGE EXPANSION.
```

Capability-specific statements are governed separately from this commercial/access decision. The current reusable Bridge capability authority is `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_BRIDGE_CAPABILITY_UPDATE_2026-09-01.md` together with the canonical Bridge product branch named there. This parent policy must not be used as a stale fixed method-list snapshot.

---

## 1. Base-package commercial rule

Canonical base-package policy:

```text
YANDEX_WEBMASTER_ACCESS_REQUIRED_TO_BUY = false
YANDEX_WEBMASTER_ACCESS_REQUIRED_TO_EXECUTE_BASE_SCOPE = false
CLIENT_PRIVATE_DATA_UNAVAILABLE = NORMAL_BASE_MODE
CLIENT_PRIVATE_DATA_UNAVAILABLE != PROCESS_FAILURE
CLIENT_PRIVATE_DATA_UNAVAILABLE != LOW_QUALITY_BY_DEFINITION
```

The base service must be designed so its promised result can be produced from accepted public/provider evidence such as:

```text
current public site evidence
Yandex Wordstat demand evidence
ordinary Yandex Search/SERP evidence
selective GenSearch evidence where the roadmap requires it
current business/site structure
analytical mapping, clustering and architecture work owned by ChatGPT
```

Private Webmaster/Metrika/Direct evidence may deepen, de-risk or accelerate parts of the analysis when available, but it must not be silently required by a base-package promise.

### Client-facing wording

Allowed meaning for the Kwork requirements/card:

> Доступ к Яндекс Вебмастеру — опционально. Основной анализ выполняется без него по данным сайта, Яндекс Wordstat и поисковой выдачи. Если доступ есть, он может ускорить и углубить проверку уже накопленной поисковой статистики и снизить неопределённость по фактическим запросам и URL.

Shorter acceptable wording:

> Доступ к Яндекс Вебмастеру — опционально, при наличии поможет ускорить и углубить анализ.

or:

> Доступ к Яндекс Вебмастеру не обязателен, но при наличии будет полезен для дополнительной проверки поисковой статистики сайта.

Forbidden before the first controlled comparison:

```text
"Webmaster does not affect quality"
"the result is identical with and without Webmaster"
"Webmaster always improves the result"
"Webmaster always speeds up the work"
```

Reason: these are empirical claims we have not yet earned. The commercial promise is narrower and defensible:

```text
NO WEBMASTER -> FULL BASE-PACKAGE SCOPE STILL DELIVERED
WEBMASTER AVAILABLE -> OPTIONAL FIRST-PARTY ENHANCEMENT
```

---

## 2. Mandatory access-state check inside access-sensitive roadmap steps

Known current access-sensitive steps are:

```text
STEP 11 — PAGE OWNERSHIP
STEP 12 — STRUCTURAL ACTIONS
STEP 13 — COMPETING-PAGE / CANNIBALIZATION DIAGNOSIS
STEP 16 — AI-SEARCH EVIDENCE ACQUISITION
```

The current `WORKING_RUNBOOK_FOR_CHATGPT.md` already establishes that Webmaster is optional for the public-site base package and that client-owned Webmaster evidence should be used when available. It also establishes that client-owned `Видимость сайта в Алисе AI` is preferred first-party AI evidence when available, while official GenSearch is the fallback when it is not. In the current 0-22 roadmap, that AI-evidence acquisition belongs to Step 16.

At the beginning of EACH access-sensitive step, before executing the step, ChatGPT must explicitly check the current job's Yandex Webmaster access state with the owner.

Required owner-facing block:

```text
YANDEX WEBMASTER ACCESS CHECK

CURRENT ACCESS STATE = AVAILABLE | UNAVAILABLE | UNKNOWN | GRANTED_NOT_READY | READY

WHY IT CAN HELP IN THIS STEP
= exact additional first-party evidence this step could use.

BASE PATH WITHOUT ACCESS
= what evidence/method will still complete the promised base scope.

ENHANCED PATH WITH ACCESS
= what extra first-party checks become possible.

FIRST-ACCESS COMPARISON STATE
= NOT_YET_RUN | REQUIRED_ON_THIS_JOB | ALREADY_COMPLETED
```

If access state is not already freshly known, ask the owner directly whether access is available.

Do not repeatedly ask the client for credentials. The question is whether delegated access exists or can be provided.

### Step 11 — why access can help

Without private access, Step 11 can still determine intended page ownership from current page content, business scope and ordinary Search evidence.

With Webmaster access, Step 11 may additionally compare:

```text
INTENDED_TARGET_URL
vs
OBSERVED_YANDEX_QUERY_URL / RELEVANT_URL EVIDENCE
```

This can expose mismatches between the page we believe should own the task and the URL Yandex has actually associated with queries.

No-access rule:

```text
TARGET OWNER DECISIONS = ALLOWED
CURRENT/HISTORICAL PRIVATE QUERY->URL CLAIMS = FORBIDDEN UNLESS OBSERVED
```

### Step 12 — why access can help

Without private access, Step 12 can still make structural decisions such as:

```text
KEEP EXISTING URL/ROLE
EXPAND
ROUTE
CREATE / SPLIT / MERGE where otherwise justified
```

With Webmaster/Metrika evidence, Step 12 may additionally evaluate real search/traffic performance and implementation risk.

Canonical distinction remains:

```text
STRUCTURAL_OWNER_DECISION != PERFORMANCE/OPTIMIZATION_STATE
```

No-access rule:

```text
KEEP_EXISTING_STRUCTURE
= KEEP THE URL / ROLE
!= PAGE IS PROVEN TO PERFORM WELL
!= NO OPTIMIZATION NEEDED
```

### Step 13 — why access can help

Without private access, Step 13 executes the sellable base mode using:

```text
current page evidence
current public Search/SERP evidence
intent / ownership / overlap analysis
```

Allowed base-mode conclusion types include:

```text
normal distinct tasks
parent/child or primary/supporting relationships
current ownership mismatch signals
current multi-URL visibility signals
public evidence insufficient for a historical/harm claim
```

Without private data, Step 13 must NOT claim:

```text
historical URL switching proved
historical cannibalization absent
historical harmful competition proved
traffic/click loss proved
```

With Webmaster query×URL history, Step 13 may additionally test repeated historical competition, URL switching, impression/click fragmentation and harm evidence.

### Current-policy override for the previous Step-13 hard block

The earlier Step-13 method required first-party query×URL history or explicit degraded closure before a full PASS. That hard requirement was appropriate for a research-grade full-history diagnosis but conflicts with the now owner-approved commercial base-package policy.

For BASE KWORK jobs, this Layer-A rule supersedes that hard block:

```text
CLIENT_PRIVATE_DATA_UNAVAILABLE
-> BASE_PUBLIC_EVIDENCE_MODE
-> NOT A PROCESS FAILURE
-> STEP 13 MAY COMPLETE THE BASE-PACKAGE PURPOSE
-> HISTORICAL/HARM CLAIMS REMAIN BOUNDED TO AVAILABLE EVIDENCE
```

A richer research-grade / enhanced mode may still require first-party history when that enhanced scope is explicitly sold or authorized.

### Step 16 — why access can help

Without private access, the base AI-evidence path remains the accepted official GenSearch route with strict provenance:

```text
GEN_SEARCH_* != CONSUMER_ALICE_* / OWNED_WEBMASTER_ALICE_*
```

With suitable client-owned Webmaster access and a currently validated Yandex surface, Step 16 may additionally use first-party owned evidence such as `Видимость сайта в Алисе AI` where relevant.

No-access rule:

```text
AI EVIDENCE STEP = ALLOWED
OFFICIAL GENSEARCH PATH = AVAILABLE FOR BASE MODE
DO NOT CLAIM CLIENT-OWNED ALICE VISIBILITY DATA WAS OBSERVED
```

With-access rule:

```text
PRESERVE OWNED WEBMASTER AI EVIDENCE SEPARATELY
PRESERVE GENSEARCH EVIDENCE SEPARATELY WHEN BOTH ARE USED
DO NOT RELABEL ONE SURFACE AS THE OTHER
COMPARE WHETHER OWNED ACCESS CHANGES / DE-RISKS THE AI DECISION
```

---

## 3. Downstream conditional use

Current Steps 14-22 other than Step 16 are not automatically declared to require Webmaster access.

If a validated step method establishes a material use for client-private Webmaster data, the pre-step review must:

```text
1. identify that use explicitly;
2. classify it as BASE-REQUIRED or OPTIONAL-ENHANCEMENT;
3. preserve the base-package no-mandatory-access promise unless the owner explicitly changes the product;
4. add a new mandatory access-sensitive step to this policy only under owner authorization.
```

Current known downstream handling:

```text
Step 18 has an approved permanent prioritization / implementation-readiness method.
First-party Webmaster/Metrika performance evidence may strengthen business/performance/measurement calibration when available and in scope.
Such evidence remains OPTIONAL for the analytical-priority base path and must never be fabricated when absent.
Implementation-ready mode requires real owner/effort/capacity/business/measurement inputs appropriate to the sold scope, but that requirement does not make Webmaster access universally mandatory; another valid current client/implementer evidence source may satisfy the relevant calibration field.

Step 20 final QA must reconcile private evidence if private evidence was used earlier, but must not demand new Webmaster access merely to close a base job unless the validated Step20 scope explicitly requires it.
```

These are governed downstream notes, not a blanket private-access requirement for Steps 18/20.

---

## 4. First real access = mandatory controlled comparison

The FIRST future job in which usable Yandex Webmaster access becomes available triggers a controlled comparison experiment.

Before viewing/using private data for analytical decisions:

```text
1. complete and freeze the relevant PUBLIC-ONLY / NO-ACCESS outputs first;
2. persist them durably;
3. mark them as the WITHOUT_ACCESS baseline;
4. only then activate/use Webmaster private evidence;
5. rerun only the affected decision layers with access;
6. persist the WITH_ACCESS outputs separately;
7. compare the two result sets before changing universal methodology or commercial claims.
```

The no-access baseline must not be contaminated by private-data knowledge.

Mandatory comparison dimensions:

```text
Step 11:
- owner/relevant-URL mismatches newly discovered
- ownership decisions changed
- ownership decisions only de-risked

Step 12:
- structural actions changed
- optimization/performance warnings newly discovered
- risky actions prevented or re-prioritized
- confidence changed

Step 13:
- current-only verdicts changed by history
- historical URL switching discovered
- actual harm evidence discovered
- cases that remained NO_CHANGE

Step 16:
- owned Webmaster AI-visibility evidence newly available
- AI-case conclusions changed
- AI-case conclusions only de-risked
- differences between owned Webmaster AI evidence and GenSearch evidence

Whole job:
- number of CHANGE decisions
- number of DE_RISK decisions
- number of NEW_FINDING decisions
- number of NO_CHANGE decisions
- analyst time difference where measurable
- provider/engineering cost difference
- client-deliverable difference
```

Required comparison verdict taxonomy:

```text
CHANGE
DE_RISK
NEW_FINDING
NO_CHANGE
INSUFFICIENT_TO_COMPARE
```

Only after this experiment may the owner decide whether to:

```text
keep Webmaster optional;
make it a recommended enhancement;
create a separate enhanced package;
change price/scope;
change marketing wording;
change any future access requirement.
```

---

## 5. First access also triggers governed Bridge capability verification

The parent access policy does **not** define a frozen list of supported Webmaster methods. Current reusable Bridge capability is governed by:

```text
CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_BRIDGE_CAPABILITY_UPDATE_2026-09-01.md
+ the canonical Bridge product branch identified by that authority
```

Therefore:

```text
PARENT ACCESS POLICY != BRIDGE CAPABILITY SNAPSHOT
OLDER EMBEDDED EXTENSION SNAPSHOT != CURRENT BRIDGE PRODUCT AUTHORITY
BRIDGE CAPABILITY != CLIENT ACCESS
BRIDGE CAPABILITY != PROPERTY RESOLVED
BRIDGE CAPABILITY != PRIVATE EVIDENCE USED
```

The first real client access triggers a capability/readiness review, but NOT an uncontrolled speculative rewrite and NOT an assumption that required methods are missing.

Required sequence:

```text
REAL ACCESS AVAILABLE
-> freeze WITHOUT_ACCESS baseline
-> identify exact private evidence needed by the affected analytical steps
-> read current Bridge capability authority
-> verify the then-current official Yandex API/UI route when material
-> validate installed runtime / Bridge version against canonical product authority
-> map each required evidence item to an existing supported Bridge operation when available
-> resolve delegated property/host readiness
-> only if a named evidence requirement is not supported, define the smallest governed Bridge enhancement
-> obtain owner authorization for any actual Bridge implementation
-> run focused tests for changed capability when applicable
-> run required pre-delivery regression when Bridge code changed
-> live read-only acceptance on the delegated property
-> WITH_ACCESS analytical pass
-> comparison
```

Do not add broad Webmaster functionality merely because the API exposes it. Do not re-implement functionality that current capability authority already proves. Extend only a named missing evidence surface justified by the real analytical job, and preserve reusable capability only after the normal product gates pass.

---

## 6. Exact safe client delegation procedure — no password sharing

Official Yandex authority:

- https://yandex.ru/support/webmaster/ru/service/rights-management
- https://yandex.ru/support/webmaster/ru/service/quick-start
- https://yandex.ru/dev/webmaster/doc/ru/reference/hosts

### What we give the client

We give the client:

```text
OUR WORKING YANDEX ID / LOGIN
```

The client does NOT give us their Yandex password.

Default requested role for analytical work:

```text
ПРОСМОТР / VIEW
```

Official Yandex describes this role as allowing the user to view all site information without editing it. This is the default least-privilege role for KW-001 analysis.

If a future exact API/export workflow is proven not to work under `Просмотр`, do not silently request broader rights. Explain the concrete limitation to the owner/client and request the smallest additional role only after evidence shows it is necessary.

### What the site owner does

The person managing access must be a Yandex Webmaster user with the `Владелец` role whose site rights are confirmed.

For the exact site:

```text
1. Open Yandex Webmaster.
2. Select the required site/property.
3. Open Настройки -> Права доступа.
4. In Список пользователей enter OUR Yandex login exactly as provided.
5. Choose role Просмотр.
6. Click Добавить.
7. Tell us that access has been granted and send/confirm the exact site URL variant used in Webmaster.
```

Yandex officially states that only a verified `Владелец` can assign roles to other users.

### What we do after the owner grants access

Delegated access does not automatically make the site appear in our Webmaster account.

We must:

```text
1. Sign in to Yandex Webmaster with the SAME Yandex ID/login the client granted.
2. Add the site to our Webmaster account manually if it is not already listed.
3. Add the exact same property variant used by the owner:
   https vs http
   www vs non-www
   exact host/property form.
4. Confirm that the delegated role is visible and the site's information can be read.
5. If Bridge/API work is needed, authorize OUR OWN Yandex OAuth context under this same delegated Yandex ID.
6. Run one bounded listHosts/provider check.
7. Persist useful provider evidence immediately to GitHub and read it back before further provider work.
8. Resolve the exact host_id from provider evidence before any host-specific API call.
```

Yandex explicitly warns that a delegated site is not added automatically to the recipient's account and that URL variants such as `https://www.example.com`, `https://example.com`, `http://www.example.com`, and `http://example.com` are distinct when adding the property.

### What we must NEVER request from a client for this access

```text
Yandex password
2FA code
recovery code
browser cookies
session export
client OAuth token
client API bearer token
mailbox password
remote-desktop credentials merely to read Webmaster
```

Normal handoff is delegation to our Yandex ID, not credential sharing.

### Troubleshooting if access was granted but site is not visible

Check in this order:

```text
1. Are we signed in under the exact Yandex ID/login the owner granted?
2. Did the verified site owner actually assign the role?
3. Did we add the site manually to our Webmaster account?
4. Is the property variant exactly the same (https/http, www/non-www)?
5. Is the role still active?
6. For API work, does OAuth belong to the same delegated Yandex ID?
7. Only after correcting a real state issue, rerun one bounded listHosts check.
```

Do not replay provider/API calls repeatedly without correcting the access/property state first.

### Revocation after work

The client may revoke our role in Webmaster after the order is complete. We do not require permanent access for completed base work.

---

## 7. Required per-job access record

Every job must be able to state:

```text
YANDEX_WEBMASTER_ACCESS_STATE = UNKNOWN | UNAVAILABLE | AVAILABLE_NOT_GRANTED | GRANTED_NOT_READY | READY
YANDEX_WEBMASTER_ROLE = NONE | VIEW | PARTIAL | EDIT | OWNER | UNKNOWN
YANDEX_WEBMASTER_PROPERTY = <exact property> | NONE | UNKNOWN
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED = true | false
FIRST_ACCESS_COMPARISON_REQUIRED = true | false
FIRST_ACCESS_COMPARISON_COMPLETE = true | false
```

For current/early no-access jobs:

```text
YANDEX_WEBMASTER_ACCESS_STATE = UNAVAILABLE
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED = false
BASE_PUBLIC_EVIDENCE_MODE = true
```

---

## 8. Non-repeat controls

```text
KW001_WEBMASTER_NOT_REQUIRED_FOR_BASE_PURCHASE = true
KW001_PRIVATE_DATA_UNAVAILABLE_IS_NORMAL_BASE_MODE = true
KW001_ACCESS_CHECK_REQUIRED_AT_STEPS_11_12_13_16 = true
KW001_NO_PASSWORD_OR_SESSION_CREDENTIAL_REQUEST = true
KW001_DEFAULT_WEBMASTER_ROLE_VIEW = true
KW001_DELEGATED_SITE_MUST_BE_ADDED_BY_RECIPIENT = true
KW001_EXACT_PROPERTY_VARIANT_REQUIRED = true
KW001_FIRST_REAL_ACCESS_COMPARISON_REQUIRED = true
KW001_WITHOUT_ACCESS_BASELINE_MUST_BE_FROZEN_FIRST = true
KW001_FIRST_ACCESS_TRIGGERS_GOVERNED_BRIDGE_CAPABILITY_REVIEW = true
KW001_PARENT_ACCESS_POLICY_DEFERS_BRIDGE_CAPABILITY_TO_CURRENT_CAPABILITY_AUTHORITY = true
KW001_DO_NOT_REIMPLEMENT_ALREADY_SUPPORTED_BRIDGE_CAPABILITY = true
KW001_NO_UNTESTED_CLAIMS_ABOUT_ACCESS_QUALITY_DELTA = true
KW001_STEP13_BASE_MODE_NOT_BLOCKED_BY_PRIVATE_DATA_ABSENCE = true
KW001_STEP16_BASE_MODE_USES_GENSEARCH_WHEN_OWNED_WEBMASTER_AI_EVIDENCE_IS_UNAVAILABLE = true
KW001_STEP18_PRIVATE_FIRST_PARTY_EVIDENCE_OPTIONAL_FOR_ANALYTICAL_PRIORITY_MODE = true
```