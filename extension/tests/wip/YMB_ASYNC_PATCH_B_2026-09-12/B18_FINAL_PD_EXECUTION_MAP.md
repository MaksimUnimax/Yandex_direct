# B18 — consolidated executable PD map on exact B17

Date: 2026-09-13. Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`.

This map is **development qualification evidence**, not the independent Codex verdict. Product bytes are unchanged from B17:

- tree SHA-256: `b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508`;
- internal QA ZIP: `1560599adfcfdb2c3180ec9103005b1584bcd39709b8fc45e233f6c1bdd11ee1`, 225660 bytes, 67 files;
- ready exact artifact: run `34699125356`, artifact `10299402884`;
- B18 production changes: **0**;
- live provider calls: **0**;
- operation host permission: **disabled**.

B18 unified Node runner completed against this exact product: original 132, Wordstat/backup 78, full/contract 99, modules 254, export 84, delivery 69; failed/skipped/cancelled = 0. Counts overlap and are not a unique-function total. CI run `34731428403`, artifact `10309960620`, round-trip PASS with 88 inner hashes.

## Mandatory PD-00…PD-17 mapping

| PD | Exact B17 executable evidence available before independent gate | Development qualification |
|---|---|---|
| PD-00 authority/freeze/identity | B17 exact package/tree, B17 cursor/raw logs, B18 node artifact round-trip | READY |
| PD-01 complete source regression | B13 original 132 + B18 unified 132/78/99/254/84/69 on unchanged B17 | READY |
| PD-02 syntax/manifest/static | B17 61/61 JS, manifest/JSON/package identity; B18 exact candidate reverified | READY |
| PD-03 package/fresh extraction | B17 deterministic package, negative packer inputs, Actions round-trip; exact 67-file extraction | READY |
| PD-04 runtime/MV3 lifecycle | Exact B17 Chrome: MV3 load, content/popup, real worker target close/restart, saved raw/UNKNOWN recovery, whole-browser profile close/reopen and persisted state. Gate requires a **safe worker restart/lifecycle contour**, not a specific `chrome.runtime.reload()` popup-navigation implementation | READY |
| PD-05 popup/settings | B16/B17 real popup; B18 browser recheck: five dedicated credentials, explicit Save/Check, unsaved-field isolation, policies | READY |
| PD-06 Manual action/DOM | B15–B17 real content controls, native Copy isolation, PRE/controlled CM shape, stable plaques/picker, navigation isolation | READY |
| PD-07 full-block discovery/content→worker | B18 whole-block/source-order/no-parallel-fanout, local errors, selected-block isolation | READY |
| PD-08 Wordstat | B13 all four methods/faults/credentials plus B18 unified exact-B17 rerun | READY |
| PD-09 policy/credentials/cost | B5–B17 shared admission/accounting/recovery plus B18 five-service credential isolation and provider-boundary fixtures | READY |
| PD-10 Autorun | B10/B17 lifecycle plus B18 installed popup pickup/pause/resume/stop/reload/owner cases | READY |
| PD-11 delivery FSM | B17 real 1/10/32/64 MiB, repeat64, File/DataTransfer/Send/ACK, corrupt chunk, duplicate Send, pause/resume/restart | READY |
| PD-12 Debug/error | B13 Debug OFF/ON storage/redaction plus B18 visible errors/diagnostics redaction | READY |
| PD-13 ownership/isolation | B16 wrong-chat RED→GREEN, tabs/conversation binding, generic Copy/user turn/conflicting identity fail closed | READY |
| PD-14 backup/import/migration | B13 V3/legacy/checksum/active-work guards; B18 fresh-install restore and checksum/security assertions | READY |
| PD-15 security/provider containment | B18 injected host/headers/credentials ignored, fixed service host/folder, secret redaction, zero live provider requests | READY |
| PD-16 phase locks | Exact manifest has no `operation.api.cloud.yandex.net` permission; deferred submit/collect fail closed while ordinary enabled services remain functional | READY for **disabled deferred-network candidate** |
| PD-17 evidence/final cleanliness | Exact B17 package, preserved RED/FAIL_HARNESS histories, full raw logs and B18 artifact round-trips | READY for independent campaign |

`READY` above means the mandatory assertion has an executable qualified venue and development evidence on the exact B17 product. It **does not** mean independent Codex PASS.

## `chrome.runtime.reload()` supplemental diagnostic — not a hidden PASS

Several B18 QA experiments additionally exercised `chrome.runtime.reload()` although PD-04 only requires a safe worker restart/lifecycle contour. Preserve them as supplemental diagnostics:

1. run `34731585712`: all other B18 browser assertions passed; after reload, direct `chrome-extension://.../popup.html` navigation returned `ERR_BLOCKED_BY_CLIENT`;
2. run `34732438321`: same direct extension-page problem without a worker debugger;
3. run `34733052385`: QA syntax error before browser product assertions — `FAIL_HARNESS`;
4. run `34733143424`: same extension remained registered/enabled/same ID/version after reload; Puppeteer `Extensions.triggerAction` target closed — QA action path failure;
5. run `34733280541`: registry survived; Puppeteer did not expose a content-script realm — QA observability failure;
6. run `34733434071`: QA waited for `targetdestroyed` on a debugger-attached worker and timed out — contradictory harness design;
7. run `34733531060`: no pre-reload worker debugger; registry survived, but target filtering also prevented post-reload worker observation — harness design failure;
8. later QA-only probes remain supplemental and must be classified by their actual layer.

None of these supplemental failures overwrite the exact B17 worker-close/profile-restart PASS that satisfies PD-04. None is relabeled as product PASS. If future evidence demonstrates a real `chrome.runtime.reload()` product defect, open a new bounded product defect with RED→GREEN rather than editing this history.

## Remaining release boundary

The exact B17 **disabled-deferred-network** product is now mapped for a complete independent PD campaign. The independent campaign has not run and therefore release remains forbidden.

A second, separate owner decision is still required before deferred Search network activation: adding the Operation API host permission and performing authorized auth/provider capability canaries would change final production bytes and would require exact-target requalification. Do not silently enable that permission and do not make paid/live provider calls under this B18 development qualification.

Current verdict:

```text
B18_DEVELOPMENT_PD_MAPPING = COMPLETE
EXACT_PRODUCT_CHANGED_IN_B18 = NO
INDEPENDENT_CODEX_GATE = NOT_RUN
OPERATION_HOST_ENABLED = NO
LIVE_PROVIDER_CALLS = 0
RELEASE_ALLOWED = NO
OWNER_INSTALLABLE_HANDOFF = FORBIDDEN
```

## ПРОСТЫМИ СЛОВАМИ

B18 собрал все обязательные проверки в одну карту. Для каждого раздела финального gate уже есть конкретный тестовый путь на сохранённой B17-сборке. Дополнительные проблемы Puppeteer вокруг `chrome.runtime.reload()` не скрыты, но они не являются отдельным обязательным PD-04 требованием и не отменяют уже выполненный настоящий restart worker/браузера. Следующий этап — независимый полный gate на этих точных байтах; включение сетевого deferred Search остаётся отдельным разрешённым изменением.
