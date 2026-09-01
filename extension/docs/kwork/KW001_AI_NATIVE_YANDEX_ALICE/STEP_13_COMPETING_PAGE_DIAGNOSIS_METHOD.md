# KW-001 — STEP 13 COMPETING-PAGE / CANNIBALIZATION DIAGNOSIS METHOD

Date: 2026-09-01
Status: **OWNER-DIRECTED CORRECTED METHOD / ACTIVE FOR STEP 13 / CURRENT OKNO_MSK EXECUTION REOPENED UNTIL FIRST-PARTY HISTORY GATE IS RESOLVED**

## 1. Step purpose

Step 13 determines whether related current URLs are:

- legitimate pages for different user tasks;
- normal parent/child or primary/supporting pages;
- pages with a current ownership warning signal;
- pages that repeatedly compete for the same query family;
- duplicate/near-duplicate candidates;
- or cases where the available evidence is insufficient for a strong conclusion.

The purpose is not to maximize the number of “cannibalization” findings. The purpose is to distinguish normal multi-page coverage from actual query-level competition without inventing certainty.

Canonical distinction:

```text
RELATED PAGES != CANNIBALIZATION
CURRENT SERP OVERLAP != HISTORICAL COMPETITION
HISTORICAL COMPETITION != PROVEN HARM
```

## 2. Why the first OKNO_MSK Step-13 execution was not methodologically complete

The error was **not a lack of external research**.

Before execution, Step 13 had already found the official Yandex source describing extended query-by-URL data with the fields:

```text
date
host
URL
query
region
clicks
impressions
position
```

The same pre-step research also stated that historical query×URL evidence is stronger than one public Search snapshot.

However, the execution still finished without this layer and was incorrectly marked PASS.

This failure is classified as:

```text
SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED
```

### Exact causal chain of the failure

```text
OFFICIAL SOURCE DISCOVERED
→ SOURCE RECORDED AS “IDEAL EVIDENCE”
→ CURRENT ACCESS PROBLEM TREATED AS A LIMITATION
→ LIMITATION WAS NOT CONVERTED INTO A BLOCKING / DEGRADED ACCEPTANCE GATE
→ PUBLIC CURRENT-PAGE + SERP WORK CONTINUED
→ ACCOUNTING / SEARCH / PAGE QA PASSED
→ QA DID NOT ASK WHETHER THE REQUIRED FIRST-PARTY HISTORY SOURCE HAD BEEN ACQUIRED OR EXPLICITLY WAIVED
→ STEP 13 WAS MARKED COMPLETE
```

### Concrete mistakes

1. **A required evidence source was downgraded to optional wording.**  
   `STEP_13_SOURCE_TO_METHOD_TRACE.tsv` called Yandex query×URL history “ideal evidence” instead of defining an executable availability gate.

2. **The unresolved Step-11 Webmaster blocker was not inherited as a Step-13 dependency.**  
   Step 11 had already proved that the current Webmaster OAuth context could reach the API but returned `hosts=[]`. The Step-13 pre-step review mentioned lack of Webmaster/Metrika access but did not make resolution or explicit degraded closure mandatory.

3. **Provider capability and account access were conflated.**  
   There are two independent blockers:
   - account/property blocker: the active OAuth context sees zero Webmaster hosts;
   - Bridge capability blocker: the current `webmaster_protocol.js` first slice supports only `listHosts`, `getSummary`, `getDiagnostics`, `getPopularQueries` and does not implement the official enhanced query-by-URL export workflow.

4. **The pass gate checked the evidence we had, not the evidence the method required.**  
   The old gate reconciled pairs, current pages, Search requests, verdict strength and destructive actions, but contained no mandatory field for first-party query×URL history availability/use/explicit waiver.

5. **A limitation paragraph was mistaken for a control.**  
   Writing “without Webmaster/Metrika some claims are impossible” is not equivalent to making the step fail/degrade when those data are absent.

6. **The final QA could not detect the omission because the omitted evidence source was not in the QA authority list.**

