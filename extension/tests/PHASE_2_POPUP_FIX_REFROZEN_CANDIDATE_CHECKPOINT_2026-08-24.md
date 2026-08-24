# Phase 2 Search — popup-fix refrozen candidate checkpoint

Date: 2026-08-24  
Status: **EXACT REPAIRED CANDIDATE FROZEN / PREFLIGHT PASS / COMPLETE CODEX RERUN REQUIRED**

## Why a new candidate exists

Owner-live use of the previous exact `d58b5bd...` artifact exposed an unusable/jumping native Chrome action popup before any real Search provider request was executed.

Root defect authority:

`extension/docs/PHASE_2_OWNER_LIVE_POPUP_CHROME151_DEFECT_2026-08-24.md`

The previous browser gate exercised `popup.html` in a normal extension tab and therefore did not exercise native `chrome.action` popup-host sizing. The affected popup had no bounded root height/internal root scroller while its intrinsic content was about 2.8–2.9k px tall against Chrome's 600 px action-popup height boundary.

## Exact repair scope

Repaired source authority:

```text
branch: fix/phase2-popup-chrome151-autosize-2026-08-24
source commit: 10bb3aca67295e5e515ff2ade8914b23e8458ca7
```

Compared with previous frozen source `0ee1d38f8d28cfccceb5a07f9606fa715261bc27`, the only production path changed is:

```text
extension/src/popup.css
```

New popup geometry contract:

```text
html/body width: 430 px fixed
html/body height: 560 px fixed
html/body overflow: hidden
main height: 100%
main overflow-y: auto
main overflow-x: hidden
```

No service-worker, content-script, Search protocol/provider, credential, policy, Manual/Autorun or delivery code changed.

## Exact refrozen artifact

```text
artifact: yandex-marketing-bridge-0.1.1-phase2-search-popup-fix-candidate.zip
source commit: 10bb3aca67295e5e515ff2ade8914b23e8458ca7
SHA-256: 0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d
bytes: 171655
files: 66
ZIP entries: 69
manifest: EXACT_POPUP_FIX_CANDIDATE_MANIFEST_2026-08-24.json
manifest SHA-256: 447bf18e54ba4a728cc6255adff5e13996366b9bf54b2668114110d525501009
manifest bytes: 11601
```

Freeze authority:

```text
workflow: phase2-popup-fix-freeze
run: 32727332723
job: 97431475994
conclusion: SUCCESS
```

Observed freeze/preflight markers:

```text
POPUP_REPAIR_SOURCE_AUTHORITY_PASS
source suite: 234/234 PASS
POPUP_FIX_DETERMINISTIC_REBUILD_PASS
PACKAGE_EXACT_IDENTITY_PASS
PACKAGED_SUITE_LAYOUT_IDENTITY_PASS
PACKAGED_SYNTAX_PASS count=60
PACKAGED_JSON_PASS count=2
packaged suite: 234/234 PASS
PACKAGED_SUITE_PASS files=39
PACKAGED_PREDELIVERY_PREFLIGHT_PASS
POPUP_FIX_FREEZE_PASS
```

## Windows-safe exact transport

```text
branch: qa/phase2-popup-fix-final-b64-transport-10bb3ac-2026-08-24
transport commit: cf467d5b2c489dc8931758debbf7bf821abe1d4f
path: extension/tests/qa_transport/phase2-popup-fix-final-b64/
.gitattributes: * -text
artifact.b64 bytes: 228876
artifact.b64 SHA-256: e8052c7db37aea022f609c6317689c2e44c93fdbb43837a86127543e732ddb79
```

Latest independent Windows transport proof:

```text
workflow: phase2-popup-fix-transport-publish
run: 32727820879
job: 97433051213
OS: Microsoft Windows Server 2025
Git: 2.55.0.windows.4
conclusion: SUCCESS
WINDOWS_RAW_MANIFEST_IDENTITY_PASS
text: unset
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
WINDOWS_POPUP_FIX_FROZEN_AUTHORITY_MATCH_PASS
WINDOWS_TRANSPORT_CLEAN_PASS
REAL_YANDEX_REQUESTS=0
```

## Exact installed-extension Windows browser preflight

```text
workflow: phase2-popup-fix-exact-browser-preflight
run: 32727820877
job: 97432999352
OS: Microsoft Windows Server 2025
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0
exact artifact: 0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d
transport commit consumed: cf467d5b2c489dc8931758debbf7bf821abe1d4f
conclusion: SUCCESS
```

Required observed markers:

```text
BROWSER_EXACT_POPUP_FIX_ARTIFACT_MATERIALIZED_PASS
B01_PROJECT_WORK_PASS
BROWSER_STEP_BIND_PASS
BROWSER_STEP_SEARCH_SETTINGS_PASS
BROWSER_STEP_MANUAL_FIRST_ON_PASS
BROWSER_STEP_NATIVE_COPY_PASS
B02_MANUAL_ON_TRANSACTION_PASS
BROWSER_STEP_AUTORUN_START_PASS
BROWSER_STEP_SEARCH_DELIVERY_PASS
B03_SEARCH_AUTORUN_PASS
BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1
BROWSER_GATE_REAL_YANDEX_REQUESTS=0
PHASE2_STAGE4_BROWSER_GATE_PASS
POPUP_CHROME151_ACTION_GEOMETRY_PASS
B04_NATIVE_ACTION_POPUP_GEOMETRY_PASS
POPUP_FIX_EXACT_BROWSER_PREFLIGHT_CLEAN_PASS
REAL_YANDEX_REQUESTS=0
```

Native action-popup geometry on the exact repaired artifact was measured as:

```text
inner: 430 x 560
html/body scroll size: 430 x 560
main client height: 560
main content scroll height: 2905
main overflow-y: auto
root/body overflow: hidden
wide regression observed: false
```

The long settings content therefore remains available through the internal scroller while Chrome's native action-popup host no longer receives an unbounded multi-thousand-pixel root document.

## Acceptance consequence

Because `popup.css` production bytes changed, the old complete Codex PASS on `d58b5bd...` cannot be transferred to this artifact.

Required next step:

```text
one new complete Codex pre-delivery campaign from the beginning
PD-00..PD-17
+ mandatory Manual-ON transaction
+ S-00..S-17
+ source 234/234
+ packaged 234/234
+ B-01/B-02/B-03
+ mandatory B-04 native chrome.action popup geometry
+ final exactness/cleanliness
```

No real Yandex requests or credentials are permitted in that campaign. Owner-live Search remains blocked until complete PASS on exact `0186b35d...`.
