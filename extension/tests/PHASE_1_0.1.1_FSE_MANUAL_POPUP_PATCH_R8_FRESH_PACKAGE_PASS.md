# FSE Manual/popup patch R8 — deterministic fresh-package gate

Date: 2026-08-17
Base candidate SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS**.

Final controlled/package candidate:

```text
yandex-marketing-bridge-0.1.1-phase1-fse-manual-popup-patch-candidate.zip
SHA-256: f06a16780bed8a1aedb6726c25baaa0667145d4adb14553868b294f95e807cc3
size: 180608 bytes
files: 42
```

Package verification:

```text
deterministic rebuild #1 ↔ #2: byte-identical
source working tree ↔ fresh extraction: 42/42 byte-identical
fresh ZIP full suite: 321/321 PASS
JS/MJS syntax: 37/37 PASS
manifest/package JSON: 2/2 PASS
manifest required entrypoints: all present
Chromium --pack-extension: exit 0
```

Exact base-to-final changed paths:

```text
popup.js
tests/popup_runtime_exhaustive.test.mjs
```

Only one **production** file differs from the governed base candidate:

```text
popup.js
SHA-256: 7286ea024033293110ad10ebc16856de0beacf512f6f86a229ac0271ac20c28c
```

The following critical production files remain byte-identical to the base K-02 candidate:

```text
manifest.json
service_worker.js
content_script.js
shared/manual_controls.js
shared/wordstat_protocol.js
```

The existing file/path inventory remains exactly 42 files. No new production file, permission, host permission, worker/provider/content transport or protocol surface was introduced.

No real/external Yandex request occurred.
