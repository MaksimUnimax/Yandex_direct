# B8 exact-input reconciliation

Date: 2026-09-12. Frozen read ref: `b77c014d02e040679829ccb2c8d61710312b386a`.

The actual saved `candidate/b7/search_async_worker_transport.js` returned by GitHub has Git blob `15c0f45a23d9852c3d8e86c1af8344f6d1f6514a`. The local byte copy was verified by computing Git's blob hash and matched that exact blob. It has 19075 UTF-8 bytes, no final newline, SHA-256 `5096aef1c747050a99aebb4e8d16cb9ce14694a111e50a0e33437a601abd107e`.

However, `BLOCK_B7_RESULT.md`, `B7_TEST_RESULTS.json` and the B7 cursor list `71a3e7e6d424f197cb3d3c39fff74df024e941858ea791e163245f1535e3080f` for this module. Adding a final newline does not produce the declared hash. The reason for this discrepancy is not established here.

Therefore the historical B7 report is NOT exact-byte proof for the actual saved worker input used by B8. Preserve both records; do not silently rewrite historical evidence or reimplement a guessed missing version. The B8 patch is based on the actual saved blob above and requires freshly executed regression on its new postimage.

Patch A artifact-store copy separately matched its actual Git blob `7d021387406cd8c9e222537c745cc697e009c928`. It is used unchanged. The existing deterministic IDB fixture matched blob `8901607d0e075ca36ab87d19990214753617e609`; the artifact tests use a documented QA-only openKeyCursor extension, not a replacement product store.

B8 exporter core currently has 39/39 executable Node assertions; tests of its connection to the unchanged Patch A binary store have 5/5 PASS using the deterministic IDB fixture. These are new results, not Chrome evidence. A one-byte export footer size error was caught by the first run (31 PASS / 8 FAIL) and corrected before the 39/39 rerun.

The existing B3 read-only peekNext/readItem/readResult/getSummary API is sufficient for revision-fenced bounded export. No B3 store edit or new database schema is needed; this narrows the originally stated possible store-edit scope.

RELEASE_ALLOWED = NO
NEXT = additive protocol/Manual export binding and fresh exact-target dependency regression.
