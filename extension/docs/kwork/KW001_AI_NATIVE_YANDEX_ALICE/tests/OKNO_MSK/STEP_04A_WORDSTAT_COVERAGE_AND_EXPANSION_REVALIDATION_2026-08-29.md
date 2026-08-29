# KW-001 / OKNO-MSK — WORDSTAT COVERAGE AND EXPANSION REVALIDATION

Date: 2026-08-29  
Status: **COMPLETE / ACQUISITION COVERAGE SUFFICIENT FOR ROW-LEVEL CLEANUP**

## Purpose and authority

This is a fresh revalidation after the repaired Step 03R produced a complete reusable 18-seed first-pass dataset. It does not silently reuse the historical Step-05 sufficiency conclusion.

The question is narrow: before row-level semantic cleanup, do the complete first-pass data plus the four already preserved targeted Wordstat probes provide sufficient acquisition breadth, or is another Wordstat request materially justified now?

This document does **not** decide final keyword retention, grouping, page ownership, or Search/AI architecture.

## Inputs

Complete repaired first pass:

```text
18/18 seeds complete
results rows = 2153
association rows = 262
total preserved + verified provider rows = 2415
```

Preserved targeted probes:

```text
P2-01 оконная фурнитура
P2-02 панорамные окна
P2-03 остекление балкона с выносом
P2-04 окна для частного дома
```

Probe accounting:

```text
P2-01 results=200 associations=17 rows=217
P2-02 results=200 associations=16 rows=216
P2-03 results=5 associations=16 rows=21
P2-04 results=78 associations=18 rows=96
TOTAL results=483 associations=67 rows=550
```

No new Yandex provider request was made during this revalidation. Additional provider cost = 0 RUB.

## Comparison method

For the quantitative overlap check, every probe row was compared by exact normalized phrase equality against the complete 2415-row first-pass corpus, including both first-pass `results` and first-pass `associations`.

Important limits:

```text
exact mismatch != unique phrase after cross-probe dedupe
exact mismatch != new semantic topic
association != automatically accepted keyword
high count != automatically a new page or acquisition seed
low frequency != proof of irrelevance
```

The overlap numbers therefore measure exact string reuse against the complete first pass. Information gain is then judged separately by whether the probes exposed materially useful vocabulary/user-task directions for later row-level review.

## Exact overlap result

| Probe | Probe rows | Exact matches in 2415-row base | Rows with no exact base match |
|---|---:|---:|---:|
| P2-01 `оконная фурнитура` | 217 | 2 | 215 |
| P2-02 `панорамные окна` | 216 | 7 | 209 |
| P2-03 `остекление балкона с выносом` | 21 | 3 | 18 |
| P2-04 `окна для частного дома` | 96 | 5 | 91 |
| **TOTAL** | **550** | **17** | **533** |

Interpretation boundary:

`533` means only that 533 rows from the four probe files are not an exact phrase match to any row of the complete first-pass corpus. It must **not** be reported as “533 new topics” and has not been asserted here as 533 cross-probe-unique phrases.

## Probe-by-probe information gain

### P2-01 — `оконная фурнитура`

Original purpose: test whether the literal first-pass accessories vocabulary under-sampled the language people use for window hardware/components.

Revalidation: **INFORMATION GAIN CONFIRMED**.

Material vocabulary exposed beyond the literal accessories seed includes:

```text
purchase / shop / Moscow intent
brands such as Vorne, Roto, Maco, Siegenia, GU, Internika
selection / reviews / ratings
repair / regulation / replacement
parts and mechanisms
maintenance / lubrication
PVC-specific fittings language
```

This is useful acquisition evidence for the existing accessories/customisation business family. Standalone commercial priority remains unresolved and must be handled later as KEEP/REVIEW/EXCLUDE decisions, not assumed now.

### P2-02 — `панорамные окна`

Original purpose: test whether `французские окна` missed broader panoramic application/design vocabulary and user jobs.

Revalidation: **INFORMATION GAIN CONFIRMED**.

Material vocabulary includes:

```text
private / country house applications
apartments plus adjacent real-estate contamination
Moscow purchase / price / turnkey / order intent
floor-to-ceiling / sliding / aluminium / plastic / corner / door combinations
balcony / loggia / terrace / veranda use cases
heating / convectors / dimensions / installation / insulation
```

The probe materially broadens the language around the already discovered French/panoramic business family, while also introducing noise that must be removed row by row.

### P2-03 — `остекление балкона с выносом`

Original purpose: test a known engineering subfamily surfaced below the broad balcony seed.

Revalidation: **NARROW INFORMATION GAIN CONFIRMED / NO RECURSIVE WORDSTAT EXPANSION NEEDED NOW**.

Direct provider results were sparse but valid and confirmed a real narrow engineering family around:

```text
остекление балкона с выносом
вынос подоконника
Moscow wording
welding / engineering wording
Provedal wording
```

