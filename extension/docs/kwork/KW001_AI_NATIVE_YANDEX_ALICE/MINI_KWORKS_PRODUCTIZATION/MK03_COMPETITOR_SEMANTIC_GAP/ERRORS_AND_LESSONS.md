# MK03 — ERRORS AND LESSONS

Status: **ACTIVE / PHASE 3 FAILURE EXTRACTION**

This ledger carries only reusable failure classes into MK03. Concrete OKNO_MSK domains, queries, counts and verdicts remain Level-2 evidence.

Each class follows:

```text
WHAT FAILED
→ ROOT CAUSE / FALSE ASSUMPTION
→ CORRECTED RULE
→ ENFORCEMENT
→ REGRESSION PASS
```

## F01 — competitor page text treated as exact ranking evidence

**Failure:** analyst sees a topic/phrase on a competitor page and reports that the competitor ranks for that exact query.

**Root cause:** page content and Search visibility were collapsed into one evidence type.

**Corrected rule:** `PAGE TOPIC != EXACT QUERY RANKING`. Exact query→competitor visibility requires direct current Search evidence for that query/region.

**Enforced in:** Steps 03, 06, 09.

**PASS:** zero exact ranking claims sourced only from page text.

## F02 — competitor visibility treated as automatic client-keyword acceptance

**Failure:** anything a competitor ranks/discusses is accepted into the client result.

**Root cause:** competitor signal was used as substitute for demand, business fit and intent.

**Corrected rule:** competitor signal is a probe; acceptance requires appropriate Wordstat demand, client scope/business fit and material Search evidence where the decision needs it.

**Enforced in:** Steps 04–07.

**PASS:** every material candidate ends in CONFIRMED_GAP / ALREADY_COVERED / REJECT_OFF_SCOPE / HOLD_EVIDENCE with evidence basis.

## F03 — endless recursive competitor expansion

**Failure:** more domains/pages/headings always create more probes and provider calls.

**Root cause:** no information-gain stop condition.

**Corrected rule:** expand only while material novelty or unresolved coverage remains; stop on diminishing information gain.

**Enforced in:** Steps 02–05.

**PASS:** explicit stop rationale; no fixed quota or recursive crawl loop.

## F04 — competitor acquisition loses provenance during merge

**Failure:** accepted phrases remain but their competitor page/seed/Wordstat lineage disappears.

**Root cause:** competitor evidence was kept in a decorative side table rather than a union-compatible analytical lineage.

**Corrected rule:** preserve source competitor/domain/page/query/topic/seed/provider lineage through normalization and gap decision.

**Enforced in:** Steps 03–07.

**PASS:** every accepted competitor-derived candidate can be traced back to the evidence-bearing page/topic and acquisition path.

## F05 — deep competitor audit silently enters base scope

**Failure:** backlink, technical, Core Web Vitals, schema, traffic, ads or conversion analysis is performed because competitor domains are already open.

**Root cause:** evidence collection scope followed tool availability rather than sold result.

**Corrected rule:** inspect only evidence needed for search-competitor and gap decisions. Deep competitor audit requires separately sold/authorized scope.

**Enforced in:** General Rules; Steps 02–03.

**PASS:** no unsupported audit dimensions in base outputs.

## F06 — third-party reverse-domain provider becomes hidden dependency

**Failure:** method cannot run without Semrush/Ahrefs-style competitor keyword databases or claims their full-universe coverage without such evidence.

**Root cause:** industry-practice tooling was confused with required Yandex-native base method.

**Corrected rule:** base MK03 is executable with Yandex Search + public pages + Wordstat; external reverse-domain data is optional enrichment only.

**Enforced in:** Steps 02, 04, 05.

**PASS:** base execution does not require third-party reverse-domain access and makes no full-domain keyword-universe claim.

## F07 — competitor-derived additions remain outside the common analytical result

**Failure:** new competitor phrases are shown in a side worksheet but are never normalized, reconciled or classified against client coverage.

**Root cause:** acquisition lineage was mistaken for a separate semantic truth silo.

**Corrected rule:** every new occurrence re-enters normalization/sanitation and common candidate accounting.

**Enforced in:** Steps 05–07.

**PASS:** no accepted side-list orphan rows.

## F08 — client receives aggregate counts only

**Failure:** report says “N competitors / N gaps” without showing what was found and why.

**Root cause:** QA checked totals/schema but not recipient usefulness.

