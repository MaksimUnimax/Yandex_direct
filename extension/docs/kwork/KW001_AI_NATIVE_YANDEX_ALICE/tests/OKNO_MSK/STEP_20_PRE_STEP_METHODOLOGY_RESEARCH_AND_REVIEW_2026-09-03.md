# OKNO_MSK — STEP 20 PRE-STEP METHODOLOGY RESEARCH AND REVIEW

Date: 2026-09-03  
Step: 20 — Final QA  
Status: **PRE-STEP METHOD RESEARCH COMPLETE / EXECUTION NOT AUTHORIZED / EXECUTION NOT STARTED**

## 1. Whole Kwork goal

Deliver a client-usable, evidence-backed semantic/page-architecture package for ordinary Yandex Search with bounded AI diagnostic evidence, where every important recommendation is traceable to accepted evidence, current-page truth, an explicit uncertainty boundary and an actionable next step.

Step19 has already produced the physical client package. Step20 is not another analysis or packaging step. Its job is to determine whether the exact current package is safe to hand over as the final current version.

## 2. Full roadmap and current position

| Step | Purpose | Status |
|---|---|---|
| 0 | Scope/order freeze | COMPLETE |
| 1 | Current site/business discovery | COMPLETE |
| 2 | Bounded acquisition planning | COMPLETE |
| 3 | Wordstat acquisition | COMPLETE |
| 3R | Recovery/reconciliation | COMPLETE |
| 4 | First family triage | COMPLETE |
| 5 | Targeted expansion | COMPLETE |
| 6 | Demand dynamics/seasonality | COMPLETE / PRESERVED |
| 6A | Coverage revalidation | COMPLETE |
| 7 | Row-level semantic cleanup | COMPLETE AFTER CORRECTION |
| 8 | Search-stage semantic freeze | COMPLETE AFTER METHOD CORRECTION |
| 9 | Ordinary Yandex Search validation | COMPLETE AFTER METHOD/PERSISTENCE CORRECTIONS |
| 10 | User-task/Search clustering | COMPLETE / VERIFIED |
| 11 | Page ownership / phrase-to-page mapping | COMPLETE AFTER EXTERNAL AUDIT + PHRASE CORRECTION |
| 12 | Structural/content-routing actions + links | COMPLETE AFTER CORRECTIONS + INDEPENDENT QA |
| 13 | Competing-page diagnosis | COMPLETE / BASE-PUBLIC BOUNDED |
| 14 | Search-only architecture freeze | FINAL PASS |
| 14A | Current-site/topology reconciliation | FINAL PASS |
| 15 | AI-case selection | COMPLETE |
| 16 | AI evidence acquisition | COMPLETE |
| 17 | Search-vs-AI comparison | COMPLETE / BOUNDED DIAGNOSTIC |
| 18 | Prioritization / implementation readiness | ANALYTICAL PRIORITY COMPLETE / FINAL SCHEDULE PENDING CALIBRATION |
| 19 | Client-facing deliverables | COMPLETE AFTER POST-EXTERNAL-AUDIT CORRECTION + FINAL READBACK SEAL |
| **20** | **Final QA** | **CURRENT PRE-STEP** |
| 21 | Handoff / revisions | NOT STARTED |
| 22 | Job close | NOT STARTED |

## 3. Completed work

Verified completed work includes Steps 0–19, including the corrected Step19 package:

- 15 primary client directions;
- 2332 materialized active phrase → task → page rows;
- 19 preserved `SEARCH_REQUIRED` unresolved rows;
- 8 bounded Search-vs-AI cases;
- 34 analytical page/action rows;
- 112 execution-addressable work packages;
- 20 HOLD/recheck packages;
- 7 measurement classes;
- physical XLSX/DOCX/PDF package;
- Step19 post-external-audit final GitHub readback seal.

Step20 must not treat any of those counts as true merely because Step19 reported them. They are inputs to be re-verified.

## 4. Remaining work

1. Step20 Final QA.
2. Step21 actual handoff / revision cycle.
3. Step22 close only after handoff/revisions and pending actions are resolved.

## 5. Current step goal

