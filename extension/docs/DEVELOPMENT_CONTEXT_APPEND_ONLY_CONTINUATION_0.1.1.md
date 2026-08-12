# DEVELOPMENT CONTEXT — APPEND-ONLY CONTINUATION — 0.1.1

Created: 2026-08-12.

## Chain rule

This file is an append-only continuation of:

```text
extension/docs/DEVELOPMENT_CONTEXT_APPEND_ONLY.md
```

The parent file is intentionally **not rewritten**. Historical entries 0001–0021 remain evidence of what was actually decided and implemented, including decisions later found to be wrong.

Current state is determined by the latest applicable entry in this continuation plus the current living `PROJECT_PURPOSE.md`, `SPECIFICATION.md` and `ROADMAP.md`.

---

# ENTRY 0022 — 2026-08-12 — LIVE 0.1.0 FAILURE: MANDATORY JOB ID WAS WRONG

During the first real ChatGPT-command acceptance attempt, the 0.1.0 candidate rejected a valid Wordstat command with:

```text
JOB_ID_MISSING: Укажите Job ID текущего заказа.
```

This proved that Phase 0/early Phase 1 had incorrectly coupled extension runtime to order/GitHub concepts.

Correction:

- `job_id` is not required by Yandex Wordstat;
- `job_id` is not a runtime authorization property of the Bridge;
- GitHub order workspaces are managed externally by ChatGPT/development workflow;
- the extension must execute safely without knowing a GitHub repository, branch, commit or `work/<job_id>/` path.

Decision: 0.1.0 is withdrawn. Search remains blocked.

---

# ENTRY 0023 — 2026-08-12 — EXPORT / IMPORT SETTINGS IS A REQUIRED REFERENCE MECHANISM

The owner clarified that preserving one storage key is insufficient. The relevant Business Bridge reference contains explicit settings Export/Import behavior for migration between unpacked installation identities.

0.1.1 therefore adds:

```text
Export settings
Import settings
```

Backup contract:

```text
format
backup_version
settings_schema_version
exported_at
extension_version
extension_id
contains_secrets = true
profile_count
settings_sha256
settings
```

The backup intentionally contains credentials and must be treated as a secret file.

Import verifies canonical SHA-256, rejects tampering, merge-imports compatible settings, creates a local rollback backup and does not replace active execution transactions.

Additional repair found during testing: active RUN/manual-operation conversation binding, service context and manual-mode safety state must also be preserved so an imported backup cannot silently invalidate a live run.

---

# ENTRY 0024 — 2026-08-12 — ALL ERRORS MUST AUTOMATICALLY RETURN TO CHATGPT

Owner requirement:

**Every error, in every operating mode, must automatically arrive in the current bound ChatGPT conversation.**

This requirement is independent of Debug Mode.

Adopted contract:

```text
Debug OFF
→ YMB_ERROR_V1 automatically delivered

Debug ON
→ same YMB_ERROR_V1
→ plus additional redacted diagnostic logs
```

Debug Mode changes diagnostic detail only; it never enables/disables error delivery.

Recoverable Autorun errors should not silently terminate automatic work. When safe, the RUN returns to command waiting after the error report is delivered.

If request outcome is unknown, the error reports that fact and automatic retry remains forbidden.

---

# ENTRY 0025 — 2026-08-12 — DURABLE ERROR DELIVERY / NO DUPLICATE SEND

Error delivery was implemented as a worker-owned durable outbox rather than a transient toast.

Lifecycle:

```text
claimed
→ stage exact YMB_ERROR_V1 in composer
→ durable commit before Send click
→ one browser Send click
→ confirmed user-turn
```

After a committed Send boundary, reload/recovery is reconciliation-only. It cannot blindly click Send again and cannot repeat the original Yandex request.

Regression tests cover duplicate commit so exactly one runtime receives click authorization.

---

# ENTRY 0026 — 2026-08-12 — MANUAL ERRORS AND ERROR QUEUE RESPONSE CONTRACT

I/O emulation found two defects after the first green repair checkpoint:

1. Manual invalid `WORDSTAT_API_V1` parse error showed only a local toast and did not reach ChatGPT.
2. A specialized worker path could durably queue an error but still respond with `error_report_queued: false`.

Both were fixed.

