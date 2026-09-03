# KW-001 — RESEARCH TO EXECUTION SCHEMA GATE

Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL / OWNER-DIRECTED / PERMANENT NON-REPEAT CONTROL**

This Layer-A gate prevents a recurring failure mode in which useful external research is completed but the discovered requirements never become executable fields, actions, QA checks or acceptance gates.

Canonical failure class:

```text
RESEARCH_TO_EXECUTION_SCHEMA_GAP
```

Canonical distinctions:

```text
SOURCE_DISCOVERED != REQUIREMENT_OPERATIONALIZED
RESEARCH_STATEMENT != EXECUTION_CONTROL
LIMITATION_DISCLOSED != LIMITATION_GOVERNED
OPTIONAL_ENHANCEMENT != SILENTLY_SKIPPED_SOURCE
QA_OF_EXISTING_ARTIFACTS != QA_OF_REQUIRED_EVIDENCE_COVERAGE
```

## 1. When this gate is mandatory

Run this gate before executing any material roadmap step that uses fresh external methodology research, provider/API research, current-site discovery, owner policy or a newly discovered evidence source that can change the method.

It is especially mandatory when research introduces or changes:

```text
required evidence source
optional enhancement source
provider/API operation
access or credential dependency
sampling rule
query/probe set
current-site freshness requirement
state taxonomy
split/merge or ownership rule
claim boundary
remediation boundary
provider cost/quota boundary
acceptance criterion
```

## 2. Required research-to-execution record

Every material research-derived requirement must be materialized with equivalent fields:

```text
requirement_id
source_authority
source_date_or_freshness
research_statement
execution_scope
execution_mode
requirement_class
required_action_or_collection
required_artifact_field_or_output
availability_or_access_state
provider_or_tool_capability_state
cost_or_quota_boundary
failure_policy
claim_boundary
qa_check
acceptance_check
status
```

Allowed requirement classes include:

```text
BASE_REQUIRED
OPTIONAL_ENHANCEMENT
CONDITIONAL_REQUIRED
FORBIDDEN_CLAIM_BOUNDARY
METHOD_CONTEXT_ONLY
```

A material source may not remain in an ungoverned label such as `ideal`, `nice to have`, `recommended` or `useful` when it can change whether the step is allowed to pass.

## 3. Mandatory conversion sequence

```text
SOURCE
-> RESEARCH STATEMENT
-> REQUIREMENT CLASS
-> CURRENT-JOB SCOPE / MODE
-> ACTION OR COLLECTION PLAN
-> ARTIFACT FIELD / OUTPUT
-> FAILURE POLICY
-> CLAIM BOUNDARY
-> QA CHECK
-> ACCEPTANCE CHECK
```

If any arrow is missing, the requirement is not operationalized.

Forbidden:

```text
SOURCE FOUND
-> NOTE WRITTEN
-> EXECUTION CONTINUES
```

## 4. Evidence-route state model

When a requirement depends on an evidence route, separately classify:

```text
SOURCE_EXISTS
ACCESS_AVAILABLE
PROPERTY_OR_OBJECT_RESOLVED
TOOL_OPERATION_AVAILABLE
PROVIDER_READY
QUOTA_OR_COST_ACCEPTABLE
COLLECTION_EXECUTED
EVIDENCE_PERSISTED
EVIDENCE_READ_BACK
```

Do not collapse account access, provider readiness, Bridge/tool capability or quota into one generic `unavailable` state.

For private/client evidence, `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` controls whether absence means base mode continues, optional enhancement is skipped explicitly, a conditional step blocks, or an enhanced mode blocks.

Absence of an optional enhancement must still be recorded together with the claims that cannot be made without it.

## 5. Reproducible execution manifest

Before material execution, the current job must preserve a compact execution manifest containing equivalent fields:

```text
step
job
method_authority
research_authorities
current_job_mode
input_universe
required_sources
optional_sources
access_states
tool_capability_states
planned_provider_calls
reuse_existing_evidence
freshness_requirements
claim_boundaries
cost_boundaries
acceptance_requirements
```

The manifest must distinguish:

```text
PLANNED
EXECUTED
REUSED
SKIPPED_BY_POLICY
UNAVAILABLE
NOT_APPLICABLE
```

Planned work must never be written as executed evidence.

## 6. Provider and paid-request trigger rule

Fresh provider/API/Search calls are allowed only when the manifest proves information gain that cannot be satisfied by persisted evidence.

Before a paid, quota-bearing or externally rate-limited request, record:

```text
exact question to resolve
why existing evidence is insufficient
exact operation/query
expected information gain
cost/quota semantics
retry boundary
persistence destination
acceptance use
```

