# Codex pre-delivery full regression gate — Yandex Marketing Bridge

Status: **MANDATORY / LIVING GATE**  
Adopted: 2026-08-18  
Scope: every installable Yandex Marketing Bridge build that is about to be handed to the owner as a working build/candidate.

## 1. Purpose

This document is the permanent regression firewall before owner handoff.

It is deliberately **not** the test policy for every intermediate edit.

Two modes are mandatory:

### Development mode — while code is still being changed

Run only the tests needed for the code being changed:

- focused tests for the changed behavior;
- directly affected dependency/regression tests;
- changed-line/branch execution where appropriate;
- syntax/static checks needed by the changed surface.

Do **not** run this whole document after every small edit. The purpose is to keep development fast and focused.

### Pre-delivery mode — immediately before handing a working build to the owner

After the feature/bug work is finished and the candidate is frozen, Codex must execute **all enabled tests in this document in one complete run against the exact candidate that would be handed to the owner**.

The full gate is one validation campaign, not a chain of separate prompts. Codex returns one final PASS/FAIL result.

If any mandatory item fails:

1. the build is **not handed to the owner**;
2. return to development mode and fix the defect;
3. run focused tests while fixing it;
4. when the fix is complete, freeze the new candidate;
5. rerun this **entire pre-delivery gate from the beginning**.

No partial previous PASS is enough after production code changes.

## 2. Living-document rule

This is a living functional test registry.

Whenever product functionality changes, this document must change with it:

- new user-visible/runtime functionality -> add regression coverage here;
- changed functionality -> update its acceptance tests here;
- removed functionality -> remove its obsolete tests here in the same governed change;
- a test must never be deleted merely because it currently fails;
- implementation and gate coverage must not intentionally drift.

Before every pre-delivery run, Codex must compare the current specification/roadmap/source surface with this registry and report any functional surface that exists but has no Codex-capable gate coverage. Missing coverage is itself a gate FAIL until the registry/test harness is updated.

## 3. Codex capability boundary

This gate includes **all functionality that Codex can reliably validate using already-qualified controlled tooling**.

Current accepted controlled capabilities include:

- repository/source/hash inspection;
- Node/VM/unit/integration tests;
- JS/MJS syntax checks;
- JSON/manifest validation;
- deterministic packaging and source↔package identity checks;
- Chrome for Testing + Puppeteer controlled browser QA;
- runtime `browser.installExtension()` of an exact unpacked source tree;
- MV3 service-worker/content-script/popup checks;
- controlled factual ChatGPT DOM fixtures;
- popup/storage lifecycle;
- multi-tab/conversation ownership tests;
- service-worker lifecycle/recovery tests;
- controlled network interception/stubs/fault injection;
- console/network diagnostics;
- localStorage/cookie persistence in the dedicated QA profile.

This gate does **not** relabel controlled evidence as real-profile/live evidence. The owner's normal logged-in Chrome/current ChatGPT and real provider behavior remain separate live acceptance surfaces when required.

Unless a future gate revision explicitly authorizes otherwise, this pre-delivery gate performs **zero real Yandex provider requests and uses no real credentials**.

## 4. Run discipline

For a pre-delivery run:

- freeze the exact source/candidate first;
- record exact candidate/source identity before testing;
- do not modify production code during the gate;
- run every enabled section below in one Codex task;
- do not stop after the first ordinary assertion failure: collect the full product failure set where continuing is safe;
- do not skip a section because a similar historical report passed;
- test the exact candidate being handed off, not a nearby tree;
- if a ZIP/package is the handoff artifact, test the extracted handoff package as well as source;
- real Yandex request count must remain `0` unless a future governed revision of this document explicitly changes that rule.

Allowed final gate states are:

- `PASS` — every enabled mandatory section passed;
- `FAIL_PRODUCT` — one or more product/regression assertions failed;
- `FAIL_ARTIFACT` — source/package identity or packaging failed;
- `FAIL_HARNESS` — the already-qualified controlled harness could not complete the run and the result cannot be trusted.

Only `PASS` permits build handoff to the owner.

---

# 5. Mandatory full regression matrix

## PD-00 — Authority, candidate freeze and exact identity

Required:

- live GitHub HEAD/governed authority recorded;
- exact candidate source path/commit/reconstruction authority recorded;
- production file count recorded;
- candidate manifest version recorded;
- governed production hashes/manifest checked where available;
- working tree/reconstruction inputs are clean and unambiguous;
- no stale historical candidate is substituted.

Acceptance: exact candidate identity is proven before any behavior test.

## PD-01 — Complete source regression suite

Run the complete current source test suite, not only focused tests.

Required:

- every current test passes;
- `0` failures;
- `0` skipped/cancelled tests unless a specific skip is explicitly governed in this document;
- test count recorded;
- all newly added tests from the just-finished development work are included.

