# KW-001 — STEP 20 FINAL QA AND RELEASE ASSURANCE METHOD

Updated: 2026-09-05  
Status: **APPROVED / ACTIVE AFTER OWNER-DIRECTED EXTERNAL METHOD AUDIT + CORRECTION**  
Scope: **UNIVERSAL / LEVEL 1 / NO JOB-SPECIFIC VALUES**

This is the canonical reusable method for **Step20 — Final QA / release assurance before handoff**.

It must be read together with the universal cross-step gates, especially:

- `RULES_ARCHITECTURE.md`
- `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`
- `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md`
- `STEP_GOAL_OUTPUT_AND_ACCOUNTABILITY_GATE.md`
- `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`
- `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md` when provider evidence is material.

The current job supplies only the Level2 profile, artifacts, constraints, evidence, risk tier and freshness window. Concrete domains, URLs, counts, file hashes, action IDs, costs and client-specific decisions are forbidden in this Level1 method.

---

## 1. Step purpose

Step20 exists to answer one release question:

> **Can the exact current deliverable revision be handed off for its intended use without materially misleading the recipient, losing analytical truth, relying on stale current-state evidence, or concealing unresolved risk?**

Step20 is not a spell-check pass and not a repetition of the previous step's own QA.

It is an **adversarial release-assurance stage** that must attempt to falsify the final package.

```text
DELIVERABLE EXISTS
!= DELIVERABLE IS INTERNALLY CONSISTENT
!= DELIVERABLE IS CURRENTLY TRUE
!= DELIVERABLE IS FIT FOR INTENDED USE
!= DELIVERABLE IS SAFE TO RELEASE
```

---

### Mandatory assurance dimensions

Global release assurance has three distinct applicable dimensions:

```text
PHYSICAL / DISTRIBUTION QA
+ SEMANTIC / CANONICAL AUTHORITY QA
+ PRODUCT / DELIVERABLE ACCEPTANCE QA
= GLOBAL RELEASE PASS
```

Physical correctness cannot compensate for stale semantic authority. Internal semantic consistency cannot compensate for failure to deliver the promised usable product. Each dimension has its own evidence, tests and blocking verdict.
## 2. Why the first Step20 method was incomplete even after research

The first method review had read good sources and already understood several correct ideas: verification vs validation, current-page freshness, physical-package QA and defect blocking. The failure was **not primarily lack of research**.

The failure was in converting research into executable controls.

### Root cause A — research was read, but not every material requirement became a hard gate

The preparation process correctly summarized external guidance, but the execution schema concentrated on the already-visible risks in the current deliverables. Requirements that were less obvious — structured risk assessment, assurance independence, accessibility, freshness expiry and stronger artifact provenance — remained narrative considerations rather than mandatory outputs.

```text
RESEARCH READ
!= REQUIREMENT OPERATIONALIZED
```

This happened because the method design asked:

> "What do I need to check in this package?"

instead of first asking:

> "What are all the dimensions that a final assurance method must cover before I look at this package?"

The corrected method therefore freezes the assurance dimensions **before** inspecting the deliverable defects.

### Root cause B — Step20 was designed too much as an extension of Step19 QA

The previous deliverable step already had strong reconciliation, readback and physical-file checks. Step20 inherited that shape and became a stronger version of package QA rather than a fully separate assurance lifecycle.

That encouraged confirmation around known structures instead of a clean risk-first design.

```text
MORE QA OF THE SAME KIND
!= INDEPENDENT RELEASE ASSURANCE DESIGN
```

The corrected method starts from intended use and business/reputational risk, then derives the QA plan.

### Root cause C — verification and validation were separated conceptually but not scoped precisely enough

The previous run correctly treated verification and validation as different layers, but analyst-side usability review was allowed to support wording equivalent to `validation complete`.

That was too strong because real-user/commissioner validation had not necessarily occurred.

