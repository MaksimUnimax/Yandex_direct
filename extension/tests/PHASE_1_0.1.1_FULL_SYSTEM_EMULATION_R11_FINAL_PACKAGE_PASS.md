# FSE R11 — final fresh-package gate

Date: 2026-08-17
Candidate: `yandex-marketing-bridge-0.1.1-phase1-k02-generic-dom-patch-candidate.zip`
Expected SHA-256: `46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c`

Status: **PASS**.

The original candidate archive was not modified. It was rehashed and independently extracted twice into fresh empty directories.

```text
ZIP SHA-256: 46458906eeaa72c373fc6ac8da868cc7540fd89a1263966a35f9d93544829f8c
ZIP files: 42
fresh extraction A ↔ fresh extraction B: 42/42 byte-identical
original exact extraction ↔ fresh extraction A: 42/42 byte-identical
manifest version: 0.1.1
package version: 0.1.1
manifest-required entrypoints: all present
built-in fresh-package suite: 319/319 PASS
JS/MJS syntax: 37/37 PASS
manifest/package JSON parse: 2/2 PASS
Chromium `--pack-extension`: exit 0
```

Manifest entrypoint existence check covered the service worker, the complete content-script script order, `content_script.js`, and the popup document.

The Chromium environment remains managed and therefore cannot load the unpacked extension for installed-MV3 acceptance (R3), but packaging itself succeeds.

This package PASS does not supersede the real-current-Chrome K-02 FAIL or the FSE R9 Manual popup/content consistency FAILs. It proves only package integrity and the existing regression suite on the exact artifact.

No production patch was made. No real/external Yandex request occurred.