Canonical non-repeat rule:

```text
SOURCE_DISCOVERED != SOURCE_OPERATIONALIZED
SOURCE_OPERATIONALIZED != EVIDENCE_ACQUIRED
LIMITATION_DISCLOSED != LIMITATION_GOVERNED
```

## 3. External method authority

### Official Yandex

- Extended search-query analytics by URL: `https://yandex.ru/support/webmaster/ru/service/queries-export`
- Enhanced export API: `https://www.yandex.ru/dev/webmaster/doc/ru/reference/enhanced-export`
- Search query monitoring: `https://yandex.ru/support/webmaster/ru/service/popular-queries`
- Search query analytics: `https://yandex.ru/support/webmaster/ru/service/queries-analytic`
- Duplicate/similar page handling: `https://yandex.ru/support/webmaster/ru/robot-workings/double`

The enhanced export is a first-party evidence source for `query × URL × time` behavior. It can expose date, URL, query, region, clicks, impressions and position. It is therefore directly relevant when Step 13 must distinguish a one-time public SERP observation from repeated page competition.

### Industry corroboration

- Ahrefs keyword cannibalization / intent methodology;
- Semrush keyword cannibalization methodology;
- relevant-URL history concepts from rank-tracking practice.

Industry sources support the principle that same/similar intent and repeated URL competition matter more than lexical overlap alone. Exact KW-001 state names remain project-specific.

## 4. Correct evidence model

Step 13 must keep four evidence layers separate.

### Layer A — relationship/accounting evidence

Answers:

```text
Which related page pairs/candidate URL sets must be investigated?
```

This is discovery/accounting evidence only. It cannot prove a conflict.

### Layer B — current first-party page evidence

Answers:

```text
What does each current page actually do now?
What object, task, lifecycle stage and intent does it serve?
```

All material candidate URLs must pass the current-site freshness gate.

### Layer C — current public Search evidence

Answers:

```text
What URL/page type does current Yandex Search select for a bounded direct query now?
Does the target site currently expose one or several URLs in the observed result set?
```

This is a current snapshot, not a historical performance series.

### Layer D — first-party historical query×URL evidence

Answers:

```text
For the same relevant query/query family, which target-site URLs received impressions/clicks over time?
Did ownership repeatedly alternate or fragment across candidate URLs?
Were position/impression/click patterns stable, complementary or conflicting?
```

This layer is required before a full Step-13 PASS unless the current job explicitly closes under an owner-approved degraded-evidence exception.

## 5. Mandatory source availability and operationalization gate

Before Step-13 execution is allowed to reach final diagnosis, create a source/capability matrix for every material evidence route:

```text
SOURCE
EXPECTED INFORMATION
ACCESS AVAILABLE?
TOOL / OPERATION AVAILABLE?
CREDENTIAL / PROPERTY RESOLVED?
COLLECTION PLAN
STORAGE PLAN
QA CHECK
IF UNAVAILABLE: BLOCK / DEGRADE / SUBSTITUTE WITH JUSTIFICATION
```

For first-party historical query×URL evidence, valid states are:

```text
AVAILABLE_AND_USED
AVAILABLE_NOT_YET_USED
UNAVAILABLE_ACCOUNT_OR_PROPERTY_ACCESS
UNAVAILABLE_TOOL_CAPABILITY
UNAVAILABLE_PROVIDER_QUOTA_OR_DATE_RANGE
UNAVAILABLE_OTHER_WITH_EVIDENCE
OWNER_APPROVED_DEGRADED_CLOSURE
```

Forbidden state:

```text
KNOWN_SOURCE_BUT_SILENTLY_SKIPPED
```

## 6. Correct execution order

