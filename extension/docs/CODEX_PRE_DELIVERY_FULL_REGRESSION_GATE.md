# Codex pre-delivery full regression gate — Yandex Marketing Bridge

Status: **MANDATORY / LIVING GATE**  
Adopted: 2026-08-18  
Updated: 2026-08-19 — external Yandex control + Ozon-parity Manual delivery lifecycle + exact-artifact transport/consumer-conformance hardening  
Scope: every installable Yandex Marketing Bridge build that is about to be handed to the owner as a working build/candidate.

## 1. Purpose and role boundary

This document is the permanent regression firewall before owner handoff. It is not the test policy for every intermediate edit.

**Role boundary is mandatory:** ChatGPT owns analysis, architecture, implementation, code changes, patching, packaging and development fixes. Codex is a **testing/QA executor only** for this gate. During the gate Codex must not design a fix, edit production code, patch tests to make failures pass, or substitute another candidate. Any product/test defect is returned to ChatGPT; after ChatGPT fixes it, a new exact candidate is frozen and the complete gate restarts from PD-00.

### Development mode

While ChatGPT is still changing code, run focused tests for changed behavior, affected dependencies, changed-line/branch coverage where appropriate, and relevant syntax/static checks. Do not run this whole gate after every edit.

### Pre-delivery mode

After ChatGPT freezes the exact candidate, Codex executes **all enabled PD-00…PD-17 sections in one complete campaign against that exact candidate**. Any mandatory FAIL blocks owner handoff. No partial historical PASS transfers across a production-byte change.

## 2. Living-document rule

Whenever product functionality changes, update this registry in the same governed change. Add coverage for new behavior, update changed behavior, remove obsolete tests only when the corresponding product behavior is intentionally removed, and never delete a test merely because it fails. Missing Codex-capable coverage for an existing functional surface is a gate FAIL.

This revision supersedes the obsolete Manual-sibling / sent-user-turn `manual_reconcile` gate wording. Manual delivery now follows the proven Ozon-style Send→ready/Microphone lifecycle; Manual `manual_reconcile`, its 12-attempt retry budget and `MANUAL_DELIVERY_RECONCILIATION_RETRY_EXHAUSTED` are not valid current behavior.

## 3. Codex capability boundary

Qualified controlled capabilities include repository/source/hash inspection; Node/VM/unit/integration tests; JS/MJS syntax; JSON/manifest validation; deterministic packaging and source↔package identity; Chrome for Testing + Puppeteer; runtime extension installation; MV3 worker/content/popup checks; controlled factual ChatGPT DOM fixtures; popup/storage lifecycle; multi-tab/conversation ownership; worker lifecycle/recovery; controlled network interception/stubs/fault injection; console/network diagnostics; and dedicated QA-profile persistence.

Controlled evidence is never relabeled as owner real-profile/live evidence. Unless a future governed revision explicitly changes this rule, the full gate uses **zero real Yandex requests and no real credentials**.

Browser/CfT is mandatory for browser-owned surfaces: DOM binding, extension installation, popup, MV3/content loading, native Copy, external Yandex control, placement, mutation lifecycle and visible plaques. Deterministic content↔worker integration is mandatory for internal asynchronous states that cannot be reliably manufactured in the qualified browser fixture. Moving a regression between qualified layers must not weaken assertions or fabricate live evidence.

### 3A. QA transport, harness and gate-authoring failure-prevention rules

These rules are permanent because failures in the 2026-08-19 pre-delivery campaign showed that a correct product can still be blocked or falsely classified by a bad QA handoff. The purpose of this subsection is to prevent ChatGPT from repeating those QA-engineering mistakes when creating future tests or gates.

#### A. The exact handoff artifact is the primary QA input

When ChatGPT has already produced the exact installable ZIP intended for owner handoff, Codex must test **those exact ZIP bytes** whenever transport to Codex is possible. ChatGPT must make the exact artifact available through a Codex-accessible transport and publish its expected SHA-256 and byte count.

Do **not** replace an available exact handoff ZIP with a preimage+patch reconstruction merely for convenience. Reconstruction is a fallback only when transporting the exact artifact is genuinely impossible.

Reason: during the 2026-08-19 campaign ChatGPT had already frozen artifact SHA-256 `31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14`, but initially failed to place those exact bytes where Codex could access them. That unnecessary reconstruction path created avoidable artifact failures before product testing.