```text
ANALYST-SIDE INTENDED-USE WALKTHROUGH
!= REAL USER / COMMISSIONER VALIDATION
```

The corrected method has explicit validation states and never collapses them.

### Root cause D — independence was disclosed as a limitation instead of designed as an assurance mode

External assurance guidance says the analyst and assurer should have some separation proportionate to risk. The previous method recognized that the same analyst could not claim formal independent assurance, but it merely disclosed the limitation.

That is insufficient as a reusable method.

The corrected method defines **assurance-independence tiers** before execution and changes the pass boundary according to the risk/use mode.

### Root cause E — current URL/content evidence channels were over-compressed

A public search result, direct page read and real HTTP response do not prove the same thing. The earlier method could treat a search fallback as enough to resolve "existence/role" together.

```text
SEARCH RESULT / CACHED DISCOVERY
!= LIVE HTTP AVAILABILITY
!= CURRENT PAGE CONTENT
!= CURRENT ANALYTICAL ROLE
```

The corrected method records these as separate evidence dimensions.

### Root cause F — freshness was treated as a timestamp, not a lifecycle

A current-site recheck can be perfectly correct and still become stale before handoff. The earlier method recorded freshness but did not require an explicit expiry/recheck condition.

```text
FRESH AT QA TIME
!= FRESH AT DELIVERY TIME
```

The corrected method requires a declared freshness window or event-triggered expiry rule.

### Root cause G — visual/privacy QA was mistaken for complete distribution QA

Openability, clipping, hidden metadata and visual correctness are important, but they do not cover accessibility. Accessibility was omitted because it was not present in the initial acceptance schema.

```text
VISUALLY READABLE
!= ACCESSIBLE TO INTENDED RECIPIENTS
```

The corrected method requires accessibility review proportional to contract/audience risk and an explicit accessible-alternative decision.

### Root cause H — hashes/workflow identity were treated as sufficient provenance

SHA-256 and workflow/run lineage prove useful integrity properties but do not themselves provide signed build provenance. Where distribution risk justifies it, stronger provenance such as an artifact attestation should be generated and verified.

```text
HASH MATCH
!= SIGNED BUILD PROVENANCE
```

The corrected method treats attestation as a risk-proportionate enhancement, not a substitute for content QA.

---

### Root cause I — consistent derivatives were mistaken for independent semantic validation

A release candidate can contain several tables and reports generated from the same stale or partially corrected path. They may agree with each other while all disagree with the current canonical authority.

```text
CONSISTENT BUGGY DERIVATIVES
!= INDEPENDENT SEMANTIC VALIDATION
```

The corrected method requires a complete correction-universe forward audit from the current authority and at least one semantic check whose expected result is derived independently of the potentially defective generation path.
## 3. Direct method sources and what they require

The method was corrected from the following reusable external authorities. Current jobs must still verify that these sources remain applicable when material standards change.

### AQuA Book — UK Government analytical quality assurance

Source: `https://www.gov.uk/guidance/the-aqua-book`

Operationalized requirements:

- all analysis needs assurance;
- assurance should be proportionate to risk and complexity;
- verification and validation are different;
- uncertainty must remain visible;
- the assurer and analyst should have appropriate separation;
- assurance planning belongs throughout the analytical lifecycle, not only at the end;
- risk assessment should guide assurance depth.

### Government Data Quality Framework

Source: `https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework-guidance`

Operationalized data-quality dimensions:

- completeness;
- uniqueness;
- consistency;
- timeliness;
- validity;
- accuracy.

These dimensions must be separate QA questions. Arithmetic reconciliation alone cannot stand in for current-world accuracy.

### Microsoft Document Inspector / hidden data guidance

Source: `https://support.microsoft.com/en-us/office/collab-files/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks`

Operationalized distribution checks include, where applicable:

- comments/revisions;
- hidden content;
- document properties/personal information;
- custom XML;
- external links/connections;
- embedded content/macros;
- headers/footers/watermarks;
- other non-obvious distribution payload.

