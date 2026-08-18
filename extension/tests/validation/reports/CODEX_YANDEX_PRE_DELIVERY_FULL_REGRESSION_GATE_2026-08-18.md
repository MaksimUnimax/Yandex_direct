# CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE

Date: 2026-08-18  
Authority: `653adb63a68f98f03f21534658f3397fd389e0c6`  
Verdict: `PASS`

Exact candidate: `D:\codex\Yandex\work\manual-surface-v2-validation-002\manual-v2\source`, 45/45 files, version 0.1.1. Audited hashes matched. Production and QA harness modifications during the gate: 0.

| Section | Status |
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

Evidence: source suite `358/358`; fresh packaged suite `358/358`; JS/MJS `40/40`; JSON `2/2`; manifest entrypoints `11/11`; Chrome for Testing `151.0.7922.47`; Puppeteer `25.4.0`; install/MV3 worker/content/popup PASS; Manual OFF/ON and 7/7 yellow `Яндекс` surface PASS; mutation/restore/re-enable PASS; controlled provider semantics and all four Wordstat methods PASS; real Yandex requests `0`; secret scan `0`.

Artifact: `yandex-marketing-bridge-0.1.1-phase1-final-live-acceptance-candidate.zip`, SHA-256 `4973c5f87c3ad7d4c052e66c449c2afef412d20a6e4d767bbe761d62abf7cb84`, 199530 bytes, 45 files. Build A/B were byte-identical and source↔fresh extraction was 45/45 byte-identical. The report is evidence-only; real-profile/live acceptance remains separate.