#### B. Never make the owner transport QA files

The owner action for this workflow is prompt-only. ChatGPT must never require the owner to download, upload, copy, move, extract, install, rename or stage QA artifacts for Codex.

ChatGPT owns transport design. Codex owns QA execution. If transport is broken, ChatGPT fixes the transport; the owner is not used as a file courier.

#### C. Exact-byte reconstruction must be byte-safe and cross-platform

If reconstruction is unavoidable, the reconstruction protocol must define and verify exact bytes, not merely logical text content. It must account for line endings, encodings, path separators, timestamps, permissions and archive metadata.

The 2026-08-19 reconstruction failure is a permanent regression lesson: applying the frozen patch on Windows produced CRLF-normalized `content_script.js` and `service_worker.js`. Their SHA-256 values differed even though logical code was equivalent. A candidate with the wrong bytes is not the frozen candidate.

Therefore:
- every reconstruction input has a published SHA-256 and byte count;
- the final tree has a complete file-path + SHA-256 manifest, not only two representative hashes;
- exact postimage identity is verified before any product test receives PASS credit;
- EOL normalization, text-mode rewriting or archive-tool metadata changes are forbidden unless they are explicitly part of the canonical build procedure;
- any ungoverned byte change is `FAIL_ARTIFACT`, not a product failure.

#### D. Deterministic packaging procedure must be recorded before the gate

If the handoff artifact is expected to be reproducible, ChatGPT must define the deterministic packer before Codex runs PD-03. The procedure must include archive root, path order, directory-entry policy, compression method/level, timestamps, separators **and every byte-affecting ZIP metadata field used or derived by the chosen implementation**.

The 2026-08-19 campaign showed that a source tree can be `45/45` byte-identical after extraction while a ZIP itself still has a different SHA because another archiver emitted different metadata. Codex must not be expected to guess the packer.

A prose description such as “dirs 0755 / files 0644” is not byte-complete. For ZIP reproduction the canonical authority must explicitly fix, where applicable, `create_system`, UNIX file-type bits (`S_IFDIR`/`S_IFREG`), `external_attr` including DOS directory flag, entry ordering, explicit directory entries, compression behavior, general-purpose flags, filename encoding, timestamps, creator/extract versions, extra fields, comments and any other implementation-dependent metadata capable of changing archive bytes.

For the 0.1.1 candidate that ultimately passed, the canonical artifact was reproduced byte-for-byte at SHA-256 `31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14`, 209697 bytes. Future releases must record their own canonical artifact identity and procedure.

#### E. Test design must stay within demonstrated Codex capabilities

Before freezing a candidate, ChatGPT must verify that every mandatory gate assertion has a concrete execution venue available to Codex. Do not write a mandatory gate step that depends on an assumed capability and discover only during pre-delivery that Codex cannot execute it.

For each mandatory assertion, the gate/test registry must identify one of:
- source/static;
- Node/VM/unit;
- deterministic content↔worker integration;
- controlled network stub/fault injection;
- qualified Chrome for Testing + Puppeteer browser runtime;
- package/extraction identity;
- another explicitly demonstrated Codex-capable venue.

Codex may use a technically equivalent invocation of an already-defined test because of local paths/environment, but Codex must not invent the test objective, weaken it, or silently move a browser-owned assertion into source review.

#### F. Browser capability means executable CfT/Puppeteer, not a UI button

A missing high-level/in-app browser control does not prove that browser QA is unavailable. If the gate requires CfT/Puppeteer, the QA design must specify or preserve a known executable browser harness accessible from Codex's shell/workspace.

The 2026-08-19 campaign demonstrated a working qualified harness at the Codex side using Chrome for Testing and Puppeteer even though an earlier run reported only an in-app browser. The earlier classification was a harness-discovery failure, not an artifact failure.

Future gate authoring must therefore record enough harness information for Codex to launch the qualified browser without inventing a new test architecture.

#### G. Every PD section must have an executable coverage map before freeze

A prose requirement is not enough. Before pre-delivery freeze, ChatGPT must ensure there is an executable mapping from every enabled `PD-00…PD-17` section to the concrete tests/harness scenarios that prove it.

The mapping may reference multiple layers. Example: a browser-owned lifecycle can use CfT/Puppeteer while rare internal recovery state can use deterministic content↔worker integration. The combination is valid only when it proves every assertion without weakening it.

