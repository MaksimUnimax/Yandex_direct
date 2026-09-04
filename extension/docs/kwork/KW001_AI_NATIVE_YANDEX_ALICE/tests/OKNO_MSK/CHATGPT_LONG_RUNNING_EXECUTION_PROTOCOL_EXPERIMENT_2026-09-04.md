# STAGE 2 EXECUTION MODE — SINGLE-PASS WORK EXPERIMENT

Date: 2026-09-04
Project: `OKNO_MSK`
Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`
Status: **OWNER-APPROVED SINGLE-PASS WORK EXPERIMENT**

## 1. Purpose

The owner is testing execution of the entire Stage 2 in ChatGPT Work as one coherent end-to-end task.

This file supersedes the previous runtime behavior that divided Stage 2 into mini-steps and divided a mini-step into durable `B###` checkpoint blocks.

The change is execution-only. It MUST NOT reduce analytical scope, source coverage, evidence requirements, acceptance criteria, quality, traceability, or the owner’s product requirements.

## 2. Effective execution unit

The execution unit is now:

`ENTIRE_STAGE_2`

Do not execute Stage 2 as `2.0..2.13` workflow units.
Do not create or use `B001/B002/...` runtime checkpoints as execution boundaries.
Do not stop for intermediate Stage-2 reports.
Do not ask for confirmation between internal analytical areas of Stage 2 unless a real authorization blocker exists.

Existing historical mini-step/checkpoint artifacts may be read as provenance or evidence, but they do not control execution and are not a resume protocol.

## 3. Stage 2 quality invariant

Stage 2 must still perform the complete audit defined by the project roadmap, Stage 1 acceptance matrix, owner clarification, and the unified Stage 2 audit contract.

Forbidden shortcuts include:

- treating file counts, row counts, request counts, SHA values, or the mere fact of an AI call as analytical results;
- auditing only the client-facing files instead of the full old research chain;
- replacing raw evidence with unsupported summaries;
- skipping contradictory, inconvenient, or negative evidence;
- assuming planned work was actually performed without verifying saved evidence;
- treating an AI response as valuable unless its effect on a decision is demonstrated;
- rewriting presentation while hiding a defect in the underlying analysis;
- omitting positive findings where the existing site/research decision is already correct.

Core analytical chain:

`question -> input -> actual work -> evidence -> conclusion -> decision -> downstream effect -> gap or positive finding -> rework or repackage decision`

Core AI-native rule:

`AI_NATIVE_VALUE != FACT_OF_AI_REQUESTS`

For AI-related findings, establish where possible:

`search-only decision -> reason for AI check -> preserved AI evidence -> comparison -> changed / confirmed / no_change / uncertainty -> effect on semantics/pages/content/priorities -> client-visible implication`

## 4. Source and authority order

Before executing Stage 2, read the current repository state rather than reconstructing old chat history.

At minimum use:

1. `EXECUTION_CURSOR.json`
2. `RESEARCH_REPORT_REBUILD_CURRENT_STATE_2026-09-04.json`
3. `RESEARCH_REPORT_REBUILD_ROADMAP_2026-09-04.md`
4. `RESEARCH_REBUILD_STAGE_01_PRODUCT_PROMISE_AND_ACCEPTANCE_MATRIX_2026-09-04.md`
5. `RESEARCH_REPORT_REBUILD_OWNER_CLARIFICATION_AI_IMPLEMENTATION_PATH_2026-09-04.md`
6. `RESEARCH_REBUILD_STAGE_02_FULL_AUDIT_CONTRACT_2026-09-04.md`
7. `RESEARCH_REPORT_REBUILD_EXECUTION_LOG_2026-09-04.md`
8. the actual preserved old research artifacts and raw evidence needed to audit the chain.

The project roadmap and Stage 1 acceptance matrix define what Stage 2 must prove. Historical mini-step/runtime-checkpoint files are secondary provenance only and MUST NOT control execution.

## 5. Persistence rule for this Work experiment

Do not persist Stage 2 as a sequence of mandatory analytical blocks or mini-step artifacts.

Work through the complete Stage 2 analysis coherently, then materialize the complete Stage 2 result in GitHub.

Required completion sequence:

`complete full Stage 2 audit -> write final Stage 2 artifact(s) -> update execution log -> update current state -> update execution cursor -> save to GitHub -> read back saved result/state -> report to owner in chat`

Supporting artifacts may be created when they materially improve auditability, but they MUST NOT recreate a mandatory mini-step/checkpoint workflow.

## 6. External data boundary

Stage 2 is primarily an audit of work and evidence already preserved in the repository.

No new paid/provider/external data calls are authorized by this execution-mode change.

If existing evidence is insufficient, record exactly:

- what evidence is missing;
- why it matters;
- which conclusion depends on it;
- whether later re-analysis would require a new external/provider call.

Do not silently obtain paid/provider data without separate authorization.

## 7. Stage 2 completion gate

Stage 2 is complete only when the full end-to-end audit has been performed and the final result demonstrates, against `PP-01..PP-19` where applicable:

- what was actually done in the old research;
- what evidence supports it;
- which conclusions and decisions were justified;
- which were weak, missing, contradictory, over-compressed, or unsupported;
- what propagated correctly to later work and what was lost;
- where the analysis itself must be reopened versus where only packaging/explanation must be rebuilt;
- what was already correct and should remain unchanged;
- what the AI-search layer genuinely changed, confirmed, failed to prove, or left uncertain;
- what concrete input Stage 2 hands to Stage 3 and later rebuild stages.

The final Stage 2 artifact must be readable as one coherent audit, not as disconnected service notes.

## 8. Owner-facing stop

After Stage 2 is fully saved and GitHub readback passes, STOP.

Do not start Stage 3 automatically.

Return a chat report containing:

- what Stage 2 audited;
- the most important findings;
- what was correct and retained;
- what is defective/unproven/missing;
- which items require re-analysis versus repackaging;
- the AI-native findings;
- created/updated artifact paths;
- commit/readback status;
- provider-call/cost status;
- exact status of Stage 2 and the next roadmap stage.

## 9. Effective operating rule

`STAGE_2_EXECUTION = ONE_COHERENT_END_TO_END_WORK_RUN`

`NO_MANDATORY_MINI_STEPS`

`NO_MANDATORY_B###_CHECKPOINT_BLOCKS`

`NO_INTERMEDIATE_OWNER_REPORTS`

`FULL_ANALYTICAL_SCOPE_AND_QUALITY_REQUIREMENTS_REMAIN`

`AFTER_STAGE_2_SAVE_AND_READBACK = STOP_AND_REPORT`