If the request is not needed for the active acceptance gate, do not launch it merely because the provider is available.

## 7. Forward and reverse traceability

Forward trace must answer:

```text
For each material research requirement, where is it executed and checked?
```

Reverse trace must answer:

```text
For each acceptance claim, which requirement, evidence and QA check authorize it?
```

No material final claim may exist without reverse trace to:

```text
requirement_id
+ evidence
+ claim boundary
+ QA result
```

## 8. QA must test missing evidence, not only existing files

Independent QA must ask both whether existing artifacts are internally consistent and whether any required research-derived source/field/check is missing entirely.

Required questions include:

```text
Did every material research source receive a requirement_id?
Did every BASE_REQUIRED requirement receive an executable action/output?
Were OPTIONAL_ENHANCEMENT requirements explicitly classified rather than silently omitted?
Were unavailable evidence routes given a failure policy and claim boundary?
Did any planned provider call get represented as executed without a receipt?
Did any accepted claim exceed the evidence mode?
Did the acceptance gate inspect required-but-absent evidence?
Was the final execution manifest persisted and read back?
```

## 9. Pass gate

A step cannot pass this gate unless:

```text
MATERIAL_RESEARCH_REQUIREMENTS_ACCOUNTED = 100%
BASE_REQUIRED_UNOPERATIONALIZED = 0
OPTIONAL_ENHANCEMENT_SILENTLY_SKIPPED = 0
REQUIRED_ARTIFACT_FIELD_MISSING = 0
CLAIM_BOUNDARY_MISSING_FOR_UNAVAILABLE_OPTIONAL_EVIDENCE = 0
PLANNED_AS_EXECUTED_FALSE_POSITIVES = 0
PROVIDER_CALL_WITHOUT_INFORMATION_GAIN_JUSTIFICATION = 0
REVERSE_TRACE_MISSING_FOR_ACCEPTED_CLAIM = 0
INDEPENDENT_QA_BLOCKING_FINDINGS = 0
FINAL_GITHUB_READBACK = PASS
```

If a material requirement cannot be operationalized, the step must be blocked, degraded or switched to a separately defined base/enhanced mode according to current owner-approved policy. It must not silently pass.

## 10. Founding failure lesson

A prior controlled execution discovered an official first-party evidence source during method research and described it as “ideal evidence,” but did not convert that finding into an execution mode, access state, artifact requirement, claim boundary and acceptance check before continuing with public evidence.

### Root cause

```text
SOURCE DISCOVERY
WAS TREATED AS
ENOUGH METHOD INTEGRATION
```

The later correction showed that the right question was not whether that private source must always be mandatory. The right question was what role that source has in each declared mode and how its absence changes the allowed claim.

Reusable pattern:

```text
BASE MODE
-> OPTIONAL ENHANCEMENT EXPLICITLY CLASSIFIED
-> BASE STEP MAY PASS WHEN SOLD SCOPE ALLOWS IT
-> CLAIMS REQUIRING THE MISSING SOURCE REMAIN FORBIDDEN

ENHANCED MODE
-> SOURCE MAY BECOME REQUIRED BY SOLD / AUTHORIZED SCOPE
```

Therefore:

```text
EVERY MATERIAL RESEARCH FINDING MUST BECOME AN EXECUTABLE SCHEMA DECISION.
```

Concrete case identity, evidence counts, job mode/results and artifact paths remain Level2.

## 11. Non-repeat markers

```text
KW001_RESEARCH_TO_EXECUTION_SCHEMA_GATE_ACTIVE = true
KW001_RESEARCH_TO_EXECUTION_SCHEMA_GAP_FORBIDDEN = true
KW001_SOURCE_DISCOVERED_NOT_EQUAL_REQUIREMENT_OPERATIONALIZED = true
KW001_MATERIAL_REQUIREMENT_ID_REQUIRED = true
KW001_OPTIONAL_ENHANCEMENT_MUST_BE_EXPLICIT = true
KW001_UNAVAILABLE_OPTIONAL_SOURCE_REQUIRES_CLAIM_BOUNDARY = true
KW001_REPRODUCIBLE_EXECUTION_MANIFEST_REQUIRED = true
KW001_PROVIDER_REQUEST_INFORMATION_GAIN_REQUIRED = true
KW001_FORWARD_AND_REVERSE_TRACEABILITY_REQUIRED = true
KW001_QA_MUST_TEST_REQUIRED_BUT_MISSING_EVIDENCE = true
KW001_FINAL_CLAIM_REQUIRES_REVERSE_TRACE = true
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