### Microsoft Accessibility guidance

Sources:

- `https://support.microsoft.com/en-US/Accessibility/office-accessibility/rules-for-the-accessibility-checker`
- `https://support.microsoft.com/en-us/accessibility/office-accessibility/create-accessible-pdfs`
- `https://support.microsoft.com/en-us/accessibility/word/make-your-word-documents-accessible-to-people-with-disabilities`

Operationalized checks include:

- semantic heading structure;
- simple tables with usable header information;
- no color-only meaning where material;
- meaningful link text where applicable;
- alt text for meaningful images where applicable;
- accessible source-document review before PDF generation;
- tagged/structured PDF where accessibility is a contractual or audience requirement;
- an explicit accessible-alternative state if the PDF itself is not fully tagged.

### GitHub artifact attestations

Sources:

- `https://docs.github.com/en/actions/concepts/security/artifact-attestations`
- `https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations`

Operationalized rule:

- hashes and workflow identity remain mandatory integrity/accounting data;
- when artifact provenance risk warrants stronger proof, generate and verify signed provenance for the actual distributable bundle/manifest;
- attestation proves build provenance, **not analytical correctness**.

---

## 4. Mandatory Step20 execution modes

Before QA begins, the current job must declare an intended-use/risk mode.

### Mode A — internal rehearsal / demo / low external consequence

Use when the package is explicitly non-production, internal, test/demo or otherwise cannot reasonably be mistaken for a real consequential delivery.

Required assurance:

- analyst adversarial self-QA;
- independent computational/mechanical verifier where feasible;
- explicit test/demo identity if distributed;
- scenario-based intended-use validation;
- real-user validation may be `NOT_APPLICABLE_TO_REHEARSAL` but must not be called complete.

### Mode B — ordinary external/client-facing delivery

Required assurance:

- analyst self-QA;
- a materially independent reviewer/assurer for high-risk claims or a documented equivalent independent review route;
- recipient-use validation or explicit Step21 commissioner validation boundary;
- accessibility/distribution review suitable for the audience;
- full release ledger and approval boundary.

### Mode C — high-impact / regulated / legally, financially or reputationally material analysis

Required assurance is stronger:

- independent assurer separate from the analyst;
- explicit approver/sign-off role;
- enhanced risk register;
- stronger reproducibility and evidence review;
- accessibility/compliance requirements according to the applicable contract/standard;
- no PASS if mandatory independent assurance is unavailable.

```text
ASSURANCE DEPTH
MUST FOLLOW
INTENDED USE + RISK + COMPLEXITY
```

Do not hard-code one universal risk tier for all jobs.

---

## 5. Phase 0 — risk register BEFORE testing

The Step20 QA plan must be generated from a pre-test risk register, not from defects discovered after testing starts.

For each credible failure mode record:

- failure class;
- affected deliverable/decision type;
- likelihood state;
- impact state;
- evidence needed to detect it;
- assurance technique;
- blocking consequence if found;
- whether independent review is required;
- whether the risk expires/reopens with time or upstream change.

Use qualitative states unless the current job has an evidence-backed quantitative risk model.

Minimum universal failure families:

1. wrong or stale client claim;
2. missing or duplicated records/IDs;
3. cross-artifact inconsistency;
4. invalid/unresolved state silently converted to certainty;
5. implementation action contradicts current site/business truth;
6. destructive/new-page action exceeds evidence;
7. AI/search evidence overgeneralized beyond sampling/time scope;
8. production priority/schedule overstated beyond calibration;
9. implementation-critical URL unavailable or redirected;
10. client file identity/version mismatch;
11. hidden/private/unsafe distribution metadata;
12. inaccessible or misleading presentation;
13. test/demo/client identity ambiguity;
14. stale evidence at delivery time;
15. provenance/reproducibility failure;
16. handoff/revision status claimed before actual handoff.

### Why this phase is first