The 2026-08-19 campaign reached PD-06 with exact source, exact package and working CfT/Puppeteer, then returned `NOT_RUN` for PD-07…PD-17. That was a QA/gate execution failure: the remaining requirements were present in prose and much of their coverage already existed in the 361-test suite, but the campaign did not have a sufficiently explicit execution map. This must not recur.

#### H. Codex executes the gate; ChatGPT designs the tests and harness

Codex is not responsible for deciding what should be tested. ChatGPT must implement/update the tests and define the QA protocol before freezing the candidate.

Codex responsibilities are limited to executing the governed tests/harness, collecting evidence, classifying failures and returning PASS/FAIL. Codex must not be asked to design missing product tests, invent acceptance criteria, patch tests, or improvise weaker substitutes.

If a required test/harness is missing, that is a ChatGPT QA-engineering defect. Fix the QA layer first; do not transfer the design burden to Codex or the owner.

#### I. One campaign means no enabled `NOT_RUN`

The final campaign is not complete while any enabled PD section is `NOT_RUN`. Codex must continue through the entire matrix unless an actual blocking condition makes later evidence impossible or unsafe.

A normal assertion failure does not justify stopping unrelated sections; collect the complete failure set when safe.

A final result containing enabled `NOT_RUN` cannot be `PASS` and must identify why execution could not continue.

#### J. Failure classes must describe the layer that failed

Use failure classes precisely:
- `FAIL_PRODUCT`: exact candidate established; a product assertion failed;
- `FAIL_ARTIFACT`: candidate/package/reconstruction byte identity failed;
- `FAIL_HARNESS`: exact candidate is valid but a required qualified test environment/harness cannot execute the governed assertion;
- `PASS`: every enabled mandatory section passed.

Do not label missing/unavailable browser harness as `FAIL_ARTIFACT`. Do not label an EOL/hash mismatch as `FAIL_PRODUCT`. Do not label an unexecuted matrix as product failure.

#### K. Do not regenerate the handoff artifact inside QA unless the gate explicitly tests reproducibility

If Codex already possesses the exact frozen handoff ZIP and its hash matches, that artifact is the package under test. Rebuilding another logically equivalent ZIP must not substitute for it.

A rebuild may additionally be performed for PD-03 deterministic-reproducibility evidence, but the final handoff identity remains the exact tested artifact. The package handed to the owner must be the same bytes Codex accepted.

#### L. QA-process fixes do not authorize product-byte mutation

When a campaign fails because of transport, packaging procedure, harness discovery, missing executable mapping or reporting, fix only the QA/process layer unless evidence proves a product defect.

Do not change frozen production bytes merely to make QA infrastructure easier to run. A production-byte change creates a new candidate and invalidates the previous product gate PASS set.

#### M. Pre-freeze / pre-Codex author checklist for every future patch

Before declaring a candidate frozen **or issuing a Codex QA prompt**, ChatGPT must answer YES to all applicable items:

1. Is the exact intended handoff artifact built and hashed?
2. Has the latest applicable proven transport route been identified and reused unless evidence proves it unavailable/inapplicable?
3. Can Codex obtain the exact frozen artifact bytes without owner file handling?
4. Has ChatGPT round-tripped the artifact through the same logical transport input Codex will consume?
5. Does the round-tripped artifact match expected SHA-256 and byte count?
6. Does the round-tripped archive open and pass integrity/extraction identity checks?
7. If exact ZIP bytes are encoded for transport, has a fresh consumer reassembled the exact expected ZIP from only published chunks/instructions?
8. If reconstruction is used, has evidence proven that no byte-safe exact-artifact transport is available?
9. If reconstruction is used, is the canonical packer executable/byte-complete rather than an underspecified prose recipe?
10. If reconstruction is used, has an independent consumer using only published inputs reproduced the exact expected ZIP SHA/bytes before Codex is asked to run?
11. Is complete source/postimage identity recorded?
12. Does every enabled PD section map to concrete executable tests/harness steps?
13. Are all browser-owned assertions backed by a known qualified CfT/Puppeteer route?
14. Are internal asynchronous assertions assigned to deterministic integration tests where browser manufacture is unreliable?
15. Can Codex execute the whole matrix with its demonstrated tools rather than assumed tools?
16. Are failure classifications unambiguous?
17. Does the final result schema forbid silently treating `NOT_RUN` as PASS?
18. Will the owner perform no QA file transport or environment setup?
19. Will the exact artifact handed to the owner be the exact artifact that received full-gate PASS?
20. Have product bytes remained unchanged during any transport/packaging-process repair unless a separate product defect required a new candidate?

