# Yandex Marketing Bridge — patch dependency and resource-safety rule

Status: **MANDATORY / OWNER-LOCKED / RELEASE-BLOCKING**  
Adopted: 2026-09-11  
Scope: every code patch, repair, feature, packaging change and installable build under `extension/`.

## 1. Why this rule exists

This rule is permanent because a 2026-09-11 Yandex Marketing Bridge 0.1.5 candidate was handed to the owner after functional/synthetic checks but without proving resource safety of the newly introduced large-payload/file-delivery path. The candidate could drive Chrome RAM usage to system-threatening levels.

The incident established a non-negotiable rule:

> **Functional correctness is not sufficient acceptance for code that touches large data, files, batch state, serialization, storage, recovery loops, polling, timers, observers, ports, binary buffers, Blob/File objects or browser delivery.**

No installable candidate may be handed to the owner until both functional correctness **and** resource safety are proven for the exact candidate bytes.

## 2. Exact baseline before every patch

Before modifying production code:

1. identify the exact source branch / commit / provided ZIP being changed;
2. record the exact production-file inventory and hashes where practical;
3. identify the defect or requested feature;
4. identify every direct dependency and shared subsystem touched by the change;
5. list protected existing behavior that must remain unchanged;
6. when practical, reproduce the defect on the baseline before changing production.

A patch must not be started from an approximate, stale or reconstructed baseline when the exact baseline is available.

## 3. Bounded patch scope

One patch must solve one coherent problem or one explicitly defined feature unit.

Do not combine unrelated refactors merely because the same files are open.

Existing ownership, lifecycle, provider-boundary, quota/cost, cache, persistence, recovery, delivery, security and service-isolation semantics remain authoritative unless the current feature explicitly requires changing them.

When a proven implementation already exists elsewhere in the owner's bridge codebase and the owner requests reuse, prefer adapting that proven mechanism over inventing a simplified replacement. Any intentional deviation requires an explicit reason and equivalence/regression evidence.

## 4. Mandatory dependency-impact matrix

Before declaring implementation complete, build a dependency-impact matrix:

```text
changed module
-> direct callers/importers/load order
-> shared state/storage touched
-> provider/network boundary touched
-> UI/content/worker surface touched
-> recovery/cancellation path touched
-> policy/cost/quota path touched
-> packaging/manifest/permission path touched
-> adjacent services sharing the dependency
-> exact tests required for every affected path
```

After every material edit, **all actually affected dependencies must be retested**.

Applicable checks include, but are not limited to:

- JavaScript / MJS syntax;
- protocol and command contracts;
- worker/state-machine transitions;
- persistence and recovery;
- quota/cost/cache accounting;
- owner/tab/conversation isolation;
- Manual / Autorun compatibility;
- composer / delivery / confirmation;
- browser / Puppeteer behavior;
- provider boundary and network failure behavior;
- credential isolation;
- backup/import compatibility;
- manifest/permissions/load order;
- packaging and fresh extraction;
- adjacent Wordstat/Search/GenSearch/Webmaster/Metrika/Direct regressions when a shared dependency is touched.

If an affected dependency is not tested:

```text
PATCH_ACCEPTANCE = FAIL
RELEASE_ALLOWED = NO
```

## 5. RED / GREEN rule for defects

For a bug fix, create or preserve RED -> GREEN evidence whenever practical:

```text
exact baseline -> defect reproduced / test fails
patched candidate -> same assertion passes
```

If RED evidence is not practical, record why and compensate with a stronger exact-target regression assertion.

## 6. Mandatory resource-safety trigger

A dedicated resource-safety gate is mandatory when a patch touches any of the following:

- large text or generated reports;
- Base64 encoding/decoding;
- ArrayBuffer / Uint8Array / Blob / File / DataTransfer;
- IndexedDB / chrome.storage / storage migrations;
- file attachment or download/upload delivery;
- batch sizes in the hundreds or thousands;
- large result payloads;
- polling, timers, observers, ports or long-lived listeners;
- recovery loops or repeated serialization;
- cloning/copying of job/result structures;
- gzip/decompression/compression;
- transformations whose memory use scales with payload size.

