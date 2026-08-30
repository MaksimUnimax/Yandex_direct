# KW-001 / OKNO-MSK — STEP 10 PROGRESS CHECKPOINT — 2026-08-30

Status: **ACTIVE / NOT ACCEPTED / V19 SEMANTIC-HARDENING IN PROGRESS**

This checkpoint records the exact live state after resuming Step 10 from the 2026-08-29 checkpoint. It is the required resume point if work stops now.

## 1. Step-10 goal

The canonical Step-10 goal from `STEP_10_USER_TASK_SERP_CLUSTERING_PRE_STEP_REVIEW_2026-08-29.md` is to build an **auditable user-task / SERP clustering layer** that determines:

```text
which phrases express the same or materially compatible user task;
which phrases can reasonably live in one query cluster;
which phrases must stay separate because intent/result type/task differs;
which rows are semantically compatible but lack direct SERP support;
which material boundaries still require additional ordinary Search evidence;
which rows are outside active business/search clustering scope.
```

Step 10 must NOT decide page ownership, structural keep/merge/split/create actions, cannibalization, Search architecture freeze, or AI-search cases. Those belong to later roadmap stages.

## 2. Current progress assessment

### Substantive implementation progress

**Estimated: ~85% complete.**

Reason for estimate:

```text
input accounting and preserved states                  = complete
base user-task clustering pipeline                     = complete
Step-09 direct-evidence consumption                    = complete
no-evidence-transfer accounting gate                   = complete
direct service/product contradiction gate              = complete
full 2840-row V18 candidate rebuild                    = complete
V18 collision + unresolved audits generated            = complete
manual/adversarial QA found remaining real classes     = complete enough to define V19 fixes
V19 systemic fixes                                     = in progress
V19 zero-flag hard gates                               = implemented but not yet reached successfully
full post-V19 manual semantic QA                        = not yet complete
formal reconciliation / acceptance                     = not yet written
```

### Formal acceptance progress

**STEP10_ACCEPTED = false.**

A percentage cannot substitute for the PASS gate. Even though most of the pipeline exists, Step 10 is still formally incomplete until the final candidate passes regression, machine accounting, direct-evidence gate, zero-flag adversarial gates, and manual semantic QA.

## 3. What was completed after the 2026-08-29 checkpoint

### V18 — replacement/action precedence

Starting regression from the prior checkpoint:

```text
замена балконного блока на французское окно
expected = WINDOW_REPLACEMENT_SERVICE
```

V18 added an explicit whole-window / balcony-block replacement precedence before the V17 French-window product guard.

The first V18 run caught another important boundary:

```text
ремонт и замена пластиковых окон
```

This is intentionally mixed rather than a pure replacement-service task, so V18 was corrected to preserve it unresolved.

After that correction, V18 successfully passed:

```text
full inherited self-test corpus
2840-row rebuild
machine accounting gate
direct Step-09 service/product contradiction gate
V15 semantic collision audit generation
V15 unresolved-state adversarial audit generation
bot commit of generated candidate artifacts
```

V18 generated candidate commit:

```text
756c07f8f2a423a084633a6ad781c1f523eb2b83
message = step10: rebuild clusters after V18 replacement-action precedence
```

### V18 machine-QA candidate state

```text
total phrase keys = 2840
active Search-stage rows = 2332
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
cluster_count = 72
SEARCH_REQUIRED = 76
MIXED_OR_BOUNDARY_REVIEW = 2
SEMANTIC_SUPPORTED_NO_DIRECT_SERP = 2191
SERP_SUPPORTED = 63
75 Step-09 probes consumed = 66 exact + 9 controls
8 duplicate comparisons consumed
DUP0004 auto merge = false
unprobed rows claiming direct SERP = 0
silent drops = 0
page ownership decisions = 0
structural action decisions = 0
cannibalization decisions = 0
provider requests = 0
```

Machine status remained correctly:

```text
MACHINE_QA_PASS__MANUAL_SEMANTIC_QA_REQUIRED
```

## 4. Why V18 was NOT accepted

Manual/adversarial review showed that the V15 audits were only **generated**, not enforced as zero-flag gates.

V18 collision audit:

```text
active rows scanned = 2332
flagged rows = 53
flagged records = 53
```

V18 unresolved audit:

```text
SEARCH_REQUIRED rows scanned = 76
flagged rows = 6
flagged records = 6
```

