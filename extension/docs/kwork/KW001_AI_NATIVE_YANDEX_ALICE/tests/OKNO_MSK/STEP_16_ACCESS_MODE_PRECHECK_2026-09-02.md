# OKNO_MSK — STEP 16 ACCESS MODE PRECHECK

Date: 2026-09-02  
Job: `OKNO_MSK`  
Stage: **BEFORE STEP 16 METHOD RESEARCH / BEFORE ANY AI PROVIDER CALL**  
Authority type: job-specific access/evidence-mode record.  
Universal authorities:

- `../../CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`
- `../../CLIENT_PRIVATE_YANDEX_ACCESS_POLICY_BRIDGE_CAPABILITY_UPDATE_2026-09-01.md`
- `../../CLIENT_ACCESS_MODES_AND_ALICE_EVIDENCE_BOUNDARY_2026-09-02.md`

This record does **not** authorize Step 16 execution and does **not** validate a permanent Step-16 method.

---

## 1. Upstream state

```text
STEP14_14A_FINAL = PASS
STEP15_CASE_SELECTION = PASS
STEP15_REVIEWED = 25
STEP15_SELECTED = 6
STEP15_REJECTED = 18
STEP15_HOLD = 1
SELECTED_CASE_IDS = C15-004,C15-006,C15-010,C15-013,C15-019,C15-020
STEP16_EXECUTED = false
STEP16_PROVIDER_CALL_AUTHORIZED = false
```

Selected queries:

```text
панорамные алюминиевые окна
алюминиевые окна для веранды
установка подоконников
французские окна
открыть пластиковое окно
лучшие пластиковые окна
```

---

## 2. Current client-private access state

Inherited from the current job manifest/access-policy capability update:

```text
YANDEX_WEBMASTER_ACCESS_STATE = UNAVAILABLE
YANDEX_WEBMASTER_ROLE = NONE
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED = false
OKNO_MSK_HOST_ID_RESOLVED = false
BASE_PUBLIC_EVIDENCE_MODE = true
WEBMASTER_METRIKA_DIRECT = UNAVAILABLE_FOR_BASE_REHEARSAL
```

Interpretation:

```text
NO CLIENT-PRIVATE ACCESS
!=
STEP16 BASE-MODE BLOCK
```

No client password, cookie, 2FA code, OAuth token or session export is needed or allowed.

---

## 3. Step-16 access/evidence matrix

| Evidence item | Surface | Acquisition channel | Requirement class | Current state | Base path without client access | Claim boundary | Blocking? |
|---|---|---|---|---|---|---|---:|
| Official generative-search evidence for the six selected cases | GenSearch | `PROVIDER_OWN_CONTEXT` | `NO_CLIENT_ACCESS_REQUIRED` | Available as project capability; **not yet authorized for this step** | Run only after Step-16 method research, manifest, owner review, provider/cost authorization and persistence gate | `GEN_SEARCH_*` only; not consumer Alice and not owned Webmaster Alice visibility | **No client-access block; yes Step-16 authorization block** |
| Public Alice AI answer observation, if future Step-16 research proves it useful | Public/consumer Alice surface | `PUBLIC_SURFACE` | `NO_CLIENT_ACCESS_REQUIRED` | Not acquired in this Step-16 precheck | Can be observed without rights to the client's Webmaster property, but only if the validated method explicitly requires it | Dated consumer-surface observation only; personalization/time variance possible | No client-access block |
| `Видимость сайта в Алисе AI` | Yandex Webmaster private property | `CLIENT_PRIVATE_DELEGATED` | `OPTIONAL_CLIENT_PRIVATE_ENHANCEMENT` | **UNAVAILABLE** | Use GenSearch base route; do not claim owned visibility statistics were observed | `OWNED_WEBMASTER_ALICE_*` claims forbidden on current evidence | **No** |
| Private Webmaster query×URL/history/indexing evidence | Yandex Webmaster | `CLIENT_PRIVATE_DELEGATED` / governed Bridge after delegation | `OPTIONAL_CLIENT_PRIVATE_ENHANCEMENT` | **UNAVAILABLE** | Preserve existing public Search/site baselines | No private historical/query×URL claims | No |
| Metrika private reports | Yandex Metrika | `CLIENT_PRIVATE_DELEGATED` / governed provider if later supported and authorized | `NOT_REQUIRED_FOR_CURRENT_STEP` | Unavailable | Not part of current Step-16 base acquisition | No traffic/session claims | No |
| Direct private account/campaign state | Yandex Direct | `CLIENT_PRIVATE_DELEGATED` / governed provider if later supported and authorized | `NOT_REQUIRED_FOR_CURRENT_STEP` | Unavailable | Not part of current Step-16 base acquisition | No campaign/account claims | No |