Acceptance: `PASS` only with a fully green current suite.

## PD-02 — Static, syntax and manifest integrity

Run all current static integrity checks:

- every JS/MJS source parses;
- every governed JSON parses;
- `manifest.json` validates;
- every manifest-declared script/HTML/resource entrypoint exists;
- extension version/product version consistency passes;
- permissions and host permissions equal the governed intended surface;
- no accidental extra production file/entrypoint appears.

Acceptance: all checks PASS.

## PD-03 — Package/reconstruction integrity

When the owner will receive a ZIP/package/reconstructed candidate:

- build/reconstruct from the exact frozen source using the governed deterministic procedure;
- build A and B when deterministic packaging is supported;
- require A == B byte-identical;
- extract a fresh copy;
- require source↔fresh-package file set and bytes to match exactly;
- run the complete packaged test suite on the fresh extraction;
- run syntax/JSON/manifest checks on the fresh extraction;
- record filename, SHA-256, bytes and file count.

If the project currently uses a governed patch/reconstruction artifact rather than committed production source, verify the patch/reconstruction on a fresh exact preimage and require final tree byte identity.

Acceptance: artifact being handed off is exactly the tested artifact.

## PD-04 — Runtime installation and MV3 lifecycle

Using the accepted Chrome for Testing/Puppeteer harness:

- launch the qualified browser engine;
- install the exact frozen unpacked candidate with `browser.installExtension()`;
- verify extension identity/version;
- verify MV3 service worker target starts;
- verify content script loads on matched controlled ChatGPT URL;
- verify actual popup loads and initializes;
- verify no unexpected extension/runtime errors;
- verify a safe service-worker lifecycle/restart contour where supported.

Acceptance: runtime installation/lifecycle PASS.

## PD-05 — Popup/settings behavior

Using the actual extension popup in controlled browser, verify all currently present controls.

Current mandatory behaviors include:

- Manual toggle applies immediately and persists correctly;
- Debug toggle applies immediately and persists correctly;
- Auto Send toggle applies immediately and persists correctly;
- Wordstat Autorun policy toggle applies immediately and persists correctly;
- report-prefix enabled toggle applies immediately and persists correctly;
- popup reopen reflects runtime/storage truth, not stale defaults;
- toggle changes do not accidentally commit unsaved text/credential fields;
- text/credential fields obey their intended explicit-Save semantics;
- current-conversation state is not confused with another conversation.

Whenever popup controls are added/removed, this section must be updated in the same development change.

## PD-06 — Manual action surface / ChatGPT DOM binding

On the current governed controlled ChatGPT DOM families, verify:

Permanent owner-directed sibling-control regressions:

- Manual OFF leaves native Copy unchanged and has no Yandex sibling.
- Manual ON leaves native Copy unchanged and creates exactly one separate
  `button[data-ymb-manual-action="true"]` per uniquely bound eligible block.
- Each sibling is yellow, visibly labeled `Яндекс`, and a different DOM element
  from native Copy.
- Native Copy has no Bridge Manual listener/effect; clicking it produces zero
  `WS_EXECUTE_MANUAL_BLOCK`.
- Clicking Yandex produces exactly one intended Manual admission.
- Generic whole-response Copy and ambiguous blocks have zero siblings.
- Mutation creates exactly one sibling; Manual OFF removes only Yandex siblings;
  re-enable creates exactly one sibling again.

### Manual OFF

- every uniquely resolved local assistant code/writing-block Copy remains native;
- no bridge yellow state;
- no visible `Яндекс` label;
- generic whole-response Copy stays native;
- ambiguous mapping stays native/fail-closed.

### Manual ON

- every uniquely resolved supported local assistant block Copy becomes yellow + visible `Яндекс`;
- decoration is independent of block contents/protocol validity;
- plain text, raw JSON, malformed command, valid command and multi-command blocks decorate equally;
- generic whole-response Copy is excluded;
- ambiguous local mapping fails closed;
- native Copy event is not prevented;
- no duplicate bridge label/listener/style appears.

### Dynamic DOM

- newly appended block is discovered/decorated;
- body replacement is handled;
- whole block/PRE replacement is handled;
- detached controls do not retain active bindings;
- Manual OFF restores exact native state;
- re-enable decorates exactly once again.

Current factual family must include the latest supported ChatGPT PRE/readonly-CodeMirror structure plus any still-supported legacy adapters.

## PD-07 — Manual full-block discovery and click/core behavior

Through actual content→worker controlled flow, cover at minimum:

- Bridge Manual execution is triggered by the separate Yandex sibling, never by
  native Copy.
- Native Copy produces no Manual transaction.
- Yandex sibling captures the complete bound block.
- Double-click/in-flight fencing applies to the Yandex sibling.