Therefore a green V18 workflow meant only that the audit scripts executed successfully, not that there were no open semantic problems.

This process weakness was corrected in V19: collision and unresolved audits are now intended to be **hard zero-flag workflow gates**.

## 5. What the 53 + 6 audit flags actually meant

They were manually reviewed as a mix of:

```text
A. real classifier errors;
B. stale / over-broad lexical audit false positives;
C. intentionally valid boundary states.
```

Important real error classes identified:

```text
ready-made product + dimensions incorrectly classified as dimension information;
mosquito-net product + size incorrectly classified as window dimensions;
window-cleaning phrases swallowed by repair service because word 'ремонт' appeared as context;
repair compounds/materials swallowed by repair-service cluster;
generic private-house fallback swallowing panoramic/French window family;
private-house shapes/types treated as generic purchase rather than selection/info;
clear French-window product/configuration phrases left SEARCH_REQUIRED;
non-panoramic roof/skylight demand hidden in generic private-house family.
```

Examples:

```text
готовое пластиковое окно двухстворчатое 1000x1200 rehau
готовые окна rehau blitz 1200x1000
москитная сетка на пластиковые окна rehau 133х45
жидкий пластик для ремонта пластиковых окон
средство для ремонта пластиковых окон
чем отмыть пластиковые окна после ремонта
чем очистить пластиковые окна после ремонта
панорамные окна в частном доме
панорамные окна для частного дома
французские окна в частном доме
формы окон для частных домов
французские окна в пол
французские окна на лоджию
французские окна на террасе
французское окно раздвижное
французское окно с дверью
```

Many inherited audit flags were also false positives due incomplete lexical markers, for example valid forms such as:

```text
кв с панорамными окнами
одноэтажный с панорамными окнами
пристройка с панорамными окнами
сколько стоит панорамное окно
панорамное окно в пол
раздвижные панорамные окна
створки панорамного окна
уплотнитель для пластиковой двери
```

V19 collision audit therefore contains explicit adjudication of these known false-positive classes instead of blindly suppressing all flags.

## 6. V19 work already saved in GitHub

Saved files:

```text
STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V19.py
STEP_10_SEMANTIC_COLLISION_AUDIT_V19.py
STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT_V19.py
.github/workflows/kw001-okno-step10-user-task-clustering.yml
```

V19 introduces:

```text
specific task precedence corrections;
ready-made product > generic dimension-info where size is only configuration;
mosquito accessory > numeric size;
cleaning/care > incidental repair-context token;
repair material/product > repair-service;
object-specific glazing > material/private-house/panoramic overlays;
specific panoramic/French family > generic private-house fallback;
private-house forms/types > selection/info;
clear French product/configuration resolution;
new non-panoramic roof/skylight outside-core task;
V19 collision audit as hard failure when flags remain;
V19 unresolved audit as hard failure when likely-false SEARCH_REQUIRED rows remain.
```

## 7. Current live HEAD and exact current failure

Current live branch HEAD at checkpoint creation time:

```text
79266669e98b39ac2a5bddc3d663c6c8918262d6
message = step10: restore object-glazing precedence in V19
```

Latest workflow run:

```text
run = 33286302475
job = 99189976870
conclusion = FAILURE
failure stage = Build conservative Step10 user-task clusters / self-test
```

Exact failing inherited regression:

```text
phrase = панорамное окно на крыше
expected = PANORAMIC_WINDOWS_COMMERCIAL
actual = ROOF_WINDOWS_COMMERCIAL
```

This failure happened **before runner.main()**, therefore no V19 generated candidate artifacts were committed.

The latest generated candidate remains V18 commit `756c07f8...`.

## 8. Why work appears to be looping

The loop is not caused by repeated execution of the same broken run. It is a sequence of **precedence regressions** exposed by a deliberately growing self-test corpus.

The classifier is layered because Russian commercial window queries combine multiple simultaneously valid signals:

```text
object (window / door / balcony / veranda / roof)
action (buy / repair / replace / install / clean)
product type (PVC / aluminium / Rehau / panoramic / French)
context (private house / apartment / balcony)
information modifier (size / type / review / requirements)
```

A rule that fixes one class can accidentally outrank a more specific older class. The self-test corpus is stopping those regressions before the 2840-row candidate is rewritten.

Recent examples:

```text
French product guard fixed apartment-context leakage
-> then swallowed explicit replacement action

replacement fix
-> then swallowed mixed repair+replacement boundary

panoramic/private-house specificity fix
-> then swallowed veranda-glazing action

roof/skylight separation
-> then swallowed protected panoramic-roof configuration
```

