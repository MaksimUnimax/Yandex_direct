# PHASE 0 — REFERENCE AUDIT

Date: 2026-08-12
Status: PASS for reference analysis; see Phase 1 plan for implementation gate.

## 1. Authority used for this audit

Repository authority before this audit:

- repository: `MaksimUnimax/Yandex_direct`;
- branch: `main`;
- starting HEAD: `62fbbeaaedcbe5a60618df1772bb5cfe344a3e47` (`Create unified extension test area`).

Owner-supplied reference artifacts:

- ZIP: `wordstat-bridge-v1.1.5-full-function-environment-audit(4).zip`;
- ZIP SHA-256: `a39bbe65b046ef6eac5a7890b8afd84e69550db34debf271b7c373d08a1fef1a`;
- canonical documentation: `WORDSTAT_BRIDGE_DOCUMENTATION_APPEND_ONLY_FULL_FUNCTION_ENVIRONMENT_AUDIT(4).md`;
- documentation SHA-256: `437a69022b31621d7a749e3b92c0faf0c45f3d7be60e1a901cda65c3faf0a25a`.

The exact supplied ZIP above is the implementation reference for Phase 1. The final append-only section of the supplied canonical documentation explicitly identifies this full-function/environment-audit ZIP and the same SHA-256.

## 2. Important history inside the canonical document

The canonical append-only document contains a historical `1.1.6` narrow patch entry which fixed stale bridge-version provenance in `WORDSTAT_RESULT_V1`.

Later append-only entries deliberately continued work on a manifest/runtime `1.1.5` artifact for Start parity, delivery single-flight/concurrency repairs and then a full-function/environment audit. The exact artifact supplied by the owner is that later audited `1.1.5` package.

Therefore:

- we do **not** silently substitute an unavailable `1.1.6` ZIP for the supplied artifact;
- we use the exact supplied audited `1.1.5` package as behavioral/reference authority;
- we treat the stale report-version issue as a **known reference defect that must not be inherited** by Yandex Marketing Bridge.

Observed directly in the supplied reference source:

```javascript
// shared/wordstat_protocol.js
const VERSION = "1.1.1";
```

while `manifest.json` and `package.json` are `1.1.5`.

Phase 1 must remove this possibility by having one authoritative product version surface or an explicit consistency test that executes result formatting and compares it with the packaged manifest version.

## 3. Exact fresh-ZIP verification performed in Phase 0

The owner-supplied ZIP was extracted into a fresh empty directory and tested without modifying production files.

### Package

```text
name: wordstat-bridge-extension
version: 1.1.5
```

### Test suite

```text
npm test
283 tests
283 PASS
0 FAIL
```

### Syntax

`node --check` PASS for:

- `service_worker.js`;
- `content_script.js`;
- `popup.js`;
- `shared/autorun_model.js`;
- `shared/composer_send.js`;
- `shared/conversation_identity.js`;
- `shared/manual_controls.js`;
- `shared/proven_writing_block_capture.js`;
- `shared/wordstat_protocol.js`.

The reference's own machine-readable full-function audit records additionally:

- source suite 283/283 PASS;
- fresh ZIP suite 283/283 PASS;
- Business Bridge 2.0.0.22 unchanged reference 437/437 PASS;
- fresh-ZIP real Chromium MV3/DOM/API-mock E2E 21/21 PASS;
- JS/MJS syntax 29/29 PASS;
- JSON parse 9/9 PASS;
- source ↔ extracted ZIP 41/41 files identical.

The Chromium E2E uses real Chromium with a ChatGPT DOM mock and Yandex HTTPS mock. It is strong browser/runtime evidence, but it is not equivalent to a new production ChatGPT live acceptance for the future unified extension.

## 4. Reference content inventory

The extracted artifact contains 41 files (44 ZIP entries including directories), total uncompressed content approximately 705 KB.

Major production files:

```text
manifest.json                  1,204 B
popup.html                    11,681 B
popup.css                      5,118 B
popup.js                      25,958 B
content_script.js             79,623 B
service_worker.js            106,684 B
shared/autorun_model.js        9,371 B
shared/composer_send.js        7,063 B
shared/conversation_identity.js 1,955 B
shared/manual_controls.js     10,269 B
shared/proven_writing_block_capture.js 14,614 B
shared/wordstat_protocol.js    6,653 B
```

The artifact also contains 19 `tests/*.test.mjs` files plus historical/current machine-readable evidence files.

`extension/reference/REFERENCE_INVENTORY.json` records the SHA-256 and byte size of every extracted file.

## 5. Byte-identical Business Bridge common modules

The reference audit proves these four Wordstat files are byte-identical to the supplied Business Bridge 2.0.0.22 common implementation:

```text
shared/composer_send.js
SHA-256 a6a2b25ea29637b76250a9f29fdcb177b52824a16a193b44ca5603df2494da79

shared/conversation_identity.js
SHA-256 e56a9f352c4668f47a0f72c2044a943a88457024c4400fa878a974551518114a

shared/manual_controls.js
SHA-256 81f302487da7b5ff7c1b746298353438b2cfec100a5bb8f7fa2c80d1e033c81e

shared/proven_writing_block_capture.js
SHA-256 5b0eaac9619cb827d1e74c61f53e2755c084a1d4b60c64d23f5fd4a5354c3aef
```

Phase 1 rule: copy these files byte-identically into the new source baseline first. Do not refactor or rename their internal semantics during the Wordstat migration unless a failing unified requirement proves the need.

## 6. Generic but Wordstat-named module

`shared/autorun_model.js` is behaviorally generic but exports:

```text
globalThis.WordstatAutorunModel
```

Only a very small amount of its source is Wordstat-specific by name; its state machine, Start/Delivery commit phases, no-replay recovery decision, Pause/Finish semantics and prefix accounting are reusable CORE behavior.

Decision for Phase 1:

- preserve its state-machine semantics;
- make the product-level export generic (`MarketingAutorunModel` or equivalent);
- optionally expose a temporary compatibility alias while Wordstat regression tests are migrated;
- prove behavior with tests before removing any compatibility alias.

This file is **not** one of the four byte-identical Business Bridge modules, so genericization is allowed but must be differential-test driven.

## 7. Service-specific module

`shared/wordstat_protocol.js` is Wordstat adapter code, not CORE.

It owns:

- `WORDSTAT_API_V1` prefix;
- Wordstat method allowlist;
- method-specific input validation;
- endpoint mapping;
- request body construction;
- Wordstat command fingerprinting;
- Wordstat error envelope shaping;
- `WORDSTAT_RESULT_V1` formatting.

It remains service-specific under `WordstatAdapter` / Wordstat protocol boundary.

## 8. Mixed orchestration files

The three large runtime/UI files mix generic lifecycle logic with Wordstat-specific transport and UI text:

### `service_worker.js`

Generic responsibilities to extract/preserve:

- local storage helpers;
- single-flight primitive;
- diagnostics sanitation/storage;
- conversation identity and explicit binding;
- popup context validation;
- durable manual operation ownership;
- run storage/mutation locks;
- Start commit/confirmation/recovery;
- delivery claim/commit/confirmation/recovery;
- owner-tab decision/rebind;
- Pause/Resume/Finish;
- content-ready recovery;
- exactly-once request grant;
- worker-owned single-flight delivery attempt;
- send/copy profile management.

Wordstat-specific responsibilities to move behind adapter/config boundaries:

- API key + folder ID settings;
- Yandex Wordstat HTTP transport;
- `executeWordstatCore()`;
- Wordstat protocol parsing/building;
- Wordstat test connection;
- Wordstat-specific start prompt and status/error text.

### `content_script.js`

Generic responsibilities:

- conversation identity/context handshake;
- manual Copy activation using supplied shared controls;
- writing-block extraction;
- composer staging/send;
- committed Start reconciliation;
- committed Delivery reconciliation;
- stable assistant-block watcher;
- owner/run synchronization;
- manual delivery recovery;
- Send/Copy picker fallback;
- browser-side diagnostics.

Wordstat-specific responsibilities:

- `WordstatProtocol` validation;
- `WORDSTAT_API_V1` check;
- Wordstat-specific toasts/labels/runtime name;
- command metadata extraction currently tied to Wordstat fields.

### popup

Generic responsibilities:

- explicit conversation bind status/action;
- Manual / Autorun controls;
- Pause / Resume / Finish;
- run state display;
- diagnostics;
- copy/send fallback selectors.

Wordstat-specific responsibilities:

- Yandex API key/folder ID fields;
- Wordstat labels/help;
- Test API action;
- Wordstat prefix/start-prompt wording.

## 9. Critical invariants inherited from reference

The unified bridge must retain, with tests:

1. explicit confirmed-conversation binding before side effects;
2. conversation identity separate from owner tab;
3. duplicate tab cannot steal a live owner;
4. dead/stale owner recovery preserves the same durable transaction;
5. native local Copy remains native Copy;
6. generic `Copy response` is never an API trigger;
7. Manual and Autorun mutual exclusion;
8. stable new writing-block capture before command acceptance;
9. atomic grant before billable/side-effect execution;
10. worker-owned single-flight delivery;
11. durable commit before browser Send click;
12. committed Send is reconciliation-only and never grants a second click;
13. service-worker loss during uncertain paid request is fail-closed/no retry;
14. user composer is never silently overwritten;
15. Pause/Finish never cause request replay;
16. result-prefix accounting is delivery-confirmation/idempotency based.

## 10. Phase 0 conclusion

The reference is sufficiently understood to begin Phase 1 without architectural guesswork.

Phase 1 must **not** start by rewriting the reference from scratch. It starts from the audited behavior, freezes the four byte-identical common modules, introduces a generic CORE around them, keeps Wordstat as the only active service, and proves parity plus the new unified policy/job/cost requirements before any Search code is introduced.
