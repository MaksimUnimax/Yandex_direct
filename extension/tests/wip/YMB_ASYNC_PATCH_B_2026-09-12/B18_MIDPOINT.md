# B18 midpoint — 2026-09-13

Exact B17 remains unchanged: 67 files, tree b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508; ZIP 1560599adfcfdb2c3180ec9103005b1584bcd39709b8fc45e233f6c1bdd11ee1.

`qa/b18_node_campaign.py` was actually executed locally (Node22.16/Python3.13). One entry point validates the ready package and QA inputs, uses the saved B13 executor with only its exact-target constant changed, and executes original132, Wordstat/backup78, full99, modules254, export84 and delivery69. All passed, failed/skipped/cancelled=0, final product identity unchanged. Test counts overlap. The new runner source SHA256 is cc6389e6c08c9e944d21575c0e451788a9d7c0fad73b2dc1a71f7eca772c3c18. No production reconstruction or real network.

First B18 browser run34731010004 is NOT PASS: eight FAIL_QUALIFICATION markers. Artifact10308669055 was downloaded and all member hashes checked; outer 25908bytes/SHA632468e61ce8a75b8147ae7d324b641b78cd1d1af3f07e2e9aaaa4384e2760b2. It contains all raw errors, successful scenarios, generated QA and RSS; it must never be overwritten or relabeled successful.

One confirmed QA error: switchService dispatched change on an unsaved/Manual-disabled selector and expected persistence. Actual popup.js explicitly requires Manual OFF, selection, and Save. The untouched product correctly retained Search, causing later Wordstat admission errors. The QA helper now uses the real governed UI. Subsequent report timeouts are not yet independently classified as product defects; rerun correct preconditions first.

Reload synchronization is also qualified separately: the first fixture scheduled extension reload while awaiting evaluation in the dying worker. The bounded recheck returns the debugger command before teardown, observes target destruction and opens the extension popup to wake the new worker. Do not assert this hypothesis explains every first-run timeout without result evidence.

QA-only exact adapter b18_fixture_recheck.py preserves all product assertions, changing the generated QA hash from f17ab8878768d1255cf0ecb85f430dd6d3c44ee9b659f4729d14c5e136be4fdd to c7df7ea3a1b54322918f7b09cc7bb403384f0926a65a046b4581e70f04b7aa92. Product files remain identical.

NEXT: read the recheck triggered by workflow commit5c6043dafdfadb87c005f8e19c242c768b1b688c; classify actual remaining failures. Persist complete logs and final coverage/cursor, not just this midpoint. Independent PD acceptance is still NOT_RUN; RELEASE_ALLOWED=NO.
