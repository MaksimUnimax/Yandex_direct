# B13 execution checkpoint — source corrections and available regression

Date: 2026-09-12. Exact current candidate tree: `f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47`.

Two production files differ from B12; the other 65 are unchanged:
- shared/phase3_provider_runtime.js: Wordstat-only JSON-object success guard, no new payload copy or result schema.
- wordstat_batch_worker_transport.js: one call routes through the existing unified service executor, preserving batch metadata/admission/checkpoints.

Both root issues were independently reproduced on original owner014. Latest 78 new full-worker/missing-coverage assertions: 78 PASS. The SAME final 78 tests on unchanged B12: 57 PASS / 21 FAIL, multiple consequences of the two documented roots, not 21 independent defects.

Original package test suites are now 118/118 PASS plus supplemental 14/14 on the modified candidate. Qualification: three old test files required explicit QA-only route adaptation. Two isolated harnesses lacked executeServiceCommand; an adapter now asserts service == wordstat and calls the unchanged fixture executor. One source-marker assertion now requires executeServiceCommand(WORDSTAT, command instead of the intentionally removed legacy-call spelling. No behavioral assertion was deleted or loosened. The unadapted run (111/118, 7 failures) is preserved separately and is NOT falsely described as PASS. All other original tests remain byte-identical.

On exact B13, the preserved development campaign also passes: 99 full/contract, 254 modules, 84 export, 61 JS syntax. These sets overlap and are not an independent Codex gate. The candidate remained unchanged during each execution. Zero real Yandex calls, no browser launch, no permission activation, no installable ZIP.

Next immediately: persist executable QA inputs, exact materializer/campaign, full original inventory and all raw logs; rerun from a fresh reconstructed tree and update the continuation cursor. No further feature development in this block.
RELEASE_ALLOWED = NO.