- non-command/plain block -> explicit worker-owned controlled error/result, no silent no-op;
- raw JSON without registered marker -> explicit controlled error/result;
- malformed registered command -> worker-owned parse/validation error;
- one valid Wordstat command -> discovered and validated;
- prose + multiple commands -> all commands discovered in source order;
- balanced-brace/string-aware extraction;
- malformed material at one marker does not consume later valid markers;
- one clicked block produces one Manual transaction/batch contour;
- strict serial semantics for multiple commands;
- no hidden parallel provider fan-out;
- double-click/in-flight duplicate fence;
- generic response Copy produces no Manual dispatch;
- ambiguous Copy produces no Manual dispatch;
- conversation mismatch/unconfirmed binding fails closed.

All cases run with zero real Yandex requests.

## PD-08 — Wordstat protocol and all enabled Phase-1 operations

For every currently enabled Wordstat method, validate with controlled provider stubs/faults:

- `getTop`;
- `getDynamics`;
- `getRegionsDistribution`;
- `getRegionsTree`.

For every method verify:

- strict input validation;
- allowed method registry;
- exact routing/endpoint;
- fixed Yandex host;
- correct request body construction;
- Folder ID placement semantics without secret disclosure;
- response parsing;
- HTTP status propagation;
- result operation identity;
- unique request ID;
- success contour;
- HTTP-error contour;
- no automatic hidden retry;
- no hidden pagination/fan-out unless a future specification explicitly adds it.

Boundary/invalid parameter tests for each method remain part of the suite as functionality evolves.

## PD-09 — Policy, credentials, cost and accounting semantics

Validate controlled semantics for:

- missing credentials -> skip before provider initiation;
- invalid/local validation -> `request_executed:false`;
- policy/request ceiling -> skip before provider initiation;
- cost ceiling -> skip before provider initiation;
- free operation accounting follows current governed pricing configuration;
- successful simulated provider request -> `request_executed:true`;
- HTTP error after simulated send -> `request_executed:true`;
- unknown irreversible request outcome -> `request_executed:"UNKNOWN"` and no blind retry;
- `automatic_retry:false` where no retry occurred;
- RUN attempted/executed/skipped counters remain exactly-once;
- standalone Manual does not require an invented Job/GitHub budget;
- paused RUN and Manual share governed RUN ceilings where applicable.

If tariff/config semantics change, update implementation and this gate together.

## PD-10 — Autorun lifecycle

Using actual popup + installed extension + controlled ChatGPT fixture, verify current Autorun functionality end-to-end without real provider traffic:

- policy enable persists;
- Start creates exactly one RUN for the confirmed conversation;
- waiting state is reached;
- popup reopen displays the same RUN identity/state/counters;
- eligible command pickup occurs without local Copy;
- controlled result/error delivery returns to same conversation exactly once;
- recoverable error returns RUN to a safe controllable state when governed;
- Pause works;
- Resume preserves RUN identity and counters;
- Stop terminates the same RUN;
- stopped RUN does not capture later blocks;
- another conversation/tab cannot steal ownership;
- safe reload/worker restart recovers governed waiting state;
- Manual/Autorun mutual-exclusion or coexistence rules match the current specification.

If Autorun functionality is removed, remove this section only in the same governed product-removal change.

## PD-11 — Delivery FSM, durability, recovery and duplicate prevention

Validate all protected delivery invariants:

Positive release regression:

`Manual operation → result/error complete → one Send commit/click → initial
confirmation misses because the sent user-turn appears late → bounded
confirmation-only reconciliation sees that existing sent user-turn → no second
Send → no second WS_EXECUTE_MANUAL_BLOCK → no provider replay → operation
COMPLETED → next Manual Yandex sibling action admitted.`

Negative fence regression:

`Committed delivery remains unconfirmed/unresolved → MANUAL_OPERATION_ACTIVE
remains enforced → no premature lock release → no repeat Send/API.`

Both are permanent mandatory gate regressions.

- normal result delivery exactly once;
- normal error delivery exactly once;
- always-on error delivery independent of Debug state;
- durable result/error outbox survives safe restart;
- claim/commit/confirmation boundaries are respected;
- pre-commit ChatGPT delivery failure preserves already completed operation/result;
- recovery may retry/reconcile only the delivery contour when provider work is already complete;
- recovery never replays a completed/unknown provider initiation;
- committed Send boundary is reconciliation-only and never blindly clicks Send again;
- duplicate content-ready/recovery events do not duplicate Send/result;
- double-click does not duplicate provider initiation;
- unknown-outcome fingerprint fence remains enforced.

## PD-12 — Debug/error contract

Using zero-provider controlled errors, verify:

### Debug OFF

- error automatically returns to bound ChatGPT;
- concise normal envelope;
- no extra debug trace;
- no secret leakage.

### Debug ON

