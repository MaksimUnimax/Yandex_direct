# B11 intermediate checkpoint

Date: 2026-09-12. Source base: exact B10 tree `191b3ed1222733cb9d3aed805b53084829740d10ad906c5246d2cf185fc9ae94`. Current B11 tree: `5fd8a55e980fa54fe5371a51070e9e899307319c8f1ee3255fdc0857b31ebd26` (67 files; four changed).

Saved source: B11_REPARSE_PROTOCOL.diff, B11_REPARSE_WORKER.diff, B11_BATCH_RUNTIME.diff, B11_BATCH_WORKER.diff. Saved executable tests: b11_reparse.test.mjs, b11_batch_faults.test.mjs. Apply these to exact B10 only. Prior A/B1-B10 snapshots are unchanged.

Implemented local normalizeSaved for exactly one stored item. It invokes the existing normalizer with no new network request, accepts no replacement raw/query/URL, preserves raw and budgets, and returns compact counters. A malformed original remains PARSE_FAILED rather than being magically repaired. Successful repeat is idempotent.

Reproduced batch defects: settlement stop was lost, consuming a later pending item; Autorun failed to pause; final-result storage failure reported confirmed work as false; a later pre-network failure lost earlier partial execution count. The exact same final batch test set against B10 has 8/12 PASS, 4 FAIL; after patch 12/12 PASS. The first draft also made an incorrect test assumption about credential Check obeying Manual allowed_methods. Existing explicitly confirmed Check intentionally bypasses those Manual settings; that test expectation was corrected, not production behavior. Added a real admission-write-failure Check assertion instead.

Actual current results in Node v22.16.0, mocked Chrome/IDB/network: local repair 15/15; batch/Check faults 12/12; combined existing B9/B10 plus new tests 75/75; preserved module suite on exact B11 254/254. No real Yandex calls. No Chrome/DOM/real-IDB/memory acceptance.

NEXT: finish reproducible B11 materializer/input manifest, fresh reconstruction tests, export dependency checks, then persist full evidence/report/cursor. Do not reimplement code or restart B10.

RELEASE_ALLOWED = NO. INSTALLABLE_ZIP_CREATED = false.
