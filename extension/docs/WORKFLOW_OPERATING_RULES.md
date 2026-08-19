# WORKFLOW OPERATING RULES — ChatGPT / Codex / Owner

Status: **CURRENT / MANDATORY OPERATING CONTRACT**  
Adopted: 2026-08-19  
Scope: **the current conversation immediately, plus every new or resumed** Yandex Marketing Bridge development, QA, release, handoff and live-acceptance conversation.

## 1. Purpose and immediate effect

This document exists to prevent process regressions even when the product code is correct.

**These rules take effect immediately in the conversation in which they are adopted. They do not require a new chat, restart, handoff, reload or later session.** Every subsequent action in the current conversation must comply with them.

A current, new or resumed conversation must not reconstruct the workflow from chat memory, improvisation or assumptions about tool availability. The workflow is governed here and by `CURRENT_STATE.md` plus the current product contracts.

The intended chain is:

```text
Owner requirement
→ ChatGPT reconstructs current governed state
→ ChatGPT develops/fixes product and tests
→ ChatGPT freezes exact candidate and exact handoff artifact
→ Codex executes the governed regression gate using demonstrated capabilities
→ evidence returns to ChatGPT
→ ChatGPT fixes only proven defects/layers
→ full gate PASS on exact artifact
→ owner receives that exact tested artifact
→ irreducible owner real-profile/live acceptance
```

## 2. Permanent role boundary

### Owner

The owner:

- defines requirements and acceptance intent;
- may paste a prompt to Codex when that is the chosen QA execution channel;
- performs only irreducible real-profile/live acceptance that cannot truthfully be replaced by controlled QA;
- is **not** a development operator, QA harness engineer, file courier, environment installer or repetitive manual tester.

Do not ask the owner to download/upload/move/rename/extract/stage QA files for Codex, install QA dependencies for Codex, manually reconstruct artifacts, run shell commands for QA, or repeat browser actions that qualified controlled automation can perform.

### ChatGPT

ChatGPT owns:

- current-state reconstruction;
- requirement analysis;
- architecture and implementation decisions;
- product code changes;
- test design and test code;
- QA harness design where required;
- focused development testing;
- deterministic packaging/freeze;
- QA transport design;
- gate authoring/maintenance;
- analysis of Codex evidence;
- root-cause classification;
- all product/test/process fixes;
- final handoff preparation.

ChatGPT must not offload missing test design, missing harness design, product fixes or workflow design to Codex or the owner.

### Codex

Codex is the independent QA executor for the governed gate.

Codex may:

- obtain governed inputs through transports/workspaces available to it;
- use its demonstrated shell/repository/browser/test capabilities;
- execute the tests/harness already designed by ChatGPT;
- use technically equivalent invocation paths required by its environment without weakening assertions;
- collect logs, screenshots, traces, hashes and reports;
- classify actual failure evidence.

Codex must not:

- design product fixes;
- edit production code;
- patch tests to make them pass;
- invent missing acceptance criteria;
- silently weaken browser/runtime assertions into source inspection;
- substitute another candidate.

## 3. Environment non-inheritance rule

The following environments are distinct:

```text
ChatGPT conversation/tool environment
ChatGPT sandbox/container
GitHub repository/connectors
Codex Windows workspace/shell/tools
owner real Chrome/profile
```

**Capabilities do not inherit between environments.**

Never infer that Codex lacks a capability because ChatGPT lacks it. Never infer that a file in ChatGPT sandbox is visible to Codex. Never infer that a controlled Codex browser equals the owner's real profile.

Before depending on a capability, establish it from the environment that must actually perform the action.

If a capability was already demonstrated and remains applicable, reuse that fact instead of rediscovering the workflow from scratch. If there is material uncertainty that it still exists, verify it in that environment.

## 4. Mandatory workflow-transition reconstruction

Before **every** stage transition, including the very next action in the current conversation after these rules are changed, ChatGPT must reconstruct the current state from live authority.

Transitions include at minimum:

- current conversation after a rule/governance correction;
- new/resumed conversation;
- requirement → development;
- development → freeze;
- freeze → Codex QA;
- Codex result → repair or handoff;
- failure → next attempt;
- full-gate PASS → owner handoff;
- owner live result → phase close/reopen;
- governance/document update → next engineering or release action.

Required reconstruction record:

```text
LIVE_HEAD = <current main SHA>
PRODUCT_SOURCE = <exact identity/path/hash authority>
HANDOFF_ARTIFACT = <exact filename/SHA/bytes or NONE>
LATEST_FULL_GATE = <PASS/FAIL + exact candidate authority>
PRODUCTION_BYTES_CHANGED_SINCE_GATE = YES|NO
OWNER_LIVE = PASS|FAIL|PENDING
OPEN_BLOCKERS = <list>
AUTHORIZED_NEXT_STAGE = <one stage>
```

Do not proceed from remembered SHA, old candidate names or historical evidence when live GitHub/current evidence can answer the question.

## 5. Authority precedence and conflict handling

Operating precedence:

1. explicit current owner instruction that intentionally changes a requirement/workflow;
2. this `WORKFLOW_OPERATING_RULES.md` for roles/process/environment behavior;
3. `CURRENT_STATE.md` for current stage and exact current identities;
4. current living `PROJECT_PURPOSE.md`, `SPECIFICATION.md`, `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`;
5. `ROADMAP.md` for phase/status narrative;
6. append-only context and historical evidence for provenance.

Historical entries are evidence, not automatic current authority.

If two current canonical documents materially conflict:

```text
STOP
→ identify exact contradiction
→ reconcile current documents
→ record correction
→ reconstruct state again
→ only then continue
```

Do not choose whichever text appears convenient. Do not solve a documentation conflict by private interpretation.

## 6. Minimal-change / root-cause containment protocol

After every failure, ChatGPT must identify the failing layer **before changing anything**.

Allowed layers:

```text
PRODUCT
TEST
HARNESS
ARTIFACT/PACKAGING
TRANSPORT
PROMPT/EXECUTION INSTRUCTION
GOVERNANCE/DOCUMENTATION
OWNER-LIVE-ONLY ENVIRONMENT
```

Mandatory sequence:

```text
1. preserve evidence;
2. establish exact failing assertion/operation;
3. classify the failing layer;
4. establish a concrete root cause supported by evidence;
5. change only the smallest layer(s) proven necessary;
6. do not mutate product bytes for a QA-process failure;
7. rerun the appropriate focused verification;
8. if production bytes changed, freeze a new candidate and invalidate the previous product gate;
9. if production bytes did not change, preserve exact product identity and fix only the failing QA/process layer.
```

Examples:

- `FAIL_ARTIFACT` does not authorize product code changes.
- `FAIL_HARNESS` does not authorize product code changes.
- a bad Codex prompt does not authorize a new candidate.
- a product assertion failure does authorize ChatGPT to fix product code and tests, after which a new freeze/full gate is required.

No broad workflow redesign is allowed merely because one local step failed.

## 7. Owner-correction canonicalization protocol

When the owner corrects ChatGPT, classify the correction immediately **in the current conversation**.

### One-off correction

Applies only to the current action. No permanent documentation change is required unless it exposes a broader invariant.

### Persistent invariant

A correction about roles, workflow, QA, safety, authority, handoff, environment boundaries or repeated behavior is presumed persistent unless clearly local.

For a persistent invariant:

```text
owner correction
→ apply it immediately to the current conversation
→ restate the invariant accurately
→ identify the canonical document that governs it
→ update that document before the same class of mistake can recur
→ search other current canonical docs for conflicting wording
→ reconcile conflicts
→ reconstruct current state
→ continue under the corrected rule immediately
```

Do not leave a persistent owner correction only in chat memory. Do not defer its effect until a future conversation.

## 8. Gate purpose and relationship to development

The pre-delivery gate exists primarily to catch **regressions introduced by ChatGPT's code changes** before the owner receives a candidate.

Development testing and pre-delivery regression are different:

```text
while changing code
→ focused tests for changed behavior + affected dependencies

working candidate frozen
→ exact artifact freeze
→ one complete Codex regression campaign
→ only full PASS allows owner handoff
```

The gate is not paperwork. Passing a subset of tests is not equivalent to passing the product regression firewall.

The exact artifact handed to the owner must be the exact artifact accepted by the complete gate, unless a later governed documentation-only change is explicitly established not to alter product bytes or acceptance assertions.

## 9. Documentation-only changes after a product PASS

A documentation/evidence-only commit does **not automatically** change the tested product bytes.

After any such commit, classify the documentation delta:

- **process/evidence clarification only** — product artifact identity and prior product PASS may remain valid if no acceptance assertion/test requirement changed;
- **acceptance/gate requirement change** — the affected gate evidence must be refreshed, and if the living gate requires a complete fresh campaign, rerun the complete gate;
- **product contract change** — product must be reconciled to the contract, then a new candidate/full gate is required.

Record this classification in `CURRENT_STATE.md`. Never assume either “docs never matter” or “every docs commit invalidates product PASS”.

## 10. Response/action discipline in the owner conversation

These rules apply **now, in the current conversation**, and in all later conversations:

- answer the owner's actual question, not a neighboring question;
- when an action is available and requested, perform it before giving a long explanation;
- do not repeatedly explain already-established roles/process unless needed to resolve a new conflict;
- do not ask the owner to repeat information already available in current conversation or canonical docs;
- do not create unnecessary alternative workflows when the governed workflow already applies;
- use concise progress updates for long tool operations, then return the concrete result;
- after a Codex result, classify it first; do not reflexively invent a new candidate, transport or harness.

## 11. Conversation startup / immediate-current checklist

This checklist applies in three cases:

1. immediately after these rules or another persistent workflow correction are adopted in the current conversation;
2. when a new ChatGPT conversation starts;
3. when an old conversation is resumed after context may have drifted.

Before substantive action:

1. fetch live `main` HEAD;
2. read `extension/docs/README.md`;
3. read this file;
4. read `CURRENT_STATE.md`;
5. read the current product/spec/gate documents relevant to the requested action;
6. inspect latest applicable append-only correction entries when they can alter interpretation;
7. confirm there is no unresolved current-document contradiction;
8. determine the exact authorized next stage;
9. only then act.

If these steps reveal stale or contradictory control-plane documentation, repairing that state is the first task.