Determine whether the exact current Step19 client package is fit for final handoff by independently rechecking, as far as the current workflow permits:

- specification compliance;
- client usability;
- claim/evidence traceability;
- count/ID/data consistency;
- unresolved/HOLD preservation;
- current implementation-critical URL existence and role;
- version identity;
- physical distribution hygiene;
- no overclaiming of implementation readiness, AI scope or business outcomes.

## 6. What Step20 solves

Step19 proves that the deliverables were built and corrected. Step20 answers a different question:

```text
CAN THIS EXACT CURRENT VERSION BE HANDED OVER WITHOUT A MATERIAL QA DEFECT?
```

A previous PASS is not evidence that the final package still passes after subsequent corrections. Step20 therefore starts from a frozen current revision and distrusts prior PASS labels until they are reconciled.

## 7. Required output

Execution must produce at minimum:

1. `STEP_20_FINAL_QA_LEDGER.tsv` — one check row per QA requirement/object.
2. `STEP_20_DEFECT_LEDGER.tsv` — every found defect, severity, affected authority/deliverable, correction owner/stage and blocking state.
3. `STEP_20_CURRENT_URL_ROLE_RECHECK.tsv` — every implementation-critical current URL checked with timestamp, final URL, availability and current role.
4. `STEP_20_CLAIM_REVERSE_TRACE.tsv` — material client claims → requirement → evidence/authority → deliverable location → QA result.
5. `STEP_20_DATA_RECONCILIATION.json` — counts/IDs/uniqueness/consistency/timeliness/validity/accuracy checks.
6. `STEP_20_PHYSICAL_PACKAGE_QA.json` — XLSX/DOCX/PDF identity/openability/distribution-hygiene checks.
7. `STEP_20_ASSURANCE_STATEMENT.md` — what was verified/validated, remaining limitations, and whether formal independent assurer separation existed.
8. `STEP_20_REPORT.md` — client-package QA result and correction decision.
9. `STEP_20_CURRENT_STATE.json` + final readback seal/job-flow sync.

Exact physical artifact rebuild is **not** part of Step20. If Step20 finds a material artifact defect, it must classify the affected prior step as correction-required and stop before Step21 rather than silently rebuilding within Final QA.

## 8. Relevant prior errors / corrections freshly re-read

### 8.1 Known defects fixed != global coherence proven

Prior failure pattern: local corrections were treated too close to proof that the whole downstream system remained coherent.

Control for Step20:

```text
PRIOR STEP PASS != STEP20 PASS
```

Every final client fact used by Step20 must be re-reconciled from current authority.

### 8.2 Historical downstream PASS != valid after material upstream mutation

Prior failure pattern: downstream results were left trusted after upstream authority changed.

Control:

- freeze Step20 start HEAD;
- compare all current terminal authorities against the client package generated from them;
- any material mismatch is `CORRECTION_REQUIRED`.

### 8.3 Old site inventory != current site truth

Step20 has an explicit Level1 requirement to run a lightweight current URL/final-role recheck for every implementation-critical URL in the client output.

Control:

- mechanically materialize the named URL universe from current client/action/execution views;
- check each URL now;
- preserve redirect/final URL/current visible role;
- do not infer continued role from Step14A alone.

### 8.4 Analytical priority != production schedule

Control:

Any client-facing wording that converts P1/P2/P3 to a committed sprint/calendar order while owner/effort/capacity remain unknown is a blocking claim defect.

### 8.5 Traceability PASS != client usability PASS

Control:

Step20 retains a distinct validation layer: the package must be understandable and usable for its intended recipient, not merely internally traceable.

### 8.6 Logical deliverable != physical artifact

Control:

The final physical XLSX/DOCX/PDF identities are explicitly part of Step20 QA. Repo-native source files cannot substitute for the client files.

### 8.7 Mock/test identity may not be silently presented as a real paid-client result

`TEST_ORDER.md` freezes this run as a mock commercial rehearsal and requires portfolio artifacts derived from it to be clearly labelled test/demo.

Control:

Step20 must explicitly check the client/package/demo labelling. Absence or ambiguity is a deliverable-governance defect; severity depends on the intended distribution surface.

