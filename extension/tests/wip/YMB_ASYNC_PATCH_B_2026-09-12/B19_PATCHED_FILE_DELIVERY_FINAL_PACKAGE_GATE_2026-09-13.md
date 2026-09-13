# B19 — patched file-delivery final package gate — 2026-09-13

## Scope

This checkpoint qualifies the file-delivery Send hardening rooted at product source commit:

- `64c1016c179de52b6e950830877f0d42a446e5e8`
- product branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
- extension version: `0.1.6`

No provider acquisition was permitted or performed by this qualification pass.

## Exact product identity

- product files: `67`
- product-tree SHA-256: `55bc2082a697598187ded73a5eaf3b18fa6a4e007eec25319690e4c9bb480f24`
- installable ZIP: `Yandex-Marketing-Bridge-0.1.6.zip`
- installable ZIP SHA-256: `3e23a70d09fab91f84cf3c9998499ce078f1467b46540dbac7fa07ac60a6765e`
- installable ZIP bytes: `225373`
- deterministic dual-build identity: `PASS`
- source ↔ fresh-extraction byte identity: `PASS`
- ZIP integrity/readback: `PASS`

## Targeted TEST-15 regression

Controlled real-Chrome TEST-15-shaped evidence on the exact ZIP:

1. `test15_blank_composer_auto_send_exactly_once` — `PASS`
   - attachment completed;
   - Send dispatched exactly once;
   - exactly one new user turn observed;
   - delivery completed and outbox cleared;
   - `request_executed=false`.
2. `occupied_user_draft_is_preserved` — `PASS`
   - user draft preserved;
   - no automatic file Send while composer is occupied.
3. `same_delivery_inline_report_auto_sends_exactly_once` — `PASS`
   - composer containing the exact same `report_text` as the delivery is accepted as same-operation ownership;
   - one attachment / one Send / one user turn.
4. `different_bridge_inline_text_is_preserved` — `PASS`
   - different Bridge-owned text is not overwritten or sent by another delivery.

Targeted evidence run: `34752327259`.
Targeted evidence artifact ID: `10315747561`.
Targeted evidence artifact digest: `8ecd674fa4c5e6eeda40caca5f91cc8e26fdcd2960fb9d48783a85ee9a4500b0`.
Provider calls: `0`.

## Final B19 package qualification

Final passing workflow:

- workflow: `YMB patched file-delivery final package qualification v2`
- run: `34752588385`
- QA workflow commit: `bf3abdc9c16882debdec21bd1c0f7b570543f36b`

Results:

- package identity/static gate: `PASS`
- targeted TEST-15 exact-package gate: `PASS`
- fresh-extracted JS syntax: `PASS`
- real-Chrome resource qualification: `PASS` — `16` cases, `0` failures
- deferred-network Chrome qualification: `PASS` — `9` cases, `0` failures
- remaining owned Chrome processes after cleanup: `0`
- peak owned RSS: `1833952 KiB`
- emergency bound: `2097152 KiB`
- real provider calls: `0`
- final gate: `pass=true`

The controlled fixture used for the passing resource/network run models the current confirmation contract: clicking Send creates a new user turn. This is required by the patched exactly-once reconciliation protocol.

## Superseded RED qualification attempt

Run `34752441663` / artifact `10316352282` is retained as failure evidence and MUST NOT be handed to the owner as a qualified candidate.

That attempt used the frozen pre-patch B15 fixture, which cleared the composer after Send but did not create a new user turn. The patched delivery correctly remained in `attachment_send_committed` because confirmation was intentionally absent. This caused the first `FILE_NOT_ACKED` and cascading later resource failures. Production bytes were not changed in response; only the controlled QA fixture was brought into conformance with the current confirmation contract.

## Final owner-candidate artifact and independent readback

Passing Actions artifact:

- artifact name: `ymb-0.1.6-patched-final-owner-candidate-v2`
- artifact ID: `10316386455`
- artifact run: `34752588385`
- outer artifact SHA-256: `8f1bedb1c71bd18b6829505e41a060fdf13232c553fcd551705616082781d9cb`
- outer artifact bytes: `234428`

Independent downloaded-artifact readback:

- outer ZIP integrity: `PASS`
- inner installable ZIP SHA-256: `3e23a70d09fab91f84cf3c9998499ce078f1467b46540dbac7fa07ac60a6765e`
- inner installable ZIP bytes: `225373`
- inner file count: `67`
- inner ZIP integrity: `PASS`
- resource evidence: `16` cases / `0` failures / cleanup `PASS`
- network evidence: `9` cases / `0` failures / cleanup `PASS`
- targeted evidence: all required cases `PASS`

## Gate state

- `PATCHED_FINAL_PACKAGE_GATE = PASS`
- `TARGETED_TEST15_CONTROLLED_CHROME = PASS`
- `INDEPENDENT_CODEX_GATE = WAIVED_BY_OWNER` (existing owner waiver remains authoritative)
- `OWNER_LIVE_SMOKE = READY / NOT YET EXECUTED AFTER PATCH`
- `LIVE_TEST_15 = PENDING_OWNER_BROWSER`
- `FINAL_RECIPIENT_ACCEPTANCE = OPEN`

Do not claim live ChatGPT/owner-browser acceptance from controlled Chrome evidence alone.
