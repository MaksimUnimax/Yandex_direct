# KW-001 / OKNO-MSK — STEP 01 ACCEPTANCE

Date: 2026-08-28
Status: **REOPENED / PREVIOUS SINGLE-PASS PASS SUPERSEDED**

## Why the previous PASS was reopened

The first Step-01 pass used ChatGPT public web and reviewed 18 representative pages. At that point it concluded that a representative inventory was sufficient and that Work/Codex was not required.

A later controlled three-pass comparison disproved that conclusion as a general execution rule.

Observed test evidence:

```text
CHATGPT PUBLIC WEB
= 18 representative OPENED_READ pages
= found material GEO district landing + Balashikha public subdomain
= weaker than Codex Work on deep internal/repeated-template coverage

CODEX WORK
= 56 OPENED_READ pages
= strongest deep internal family/template coverage
= found profiles, house-series templates, door variants, balcony geometry,
  service/finance/accessory/article families at much greater depth
= did NOT reach LOCAL_GEO/subdomain family through checked internal navigation

CODEX DESKTOP/APP
= 5 OPENED_READ pages
= navigation exposed useful additional candidate axes such as sash count,
  object/room, house-series, balcony modes, accessories/services/prices/content
= browser timeouts prevented representative validation
= correctly returned DISCOVERY_SATURATION_REACHED = false
```

Therefore:

```text
REPRESENTATIVE_SINGLE_SURFACE_PASS = NOT SUFFICIENT AS DEFAULT
INTERNAL_NAVIGATION_SATURATION != COMPLETE_PUBLIC_SITE_SATURATION
DISCOVERED_LINK_ONLY != OPENED_READ
```

Detailed comparison:

`STEP_01_MULTI_PASS_DISCOVERY_CROSSCHECK.md`

Canonical current method:

`../../WORKING_RUNBOOK_FOR_CHATGPT.md` → `STEP 1 — Site/content discovery to CROSS-CHANNEL saturation`

---

## Purpose of the reopened gate

**RULE**  
Do not begin Wordstat/provider acquisition until the three discovery reports have been merged into one provenance-preserving factual inventory and business/page model.

**PURPOSE**  
Prevent later semantic collection and page mapping from being based on only one tool's blind spots.

**EVIDENCE**  
The real `okno-msk.ru` test showed complementary misses: Codex Work found much deeper internal architecture but missed real GEO/subdomain assets; ChatGPT public web found those GEO assets but did not read the internal repeated families as deeply.

**FAILURE IF IGNORED**  
A premature Step-02 seed plan can omit real business/page families or treat an existing page job as missing, which can later produce:

```text
missing seed directions
incomplete semantic core
false NEW_PAGE recommendations
false merge/cannibalization hypotheses
missed existing URL targets
```

**REVIEW TRIGGER**  
The gate may be simplified in future only if a validated single acquisition mechanism proves reliable complete coverage of both deep internal architecture and the relevant public URL universe for the site class being processed.

---

## Evidence already preserved

```text
TEST_ORDER.md = frozen before provider acquisition
SITE_PAGE_INVENTORY.md = original ChatGPT 18-page pass
BUSINESS_AND_PAGE_MODEL.md = original analyst model, now provisional pending merge
OPEN_QUESTIONS_FOR_CLIENT.md = client clarification set + frozen mock assumptions
STEP_01_MULTI_PASS_DISCOVERY_CROSSCHECK.md = three-pass comparison and method evidence
```

No Wordstat, ordinary Search API, Search batch or GenSearch requests were made before this reopening.

---

## New Step-01 exit criteria

Step 01 returns to PASS only after all are true:

```text
all three discovery reports compared = true
union URL inventory created = true
per-URL provenance preserved = true
OPENED_READ vs DISCOVERED_LINK_ONLY vs INFERRED_TEMPLATE_FAMILY separated = true
material unique families from every pass retained = true
material weak-state families representative-read where technically possible = true
merged business/page model rebuilt from union = true
open client questions updated from merged model = true
cross-channel saturation decision recorded = true
seed directions re-derived from merged model = true
Wordstat requests before re-freeze = 0
Search API requests before re-freeze = 0
GenSearch requests before re-freeze = 0
```

New acceptance marker:

```text
KW001_OKNO_MSK_STEP_01_CROSS_CHANNEL_PASS = true
```

Until that marker exists:

```text
STEP_02_WORDSTAT_START = FORBIDDEN
```

## Next action

Create the merged factual inventory and merged business/page model from:

```text
ChatGPT public-web pass
+ Codex Work deep pass
+ Codex desktop/app control pass
```

using the merge algorithm defined in the working runbook.
