# B19 — canonical 0.1.6 Node gate checkpoint

Date: 2026-09-13.

Exact product under test:

- version: `0.1.6`;
- files: 67;
- tree SHA-256: `b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86`;
- `https://operation.api.cloud.yandex.net/*`: enabled exactly once;
- `https://searchapi.api.cloud.yandex.net/*`: preserved;
- `chrome.alarms`: not enabled;
- real provider calls: 0.

Canonical final Node run: GitHub Actions `34735461440`, artifact `10311260104` (`ymb-b19-canonical-final-node`), artifact digest `sha256:751d58bab286e4b81bd5171b0e365e26da4323dac4c642551375b83dbceeb13a`.

Executed result on the exact B19 bytes:

| Suite | Result |
|---|---:|
| Original source tests | 132 / 132 PASS |
| Wordstat / Debug / backup additional coverage | 78 / 78 PASS |
| Full worker / contract with network-enabled deferred expectations | 99 / 99 PASS |
| Preserved async/admission/state modules | 254 / 254 PASS |
| Export / file modules | 84 / 84 PASS |
| Delivery / recovery / content ownership combined | 69 / 69 PASS |
| JavaScript syntax | 61 / 61 PASS |

No failed, skipped or cancelled test remains in the canonical Node scope. Candidate source identity was rechecked after tests and remained the exact tree above.

The first B19 classification and subsequent failed runs are preserved as QA history. Their failures were obsolete disabled-network expectations or missing harness bindings; no production edit was made in response. The final run replaces only those QA assumptions with controlled `searchAsync -> Operation GET` tests using synthetic credentials and controlled provider responses.

Next mandatory block: install these exact `0.1.6` bytes in isolated Chrome for Testing and re-run the affected browser/resource matrix: providerEnabled/network origin containment, explicit deferred submit/collect, IndexedDB 1500-state/restart contour, file delivery/resource checks including repeated 64 MiB, ownership/double-Send and process cleanup. No owner ZIP handoff before that browser/resource gate and final package identity checks.

```text
B19_NODE_GATE = PASS
B19_BROWSER_RESOURCE_GATE = NOT_RUN
RELEASE_ALLOWED = NO
OWNER_INSTALLABLE_HANDOFF = FORBIDDEN
```