Current contract:

- Manual parse/validation errors use the same always-on ChatGPT error-delivery path;
- if an error is already durably queued, the runtime response reports `error_report_queued: true`;
- generic message error handling does not enqueue a duplicate report.

---

# ENTRY 0027 — 2026-08-12 — MANUAL ON PAUSED RUN MUST NOT BYPASS RUN BUDGET

Removing the incorrect JOB-level accounting exposed another safety boundary.

Decision:

- standalone Manual with no active RUN is an explicit per-Copy operator action and has no invented Job budget;
- Manual used while an Autorun RUN is PAUSED belongs to the same RUN budget;
- its attempt/executed/skipped counters and estimated cost are recorded in that RUN;
- RUN request/cost limits apply before the Manual external initiation.

Therefore:

```text
Pause RUN
→ switch/use Manual
→ cannot bypass RUN ceiling
```

---

# ENTRY 0028 — 2026-08-12 — 0.1.1 PRE-LIVE AUTOMATED ACCEPTANCE

Current exact candidate:

```text
yandex-marketing-bridge-0.1.1-phase1-repair-candidate.zip
SHA-256 311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb
size 172705 bytes
files 41
```

Final automated/pre-live evidence after all repairs above:

```text
source full suite:          311/311 PASS
fresh ZIP full suite:       311/311 PASS
source ↔ fresh ZIP:          41/41 byte-identical
fresh ZIP JS/MJS syntax:     36/36 PASS
manifest/package JSON:        2/2 PASS
manifest/package version:   0.1.1 / 0.1.1
Chromium 144 load smoke:     PASS
```

No paid Yandex request was executed while developing/testing this repair.

Machine-readable evidence:

```text
extension/tests/PHASE_1_0.1.1_PRELIVE_TEST_EVIDENCE.json
```

Current gate:

```text
PHASE 0: PASS
PHASE 1: 0.1.1 PRE-LIVE PASS / PRODUCTION CHATGPT LIVE PENDING
PHASE 2 SEARCH: BLOCKED
```

Production live acceptance in the owner's real Chrome remains mandatory before Search development.

---

# ENTRY 0029 — 2026-08-12 — GOVERNED TEST-PLAN-FIRST / PATCH-AFTER-LEDGER RULE

The owner changed the Phase 1 live-testing method after repeated defect discovery during ad-hoc testing.

Mandatory rule from this checkpoint forward:

1. **Before additional test execution begins, create and commit one explicit test-plan/result ledger containing the complete intended test set.**
2. Execute tests against that ledger, marking each test `PASS`, `FAIL`, `BLOCKED`, `TEST ERROR` or `NOT RUN` and recording actual versus expected behavior.
3. Newly discovered test requirements must be appended to the ledger before they are executed.
4. **Do not begin the implementation patch while the test campaign is still discovering defects**, unless the owner explicitly orders an immediate interruption and patch.
5. When the campaign is complete, derive the patch scope from the documented FAIL/BLOCKED defect set rather than from memory or ad-hoc conversation state.
6. After patching, rerun affected tests plus the required full regression set and update the same ledger with post-patch evidence.

Execution-channel clarification:

- real Yandex/extension command behavior is tested in the current ChatGPT conversation through actual `WORDSTAT_API_V1` commands;
- maximum one executable Yandex command per assistant turn;
- current official Yandex pricing is freshly checked before every command that can make a real Yandex request;
- popup/UI/toggle/state-machine behavior is tested in controlled browser/emulation by the assistant and is not offloaded to the owner as repetitive manual UI testing;
- static/unit/regression tests remain supporting evidence only and do not replace mandatory live command gates.

Authoritative active ledger:

```text
extension/tests/PHASE_1_0.1.1_LIVE_TEST_PLAN_AND_RESULTS.md
```

The ledger also carries forward pre-rule live evidence already observed in the installed 0.1.1 candidate, including:

- generic/non-reference YMB plaque behavior;
- Debug toggle persistence failure;
- Autorun start failure;
- incorrect `charged:true` semantics for zero-cost `getRegionsTree`;
- successful live execution evidence for the core Wordstat methods already exercised.

Search remains blocked until the governed ledger has no unresolved mandatory FAIL/BLOCKED acceptance item on the patched candidate.
