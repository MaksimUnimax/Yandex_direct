# Pre-delivery full regression accepted — 2026-08-18

Status: **ACCEPTED FOR OWNER HANDOFF / REAL-PROFILE LIVE ACCEPTANCE**

Validation authority:

- main SHA tested: `653adb63a68f98f03f21534658f3397fd389e0c6`
- validation branch: `validation/yandex-pre-delivery-full-regression-2026-08-18`
- validation commit: `c71e1e69aa70babd31c30b4f461323299562ae2b`
- gate: `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`

Exact accepted artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-final-live-acceptance-candidate.zip
SHA-256 4973c5f87c3ad7d4c052e66c449c2afef412d20a6e4d767bbe761d62abf7cb84
size 199530 bytes
files 45
```

Acceptance evidence:

- PD-00…PD-17: all PASS
- coverage registry: PASS
- source suite: `358/358 PASS`
- fresh packaged suite: `358/358 PASS`
- JS/MJS syntax: `40/40 PASS`
- JSON: `2/2 PASS`
- manifest entrypoints: `11/11 PASS`
- deterministic Build A/B: PASS
- source ↔ fresh package: `45/45` byte-identical
- Chrome for Testing 151.0.7922.47 / Puppeteer 25.4.0 controlled runtime: PASS
- extension install / MV3 worker / content script / popup: PASS
- production modified during gate: `0`
- harness modified during gate: `0`
- real Yandex requests: `0`
- secrets in report: `0`

This acceptance permits handoff of **this exact artifact only**. Controlled evidence does not equal real-profile/live PASS. Phase 1 remains not LIVE PASS until its separate real-profile/live acceptance is completed.

Any production-byte change invalidates this handoff acceptance and requires a new full pre-delivery Gate run from PD-00 through PD-17 on the new frozen candidate. Documentation/evidence-only commits do not alter the accepted artifact identity.
