# MK03 STEP 03 — EVIDENCE-BEARING COMPETITOR PAGE INSPECTION

## Purpose
Inspect competitor pages that actually carried useful Search evidence and extract only the public topic signals needed to find missed demand.

## Why this step exists
Domain-level competitor presence does not reveal which concrete page/topic created a new demand hypothesis.

## Inputs
Accepted competitor discovery register and observed competitor URLs.

## Required evidence
Public competitor page content plus the Yandex query/result observation that exposed the page.

## Method
For relevant URLs record:
- competitor domain and URL;
- exposing query/family and observed order when available;
- page type;
- Title/H1 when available;
- material product/service/use-case/topic axes;
- material headings/navigation directions needed for gap discovery;
- observation date.

Inspect only pages with decision value. Do not expand into technical/backlink/traffic/conversion audit.

## Outputs
`COMPETITOR_PAGE_EVIDENCE_REGISTER`.

## Source authority
Parent Step5A sections 5A.2/claim boundary; local scope controls.

## Known failures / root causes
- page wording treated as exact-query ranking proof;
- entire competitor site crawled without information-gain purpose;
- deep audit scope creep.

## Non-repeat controls
`PAGE TOPIC != RANKING`; only evidence-bearing public elements are captured.

## Claim boundary
Page content proves that the page contains/targets a topic; exact query visibility remains a separate Search fact.

## Unknown behavior
If page content cannot be read reliably, preserve missing-page-evidence state; do not infer unseen headings/content.

## PASS gate
Every retained page has source/query lineage and a clear reason it matters; zero ranking claims sourced only from page text.

## Client-facing meaning
“We show which competitor pages led to new ideas, not just a list of domains.”
