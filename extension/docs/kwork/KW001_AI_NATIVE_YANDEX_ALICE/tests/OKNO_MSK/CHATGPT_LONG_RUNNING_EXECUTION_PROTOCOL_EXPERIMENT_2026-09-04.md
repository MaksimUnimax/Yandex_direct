# CHATGPT LONG-RUNNING EXECUTION PROTOCOL — EXPERIMENT

Date: 2026-09-04
Project: `OKNO_MSK`
Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`
Status: **EXPERIMENTAL / REVERSIBLE**

## 1. Purpose

This protocol exists because one analytical mini-step may be larger than one ChatGPT conversation. The goal is to preserve completed work online while it is being performed, so a new conversation continues from the last durable analytical point instead of reconstructing and repeating the mini-step.

This protocol changes execution and persistence mechanics only. It does **not** reduce source coverage, evidence requirements, analytical depth, QA requirements, product acceptance criteria, or authorization gates.

Core invariant:

`COMPLETED_ANALYTICAL_WORK_MUST_BECOME_DURABLE_BEFORE_STARTING_TOO_MUCH_NEW_WORK`

A mini-step is allowed to span multiple conversations.

## 2. Quality invariant — no quality reduction for token economy

Forbidden optimizations:

- reading only a convenient subset of required evidence;
- replacing raw evidence with an unverifiable summary;
- skipping contradictory or inconvenient sources;
- closing a mini-step because the chat is near its limit;
- treating a checkpoint as proof that the underlying analysis is correct;
- restarting a completed durable block merely because a new conversation started.

All sources required by the active mini-step remain in scope. Raw evidence stays authoritative in GitHub. A checkpoint stores analytical work and exact source locators; it does not replace the source.

## 3. Execution unit: durable analytical block

A conversation is **not** a unit of work.

A mini-step such as `2.1` is divided into a small number of coherent analytical blocks. A block ends only at a meaningful analytical boundary, for example one completed handoff in the research chain.

Default planning target for a large mini-step: approximately **5–8 durable blocks**. This is not a quota. Use fewer or more only when the analytical structure requires it.

Do **not** checkpoint after every GitHub read or arbitrary time interval. That persistence overhead would consume the session.

Do **not** wait until the entire mini-step is finished. That would expose too much completed work to loss on interruption.

Target cycle:

`coherent source group -> analysis -> meaningful analytical result -> ONE durable checkpoint -> immediately continue inside the same mini-step`

## 4. Online persistence implementation

Use append-only checkpoint files under the job workspace, grouped by mini-step:

`runtime_checkpoints/<mini-step>/B001.md`
`runtime_checkpoints/<mini-step>/B002.md`
`runtime_checkpoints/<mini-step>/B003.md`
`...`

Each completed block is written once as a new file. Do not repeatedly rewrite a growing journal for every block.

Why:

- one checkpoint requires one small GitHub create operation;
- already persisted blocks never need rewriting;
- GitHub commit history provides durable online persistence;
- a chat interruption cannot erase committed blocks;
- recovery can locate the latest block by listing only the small active-mini-step checkpoint directory.

Checkpoint files are runtime/recovery artifacts, not the final client deliverable.

## 5. Required checkpoint completeness

Every durable block must preserve enough information for another conversation to continue and for the later synthesis to audit the reasoning outcome without needing the old chat.

Required fields:

1. `BLOCK_ID`
2. `MINI_STEP`
3. `STATUS = COMPLETE`
4. `SOURCE_SET`
   - repository path;
   - source SHA/blob identity when available;
   - exact row IDs, line ranges, sections, or artifact identifiers where relevant.
5. `QUESTION`
   - what was checked and why it matters.
6. `WHAT_WAS_ACTUALLY_DONE`
7. `OBSERVATIONS`
   - all decision-relevant factual observations from this block.
8. `EVIDENCE`
   - exact source locators for the observations.
9. `INTERPRETATION`
10. `SUPPORTED_CONCLUSIONS`
11. `UNSUPPORTED_OR_NOT_PROVEN`
12. `DECISIONS`
   - accepted, rejected, deferred; with reasons.
13. `DOWNSTREAM_EFFECT`
14. `CONTRADICTIONS`
15. `UNKNOWNS_OR_OPEN_GAPS`
16. `ARTIFACT_CHANGES_ALREADY_MATERIALIZED`
17. `NEXT_EXACT_ACTION`
   - next source/group/range/question.

The checkpoint does not store hidden chain-of-thought. It stores the complete reproducible work product:

`evidence -> interpretation -> conclusion -> decision -> downstream effect`.

## 6. Raw evidence preservation

Do not duplicate whole large source files into checkpoints unless unavoidable.

Preserve source identity as:

`repo_path + SHA/blob + exact locator`.

This keeps checkpoint overhead low while making every material finding reversible to raw evidence.

If the source identity changes, affected checkpoint conclusions are `STALE_PENDING_REVALIDATION` until rechecked.

## 7. Maximum acceptable loss on interruption

At any time, every previously completed durable block must remain recoverable online.

If the conversation terminates unexpectedly, the maximum acceptable loss is only the currently unfinished block.

A new conversation must not redo `B001..B00N` when those blocks are already durable and their source identities remain valid.

## 8. Recovery in a new conversation

Recovery is continuation, not reconstruction of the old chat.

Required startup sequence:

1. Read the small project execution cursor/current active mini-step.
2. List only `runtime_checkpoints/<active-mini-step>/`.
3. Read only the lexicographically latest completed block.
4. Resume from its `NEXT_EXACT_ACTION`.
5. Read older checkpoint blocks only when needed for cross-block synthesis, contradiction resolution, QA, or final mini-step closure.
6. Do not reread the whole execution log, roadmap, old conversations, or already-processed raw sources merely to rediscover progress.

If no checkpoint exists for the active mini-step, start its first planned block.

## 9. Checkpoint overhead control

The checkpoint itself must be compact but complete with respect to decision-relevant analytical state.

Do not paste raw tables or long source text when an exact locator is sufficient.

Do not include:

- repeated roadmap prose;
- generic methodology already frozen elsewhere;
- tool schemas;
- full directory listings;
- full prior checkpoint text;
- narrative status padding.

Checkpoint frequency must be chosen so that:

`expected_rework_if_chat_dies < checkpoint_overhead`

If checkpoints become more expensive than the work they protect, increase block size. If too much completed work is being held only inside the chat, decrease block size.

## 10. Mini-step completion gate

Checkpoint completion is NOT mini-step completion.

Before a mini-step can be closed:

1. required source coverage is complete or every missing source is explicitly labeled and justified;
2. all planned durable blocks are complete;
3. cross-block contradictions are reconciled or explicitly unresolved;
4. important conclusions are traceable back to raw evidence;
5. the mini-step acceptance criteria are satisfied;
6. a final mini-step artifact is materialized in GitHub;
7. GitHub readback passes;
8. the execution cursor/state is advanced to the next mini-step.

Only then is the mini-step `COMPLETE`.

## 11. REQUIRED USER STOP AFTER EVERY COMPLETED MINI-STEP

**This experimental protocol explicitly changes the previous no-stop behavior between Stage 2 mini-steps.**

Durable blocks inside a mini-step do NOT cause a user-facing stop. After a checkpoint, work continues immediately inside the same mini-step.

But after the entire mini-step has passed its completion gate, the assistant MUST STOP and provide the user a completion report before starting the next mini-step.

The report must contain all of the following.

### A. What was done in the completed mini-step

Include:

- objective of the mini-step;
- what sources/areas were actually analyzed;
- main findings;
- what was correct and retained;
- what was defective, missing, contradictory, or unproven;
- what must be repaired/rebuilt/rechecked;
- materialized artifacts;
- commit/readback status;
- cost/provider-call status when relevant.

### B. Full project roadmap

List the **entire roadmap**, not only the current area, with the status of every major stage/step so the owner can always see the whole project position.

Use concise status markers such as:

`COMPLETE / ACTIVE / NOT_STARTED / BLOCKED / CONDITIONAL`.

Do not omit future stages merely because they are not yet active.

### C. Full roadmap of the current stage/step

List **all mini-steps/substeps of the active major stage**, including:

- completed mini-steps;
- the mini-step just completed;
- remaining mini-steps;
- their current statuses;
- the exact next mini-step and its purpose.

For current Stage 2 this means showing `2.0..2.13` every time a Stage 2 mini-step is completed.

### D. Explicit stop

After the report, do not automatically start the next mini-step. Wait for the owner's next instruction.

This owner-facing stop occurs only at **mini-step completion**, not at internal durable-block checkpoints.

## 12. Rules inside a mini-step

Once the owner starts/continues a mini-step:

- do not stop after each source;
- do not stop after each checkpoint;
- do not ask for confirmation between durable blocks unless a genuine authorization/blocker condition exists;
- keep analyzing and persisting blocks until the mini-step completion gate is reached or a real blocker occurs;
- if the current conversation ends, resume in the next conversation from the latest durable block rather than restarting the mini-step.

## 13. Real blockers

Execution may stop before mini-step completion only for a real blocker, including:

- required evidence is unavailable and owner decision is necessary;
- an external/paid/provider action requires authorization not currently granted;
- repository state makes safe continuation impossible;
- a material contradiction cannot be resolved without owner input.

Running low on chat budget is **not** a blocker. Persist the current coherent block if complete, then the next conversation continues.

## 14. Rollback

This protocol is experimental.

Rollback requires:

1. mark this protocol `REJECTED/ROLLED_BACK` or delete the working copy if desired;
2. stop creating new `runtime_checkpoints/` blocks;
3. retain already created checkpoint files only as provenance unless the owner chooses to delete them;
4. restore the previous execution/persistence behavior explicitly chosen by the owner.

Rollback must not alter or discard substantive research findings already validated independently of this protocol.

## 15. Experimental success criteria

After trying this protocol, evaluate:

- how much of a mini-step is completed per conversation;
- how many tokens/tool calls are spent on persistence versus analysis;
- how much work is repeated after a chat interruption;
- whether recovery begins from the correct exact point;
- whether source/evidence completeness is preserved;
- whether the owner-facing mini-step reports remain complete and understandable.

The protocol is successful only if it reduces repeated work and recovery cost **without decreasing analytical quality or source coverage**.

## 16. Current operating rule

Effective immediately for this experiment:

`WITHIN_MINI_STEP = CONTINUE_THROUGH_DURABLE_BLOCKS_WITHOUT_USER_STOP`

`AFTER_MINI_STEP_COMPLETE = STOP_AND_REPORT`

`MINI_STEP_REPORT = WHAT_WAS_DONE + FULL_PROJECT_ROADMAP + FULL_CURRENT_STAGE_ROADMAP`

`NEXT_MINI_STEP_START = ONLY_AFTER_OWNER_INSTRUCTION`
