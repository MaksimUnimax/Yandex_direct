# B13 — one inherited Wordstat response defect, reproduced before correction

Date: 2026-09-12. Original suite on exact B12: 118/118 plus 14 supplemental PASS. Additional complete-worker Wordstat/Debug/backup coverage: 59 tests, 55 PASS / 4 FAIL. All four failures share one root.

Actual path: shared/phase3_provider_runtime.js executeCloud parses the response with parseJson, which returns null on malformed input. For Wordstat, that null then passes directly into an OK result envelope when HTTP status is 200. There is no equivalent of the Search response parser failure at this point.

The exact same four full-Manual assertions were run on the unchanged owner014 ZIP extraction. All four fail there too. This is an inherited 0.1.4 defect, NOT an async-patch regression and NOT a reproduction of the owner's RAM incident.

- New test SHA-256 at RED: 87873583ecf84632a4e4ae6828de7b7c755abd85dc91b422e12fedec8eea9b61.
- 59-case initial log SHA-256: ae3a43767c9defa6307ced46087d65bf0532d169cad97b5f5d799369126ffb8a.
- Owner014 four-case RED log: 8dd444fc28139ec84194d13ae9d6c8eca0c66335a4819758110bfb8543d58211.

## Bounded correction scope

Add a Wordstat-only successful-response guard in the actual cloud provider: JSON must be a non-null object, not an array/scalar/malformed body. Do not impose a new result-field schema; preserve valid objects including omitted optional fields. Reject locally after the completed request with request_executed=true and automatic_retry=false; do not start another request or echo raw malformed text.

Only one production file is proposed to change. Search and GenSearch parsing, endpoint/auth/request construction, HTTP error handling, cost reservation, all other services, file transport, store schemas, manifest and permissions remain unchanged.

Required affected tests: four Wordstat methods and malformed/scalar/unreadable bodies; full Manual error delivery; Wordstat batch failure; cloud credential Check; original 18 suites plus supplemental Direct suite; preserved full-worker/module/export regressions on the new exact target. Recheck source identity and syntax. No unavailable Chrome proof will be asserted.

## Independent basis checked now

Official REST Wordstat GetTop, GetDynamics, GetRegionsDistribution and GetRegionsTree documentation all describe a JSON response object:
https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Wordstat/getTop
https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Wordstat/getDynamics
https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Wordstat/getRegionsDistribution
https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Wordstat/getRegionsTree

The error code and non-retry outcome are project-specific decisions grounded in the existing request lifecycle; the documentation does not claim a provider call was executed by this test.

Production not modified at this checkpoint. Real provider calls = 0. RELEASE_ALLOWED = NO.
