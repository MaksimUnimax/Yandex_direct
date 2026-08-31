# KW-001 — STEP GOAL, OUTPUT AND ACCOUNTABILITY GATE

Date: 2026-08-29  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / REQUIRED INSIDE EVERY CONCRETE JOB STEP**

This is an owner-approved universal operating rule for KW-001.

It applies to **every concrete step**, whether or not the step uses Yandex Marketing Bridge.

The rule exists to prevent technical activity, research activity, API activity, document activity or analyst activity from replacing the actual business objective of the Kwork and the concrete step.

---

## 1. Goal-first order is mandatory

Before ChatGPT searches external materials, researches a method, prepares provider commands, analyzes data, edits job artifacts or performs any other execution for a new step, ChatGPT must first explain the step to the owner in plain language.

The explanation must contain, in this exact conceptual order:

```text
A. GOAL OF THE WHOLE KWORK
= what the sold KW-001 service is ultimately supposed to deliver to the client.

B. FULL KWORK ROADMAP WITH CURRENT PROGRESS
= one continuous owner-facing roadmap from the first job stage through final delivery, QA/revision and job close, showing the status of every major stage.

C. WORK ALREADY COMPLETED ACROSS THE WHOLE KWORK / JOB
= explicit list of steps/results that are genuinely complete and verified.
Only verified completed work may appear here.

D. WORK STILL REMAINING ACROSS THE WHOLE KWORK / JOB
= explicit ordered list of everything still required from the current point to final client delivery/acceptance.

E. GOAL OF THE CURRENT STEP
= the single concrete result this step is supposed to achieve.

F. WHAT THIS STEP SOLVES
= which uncertainty, missing evidence, decision or production requirement this step closes.

G. REQUIRED OUTPUT OF THE CURRENT STEP
= what concrete artifact/data/decision/evidence must exist at the end for the step to count as complete.
```

This block must be written **before external method research for the step**.

ChatGPT may not jump directly into methodology, provider syntax, SEO terminology, source links or execution before establishing A–G.

If A–G are not stated clearly, the step is not ready for research or execution.

```text
STEP_GOAL_GATE = FAILED
FULL_ROADMAP_GATE = FAILED if the single full roadmap is missing
METHOD_RESEARCH = BLOCKED
EXECUTION = BLOCKED
```

---

## 2. The completed/remaining lists are mandatory status truth

Every step must explicitly show two owner-facing lists:

```text
COMPLETED WORK
= what is already genuinely complete in the Kwork/job.

REMAINING WORK
= what still has to be done before the Kwork/job is finished.
```

Rules:

```text
1. A step/result enters COMPLETED WORK only after its declared output exists and verification passes.
2. Technical success alone does not move an item into COMPLETED WORK.
3. If a previous step is later found incomplete or invalid, it must be removed from COMPLETED WORK and returned to REMAINING WORK / CORRECTION REQUIRED.
4. The lists must be updated after every step.
5. The lists must reflect the whole Kwork/job, not only the current local operation.
6. A future clean-context ChatGPT must be able to understand current progress from these lists without reconstructing progress from commits or API logs.
```

The owner-facing list must use plain language. Internal step IDs may be shown secondarily, but they may not replace a human-readable explanation of what was actually completed.

### 2A. Mandatory single full-roadmap progress view

`COMPLETED WORK` and `REMAINING WORK` are **not sufficient by themselves** and may not be used as a substitute for one continuous roadmap of the whole job.

Before **every major step**, the owner-facing pre-step report must contain one unified roadmap covering the complete job from start to finish.

The roadmap must:

```text
1. include every major stage required to deliver the whole Kwork, not only the current local stage;
2. begin with intake/scope freeze or the first real job stage;
3. continue through all acquisition, analysis, validation, mapping/decision, deliverable, QA, revision/handoff and close stages that belong to the current job flow;
4. show one plain-language description of what each stage does or produces;
5. show the current status of every stage;
6. clearly identify the current active stage;
7. keep completed historical stages visible instead of omitting them after completion;
8. keep future stages visible instead of collapsing them into a generic phrase such as "remaining work";
9. change an earlier stage's status if later evidence invalidates it;
10. be rebuilt from the current authoritative JOB_FLOW / job state, not reconstructed loosely from memory.
```

Canonical owner-facing status vocabulary:

