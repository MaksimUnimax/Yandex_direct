# Step 14 — Search-only architecture freeze report

Date: 2026-09-01  
Job: `OKNO_MSK`  
Mode: `BASE_PUBLIC_EVIDENCE_MODE`  

## Executive result

Step 14 Search-only architecture freeze is complete and passes the job-level acceptance gate.

The freeze is built from the canonical Step 12 V6 architecture plus explicit Step 13 current ownership boundaries. It does not import GenSearch/Alice evidence and it does not infer private historical performance.

Key result:

- active phrase universe: **2332**;
- assigned phrases: **2313**;
- preserved unresolved phrases: **19**;
- final Step 12 structural units consumed: **168/168**;
- Step 13 query-family cases consumed: **21/21**;
- Step 13 effective pair accounting retained: **199**;
- implementation-relevant current URLs discovered from structural actions + link graph + Step 13: **59**;
- current URL live checks: **59/59 PASS**, critical fail-closed blockers: **0**;
- final Step 12 link rows accounted: **58/58**;
- frozen implementation links: **15**;
- unchanged defer/not-applicable link rows: **43**;
- new-page actions authorized by Step 14: **0**;
- destructive merge/delete/redirect/canonical actions authorized: **0**;
- new provider calls: **0**;
- provider cost in Step 14: **0.0 RUB**;
- GenSearch/Alice calls: **0**.

## 1. Structural baseline

The immutable baseline is `STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv` with content SHA `faaf7526709418d6c4b5a414b8cf2c73123403b6`.

Its 168-unit action distribution remains:

| Action | Units |
|---|---:|
| KEEP_EXISTING_STRUCTURE | 72 |
| ROUTE_TO_EXISTING_PAGE_AS_SUBTASK | 46 |
| DEFER_PENDING_EVIDENCE | 20 |
| NO_STANDALONE_PAGE | 15 |
| OUTSIDE_SCOPE_NO_ACTION | 7 |
| ADD_SECTION_OR_FAQ_TO_EXISTING | 6 |
| EXPAND_EXISTING_PAGE | 2 |
| **Total** | **168** |

The final Step 12 reconciliation already closed old proposed-new references: `new_page_actions=0`, `proposed_new_refs=0`. Step 14 therefore does not resurrect any intermediate `PROPOSED_NEW:*` record.

`STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE.tsv` uses a content-addressed baseline plus 21 explicit Step 13 boundary overlays rather than silently regenerating or manually mutating 168 previously accepted units.

## 2. Current-site freshness recheck

Before freezing architecture, Step 14 derived implementation-relevant URLs from:

1. Step 12 structural action primary/supporting/intended/current URLs;
2. Step 12 internal-link source and target URLs;
3. Step 13 primary/supporting ownership URLs;
4. Step 13 current-page evidence.

This produced **59 unique URLs**. The execution runner reread all 59 in the current run:

- `live_pass=59`;
- `live_fail_or_indeterminate=0`;
- `critical_fail_closed=0`.

Therefore no architecture unit is blocked by a missing or changed current URL at the Step 14 execution gate.

The detailed evidence is `STEP_14_CURRENT_URL_RECHECK.tsv`.

## 3. Step 13 ownership boundaries consumed

All **21/21** corrected Step 13 query-family cases are explicitly represented in `STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE.tsv`.

The freeze preserves the rule that related pages are not automatically cannibalizing pages. Specific task owners are kept primary and broader pages remain supporting where the evidence supports that relationship.

Two freshness corrections are mandatory and are consumed explicitly:

- **QF016** — `https://okno-msk.ru/okna-rehau/po-tipu-doma/panoramnoe-osteklenie-domov-i-kottedzhej/` is the primary current owner for panoramic windows in a private house; the generic panoramic page and broad private-house page remain supporting.
- **QF017** — `https://okno-msk.ru/verandy/panoramnye-okna-na-terrasu/` is the primary current owner for panoramic terrace glazing; the generic panoramic page and veranda hub remain supporting.

