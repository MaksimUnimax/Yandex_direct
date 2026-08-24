# Phase 2 popup-fix — complete governed gate PASS

Date: 2026-08-24  
Status: **FINAL ACCEPTANCE / COMPLETE GATE PASS**

This checkpoint closes the owner-live Chrome 151 action-popup defect and supersedes the earlier `COMPLETE CODEX RERUN REQUIRED` state for the repaired Phase-2 candidate.

## Accepted exact candidate

```text
source commit:
10bb3aca67295e5e515ff2ade8914b23e8458ca7

artifact:
yandex-marketing-bridge-0.1.1-phase2-search-popup-fix-candidate.zip

artifact SHA-256:
0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d

artifact bytes: 171655
files: 66
ZIP entries: 69

payload manifest:
EXACT_POPUP_FIX_CANDIDATE_MANIFEST_2026-08-24.json

payload manifest bytes: 11601
payload manifest SHA-256:
447bf18e54ba4a728cc6255adff5e13996366b9bf54b2668114110d525501009
```

The previously frozen artifact `d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16` remains revoked and must not be installed or represented as the accepted Phase-2 candidate.

## Exact Windows-safe transport

```text
branch:
qa/phase2-popup-fix-final-b64-transport-10bb3ac-2026-08-24

commit:
cf467d5b2c489dc8931758debbf7bf821abe1d4f

path:
extension/tests/qa_transport/phase2-popup-fix-final-b64/
```

The complete campaign re-verified the transport both before execution and after all browser/package work:

```text
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

## Complete campaign evidence

```text
workflow: phase2-popup-fix-complete-gate
run: 32730308190
job: 97440819536
conclusion: SUCCESS

OS: Microsoft Windows Server 2025
Git: 2.55.0.windows.4
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0

QA PR: #12
QA executor branch head used by the successful run:
d1bccc8afcc39800c7f1e50ffb83db3bcdd809d4

PR merge checkout used by GitHub Actions:
dad034d59ff348f8e5e0eeb71602f1b42f9da9e8

effective Windows gate executor SHA-256:
aca85b6b04b4dcf6202c2a123b24098cedde87757f1794c71a2346a4764b4bd2
```

The campaign started from live `main`:

```text
35574cca4551b2e5210f3bb8cb1433b7d555948c
qa: require native Chrome action-popup geometry gate
```

No production file and no package-test file was modified during the campaign.

## Full source/package result

```text
source suite: 234/234 PASS
packaged suite: 234/234 PASS
packaged syntax: 60/60 PASS
packaged JSON: 2/2 PASS
final exactness: PASS
final cleanliness: PASS
not-run enabled sections: 0
```

For the Windows source worktree, the campaign used the exact Git blob line endings without mutating the QA checkout:

```text
git -c core.autocrlf=false -c core.eol=lf worktree add --detach ...
WINDOWS_QA_CHECKOUT_CONFIG_UNCHANGED_PASS
```

This reconciles the earlier two source-only false failures caused by Windows CRLF checkout interacting with tests that locate source boundaries using literal LF delimiters. The exact package had already remained 234/234 PASS.

## Browser B-01 / B-02 / B-03

The installed-extension browser campaign passed:

```text
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
```

The underlying published Stage-4 harness authority remained based on:

```text
667fda2f9a0e4197c4873ea96f27862c8453f2f0
```

The final campaign applied a QA-only deterministic popup-reopen harness correction from the tracked QA executor at `d1bccc8...`: popup tabs are identified by the exact Chrome `tab.id` through `chrome.tabs.getCurrent()`, and tab removal is confirmed before the next reopen. This replaced the flaky Puppeteer target-creation race exposed in the prior complete attempt. Marker:

```text
STAGE4_POPUP_REOPEN_BY_TAB_ID_HARNESS_PATCH_PASS
```

This correction changes no extension runtime byte and was removed before the harness cleanliness proof.

## Native toolbar popup B-04

The native Chrome action-popup gate was executed separately through real `chrome.action.openPopup()` against the same exact extracted artifact.

Observed geometry:

```text
innerWidth: 430
innerHeight: 560
htmlScrollHeight: 560
bodyScrollHeight: 560
mainClientHeight: 560
mainScrollHeight: 2905
mainOverflowY: auto
rootOverflow: hidden
bodyOverflow: hidden
POPUP_WIDE_REGRESSION_OBSERVED=false
POPUP_CHROME151_ACTION_GEOMETRY_PASS
```

Therefore the repaired popup remains size-stable and the long settings form scrolls inside `main` instead of forcing the native Chrome action host to resize.

## Governed acceptance matrix

All mandatory pre-delivery sections passed:

```text
PD-00 PASS
PD-01 PASS
PD-02 PASS
PD-03 PASS
PD-04 PASS
PD-05 PASS
PD-06 PASS
PD-07 PASS
PD-08 PASS
PD-09 PASS
PD-10 PASS
PD-11 PASS
PD-12 PASS
PD-13 PASS
PD-14 PASS
PD-15 PASS
PD-16 PASS
PD-17 PASS
```

Mandatory Manual-ON transaction:

```text
PASS
```

All Search Phase-2 sections passed:

```text
S-00 PASS
S-01 PASS
S-02 PASS
S-03 PASS
S-04 PASS
S-05 PASS
S-06 PASS
S-07 PASS
S-08 PASS
S-09 PASS
S-10 PASS
S-11 PASS
S-12 PASS
S-13 PASS
S-14 PASS
S-15 PASS
S-16 PASS
S-17 PASS
```

Search sub-contracts were all PASS, including protocol registry, parser validation, exactly-once provider request, credential policy, cost guard, base64 XML decode, XML normalization, Manual path, Autorun path, Wordstat/Search isolation, unknown-HTTP no-retry, and future Search-mode lock.

## Provider safety

```text
controlled Search stub requests: 1
real Yandex requests: 0
real credentials used: NO
```

No production Yandex endpoint or real Yandex credential was used by the campaign.

## Final cleanliness

After removing externally installed browser-driver material and the temporary tab-identity harness file:

```text
source worktree: CLEAN
transport worktree: CLEAN
Stage-4 harness worktree: CLEAN
QA checkout: CLEAN except generated gate-evidence/ directory
production modified during gate: NO
package tests modified during gate: NO
final cleanliness: PASS
```

## Final verdict

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT
verdict: PASS
COMPLETE_GATE_VERDICT=PASS
PHASE2_POPUP_FIX_COMPLETE_GATE_PASS
PHASE2_POPUP_FIX_COMPLETE_GATE_ENFORCED_PASS
```

The exact repaired candidate `0186b35d66cf1e7e20a522dc128b3fdd317cd660c665b8294120a1ab8affe91d` is accepted for installation/use as the current Phase-2 candidate. The revoked `d58b5bd...` artifact is not accepted.