```text
✅ COMPLETE
🟡 CURRENT
⬜ NOT STARTED
⛔ BLOCKED
🔁 CORRECTION / REWORK REQUIRED
```

Equivalent wording is allowed when needed, but the meaning must remain unambiguous.

Preferred owner-facing shape:

```text
| Stage | What this stage does | Status |
|---|---|---|
| ... | ... | ✅ COMPLETE |
| ... | ... | 🟡 CURRENT |
| ... | ... | ⬜ NOT STARTED |
```

The roadmap is a **progress/navigation view**, not the quantitative accounting table.

Therefore:

```text
- detailed row counts, provider request counts, costs, percentages, reconciliation arithmetic and technical bookkeeping remain in the detailed text;
- the roadmap should stay readable and should not be overloaded with those numbers unless a number is necessary to distinguish the actual stage state;
- the roadmap does not replace COMPLETED WORK, REMAINING WORK, quantitative accounting, or the current-step gate;
- those blocks do not replace the roadmap either.
```

A pre-step report that shows only `COMPLETED WORK` plus `REMAINING WORK`, without the single full roadmap, fails this gate even if all underlying facts are technically present elsewhere.

If the full roadmap is missing, fragmented, or does not show the whole path to final delivery:

```text
FULL_ROADMAP_GATE = FAILED
METHOD_RESEARCH = BLOCKED
STEP_AUTHORIZATION = BLOCKED
EXECUTION = BLOCKED
```

After every completed major step, the end-of-step report must show the same full roadmap again with statuses updated to the new truth before the next step may be introduced.

---

## 3. Then research the method

Only after the goal-first, full-roadmap and status-list block is complete may ChatGPT research how to perform the step.

The next owner-facing block must explain:

```text
WHAT SOURCES WERE CHECKED
= direct links/citations to official/current sources and credible external methodology where relevant.

WHAT THE SOURCES SUPPORT
= what is actually established by those materials.

WHAT IS PROJECT-SPECIFIC
= what is a bounded project choice rather than an external standard.

HOW THE STEP WILL BE DONE
= the exact practical procedure for this job.

WHAT WILL NOT BE DONE YET
= decisions or actions intentionally deferred to later steps.

PASS CONDITION
= the evidence required to mark this step complete.
```

Method research must be adversarial: it must check whether ChatGPT's planned approach is wrong or incomplete, not merely search for confirmation.

After this explanation ChatGPT stops and waits for explicit owner authorization before execution.

---

## 4. Every concrete job step must embed this gate

This rule is not satisfied by merely citing this universal document.

Every concrete job step pre-step/review/manifest must itself contain a compact version of:

```text
KWORK_GOAL
KWORK_FULL_ROADMAP
KWORK_COMPLETED_WORK
KWORK_REMAINING_WORK
STEP_GOAL
STEP_SOLVES
STEP_REQUIRED_OUTPUT
METHOD_SOURCES
METHOD_PLAN
STEP_PASS_CONDITION
```

If the step uses YMB, it must additionally embed the YMB interaction/completeness gate required by `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md` and `DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md`.

If the concrete step does not contain the goal/output/status block **or the full roadmap**:

```text
FULL_ROADMAP_GATE = FAILED if roadmap missing
STEP_AUTHORIZATION = BLOCKED
STEP_EXECUTION = BLOCKED
```

---

## 5. Technical activity never substitutes for the step goal

The following are examples of activity, not proof that the step goal was achieved:

```text
API request succeeded
HTTP 200
file created
commit created
source pages opened
keywords viewed
queries executed
batch completed
analysis text written
examples recorded
provider cost recorded
```

The step is complete only when the **required output defined before execution actually exists, is preserved, is verified, and is usable for the next Kwork step**.

For data-collection steps this means the required complete dataset must be saved and verified.

For cleanup steps this means the intended input set must be fully accounted for and quantitative before/after counts must reconcile.

For analysis steps this means every required input has been considered and the required decisions/evidence table exists.

For deliverable steps this means the promised client artifact exists and passes its stated checks.

---

## 6. Mandatory end-of-step report

After execution ChatGPT must report against the goal that was stated **before** the step.

Required report structure:

```text
WHOLE KWORK GOAL
= one short reminder of the final client objective.

UPDATED FULL KWORK ROADMAP
= the same continuous roadmap from job start through final delivery/QA/revision/close with every stage status updated to current truth.

STEP GOAL
= the exact goal stated before execution.

STEP VERDICT
= COMPLETE / INCOMPLETE / FAILED / BLOCKED.

HOW THE GOAL WAS OR WAS NOT ACHIEVED
= factual explanation tied to the required output.

QUANTITATIVE ACCOUNTING
= all material counts applicable to the step.

UPDATED COMPLETED WORK
= full updated list of genuinely completed work across the Kwork/job.

UPDATED REMAINING WORK
= full updated ordered list of work still required across the Kwork/job.
```

Quantitative accounting must be concrete and reconcile the work. Depending on the step it includes, for example:

```text
requested
provider calls attempted
provider calls actually executed
items/results returned
rows expected
rows saved
rows verified
unique rows after exact dedupe
rows excluded
rows retained
rows left for review
queries analyzed
pages analyzed
clusters created
clusters rejected/merged
Search requests executed
AI requests executed
artifacts produced
errors / outcome_unknown
provider cost
```

Do not write vague completion statements such as `everything collected`, `cleanup complete`, `analysis done` or `step passed` without the relevant numbers and verification truth.

If counts do not reconcile, the step is not complete.

Example:

```text
provider returned = 200
saved = 200
verified = 200
=> preservation gate can pass
=> this item may move to COMPLETED WORK
```

but:

```text
provider returned = 200
saved = 10 representative examples
=> preservation gate fails
=> step is INCOMPLETE
=> item stays in REMAINING WORK
=> next step is BLOCKED
```

---

## 7. Mandatory transition decision

Every end-of-step report must end with one explicit state:

```text
NEXT_STEP_ALLOWED = true | false
```

`true` is allowed only if:

```text
step required output exists;
required data/artifacts are preserved;
verification passed;
quantitative accounting reconciles;
full roadmap was updated to current truth;
completed/remaining lists were updated truthfully;
no blocking uncertainty or failure remains.
```

If any of these are false, ChatGPT must stop and correct the current step rather than advance the Kwork.

---

## 8. Plain-language owner communication

The owner-facing explanation must be understandable without SEO-specialist terminology.

Technical terms may be used only when needed, and then ChatGPT must immediately explain what they mean and why they matter to the client result.

The owner should always be able to answer from the report:

```text
What are we ultimately building?
What is the full roadmap from start to final delivery?
Where exactly are we on that roadmap right now?
What have we already actually completed?
What is still left to do?
Why are we doing this exact step now?
What must we have when it finishes?
What did we actually get?
How much did we get/save/remove/analyze?
Can we safely move to the next step?
```

### Mandatory plain-language summary before AND after every step

A detailed analytical report is not enough. For **every concrete step**, ChatGPT must also provide a short summary in ordinary everyday language that a person with no SEO, analytics, API or programming background can understand.

The summary is mandatory in two places:

```text
1. at the END of the pre-step explanation, immediately before execution/authorization;
2. at the END of the end-of-step report, after the detailed evidence and accounting.
```

The pre-step summary must answer:

```text
ЗАЧЕМ НУЖЕН ЭТОТ ШАГ?
= what useful problem this step solves for the client/project.

ЧТО КОНКРЕТНО МЫ БУДЕМ ДЕЛАТЬ?
= the practical work in ordinary words, without internal workflow terminology.

ЧТО МЫ ПОЛУЧИМ В КОНЦЕ?
= the understandable result that will exist when the step is finished.
```

The end-of-step summary must answer:

```text
ЗАЧЕМ МЫ ДЕЛАЛИ ЭТОТ ШАГ?
= one simple reminder of its purpose.

ЧТО МЫ ФАКТИЧЕСКИ СДЕЛАЛИ?
= what work was really performed.

ЧТО ПОЛУЧИЛОСЬ И ЧТО ЭТО ДАЁТ ДАЛЬШЕ?
= the practical result and why it matters for the next work/client result.
```

Hard communication rule:

```text
PLAIN_LANGUAGE_SUMMARY != TECHNICAL_SUMMARY
```

Rules for both summaries:

```text
1. Write for an ordinary person, not an SEO specialist, analyst, developer or API operator.
2. Do not use internal status names, cluster IDs, protocol names, provider terminology, abbreviations or specialist jargon as the explanation itself.
3. If a technical term is genuinely unavoidable, immediately translate it into ordinary language in the same sentence.
4. Never assume the owner should decode terms such as cluster, intent, SERP, ownership, canonical, cannibalization, semantic freeze, provider, route, ledger, batch or similar project vocabulary.
5. Explain the real-world action instead: for example, not “map cluster to owner”, but “decide which existing page should answer this group of similar searches”.
6. Keep detailed numbers, sources, costs, statuses and audit terminology in the detailed report above; the plain-language summary exists for comprehension.
7. The summary does not replace the detailed gate, evidence, QA or roadmap. Both are mandatory.
8. Never finish a step explanation with only technical wording. The last explanation of the step must always make its purpose, practical work and result understandable without specialist knowledge.
```

Preferred pre-step shape:

```text
ПРОСТЫМИ СЛОВАМИ

Зачем нужен этот шаг:
...

Что конкретно будем делать:
...

Что получим в конце:
...
```

Preferred end-of-step shape:

```text
ПРОСТЫМИ СЛОВАМИ — ИТОГ

Зачем делали этот шаг:
...

Что фактически сделали:
...

Что получили и что это даёт дальше:
...
```

Failure condition:

```text
PLAIN_LANGUAGE_SUMMARY_MISSING = true
-> OWNER_COMMUNICATION_GATE = FAILED
-> STEP_TRANSITION = BLOCKED
```

---

## 9. Relationship to YMB completeness rule

This gate applies to **every step**.

When YMB is used, both gates apply simultaneously:

```text
STEP GOAL/OUTPUT/STATUS GATE
+
YMB PER-INTERACTION RESULT-PRESERVATION GATE
```

Therefore a YMB step cannot pass merely because all requests technically succeeded. The complete collected evidence required by the step objective must be saved and verified after each interaction before continuing.

---

## 10. Markers

```text
KW001_GOAL_FIRST_BEFORE_METHOD_RESEARCH_REQUIRED = true
KW001_WHOLE_KWORK_GOAL_RESTATE_EVERY_STEP = true
KW001_FULL_ROADMAP_REQUIRED_EVERY_MAJOR_STEP = true
KW001_FULL_ROADMAP_MUST_COVER_START_TO_FINAL_CLOSE = true
KW001_COMPLETED_REMAINING_LISTS_DO_NOT_REPLACE_FULL_ROADMAP = true
KW001_FULL_ROADMAP_UPDATED_AFTER_EVERY_MAJOR_STEP = true
KW001_MISSING_FULL_ROADMAP_BLOCKS_METHOD_AND_EXECUTION = true
KW001_COMPLETED_WORK_LIST_REQUIRED_EVERY_STEP = true
KW001_REMAINING_WORK_LIST_REQUIRED_EVERY_STEP = true
KW001_COMPLETED_AND_REMAINING_LISTS_UPDATE_AFTER_EVERY_STEP = true
KW001_STEP_GOAL_AND_REQUIRED_OUTPUT_BEFORE_RESEARCH = true
KW001_EVERY_CONCRETE_STEP_MUST_EMBED_GOAL_GATE = true
KW001_QUANTITATIVE_END_OF_STEP_ACCOUNTING_REQUIRED = true
KW001_STEP_COMPLETION_MUST_MATCH_PREDECLARED_OUTPUT = true
KW001_NEXT_STEP_BLOCKED_UNTIL_CURRENT_GOAL_VERIFIED = true
KW001_OWNER_FACING_PLAIN_LANGUAGE_REQUIRED = true
KW001_PRE_STEP_NON_SPECIALIST_SUMMARY_REQUIRED = true
KW001_PRE_STEP_SUMMARY_NUMBERS_STAY_IN_MAIN_TEXT = true
KW001_PLAIN_LANGUAGE_SUMMARY_REQUIRED_BEFORE_AND_AFTER_EVERY_STEP = true
KW001_PLAIN_LANGUAGE_SUMMARY_MUST_STATE_WHY_HOW_RESULT = true
KW001_PLAIN_LANGUAGE_SUMMARY_NO_UNEXPLAINED_JARGON = true
KW001_MISSING_PLAIN_LANGUAGE_SUMMARY_BLOCKS_STEP_TRANSITION = true
```