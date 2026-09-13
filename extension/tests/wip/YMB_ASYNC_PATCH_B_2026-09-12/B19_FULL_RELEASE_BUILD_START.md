# B19 — full normal release build, execution started

Date: 2026-09-13.

Owner authorized completing the normal build, including enabling the deferred Search network path that was intentionally disabled in B17.

## Exact preimage

Do not reconstruct earlier patch blocks. Use exact B17 artifact:

- Actions run: `34699125356`
- artifact: `10299402884` (`ymb-b17-pause-internal-evidence`)
- inner production ZIP SHA-256: `1560599adfcfdb2c3180ec9103005b1584bcd39709b8c32c778a306f73f6703bfe508`
- inner ZIP bytes: `225660`
- exact B17 production tree SHA-256: `b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508`
- files: 67

## Intended product changes only

1. Publish the exact B17 product as the canonical `extension/src` source tree instead of the stale 0.1.2 source snapshot.
2. Enable `https://operation.api.cloud.yandex.net/*` in `manifest.json`, preserving all existing hosts/permissions and adding no `alarms` permission.
3. Bump the release identity to **0.1.6** (0.1.5 was the previously rejected build) consistently in manifest/package/product/popup/version fallback and release README files.
4. Update README text from internal-disabled-candidate wording to the actual 0.1.6 behavior: deferred Search is Manual-only, explicit submit/collect, no background polling/Autorun/retry.
5. Do not change deferred orchestration/state/network algorithms unless an executable test first reproduces a defect on the B19 candidate.

## Required dependency and safety gates before owner ZIP

- exact preimage and intended-diff proof;
- JS syntax / JSON / manifest load order;
- version consistency;
- Search sync + GenSearch regression;
- Wordstat/Webmaster/Metrika/Direct regression on unchanged logic;
- deferred provider permission recognition and real command ingress using controlled synthetic provider responses only;
- auth/folder/provider-origin containment and no credential export;
- shared cost/quota/state-machine/recovery/duplicate-submit protections;
- file attachment/delivery/recovery regressions;
- real Chrome install + providerEnabled true;
- real Chrome IndexedDB and file-resource checks, including repeated 64-MiB delivery path and 1500-item deferred state path where qualified harness permits;
- deterministic package/fresh extraction/source↔ZIP identity;
- no owner browser/profile access;
- no owner ZIP handoff until exact candidate tests complete.

## Provider canary boundary

A full successful live Yandex deferred canary needs a real valid Search API credential. No owner credential is available in this QA environment. Do not invent one and do not use repository secrets. Build and fully test the network-enabled product with controlled provider responses. Record the successful-live-provider canary as a separate final capability check if/when an authorized valid credential is supplied.

B19_STATUS = IN_PROGRESS
RELEASE_ALLOWED = NO
OWNER_ZIP_HANDOFF = FORBIDDEN
