# B18 — unified final development qualification and exact PD execution map

Date: 2026-09-13. Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`.

**B18 development qualification is complete on the exact B17 product. No production bytes changed in B18. Independent Codex pre-delivery gate has not run. RELEASE_ALLOWED = NO.**

## 1. Exact product under qualification

B18 reused the exact already-qualified B17 candidate instead of rebuilding A/B1–B17:

- product tree SHA-256: `b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508`;
- files: 67;
- exact internal QA ZIP SHA-256: `1560599adfcfdb2c3180ec9103005b1584bcd39709b8fc45e233f6c1bdd11ee1`;
- ZIP bytes: 225660;
- ready exact B17 artifact: run `34699125356`, artifact `10299402884`;
- production changes in B18: **0**;
- Operation API host permission: **disabled**;
- real/live provider requests in B18: **0**;
- owner browser/profile touched: **no**.

The B17 product remains the candidate under test. B18 added only QA runners, evidence, mapping and documentation.

## 2. One unified executable Node campaign

`qa/b18_node_campaign.py` runs the previously qualified executable Node/VM suites against the exact B17 product and rejects wrong/incomplete inputs before granting PASS.

CI run `34731428403`, artifact `10309960620`, artifact SHA-256 `9115aab772d2b1de314b28363b4ef61b9cf849c33e8d49f4fa56a0e4ef962e8f`, 78717 bytes; fresh download/consumer verification passed 88 inner hashes.

Final available Node scope:

- original extension source suites: 132 PASS;
- Wordstat / Debug / backup coverage: 78 PASS;
- full/contract set: 99 PASS;
- saved module regressions: 254 PASS;
- export/file-delivery module set: 84 PASS;
- delivery/pause/context set: 69 PASS;
- failed/skipped/cancelled: 0.

These sets overlap. They are not summed as a unique-function count. No real provider request is part of this campaign.

## 3. Remaining real-browser development qualification

The B18 browser work targeted PD assertions that were still only partially covered by prior B15–B17 development runs. The exact B17 extension was installed in isolated GitHub-hosted Chrome for Testing/Puppeteer; provider outcomes and ChatGPT page content were controlled fixtures.

The successful mandatory development cases include:

- five dedicated service credentials with explicit Save/Check and password-field non-repopulation;
- popup policy/toggle behavior and unsaved-field isolation;
- whole Manual block capture in source order with no parallel provider fanout;
- plain/malformed/validation/unsupported local errors without provider execution;
- injected URL/headers/credentials ignored at the fixed service provider boundary;
- Debug OFF/ON visible error behavior and diagnostic secret redaction;
- legacy command adapters and selected-block isolation;
- generic Copy/user-turn isolation and conflicting conversation identity fail-closed;
- stable operation/composer/picker status surfaces and native picker no-Send behavior;
- installed Autorun pickup/pause/resume/stop/reload/ownership behavior;
- fresh-install backup restore/checksum/security assertions.

Run `34731585712` is the most complete remaining-browser development recheck. All mandatory cases above passed on exact B17. Its only failing assertion was an extra `chrome.runtime.reload()` experiment that attempted to reopen an extension popup through direct Puppeteer extension-page navigation and received `ERR_BLOCKED_BY_CLIENT`.

## 4. PD-04 and the supplemental `chrome.runtime.reload()` experiments

The authoritative PD-04 requirement is a **safe worker restart/lifecycle contour**. Exact B17 already executed that requirement in real Chrome before B18:

- MV3 service worker installed and running;
- real worker target close/restart;
- preserved raw/UNKNOWN state and no replay;
- whole-browser profile close/reopen with durable state;
- content script and popup initialization on controlled pages.

Therefore B18 does not redefine PD-04 to require a particular Puppeteer implementation of `chrome.runtime.reload()` popup reopening.

All additional `chrome.runtime.reload()` experiments are nevertheless preserved rather than hidden. They repeatedly established some useful facts — same extension ID, enabled state and version after reload — while failing in different Puppeteer observability/action paths. They are classified at their actual layer (`FAIL_HARNESS` / supplemental diagnostic), not as product PASS and not as product FAIL without a reached product assertion.

The preserved history includes runs `34731010004`, `34731343657`, `34731585712`, `34732438321`, `34733052385`, `34733143424`, `34733280541`, `34733434071`, and `34733531060`. Later QA-only reload probes remain supplemental and do not block the mandatory PD map.

## 5. Consolidated PD-00…PD-17 mapping

`B18_FINAL_PD_EXECUTION_MAP.md` maps every enabled PD section to a concrete executable venue/test source on the exact B17 candidate. Development mapping result:

```text
B18_DEVELOPMENT_PD_MAPPING = COMPLETE
ALL_PD_SECTIONS_HAVE_QUALIFIED_EXECUTABLE_MAPPING = YES
EXACT_PRODUCT_CHANGED_IN_B18 = NO
```

Important distinction: **mapping complete / development-qualified is not the independent Codex verdict.** The independent campaign must still execute the governed matrix on the exact candidate and return one final PASS/FAIL verdict with no enabled NOT_RUN sections.

PD-16 is ready only for the product that exists today: ordinary enabled services remain enabled, but the new deferred Search network route is intentionally fail-closed because `https://operation.api.cloud.yandex.net/*` is absent from the manifest.

