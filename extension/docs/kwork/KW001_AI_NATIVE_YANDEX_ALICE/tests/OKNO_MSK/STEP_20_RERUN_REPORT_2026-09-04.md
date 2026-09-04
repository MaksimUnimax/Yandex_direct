# OKNO_MSK — Step20 enhanced Final QA rerun report

Date: 2026-09-04  
Step: **20 — Final QA / release assurance**  
Declared use mode: **MODE A — TEST/DEMO REHEARSAL**  
Provider calls: **0**  
New paid cost: **0 RUB**

## Why Step20 was rerun

The first Step20 execution correctly found material defects and blocked handoff. Those defects were then fixed in Step18/Step19 and the corrected package was rebuilt and read back.

A corrected package cannot inherit the old QA verdict automatically. The enhanced Step20 method therefore required a **fresh release-candidate freeze and a complete rerun**.

```text
KNOWN DEFECTS RESOLVED
!= GLOBAL FINAL QA PASS

OLD QA VERDICT
!= VERDICT FOR A NEW REVISION
```

## Why the Step20 method itself was changed

The first Step20 preparation had researched strong external assurance guidance, but several important requirements remained narrative knowledge instead of hard execution gates.

The main process failure was:

```text
RESEARCH READ
!= REQUIREMENT OPERATIONALIZED
```

The first method was also shaped too closely like a stronger version of Step19 package QA. That produced good reconciliation, current-site checks and defect detection, but it did not start from a full risk/assurance lifecycle.

The corrected permanent Step20 method now requires, before release:

- intended-use/risk mode;
- pre-test risk register and severity consequences;
- exact release-candidate freeze;
- verification plus six explicit data-quality dimensions;
- separate live HTTP availability, current content and analytical-role evidence;
- freshness expiry/sunset logic;
- reverse trace of material client claims;
- hidden-data/distribution QA;
- accessibility QA/state;
- separate analyst-scenario vs independent-review vs real-user validation states;
- assurance-independence mode proportional to risk;
- exact provenance and, when justified, signed artifact attestation;
- fresh Step20 rerun after any material mutation.

Canonical Level1 authority:

`STEP_20_FINAL_QA_AND_RELEASE_ASSURANCE_METHOD.md`

## Declared assurance mode

This job is a mock commercial rehearsal and the physical package is explicitly marked TEST/DEMO.

Therefore the enhanced rerun uses **Mode A**:

- adversarial analyst QA = required;
- separate independent mechanical verifier = required;
- formal independent analytical assurer = not required for this rehearsal and is **not claimed**;
- real user/commissioner validation = `NOT_APPLICABLE_TO_MOCK_REHEARSAL`, which is **not equivalent to completed real-user validation**.

A consequential real-client or high-impact job must use the stronger independence mode defined by the Level1 method.

## Risk was registered before testing

`STEP_20_RERUN_RISK_REGISTER.tsv` pre-registered 17 failure families before substantive rerun testing, including:

- stale/wrong actions;
- missing or duplicate records;
- cross-artifact contradiction;
- unresolved/HOLD promoted to certainty;
- URL transport/redirect changes;
- stale content/role truth;
- AI overgeneralization;
- analytical priority overstated as a production schedule;
- corrupted or mismatched physical artifacts;
- hidden/private metadata;
- accessibility/usability limitations;
- TEST/DEMO identity ambiguity;
- expired evidence at handoff;
- provenance gap;
- false real-user validation claim;
- false handoff/revision claim;
- treating known defect fixes as a new global PASS.

Every risk had a release consequence before testing. After execution, all 17 risks are closed for the declared Mode A; one accessibility item remains as an accepted MINOR residual.

## Exact release candidate

The rerun froze the corrected physical package before testing:

```text
STEP_19_CLIENT_WORKBOOK_CORRECTED.xlsx
bytes = 458600
sha256 = 9f08cb47b1f4863f90b84c2d3a1ae145341ff5fd5f9c57ee76f2c087c642d499

STEP_19_CLIENT_REPORT_CORRECTED.docx
bytes = 44078
sha256 = d68001ee36f1677cf0817e3058e490bdfcc1598da324b3cd62a5670c1644b3dd

STEP_19_CLIENT_REPORT_CORRECTED.pdf
bytes = 59868
sha256 = cf4a208ba5286243e41ef5dff31a5d3eea9fdc0dab93800850addcc07663915e
```