## 9. Fresh external methodology research

Step20 is `UNVALIDATED` in the permanent rules index, so fresh method research was required.

### 9.1 GOV.UK — The AQuA Book

Source: https://www.gov.uk/guidance/the-aqua-book

Classification: `OFFICIAL / PRIMARY ANALYTICAL QA GUIDANCE`.

Material method support:

- analytical assurance must include both **verification** (does analysis meet its specified design requirements?) and **validation** (does it meet intended user needs/use environment?);
- QA should reconcile results to independent sources where practical;
- the latest version must be controlled and changes visible/assurable;
- delivery/sign-off should confirm commission requirements were met, documentation/evidence captured and assurance performed;
- uncertainty and limitations must remain visible;
- formal assurer/analyst separation is a stronger standard than a self-check.

Step20 operationalization:

```text
VERIFICATION LAYER
= spec/count/ID/file/claim/evidence/current-URL checks

VALIDATION LAYER
= client-independent-use / clarity / intended-use / limitation checks
```

Important limitation: this current workflow does not have a formally separate human/analytical assurer. Therefore Step20 may claim an adversarial final QA pass, not formal independent assurance in the AQuA sense. Owner/recipient sign-off remains Step21.

### 9.2 GOV.UK — Verification and Validation for the AQuA Book

Source: https://www.gov.uk/government/publications/verification-and-validation-for-the-aqua-book

Classification: `OFFICIAL`.

Material support: verification and validation are both necessary components of analytical quality. This reinforces the two-layer QA design instead of treating error-free computation as sufficient.

### 9.3 GOV.UK — Government Data Quality Framework

Source: https://www.gov.uk/government/publications/the-government-data-quality-framework/the-government-data-quality-framework-guidance

Classification: `OFFICIAL`.

Material support: fit-for-purpose quality can be evaluated using dimensions including:

- completeness;
- uniqueness;
- consistency;
- timeliness;
- validity;
- accuracy.

Step20 maps these to the client package:

```text
COMPLETENESS = all expected deliverables/rows/IDs/states exist
UNIQUENESS = IDs/keys expected unique are unique
CONSISTENCY = same fact/count/state agrees across views
TIMELINESS = implementation-critical URL/page role reflects current site
VALIDITY = formats/enums/URLs/hashes/files obey contract
ACCURACY = material claims match accepted evidence and current reality
```

### 9.4 Microsoft Support — Document Inspector

Source: https://support.microsoft.com/en-us/office/collab-files/remove-hidden-data-and-personal-information-by-inspecting-documents-presentations-or-workbooks

Classification: `OFFICIAL PRODUCT GUIDANCE`.

Material support: before sharing Office files, hidden data/personal information, comments/revisions, document properties, hidden rows/worksheets, external links and related hidden content should be inspected.

Operationalization:

Step20 must inspect the persisted XLSX/DOCX package for distribution-hygiene risks available to our tooling. It must not delete or mutate content during QA. A material hygiene defect reopens Step19 packaging.

### 9.5 Microsoft Support — Detect formula errors in Excel

Source: https://support.microsoft.com/en-us/excel/detect-formula-errors-in-excel

Classification: `OFFICIAL PRODUCT GUIDANCE`.

Material support: formula error checking helps identify common mistakes but does not guarantee a workbook is error-free.

Operationalization:

- preserve Step19 formula-error scan;
- independently rescan workbook formulas/error tokens where tooling permits;
- do not use “0 formula errors” as a substitute for semantic/data QA.

### 9.6 Yandex Webmaster — Page check / diagnostics / query analytics

Sources:

- https://www.yandex.com/support/webmaster/en/service/check-url
- https://yandex.com/support/webmaster/en/service/site-diagnostics
- https://yandex.com/support/webmaster/en/service/statistics
- https://yandex.com/support/webmaster/en/service/queries-analytic

Classification: `OFFICIAL YANDEX`.

Material support:

- URL/page status and bot response are separate things that can be checked in Webmaster when access exists;
- Search query statistics include impressions, clicks, CTR and average position with specific Yandex semantics and can differ from Wordstat/Metrika;
- current diagnostics can change over time.