The complete site/business model already contains balcony engineering/extension as a real family. This probe is sufficient as acquisition evidence; additional Wordstat recursion is not justified solely by this branch.

### P2-04 — `окна для частного дома`

Original purpose: test a distinct application/user-job family that appeared only incidentally in the first acquisition design.

Revalidation: **INFORMATION GAIN CONFIRMED**.

Material vocabulary includes:

```text
sizes / standards
selection / comparison / profile choice
PVC purchase and price intent
boiler-room / gas-boiler technical requirements
panoramic applications
wood / aluminium material alternatives
floor / form / room-specific use cases
```

The exact root `окна для частного дома` was not found in the complete first-pass corpus during the revalidation search. The probe therefore filled a genuine acquisition gap.

Association `остекление коттеджей` remains vocabulary evidence only. The current business model does not prove a separate standalone cottage-glazing product family, so it remains for later review instead of automatically triggering another provider request.

## Recheck of deferred expansion candidates

The historical deferred candidates were re-evaluated against the repaired complete first-pass data plus the four probes.

```text
остекление террасы
```
Covered sufficiently for acquisition by the deep `остекление веранды` result family and P2-02 panoramic/terrace language. Whether veranda and terrace need different pages is a later ordinary Yandex Search boundary question.

```text
панорамное остекление балкона
```
Already present directly in the broad balcony dataset and again in P2-02 vocabulary evidence. No new Wordstat call is justified now.

```text
монтаж окон
```
The installation family is deeply sampled by `установка пластиковых окон`; broader `монтаж окон` is potentially ambiguous and is better resolved later by Search/user-task evidence than by broadening acquisition now.

```text
регулировка окон пвх
```
Repair/regulation vocabulary is represented through repair and fittings evidence. Standalone repair/regulation priority remains a business/page question, not a current acquisition hole.

```text
москитные сетки на пластиковые окна
```
Already represented repeatedly in the broad PVC, installation, price and accessories/fittings evidence. No new call justified now.

```text
окна пвх
```
Broad near-synonym family is already heavily represented through the main PVC seed and associations. Another broad probe is more likely to add duplication/noise than resolve a concrete uncertainty.

```text
стеклопакет
```
Appears repeatedly as association vocabulary, but standalone glass-unit sales are not established as a frozen business priority. Expanding it now could widen the scope beyond the order; keep for REVIEW/business/Search resolution.

```text
оконный завод
```
Manufacturer/trust language is already represented by the manufacturer seed and manufacturer associations. Whether “factory/manufacturer” deserves separate page treatment is a later Search/page-boundary decision.

```text
остекление коттеджей
```
Retain as REVIEW vocabulary from P2-04. Current evidence does not justify an automatic new Wordstat recursion before cleanup.

## Coverage verdict

```text
ACQUISITION_COVERAGE_VERDICT = SUFFICIENT
ADDITIONAL_WORDSTAT_REQUESTS_REQUIRED_NOW = 0
ADDITIONAL_PROVIDER_COST_RUB = 0
ROW_LEVEL_CLEANUP_ALLOWED = true
FINAL_SEMANTIC_SET_COMPLETE = false
PAGE_ARCHITECTURE_COMPLETE = false
```

Why `SUFFICIENT`:

1. The repaired first pass now provides the complete 2415-row evidence base that was missing when the historical Step-05 conclusion was made.
2. All four targeted probes produced measurable information gain against that complete base; only 17 of 550 probe rows are exact matches to base rows.
3. The probes filled the intended vocabulary/application gaps: hardware, panoramic, balcony extension and private-house demand.
4. Previously deferred broad roots are either already represented strongly enough for acquisition or are better resolved by row-level cleanup, business scope, or ordinary Yandex Search rather than another broad Wordstat call.
5. No material business family in the current site/business model has been shown by this revalidation to require a new Wordstat request before cleanup.

This verdict means **acquisition breadth is sufficient to start checking every collected phrase**. It does not mean all 2965 source rows (`2415 + 550`) are relevant, unique, final, or destined for separate pages.

## Next step

```text
NEXT_STEP = ROW_LEVEL_CLEANUP
NEXT_STEP_AUTOMATICALLY_AUTHORIZED = false
```

The cleanup step must account for every source row and preserve explicit decisions/reasons. It must not delete low-frequency phrases solely for being low-frequency and must keep unresolved valuable/business-boundary phrases in REVIEW until later Search/business evidence resolves them.

## Non-repeat controls

```text
probe success was not treated as sufficiency proof by itself = PASS
complete repaired first-pass corpus used = PASS
all four preserved probes rechecked = PASS
exact overlap separated from semantic information gain = PASS
associations not promoted automatically = PASS
no arbitrary numeric sufficiency threshold invented = PASS
no additional provider call made = PASS
historical Step-05 acceptance not silently rewritten = PASS
```

`NON_REPEAT_CONTROLS = PASS`
