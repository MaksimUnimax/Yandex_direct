# Phase 9 — Google Search Console stable extension identity migration gate

Date: 2026-08-28
Status: **PREPARED / EXTERNAL PERMANENT ID ASSIGNMENT REQUIRED**
Branch: `phase9/google-organic-provider-research-2026-08-28`

## 1. Why this gate exists

Google Search Console OAuth for a Chrome MV3 extension needs a stable extension identity. Chrome Identity obtains OAuth configuration from the extension manifest, while a Chrome Extension OAuth client is bound to an extension Item ID.

The accepted production extension has historically been installed as unpacked builds and currently has no manifest `key`. Chrome documents that an unpacked extension without a stable key derives its ID from its load path. That makes the existing owner-live unpacked ID unsuitable as permanent OAuth/release authority because moving the extracted folder can change the ID.

Official references:

- https://developer.chrome.com/docs/extensions/how-to/integrate/oauth
- https://developer.chrome.com/docs/extensions/reference/manifest/oauth2
- https://developer.chrome.com/docs/apps/manifest/key/
- https://developer.chrome.com/docs/webstore/

## 2. Decision

The permanent Phase-9 extension identity will **not** be invented from the current transient unpacked path and will **not** be generated ad hoc inside the repository.

The preferred release-compatible authority is a **Chrome Web Store draft item**:

1. upload the exact accepted identity-seed ZIP as a new draft item;
2. do not publish it;
3. obtain the assigned 32-character Item ID and the item public key;
4. add that public key as production manifest `key` in a later test-first commit;
5. verify that the unpacked extension ID derived from that key is exactly the Web Store Item ID;
6. only after this identity match create/bind the Google OAuth client of application type **Chrome Extension** to that Item ID.

This gives one stable identity for unpacked owner-live testing and a future Web Store distribution path.

## 3. Frozen identity seed

The identity seed intentionally comes from the accepted Phase-8 production main, not from unmerged Phase-9 GSC product code.

```text
IDENTITY_SEED_SOURCE_SHA = b13886df49c4591320f780769e78016eff23301e
IDENTITY_SEED_SRC_TREE = bdad1e87a2537d8646e480ca23f8068c3dced17e
IDENTITY_SEED_ZIP = phase9-gsc-identity-seed-main-b13886df.zip
IDENTITY_SEED_SHA256 = ef447b1839d3d0e3ad1e8cf33c11e4b3854e271c634dc99aa2c717da787ca103
IDENTITY_SEED_BYTES = 151237
IDENTITY_SEED_PRODUCT_FILES = 53
IDENTITY_SEED_MANIFEST_AT_ROOT = true
IDENTITY_SEED_REAL_GOOGLE_REQUESTS = 0
IDENTITY_SEED_REAL_YANDEX_REQUESTS = 0
```

Freeze workflow:

```text
WORKFLOW = phase9-gsc-identity-seed
RUN_ID = 33161230756
RUN_HEAD = c73681f10c3de3e474c2463a2260908112190de6
JOB = freeze-identity-seed
CONCLUSION = success
ARTIFACT_ID = 9681707516
ARTIFACT_NAME = phase9-gsc-identity-seed-main-b13886df
```

The seed manifest intentionally has no `identity` permission, no Google host permission, no `oauth2` block, and no `key`. Its only purpose is permanent Chrome item identity assignment.

## 4. Existing-settings migration is proven before ID change

A permanent `key` will create a new extension origin compared with the transient path-derived unpacked identity. Existing extension-local storage therefore must be migrated deliberately rather than assumed to follow the new ID.

The existing Backup V3 runtime already provides the required migration mechanism. A new executable Phase-9 regression proves this sequence using only synthetic secrets:

1. seed five Yandex service credential records and current settings under simulated old extension ID A;
2. export Backup V3;
3. verify the backup records extension ID A, checksum and `contains_secrets=true`;
4. clear extension-local storage;
5. switch runtime to simulated permanent extension ID B;
6. import the same Backup V3;
7. verify all five Yandex credential records and representative settings are restored;
8. re-export and verify the new backup records extension ID B;
9. verify no Google Search Console bearer token/scope is persisted in the credential/backup models.

Gate:

```text
TESTED_HEAD = 23516dcd5c046fd6908f2323290326b22bd1ed6d
WORKFLOW = phase9-gsc-dev
RUN_ID = 33161168476
PURE_JOB = success
CONTROLLED_BROWSER_JOB = success
PHASE9_GSC_STABLE_ID_MIGRATION_PREFLIGHT_PASS = true
PHASE9_GSC_COMPLETE_NODE_REGRESSION_PASS = true
PHASE9_GSC_CONTROLLED_BROWSER_GATE_PASS = true
REAL_GOOGLE_REQUESTS = 0
REAL_YANDEX_REQUESTS = 0
```

## 5. Secret-handling rule

Backup V3 contains the existing Yandex API keys/OAuth tokens by design.

Therefore the owner must export and retain the backup **locally only** before the first permanent-ID installation. The backup must never be pasted into ChatGPT, committed to GitHub, attached to an issue, uploaded as a CI artifact, or otherwise shared.

The following identity values are not secrets and may be returned for repository wiring:

```text
Chrome Web Store Item ID
Chrome Web Store item public key
Google OAuth Chrome Extension client_id
```

No OAuth client secret, refresh token, bearer/access token or Backup V3 file is requested.

## 6. Next governed sequence

### External identity assignment — required now

Owner action:

1. In the currently installed old unpacked extension, export Backup V3 and save it locally. Do not share it.
2. Open Chrome Web Store Developer Dashboard.
3. Create a new item and upload exactly `phase9-gsc-identity-seed-main-b13886df.zip`.
4. Keep the item as a draft; do not publish or submit for review.
5. Return only the assigned Item ID and the item public key.

### P9-06A — repository identity wiring

After Item ID + public key are available:

1. add a test-first permanent-ID contract;
2. add the exact public key to `extension/src/manifest.json`;
3. derive and assert the manifest-key extension ID equals the Web Store Item ID;
4. run full Node and controlled-browser regression;
5. freeze identity evidence before any OAuth client wiring.

### External OAuth client creation

After P9-06A passes:

1. enable Google Search Console API in the chosen Google Cloud project;
2. configure the OAuth consent/app settings as required for the owner account;
3. create an OAuth client with application type **Chrome Extension** and the frozen Item ID;
4. return only the resulting OAuth `client_id`.

### P9-06B — OAuth manifest/UI wiring

Then, test-first:

- add `identity` permission;
- add only the required Google API host permission;
- add `oauth2.client_id`;
- add only `https://www.googleapis.com/auth/webmasters.readonly` scope;
- keep access tokens Chrome-Identity-managed and out of persistent credential/backup models;
- add explicit user-gesture connect/disconnect/auth-status UI;
- keep Autorun default off;
- run controlled browser proof with zero real Google requests before owner-live OAuth.

## 7. Current verdict

```text
P9_05 = PASS / CLOSED
P9_06_STABLE_ID_MIGRATION_PREFLIGHT = PASS
P9_06_IDENTITY_SEED = FROZEN
P9_06_PERMANENT_ITEM_ID = EXTERNAL INPUT REQUIRED
P9_06_PRODUCTION_MANIFEST_KEY = NOT YET AUTHORIZED
P9_06_OAUTH_CLIENT = NOT YET AUTHORIZED
REAL_GOOGLE_REQUESTS = 0
REAL_YANDEX_REQUESTS = 0
```
