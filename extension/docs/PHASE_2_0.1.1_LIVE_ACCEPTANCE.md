# Phase 2 Search — 0.1.1 owner live acceptance

Date: 2026-08-25  
Status: **AUTHORIZED / REAL-PROFILE CHECK + ONE MINIMAL REAL SYNCHRONOUS SEARCH REQUIRED**

## Exact independently accepted candidate

Use only these exact tested bytes:

```text
source commit: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact: yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes: 179013
files: 69
ZIP entries: 72
payload manifest SHA-256: ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
payload manifest bytes: 12125
Windows-safe transport commit: 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
```

The older `739dd5d7...`, `d58b5bd...` and `0186b35d...` artifacts are withdrawn/historical and must not be used.

## Independent Codex complete gate

The first independent campaign returned `FAIL_HARNESS` only and did not implicate frozen product bytes. After external Stage-4 popup-lifecycle reconciliation, Codex executed a **new complete campaign from Step 0** on the same exact `ce824a9f...` artifact.

Accepted independent result:

```text
campaign: COMPLETE_RERUN_AFTER_STAGE4_HARNESS_RECONCILIATION
live main observed by Codex: 14c8a068d79ae97ca0af80557a55a51fbd699167
step_0_authority: PASS
transport: PASS
source suite: 244/244 PASS
packaged suite: 244/244 PASS
source syntax: 22/22 PASS
packaged syntax: 63/63 PASS
source JSON: 2/2 PASS
packaged JSON: 2/2 PASS
B-01 Project/Work: PASS
B-02 Manual-ON browser transaction: PASS
B-03 Search Autorun: PASS
PD-00..PD-17: ALL PASS
mandatory Manual-ON transaction: PASS
S-00..S-17: ALL PASS
real-id late-install repair scenario: PASS
canonical live-receiver repair scenario: PASS
controlled Search stub requests: 1
real Yandex requests: 0
real credentials used: NO
production/package-test/harness mutation: NO
final cleanliness: PASS
enabled NOT_RUN sections: 0
failures: []
verdict: PASS
```

Durable evidence:

```text
extension/tests/PHASE_2_REAL_PROFILE_BINDING_REPAIR_FREEZE_TRANSPORT_CHECKPOINT_2026-08-25.md
extension/tests/PHASE_2_REAL_PROFILE_BINDING_STAGE4_HARNESS_RECONCILIATION_2026-08-25.md
extension/tests/PHASE_2_REAL_PROFILE_BINDING_CODEX_COMPLETE_PASS_2026-08-25.md
```

No product or package-test bytes changed after freeze. No refreeze is required.

## Owner-live scope

The owner performs only irreducible real-profile/provider behavior. Do not repeat the controlled regression campaign manually.

### A. First verify the repaired real-profile path

Load the **exact `ce824a9f...` artifact** in the owner's real Chrome profile and open/keep open the target ChatGPT conversation.

The repaired UI path must now behave as follows:

```text
Текущий ChatGPT = determined current conversation
→ Привязать диалог = available and succeeds
→ Ручной режим Yandex = can be enabled
→ Bridge-owned Яндекс Manual action becomes usable for the bound conversation
```

A page reload must not be required merely because the extension was loaded after the ChatGPT tab was already open; the repaired late-install/bootstrap path is specifically covered by controlled browser regression.

If this real-profile path still shows `не определён`, Bind remains disabled, Manual cannot enable, or another visible regression appears, **do not perform a paid Search request**. Return the exact screenshot/text/diagnostics to ChatGPT and Phase 2 reopens at owner-live evidence.

### B. Only after A passes, perform one provider-bound Search acceptance

Before the click:

1. select Search as active service;
2. enable Search Manual permission;
3. enable conversation Manual mode;
4. ensure valid local Yandex Search API credential/folder settings are present;
5. perform a **fresh official Search API pricing/tariff check at the actual click time**;
6. execute exactly one real synchronous Search command through the external `Яндекс` Manual action;
7. do not click twice and do not blind-retry an ambiguous provider outcome.

## Fresh official pricing rule

Official pricing source:

```text
https://aistudio.yandex.ru/docs/ru/search-api/pricing.html
```

Previously verified published values on 2026-08-25 were:

```text
daytime synchronous: 488 RUB / 1000 = 0.488 RUB/request
night synchronous:   366 RUB / 1000 = 0.366 RUB/request
night window:         00:00:00–07:59:59 UTC+3
```

These values are **not permission to skip the fresh check**. Re-check the official page immediately before the owner initiates the paid request and use the tariff applicable at the actual click time.

## Exact first live command

Use exactly one block:

```text
SEARCH_API_V1
{
  "method": "search",
  "queryText": "купить ноутбук",
  "searchType": "SEARCH_TYPE_RU",
  "region": "225",
  "page": 0,
  "groupsOnPage": 5,
  "familyMode": "FAMILY_MODE_MODERATE",
  "fixTypoMode": "FIX_TYPO_MODE_ON",
  "sortMode": "SORT_MODE_BY_RELEVANCE",
  "sortOrder": "SORT_ORDER_DESC",
  "groupMode": "GROUP_MODE_FLAT",
  "docsInGroup": 1,
  "maxPassages": 2,
  "l10n": "LOCALIZATION_RU"
}
```

Expected external provider initiations for this acceptance:

```text
exactly 1 if locally admitted
```

## PASS criteria

Owner-live Phase 2 passes when both layers pass:

```text
real-profile binding/manual UI path = PASS
single synchronous Search = truthful usable PASS
```

The Search response must contain one Bridge report with:

```text
signature: SEARCH_RESULT_V1
service: search
operation: search
status: OK
http_status: 200
request_executed: true
automatic_retry: false
response_format: FORMAT_XML
result.results: non-empty usable normalized result list
```

For returned documents, `url` is the essential identity; optional fields such as title/snippet/domain/modtime may legitimately be null according to the product contract and provider variability.

No duplicate report/provider initiation may appear from the one click.

## Controlled non-PASS outcomes

The following do not authorize a blind second click:

```text
request_executed: "UNKNOWN"
timeout/session loss after possible initiation
ambiguous delivery after irreversible provider boundary
```

Return the exact evidence to ChatGPT for reconciliation.

A clear pre-network rejection such as missing Search credentials/access/policy returns `request_executed:false` and is not evidence that Search provider execution was tested. ChatGPT must classify whether it is owner configuration/access or product behavior before any further live attempt.

A clear HTTP/provider error after one request returns `request_executed:true`, `automatic_retry:false`; return the report to ChatGPT and do not repeat automatically.

## Closure rule

```text
owner real-profile path PASS
+ owner single Search PASS
→ record exact report evidence
→ Phase 2 Search first slice = LIVE PASS / CLOSED
→ only then may Phase 3 Webmaster unlock
```

If owner-live proves a real product defect, Phase 2 reopens at the proven layer; any production or packaged-test byte change requires a new candidate and complete freeze/transport/independent-Codex chain.