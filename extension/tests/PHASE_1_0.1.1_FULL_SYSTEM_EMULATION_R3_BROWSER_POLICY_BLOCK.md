# FSE R3 — local Chromium MV3-load environment classification

Date: 2026-08-17
Candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`
Chromium: 144.0.7559.96

Status: **BLOCKED BY TEST ENVIRONMENT — not an extension FAIL.**

Attempted to launch the exact fresh-extracted unpacked candidate in local Chromium with `--load-extension` / `--disable-extensions-except`, first headless and then under Xvfb with a fresh profile and DevTools endpoint.

The browser's managed policy file is authoritative for this local browser instance and contains:

```json
"ExtensionInstallBlocklist": ["*"]
"ExtensionInstallForcelist": []
"ExtensionInstallSources": []
"URLBlocklist": ["*"]
```

Observed consequence:

- normal Chromium/DevTools process starts;
- command-line unpacked extension does not create a service-worker/content-script target;
- `chrome://extensions` navigation is policy-blocked with `ERR_BLOCKED_BY_ADMINISTRATOR` / "Your organization doesn’t allow you to view this site";
- therefore this environment cannot honestly be called a real installed-MV3 acceptance browser.

The managed security policy is not modified or bypassed for the campaign.

Continuation allowed by FSE plan:

- use the same real Chromium 144 renderer/V8/DOM/event model with production content scripts injected against an independent DOM permutation generator and a controlled `chrome.*` boundary emulator;
- execute the production service worker separately in an exhaustive VM/runtime-message/storage/fetch harness;
- route worker fetches only to a recorded local mock / stub boundary, never to real Yandex;
- keep final real installed-MV3/current-ChatGPT acceptance BLOCKED/PENDING for an environment where the extension can actually be loaded.

No real/external Yandex request occurred.