**Corrected rule:** expose inspectable competitor, page, new direction, demand, tested visibility, client coverage and gap state at useful depth.

**Enforced in:** Step 09 and QA_AND_RELEASE.

**PASS:** recipient can trace material results without repository knowledge.

## F09 — MK03 discovery baseline expands into a free full MK01 rebuild

**Failure:** before competitor analysis, executor rebuilds the client's entire semantic core.

**Root cause:** “need representative queries” was interpreted as “need complete semantic universe”.

**Corrected rule:** build only the smallest representative in-scope baseline sufficient to discover search competitors and material gaps; expand only for a named uncovered direction.

**Enforced in:** Steps 00–01.

**PASS:** baseline purpose and stop rationale are explicit; no full-core completeness claim.

## F10 — client-supplied competitor list treated as organic-search truth

**Failure:** offline/business competitors are accepted without Yandex evidence.

**Root cause:** business rivalry and Search competition were conflated.

**Corrected rule:** supplied names are hints; MK03 competitor status requires current regional organic Yandex evidence.

**Enforced in:** Step 02.

**PASS:** every accepted search competitor has a discovery evidence locator.

## F11 — raw Wordstat rows appended directly to result

**Failure:** competitor-derived provider rows inflate the candidate set with duplicates/noise.

**Root cause:** RAW evidence and analytical identities were conflated.

**Corrected rule:** `RAW → NORMALIZE → SANITIZE → RECONCILE`. `NEW PROVENANCE != NEW KEYWORD ID`.

**Enforced in:** Step 05.

**PASS:** raw/normalized/sanitized counts reconcile; duplicate lineage is preserved without duplicate analytical rows.

## F12 — confirmed gap automatically becomes CREATE-page recommendation

**Failure:** missing topic is converted directly into new URL/architecture.

**Root cause:** semantic absence and page-architecture evidence were collapsed.

**Corrected rule:** MK03 may state bounded page/topic/section opportunity, but does not assign final page ownership or implementation-ready CREATE without MK02/MK04/MK05 evidence.

**Enforced in:** Step 08.

**PASS:** zero automatic new-page decisions from gap state alone.

## F13 — selective Search overgeneralized to unprobed rows

**Failure:** a family anchor is checked and all related phrases are reported as Search-confirmed.

**Root cause:** SELECTIVE_DECISION_SERP was misread as permission to generalize exact observations.

**Corrected rule:** exact observation remains exact. Unprobed rows may inherit analytical context only with explicit non-Search-confirmed state.

**Enforced in:** Step 06.

**PASS:** tested vs untested distinction is visible and accurate.

## F14 — stale client-site inventory creates false gap

**Failure:** an old inventory says a topic/page is absent, so MK03 reports a gap that the current site already covers.

**Root cause:** historical inventory absence was treated as current site absence.

**Corrected rule:** current coverage decisions require current public-site reconciliation sufficient for the claim.

**Enforced in:** Steps 00, 07.

**PASS:** material gap decisions have current coverage evidence or HOLD_EVIDENCE.

## F15 — tested queries are presented as the competitor's full keyword universe

**Failure:** bounded observed visibility becomes “all competitor keywords”.

**Root cause:** direct observation coverage was overstated.

**Corrected rule:** MK03 reports tested visibility and competitor-derived gaps, never a complete reverse-domain keyword universe unless a separately authorized dataset genuinely supports it.

**Enforced in:** Steps 06, 09.

**PASS:** full-universe overclaim = 0.

## F16 — structural opportunity wording leaks neighbouring-product scope

**Failure:** report provides final target URL, ownership, complete architecture or implementation-ready TZ although MK03 evidence only proves a gap.

**Root cause:** useful next-step interpretation was allowed to become silent MK02/MK05 delivery.

**Corrected rule:** opportunity notes remain bounded: content/page-type/section direction, evidence meaning, uncertainty and recommended next decision. No full target architecture or ready implementation ticket.

**Enforced in:** Step 08; DELIVERABLE_SPEC.

**PASS:** neighbouring-product leakage = 0.

## F17 — internal research chronology replaces client explanation

**Failure:** client report exposes Step IDs, provider-call logs, repo filenames and state-machine jargon instead of useful findings.

**Root cause:** audit traceability and recipient communication were merged.

**Corrected rule:** keep provenance durable internally; client-facing text explains what was found, why it matters, what is confirmed and what remains uncertain.

**Enforced in:** Step 09.

**PASS:** internal-token/client-language QA passes and recipient can use the result without repository context.
