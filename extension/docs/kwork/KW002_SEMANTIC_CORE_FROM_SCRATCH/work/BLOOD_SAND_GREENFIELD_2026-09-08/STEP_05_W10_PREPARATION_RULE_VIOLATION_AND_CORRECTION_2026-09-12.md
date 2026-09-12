# KW-002 Blood & Sand — Step05 preparation-rule violation and correction

Date: 2026-09-12
Status: **JOB-SPECIFIC EXECUTION-PREPARATION DEFECT RECORDED / V1 HANDOFF NOT AUTHORIZED FOR EXECUTION / CORRECTION IN PROGRESS**

## Incident

Main ChatGPT materially prepared and published the first W10 Step05 prompt/release before presenting the mandatory owner-facing pre-step disclosure in chat in the order required by:

- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`;
- `LEVEL1/WORK_HANDOFF_RULE.md`.

The earlier preparation also lacked an explicit frozen pre-handoff manifest file before the canonical Work prompt was authored.

No Step05 Work execution and no provider call occurred under that premature release.

## Root cause

The preparation treated creation of the Work prompt/release as the beginning of the pre-step process instead of treating the owner-facing pre-step review + source disclosure + pre-handoff manifest as mandatory gates that precede Work execution handoff.

This is not a new universal failure class: the universal prevention rules already exist. This file records the concrete job incident only.

## Existing universal prevention rule

Required order:

```text
CURRENT STEP PRE-STEP REVIEW
→ FRESH EXTERNAL RESEARCH
→ OWNER-FACING CLICKABLE SOURCE DISCLOSURE
→ PLAIN-RUSSIAN WHY/WHAT/RESULT/BLOCKER/NEXT
→ WORK TRIGGER CONFIRMED
→ PRE-HANDOFF MANIFEST FROZEN
→ CANONICAL WORK PROMPT
→ EXECUTION RELEASE
→ OWNER RELAY
→ WORK EXECUTION
→ MAIN RETURN QA
```

The owner-facing disclosure must contain the whole Kwork goal, full roadmap, completed work, remaining work, current-step purpose/problem/output, prior errors, non-repeat controls, fresh research, clickable sources with exact support/limitations, source→method trace, execution plan, Work/Bridge gate, PASS conditions and a plain-language conclusion.

## Additional current-state defect discovered during correction

`JOB_FLOW.md` and `JOB_MANIFEST.md` still contain W08-era current-status text and are stale relative to the accepted W09 Step04 authority and current cursor.

Until reconciled, they MUST NOT be treated as current Step05 execution authority. Current state authority for this handoff is:

1. `KW002_EXECUTION_CURSOR_2026-09-11.json` current V8 state;
2. `STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`;
3. accepted W09 `STEP_04_CURRENT_AUTHORITY_*` artifacts;
4. the corrected Step05 V2 preparation package.

Work must not overwrite `JOB_FLOW.md`, `JOB_MANIFEST.md` or the cursor from a stale local base. Main ChatGPT will reconcile mutable state after the corrected Step05 pre-step gate / Work return using the live remote head.

## V1 disposition

The following first W10 files remain historical preparation evidence but are NOT the execution handoff to relay:

- `STEP_05_W10_PRE_ACQUISITION_WORK_PROMPT_2026-09-12.md`;
- `STEP_05_W10_PRE_ACQUISITION_EXECUTION_RELEASE_2026-09-12.md`;
- `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_2026-09-12.md`.

They are superseded for execution by the corrected V2 package created after this incident review.

## Hard correction gate

```text
V1_WORK_EXECUTION_AUTHORIZED = false
V1_PROVIDER_EXECUTION_AUTHORIZED = false
STEP05_PROVIDER_CALLS_DURING_CORRECTION = 0
STEP06_STARTED = false
OWNER_FACING_PRE_STEP_DISCLOSURE_REQUIRED_BEFORE_RELAY = true
PRE_HANDOFF_MANIFEST_REQUIRED = true
CORRECTED_V2_PROMPT_REQUIRED = true
CORRECTED_V2_RELEASE_REQUIRED = true
```
