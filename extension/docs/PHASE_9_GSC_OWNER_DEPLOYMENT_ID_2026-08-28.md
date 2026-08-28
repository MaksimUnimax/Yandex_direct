# Phase 9 — Google Search Console owner deployment ID

Date: 2026-08-28
Branch: `phase9/google-organic-provider-research-2026-08-28`
Status: `OWNER_DEPLOYMENT_ID_CAPTURED / OAUTH_CLIENT_PENDING`

## Existing installed extension identity

Owner-confirmed Chrome extension ID:

`fegfjjjfcginmfbiddddgcmhlddpmodb`

Validation:

- exactly 32 characters;
- only letters `a` through `p`;
- captured from the already installed unpacked Yandex Marketing Bridge instance;
- this ID is treated as an external deployment parameter for Google OAuth registration;
- it is intentionally **not** written into `extension/src/manifest.json`;
- production manifest remains without `key` so Phase 9 does not introduce an identity migration.

## Update contract

The owner deployment must preserve the already installed unpacked extension identity. Phase 9 must not create or require a Chrome Web Store item, registration payment, migration backup, or a replacement manifest key.

When updating the owner installation for the live OAuth check, update/reload the existing unpacked extension deployment rather than intentionally creating a second extension identity.

## Google OAuth registration target

Create the Google OAuth client with application type `Chrome Extension` and Item ID:

`fegfjjjfcginmfbiddddgcmhlddpmodb`

Required Search Console scope:

`https://www.googleapis.com/auth/webmasters.readonly`

Only the resulting OAuth `client_id` is required for the Phase 9 manifest. No client secret, Google bearer/access/refresh token, Yandex credential, or Backup V3 file may be committed or requested.

## Current product safety state

Until the OAuth client ID is supplied:

- no `identity` permission in production manifest;
- no `oauth2` block in production manifest;
- no Google API host permission in production manifest;
- no persistent Google token storage;
- real Google provider requests remain forbidden;
- real Yandex provider requests remain forbidden by the Phase 9 development gate.
