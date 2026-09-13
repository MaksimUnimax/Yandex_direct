# B19 — pre-Codex exact-artifact transport/readback checkpoint

Date: 2026-09-13

Scope: QA/process evidence only. Production bytes are unchanged. This checkpoint does not count as independent Codex acceptance and does not unlock owner handoff.

## Live recovery state before this checkpoint

Working branch: `wip/ymb-file-delivery-patch-a-2026-09-12`

Branch HEAD before this checkpoint: `affdd2a6bfc84b966d1429ae8bbc336901c92d65` (`wip(extension): persist exact independent Codex gate prompt for final 0.1.6 ZIP`).

The current continuation cursor still records `INDEPENDENT_CODEX_NOT_RUN`, `release_allowed=false`, and `owner_installable_handoff=FORBIDDEN`.

A live GitHub Actions readback found no workflow runs created at or after the independent-prompt commit time (`2026-09-13T04:20:43Z`) and no workflow run attached to the prompt HEAD. Therefore no later independent B19/Codex result was found and completed B9–B19 development must not be restarted.

## Exact frozen artifact

Primary GitHub Actions package source:

- workflow run: `34737506830`
- artifact id: `10311695957`
- artifact name: `ymb-0.1.6-final-owner-candidate`
- artifact expiration: `2026-12-12T04:16:39Z`
- published artifact bytes: `225323`
- published artifact SHA-256: `07d9b9e70181983172b7af448e07e087ec9551144905562e506053670c40b059`

The existing artifact was downloaded through the GitHub Actions artifact route used by the B19 handoff contract. No owner file handling and no candidate reconstruction were used.

Fresh-consumer readback of the downloaded outer artifact:

- observed bytes: `225323`
- observed SHA-256: `07d9b9e70181983172b7af448e07e087ec9551144905562e506053670c40b059`
- ZIP CRC/integrity: `PASS`
- members: `15`
- published `SHA256SUMS` entries checked: `14/14 PASS`

Exact nested installable candidate:

- filename: `Yandex-Marketing-Bridge-0.1.6.zip`
- observed bytes: `220045`
- observed SHA-256: `81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2`
- ZIP CRC/integrity: `PASS`
- product files after fresh extraction: `67`
- archive root: exactly one root, `Yandex-Marketing-Bridge-0.1.6/`
- path-safety readback: no absolute paths or `..` traversal components encountered
- independently recalculated product-tree SHA-256 using the canonical file-hash manifest algorithm: `b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86`

Manifest readback from the exact nested ZIP:

- version: `0.1.6`
- `https://searchapi.api.cloud.yandex.net/*`: present exactly once
- `https://operation.api.cloud.yandex.net/*`: present exactly once
- `alarms` permission: absent

`PACKAGE_RESULT.json` and `FINAL_PACKAGE_GATE.json` inside the downloaded artifact agree on the same exact package/tree identity. They continue to state `release_allowed=false`; the development package/browser gate PASS is not being relabelled as independent Codex PASS.

## Pre-Codex conclusion

Exact-artifact transport/readback requirement: `PASS`.

Artifact substitution/rebuild: `NO`.

Production edits during this checkpoint: `0`.

Real Yandex provider calls: `0`.

Owner credentials used: `NO`.

Owner browser/profile touched: `NO`.

Independent Codex PD-00..PD-17 campaign: `NOT_RUN`.

Overall release state remains:

```text
PRODUCT_VERSION = 0.1.6
PRODUCT_TREE_SHA256 = b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86
INSTALL_ZIP_SHA256 = 81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2
INSTALL_ZIP_BYTES = 220045
PRE_CODEX_TRANSPORT_READBACK = PASS
INDEPENDENT_CODEX_GATE = NOT_RUN
RELEASE_ALLOWED = NO
OWNER_INSTALLABLE_HANDOFF = FORBIDDEN
```

Next authorized unit: execute the already-persisted `B19_INDEPENDENT_CODEX_GATE_PROMPT.md` as one independent full PD-00..PD-17 campaign against this exact ZIP. Do not edit production during that campaign. If any enabled mandatory section is `NOT_RUN`, overall PASS is forbidden.