If severity is assigned only after defects are found, the analyst can unconsciously move the goalposts to fit the result. Pre-registering failure classes and release consequences reduces that confirmation bias.

---

## 6. Phase 1 — freeze the exact release candidate

Before any Step20 test:

1. record branch/ref;
2. record exact commit/HEAD;
3. record logical deliverable versions;
4. record physical artifact names, byte sizes and hashes;
5. record current manifest/provenance;
6. prohibit mixed-revision execution.

```text
QA OF REVISION A
CANNOT AUTHORIZE
DELIVERY OF REVISION B
```

Any material mutation after this freeze invalidates the affected Step20 result and requires a fresh rerun at the necessary scope. If the mutation changes a client-facing action/claim, the default is full Step20 rerun unless the approved method explicitly proves the unaffected subset.

---

## 7. Phase 2 — build complete QA universes mechanically

Never sample by convenience when the exact implementation-critical universe can be derived.

Mechanically build, as applicable:

- all client-visible deliverables;
- all client-visible material claims;
- all semantic/task/page rows promised as complete;
- all actions and priority rows;
- all implementation packages;
- all unresolved/HOLD/recheck states;
- all AI/Search comparison cases;
- all measurement classes;
- all physical client artifacts;
- all implementation-critical URLs;
- all source/target edges that the client is instructed to change.

```text
CLOSED TEST LIST
MUST BE DERIVED FROM CURRENT AUTHORITY
NOT FROM MEMORY
```

---

### Complete correction-universe forward audit

For every final correction ledger or changed authority set, derive the complete governed universe and reconcile:

```text
CORRECTION
-> FINAL CANONICAL MASTER
-> EVERY MATERIAL CLIENT VIEW
-> NARRATIVE CLAIM / ACTION
-> PHYSICAL CLIENT PACKAGE
```

Use current authority to compute the expected result. A sibling derivative produced by the same materializer is not the only allowed semantic oracle.

Required outputs include equivalent fields:

```text
correction_or_mutation_id
affected_entity_key
expected_current_canonical_state
final_master_state
consumer_artifact_and_field
physical_artifact_location
reconciliation_verdict
independent_oracle_source
```

If the correction universe cannot be bounded, reopen the full promised semantic/action universe.
## 8. Phase 3 — verification and six-dimensional data QA

Verification asks whether the release candidate matches its specification and accepted upstream authority.

Run explicit tests for:

### Completeness
Every promised record/state/output is accounted for. Missing-by-design values remain explicitly marked rather than silently dropped.

### Uniqueness
Keys that must be unique are unique. Legitimate repeated entities have a declared reason.

### Consistency
The same action, URL, priority, verdict and limitation do not contradict each other across summary, workbook, report, delivery text and machine authorities.

### Timeliness
Every current-world fact has a collection timestamp and an intended-use freshness state.

### Validity
IDs, enums, URL formats, file identities, state transitions and allowed values satisfy their schema/contracts.

### Accuracy
The current client statement matches current canonical authority and, where the claim concerns current external reality, current direct evidence. Another table generated from the same path cannot be the only proof.

For changed semantic/entity assignments, compare dependent fields with the canonical target-entity contract, not only with the changed ID or a sibling derivative.

```text
CONSISTENT WITH ITSELF
!= ACCURATE AGAINST REALITY
```

---

## 9. Phase 4 — current truth: separate availability, content and analytical role

For every implementation-critical URL, do not compress evidence channels.

Required fields should distinguish:

- requested URL;
- live HTTP availability status when executable;
- redirect/final URL;
- retrieval timestamp;
- current content evidence status;
- observed page identity/title;
- current analytical role verdict;
- source/evidence channel;
- freshness expiry/recheck trigger.

### Evidence rule

```text
SEARCH RESULT / INDEXED DISCOVERY
MAY SUPPORT DISCOVERY OR ROLE EVIDENCE
BUT DOES NOT BY ITSELF PROVE
LIVE HTTP AVAILABILITY
```