If any applicable answer is NO, the candidate is **not ready for Codex pre-delivery gate execution**. ChatGPT must repair the QA design/transport first and must not give the owner a Codex prompt.

#### N. Proven-route reuse is mandatory

A transport path that previously carried an exact artifact into Codex and reached actual gate execution is a demonstrated capability. Before inventing a new transport, branch, reconstruction protocol or packaging route, ChatGPT must inspect that successful evidence and reuse the same mechanism when still applicable.

The successful `31cc5f3f…` campaign that reached complete Codex execution is the canonical 2026-08-19 example. A later failure must not be answered by forgetting that route and improvising a new one unless the old route is first shown by evidence to be unusable for the current artifact.

#### O. Exact-artifact transport precedence and mandatory round-trip

For a frozen ZIP, mandatory precedence is:

```text
1. proven direct exact-ZIP route;
2. another verified byte-safe direct exact-ZIP route;
3. byte-safe text encoding of the EXACT ZIP bytes, reassembled to the original ZIP;
4. source/preimage reconstruction only when exact artifact transport is genuinely impossible.
```

Before a Codex prompt is issued, ChatGPT must publish the selected input and then **read/download/reassemble it back through the same logical route**. A successful upload/API/blob/commit response is not evidence of byte identity.

Required round-trip result before prompt:

```text
SHA == frozen expected SHA
bytes == frozen expected bytes
archive integrity/open == PASS
fresh extraction identity == PASS where applicable
```

The 14999-byte non-ZIP GitHub object that was mistakenly treated as the 209505-byte `e13a…` candidate is a permanent negative regression case. The prompt was unauthorized because no round-trip artifact proof had occurred.

#### P. Reconstruction requires consumer-conformance, not producer confidence

If exact artifact transport is genuinely impossible and reconstruction is unavoidable, ChatGPT must verify the **published handoff contract as an independent consumer would** before Codex receives a prompt:

```text
fresh location/process
+ only published transport objects/instructions
+ explicitly governed preexisting input
→ reconstruct/reassemble
→ exact target source identity
→ exact expected package SHA
→ exact expected byte count
→ archive integrity/open
```

Hidden local packer state, unpublished defaults, or knowledge available only to the producer invalidates this proof.

The `8359c6cf…` reconstruction failure is a permanent negative regression case: source tree `45/45` and archive size `209505` were insufficient because the packaging contract omitted byte-affecting ZIP metadata. `45/45` source identity does not substitute for exact package identity.

#### Q. Transport/process failure cannot be delegated to Codex discovery

Codex is not the probe used to discover whether ChatGPT's newly invented transport works. Transport viability, exact artifact accessibility and reconstruction sufficiency are ChatGPT QA-engineering responsibilities and must be proven before prompt handoff.

A `FAIL_ARTIFACT` caused solely by an unverified transport/reconstruction path is a ChatGPT process failure. On retry, keep production bytes frozen, fix only the proven artifact/transport/packaging/prompt layer, run the required round-trip/consumer-conformance proof, and only then authorize another complete Codex campaign.

## 4. Run discipline

Before testing, freeze and record the exact source/candidate identity. Do not modify production bytes during the gate. Test source and the fresh extracted handoff ZIP when a ZIP is the handoff artifact. Do not stop at the first ordinary assertion failure when continuing safely can collect the complete failure set. Do not skip a section because an older candidate passed it.

Allowed final states are `PASS`, `FAIL_PRODUCT`, `FAIL_ARTIFACT`, `FAIL_HARNESS`. Only `PASS` permits handoff.

---

# 5. Mandatory full regression matrix

## PD-00 — Authority, freeze and exact identity

Record live GitHub HEAD/governed authority; exact candidate source/reconstruction authority; manifest version; file count; source hashes; reconstruction inputs; and prove no stale historical candidate was substituted.

## PD-01 — Complete source regression suite

Run the entire current source suite. Require 0 failures and 0 skipped/cancelled tests unless an explicit governed skip exists. Record total/pass count and prove all tests added for the current patch are included.

## PD-02 — Static, syntax and manifest integrity

