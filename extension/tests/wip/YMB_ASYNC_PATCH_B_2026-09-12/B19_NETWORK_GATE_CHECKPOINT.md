# B19 deferred Search real-Chrome network gate checkpoint

Date: 2026-09-13. Product bytes under test are unchanged from canonical B19 0.1.6 tree:

`b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86` — 67 files.

Production network boundary:

- `https://searchapi.api.cloud.yandex.net/*` present;
- `https://operation.api.cloud.yandex.net/*` present exactly once;
- `chrome.alarms` absent;
- deferred mode Manual-only.

## Canonical PASS

GitHub Actions run: `34737190955`

Artifact: `10311158854` / `ymb-b19-browser-network-v6-evidence`

Artifact SHA-256: `ea8638d701b28ec22acaca0cefe9fd22ec7c555cca570811134015ccd294d4f2`

The run succeeded in real Chrome for the complete controlled deferred contour:

1. exact 0.1.6 loaded with provider capability enabled and zero startup fetches;
2. `start` creates the job with zero network traffic;
3. `submitN` performs exactly the fixed `POST https://searchapi.api.cloud.yandex.net/v2/web/searchAsync`, using the stored synthetic Search credential/folder and persists the returned operation ID before continuing;
4. the result report is delivered once through the normal content/outbox/Send path;
5. `collect` performs exactly the fixed `GET https://operation.api.cloud.yandex.net/operations/<operation_id>` and the saved raw response is normalized to the expected result;
6. command JSON cannot override provider URL, authorization or folder/credential context;
7. Manual disabled prevents network initiation;
8. controlled unknown submit outcome executes once, becomes `UNKNOWN` and is not automatically retried;
9. no unexpected page error and no leftover owned Chrome process.

`real_provider_calls = 0`: all provider responses were controlled test fixtures, so no owner key/provider cost was used by this gate.

## Preserved RED / harness history

- v3/v4 exposed the first submit delivery as apparently stuck; diagnostics proved provider/store/outbox were already correct and the controlled fixture had removed its Send button after the prior report. Product was unchanged.
- v5 re-armed the synthetic Send like real ChatGPT and proved submit+delivery; the run then hit a QA-only `ReferenceError` because owner `KEY` was referenced inside another JS realm without being passed as an argument. Product was unchanged.
- v6 fixed only that QA realm argument and completed the whole network contour.

No production source was modified by these QA fixes.

Current boundary:

```text
B19_NETWORK_CHROME_GATE = PASS
PRODUCT_TREE = b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86
REAL_PROVIDER_CALLS = 0
RESOURCE_GATE = STILL_RUNNING
RELEASE_ALLOWED = NO
OWNER_ZIP_HANDOFF = FORBIDDEN
```