If the trigger applies, resource safety is a **release-blocking requirement**, not an optional performance test.

## 7. Mandatory large-file memory matrix

For a large-file / large-text / attachment path, test at least:

```text
1 MB
10 MB
32 MB
64 MB
```

If the intended production path can legitimately exceed 64 MB, test the larger supported size as well.

Measure and record, as applicable:

- baseline idle memory;
- peak process RSS / private memory where measurable;
- JS heap where measurable;
- number of simultaneously materialized full-payload copies;
- temporary allocation behavior;
- post-operation cleanup/reclamation trend;
- repeated-run memory trend;
- reload/recovery memory trend;
- cancel/failure cleanup;
- storage-read/write amplification;
- CPU/time amplification caused by repeated full-payload work.

Mandatory assertions:

```text
NO_UNBOUNDED_MEMORY_GROWTH = PASS
NO_FULL_STORE_READ_PER_CHUNK = PASS
NO_REPEATED_FULL_PAYLOAD_CLONING = PASS
NO_BASE64_OVER_BASE64_WITHOUT_PROVEN_NEED = PASS
NO_UNNECESSARY_CHUNKS_PLUS_FULL_BUFFER_DUPLICATION = PASS
NO_ACCUMULATING_TIMERS_OBSERVERS_PORTS = PASS
POST_OPERATION_CLEANUP = PASS
REPEATED_RUN_LEAK_TEST = PASS
```

## 8. Mandatory large-batch matrix

For a batch path intended to operate at scale, test at least:

```text
10 items
100 items
500 items
1500 items
```

If product limits differ, also test the actual maximum intended supported volume.

The test must verify more than result correctness. Record:

- runtime growth as item count increases;
- memory growth as item count increases;
- storage operation count and amplification;
- whether one-item updates clone/rewrite the whole batch;
- whether algorithmic behavior becomes quadratic or worse unexpectedly;
- whether completed provider results accumulate unnecessarily in active memory;
- partial completion and recovery at scale;
- restart/reload recovery;
- duplicate-action protection;
- cancel/pause behavior;
- no provider replay from recovery.

A scale test that times out, exhausts memory or is not completed is not PASS.

## 9. Permanent negative regression case — YMB 0.1.5

Future file-delivery and large-payload tests must explicitly reject the failure pattern observed in the withdrawn 0.1.5 candidate:

```text
large payload
-> full in-memory text/bytes copy
-> Base64 expansion
-> all Base64 chunks stored inside one large chrome.storage object
-> every requested chunk reloads/deserializes the entire large object
-> content side retains every decoded chunk
-> another full Uint8Array is allocated
-> File/Blob representation is allocated as well
```

The following implementation patterns require explicit proof or must be rejected:

- `N chunks x full-store read`;
- serializing the whole artifact map for every chunk;
- holding `chunks[]` and an additional full buffer simultaneously without proven necessity;
- converting already-Base64 provider payloads into another full Base64 transport layer without bounded-memory evidence;
- storing a 500/1500-item mutable job as one giant JSON object and cloning/stringifying the whole structure for every item transition.

A new implementation does not pass merely because it uses the word "chunked". The memory/storage behavior must actually be bounded and measured.

## 10. Browser/runtime evidence is mandatory when the browser owns the risk

Synthetic Node/VM tests do not prove Chrome resource safety, DOM attachment behavior, MV3 worker lifecycle, browser File/DataTransfer behavior or process-level memory usage.

If the changed path is browser-owned, an appropriate qualified browser test is mandatory before release.

If the required browser/resource test cannot be executed and is classified as `BLOCKED`:

```text
REQUIRED_RESOURCE_TEST = BLOCKED
RELEASE_ALLOWED = NO
```

Do not substitute "unit tests passed" for a required browser/resource PASS.

## 11. Failure classification

Use precise classes:

- `PASS` — required assertion executed and succeeded;
- `FAIL_PRODUCT` — exact candidate established and product assertion failed;
- `FAIL_RESOURCE` — exact candidate showed unsafe or unbounded resource behavior;
- `FAIL_ARTIFACT` — candidate/package bytes or inventory are wrong;
- `FAIL_HARNESS` — governed assertion could not execute because the validation environment/harness failed;
- `BLOCKED` — required proof cannot currently be reached safely.

`BLOCKED`, `FAIL_HARNESS` and `NOT_RUN` never count as PASS for a mandatory release assertion.

## 12. Exact-target and dependency-regression rule

Evidence belongs to the exact production bytes it exercised.

After a production-byte change:

- rerun focused tests for the changed path;
- rerun every affected dependency regression;
- rerun applicable resource tests;
- preserve unchanged exact-target evidence only when production bytes relevant to that assertion are demonstrably unchanged;
- do not claim an old report proves a later candidate.

## 13. Pre-delivery release gate

Before handing any installable ZIP/build to the owner, the exact candidate must satisfy:

```text
EXACT_BASELINE_FROZEN = PASS
PATCH_SCOPE_BOUNDED = PASS
DEPENDENCY_MATRIX_COMPLETE = PASS
RED_REPRODUCTION = PASS_OR_JUSTIFIED_NA
TARGETED_TESTS = PASS
ALL_IMPACTED_DEPENDENCIES = PASS
OLD_FUNCTIONALITY_REGRESSION = PASS
MEMORY_STRESS = PASS_OR_NOT_APPLICABLE
LARGE_DATA_STRESS = PASS_OR_NOT_APPLICABLE
REPEATED_RUN_LEAK_TEST = PASS_OR_NOT_APPLICABLE
RECOVERY_TEST = PASS_OR_NOT_APPLICABLE
BROWSER_REQUIRED_TESTS = PASS_OR_NOT_APPLICABLE
SECURITY_PROVIDER_BOUNDARY = PASS
FRESH_PACKAGE_EXTRACTION = PASS
PACKAGE_BYTES_MATCH_TESTED_CANDIDATE = PASS
```

For any item marked `NOT_APPLICABLE`, the reason must be explicit and technically defensible.

If any mandatory item is `FAIL`, `BLOCKED`, `FAIL_HARNESS`, `NOT_RUN` or otherwise unproven:

```text
RELEASE_ALLOWED = NO
OWNER_HANDOFF = FORBIDDEN
```

The owner must not receive the candidate framed as ready/working.

## 14. Fresh-package rule

The installable artifact handed to the owner must be the exact tested candidate.

Before handoff:

1. build/package only intended production files;
2. record artifact SHA-256 and byte count;
3. extract into a fresh location;
4. verify inventory and file hashes against the tested production candidate;
5. run syntax/static/package checks on the fresh extraction;
6. rerun any package-sensitive regression on the extracted artifact;
7. never substitute a logically equivalent but byte-different package without re-establishing evidence.

## 15. No false readiness claims

Do not state or imply:

- "safe" when resource safety was not measured where required;
- "fully tested" when a mandatory path is BLOCKED/NOT_RUN;
- "production ready" when only synthetic tests passed for a browser-owned feature;
- "no regressions" when affected dependencies were not enumerated and tested;
- "same build" when source/package byte identity was not checked.

## 16. Required patch report

Every material patch report must contain:

1. exact baseline;
2. defect/feature statement;
3. changed files;
4. dependency-impact matrix;
5. protected invariants;
6. RED/GREEN evidence or justified N/A;
7. focused test results;
8. affected-dependency regression results;
9. resource test results when triggered;
10. browser/live boundary;
11. exact package identity;
12. unresolved blockers;
13. explicit `RELEASE_ALLOWED = YES|NO` verdict.

## 17. Authority relationship

This rule is mandatory alongside:

- `extension/README.md`;
- `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`;
- the current feature/phase-specific authority;
- exact provided owner source/build when the owner supplies a candidate archive.

When a future feature-specific document is less strict than this rule on dependency or resource safety, **this rule wins unless the owner explicitly supersedes it**.
