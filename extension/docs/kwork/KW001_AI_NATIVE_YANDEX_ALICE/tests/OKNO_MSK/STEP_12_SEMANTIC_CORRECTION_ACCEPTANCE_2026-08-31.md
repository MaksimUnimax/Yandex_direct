# Step 12 — semantic/structural-unit correction acceptance

Date: 2026-08-31  
Scope: acceptance of **D12-01, D12-02, D12-08, D12-09 and D12-12 only**.  
This does **not** re-accept all of Step 12 and does not authorize Step 13.

## Purpose

The first Step-12 run could not be repaired safely by editing final action labels. The structural units themselves first had to be corrected so later demand, Search evidence, confidence and QA would not be calculated over mixed or hidden phrase routes.

This acceptance therefore answers only:

```text
Are the previous hidden phrase overrides now explicit auditable task units?
Have the known mixed units been decomposed before later action decisions?
Have historical NO_STANDALONE / OUTSIDE groups been rechecked for useful stranded phrases?
Have known contradictions between old OUTSIDE states and verified current site offer been corrected without blindly rescuing unrelated/competitor demand?
```

## Accepted V4 artifacts

```text
STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V4.tsv
STEP_12_STRUCTURAL_UNITS_V4.tsv
STEP_12_STRUCTURAL_UNIT_CORRECTIONS_V4.tsv
STEP_12_NO_PAGE_OUTSIDE_SALVAGE_REVIEW_V4.tsv
STEP_12_STRUCTURAL_UNIT_CORRECTION_QA_V4.json
STEP_12_SEMANTIC_CORRECTION_REVIEW_PACKET.md
STEP_12_SEMANTIC_CORRECTION_REGRESSION_ACTUAL.tsv
STEP_12_CORRECTION_FIRST_PARTY_REFRESH_2026-08-31.md
STEP_12_CORRECTION_EXTERNAL_SCOPE_CHECK_2026-08-31.md
```

Historical first-pass files remain preserved but are not the accepted final architecture.

## Accounting / mechanical evidence

Persisted V4 QA:

```text
SOURCE_ROWS = 2332
SEARCH_REQUIRED_ROWS = 19
EXPLICIT_STRUCTURAL_UNITS = 159
CORRECTION_ROWS = 1037
HISTORICAL_OVERRIDE_ROWS = 191
HISTORICAL_OVERRIDE_ROWS_WITH_EXPLICIT_FINAL_UNIT = 191
HIDDEN_RUNTIME_OVERRIDE_RULES_IN_V4_OUTPUT = 0
UNIT_METADATA_INCONSISTENCY_ROWS = 0
MANDATORY_MIXED_ORIGINAL_UNITS_STILL_FINAL = 0
HISTORICAL_NO_PAGE_OR_OUTSIDE_REVIEW_ROWS = 481
SALVAGED_TO_IN_SCOPE_UNITS = 127
EXPLICITLY_DEFERRED_ROWS = 6
OUTSIDE_CONFIRMED_ROWS = 108
NO_STANDALONE_CONFIRMED_ROWS = 240
DEFAULT_HIGH_CONFIDENCE_ROWS = 0
```

These numbers are not used as semantic proof by themselves. They establish completeness and identify what had to be read/reviewed.

## Manual semantic readback — mixed-unit corrections

The persisted review packet confirms the major mixed first-pass units are no longer used as one final unit.

### DIY installation

Historical:

```text
WINDOW_INSTALLATION_DIY_INFO = 36 phrases -> one PVC-window DIY article candidate
```

V4:

```text
PVC_WINDOW_INSTALLATION_DIY = 26
PVC_DOOR_INSTALLATION_REMOVAL_DIY = 5
ALUMINIUM_WINDOW_INSTALLATION_REMOVAL_DIY = 3
FRENCH_WINDOW_INSTALLATION_DIY = 2
```

This corrects the original object mixing. A later Step-12 action may still decide whether the 26-phrase PVC subset deserves a page, but doors/aluminium/French-window phrases no longer support that page by accident.

### Panoramic windows

Historical:

```text
PANORAMIC_WINDOWS_COMMERCIAL = 73 phrases -> one broad commercial page candidate
```

V4 source-cluster redistribution:

```text
PANORAMIC_WINDOWS_COMMERCIAL_CORE = 45
PANORAMIC_DESIGN_INSPIRATION = 13
PANORAMIC_OUTDOOR_GLAZING = 5
PANORAMIC_WINDOW_TECH_SELECTION_INFO = 4
PANORAMIC_WINDOW_OPERATION_AMBIGUOUS = 3
PANORAMIC_BALCONY_GLAZING = 2
PANORAMIC_REAL_ESTATE_BRAND_QUERY = 1
```

The broad commercial candidate therefore no longer claims all 73 phrases as commercial evidence.

### Glazing permission / legal

