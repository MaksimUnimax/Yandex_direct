# B19 — patched file-delivery owner handoff — 2026-09-13

## Handoff state

- `PATCHED_FINAL_PACKAGE_GATE = PASS`
- `TARGETED_TEST15_CONTROLLED_CHROME = PASS`
- `INDEPENDENT_CODEX_GATE = WAIVED_BY_OWNER`
- `OWNER_LIVE_SMOKE = READY`
- `LIVE_TEST_15 = PENDING_OWNER_BROWSER`
- `FINAL_RECIPIENT_ACCEPTANCE = OPEN`

This handoff does not claim live ChatGPT owner-browser acceptance yet.

## Exact installable candidate

- filename: `Yandex-Marketing-Bridge-0.1.6.zip`
- source commit: `64c1016c179de52b6e950830877f0d42a446e5e8`
- product-tree SHA-256: `55bc2082a697598187ded73a5eaf3b18fa6a4e007eec25319690e4c9bb480f24`
- ZIP SHA-256: `3e23a70d09fab91f84cf3c9998499ce078f1467b46540dbac7fa07ac60a6765e`
- ZIP bytes: `225373`
- product files: `67`

Qualified outer evidence artifact:

- name: `ymb-0.1.6-patched-final-owner-candidate-v2`
- Actions run: `34752588385`
- artifact ID: `10316386455`
- outer artifact SHA-256: `8f1bedb1c71bd18b6829505e41a060fdf13232c553fcd551705616082781d9cb`
- outer artifact bytes: `234428`

## Qualification facts

- deterministic dual ZIP build: `PASS`
- source ↔ fresh-extraction identity: `PASS`
- syntax: `PASS`
- controlled targeted TEST-15 regression: `PASS`
- B19 real-Chrome resource matrix: `16/16 PASS`
- B19 controlled deferred-network matrix: `9/9 PASS`
- browser cleanup: `PASS`
- real provider calls during qualification: `0`
- downloaded artifact readback: `PASS`

## Owner live TEST-15

Use the newly installed candidate, reload the ChatGPT conversation after extension reload, and do not manually press Send while observing this test.

Command:

```text
SEARCH_ASYNC_BATCH_API_V1
{"action":"exportPage","jobId":"owner-smoke-016-01","after":-1,"limit":25}
```

Expected behavior:

1. the operation remains local/provider-free for this preserved export (`request_executed=false`, `provider_calls=0`);
2. the JSON export file is attached;
3. attachment reaches ready state;
4. the extension presses Send automatically exactly once;
5. exactly one new owner-visible user turn appears containing the result text/file;
6. there is no duplicate Send / duplicate user turn;
7. no manual Send click is required.

Owner evidence to record after the test:

- exact result text;
- delivered filename;
- whether Send was automatic;
- count of visible user turns created by this operation;
- whether any duplicate appeared;
- whether any manual click was needed.

Do not claim `LIVE_TEST_15=PASS` until these owner-browser facts are observed.
