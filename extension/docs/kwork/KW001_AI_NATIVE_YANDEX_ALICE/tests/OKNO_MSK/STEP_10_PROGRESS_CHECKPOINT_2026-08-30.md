# KW-001 / OKNO-MSK — STEP 10 PROGRESS CHECKPOINT — 2026-08-30

Status: **ACTIVE / NOT ACCEPTED / V19 MACHINE+HARD GATES PASS / MANUAL SEMANTIC QA FAIL**

This checkpoint supersedes the earlier 2026-08-30 state and records the exact stop point requested by the owner.

## 1. Step-10 goal

Build an auditable user-task / SERP clustering layer that determines which phrases express the same or materially compatible user task, which must stay separate, which are supported by direct Step-09 SERP evidence, which are semantic-only, and which remain genuinely unresolved / SEARCH_REQUIRED.

Step 10 must NOT decide page ownership, page keep/merge/split/create actions, cannibalization, Search architecture freeze, or AI-search cases. Those belong to later roadmap steps.

## 2. Current completion state

Substantive implementation progress remains approximately **85–90%**.

Formal state:

```text
STEP10_EXECUTION_STARTED = true
STEP10_MACHINE_QA = PASS
STEP10_DIRECT_SERP_CONTRADICTION_GATE = PASS
STEP10_V19_COLLISION_HARD_GATE = PASS
STEP10_V19_UNRESOLVED_HARD_GATE = PASS
STEP10_MANUAL_SEMANTIC_QA = FAIL / IN PROGRESS
STEP10_COMPLETE = false
STEP10_ACCEPTED = false
STEP11_ALLOWED = false
```

The percentage is only a progress estimate. It does not override the PASS gate.

## 3. What changed since the earlier checkpoint

The previous V19 roof-taxonomy expansion was found to be unsupported and was removed rather than weakening old regression tests.

Protected boundaries now remain:

```text
панорамное окно на крыше
-> PANORAMIC_WINDOWS_COMMERCIAL

окна для крыши частных домов
-> PRIVATE_HOUSE_WINDOWS_COMMERCIAL
```

The attempted separate `ROOF_WINDOWS_COMMERCIAL` taxonomy was removed because it was being introduced to satisfy an audit rather than from sufficiently supported clustering evidence.

Implementation commits after the prior checkpoint:

```text
553681f2148b546d3737ef5d101135c02dc127ce
  step10: preserve panoramic roof boundary in V19

984fbaef00cf7b7d31d89bc45e65f04fb3ef0738
  step10: remove unsupported V19 roof taxonomy expansion

93f48b7bda50bc68f3c6ec87abbd4b7120e72070
  step10: adjudicate remaining V19 collision false positives
```

## 4. V19 full pipeline result

GitHub Actions run:

```text
run = 33286539033
job = 99190583856
conclusion = SUCCESS
```

All workflow stages passed:

```text
Build conservative Step10 user-task clusters = PASS
Step10 machine accounting gate = PASS
direct Step09 service-product contradiction gate = PASS
V19 adversarial semantic collision hard gate = PASS
V19 unresolved-state hard gate = PASS
generated candidate/artifact commit = PASS
```

Bot-generated V19 candidate commit:

```text
f62932ebe80de18a8ee39113a3080faaf7ecde81
message = step10: rebuild clusters after V19 specificity and hard-gate corrections
```

## 5. Current V19 machine-QA facts

```text
total phrase keys = 2840
active Search-stage rows = 2332
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
cluster_count = 73
SEARCH_REQUIRED = 70
MIXED_OR_BOUNDARY_REVIEW = 2
SEMANTIC_SUPPORTED_NO_DIRECT_SERP = 2197
SERP_SUPPORTED = 63
75 Step-09 probes consumed = 66 exact + 9 control anchors
8 duplicate comparisons consumed
DUP0004 auto merge = false
unprobed rows claiming direct SERP = 0
silent drops = 0
page ownership decisions = 0
structural action decisions = 0
cannibalization decisions = 0
provider requests = 0
provider cost = 0 RUB
```

`STEP_10_QA.json` correctly remains:

```text
status = MACHINE_QA_PASS__MANUAL_SEMANTIC_QA_REQUIRED
manual_semantic_qa_pass = false
```

## 6. V19 hard-gate facts

### Collision hard gate

```text
status = PASS
active rows scanned = 2332
flagged rows = 0
flagged records = 0
```

Three inherited false positives were manually adjudicated before this PASS:

```text
окна для крыши частных домов
панорамное окно на крыше
сколько стоит панорамное окно
```

The classifier was not changed merely to satisfy those audit flags; audit semantics were corrected instead.

### Unresolved hard gate

```text
status = PASS
SEARCH_REQUIRED rows scanned = 70
flagged rows = 0
flagged records = 0
intentionally mixed direct rows = 1
```

Intentionally mixed direct example remains:

```text
цены материала на пластиковые окна
SP09-039
AMBIGUOUS_PRICE_MATERIAL_BOUNDARY
```

## 7. Why Step 10 is STILL NOT accepted

After V19 machine/hard-gate PASS, full manual semantic QA was resumed across the cluster summary and representative sample.

Manual QA found real semantic errors that the current hard gates do not detect. Therefore the hard gates are necessary but not sufficient, exactly as the methodology requires.

Confirmed remaining real error classes:

### A. Balcony-glazing demolition lost inside generic glazing

```text
демонтаж остекления балкона
current = BALCONY_GLAZING
Step-09 direct evidence = BALCONY_GLAZING_DEMOLITION / COMMERCIAL_SERVICE
```

