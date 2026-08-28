# Phase 9 — Google Search Console stable extension identity migration gate

Date: 2026-08-28
Status: **P9-06A PASS / LOCAL STABLE ID FROZEN**
Branch: `phase9/google-organic-provider-research-2026-08-28`

## 1. Decision

Phase 9 no longer depends on Chrome Web Store registration, a paid developer account, a draft item, or a Web Store-assigned key.

For the current owner-live / unpacked-extension path, the extension identity is pinned directly in the production manifest with a fixed public `key`. Chrome uses that key to derive the same extension ID regardless of the folder from which the unpacked build is loaded.

Frozen identity:

```text
EXTENSION_ID = pckmmaodnfeajgigadfaejfjppdbgmpo
PUBLIC_KEY_DER_SHA256 = f2acc0e3d540968603504959ff316cfe0310622c9b948478e26b955181173e72
PUBLIC_KEY_DER_BYTES = 294
IDENTITY_SOURCE = extension/src/manifest.json -> key
CHROME_WEB_STORE_REQUIRED_FOR_P9_06A = false
```

The manifest public key is not a secret. No private signing key is stored in the repository and none is required for loading the extension unpacked with a stable ID.

If public Chrome Web Store distribution is ever chosen later, release identity/distribution can be handled as a separate release concern. It is not a Phase-9 development blocker.

## 2. What changed

P9-06A was completed test-first:

1. added `extension/tests/google_search_console_manifest_identity.test.mjs`;
2. froze one manifest public key and expected 32-character extension ID;
3. added that exact `key` to `extension/src/manifest.json`;
4. changed the controlled-browser proof to load the real production key instead of generating a temporary QA key;
5. kept `identity`, Google host permission and `oauth2` absent at P9-06A;
6. kept Google bearer tokens out of persistent credential and Backup V3 models;
7. ran the full Node + controlled-browser gate with zero real provider requests.

Gate commit:

```text
GATE_HEAD = 35182cc9f0e687416a4fe5123742197c796c3c91
COMMIT_STATUS_CONTEXT = phase9-gsc-dev/gate
COMMIT_STATUS = success
REAL_GOOGLE_REQUESTS = 0
REAL_YANDEX_REQUESTS = 0
```

## 3. Existing-settings migration remains required when the owner installs the first stable-ID build

The old unpacked installation used a different path-derived extension ID. A manifest `key` creates a different Chrome extension origin, so `chrome.storage.local` from the old installation does not automatically appear under the new stable ID.

Backup V3 is the approved migration mechanism. The existing executable preflight proves that a backup exported under simulated old ID A can be imported under simulated stable ID B while restoring the five existing Yandex credential records and representative settings.

Backup V3 contains Yandex API/OAuth secrets by design. Therefore, when migration is actually performed, the backup must stay local to the owner machine and must not be pasted into ChatGPT, committed to GitHub, attached to an issue, or uploaded as a CI artifact.

No Google Search Console token is added to Backup V3.

## 4. Auth path after P9-06A

Google Search Console remains the sixth service `google_search_console`. Its first official read-only slice remains:

- `listSites`
- `searchAnalytics`

The intended OAuth scope remains:

```text
https://www.googleapis.com/auth/webmasters.readonly
```

The stable extension ID to use for a Google OAuth client is now already known:

```text
pckmmaodnfeajgigadfaejfjppdbgmpo
```

No Chrome Web Store Item ID is needed by the repository to continue development.

P9-06B will be implemented test-first around the following rules:

- explicit user-gesture connect/disconnect/status UI;
- interactive authorization only from the connect action;
- provider execution remains noninteractive;
- access tokens remain Chrome-Identity-managed and are never persisted in YMB credential storage or Backup V3;
- Autorun stays disabled by default;
- one command performs at most one provider business request;
- no automatic provider retry;
- controlled browser proof must pass before any owner-live Google request.

The external Google OAuth `client_id` is not required until the final production OAuth binding step. All repository work that does not require that value should proceed first.

## 5. Superseded Web Store path

The previous plan that required:

- Chrome Web Store Developer Dashboard registration;
- the one-time developer registration fee;
- a draft Web Store item;
- a Web Store public key / Item ID;

is **superseded and removed from the active Phase-9 path**.

The former `phase9-gsc-identity-seed` workflow has been deleted from the branch.

## 6. Current verdict

```text
P9_05 = PASS / CLOSED
P9_06_STABLE_ID_MIGRATION_PREFLIGHT = PASS
P9_06A_LOCAL_STABLE_ID = PASS / FROZEN
P9_06A_EXTENSION_ID = pckmmaodnfeajgigadfaejfjppdbgmpo
P9_06A_CHROME_WEB_STORE_REQUIRED = false
P9_06B_OAUTH_UI_AND_BINDING = NEXT
REAL_GOOGLE_REQUESTS = 0
REAL_YANDEX_REQUESTS = 0
```