If live HTTP status cannot be measured with current tooling, record it as unresolved rather than upgrading a search result into HTTP proof.

Likewise:

```text
HTTP 200
!= CORRECT CURRENT CONTENT
!= CORRECT ANALYTICAL ROLE
```

Current-role QA still requires reading the page/content or an equivalent reliable current source.

---

## 10. Phase 5 — freshness window and expiry/sunset rule

Every current-site/current-offer/current-role evidence set used to authorize handoff must have one of:

- explicit validity window chosen for the current job/risk;
- event-triggered expiry condition;
- both.

Examples of expiry triggers:

- handoff delayed beyond the declared current-evidence window;
- site deploy/content release after QA;
- client reports offer/business change;
- redirects/URL structure change;
- upstream analytical correction;
- a material file rebuild.

Do **not** encode one permanent number of days in Level1. The current job chooses and records the window proportionate to volatility/risk.

```text
TIMESTAMP WITHOUT EXPIRY LOGIC
!= FRESHNESS GOVERNANCE
```

---

## 11. Phase 6 — reverse-trace every material client claim

For each material conclusion or action exposed to the recipient, record:

```text
CLIENT CLAIM
-> CURRENT REQUIREMENT / CONTRACT
-> CURRENT UPSTREAM AUTHORITY
-> DIRECT EVIDENCE
-> LIMITATION / UNCERTAINTY
-> QA TEST
-> RELEASE VERDICT
```

The reverse trace must be able to detect when a claim is internally consistent but stale.

At minimum reverse-trace:

- create/keep/merge/delete/redirect decisions;
- page-owner changes;
- content-gap actions;
- priority/scheduling language;
- AI/generalization claims;
- performance/business impact claims;
- unresolved/HOLD meaning;
- client/demo identity;
- claimed package completeness.

---

## 12. Phase 7 — physical distribution QA

For every distributable file:

### Identity/integrity

- exact filename;
- size;
- SHA-256;
- manifest match;
- workflow/build provenance.

### Openability/render

- open in an appropriate parser/application;
- render and visually inspect every page for final DOCX/PDF delivery;
- inspect key spreadsheet surfaces, not only workbook metadata;
- no clipped text, overlap, broken tables, missing glyphs or unusable widths.

### Hidden/private payload

Inspect where applicable:

- comments;
- tracked changes;
- hidden text/sheets;
- external links/connections;
- embedded files;
- macros;
- custom/document properties;
- personal metadata;
- stale template chronology;
- custom XML/other hidden payload.

### Distribution identity

The file must identify its status correctly: real client, draft, internal, test/demo, confidential, etc., according to the current contract.

```text
CORRECT CONTENT IN WRONG DISTRIBUTION IDENTITY
CAN STILL BE A MATERIAL RELEASE DEFECT
```

---

## 13. Phase 8 — accessibility QA

Accessibility is a release dimension, not a visual nicety.

The current job first declares whether accessibility is:

- CONTRACT_REQUIRED;
- AUDIENCE_MATERIAL;
- BEST_EFFORT_STANDARD;
- NOT_MATERIAL_FOR_THIS INTERNAL/DEMO USE.

Then test the applicable surfaces.

### DOCX/Office minimum review

- built-in heading hierarchy is logical;
- tables use simple structures and meaningful header rows;
- links are meaningful where present;
- meaningful images have alt text or are explicitly decorative;
- color is not the only carrier of critical meaning;
- text remains readable without visual-only cues;
- automated accessibility audit/checker is used when executable;
- residual limitations are disclosed.

### XLSX minimum review

- sheet names and navigation are meaningful;
- table headers are explicit;
- critical states are text-labelled, not color-only;
- hidden sheets/columns are intentional;
- editable/calibration fields are identifiable;
- key information remains understandable without charts alone.

### PDF minimum review