- same automatic error delivery still occurs;
- useful diagnostics are added;
- credentials/tokens/Authorization/storage secrets remain redacted;
- Debug state persists according to popup contract.

Verify representative parse, validation, policy/credential, delivery and unknown-outcome errors where current tests support them.

## PD-13 — Conversation, tab and ownership isolation

Verify:

- confirmed conversation binding is required;
- one tab cannot steal another tab's active delivery/RUN ownership;
- duplicate tabs fail closed according to governed ownership rules;
- multiple assistant blocks bind only to their own local Copy;
- no cross-PRE or cross-assistant binding;
- conversation reload/rebind preserves only governed state;
- stale conversation identity cannot execute a command;
- no global accidental "current conversation" state is introduced.

## PD-14 — Export/import, migration and persistence

Verify all currently supported backup/migration behavior:

- export schema/metadata;
- checksum generation/validation;
- untampered backup accepted;
- tampered backup rejected;
- secrets are present only where backup design intentionally contains them;
- secrets never enter ChatGPT/debug/GitHub-facing payloads;
- cross-install restore works in a fresh extension identity;
- compatible settings survive same-folder upgrade/reload;
- active RUN/manual-operation safety state is not overwritten unsafely by import;
- legacy `wsmb_*` compatibility remains as long as specification requires it;
- text/toggle settings restore according to current semantics.

## PD-15 — Security and provider-surface containment

Verify fail-closed security invariants:

- no API key/OAuth token/Authorization secret in page/content/result/error/debug evidence;
- assistant content cannot choose arbitrary URL/host;
- arbitrary HTTP method is rejected;
- arbitrary headers/auth are rejected;
- provider hosts remain fixed to governed allowlist;
- operation registries remain explicit;
- unsupported operations fail before network;
- no runtime GitHub token/repo/branch/job coupling is required for provider execution;
- backup secrets stay isolated from user-facing logs;
- no real Yandex request is made during this gate.

## PD-16 — Future-service phase locks

Until their phases are explicitly enabled, verify that:

- Search;
- Webmaster;
- Metrika;
- Direct

cannot execute provider requests through assistant-supplied content.

Recognizing future markers, if supported, must not silently enable execution.

When one of these services becomes an enabled product phase, replace its phase-lock assertion with a full functional section equivalent in depth to PD-08 and add all relevant popup/policy/delivery/security coverage.

## PD-17 — Final artifact cleanliness and evidence

At the end of the one complete gate run verify again:

- production candidate did not mutate during validation;
- exact production hashes/file set still match the frozen candidate;
- repository/test working tree state is recorded;
- real Yandex request count is exactly `0` unless a future governed gate revision authorizes otherwise;
- no secret is present in generated reports;
- all mandatory PD sections have an explicit status;
- no `NOT_RUN`/`UNKNOWN` is silently treated as PASS.

Create one final Markdown + JSON report containing the complete gate matrix and exact artifact identity.

---

# 6. Required final verdict

Codex must return one final result for the whole run:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT

candidate:
  authority: <sha/ref>
  version: <value>
  source_identity: PASS|FAIL
  artifact: <filename|UNPACKED>
  artifact_sha256: <sha|NONE>

sections:
  PD-00: PASS|FAIL
  PD-01: PASS|FAIL
  PD-02: PASS|FAIL
  PD-03: PASS|FAIL|NOT_APPLICABLE
  PD-04: PASS|FAIL
  PD-05: PASS|FAIL
  PD-06: PASS|FAIL
  PD-07: PASS|FAIL
  PD-08: PASS|FAIL
  PD-09: PASS|FAIL
  PD-10: PASS|FAIL
  PD-11: PASS|FAIL
  PD-12: PASS|FAIL
  PD-13: PASS|FAIL
  PD-14: PASS|FAIL
  PD-15: PASS|FAIL
  PD-16: PASS|FAIL
  PD-17: PASS|FAIL

source_suite: <pass>/<total>
packaged_suite: <pass>/<total>|NOT_APPLICABLE
real_yandex_requests: <integer>
production_modified_during_gate: YES|NO

verdict:
  PASS|
  FAIL_PRODUCT|
  FAIL_ARTIFACT|
  FAIL_HARNESS
```

`PASS` is valid only when every enabled mandatory section is PASS and the exact handoff artifact/candidate is the one tested.

# 7. Handoff rule

ChatGPT must not present an installable candidate to the owner as the working build until the latest exact candidate has a fresh `PASS` from this gate.

Historical PASS from an older source tree/package is not transferable to a newer candidate.

This full gate is intentionally run **only at the final pre-handoff boundary**. During normal implementation and bug fixing, use focused tests for changed code and its affected dependencies instead.

Real-profile/live acceptance, when still required by the roadmap, occurs after this gate and remains a separate classification; this gate never fabricates a live PASS.