Require every JS/MJS to parse; every governed JSON to parse; manifest validity; every manifest-declared entrypoint/resource to exist; version consistency; governed permission/host-permission surface; and no accidental extra production entrypoint/file.

## PD-03 — Package/reconstruction integrity

Use the already frozen exact handoff ZIP as the primary package under test whenever its bytes can be transported. A reproducibility rebuild is additional evidence only and may not substitute for the primary exact artifact.

If reconstruction is exceptionally authorized under section 3A, build/reconstruct using the governed byte-complete executable procedure, require the pre-Codex consumer-conformance proof, and independently reproduce expected exact SHA/bytes before product PASS credit is possible. Where supported, build A and B and require byte identity. Freshly extract the exact handoff ZIP; require source↔package path set and bytes to match exactly; run the complete packaged suite plus syntax/JSON/manifest checks; record filename, SHA-256, bytes and file count. If reconstruction uses an exact preimage + patch, reproduce it from a fresh preimage and require final-tree byte identity **and exact expected package-byte identity**.

## PD-04 — Runtime installation and MV3 lifecycle

Using qualified CfT/Puppeteer, install the exact frozen unpacked source; verify extension identity/version, MV3 service worker, content script on controlled ChatGPT URL, popup initialization, no unexpected runtime errors, and a safe worker restart/lifecycle contour.

## PD-05 — Popup/settings behavior

Verify all present controls and persistence semantics, including Manual, Debug, Auto Send, Wordstat Autorun policy, report-prefix toggle, explicit-Save text/credential fields, popup reopen truth, and conversation isolation. Toggle changes must not accidentally commit unrelated unsaved fields.

## PD-06 — Manual action surface / ChatGPT DOM binding

On the current governed ChatGPT DOM families, browser-test all of the following:

- Manual OFF leaves native ChatGPT Copy byte/state/event behavior untouched and leaves no Bridge-owned action residue.
- Manual ON creates exactly one Bridge-owned **external** Yandex action for each structurally/uniquely bound eligible block.
- The action is hosted on the Bridge-owned external surface/Shadow DOM, visually outside/to the right of the block (`rect.right + 10` when room exists, governed inside fallback otherwise), and is not a child/sibling-lifecycle derivative of native Copy.
- The action is visibly labeled `Яндекс`, yellow when ready, and is a different DOM element/lifetime owner from native Copy.
- A newly rendered eligible PRE/code block receives an enabled Yandex action **before native Copy exists**.
- Full native Copy lifecycle regression is permanent: `PRE before Copy → Yandex immediately enabled → Copy appears → Copy checkmark/state change → Copy removed → replacement Copy appears`; the **same Yandex action identity** remains connected/enabled throughout.
- Native Copy receives no Bridge Manual listener/style/title mutation and clicking native Copy produces exactly 0 `WS_EXECUTE_MANUAL_BLOCK`.
- Clicking Yandex produces exactly 1 intended Manual admission; duplicate/in-flight clicking is fenced.
- Generic whole-response Copy is excluded from Bridge execution.
- Local Copy missing/ambiguity is diagnostic only for an otherwise structurally bound external Yandex control; it must not lifecycle-gate that control. Structural/assistant binding ambiguity still fails closed.
- Mutation-added/replaced blocks are discovered; detached block roots lose their Bridge control; repeated rescans do not duplicate controls/listeners.
- Manual OFF removes only Bridge-owned controls; re-enable creates exactly one control again.
- Runtime/status plaque root is **top-right** (`right:18px; top:18px`).
- Same logical status uses a stable key and does not stack on repeated scans/events. At minimum verify `operation-state`, `composer-occupied`, `autorun-state`, and `picker-state` behavior.

Current factual family must include current ChatGPT PRE/readonly-CodeMirror plus still-supported legacy adapters. This section is browser-owned and cannot be replaced by source-only assertions.

## PD-07 — Manual full-block discovery and content→worker behavior

Through actual controlled content→worker flow verify: only external Yandex authorizes Manual; native Copy authorizes none; whole bound block is captured; plain/raw/malformed/valid/multi-command blocks are worker-owned and deterministic; balanced/string-aware extraction; source-order serial semantics; no hidden parallel fan-out; one click creates one transaction; duplicate/in-flight fence; generic response Copy no dispatch; structural/conversation ambiguity fails closed. Zero real Yandex requests.