If an accessible PDF is required, it must have appropriate document structure/tags/navigation and be generated from an accessible source workflow.

If the PDF is not fully accessible but accessibility is not a contractual blocker, the package must identify an accessible alternative (for example an accessible DOCX/HTML source) and record the residual limitation.

```text
ACCESSIBILITY LIMITATION DISCLOSED
MAY BE ACCEPTABLE ONLY
WHEN CURRENT CONTRACT/RISK MODE ALLOWS IT
```

---

## 14. Phase 9 — intended-use validation without overclaiming

Step20 must maintain distinct validation states:

1. `ANALYST_SCENARIO_VALIDATION` — adversarial cognitive walkthrough against expected recipient tasks;
2. `INDEPENDENT_REVIEWER_VALIDATION` — separate assurer/reviewer when required by risk mode;
3. `REAL_USER_OR_COMMISSIONER_VALIDATION` — actual intended user/commissioner feedback, usually in Step21 unless the workflow explicitly performs it earlier.

Never write `VALIDATION COMPLETE` when only state 1 happened.

### Scenario validation questions

Use realistic recipient tasks, for example:

- Can the recipient identify what the package is and whether it is draft/demo/final?
- Can they find the most important actions without internal repo knowledge?
- Can they understand what not to do?
- Can they trace a semantic/task/page decision?
- Can they distinguish analytical priority from production schedule?
- Can they locate unresolved/HOLD items and understand what would unblock them?
- Can they identify implementation owner/effort fields that require real calibration?
- Can they see what evidence is current vs historical/limited?
- Can they find measurement/acceptance guidance?
- Can they use the package without manual reconstruction of internal files?
- Does the package visibly satisfy each applicable product-promise/acceptance criterion rather than only matching internal schemas?
- Can they distinguish ordinary Search evidence, AI causal results, supported positive no-change findings and unresolved states?

For a rehearsal with no real recipient, `REAL_USER_OR_COMMISSIONER_VALIDATION` may be `NOT_APPLICABLE_TO_REHEARSAL`, but that state is not equivalent to a completed real-user test.

---

## 15. Phase 10 — assurance independence

Assurance independence is an execution property, not a disclaimer paragraph.

The current job must record:

- analyst identity/role;
- assurer identity/role or independence route;
- independence level;
- what the independent path actually rechecked;
- what remains self-assured only;
- whether current risk mode permits that residual limitation.

### Acceptable examples by proportionality

- separate analyst/reviewer;
- owner-approved external reviewer;
- independent computational verifier for mechanical invariants **plus** a separate human/analytical reviewer for high-risk judgments;
- for low-risk rehearsal only, adversarial same-analyst review + independent mechanical route, explicitly not called formal independent assurance.

```text
INDEPENDENT COMPUTATIONAL CHECK
!= INDEPENDENT ANALYTICAL JUDGMENT
```

Mode B/C cannot silently downgrade mandatory independence because no reviewer is available.

---

## 16. Phase 11 — artifact provenance / attestation

Always record hashes and exact build/run lineage.

When provenance risk is material or artifacts are formally released, prefer a signed provenance statement/attestation for the release bundle or manifest where the platform supports it.

Required distinction:

```text
ATTESTATION PROVES WHERE/HOW AN ARTIFACT WAS BUILT
IT DOES NOT PROVE THE ANALYTICAL CLAIMS ARE CORRECT
```

If attestation is not used, record why the current risk mode does not require it.

---

## 17. Defect severity must be pre-defined and release-linked

Use a declared severity policy before execution.

### BLOCKING / CRITICAL

Examples: corrupted/unopenable required artifact, unreconciled core dataset, client claim contradicts accepted evidence in a way that could materially misdirect implementation, mandatory assurance/accessibility/compliance requirement unavailable.

Consequence: immediate release STOP; affected upstream work reopened.

### MATERIAL

Examples: stale recommendation, wrong current-page scope, missing required contract/distribution identity, incorrect priority/action state, material cross-artifact contradiction.

