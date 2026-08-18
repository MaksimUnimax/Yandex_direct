# CODEX_YANDEX_MANUAL_LIVE_FIX_CONTROLLED_BROWSER_2026-08-18

## Verdict

`CONTROLLED_BROWSER_HARNESS_FAIL`

The product source identity and source-focused validation remained PASS. Browser A
completed on the specified CFT/Puppeteer engine and all independent sibling
control assertions passed. Browser B/negative-fence could not be accepted because
the external CFT/Puppeteer harness became unstable after the bounded run: later
restarts hit `TargetCloseError` and `Runtime.callFunctionOn timed out` during
popup binding. No product failure is inferred from that harness failure.

## Governance

- Initial `origin/main`: `8f307f8f9fa7706790e9df053d0f5716782652e1`
- Governed commit: `ca38480ca3dc049e3b29671fa83ae275aed35a1d`
- `HEAD == origin/main`: PASS at governance publication.
- Governance commit contains only docs, patch authority, manifest and focused evidence.
- Product extension source was not committed.

## Patch and source

- Patch SHA-256: `4dc0f5a40ea816fe9a3000ec62f0fe914377b41e8cac1e2dda4aea5f0f664c55`
- Patch bytes: `38330`
- Patched source: `D:\codex\Yandex\work\manual-v2-live-fix-014\source`
- Source files: `45`
- `content_script.js`: `d942bcbfeaa2f3a77f21f3f0191ed807434fe6d342780bd3a6dd5ea4336728ed`
- `service_worker.js`: `4be10f692faf72880fc50abd3f32b97538c14b4c4afc59a9ddd22a48a3ae14c8` unchanged.

## Focused source validation

- Syntax: content script PASS; service worker PASS.
- Tests: `183/183 PASS`, fail `0`, skipped `0`, cancelled `0`.
- The exact nine-file source set was rerun once after all external harness edits.

## Browser engine

- Puppeteer: `25.4.0`
- Chrome for Testing: `151.0.7922.47`
- Observed browser version: `Chrome/151.0.7922.47`
- Extension install: PASS.
- MV3 worker: PASS.
- Product source under test was the patched working source, not READY_TO_INSTALL.

## Browser A — independent controls

- Eligible blocks: `7`
- Native Copy count: `7`
- Yandex sibling count: `7`
- Native Copy and sibling distinct elements: PASS.
- Native Copy unchanged: PASS.
- Native Copy Manual dispatches: `0`.
- Yandex sibling Manual dispatches: `1`.
- Generic whole-response excluded: PASS.
- Ambiguous block excluded: PASS.
- Manual OFF removes only Yandex siblings: PASS.
- Re-enable idempotence: PASS.
- Mutation creates one sibling: PASS.
- Real Yandex requests: `0`.

## Browser B and negative fence

The browser harness did not produce admissible completion evidence for these
sections. The last completed partial matrix recorded:

- Initial confirmation missed: FAIL/not proven.
- Send clicks observed: `2`.
- Reconciliation attempts observed: `0`.
- Extra `WS_EXECUTE_MANUAL_BLOCK`: `0`.
- Provider requests: `0`.
- First operation terminal/completed: FAIL/not proven.
- Second Manual admitted: PASS in the partial run, but not sufficient to close B.
- Negative unresolved fence: FAIL/not proven.
- Negative extra Send: `0`.
- Negative extra first-operation execute: `0`.
- Negative provider requests: `0`.

The harness-only runner used a synthetic UTF-8 ChatGPT PRE/CodeMirror fixture,
the actual popup binding flow, and a harness-side MV3 worker `fetch` stub for
controlled provider behavior. No production file was changed. The fixture
charset correction and runner changes were external Yandex-adapter changes only.

## Safety and governance state

- Real Yandex requests: `0`.
- Product modified during browser QA: `0`.
- Shared Ozon engine modified: `NO`.
- Yandex external harness modified: `YES` (`projects/yandex/controlled-browser-015.mjs` only).
- READY_TO_INSTALL modified: `NO`.
- Full PD-00…PD-17 gate: not run.
- Final ZIP: not built.
- Issues #1/#2: not closed.
- Phase 1 LIVE PASS: remains FALSE.
- Search: remains BLOCKED.