## 6. Permanent raw evidence

B18 evidence is no longer dependent on 90-day Actions retention.

A dedicated read-only/download workflow collected the complete extracted artifact members from the mandatory unified Node campaign, three browser-development runs and the supplemental reload diagnostics, built a deterministic xz/tar archive, round-tripped it with a fresh consumer and committed split binary parts to Git.

Permanent location:

`extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/evidence/B18_RAW_LOGS/`

Manifest:

- reconstructed archive SHA-256: `8d12495ab38d5f59517c05d831c814e690e37dab69ade0ff68214b13428444d3`;
- archive bytes: 70152;
- archive members: 172;
- two binary parts: 50000 + 20152 bytes;
- `restore.py` verifies every part, final archive identity and safe tar members before exclusive output;
- producer/consumer round-trip: PASS.

Permanent evidence commit: `ba4a59ca07c2be06370e707fd42bef053bb508ba`.

## 7. What remains before any owner installable handoff

### A. Independent Codex gate

The exact B17 disabled-deferred-network product now has a complete executable PD map and can be handed to the independent Codex QA executor. Codex must test the exact frozen candidate and may not change production or weaken tests. Any production-byte change invalidates applicable PASS evidence and requires a new exact candidate.

### B. Deferred Search network activation is a separate production decision

The code for deferred Search exists, but its Operation API host permission remains disabled. Enabling it changes production bytes and activates a real network surface. It must not be silently folded into this B18 PASS set.

Before a release that promises working deferred provider submit/collect, separately authorize and execute:

1. exact manifest/host-permission activation;
2. exact credential-type compatibility canary against async submit and Operation GET;
3. provider/auth/rate-limit/error canaries with explicit cost authorization where applicable;
4. exact-target regression/resource/security checks on the new bytes;
5. independent gate on the actual final release bytes.

Until then the current exact candidate is a **disabled-deferred-network candidate**, not a finished deferred-network release.

## 8. Verdict

```text
B18 = COMPLETE
PRODUCT_BYTES_CHANGED_IN_B18 = NO
UNIFIED_NODE_AVAILABLE_SCOPE = PASS
MANDATORY_BROWSER_DEVELOPMENT_COVERAGE = PASS
PD_EXECUTION_MAPPING = COMPLETE
PERMANENT_RAW_EVIDENCE = PASS
SUPPLEMENTAL_RUNTIME_RELOAD_DIAGNOSTICS = PRESERVED_NON_GATE
INDEPENDENT_CODEX_GATE = NOT_RUN
OPERATION_HOST_ENABLED = NO
LIVE_PROVIDER_CALLS = 0
FINAL_GATE_READY_FOR_DISABLED_DEFERRED_CANDIDATE = YES
RELEASE_ALLOWED = NO
OWNER_INSTALLABLE_HANDOFF = FORBIDDEN
```

## ПРОСТЫМИ СЛОВАМИ

Все обязательные проверки, которые нужно было подготовить до независимой финальной приёмки, сведены и реально имеют исполнимые тесты на одной сохранённой B17-сборке. Node-набор прошёл, недостающие браузерные сценарии пройдены, а полные логи навсегда зафиксированы в Git. Отдельные эксперименты с `chrome.runtime.reload()` не скрыты, но это проблемы конкретных QA-путей Puppeteer, а обязательный restart/lifecycle уже проверен другим реальным браузерным сценарием. Сборку владельцу пока нельзя отдавать: нужен независимый Codex gate, а если нужен именно работающий deferred Search по сети — отдельно надо включить Operation API permission и проверить реальные provider/auth границы на новых байтах.