No mixed-revision assurance was allowed.

## Independent mechanical verification

GitHub Actions run `33826172895` completed successfully.

It independently checked:

- exact physical file identity;
- materialized package accounting;
- corrected A012/A027 propagation;
- forbidden claim boundaries;
- TEST/DEMO identity;
- DOCX metadata hygiene;
- all 48 implementation-critical URLs by direct HTTP request;
- release-bundle provenance.

HTTP result:

```text
implementation-critical URLs = 48
HTTP 200 = 48
redirects = 0
non-2xx = 0
transport errors = 0
```

This is deliberately treated as **transport availability only**.

```text
HTTP 200
!= CURRENT CONTENT CORRECT
!= CURRENT ANALYTICAL ROLE CORRECT
```

## Fresh current-content evidence

Because the old role ledger contained evidence of different ages, the rerun did not pretend that fresh HTTP 200 responses refreshed content truth.

A second workflow, run `33826432798`, fetched fresh full text for all 48 implementation-critical pages.

Result:

```text
fresh full-text pages = 48/48
HTTP 200 = 48/48
compatible current title/H1 identity = 48/48
review/error = 0
```

The fresh snapshot was then used for deeper analyst review of action-sensitive content.

### Current action-sensitive findings

- **Door page:** current price factors/calculator/measurer guidance remains present. The corrected action therefore remains narrow: only door-specific professional installation scope/process depth may still be strengthened. Existing price guidance must not be duplicated.
- **French-window page:** a basic French/in-floor definition remains present. The corrected definition action remains downstream/combined with the broader French-window content action; only residual naming/French-vs-panoramic distinction may be added if still missing.
- **Private-house page:** it already has sample dimensions, non-standard opening material, calculator sizing and measurement guidance. The remaining action is only a clearer standard-vs-non-standard sizing-principles explanation, not a claim that all size/measurement content is absent.
- **Hardware guide:** it already has substantial hardware guidance and several brands; the current gap is a bounded parts/additional-brand expansion, not absence of hardware content.
- **Aluminium technical article:** generic ventilation is mentioned, but current text does not expose the intended micro-ventilation/ventilation-valve guidance; the action remains bounded.
- **Best-windows article:** fresh text still contains a ranking framed around 2024 while the current job date is 2026, so the freshness/methodology recheck remains valid.
- **Portfolio:** project examples exist; no clear filter/category system for the target design families was observed, so taxonomy/discoverability remains a bounded improvement.
- **Panoramic aluminium:** current aluminium material covers warm/cold and large-format context, but no dedicated decision subsection for the bounded panoramic-aluminium need was observed; no new URL is authorized.

No new MATERIAL action contradiction or page-role disappearance was found.

## Six-dimensional data quality

`STEP_20_RERUN_DATA_QUALITY.json` records:

```text
completeness = PASS
uniqueness = PASS
consistency = PASS
timeliness = PASS WITH EXPLICIT EXPIRY
validity = PASS
accuracy = PASS FOR DECLARED CURRENT SCOPE
```

Internal consistency was not used as a substitute for current-world accuracy.

## Core accounting

The rerun preserves:

```text
logical deliverables = 9/9
primary directions = 15 / max 15
active semantic rows = 2332
SEARCH_REQUIRED = 19
AI cases = 8
  CHANGE = 0
  DE_RISK = 4
  NO_CHANGE = 3
  INSUFFICIENT = 1
page actions = 34
execution packages = 112
  exact action = 31
  internal link = 15
  route to existing = 46
  HOLD/recheck = 20
non-HOLD packages = 92
measurement classes = 7
supported new-page actions = 0
supported destructive actions = 0
```

Production sequence remains `PENDING_CALIBRATION`. P1/P2/P3 are not described as a committed sprint/calendar schedule.

## Claim reverse trace

The enhanced claim ledger reverse-traces 28 material release claims from client surface back to current authority/evidence/QA.

