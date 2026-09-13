# B18 — independent Codex pre-delivery gate prompt

Use this prompt only as the **independent QA handoff** after B18 development qualification. Codex is the QA executor only. It must not patch product code, design fixes, weaken tests, substitute a different candidate, or convert enabled NOT_RUN into PASS.

---

Continue independent pre-delivery QA for Yandex Marketing Bridge.

THIS IS A QA EXECUTION TASK.
THIS IS NOT A DEVELOPMENT TASK.
DO NOT EDIT PRODUCTION CODE.
DO NOT FIX FAILURES.
DO NOT CHANGE TEST ASSERTIONS TO MAKE THEM PASS.
DO NOT SUBSTITUTE ANOTHER CANDIDATE.
DO NOT MAKE REAL YANDEX PROVIDER CALLS OR USE REAL OWNER CREDENTIALS.

Repository:
`MaksimUnimax/Yandex_direct`

Working branch containing authorities/evidence only:
`wip/ymb-file-delivery-patch-a-2026-09-12`

Authoritative QA rules to read in full before execution:

1. `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`
2. `extension/docs/YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`
3. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/BLOCK_B17_RESULT.md`
4. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/BLOCK_B18_RESULT.md`
5. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B18_FINAL_PD_EXECUTION_MAP.md`
6. `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/evidence/B18_TEST_RESULTS.json`
7. current `extension/tests/wip/YMB_FILE_DELIVERY_PATCH_A_2026-09-12/CONTINUATION_CURSOR_2026-09-12.json`

## Exact product under test

The product is the exact B17 **disabled-deferred-network** candidate. Do not reconstruct it if the ready artifact is available.

Product tree SHA-256:
`b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508`

Exact internal QA ZIP SHA-256:
`1560599adfcfdb2c3180ec9103005b1584bcd39709b8fc45e233f6c1bdd11ee1`

ZIP bytes:
`225660`

Files:
`67`

Primary existing Actions artifact carrying the exact package plus qualified QA inputs:
- run: `34699125356`
- artifact: `10299402884`
- name: `ymb-b17-pause-internal-evidence`
- artifact SHA-256: `0a6b938c6d39392ed1f61f072bfc1ed5e590e99c207bc0bb2d9defebce1e5c3c`

If that artifact is unavailable, STOP with `FAIL_ARTIFACT`/transport classification according to authority unless the governed exact fallback in the cursor is still available. Do not ask the owner to move QA files.

## Product boundary

This candidate intentionally DOES NOT grant:
`https://operation.api.cloud.yandex.net/*`

Therefore deferred Search provider submit/collect must remain fail-closed in this candidate. Do not fail PD-16 because an intentionally disabled future network phase does not execute. Do fail it if recognition or local commands silently bypass the permission lock.

Ordinary already-enabled services — Wordstat, ordinary Search/GenSearch, Webmaster, Metrika and Direct — remain part of the enabled regression surface.

Real provider requests = 0 for this independent gate.
Real owner credentials = forbidden.
Synthetic/stub credentials and controlled network interception are allowed by the gate.

## Mandatory campaign

Execute ALL enabled `PD-00…PD-17` in one governed campaign against the exact candidate. Use `B18_FINAL_PD_EXECUTION_MAP.md` for the concrete executable mapping, but the original gate remains authoritative.

Important:
- PD-04 requires safe MV3 worker restart/lifecycle behavior. The development campaign used real worker target restart and whole-browser profile close/reopen. Do not invent an extra mandatory requirement that a particular Puppeteer `chrome.runtime.reload()` popup-navigation method must work.
- Browser-owned assertions stay browser-owned.
- Internal deterministic state assertions may use the qualified Node/VM/integration venue mapped in B18.
- Existing historical PASS is context, not your verdict. Run the independent campaign yourself.
- A normal product assertion failure does not justify leaving unrelated enabled sections NOT_RUN when safe to continue.

## Required final classifications

For every PD section report exactly one allowed state from the governing gate.

The final overall result must be one of:
- `PASS`
- `FAIL_PRODUCT`
- `FAIL_ARTIFACT`
- `FAIL_HARNESS`

No overall PASS is allowed if an enabled mandatory section is NOT_RUN.

If a product assertion fails:
- preserve exact evidence;
- classify it;
- do NOT patch it;
- return the complete failure set to ChatGPT.

If artifact/harness fails:
- preserve evidence;
- do NOT mutate production bytes;
- classify precisely.

## Required evidence

Record at minimum:
- exact input ZIP SHA-256 / bytes / file count;
- fresh extraction identity against the exact product tree;
- full test/harness invocation and versions;
- PD-00…PD-17 matrix;
- all FAIL/NOT_RUN details;
- resource measurements required by applicable sections;
- final package/source identity;
- confirmation of zero real Yandex provider calls;
- confirmation owner profile/credentials were not used;
- final overall verdict.

The exact artifact that receives independent PASS is the only artifact that may later be considered for owner handoff. If product bytes change after this campaign, this verdict does not transfer.

## Permanent evidence references

B18 development raw evidence is permanently reconstructable from:
`extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/evidence/B18_RAW_LOGS/`

Do not treat its development PASS as your independent PASS. It exists to give provenance, regression history and known qualified harness routes.

Return one concise acceptance report plus machine-readable PD matrix/evidence manifest. Do not implement fixes.

---

Current expected status before Codex begins:

```text
EXACT_PRODUCT = B17 disabled-deferred-network candidate
B18_DEVELOPMENT_PD_MAPPING = COMPLETE
INDEPENDENT_CODEX_GATE = NOT_RUN
OPERATION_HOST_ENABLED = NO
LIVE_PROVIDER_CALLS = 0
RELEASE_ALLOWED = NO
```
