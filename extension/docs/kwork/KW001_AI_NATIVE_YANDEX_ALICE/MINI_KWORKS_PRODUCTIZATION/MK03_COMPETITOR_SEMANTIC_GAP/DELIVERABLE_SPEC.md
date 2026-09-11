# MK03 — DELIVERABLE SPEC

Status: **PHASE 4 PASS CANDIDATE / CLIENT PACKAGE CONTRACT**

## 1. Physical package

Base MK03 V1 client delivery is:

```text
1 XLSX
+ 1 ANALYTICAL PDF
+ 1 SHORT HANDOFF MESSAGE
```

There is no separate implementation-TZ PDF in base MK03. A full target architecture, phrase→page map or implementation-ready SEO TZ belongs to neighbouring products.

The physical file count does not dictate a fixed sheet count or PDF page count.

## 2. Sold client result

The package must let a recipient understand and inspect:

```text
WHERE THE REAL YANDEX SEARCH COMPETITION WAS OBSERVED
→ WHICH COMPETITOR PAGES CARRIED MATERIAL EVIDENCE
→ WHAT NEW IN-SCOPE DIRECTIONS THOSE PAGES EXPOSED
→ WHICH DIRECTIONS HAVE WORDSTAT DEMAND
→ WHICH EXACT QUERY→COMPETITOR CLAIMS WERE CURRENT-SEARCH TESTED
→ WHAT THE CLIENT ALREADY COVERS
→ WHAT IS A CONFIRMED GAP / OFF-SCOPE / HOLD
→ WHAT BOUNDED OPPORTUNITY FOLLOWS
```

Aggregate counts without inspectable rows are not an acceptable product.

## 3. XLSX role

The workbook is the detailed evidence and decision surface. It must expose equivalent logical views for the following information. Exact sheet names and sheet count may follow the generator/design convention.

### A. Start / guide

Plain-language explanation of:
- site and target region;
- what was checked;
- evidence boundaries;
- meaning of key states;
- where detailed evidence and final conclusions live.

### B. Yandex search competitors

For material competitor discovery evidence, expose enough fields to understand:
- search family / representative query;
- region;
- competitor domain;
- observed result URL/page;
- competitor/result routing type where useful;
- current Search evidence state/source;
- notes/uncertainty where material.

Client-supplied hints must not be indistinguishable from Yandex-observed organic competitors.

### C. Evidence-bearing competitor pages

Expose material competitor pages used as acquisition evidence, including:
- domain / URL;
- page type/topic;
- visible product/service/use-case axes used for discovery;
- which discovery observation led to the page;
- which candidate directions were derived;
- evidence limitations.

A competitor page topic must not be presented as proof that the page ranks for every derived exact query.

### D. Competitor-derived candidate / provenance ledger

For each material candidate direction or phrase identity, preserve:
- normalized identity;
- source competitor/page/topic lineage;
- whether lineage is new even if the keyword identity already existed;
- business/scope state;
- sanitation/duplicate state;
- downstream evidence links/state.

```text
NEW PROVENANCE != NEW KEYWORD ID
```

### E. Wordstat demand validation

Expose sufficient demand evidence for genuinely new probes:
- probe/seed;
- returned candidate or normalized identity;
- demand/frequency fields actually used;
- region/access context where relevant;
- sanitation/scope decision;
- final candidate routing.

Raw Wordstat rows must not be silently copied as final accepted keywords.

### F. Tested query→competitor Search matrix

Expose only actually tested exact-query claims as Search-tested, with enough fields to reconstruct:
- exact query;
- region;
- competitor/domain/URL tested;
- observed visibility/result evidence;
- observation date/evidence reference;
- resulting decision use.

Unprobed page-topic-derived candidates must remain distinguishable from this matrix.

### G. Client coverage + final gap decision

For every material candidate, expose:
- candidate identity/direction;
- current client coverage evidence or uncertainty;
- final state;
- reason;
- relevant competitor/Wordstat/Search lineage;
- resolving evidence for HOLD where applicable.

Canonical visible terminal states are equivalent to:

```text
CONFIRMED_GAP
ALREADY_COVERED
REJECT_OFF_SCOPE
HOLD_EVIDENCE
```

### H. Opportunities / next actions

For confirmed gaps and material already-covered findings where useful, expose the bounded consequence:
- content/topic opportunity;
- strengthen current coverage;
- possible page/section opportunity;
- route to another mini-kwork/product;
- no action / keep where appropriate;
- exact uncertainty when no structural conclusion is justified.

Do not silently convert every confirmed gap into CREATE PAGE.

## 4. Analytical PDF role

The PDF is the recipient-readable synthesis, not a dump of all rows and not a substitute for the workbook.

It should explain, in plain language:

1. scope, site and region;
2. what Yandex evidence was used and what was not claimed;
3. the principal actual organic competitors and where they intersect the client's search demand;
4. material competitor pages/directions that exposed additional demand;
5. which new directions were supported by Wordstat;
6. representative exact Search-tested examples, explicitly separated from page-topic inference;
7. the gap picture: confirmed gaps, already-covered directions, rejected/off-scope and unresolved evidence where material;
8. the most important bounded opportunities and why they matter;
9. positive keep/already-covered findings where they validate current coverage;
10. limitations and what would be required for claims outside MK03 scope;
11. a clear pointer to the XLSX for row-level evidence.

The PDF must not imply a full reverse-domain keyword universe, full site architecture, implementation-ready TZ, traffic/revenue estimate or Google/AI result.

## 5. Handoff message role

The short handoff should tell the client:
- what files are included;
- where the detailed evidence is;
- where the conclusions are;
- the most important finding categories in concise client language;
- which items remain uncertain, if any;
- that a gap/opportunity is not automatically an implementation decision.

Internal repository filenames, Step IDs, commit hashes and QA codes are omitted from ordinary client prose.

## 6. Required cross-artifact consistency

The same material entity may not receive contradictory states across workbook and PDF.

At minimum reconcile:

```text
COMPETITOR IDENTITY / TYPE
COMPETITOR PAGE / TOPIC
CANDIDATE IDENTITY
WORDSTAT DEMAND STATE
SEARCH-TESTED STATE
CLIENT COVERAGE STATE
FINAL GAP STATE
OPPORTUNITY / HOLD REASON
```

Summary totals must be derivable from canonical row authorities. No client artifact may introduce a conclusion absent from the canonical data.

## 7. No-silent-drop requirement

The workbook must allow accounting from acquired material candidates to final terminal states, including deterministic duplicate collapse with preserved lineage.

A row may disappear from a final client view only because a canonical rule deterministically merged/routed it and the provenance/accounting remains reconstructable.

## 8. Spreadsheet physical QA contract

For the exact final XLSX:
- open/read all intended sheets and visible client cells;
- verify headers, filters, freeze panes and widths/readability where applicable;
- verify formulas/references if any;
- inspect raw workbook XML/table metadata when needed to catch structural defects not visible through a dataframe read;
- ensure no broken formulas, hidden critical columns, clipped primary fields or accidental internal-only data leakage;
- re-run checks after any final file change.

Do not hard-code a universal sheet count or row count as the product definition.

## 9. PDF physical QA contract

For the exact final PDF:
- parse/extract text enough to detect missing/truncated content;
- render every final page;
- inspect every rendered page for clipping, overlap, blank/missing pages, unreadable tables, broken fonts and orphaned headings;
- any byte-level change to the final PDF invalidates earlier render QA and requires a new final render inspection.

Do not hard-code a universal PDF page count.

## 10. Recipient acceptance tasks

Without repository access, a recipient must be able to answer:

1. Which sites were actually observed as Yandex organic competitors and for what search families?
2. Which competitor page exposed a selected new direction?
3. Was a selected exact query→competitor relation actually Search-tested, or only derived from page-topic evidence?
4. Is a selected candidate a confirmed gap, already covered, off-scope or evidence-required?
5. What client opportunity follows and why?
6. What remains uncertain and what evidence would resolve it?

If the package cannot answer these questions, it fails even if the files open successfully.