QF019 retains its explicit uncertainty boundary: the ordinary Search probe drifted toward outside/emergency-opening intent, so Step 14 keeps the narrow two-position troubleshooting article primary only for its narrow fault and does not invent a broader conclusion.

## 4. The 19 unresolved phrases

All **19/19** Step 12 `DEFER_UNRESOLVED` phrases were explicitly reviewed in `STEP_14_UNRESOLVED_REVIEW_PACKET.tsv`.

Result:

- `architecture_material=true`: **0**;
- `architecture_material=false`: **19**;
- silently assigned: **0**;
- silently dropped: **0**.

These phrases are malformed, underspecified, ambiguous numeric/entity phrases, or broad DIY/instruction wording that does not establish a stable separate user task or page responsibility. They remain preserved unassigned. This is not a claim that they have zero search demand; it is a decision that current Search-only evidence is insufficient to change the architecture because of them.

## 5. Internal-link architecture

The canonical Step 12 link graph contains **58 rows**:

- `IMPLEMENT`: **15**;
- `DEFER_SOURCE_CONTEXT_NOT_MATERIALIZED`: **6**;
- `DEFER_TARGET_CONTENT_GAP`: **7**;
- `NOT_APPLICABLE_NO_DISTINCT_SOURCE_CONTEXT`: **23**;
- `NOT_APPLICABLE_NO_DISTINCT_TARGET`: **7**.

Step 14 preserves all 15 existing implementation edges after current source/target URL recheck. The other 43 rows remain in their prior defer/not-applicable state.

Promotions from defer/not-applicable to `IMPLEMENT`: **0**.

The scoped limitation on `IL0041` is preserved: the repair-service → adjustment-guide handoff is valid only in adjustment/simple-handle contexts, not as a blanket broad DIY-repair link.

Detailed freeze: `STEP_14_INTERNAL_LINK_ARCHITECTURE.tsv`.

## 6. Safety and evidence boundaries

Step 14 authorizes no destructive action:

- merge: 0;
- delete: 0;
- redirect: 0;
- canonical consolidation: 0.

It also authorizes no new standalone page under the current evidence.

Private Yandex Webmaster query×URL history is unavailable in this job. Therefore this freeze does **not** claim:

- absence of historical URL competition;
- absence of historical owner switching;
- absence of historical cannibalization;
- absence of traffic/click/impression loss caused by competition.

The Step 13 base-public/current evidence boundary is preserved unchanged.

## 7. Provider / AI boundary

Step 14 required no fresh paid provider evidence after the pre-step review and current-site recheck:

- ordinary Search Bridge calls: 0;
- Webmaster Bridge calls: 0;
- other provider calls: 0;
- provider cost: 0.0 RUB;
- GenSearch/Alice calls: 0.

Step 15 and Step 16 were not executed during Step 14.

## 8. What is frozen

The Search-only baseline for the next stage is now:

`STEP12 V6 structural architecture`
`+ corrected Step13 ownership/support boundaries`
`+ 59/59 current-site URL existence check`
`+ 19/19 unresolved explicit non-material preservation`
`+ 58/58 internal-link accounting`
`= STEP14 SEARCH-ONLY ARCHITECTURE FREEZE`

Any later AI-search evidence must be compared against this baseline. It must not rewrite the baseline retroactively without a separately evidenced correction/reopen decision.

## 9. Limitations

This is an architecture freeze, not a performance audit and not an AI-search audit.

It establishes the current Search-only page/task/link responsibility model. It does not establish which pages have the best historical traffic performance and it does not yet say how Yandex AI/GenSearch answers differ from ordinary Search.

## 10. Next step

**Step 15 is allowed only to enter its own pre-step evidence/method review. Step 15 is not executed by this acceptance.**

Step 15 must start from this frozen Search-only baseline. Step 16/AI evidence remains prohibited until the Step 15 gate has been completed and separately authorized as required by the workflow rules.
