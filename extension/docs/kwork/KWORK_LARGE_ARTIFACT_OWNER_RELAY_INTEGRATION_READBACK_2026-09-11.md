# KWORK — LARGE ARTIFACT OWNER-RELAY RULE — INTEGRATION READBACK

Date: 2026-09-11  
Status: **PASS / UNIVERSAL RULE INTEGRATED**

## Universal authority

`KWORK_LARGE_ARTIFACT_OWNER_RELAY_AND_PUBLICATION_RULE.md`

The rule is active for:

```text
KW-001
KW-002
MK01–MK07
future mini-kworks in the same series
Work executions that generate material/large artifacts
```

## Integrated entry points

### KW-001

`KW001_AI_NATIVE_YANDEX_ALICE/RULES_ARCHITECTURE.md`

Verified:

```text
cross-Kwork publication authority referenced = yes
owner-relay recognized as approved transport = yes
native Git vs owner-relay transport decision = present
large artifact model-byte transport forbidden by default = yes
remote readback remains mandatory = yes
Git auth failure does not require artifact recomputation = yes
```

### KW-002 common Level 1

`KW002_SEMANTIC_CORE_FROM_SCRATCH/LEVEL1/COMMON_RULES.md`

Verified:

```text
cross-Kwork publication authority referenced = yes
mandatory authority read order updated = yes
owner-relay web publication recognized = yes
direct GitHub upload link + downloadable files/ZIP = required when owner relay selected
remote readback after owner upload = required
large artifact model-byte transport forbidden by default = yes
```

### KW-002 Work handoff

`KW002_SEMANTIC_CORE_FROM_SCRATCH/LEVEL1/WORK_HANDOFF_RULE.md`

Verified:

```text
Work prompt must freeze ARTIFACT_PUBLICATION_POLICY = yes
native Git when already authenticated/reliable = yes
owner-relay when more efficient = yes
large file base64/chat/chunk transport forbidden by default = yes
downloadable files / optional transport ZIP = required
direct GitHub upload page = preferred/required when possible
owner credentials must not be pasted into chat = yes
publication states separated from analytical completion = yes
owner relay allowed at semantic checkpoints = yes
remote identity/readback = mandatory
```

### Mini-kwork series

`KW001_AI_NATIVE_YANDEX_ALICE/MINI_KWORKS_PRODUCTIZATION/MINI_KWORK_DEVELOPMENT_PROTOCOL.md`

Verified:

```text
cross-Kwork rule added to mandatory entry gate = yes
Phase-5 Work prompt must freeze publication policy = yes
old Work-self-push-only checkpoint assumption superseded = yes
checkpoint publication = native Git OR owner-relay web upload
owner relay allowed for large TSV/CSV/JSON/XLSX/DOCX/PDF/ZIP and client deliverables = yes
owner relay allowed for intermediate recoverable checkpoints = yes
model-byte transport forbidden by default = yes
remote readback after owner upload = mandatory
```

## Universal failure lesson preserved

```text
COMPLETED LARGE ARTIFACT
+ GIT AUTH / NETWORK PUBLICATION BLOCKER
MUST NOT CAUSE
RECOMPUTATION
OR
LLM / BASE64 / CHUNK BYTE TRANSPORT
```

Correct route:

```text
LOCAL GENERATION + QA
→ NATIVE AUTHENTICATED GIT IF ALREADY RELIABLE
OR
→ DOWNLOADABLE FILES / TRANSPORT ZIP
→ DIRECT GITHUB UPLOAD PAGE
→ OWNER WEB UPLOAD
→ REMOTE READBACK + IDENTITY QA
```

## Universality audit

The permanent rule itself contains no client/domain-specific IDs, current job counts, current job SHA values, concrete query/cluster/action IDs or test-case paths as method requirements.

```text
PERMANENT_RULE_UNIVERSALITY_AUDIT = PASS
JOB_SPECIFIC_BINDINGS_IN_UNIVERSAL_RULE = 0
```

The successful concrete publication incident remains historical/job evidence; only its reusable transport lesson was promoted.

## Final state

```text
GLOBAL_RULE_CREATED = PASS
KW001_INTEGRATION = PASS
KW002_COMMON_INTEGRATION = PASS
KW002_WORK_HANDOFF_INTEGRATION = PASS
MINI_KWORK_SERIES_INTEGRATION = PASS
REMOTE_CONTENT_READBACK = PASS
```