---

## 4. Alice answer for this job

For `OKNO_MSK` specifically:

```text
DO WE NEED THE SITE OWNER'S CABINET TO TEST THE BASE AI EVIDENCE PATH?
= NO.

CAN WE COLLECT THE BASE STEP-16 AI EVIDENCE OURSELVES?
= YES, THROUGH THE OFFICIAL GENSEARCH ROUTE AFTER THE SEPARATE STEP-16 METHOD/AUTHORIZATION GATE.

CAN WE OBSERVE A PUBLIC CONSUMER ALICE ANSWER WITHOUT THE OWNER'S WEBMASTER RIGHTS?
= YES, IF THAT PUBLIC SURFACE IS AVAILABLE AND THE VALIDATED METHOD CALLS FOR IT.

CAN WE SEE THE PRIVATE WEBMASTER "ВИДИМОСТЬ САЙТА В АЛИСЕ AI" FOR OKNO_MSK WITHOUT DELEGATED RIGHTS?
= NO.

DOES THAT PRIVATE-DASHBOARD ABSENCE BLOCK THE BASE KWORK?
= NO.
```

The evidence surfaces must remain separate:

```text
GEN_SEARCH_* != CONSUMER_ALICE_* != OWNED_WEBMASTER_ALICE_*
```

---

## 5. Client-access request decision

Current decision:

```text
REQUEST_CLIENT_WEBMASTER_ACCESS_NOW = false
```

Reason:

1. The owner-approved base package is explicitly executable without mandatory Webmaster access.
2. Current `OKNO_MSK` is the no-access/base-public rehearsal.
3. The six Step-16 cases already have frozen pre-AI Search baselines.
4. GenSearch is the documented no-private-access route, subject to its own Step-16 method/provider gate.
5. Requesting access merely because a private Alice dashboard exists would violate the access policy.

If delegated Webmaster access unexpectedly becomes available before job close, the universal first-real-access comparison rule applies: freeze/preserve the no-access baseline before private evidence is used analytically.

---

## 6. Step-16 execution boundary

```text
STEP16_CLIENT_PRIVATE_ACCESS_BLOCK = false
STEP16_METHOD_RESEARCH_REQUIRED = true
STEP16_SOURCE_TO_METHOD_TRACE_REQUIRED = true
STEP16_RESEARCH_TO_EXECUTION_SCHEMA_REQUIRED = true
STEP16_OWNER_REVIEW_REQUIRED = true
STEP16_PROVIDER_CALL_AUTHORIZED = false
STEP16_GENSEARCH_CALLS = 0
STEP16_PRIVATE_WEBMASTER_EVIDENCE_USED = false
STEP16_EXECUTED = false
```

Next legal action:

```text
STEP16 PRE-STEP CURRENT METHOD/CAPABILITY RESEARCH
-> SOURCE-TO-METHOD TRACE
-> ACCESS/EVIDENCE MATRIX RECHECK
-> EXECUTION MANIFEST
-> OWNER-FACING REVIEW
-> WAIT FOR EXPLICIT AUTHORIZATION
-> ONLY THEN ANY GENSEARCH/AI ACQUISITION
```

---

## 7. Required final reporting distinction

When this job reaches delivery, the report must explicitly state separately:

```text
A. what was established from the public site and ordinary Search;
B. what was established from GenSearch;
C. whether any direct public consumer-Alice observations were made;
D. that private Webmaster Alice-visibility data was not observed unless access later changes;
E. which conclusions therefore remain bounded by the no-access mode.
```

Forbidden wording for current evidence state:

```text
"we checked the site's Alice visibility in Webmaster"
"Webmaster confirms Alice visibility"
"Alice visibility statistics show ..."
```

unless delegated private evidence is actually acquired and persisted later.