Consequence: Step21 blocked until upstream correction and fresh Step20 rerun.

### MINOR

Examples: metadata/layout/hygiene issue with no material effect on analytical meaning or safe use.

Consequence: fix before handoff when practical; it blocks only if the current contract/risk mode says so.

### INFORMATIONAL

Improvement suggestion with no current correctness/release impact.

Consequence: does not block release.

Do not downgrade a defect merely because fixing it is inconvenient.

---

## 18. Material mutation invalidates the old Final QA

This is a hard rule:

```text
MATERIAL UPSTREAM OR CLIENT-PACKAGE CHANGE
-> OLD STEP20 VERDICT IS HISTORICAL
-> FREEZE NEW RELEASE CANDIDATE
-> RUN FRESH STEP20
```

Fixing every previously known defect does **not** prove no new defect was introduced.

```text
KNOWN DEFECTS RESOLVED
!= GLOBAL FINAL QA PASS
```

This rule prevents the exact failure mode where a correction is treated as retroactively validating an earlier QA run.

---

## 19. Mandatory Step20 outputs

The physical filenames are job-specific, but every Step20 execution must produce equivalent logical outputs:

1. execution/release-candidate freeze;
2. risk register;
3. full final-QA ledger;
4. defect ledger;
5. current-URL availability/content/role ledger when current pages matter;
6. data-quality reconciliation;
7. claim reverse-trace;
8. physical distribution QA;
9. accessibility QA/state;
10. intended-use validation ledger;
11. assurance-independence statement;
12. freshness/expiry statement;
13. provenance/attestation statement;
14. final assurance report;
15. current state + workflow sync;
16. persistence/readback seal.

Jobs may combine physical files, but none of these logical controls may disappear silently.

---

## 20. Correct execution order

The required order is deliberately causal:

```text
1. READ LEVEL1 + CURRENT JOB TRUTH
2. STATE WHOLE GOAL + ROADMAP + STEP20 PURPOSE
3. DECLARE INTENDED USE / ASSURANCE MODE
4. BUILD RISK REGISTER BEFORE TESTING
5. FREEZE EXACT RELEASE CANDIDATE
6. DERIVE COMPLETE QA UNIVERSES MECHANICALLY
7. RUN VERIFICATION + SIX DATA-QUALITY DIMENSIONS
8. RECHECK CURRENT HTTP AVAILABILITY WHERE EXECUTABLE
9. RECHECK CURRENT CONTENT / ANALYTICAL ROLE SEPARATELY
10. ASSIGN FRESHNESS WINDOW / EXPIRY CONDITIONS
11. REVERSE-TRACE MATERIAL CLIENT CLAIMS
12. RUN PHYSICAL / HIDDEN-DATA / METADATA QA
13. RUN ACCESSIBILITY QA OR DOCUMENT PROPORTIONATE LIMITATION
14. RUN ANALYST SCENARIO VALIDATION
15. RUN REQUIRED INDEPENDENT ASSURANCE PATH
16. RECORD ARTIFACT PROVENANCE / ATTESTATION STATE
17. CLASSIFY DEFECTS AGAINST PRE-DECLARED SEVERITY POLICY
18. IF MATERIAL/BLOCKING -> REOPEN EXACT UPSTREAM WORK
19. IF CORRECTED -> FREEZE NEW REVISION AND RERUN STEP20
20. ONLY AFTER NO UNRESOLVED RELEASE-BLOCKING DEFECTS -> PERSIST + READBACK
21. ISSUE FINAL ASSURANCE VERDICT WITH RESIDUAL RISKS
22. ONLY THEN ALLOW STEP21
```

### Why this order matters

Risk must precede testing so severity is not result-driven. Freeze must precede QA so one exact revision is assured. Current-world accuracy must be tested separately from internal consistency. Accessibility and intended-use validation happen before release, not as post-handoff cleanup. Material corrections invalidate the previous assurance revision. Readback occurs before transition so a local result cannot masquerade as project truth.