## PD-08 — Wordstat protocol / all Phase-1 operations

For `getTop`, `getDynamics`, `getRegionsDistribution`, `getRegionsTree`, with controlled stubs/faults verify strict validation, registry allowlist, fixed endpoint/host, body construction, Folder-ID semantics without secret exposure, response parsing, HTTP propagation, operation/request identity, success/error contours, no automatic hidden retry, and no hidden pagination/fan-out.

## PD-09 — Policy, credentials, cost and accounting

Verify missing credentials/local validation/policy/request/cost ceilings fail before provider initiation; correct `request_executed:false|true|"UNKNOWN"`; `automatic_retry:false`; conservative unknown-outcome accounting/no blind retry; exactly-once counters; standalone Manual has no invented Job/GitHub runtime dependency; paused RUN/manual shares governed RUN ceilings where applicable.

## PD-10 — Autorun lifecycle

Using actual popup + installed extension + controlled ChatGPT fixture, verify policy persistence; exactly one RUN; waiting state; popup reopen identity/counters; command pickup without local Copy; exactly-once controlled result/error delivery; recoverable safe state; Pause/Resume/Stop; stopped RUN ignores later blocks; conversation/tab ownership; safe reload/worker restart; and current Manual/Autorun coexistence rules. All automatic Autorun plaques use the stable `autorun-state` key and do not stack.

## PD-11 — Manual delivery FSM, durability and duplicate prevention

Permanent current Manual regressions:

### A. Normal auto-send terminal release

`Manual admission → worker result/error → one delivery commit → current recognized Send clicked at most once → no second WS_EXECUTE_MANUAL_BLOCK/provider initiation → ChatGPT composer control transitions to ready/Microphone → exactly one WS_MANUAL_DELIVERY_COMPLETE with delivery_confirmed:true, confirmation_basis:"microphone", composer_empty:true → Manual worker lock releases → next Manual Yandex action is immediately admissible.`

Assertions: Send count exactly 1 for the admitted delivery; provider/block execution count unchanged after admission; no chat-history sent-user-turn search is required for Manual completion.

### B. Already-committed recovery is watch-only

`Committed Manual delivery recovered → watcher observes composer controls only → Send count remains 0 → delivery commit count remains 0 → WS_EXECUTE_MANUAL_BLOCK/provider count remains 0 → later ready/Microphone appears → exactly one confirmed completion → lock releases.`

Recovery must never click Send or re-initiate Yandex/API work.

### C. Occupied/missing composer preservation

`Manual report is worker-owned while composer contains user text or is temporarily unavailable → user text remains byte-for-byte unchanged → one persistent keyed "Очистите поле ввода, чтобы получить отчёт." plaque → repeated DOM events do not stack it → DOM-change/bounded fallback wakeup → when composer becomes empty, report proceeds exactly once → no block/provider replay.`

### D. Genuine active/unresolved fence

While provider/requesting work or another genuinely active Manual operation remains unresolved, new Manual admission returns/retains `MANUAL_OPERATION_ACTIVE`; Manual OFF must not falsely erase requesting/provider/committed work. Unknown irreversible provider outcome is never cleared by timeout.

### E. Cancellation boundary

Manual OFF may cancel only a claimed/pre-commit pending Manual report where governed; it must not erase requesting/provider work or an already committed delivery.

### F. Truthful execution provenance

Validation-only/zero-provider committed deliveries preserve truthful `request_executed:false`; successful provider initiation remains true; unknown stays `"UNKNOWN"`.

Also retain normal result/error exactly-once delivery, always-on error delivery independent of Debug, durable outbox/restart behavior, claim/commit boundaries, pre-commit failure preservation, duplicate content-ready recovery dedupe, double-click provider dedupe, and unknown-outcome fingerprint fence.

The exact source and fresh package tests must cover these assertions. The obsolete Manual `manual_reconcile` and 12-retry exhaustion tests are forbidden as current acceptance criteria.

## PD-12 — Debug/error contract

With zero-provider controlled errors, Debug OFF still automatically delivers concise `YMB_ERROR_V1`; Debug ON delivers the same error plus useful redacted diagnostics. No credentials/tokens/Authorization/storage secrets. Cover representative parse/validation/policy/credential/delivery/unknown-outcome errors.

## PD-13 — Conversation/tab/ownership isolation