Current job boundary:

Private Webmaster access is excluded from this base rehearsal. Step20 therefore does **not** acquire or imply private Webmaster evidence. It uses current public page existence/content for URL-role QA. Any future Webmaster metric mentioned remains an optional future measurement route, not current evidence.

### 9.7 Ahrefs — SEO reporting

Source: https://ahrefs.com/blog/seo-reporting/

Classification: `INDUSTRY_PRACTICE`.

Material support: strong SEO reports should be data-led and actionable; executive summaries should represent the reconciled report rather than replace detail.

Operationalization: Step20 validates that key recommendations are specific enough to act on and that the summary does not contradict the detailed package.

### 9.8 Search Engine Land — audit recommendation failures

Source: https://searchengineland.com/technical-seo-audit-mistakes-486318

Classification: `INDUSTRY_PRACTICE`.

Material support: audits fail when findings are not validated or recommendations do not explain cause, importance and what should happen next.

Operationalization: Step20 tests action rows for evidence/cause/next-step/boundary, not merely presence of a recommendation label.

## 10. Method verdict

`PROJECT_SPECIFIC_BUT_REASONED`

Reason:

- Step20 has no owner-approved permanent full method;
- the proposed method is grounded in official analytical QA/data-quality/product documentation plus current Yandex semantics and corroborating SEO reporting practice;
- formal independent analyst/assurer separation cannot be claimed in this execution environment;
- final owner/recipient approval therefore remains Step21.

No Level1 permanent rule is modified or promoted by this current-job preparation.

## 11. Exact Step20 execution design after owner authorization

### Phase 1 — freeze version truth

Freeze:

- Step20 execution-start branch HEAD;
- terminal Step19 current state/seal;
- physical artifact manifest;
- logical deliverable blob identities;
- current canonical upstream authorities needed for reverse trace.

If branch HEAD changes materially during Step20, classify and re-freeze or stop; do not mix revisions.

### Phase 2 — materialize QA universes

Mechanically derive:

1. logical deliverable universe: 9/9 required outputs;
2. physical package universe: XLSX/DOCX/PDF + manifest;
3. semantic universe: 2332 materialized rows + 19 unresolved accounting;
4. AI universe: 8 exact cases;
5. page/action universe: 34 actions;
6. execution universe: 112 exact packages;
7. HOLD universe: 20 packages;
8. measurement universe: 7 classes;
9. implementation-critical URL universe: exact unique current-site URLs referenced by client/action/execution views where a live page role affects implementation.

The URL count is produced mechanically at execution start; it is not guessed in pre-step.

### Phase 3 — full mechanical data-quality reconciliation

Run full, not sample-only, checks where deterministic structure permits:

- expected row counts;
- stable IDs/keys;
- uniqueness;
- enum/state validity;
- null/intentional unknown distinction;
- action ↔ package membership;
- HOLD preservation;
- priority/state consistency;
- cross-view count equality;
- source provenance presence;
- no silent active semantic drops;
- AI verdict accounting;
- physical file identity against manifest.

### Phase 4 — claim reverse trace

Material claims from:

- client summary;
- standalone report;
- method/limitations;
- delivery message;
- page-action map;
- priority plan;

must reverse-trace to:

```text
CLIENT CLAIM
-> CONTRACT/REQUIREMENT
-> CURRENT ACCEPTED EVIDENCE/AUTHORITY
-> CLAIM BOUNDARY
-> QA RESULT
```

High-risk forbidden claim families receive explicit negative tests:

- new-page authorization;
- destructive merge/delete/redirect authorization;
- implementation-ready sprint/calendar;
- client-confirmed private business priority;
- sitewide AI visibility;
- longitudinal AI stability;
- ranking/traffic/lead/revenue guarantee;
- private Webmaster/Metrika observation;
- completed handoff/revision claim before Step21.

### Phase 5 — current implementation-critical URL / final-role recheck

For every exact URL in the materialized critical-URL universe:

- timestamp;
- source deliverable/action/package;
- requested URL;
- final URL after redirect;
- HTTP/public availability where observable;
- page title/H1 or equivalent visible identity;
- visible current user task/role;
- role unchanged / materially changed / unavailable / ambiguous;
- affected action/package IDs;
- evidence route;
- QA verdict.

A URL that moved is not automatically a defect if the final target is equivalent and the client artifacts can be corrected without changing analytical meaning. A disappeared or materially repurposed implementation target is a blocking defect.

No negative whole-site absence claim is expected in Step20; therefore a fresh broad crawl is not the default method.

### Phase 6 — physical distribution QA

Against the exact persisted client binaries:

- filename/size/hash identity;
- openability/render status from current persisted package;
- workbook required sheets/rows;
- formula error rescan where possible;
- inspect workbook/document ZIP metadata for comments/revisions, external links, hidden sheets/rows where detectable, document properties and embedded objects;
- PDF metadata/openability/page count/content markers;
- explicit mock/test/demo distribution labelling requirement;
- no repo-path dependency for core client use.

If a physical artifact must change, Step20 records the defect and reopens Step19; Step20 does not silently become a packaging step.

### Phase 7 — validation / intended-use gate

Ask:

- Can a recipient understand what was studied and what was not?
- Can a recipient identify what to change and what not to change?
- Are unknown execution facts visibly calibratable rather than hidden?
- Are HOLD items distinguishable from rejection/low value?
- Is AI scope visibly bounded?
- Is the mock/demo nature clear enough for the intended distribution?
- Does the package require internal repo reconstruction for core use?

### Phase 8 — defect classification

Every issue receives:

```text
defect_id
severity = BLOCKING | MATERIAL | MINOR
quality_dimension
verification_or_validation
affected_artifact
source_authority
root_cause
required_correction_stage
step21_blocked = true/false
```

Rules:

- any BLOCKING defect => Step20 FAIL/CORRECTION_REQUIRED;
- any unresolved MATERIAL defect => Step20 CORRECTION_REQUIRED;
- MINOR non-semantic/editorial issues may be recorded for Step21 only if they do not alter evidence, action, scope, current URL, physical usability, contract or claim boundaries.

### Phase 9 — assurance statement and transition

Only if all blocking/material checks pass:

- write the assurance statement;
- explicitly state the lack of formal independent assurer separation;
- seal Step20 PASS;
- allow Step21 to begin.

If not:

- identify which prior step must reopen;
- Step21 remains blocked;
- no silent correction outside authorized Step20 QA scope.

## 12. Provider / Bridge plan

Default and planned provider execution:

```text
WORDSTAT = 0
SEARCH = 0
GENSEARCH = 0
WEBMASTER = 0
METRIKA = 0
DIRECT = 0
NEW PAID COST = 0 RUB
```

Step20 needs current public URL/content checks, not new paid evidence acquisition.

If execution uncovers a client claim that genuinely cannot be verified from persisted evidence/current public truth and would require new provider/private evidence, stop at the normal separate authorization gate. Do not call a provider merely to make Final QA look stronger.

## 13. Adversarial self-audit findings

### Finding A — formal independence cannot be claimed

The AQuA standard treats analyst/assurer separation as important. Current execution can be adversarial and frozen-input, but it is still performed by the same analytical system.

Control: record this limitation in the assurance statement; Step21 owner/recipient approval remains distinct.

### Finding B — current-site timeliness is the largest remaining live-data risk

The package can be internally perfect while a target page has moved/disappeared/changed role after Step14A.

Control: full named critical-URL recheck.

### Finding C — mock/demo labelling may be under-specified in current client-facing materials

This is a frozen order requirement and must be checked explicitly rather than assumed.

Control: distribution-labelling QA row; defect if missing/ambiguous for intended use.

### Finding D — prior physical QA does not cover every distribution-hygiene risk

Step19 checked openability/layout/formulas, but final QA should also inspect hidden metadata/external links/comments/revisions where tooling permits.

Control: physical-package hygiene scan.

### Finding E — 2332 semantic rows are too large for manual semantic re-review in Final QA