Historical seven phrases are explicitly separated into:

```text
BALCONY_GLAZING_PERMISSION_INFO = 3
BOILER_ROOM_WINDOW_REQUIREMENTS_INFO = 2
FRENCH_WINDOW_REDEVELOPMENT_PERMISSION_INFO = 1
WINDOW_HARDWARE_STANDARD_INFO = 1
```

The first-pass prose "distribute these later" is no longer the structural result; the subunits exist explicitly and legal/standard facts can remain deferred until verified.

### Wooden windows

The five historical rows no longer imply one wooden-window product task:

```text
WOOD_WINDOWS_UNVERIFIED_PRODUCT = 3
PRIVATE_HOUSE_PVC_WINDOWS_WOODEN_HOUSE = 1
WOOD_VS_PVC_WINDOWS_AMBIGUOUS = 1
```

`пластиковые окна в деревянном доме` is now explicitly rescued to the existing private-house PVC context.

### Window hardware information

The historical 41-row broad information unit is decomposed into selection/guide, third-party brand reviews, component selection, maintenance and aluminium-specific component information. Brand reviews are not allowed to inflate the proposed general guide.

### Window hardware shopping

The historical 239-row broad marketplace demand is no longer one no-page bucket. V4 salvages service/info/supported-accessory subsets (replacement service, hardware guide, handles, maintenance, installation materials, safety hardware) while the unsupported broad aftermarket catalogue remains explicit.

### Window accessories

The historical 47-row accessory group is decomposed into real accessory/product/service subtasks such as windowsills, drip caps, decorative bars, glazing units, profiles, finishing and frame/sash components. Existing-page routing is therefore based on explicit structural units rather than hidden per-phrase overrides.

## Manual regression cases

The persisted regression table was read back and the following known failure cases were checked semantically:

1. `пластиковые окна в деревянном доме` -> private-house PVC task, not wooden windows — **accepted**.
2. `остекление открытого балкона` -> balcony glazing, not finishing-without-glazing — **accepted**.
3. `алюминиевые жалюзи на окна` -> current blinds product family — **accepted**.
4. `rehau окна официальный сайт` -> official-brand navigation outside target domain — **accepted**.
5. `пластиковые окна от производителя официальный сайт` -> generic manufacturer/seller navigation, not automatically REHAU-brand navigation — **accepted as in-scope candidate**.
6. PVC-door DIY phrase -> PVC-door DIY unit — **accepted**.
7. PVC-window DIY phrase -> PVC-window DIY unit — **accepted**.
8. aluminium-window DIY phrase -> aluminium DIY unit — **accepted**.
9. French-window DIY phrase -> French-window DIY unit — **accepted**.
10. command-like `открой панорамное окно` -> deferred ambiguity — **accepted**.
11. `панорамные окна купить` -> corrected panoramic commercial core — **accepted**.
12. `панорамные окна на балконе` -> existing panoramic-balcony task — **accepted**.
13. `веранда с панорамными окнами` -> outdoor glazing task with later page-boundary dependency — **accepted**.
14. `какие панорамные окна лучше` -> technical/selection task — **accepted**.
15. `барбекю с панорамными окнами` -> design/application inspiration, not counted as commercial-core evidence — **accepted**.
16. `оконная фурнитура roto отзывы` -> third-party brand review subtask, not general guide core — **accepted**.
17. `чем смазать оконную фурнитуру` -> maintenance subtask — **accepted**.
18. `оконная фурнитура виды` -> hardware explanation/selection core — **accepted**.
19. `замена фурнитуры на пластиковых окнах цена` -> current repair/component-replacement service — **accepted**.
20. `купить оконную фурнитуру` -> unsupported broad aftermarket catalogue rather than invented store page — **accepted**.
21. `ремонт жалюзи на пластиковые окна` -> deferred because repair service is not verified — **accepted**.
22. `жалюзи на пластиковые окна` -> verified current blinds page — **accepted**.
23. `шторы на пластиковые окна` -> not automatically equated with the verified blinds offer — **accepted**.
24. `пластиковые окна в рассрочку` -> PVC-window purchase remains the primary product task; finance page is supporting payment information, not automatically the primary landing — **accepted**.

## D12-12 current-evidence challenge

The current first-party blinds page was re-opened during correction. It directly shows:

```text
H1 = Жалюзи на пластиковые окна
visible product types = horizontal / vertical / Isolite Isotra / pleated
selection help = yes
order path = yes
measurement = yes
delivery = yes
installation/montage = yes
standalone repair service = not verified by this read
```

Therefore the historical decision that all blinds demand was outside the target business is materially contradicted and corrected. Generic curtains/roller-curtain wording is not automatically rescued because the page read does not prove every curtain product variant.

