# CODEX_YANDEX_MANUAL_LIVE_FIX_FOCUSED_2026-08-18

## Result

Focused exact-patch validation PASS.

## Authority and base

- `origin/main`: `8f307f8f9fa7706790e9df053d0f5716782652e1`
- Frozen base: `D:\codex\Yandex\work\manual-surface-v2-validation-002\manual-v2\source`
- Fresh working source: `D:\codex\Yandex\work\manual-v2-live-fix-014\source`
- Base identity: PASS; 45 files; manifest version `0.1.1`.
- Frozen base unchanged: PASS.
- READY_TO_INSTALL read-only check: unchanged.

Base audited hashes:

- `content_script.js`: `03826461d0f8bd7a00ddf653b505d333755002d22a827d9ee286103321f746f4`
- `service_worker.js`: `4be10f692faf72880fc50abd3f32b97538c14b4c4afc59a9ddd22a48a3ae14c8`
- `shared/block_command_discovery.js`: `6375736431b06ce7029ea17fae0c64ac35c0adb1972890a97101230473d94434`
- `shared/manual_controls.js`: `01882215246e8ff5239fec438ef608220161008054a4ea6f5f6bbf1864ecc3b3`
- `shared/wordstat_protocol.js`: `044f2fb2733a48e915eacc9da01f004c24d083d6a1899812b2074a0d19e7cd85`

## Exact patch

- Raw patch SHA-256: `4dc0f5a40ea816fe9a3000ec62f0fe914377b41e8cac1e2dda4aea5f0f664c55`
- Raw patch bytes: `38330`
- `git apply --no-index --check`: PASS
- Applied to fresh working source: PASS
- Exact changed files: 4.
- Production changed files: exactly `content_script.js`.
- No extra changed files.

Post-patch hashes:

- `content_script.js`: `d942bcbfeaa2f3a77f21f3f0191ed807434fe6d342780bd3a6dd5ea4336728ed`
- `tests/content_runtime_exhaustive.test.mjs`: `acf7b18dc11258f5fdd9a6eeaeeca93e419ac938e0f14cbbecd4144bf8f9bc0e`
- `tests/manual_mode.test.mjs`: `7ab31c21e73f927c0cf8cbfce0baa9038f10ccecf6be02c5f1485f5ca6ce21d9`
- `tests/manual_surface_v2_worker.test.mjs`: `65794d1349aa18ae43d876f7929cda355d33d64577eca4bbf503b7d73fd38987`
- `service_worker.js` unchanged: `4be10f692faf72880fc50abd3f32b97538c14b4c4afc59a9ddd22a48a3ae14c8`

The four patched files were normalized to LF in the fresh working copy so their mandated post-patch hashes match exactly; patch content was not changed.

## Syntax and focused tests

- `content_script.js` syntax: PASS
- `service_worker.js` syntax: PASS
- One exact `node --test` invocation: PASS
- Tests passed: 183/183
- Failed: 0
- Skipped: 0
- Cancelled: 0

Named regressions:

- Separate Yandex sibling action: PASS
- Native Copy remains independent: PASS
- Manual OFF removes only Yandex-owned action: PASS
- Late-delivery reconciliation performs no resend/replay: PASS
- Lock release admits the next Manual operation: PASS

## Safety observations

- Send count in reconciliation test: `1`
- Extra Manual execute during reconciliation: `0`
- Provider fetch count: `0`
- Real Yandex requests: `0`
- Browser tests: not run.
- Full PD-00…PD-17 regression gate: not run.
- New ZIP: not created.
- Git commit: not created.
- GitHub production modified: NO.