---

## 21. PASS gate

Step20 may return release PASS only when all applicable conditions are true:

- exact revision frozen;
- risk mode declared;
- physical/distribution, semantic/canonical and product/deliverable assurance dimensions separately pass;
- risk register complete;
- all promised logical/physical deliverables accounted;
- completeness/uniqueness/consistency/timeliness/validity/accuracy reviewed;
- complete correction universe reconciles through final master, every material client view and physical package;
- no semantic correctness claim relies only on sibling derivatives from the same generation path;
- all applicable product-promise/acceptance criteria have explicit release evidence/verdict;
- implementation-critical current-world claims are fresh enough for intended handoff;
- HTTP availability and content/role evidence are not conflated;
- material claims reverse-trace to current evidence and limitations;
- physical artifact identity/openability/render/distribution hygiene pass;
- accessibility requirement/state is explicit and acceptable for current mode;
- analyst scenario validation passes;
- required independence tier is satisfied;
- provenance state is acceptable for current risk mode;
- no unresolved BLOCKING/CRITICAL defect;
- no unresolved MATERIAL defect;
- unresolved MINOR/INFORMATIONAL items are explicitly accepted under current contract/risk;
- current release candidate has not mutated after QA;
- all authorities persisted and read back;
- Step21 has not been falsely claimed before actual handoff.

A PASS must state residual risks and expiry/recheck conditions.

---

## 22. Claim boundaries

Step20 PASS means:

> the exact tested revision passed the declared assurance method for the declared intended use and risk mode at the recorded freshness state.

It does **not** mean:

- future site state will remain unchanged;
- all business outcomes are guaranteed;
- real user acceptance occurred unless explicitly recorded;
- formal independent assurance occurred unless the required reviewer actually performed it;
- accessibility compliance beyond the tested standard/contract is guaranteed;
- provider/private evidence exists when it was not used;
- a later modified package inherits the same PASS.

---

## 23. Permanent non-repeat rules

```text
RESEARCH READ != REQUIREMENT OPERATIONALIZED
STEP19 QA != STEP20 RELEASE ASSURANCE
CONSISTENCY != ACCURACY
SEARCH RESULT != LIVE HTTP AVAILABILITY
HTTP 200 != CORRECT CURRENT ROLE
TIMESTAMP != FRESHNESS GOVERNANCE
VISUALLY READABLE != ACCESSIBLE
ANALYST SCENARIO VALIDATION != REAL USER VALIDATION
INDEPENDENT COMPUTATIONAL CHECK != INDEPENDENT ANALYTICAL ASSURANCE
HASH MATCH != SIGNED BUILD PROVENANCE
KNOWN DEFECTS RESOLVED != GLOBAL FINAL QA PASS
CONSISTENT BUGGY DERIVATIVES != INDEPENDENT SEMANTIC VALIDATION
PHYSICAL QA PASS != SEMANTIC QA PASS != PRODUCT ACCEPTANCE PASS
OLD QA PASS/CORRECTION_REQUIRED != VERDICT FOR A NEW REVISION
```

These are causal controls, not slogans. Before Step20 execution, the analyst must be able to explain the failure mechanism behind each rule that is material to the current job.

---

## 24. Mandatory owner-facing summary

Before execution, explain in plain language:

- what the final QA is trying to disprove;
- what can block release;
- what evidence/current-site freshness will be rechecked;
- what independence/accessibility/user-validation level applies;
- what will happen if a material defect is found.

After execution, explain:

- what was tested;
- whether physical/distribution, semantic/canonical and product/deliverable assurance each passed;
- whether the complete correction universe reached every material client view and physical artifact;
- what defects were found;
- what remains uncertain;
- whether the exact revision may move to handoff;
- when the QA expires or must be rerun.

Technical tables do not replace this explanation.
