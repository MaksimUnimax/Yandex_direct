# Lifecycle button gating — installed-extension browser preflight

Status: **PASS / CHATGPT PRE-CODEX PREFLIGHT ONLY / NOT INDEPENDENT CODEX EVIDENCE**  
Date: 2026-08-26

This checkpoint records the installed-extension browser preflight for the frozen lifecycle-button gating candidate. It does not authorize owner handoff. Independent Codex complete applicable gate remains mandatory.

## Frozen candidate under test

```text
candidate branch = candidate/lifecycle-button-gating-2026-08-25
candidate source = 939e880f820e52beae9dcbcedc86d5cd9e13b075
candidate parent = b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact = yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
artifact SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
artifact bytes = 179877
files = 69
ZIP entries = 72
ZIP integrity = PASS
```

The package used by this browser preflight was not rebuilt from source for the browser step. It was reassembled from the already published exact B64 transport and independently rechecked before extraction.

## Exact transport used

```text
transport branch = qa/lifecycle-button-gating-exact-transport-2026-08-26
transport commit = e11b4f9d5dfb9f5b1bd01bd885151aefdcddc797
transport dir = extension/tests/qa_transport/lifecycle-button-gating
transport format = YMB_EXACT_ZIP_B64_TRANSPORT_V1
chunk count = 69
base64 chars = 239836
base64 SHA-256 = a226f87c626659ba16b9f992fc526019c3d3d98702d5655659846b5a8f74e359
fresh-consumer exact round-trip = PASS
byte-identical to frozen target = PASS
```

Durable transport checkpoint:

```text
extension/tests/LIFECYCLE_BUTTON_GATING_EXACT_TRANSPORT_PASS_2026-08-26.md
```

## Browser harness identity

The lifecycle harness is QA-only and is exactly one commit / one file above the frozen product source:

```text
branch = qa/lifecycle-button-gating-browser-harness-939e880-2026-08-26
commit = 1009b224d1cfe389f6f041a16cd2a8d53657284a
parent = 939e880f820e52beae9dcbcedc86d5cd9e13b075
path = extension/tests/qa_browser/lifecycle_button_gating_gate.mjs
blob = 43739af40d50c35d910752c0cdb1371487393e9a
product bytes in harness delta = 0
package-test bytes in harness delta = 0
```

The harness creates controlled lifecycle occupancy only through extension-local storage. It does not use real credentials and does not initiate a real Yandex provider request.

## Qualified environment

```text
Chrome for Testing = 151.0.7922.47
puppeteer-core = 25.4.0
installed extension = exact transported 0430463e... package
browser mode = headed under Xvfb in isolated QA profile
real credentials = NO
real Yandex requests = 0
```

Development/preflight run:

```text
GitHub Actions run = 32920317520
job = 98032481002
conclusion = SUCCESS
```

GitHub Actions is development/preflight evidence only. Codex must rerun the governed harness independently.

## Required behavior observed

Initial ready state:

```text
LIFECYCLE_BUTTON_INITIAL_ENABLED_PASS
```

Active Manual operation:

```text
LIFECYCLE_MANUAL_OPERATION_DISABLED_PASS
LIFECYCLE_MANUAL_OPERATION_BLOCKED_CLICK_NO_DISPATCH_PASS
LIFECYCLE_MANUAL_OPERATION_CLEAR_REENABLE_PASS
```

Active delivery/outbox occupancy:

```text
LIFECYCLE_DELIVERY_DISABLED_PASS
LIFECYCLE_DELIVERY_BLOCKED_CLICK_NO_DISPATCH_PASS
LIFECYCLE_DELIVERY_CLEAR_REENABLE_PASS
```

Provider safety and final browser verdict:

```text
LIFECYCLE_GATE_PROVIDER_HITS=0
LIFECYCLE_GATE_REAL_YANDEX_REQUESTS=0
LIFECYCLE_BUTTON_GATING_BROWSER_GATE_PASS
CHATGPT_BROWSER_PREFLIGHT_PASS
```

The blocked-click assertions verify that the real Bridge-owned `Яндекс` action is disabled at the DOM control layer and a click attempt while disabled does not dispatch the Manual operation. After the authoritative blocker is cleared, the same action becomes enabled again.

## Product-state preservation

The browser scenario does not require resetting worker/delivery timers or reconstructing runtime state to refresh the action. The frozen product contract remains:

```text
blocking lifecycle active
-> existing Bridge action remains present but disabled/non-clickable
-> blocked UI click cannot dispatch WS_EXECUTE_MANUAL_BLOCK
-> backend admission guards remain fail-closed
-> lifecycle/outbox clear is positively observed
-> action becomes clickable again
```

No popup geometry change is part of this candidate.

## Authorization after this checkpoint

```text
CHATGPT_PRE_CODEX_BROWSER_PREFLIGHT = PASS
INDEPENDENT_CODEX_GATE = STILL_REQUIRED
OWNER_HANDOFF = BLOCKED
OWNER_LIVE = BLOCKED
AUTHORIZED_NEXT_STAGE = INDEPENDENT_CODEX_COMPLETE_APPLICABLE_GATE_ON_EXACT_0430463E_ARTIFACT
```

Any product or package-test byte change after this checkpoint invalidates the frozen candidate and requires a new exact artifact, transport proof and complete applicable gate.