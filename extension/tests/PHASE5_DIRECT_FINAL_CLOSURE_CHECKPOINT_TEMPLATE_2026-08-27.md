# Phase 5 Direct — final closure checkpoint template

Date prepared: 2026-08-27

Status: **TEMPLATE ONLY / NOT A PASS RECORD / DO NOT USE AS ACCEPTANCE EVIDENCE**

This file is prepared in advance while Yandex production Direct API approval is pending. It must not be renamed or interpreted as a final closure until owner-live and post-merge acceptance both succeed.

## Final authority to preserve

```text
accepted source = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
accepted extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
frozen ZIP SHA-256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
frozen ZIP bytes = 406656
frozen ZIP files = 39
freeze run = 33037955943
freeze artifact id = 9632728199
independent Codex campaign = PHASE5_DIRECT_R2_COMPLETE_APPLICABLE_GATE_RERUN2
independent Codex verdict = PASS
D-00..D-22 = PASS
NOT_RUN_COUNT = 0
PRODUCT_BYTES_POST_TEST = IDENTICAL
```

## Owner-live section — fill only from real non-secret evidence

```text
Direct application production/full API access = <APPROVED>
dedicated Direct OAuth credential = <PASS; NEVER RECORD TOKEN>
Client-Login mode = <BLANK_ORDINARY_ACCOUNT / AGENCY_CLIENT_LOGIN>
Direct Check exactly once = <PASS>
listCampaigns exactly once = <PASS>
listAdGroups = <PASS / NOT_APPLICABLE_EMPTY_ACCOUNT>
getCampaignPerformance = <PASS / NOT_APPLICABLE_NO_REAL_DATA>
write/mutation operations = NONE
blind retries after provider initiation = NONE
owner-live verdict = <PASS>
owner-live evidence file = extension/tests/PHASE5_DIRECT_OWNER_LIVE_PASS_2026-08-27.md
```

Do not fill `PASS` values from expectation. Copy only observed owner-live evidence.

## Integration section — fill after actual merge

```text
live main immediately before integration = <SHA>
final integration branch = <branch>
final integration PR = <number/url>
accepted product tree before merge = edf1c2d3494ebbc53ae778d23be1457eb885b605
main merge commit = <SHA>
main extension/src tree after merge = <must equal edf1c2d3494ebbc53ae778d23be1457eb885b605>
product diff vs 841a1e2... after merge = <EMPTY>
```

If the post-merge product tree differs, this template must remain unclosed and the acceptance process stops.

## Post-merge controlled regression — fill after workflow succeeds

Workflow authority:

```text
.github/workflows/phase5-direct-postmerge-final.yml
```

Observed result:

```text
post-merge run = <RUN_ID>
post-merge job = <JOB_ID>
source suite = <34/34>
packaged suite = <34/34>
source syntax = <33/33>
packaged syntax = <33/33>
source JSON = <2/2>
packaged JSON = <2/2>
credential concurrency regression = <PASS>
browser Direct popup D18 = <PASS>
browser Direct Manual lifecycle = <PASS>
browser Direct addendum = <PASS>
browser prior-phase compatibility = <PASS>
D-00..D-22 = <PASS>
real credentials used = <NO>
real Yandex Direct requests = <0>
real Yandex total requests = <0>
NOT_RUN_COUNT = <0>
PRODUCT_BYTES_POST_TEST = <IDENTICAL>
final marker = <PHASE5_DIRECT_POSTMERGE_FINAL_PASS>
```

## Final documentation closure — fill after post-merge PASS

Required docs-only updates:

```text
extension/docs/CURRENT_STATE.md
extension/docs/ROADMAP.md
```

Required final values:

```text
ACCEPTED_PHASE5_SOURCE = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
ACCEPTED_PHASE5_SRC_TREE = edf1c2d3494ebbc53ae778d23be1457eb885b605
ACCEPTED_PHASE5_ZIP_SHA256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
ACCEPTED_PHASE5_ZIP_BYTES = 406656
ACCEPTED_PHASE5_FREEZE_RUN = 33037955943
ACCEPTED_PHASE5_FREEZE_ARTIFACT_ID = 9632728199
ACCEPTED_PHASE5_CODEX_FINAL = PASS
ACCEPTED_PHASE5_OWNER_LIVE = PASS
ACCEPTED_PHASE5_MAIN_MERGE = <actual SHA>
ACCEPTED_PHASE5_POSTMERGE_RUN = <actual run ID>
ACCEPTED_PHASE5_POSTMERGE = PASS
PHASE5_STATUS = LIVE PASS / CLOSED
```

## Final project-cycle state

Only after every placeholder above has real PASS evidence may the final checkpoint state:

```text
PHASE_1_WORDSTAT = LIVE PASS / CLOSED
PHASE_2_SEARCH = LIVE PASS / CLOSED
LIFECYCLE_BUTTON_PATCH = OWNER LIVE PASS / CLOSED
PHASE_3_WEBMASTER = LIVE PASS / CLOSED
PHASE_4_METRIKA = LIVE PASS / CLOSED
PHASE_5_DIRECT = LIVE PASS / CLOSED
FIRST_PLANNED_FIVE_SERVICE_CYCLE = COMPLETE
```

Deferred/locked surfaces remain locked after closure:

```text
Direct writes = LOCKED
bid mutation = LOCKED
finance/payment = LOCKED
arbitrary provider requests = LOCKED
arbitrary reports = LOCKED
offline report queues/polling = LOCKED
blind automatic retry after provider initiation = LOCKED
```

## Next-stage authority after closure

The current project purpose names exactly five provider services. Therefore completion of Phase 5 does not implicitly authorize a sixth API integration.

After final closure use:

```text
AUTHORIZED_NEXT_STAGE = PRODUCT_RELEASE_DOCUMENTATION_OR_NEW_EXPLICIT_ROADMAP_DECISION
```

A new provider, write capability, broader Direct surface, packaging/release redesign, branding change or distribution stage requires an explicit new decision/contract rather than being smuggled into the Phase-5 closure.