A distinct `WINDOW_DEMOLITION` task already exists, so this service-vs-service subtype boundary needs correction rather than remaining inside generic balcony glazing.

### B. PVC-door repair DIY swallowed by installation DIY

```text
регулировка пластиковых дверей своими руками
current = PVC_DOOR_INSTALLATION_DIY
expected semantic task = PVC_DOOR_REPAIR_DIY
```

Explicit repair/adjustment action must outrank generic DIY installation handling.

### C. Commercial measurement+installation package classified as informational measurement

Examples:

```text
заказ окон пластиковых с замером и установкой
замер и установка пластиковых окон москва
пластиковые окна установка цена с размерами
```

Current cluster:

```text
WINDOW_MEASUREMENT_INFO / INFORMATIONAL
```

These phrases contain explicit commercial/service intent and should not be reduced to informational measurement merely because measurement/size language is present.

### D. Direct windowsill-repair evidence remains inside generic window repair

```text
ремонт подоконников пластиковых окон
current = WINDOW_REPAIR
Step-09 direct evidence = WINDOWSILL_REPAIR / COMMERCIAL_REPAIR_SERVICE
```

A dedicated `WINDOWSILL_REPAIR` cluster already exists, so the specific component-repair task should win.

### E. SEARCH_REQUIRED hard gate still misses obvious resolvable tasks

Manual inspection of the 70 unresolved rows exposed examples that should not remain unresolved, including:

```text
студия с панорамными окнами
  -> architecture / real-estate context

теплый пол панорамные окна
  -> heating context

угловое панорамное окно
  -> panoramic product/configuration

устанавливаем французские окна
  -> installation/service

французские вертикальные задвижки для окон
  -> hardware/component

французские занавески на окна
  -> curtains

французские окна название
что значит французское окно
  -> definition/naming

французский тип окон
  -> information/types

французское окно распашное
  -> product/configuration

французское окно оформление
французское окно примеры
  -> design/inspiration
```

Therefore `V19_UNRESOLVED_HARD_GATE = PASS` is not sufficient evidence that all remaining unresolved rows are truly ambiguous. The unresolved audit itself needs another strengthening pass.

## 8. Root cause of current remaining work

The current bottleneck is still classifier/audit precedence, but the failure surface has narrowed significantly.

The recurring semantic pattern is:

```text
specific action/object/component/user task
must outrank
broad material / panoramic / French / DIY / private-house / measurement fallback
```

The next version must fix classes, not individual strings.

Do NOT reintroduce unsupported taxonomy merely to make an audit green.

## 9. Exact resume point

Next implementation iteration should be **V20**.

V20 should address, as classes:

```text
1. demolition action > generic object glazing;
2. PVC-door repair/adjustment DIY > installation DIY;
3. explicit commercial order/install/price + measurement > informational measurement;
4. windowsill-specific repair > generic window repair;
5. French/panoramic object-specific action/component/design/definition/context > generic unresolved fallback;
6. strengthen unresolved hard gate to flag those obvious resolvable classes.
```

Then execute in this exact order:

```text
1. inherited regression corpus + new V20 regression tests;
2. full 2840-row rebuild;
3. machine accounting gate;
4. direct Step-09 contradiction gate;
5. collision hard gate = zero;
6. unresolved hard gate = zero likely-false unresolved;
7. inspect bot-generated HEAD;
8. repeat manual semantic QA across all 73+ final clusters and every remaining SEARCH_REQUIRED row;
9. only if manual semantic QA truly passes, write STEP_10_RECONCILIATION.md and formal acceptance;
10. only after formal Step-10 acceptance may Step 11 pre-step work begin.
```

## 10. Current canonical stop state

```text
LATEST_GENERATED_CANDIDATE = V19
LATEST_GENERATED_CANDIDATE_COMMIT = f62932ebe80de18a8ee39113a3080faaf7ecde81
LATEST_SUCCESSFUL_WORKFLOW_RUN = 33286539033
MACHINE_QA = PASS
DIRECT_SERP_CONTRADICTION_GATE = PASS
COLLISION_HARD_GATE = PASS
UNRESOLVED_HARD_GATE = PASS
MANUAL_SEMANTIC_QA = FAIL
NEXT_ITERATION = V20
PAID_PROVIDER_REQUESTS_NEEDED_NOW = no
STEP10_ACCEPTED = false
STEP11_BLOCKED = true
```

## 11. Links

- V19 generated candidate: https://github.com/MaksimUnimax/Yandex_direct/commit/f62932ebe80de18a8ee39113a3080faaf7ecde81
- Successful V19 workflow run: https://github.com/MaksimUnimax/Yandex_direct/actions/runs/33286539033
- V19 classifier: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V19.py
- V19 collision hard gate: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_SEMANTIC_COLLISION_AUDIT_V19.py
- V19 unresolved hard gate: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT_V19.py
- Current QA: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_QA.json
- Current cluster summary: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_CLUSTER_SUMMARY.tsv
- Current semantic QA sample: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_SEMANTIC_QA_SAMPLE.tsv

## Checkpoint marker

```text
KW001_OKNO_STEP10_2026_08_30_CHECKPOINT = UPDATED_AFTER_V19_FULL_PASS_AND_MANUAL_QA_FAIL
SUBSTANTIVE_PROGRESS_ESTIMATE = 85_TO_90_PERCENT
RESUME_FROM = V20_MANUAL_QA_FAILURE_CLASSES
STEP10_ACCEPTED = false
STEP11_BLOCKED = true
OWNER_REQUESTED_STOP = true
```
