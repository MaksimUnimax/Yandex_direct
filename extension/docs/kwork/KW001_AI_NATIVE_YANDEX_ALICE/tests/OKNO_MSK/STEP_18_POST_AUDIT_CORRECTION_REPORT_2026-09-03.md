# OKNO_MSK — STEP 18 POST-EXTERNAL-AUDIT CORRECTION

Date: 2026-09-03  
Step: 18 — Prioritization + implementation readiness  
Status at write time: **ANALYTICAL PRIORITY PASS / IMPLEMENTATION-READINESS GOVERNANCE PASS / FINAL SCHEDULE PENDING REAL CALIBRATION / FINAL READBACK PENDING**

## 1. Why Step18 was reopened after its first PASS

The first Step18 execution correctly produced a complete evidence-backed analytical priority register, but the owner-requested external audit found that the result was reported too strongly as a ready implementation order.

The actual first-pass result was:

```text
IDEAL_ANALYTICAL_PRIORITY = COMPLETE
FINAL_IMPLEMENTATION_SCHEDULE = NOT PROVEN
```

The distinction matters because the current job does not contain real implementation-team evidence for:

```text
execution owner
implementation effort
available capacity/calendar
actual sprint/deployment constraints
private client business priority where it would alter scheduling
```

Those values were correctly not guessed, but the old process did not make their absence mechanically block the implementation-schedule claim.

## 2. External method findings used for the correction

The external post-run audit compared Step18 against current prioritization/roadmap practice, including:

- Search Engine Land — SEO backlog to roadmap / SCOPE: ownership, impact, effort, elapsed time, sequencing and measurement are required to turn recommendations into a real roadmap;
- Aleyda Solis — separate ideal SEO priority from expected priority after real implementation difficulty/resources are considered;
- Semrush SEO Roadmap — goals, impact, effort and dependencies;
- Ahrefs SEO Roadmap — impact/effort, workable task granularity and reprioritization;
- Intercom RICE — confidence is distinct from impact and effort; dependencies can legitimately override raw score order;
- Aleyda Solis AI-search prioritization — traffic/citation/business value are separate and must be adapted to actual business evidence.

These sources do not create a mandatory universal numeric formula. They support the corrected separation of analytical importance from implementation readiness.

Canonical permanent method after the owner-authorized correction:

`STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md`

## 3. What remains valid from the original Step18

The original 34-row action register remains valid as the job's **ideal analytical priority layer**:

```text
P1_HIGH = 12
P2_MEDIUM = 20
P3_LATER = 1
HOLD = 1
```

The single P3 row is an accounting batch representing 46 accepted routing units.  
The single HOLD row is an accounting batch representing 20 exact unresolved units.

The original accounting remains preserved:

```text
STRUCTURAL UNITS = 168/168
STEP14A MATERIAL DELTAS = 21/21
STEP14 LINK ROWS = 58/58
STEP14 IMPLEMENT LINKS = 15/15
STEP17 CASES = 8/8
STEP17 CONTENT CANDIDATES = 3/3
PRESERVED UNRESOLVED PHRASES = 19/19
SILENT DROPS = 0
DUPLICATE CANONICAL ACTIONS = 0
```

No architecture decision is changed by this correction.

## 4. Error 1 corrected — analytical priority is not an implementation schedule

Old overstatement:

```text
P1/P2/P3 = ready order of real implementation work
```

Correct interpretation:

```text
P1/P2/P3 = IDEAL_ANALYTICAL_PRIORITY
```

It tells the client/analyst which work is more important under the currently available evidence, dependencies and uncertainty.

It does **not** yet prove which developer/editor/SEO task should enter which sprint or calendar slot.

Hard current-job state:

```text
EXPECTED_IMPLEMENTATION_PRIORITY = PENDING_CALIBRATION
FINAL_IMPLEMENTATION_SCHEDULE_READY = false
```

## 5. Error 2 corrected — UNKNOWN effort now changes the allowed claim

The old action register already preserved implementation effort as `UNKNOWN` where there was no real evidence. That was correct, but incomplete as governance: the report could still look like a final implementation order.

Now:

```text
IMPLEMENTATION_EFFORT = UNKNOWN
-> EXPECTED_IMPLEMENTATION_PRIORITY = PENDING_CALIBRATION
```

The same fail-closed rule applies to missing owner and capacity.

No `LOW/MEDIUM/HIGH effort` was fabricated.

## 6. Error 3 corrected — execution owner/capacity are explicit blockers

A new implementation-calibration artifact defines two profiles.

### Non-HOLD packages

```text
PACKAGE COUNT = 92
EXECUTION OWNER = UNCONFIRMED
EFFORT = UNKNOWN
CAPACITY = UNKNOWN
SCHEDULING = NOT_READY
EXPECTED IMPLEMENTATION PRIORITY = PENDING_CALIBRATION
```

This means the job can truthfully say what should be changed and why, but cannot truthfully assign a final production calendar.

### HOLD packages

```text
PACKAGE COUNT = 20
IMPLEMENTABILITY = BLOCKED_BY_NAMED_UNCERTAINTY
SCHEDULING = BLOCKED
EXPECTED IMPLEMENTATION PRIORITY = NOT_APPLICABLE_UNTIL_BLOCKER_RESOLVED
```

HOLD remains unresolved evidence/policy truth, not low value.

## 7. Error 4 corrected — recheck trigger is not success measurement

The original Step18 had strong HOLD recheck triggers, but implementation work also needs an explicit answer to:

```text
After the change is made, how will we verify that the intended result exists?
```

`STEP_18_MEASUREMENT_PLAN.tsv` now defines seven measurement classes:

```text
M01 OWNER / ROLE CORRECTION
M02 OVERLAP DIFFERENTIATION
M03 CONTENT ENHANCEMENT
M04 BOUNDED AI CONTENT RECHECK
M05 INTERNAL-LINK IMPLEMENTATION
M06 ROUTE TO EXISTING PAGE
M07 HOLD / RECHECK
```

Examples of the corrected distinction:

```text
HOLD recheck trigger
= when missing evidence becomes available

implementation verification
= whether the exact intended page/content/link/route actually exists after the work
```

Optional Webmaster/Metrika/AI evidence may strengthen post-implementation evaluation when later authorized/available, but it is not fabricated and no performance guarantee is made.

## 8. Error 5 corrected — accounting batches were too coarse for execution

The original 34 rows were suitable for analytical accounting but not all were suitable as implementation tasks.

The correction creates:

`STEP_18_WORK_PACKAGE_REGISTER.json`

with **112 exact work packages**:

```text
31 exact action packages
15 exact accepted internal-link packages
46 exact route-to-existing packages
20 exact HOLD/recheck packages
TOTAL = 112
```

Therefore:

```text
SOURCE ACCOUNTING BATCH != ONE IMPLEMENTATION TASK
```

The former 46-unit `S18-A033` routing batch is now 46 separately addressable packages.  
The 15-link `S18-A032` batch is now 15 separately addressable packages.  
The 20-unit `S18-A034` HOLD batch is now 20 separately addressable blocked/recheck packages.

This decomposition does not invent new SEO recommendations. It makes the already accepted recommendations executable/addressable at the correct granularity.

## 9. Public business relevance remains separate from private business impact

The current job can use supported public business relevance such as whether a current page/offer is commercial, informational, service-oriented or a decision-support asset.

It still cannot infer private values such as:

```text
margin
lead value
sales capacity
conversion value
strategic internal growth priority
implementation budget
```

Therefore the final calendar may later change after explicit client business priorities are supplied. That does not invalidate the analytical priority; it calibrates the production order.

## 10. AI boundary remains unchanged

No new AI evidence was acquired and no architecture action was created from the post-run audit.

The bounded Step17 AI content candidates remain supporting evidence only.

```text
AI-ONLY ARCHITECTURE PROMOTIONS = 0
SITEWIDE AI VISIBILITY CLAIM = FORBIDDEN
LONGITUDINAL AI STABILITY CLAIM = FORBIDDEN
```

## 11. Provider / Bridge accounting

This Step18 correction required no new provider evidence.

```text
WORDSTAT = 0
SEARCH = 0
GENSEARCH = 0
WEBMASTER = 0
METRIKA = 0
DIRECT = 0
NEW PAID COST = 0 RUB
```

The Bridge remains conditional-only for Step18: a later provider call would require a named unresolved information-gain need and its own authorization gate.

## 12. Corrected Step18 acceptance meaning

Step18 now has two explicitly different acceptance states.

### Mode A — analytical prioritization

```text
ANALYTICAL PRIORITY = COMPLETE / PASS
```

The job has a complete, traceable, evidence-backed order of importance and named dependencies/uncertainties.

### Mode B — final implementation schedule

```text
IMPLEMENTATION READINESS GOVERNANCE = PASS
FINAL SCHEDULE = PENDING CALIBRATION
```

This is not a failure of analytical work. It is the truthful result when real implementation owner/effort/capacity evidence has not been supplied.

## 13. Step19 handoff after correction

Step19 pre-step remains allowed because the sold/base deliverable can legitimately contain prioritized analytical recommendations.

But Step19 is required to use the corrected language:

```text
P1 / P2 / P3 = ANALYTICAL PRIORITY
```

and must visibly state:

```text
FINAL IMPLEMENTATION SCHEDULE = PENDING CLIENT/IMPLEMENTER CALIBRATION
```

Step19 must not relabel the analytical priority as a committed sprint/calendar plan.

## 14. New/updated Step18 artifacts

New post-audit artifacts:

- `STEP_18_WORK_PACKAGE_REGISTER.json`
- `STEP_18_IMPLEMENTATION_CALIBRATION.json`
- `STEP_18_MEASUREMENT_PLAN.tsv`
- `STEP_18_POST_AUDIT_CORRECTION_QA_2026-09-03.json`
- `STEP_18_POST_AUDIT_CORRECTION_REPORT_2026-09-03.md`

Existing analytical authorities preserved:

- `STEP_18_ACTION_REGISTER.tsv`
- `STEP_18_PRIORITY_SUMMARY.tsv`
- `STEP_18_HOLD_RECHECK_LEDGER.tsv`

Final state/readback artifacts are written after this report and then reread from GitHub.

## ПРОСТЫМИ СЛОВАМИ — ИТОГ

**Где была ошибка:** мы правильно определили, какие изменения важнее, но я слишком рано назвал эту очередь готовым планом внедрения. Для реального рабочего графика недостаточно знать, что важнее: нужно ещё знать, кто будет делать каждую работу, сколько она реально займёт и сколько у команды есть ресурсов.

**Что исправили:** прежние приоритеты не выбросили. Мы оставили их как порядок важности и отдельно разложили крупные пакеты на 112 конкретных работ/проверок. Для каждой категории теперь заранее определено, как проверять результат. Там, где нет реальных данных от исполнителя, прямо записано `неизвестно`, а не придумано `легко` или `быстро`.

**Что теперь реально получили:** Step18 теперь честно даёт две вещи. Первая полностью готова — понятный аналитический приоритет того, что важнее исправлять. Вторая подготовлена, но не сфальсифицирована — основа реального плана внедрения, которую можно окончательно разложить по исполнителям и срокам только после получения реальной оценки трудозатрат и ресурсов. Следующий клиентский материал обязан показывать именно эту разницу.