It confirms, among other things:

- no unsupported new-page/destructive action;
- no sitewide or longitudinal AI claim from the 8-case diagnostic;
- no ranking/traffic/lead/revenue guarantee;
- no private Webmaster/Metrika/Direct observation presented as current evidence;
- observed Wordstat counts are not relabelled as guaranteed exact-query frequency;
- actual handoff/revision completion is not claimed before Step21.

## Physical distribution QA

### XLSX

- exact frozen identity = PASS;
- 9 expected visible sheets;
- 2332 semantic rows;
- 112 execution packages;
- 7 measurement classes;
- hidden sheets = 0;
- comments parts = 0;
- external-link parts = 0;
- VBA = 0;
- formula-error tokens = 0;
- critical statuses remain text-labelled, not color-only;
- TEST/DEMO identity visible.

### DOCX

- exact frozen identity = PASS;
- 6/6 rendered pages previously inspected on the same SHA-256 = PASS;
- TEST/DEMO identity visible;
- generic python-docx metadata/stale template chronology removed;
- automated accessibility audit = **0 high / 0 medium / 0 low findings**.

### PDF

- exact frozen identity = PASS;
- 4/4 rendered pages previously inspected on the same SHA-256 = PASS;
- TEST/DEMO identity visible;
- encrypted = false;
- attachments = 0;
- annotations = 0;
- **tagged = false**.

The untagged PDF is the single accepted MINOR residual for this Mode A rehearsal. The DOCX is available as an accessible alternative and passed the automated accessibility audit.

This is **not** a claim of PDF accessibility compliance. If a future contract/audience requires an accessible/tagged PDF, this same state becomes a release defect and must be corrected before handoff.

## Intended-use validation

Twelve analyst scenario tasks were tested and passed, including:

- identify TEST/DEMO status;
- find important actions;
- understand do-not-do boundaries;
- use semantic mapping without repository reconstruction;
- distinguish analytical priority from production schedule;
- find HOLD items and blockers;
- find owner/effort/capacity calibration fields;
- find measurement logic;
- understand AI limits;
- understand corrected door and French-window actions;
- see that actual handoff has not yet occurred.

Real user/commissioner validation was not performed and is not claimed.

## Assurance independence

For this Mode A rehearsal:

- adversarial same-analyst analytical QA = performed;
- independent mechanical verifier = performed via GitHub Actions;
- fresh current-content acquisition route = performed separately;
- formal independent analytical assurer = absent and not claimed;
- real user/commissioner acceptance = not performed and not claimed.

This satisfies the declared rehearsal mode, not a stronger real-client Mode B/C assurance claim.

## Freshness / expiry

The current-site evidence is deliberately time bounded.

For this Level2 rehearsal configuration:

```text
valid through UTC = 2026-09-07T01:37:05Z
```

It expires earlier if there is a known site deploy/content change, offer/business change, redirect/URL-structure change, material upstream correction or material client-package rebuild.

Before actual Step21 distribution, the freshness gate must be checked again. If expired, affected current-site checks must be rerun.

This 72-hour window is **not a universal permanent Step20 constant**.

## Signed provenance

The exact release bundle was built in GitHub Actions and received a signed artifact attestation.

```text
workflow run = 33826172895
bundle sha256 = f1c06b653c5b7540d03ad8ae6d5872ac24d87011a8cab211d06dd5be2ec79623
attestation id = 45139802
```

Build provenance does not prove analytical correctness; it proves which workflow/repository context produced the attested bundle.

## Defect verdict

```text
BLOCKING = 0
MATERIAL = 0
MINOR ACCEPTED FOR MODE A = 1
```

The only residual is the untagged PDF accessibility state.

## Prefinal transition verdict

All substantive enhanced Step20 gates pass for the declared Mode A.

The final transition remains **prefinal** until the enhanced Step20 ledgers/report/state are persisted and read back from GitHub.

If readback succeeds:

```text
STEP20 = PASS FOR DECLARED MODE A TEST/DEMO RELEASE ASSURANCE
STEP21 = ALLOWED, NOT STARTED
```

Actual Step21 handoff/revisions remain separately authorized work.