So the current bottleneck is **classifier precedence stabilization**, not data collection, Wordstat, Search API, provider cost, or GitHub mechanics.

## 9. Exact resume action

Do NOT move to Step 11.

Start from current V19 and correct the roof rule so:

```text
панорамное окно на крыше
-> PANORAMIC_WINDOWS_COMMERCIAL
```

while still allowing a distinct outside-core roof/skylight task for unambiguous non-panoramic cases such as:

```text
окна для крыши частных домов
мансардные окна
```

The systemic rule should be:

```text
SPECIFIC_PANORAMIC_OR_FRENCH_WINDOW_FAMILY
> generic roof/location modifier

but

NON_PANORAMIC_ROOF_OR_SKYLIGHT_HEAD_OBJECT
-> ROOF_WINDOWS_COMMERCIAL
```

Then:

```text
1. rerun full inherited V15/V16/V17/V18/V19 self-test corpus;
2. fix any further real precedence regression without deleting/weakening tests;
3. reach full 2840-row rebuild;
4. pass machine accounting gate;
5. pass direct Step-09 contradiction gate;
6. pass V19 collision hard gate with 0 flags;
7. pass V19 unresolved hard gate with 0 likely-false unresolved flags;
8. inspect bot-generated final HEAD;
9. perform final manual semantic QA across every cluster and historical boundary;
10. only then write STEP_10_RECONCILIATION.md and formal acceptance artifact.
```

## 10. Remaining work to Step-10 PASS

Estimated remaining substantive work: **~15%**, but it is QA-critical work.

Remaining:

```text
stabilize V19 precedence until full self-test passes;
get V19 hard gates to zero;
manual QA final candidate across all cluster families;
adjudicate any remaining SEARCH_REQUIRED as blocking vs genuinely unresolved;
formal reconciliation;
formal Step-10 acceptance;
roadmap/job-flow update.
```

No paid Search/provider acquisition is authorized or currently necessary merely because V19 is failing. Current failures are semantic-classifier issues visible in existing data.

## 11. Formal state

```text
STEP10_EXECUTION_STARTED = true
STEP10_LATEST_GENERATED_CANDIDATE = V18 / 756c07f8f2a423a084633a6ad781c1f523eb2b83
STEP10_LATEST_IMPLEMENTATION_ITERATION = V19
STEP10_CURRENT_HEAD_BEFORE_THIS_CHECKPOINT = 79266669e98b39ac2a5bddc3d663c6c8918262d6
STEP10_V19_SELF_TEST = FAIL
STEP10_V19_FULL_REBUILD = NOT_REACHED
STEP10_V19_COLLISION_HARD_GATE = NOT_REACHED
STEP10_V19_UNRESOLVED_HARD_GATE = NOT_REACHED
STEP10_MANUAL_SEMANTIC_QA = IN_PROGRESS / NOT PASS
STEP10_COMPLETE = false
STEP10_ACCEPTED = false
STEP11_ALLOWED = false
```

## 12. Links

- Current implementation HEAD before checkpoint: https://github.com/MaksimUnimax/Yandex_direct/commit/79266669e98b39ac2a5bddc3d663c6c8918262d6
- Latest successful generated candidate V18: https://github.com/MaksimUnimax/Yandex_direct/commit/756c07f8f2a423a084633a6ad781c1f523eb2b83
- Current failed V19 run: https://github.com/MaksimUnimax/Yandex_direct/actions/runs/33286302475
- V19 classifier: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V19.py
- V19 collision hard gate: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_SEMANTIC_COLLISION_AUDIT_V19.py
- V19 unresolved hard gate: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT_V19.py
- Canonical Step-10 pre-step review: https://github.com/MaksimUnimax/Yandex_direct/blob/roadmap/kwork-productization-2026-08-28/extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_10_USER_TASK_SERP_CLUSTERING_PRE_STEP_REVIEW_2026-08-29.md

## Checkpoint marker

```text
KW001_OKNO_STEP10_2026_08_30_CHECKPOINT = RECORDED
SUBSTANTIVE_PROGRESS_ESTIMATE = 85_PERCENT
RESUME_FROM = V19_PANORAMIC_ROOF_PRECEDENCE_REGRESSION
STEP10_ACCEPTED = false
STEP11_BLOCKED = true
```
