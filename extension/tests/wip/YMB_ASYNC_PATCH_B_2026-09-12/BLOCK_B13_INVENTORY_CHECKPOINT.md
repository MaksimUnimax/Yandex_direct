# B13 — first executed checkpoint

Date: 2026-09-12. Frozen source ref `1aafee85d8534ab08848c217efa517a8a2cbec23`; candidate remains exact B12 `73e6ed85bfd843bf2590a2d1a44a9d04224ce5f63563d127bcd35c2ad092eeec`.

The read-only snapshot returned the full original extension/tests, source/reference and documentation. All 2431 archived file blobs matched the git ls-tree inventory. The owner baseline and the saved b9 -> b10 -> b11 -> b12 materializers restored the 67-file B12 candidate without rewriting code.

## Complete original inventory, excluding WIP

158 tracked files: 18 package-script Node test files, 1 supplemental Node test, 8 browser harness scripts, 2 controlled QA campaign runners, 1 runtime fixture/helper and 128 historical evidence/documents. No original test file was omitted from the inventory.

## Actually executed now

- All 18 files selected by the original package.json test script: 118/118 assertions PASS, zero failed/skipped/cancelled.
- Additional qa_phase5_codex/direct_addendum_coverage.test.mjs: 14/14 PASS, zero failed/skipped/cancelled.
- All tests and original helper bytes remained unchanged. The tests saw B12 as extension/src, not the older repository 0.1.2 sources.
- Each suite had a 10-second per-test and 25-second process deadline; two processes maximum, Node heap budget 256 MiB per process. Accidental real fetch/http/https/net/tls/dgram entry points were blocked by a QA-only guard. Test-owned network fixtures remained available.
- Candidate file hashes before/after were identical. No production modifications, browser launches or provider calls.

These 132 assertions are original-suite evidence, not the independent PD gate and not Chrome memory/DOM/real-IDB proof. Raw TAP and stderr for each suite, inventory and the reproducible runner are local and will be published in the closing B13 evidence archive; this checkpoint does not claim they are already remote.

Next in this same block: inspect saved successful browser-harness records without launching a blocked browser, and exercise feasible missing Wordstat-all-methods, Debug OFF/ON and settings-backup contracts using preserved full-worker harness. Do not invent a new feature or change production merely to make a test pass.

RELEASE_ALLOWED = NO.