Step20 must not pretend to manually re-decide 2332 phrases. Their QA mode is full mechanical reconciliation plus targeted claim/action-level review. Reopening semantic judgement requires a concrete contradiction, not routine re-analysis.

## 14. Risks / uncertainties

- public-site access can fail or return inconsistent responses; such rows remain `UNVERIFIED_CURRENTLY` and may block affected actions if current role is material;
- some Office hidden-data inspections available in desktop Excel/Word may not be perfectly reproducible in our environment; we inspect the underlying package structures and record the coverage limit;
- current job has no private Webmaster/Metrika access;
- no formally independent assurer is available in this execution environment;
- Step20 is QA, not a new semantic/SEO research phase.

## 15. What Step20 will not do

- no new Wordstat/Search/GenSearch/Webmaster/Metrika/Direct acquisition by default;
- no new keyword expansion;
- no new AI sampling;
- no new page architecture design unless a defect forces upstream correction;
- no invented business priority, effort, owner, capacity, timeline or KPI;
- no physical artifact mutation/rebuild inside QA;
- no handoff/revision claim;
- no permanent Level1 method promotion.

## 16. Proposed PASS gate

Step20 may pass only when:

```text
START REVISION FROZEN = PASS
9/9 LOGICAL DELIVERABLES ACCOUNTED = PASS
PHYSICAL XLSX/DOCX/PDF IDENTITY = PASS
DATA QUALITY COMPLETENESS = PASS
DATA QUALITY UNIQUENESS = PASS
DATA QUALITY CONSISTENCY = PASS
DATA QUALITY VALIDITY = PASS
DATA QUALITY ACCURACY FOR MATERIAL CLAIMS = PASS
CURRENT CRITICAL-URL TIMELINESS = PASS OR NON-MATERIAL EXPLICIT LIMITATION
15 PRIMARY DIRECTIONS = RECONCILED
2332 ACTIVE SEMANTIC ROWS = RECONCILED
19 SEARCH_REQUIRED = PRESERVED
8 AI CASES / VERDICTS = RECONCILED
34 ACTIONS = RECONCILED
112 WORK PACKAGES = RECONCILED
20 HOLD PACKAGES = PRESERVED
7 MEASUREMENT CLASSES = RECONCILED
SUPPORTED NEW PAGE ACTIONS = 0
SUPPORTED DESTRUCTIVE ACTIONS = 0
IMPLEMENTATION SCHEDULE CLAIM = PENDING_CALIBRATION ONLY
FORBIDDEN AI/BUSINESS/PERFORMANCE CLAIMS = 0
MOCK/DEMO DISTRIBUTION LABELLING = PASS
CLIENT-INDEPENDENT-USE VALIDATION = PASS
BLOCKING DEFECTS = 0
UNRESOLVED MATERIAL DEFECTS = 0
PROVIDER CALLS = 0 UNLESS SEPARATELY AUTHORIZED
GITHUB PERSISTENCE + READBACK = PASS
```

Only then:

```text
STEP20 = COMPLETE_PASS
STEP21_ALLOWED = true
```

Otherwise:

```text
STEP20 = CORRECTION_REQUIRED
STEP21_ALLOWED = false
```

## 17. Plain-language owner summary

### Зачем нужен этот шаг

Чтобы перед отправкой клиенту не доверять даже нашему собственному прошлому PASS, а ещё раз проверить именно финальную текущую версию: правильные ли там цифры, живы ли нужные страницы, не изменился ли их смысл, не потерялись ли ограничения и не написали ли мы где-то больше, чем реально доказали.

### Что конкретно будем делать после авторизации

Сверим все основные таблицы и отчёты между собой и с исходными доказательствами, перепроверим все страницы сайта, от которых реально зависят рекомендации, проверим физические Excel/Word/PDF как файлы для передачи, отдельно проверим тестовую/demo маркировку и попробуем специально найти причины НЕ пропускать пакет дальше.

### Что получим в конце

Либо доказанный Final QA PASS, после которого можно переходить к фактической передаче Step21, либо точный список дефектов с указанием, что именно надо открыть на исправление. Step20 не будет скрывать дефект ради красивого статуса.
