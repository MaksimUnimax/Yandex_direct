# KW-002 / BLOOD & SAND — RULE COMPLIANCE FAILURE INCIDENT — 2026-09-17

Status: **ACTIVE INCIDENT RECORD / ANTI-REGRESSION EVIDENCE**  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`  
Date: 2026-09-17

This file records concrete job-specific failures. Universal mechanisms/controls belong in Level1.

## 1. Incident summary

During Step07 preparation/handoff/acceptance, Main Chat repeatedly violated already-existing owner-locked rules by relying on memory, summaries and technical artifacts instead of reopening and obeying the current live rules in full.

The repeated pattern was:

```text
RULE ALREADY EXISTED
→ MAIN CHAT DID NOT FRESHLY READ IT IN FULL
→ MAIN CHAT PRODUCED AN INCOMPLETE / WRONG PROCESS RESPONSE
→ OWNER POINTED TO THE RULE
→ MAIN CHAT THEN REOPENED / APPLIED IT
```

This was not caused by missing project documentation. The controlling rules already existed.

## 2. Concrete failures in this job

### I-2026-09-17-01 — wrong Work boundary for Step07 preparation

Observed:

Main Chat initially moved the Work boundary forward to actual Step07, instead of recognizing that `STEP07_PREPARATION` itself required full-volume reconciliation across large accepted Step03B/04/05/06 evidence and therefore already triggered `WORK_HANDOFF_RULE.md`.

Required rule:

```text
LARGE DATA
→ HAND OFF THE COMPLETE EXECUTION UNIT TO CHATGPT WORK
```

Corrected behavior:

`STEP07_PREPARATION` was delegated as the complete Work execution unit.

### I-2026-09-17-02 — owner was initially asked to route handoff files manually

Observed:

Main Chat initially gave separate Level2 and job-root GitHub upload targets and expected the owner to place files into multiple final directories.

This violated the owner-relay model.

Corrected permanent control:

```text
ONE HANDOFF UNIT
→ ONE OWNER STAGING TARGET
→ OWNER UPLOADS ALL FILES TOGETHER
→ MAIN CHAT / WORK DOES FINAL REPOSITORY PLACEMENT
→ STAGING CLEANUP
→ REMOTE READBACK
```

The owner is not responsible for NEW/REPLACE routing or directory placement.

### I-2026-09-17-03 — preparation report omitted mandatory clickable external materials

Observed:

The Step07 methodology-audit artifact contained the external materials used during preparation, but Main Chat's owner-facing report did not initially show those sources as clickable links with what each source supported and how it affected the method.

This violated:

`LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`.

Hard distinction now reinforced:

```text
SOURCE LINKS IN ARTIFACT
!=
OWNER-FACING SOURCE DISCLOSURE IN CHAT
```

### I-2026-09-17-04 — plain-language summary omitted / replaced by technical reporting

Observed:

Main Chat returned technical statuses, counts, hashes, filenames and execution-state markers without the mandatory final normal-Russian summary that explains:

```text
WHY
WHAT
RESULT
CAN WE CONTINUE
BLOCKER
NEXT PHYSICAL ACTION
```

This violated the owner-facing plain-language requirement in `COMMON_RULES.md` and `PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`.

### I-2026-09-17-05 — technical preparation acceptance was treated as enough before chat-report compliance was checked

Observed:

The preparation artifacts, publication and return QA could be technically correct while the mandatory owner-facing source disclosure/plain-language report was still incomplete.

Correct distinction:

```text
TECHNICAL_ARTIFACT_PASS
!=
OWNER_FACING_REPORT_PASS
```

Both are required where the step rules require owner-facing reporting.

### I-2026-09-17-06 — assistant explained consequences before reopening the exact live rule

Observed:

When the owner pointed out the Work/source-disclosure/reporting failures, Main Chat initially explained from memory instead of immediately fetching the controlling live rule and applying it.

Correct response order:

```text
OWNER POINTS TO RULE FAILURE
→ FETCH CURRENT LIVE RULE
→ READ IN FULL
→ APPLY THE RULE
→ THEN EXPLAIN
```

### I-2026-09-17-07 — first anti-regression patch briefly contaminated Level1 with a Step07-specific example

Observed:

While implementing the new recurring-assistant-failure checklist, Main Chat initially wrote a concrete Step07 incident directly into a Level1 checklist.

Fresh reread of `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md` caught this before final acceptance.

Correction:

- Level1 checklist now contains only universal mechanisms;
- this file contains the concrete Step07 incident history.

This incident demonstrates why the new full-rule reread gate must apply to rule edits themselves.

## 3. Root cause

The common root cause across the incidents above is:

```text
MAIN CHAT TREATED REMEMBERED PROJECT CONTEXT AS SUFFICIENT RULE AUTHORITY
```

instead of:

```text
FETCH LIVE AUTHORITY
→ READ APPLICABLE RULES IN FULL
→ APPLY THEM BEFORE ACTING
```

The problem was not lack of documentation. It was failure to reread and enforce existing documentation before action.

## 4. Permanent controls added after this incident

New universal Level1 authorities/guards:

- `LEVEL1/00_MANDATORY_FULL_RULE_REREAD_NO_ACTION_GATE.md`;
- `LEVEL1/01_RECURRING_ASSISTANT_RULE_FAILURES_ANTI_REGRESSION_CHECKLIST.md`.

Visible read-first guards were also added at:

- project root;
- Level2 root;
- work root;
- this job root.

These guards make the rule-read requirement visible before entering any major project layer.

## 5. New hard prohibition

For this job and all future KW-002 execution under the universal rule:

```text
NO FRESH FULL RULE REREAD
→ NO MATERIAL ACTION
```

This includes:

```text
no preparation
no planning presented as executable authority
no Work prompt
no Work execution
no Bridge/provider action
no analysis
no file mutation
no QA acceptance
no publication acceptance
no cursor movement
no roadmap advancement
```

## 6. Required rule-read ledger before next material action

Before actual Step07 or any other material action, the executor must explicitly record:

```text
LIVE_REMOTE_HEAD
CURRENT_ACTION
RULES_READ_IN_FULL
JOB_STATE_READ
FAILURE_LEDGER_READ
OWNER_REPORT_GATE_READ
WORK_GATE_READ when applicable
PROVIDER_GATE_READ when applicable
UNRESOLVED_AUTHORITY_CONFLICTS
EXECUTION_ALLOWED
```

## 7. Current job boundary

This incident record does not execute Step07 and does not change semantic evidence.

Current semantic cursor remains:

```text
STEP06 = DURABLE PASS
STEP07_PREPARATION = ACCEPTED
STEP07 = NOT STARTED
STEP08 = NOT STARTED
```

The next material Step07 execution remains blocked until the new full-rule reread/no-action gate and all applicable pre-step chat/source-disclosure requirements have been satisfied for the actual Step07 execution unit.

## 8. Plain-language incident conclusion

The rules were already there, but Main Chat repeatedly acted as if remembering them was enough. That caused the same kind of mistake several times: wrong Work boundary, wrong file-upload instructions, missing source links and missing plain-language reporting. The permanent correction is not another reminder in chat. The repository now forces a fresh full reread before action, and this concrete incident remains in the job history so future sessions can see exactly what went wrong here.