The suspicious phrase `окна сок панорамное раздвижное остекление` was separately checked in current public Search. `Окна СОК` is another window/glazing company/brand. Therefore this phrase remains outside; D12-12 is not a rule to rescue every phrase containing window vocabulary.

## Historical NO_STANDALONE / OUTSIDE universe review

The V4 review covers all **481** phrases whose historical Step-12 cluster action was `NO_STANDALONE_PAGE` or `OUTSIDE_SCOPE_NO_ACTION`.

Final review dispositions at this semantic layer:

```text
SALVAGED_TO_IN_SCOPE_UNIT = 127
EXPLICITLY_DEFERRED = 6
OUTSIDE_CONFIRMED = 108
NO_STANDALONE_CONFIRMED = 240
TOTAL = 481
```

This resolves the first-pass defect where "this cluster should not become a standalone page" could strand a useful phrase. Salvaged rows now have explicit units; uncertain rows are explicitly deferred instead of being forced; truly unsupported/outside rows remain explicit.

## Defect verdicts

### D12-01 — HIDDEN_LEXICAL_OVERRIDES

**VERIFIED_FIXED at the semantic-unit layer.**

Why:
- 191/191 historical override rows are represented by explicit V4 structural units;
- finance was decomposed into product/service-specific instalment-condition units instead of one blanket finance target;
- aluminium sliding was decomposed into generic product, balcony and outdoor tasks;
- final V4 artifacts contain no runtime `route_override()` mechanism as architecture truth.

Historical first-pass code is preserved only for provenance and is not accepted as the corrected final routing method.

### D12-02 — MIXED_UNITS_SURVIVED_FULL_AUDIT

**VERIFIED_FIXED for the known/re-audited mixed-unit classes.**

Why:
- all mandatory mixed original unit IDs were decomposed;
- V4 has zero unit-metadata inconsistencies;
- known regression phrases demonstrate that object, service, informational, inspiration and ambiguous rows no longer inherit one dominant action merely from the old cluster label.

### D12-08 — NO_STANDALONE_SUBTASKS_NOT_FINISHED

**VERIFIED_FIXED at the semantic-routing layer.**

Why:
- all 481 historical no-page/outside rows have an explicit review disposition;
- useful subparts receive another explicit unit/page candidate or a named defer state rather than only prose saying "distribute later".

### D12-09 — SALVAGEABLE_PHRASES_TRAPPED_IN_REJECTED_UNITS

**VERIFIED_FIXED at the semantic-routing layer.**

Why:
- the entire rejected/outside universe was included in the salvage review;
- known trapped phrases such as PVC windows in a wooden house and open-balcony glazing are explicitly rescued;
- the review does not assume every row should be rescued.

### D12-12 — UPSTREAM_OUTSIDE_SCOPE_CONFLICT_WITH_VERIFIED_SITE_OFFER

**VERIFIED_FIXED for the reviewed current job state and promoted as a permanent causal rule.**

Why:
- current first-party evidence proved blinds selection/purchase/installation is a real site offer and those rows are no longer globally outside;
- unrelated curtains remain outside instead of being rescued mechanically;
- another suspicious window-looking `OUTSIDE_OTHER` phrase was disambiguated as other-brand demand and correctly retained outside;
- upstream history remains preserved and corrections are overlays rather than silent rewrites.

## What remains OPEN

This acceptance deliberately does **not** close:

```text
D12-03 NEW_PAGE_EVIDENCE_NOT_MATERIALIZED
D12-04 DEFAULT_HIGH_CONFIDENCE
D12-05 QA_SELF_CERTIFICATION_AND_SPLIT_MERGE_BUG
D12-06 STEP13_HANDOFF_MANUAL_NOT_DERIVED
D12-07 NEW_PAGE_HIERARCHY_INCOMPLETE
D12-10 PHRASE_COUNT_USED_AS_DEMAND_PROXY
D12-11 PROVISIONAL_DEPENDENCIES_HIDDEN_BY_FINAL_ACTION
```

Step 12 therefore remains **CORRECTION REQUIRED**, and Step 13 remains blocked.

## Next correction

Next item is D12-03 + D12-10: attach actual persisted demand and ordinary Search evidence to the corrected standalone-page candidates. Phrase count will be treated only as coverage, not demand.

No new Bridge call is authorized merely by this transition; existing Wordstat/Search evidence must be exhausted first.

## Plain-language summary

**Why this correction was needed:** the first version sometimes mixed different kinds of searches together or threw away a whole group even though individual useful searches inside it still belonged to the site.

**What was fixed:** every old shortcut and every rejected/outside group was reopened at phrase level. Different user tasks were separated, useful phrases were rescued, uncertain ones were explicitly postponed, and genuinely external demand stayed external.

**What this gives us:** we now have a much cleaner foundation for deciding which pages really deserve to exist. The next job is to prove those page ideas with actual search demand and ordinary Yandex evidence instead of the number of phrases in the group.