```text
1. FREEZE INPUT PAIR / URL UNIVERSE
2. RECONCILE ALL INPUT IDS
3. READ CURRENT URL EVIDENCE
4. DISCOVER MATERIAL CURRENT SPECIALIST PAGES MISSED BY FROZEN EVIDENCE
5. EXTEND THE EFFECTIVE PAIR / URL UNIVERSE WHEN CURRENT DISCOVERY REQUIRES IT
6. GROUP MATERIAL SURVIVORS AS QUERY FAMILY × CANDIDATE URL SET
7. BUILD SOURCE / CAPABILITY / ACCESS MATRIX
8. REUSE SAVED HISTORICAL FIRST-PARTY DATA IF IT ALREADY EXISTS
9. REUSE SAVED ORDINARY SEARCH EVIDENCE
10. CLOSE CLEAR DISTINCT-TASK / HIERARCHICAL RELATIONSHIPS
11. COLLECT FOCUSED ORDINARY SEARCH ONLY WHERE CURRENT OWNERSHIP IS STILL MATERIAL
12. COLLECT / INSPECT FIRST-PARTY QUERY×URL HISTORY FOR MATERIAL COMPETITION CASES
13. SEPARATE CURRENT SIGNAL, HISTORICAL COMPETITION AND HARM
14. ASSIGN VERDICT WITH EVIDENCE LEVEL
15. RECOMMEND REMEDIATION ONLY AFTER THE VERDICT
16. INDEPENDENT QA MUST CHECK BOTH PRESENT AND MISSING EVIDENCE
17. GITHUB PERSISTENCE + READBACK
18. ONLY THEN FINAL ACCEPTANCE
```

## 7. First-party history collection protocol

### Preferred evidence routes

Use current official Yandex Webmaster capabilities in this order as appropriate to the concrete job:

1. existing saved Webmaster exports already in the job;
2. Webmaster query/URL monitoring or page/query analytics if they provide the required historical view for the exact case;
3. enhanced query-by-URL export for selected candidate URLs and justified date/region scope;
4. another first-party source only if it genuinely exposes comparable query×URL historical behavior and the substitution is explicitly documented.

Do not invent a universal fixed number of days. The concrete job must predeclare a justified window based on:

```text
available dates
seasonality
query volume
case severity
provider quota
number of candidate URLs
client decision being made
```

The method must preserve why the chosen window is sufficient or why it is only partial.

### Required normalized historical row

At minimum, when available:

```text
date
host
url
query
region
clicks
impressions
position
source
collection_window
```

### Historical analysis questions

For each material query-family case:

```text
Do two or more candidate URLs receive impressions for the same/similar query family?
Is that simultaneous, alternating, episodic or stable by intent/long-tail?
Does one URL clearly dominate while another is incidental/supporting?
Does ownership switch repeatedly across comparable periods?
Is the apparent switch explained by changed content, seasonality, mixed intent or page availability?
Are impressions/clicks fragmented in a way consistent with a same-intent competition theory?
Is there evidence of actual harmful impact, or only multi-URL visibility?
```

## 8. Verdict taxonomy

Use evidence-separated verdicts. Do not collapse all overlap into one label.

Permitted classes include:

```text
NORMAL_DISTINCT_TASKS
NORMAL_PARENT_CHILD
NORMAL_PRIMARY_SUPPORTING
NORMAL_MIXED_INTENT
CURRENT_TARGET_RELEVANT_MISMATCH_SIGNAL
CURRENT_MULTI_URL_VISIBILITY_SIGNAL
HISTORICAL_MULTI_URL_COMPETITION_SUPPORTED
HISTORICAL_OWNER_SWITCHING_SUPPORTED
TRUE_DUPLICATE_OR_NEAR_DUPLICATE_CONFLICT
HARMFUL_IMPACT_SUPPORTED
EVIDENCE_INSUFFICIENT
```

`CONFIRMED_HARMFUL_CANNIBALIZATION` may be used only when the concrete evidence supports all necessary parts of that statement. It must not be inferred from:

```text
shared keywords
shared cluster
related pages
one public SERP
one target/relevant mismatch
multi-URL visibility without harm evidence
```

## 9. Remediation rules

No destructive site action follows automatically from overlap.

Possible outputs:

```text
KEEP_BOTH
DIFFERENTIATE_PRIMARY_RESPONSIBILITY
STRENGTHEN_INTERNAL_LINK_SIGNAL
REASSIGN_PRIMARY_OWNER
CONTENT_SCOPE_REPAIR
CONSOLIDATION_CANDIDATE
REDIRECT_CANDIDATE
CANONICAL_CANDIDATE
DEFER_PENDING_HISTORY
```

Destructive remediation requires qualifying evidence and a check that useful independent intent/value will not be lost.

## 10. Mandatory QA

QA must check absence as well as presence.

Required questions:

```text
Did every declared pair/case reconcile?
Were current URLs re-read?
Were newly discovered material pages incorporated?
Was every official source that materially changes the method operationalized?
Was first-party query×URL history availability explicitly classified?
If unavailable, was Step-13 status degraded/blocked instead of silently passed?
Did the verifier inspect evidence-source omissions rather than only validate existing artifacts?
Did any one-SERP observation become a historical/harm claim?
Did any destructive action exceed its evidence level?
Are provider outcomes/costs/readbacks reconciled?
```

## 11. Pass gate

A full Step-13 PASS requires:

```text
PAIR / CASE ACCOUNTING = COMPLETE
SILENT DROPS = 0
CURRENT PAGE FRESHNESS = COMPLETE FOR MATERIAL URLS
MATERIAL CURRENT-SITE DISCOVERIES = INCORPORATED
PUBLIC SEARCH EVIDENCE = RECONCILED WHERE USED
FIRST_PARTY_QUERY_URL_HISTORY_GATE = AVAILABLE_AND_USED
OR OWNER_APPROVED_DEGRADED_CLOSURE = true
KNOWN_REQUIRED_SOURCE_SILENTLY_SKIPPED = 0
HISTORICAL CLAIM FROM ONE PUBLIC SERP = 0
HARM CLAIM WITHOUT HARM EVIDENCE = 0
DESTRUCTIVE REMEDIATION WITHOUT QUALIFYING EVIDENCE = 0
INDEPENDENT QA BLOCKING FINDINGS = 0
FINAL GITHUB READBACK = PASS
STEP14_EXECUTED = false
```

If first-party history is unavailable and no owner-approved degraded closure exists:

```text
STEP13 = REOPENED / BLOCKED OR DEGRADED
NEXT_STEP_ALLOWED = false
```

## 12. Current OKNO_MSK application

The public/current-page portion of Step 13 is valuable and remains preserved:

```text
historical base pairs = 195
effective pair universe after current-site discoveries = 199
pairs accounted = 199/199
query-family cases = 21
fresh ordinary-Search cases with usable evidence = 16/16
current-page evidence URLs = 49
confirmed harmful cannibalization from existing evidence = 0
destructive remediation authorized = 0
```

But the full Step-13 PASS is withdrawn because first-party historical query×URL evidence was not acquired and was not governed by an explicit degraded-closure gate.

Current blockers are separately documented in the OKNO_MSK Step-13 postmortem/current state.

## 13. Non-repeat markers

```text
STEP13_SOURCE_KNOWN_BUT_NOT_OPERATIONALIZED_FORBIDDEN = true
STEP13_SOURCE_DISCOVERED_NOT_EQUAL_SOURCE_OPERATIONALIZED = true
STEP13_LIMITATION_DISCLOSED_NOT_EQUAL_LIMITATION_GOVERNED = true
STEP13_FIRST_PARTY_QUERY_URL_HISTORY_GATE_REQUIRED = true
STEP13_ACCOUNT_ACCESS_AND_TOOL_CAPABILITY_ARE_SEPARATE = true
STEP13_QA_MUST_TEST_MISSING_REQUIRED_EVIDENCE = true
STEP13_ONE_SERP_CANNOT_PROVE_HISTORY_OR_HARM = true
STEP13_FULL_PASS_BLOCKED_WITHOUT_HISTORY_OR_OWNER_DEGRADED_EXCEPTION = true
```