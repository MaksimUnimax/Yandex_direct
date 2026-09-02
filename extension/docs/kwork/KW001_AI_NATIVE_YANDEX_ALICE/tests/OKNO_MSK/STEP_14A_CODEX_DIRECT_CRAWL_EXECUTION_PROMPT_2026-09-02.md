# Codex prompt — OKNO_MSK Step 14A direct crawl execution

Date: 2026-09-02
Status: **CURRENT OWNER-DIRECTED EXECUTION PROMPT**

The objective now is the actual site crawl and topology evidence, not more framework work.

Repository: `MaksimUnimax/Yandex_direct`
Branch: `roadmap/kwork-productization-2026-08-28`
Site: `https://okno-msk.ru/`

Your last reported local state:

```text
LOCAL_HEAD_QUALIFICATION_START = 4dce8e4c1cbc5495e2371b630603718c35a3f62f
REMOTE_HEAD_AFTER_FETCH_QUALIFICATION = a3e816dc736e65b25a4c6734827b17d15d1b2aa5
SYNC_MODE_QUALIFICATION = SAFE_MERGE
LOCAL_HEAD_AFTER_SYNC_QUALIFICATION = d73010623467506e67ac6ebe7247efc4bd8377fa
STEP15_EXECUTED = false
```

## Owner intent

Do not spend another turn merely reporting that qualification rules are present or that qualification has not started.

The required outcome is:

```text
ACTUALLY CRAWL okno-msk.ru
-> collect the current public URL universe
-> collect literal current same-site <a href> edges
-> reconcile against Step 12/13/14 known URLs
-> verify the 15 planned Step-14 IMPLEMENT edges
-> persist and push the evidence
```

## Execution instruction

1. Fetch/integrate the latest remote branch safely only if necessary. Do not redo already-completed repository analysis unless the remote materially changed.

2. Quarantine/remove the seven stale uncommitted final-named artifacts from the previous invalid run. They must not be published as current final evidence.

3. Use the existing runner `step14a_codex_site_discovery.py`, fixing or replacing it as needed. The implementation mechanism is not the goal. If the current runner remains unreliable, replace the problematic mechanism with a simpler bounded implementation rather than spending another cycle building framework around it.

4. Perform Q1-Q4 as immediate smoke checks inside this same execution, not as a separate reporting milestone. Do not stop merely because Q1-Q4 completed successfully. If they pass, continue directly into the full crawl in the same work session.

5. Network/fetch behavior must be fail-soft per URL:
   - explicit per-request timeout;
   - bounded retries;
   - a failed/slow URL is recorded as failed or indeterminate and the crawl continues;
   - one problematic URL must not stop the whole site crawl;
   - use a global bound/watchdog so the process terminates;
   - same-site HTML only for the crawl graph;
   - sitemap(s) are an additional discovery source, not the sole source.

6. Crawl from `https://okno-msk.ru/` through literal same-site HTML `<a href>` links. Also parse public sitemap(s). Normalize URLs deterministically and preserve discovery source/provenance.

7. Produce the actual required evidence:

`STEP_14A_CODEX_SITE_DISCOVERY_URLS.tsv`
`STEP_14A_CODEX_INTERNAL_LINK_GRAPH.tsv`
`STEP_14A_CODEX_PAGE_PROFILE_LEDGER.tsv`
`STEP_14A_CODEX_UPSTREAM_RECONCILIATION.tsv`
`STEP_14A_CODEX_REQUIRED_EDGE_VERIFICATION.tsv`
`STEP_14A_CODEX_QA.json`
`STEP_14A_CODEX_REPORT.md`

8. Required URL/page fields include at least:
   - normalized URL;
   - discovery source: crawl / sitemap / upstream or combination;
   - HTTP status/fetch state;
   - final URL/redirect evidence;
   - title;
   - H1;
   - crawl depth where observable;
   - incoming internal-link count;
   - outgoing internal-link count;
   - sitemap membership;
   - fetch/error state.

9. The literal link graph must contain at least:
   - source URL;
   - target URL;
   - normalized target;
   - anchor text where available;
   - source fetch state;
   - target/final state;
   - current literal `<a href>` provenance.

10. Reconcile newly discovered current URLs against the Step 12/13/14 upstream universe. Do not make semantic ownership decisions yourself. Surface every URL absent upstream for ChatGPT review.

11. Verify all 15 planned Step-14 IMPLEMENT edges exactly once as one of:

```text
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
```

`AS_IS_PRESENT` requires literal normalized current HTML `<a href>` evidence. Source/target liveness or semantic fit is not enough.

12. Do not execute Step 15. Do not use paid Yandex APIs, GenSearch or Alice. Do not mutate the public website.

13. Commit the crawler changes plus valid Step-14A artifacts and NORMAL-PUSH them to `origin roadmap/kwork-productization-2026-08-28`. No force push.

14. If the full crawl still cannot complete, do not return only a prose description again. Commit and normal-push the actual runner plus the smallest reproducible diagnostic and terminal-state report so ChatGPT can inspect the code directly.

## Final report

Return:

```text
FINAL_COMMIT_SHA
PUSH_STATUS
CRAWLER_SCRIPT_PATH
Q1_STATUS
Q2_STATUS
Q3_STATUS
Q4_STATUS
FULL_CRAWL_EXECUTED = true/false
FULL_RUN_ID
TOTAL_NORMALIZED_CURRENT_URLS
CRAWL_DISCOVERED_URLS
SITEMAP_DISCOVERED_URLS
CURRENT_URLS_NOT_IN_UPSTREAM
FETCH_FAILED_OR_INDETERMINATE
BROKEN_INTERNAL_TARGETS
ORPHAN_CANDIDATES
PLANNED_IMPLEMENT_EDGE_BASELINE = 15
AS_IS_PRESENT
AS_IS_ABSENT_PLANNED
BLOCKED_OR_UNVERIFIED
NOT_APPLICABLE
EDGE_ACCOUNTING = 15/15
QA_STATUS
BLOCKERS_OR_LIMITATIONS
STEP15_EXECUTED = false
```

Do not claim Step 14 is finally accepted. ChatGPT performs the semantic reconciliation and final acceptance after GitHub readback.