Verify confirmed binding, no tab stealing, duplicate-tab fail-closed behavior, local block isolation, no cross-PRE/cross-assistant binding, governed reload/rebind, stale identity rejection, and no accidental global current-conversation state.

## PD-14 — Export/import, migration and persistence

Verify export schema/metadata/checksum; untampered accept/tampered reject; intentional backup-secret containment; no secrets in ChatGPT/debug/GitHub-facing payloads; cross-install restore; same-folder upgrade persistence; import cannot overwrite active RUN/manual safety state unsafely; required legacy `wsmb_*` compatibility; and current text/toggle semantics.

## PD-15 — Security/provider-surface containment

Verify no secrets in page/content/result/error/debug evidence; assistant content cannot choose arbitrary URL/method/headers/auth; provider hosts/operations are explicit allowlists; unsupported operations fail pre-network; no runtime GitHub token/repo/branch/job requirement; backup secret isolation; real Yandex request count 0.

## PD-16 — Future-service phase locks

Until explicitly enabled, Search, Webmaster, Metrika and Direct cannot execute provider requests from assistant content. Recognizing a future marker must not enable execution. When a phase is enabled, replace its lock with full functional coverage.

## PD-17 — Final artifact cleanliness/evidence

At gate end re-check exact production hashes/path set; prove candidate did not mutate; record repository/test working state; real Yandex requests exactly 0; no secrets in reports; every PD section explicit; no NOT_RUN/UNKNOWN silently treated as PASS. Produce one final Markdown + JSON report with full matrix and exact artifact identity.

---

# 6. Required final verdict

Codex returns one final result for the entire campaign:

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
verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

`PASS` is valid only if every enabled mandatory section passes and the exact handoff artifact is the exact tested artifact.

# 7. Handoff rule

ChatGPT must not present an installable candidate to the owner as a working build until the latest exact frozen candidate has a fresh `PASS` from this full gate. Historical PASS is not transferable. Owner real-profile/live acceptance remains a separate later classification and this gate never fabricates it.

## 8. v0.1.3 Webmaster KW-001 read-surface mandatory delta coverage

When `product_version >= 0.1.3`, the full gate additionally requires all of the following without weakening PD-00…PD-17:

```text
WEBMASTER_V013_PROTOCOL_AND_VALIDATION = PASS
WEBMASTER_V013_OLD4_COMPATIBILITY = PASS
WEBMASTER_V013_QUERY_HISTORY = PASS
WEBMASTER_V013_INDEXING_AND_IN_SEARCH_SAMPLES = PASS
WEBMASTER_V013_EXPORT_METADATA = PASS
WEBMASTER_V013_EXPORT_PROJECTION_AND_CONFIRMATION_GUARDS = PASS
WEBMASTER_V013_EXPORT_POST_NO_AUTO_RETRY = PASS
WEBMASTER_V013_DURABLE_TASK_RECOVERY = PASS
WEBMASTER_V013_SIGNED_DOWNLOAD_ALLOWLIST = PASS
WEBMASTER_V013_CSV_RAW_AND_NORMALIZED_PERSISTENCE = PASS
WEBMASTER_V013_CHUNKED_LOCAL_READ = PASS
WEBMASTER_V013_LOCAL_COMMAND_REQUEST_EXECUTED_FALSE = PASS
WEBMASTER_V013_REMOTE_COMMAND_REQUEST_EXECUTED_TRUE = PASS
WEBMASTER_V013_MANUAL_PROVIDER_ACCOUNTING_TRUTH = PASS
WEBMASTER_V013_POPUP_POLICY_PRESERVATION = PASS
WEBMASTER_V013_POLICY_MIGRATION = PASS
WEBMASTER_V013_WORDSTAT_SEARCH_METRIKA_DIRECT_REGRESSION = PASS
WEBMASTER_V013_EXACT_ARTIFACT_IDENTITY = PASS
```

The controlled gate must stub every Yandex endpoint. Real provider requests remain `0`. A successful `startQueryUrlExport` POST is stateful: network outcome uncertainty must remain `REQUEST_OUTCOME_UNKNOWN_NO_RETRY`; an automatic retry is forbidden. `collectQueryUrlExport` may download only a URL previously returned by the official status endpoint and accepted by the exact `https://storage.mds.yandex.net/get-webmaster-download/` allowlist. Local projection/manifest/chunk/job-list commands must not increment physical provider request accounting.
