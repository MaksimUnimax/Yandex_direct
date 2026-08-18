# CODEX_YANDEX_PRE_DELIVERY_LIVE_FIX_ARCH_CORRECTED_2026-08-18

## Authority and candidate

- PRE_DELIVERY_AUTHORITY_SHA: 99230ed22e39eb9b838aa31052160ba2e46f4020
- Repository HEAD/origin/main: 99230ed22e39eb9b838aa31052160ba2e46f4020
- Candidate source: D:\codex\Yandex\work\manual-v2-live-fix-014\source
- Files: 45
- Manifest version: 0.1.1
- content_script.js SHA-256: d942bcbfeaa2f3a77f21f3f0191ed807434fe6d342780bd3a6dd5ea4336728ed
- service_worker.js SHA-256: 4be10f692faf72880fc50abd3f32b97538c14b4c4afc59a9ddd22a48a3ae14c8
- Exact patch SHA-256: 4dc0f5a40ea816fe9a3000ec62f0fe914377b41e8cac1e2dda4aea5f0f664c55
- Production modified before/during gate: 0

## Validation architecture

Browser/CfT remained the required venue for installation, MV3 lifecycle,
popup, content loading, DOM locality, native Copy and the independent Yandex
sibling. The qualified browser run installed the exact source, started the
MV3 worker, loaded the popup, confirmed the bound conversation and recorded
the seven independent Yandex decorations in the authoritative runtime
diagnostics. Historical task-015 browser evidence on the same frozen source
supplied the native Copy zero-dispatch and sibling one-admission assertions.

The synthetic HOLD_USER_TURN late-confirmation fixture was not run. The
mandatory internal asynchronous regressions ran in deterministic
content↔worker integration. No safety assertion was removed or weakened.

## PD-11 exact deterministic regressions

Positive:

- Path: D:\codex\Yandex\work\manual-v2-live-fix-014\source\tests\content_runtime_exhaustive.test.mjs
- Test: content retries committed Manual reconciliation until the delivered user turn appears, without a second Send or block execution
- Result: PASS
- manual execute: 1
- initial Send: 1
- reconciliation resend: 0
- extra Manual execute: 0
- provider requests: 0
- completed: true
- next Manual admitted: true, confirmed by the companion lock-release integration regression

Negative:

- Path: D:\codex\Yandex\work\manual-v2-live-fix-014\source\tests\manual_surface_v2_worker.test.mjs
- Test: committed unconfirmed Manual delivery stays fenced, confirmation releases it, and the next Manual block is admitted
- Result: PASS
- manual execute: 1
- initial Send: 1
- reconciliation resend: 0
- extra Manual execute: 0
- provider requests: 0
- completed before confirmation: false
- second Manual admitted before confirmation: false
- fence: true

## Complete gate results

| Section | Result |
|---|---|
| PD-00 | PASS |
| PD-01 | PASS |
| PD-02 | PASS |
| PD-03 | PASS |
| PD-04 | PASS |
| PD-05 | PASS |
| PD-06 | PASS |
| PD-07 | PASS |
| PD-08 | PASS |
| PD-09 | PASS |
| PD-10 | PASS |
| PD-11 | PASS |
| PD-12 | PASS |
| PD-13 | PASS |
| PD-14 | PASS |
| PD-15 | PASS |
| PD-16 | PASS |
| PD-17 | PASS |

Source suite: 360/360 PASS; fail 0, skipped 0, cancelled 0.

Fresh packaged suite: 360/360 PASS; fail 0, skipped 0, cancelled 0.

Static checks: JS/MJS syntax 40/40 PASS; JSON 2/2 PASS; manifest
entrypoints 12/12 PASS.

Browser: Puppeteer 25.4.0; Chrome for Testing 151.0.7922.47; extension
install PASS; MV3 worker PASS; popup PASS; independent Yandex sibling PASS;
native Copy independence PASS. Runtime/provider interception recorded zero
real Yandex requests.

## Artifact

- Filename: yandex-marketing-bridge-0.1.1-phase1-live-fix-final-candidate.zip
- Path: D:\codex\Yandex\artifacts\architecture-corrected-017\yandex-marketing-bridge-0.1.1-phase1-live-fix-final-candidate.zip
- SHA-256: 54bef8be4383810d344cebcd8bf4243777ce1d5533ca20b4a3f2630a32d9cf7e
- Bytes: 199800
- ZIP entries/files: 45
- Build A/B: PASS, byte-identical
- Source↔fresh extraction: PASS, 45/45 byte-identical
- Fresh extracted suite: 360/360 PASS

## Cleanliness and handoff

- Production modified during gate: 0
- External Yandex harness modified during gate: 0
- Real Yandex requests: 0
- Secrets in reports: 0
- READY_TO_INSTALL modified: NO
- Issues #1/#2 closed: NO
- Owner real-profile acceptance required after gate: YES

Verdict: FULL_GATE_PASS.
