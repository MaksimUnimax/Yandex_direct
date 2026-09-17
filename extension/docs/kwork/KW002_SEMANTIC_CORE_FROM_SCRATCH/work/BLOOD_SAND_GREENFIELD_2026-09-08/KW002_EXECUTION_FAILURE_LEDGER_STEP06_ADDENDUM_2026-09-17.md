# KW-002 — Step06 execution failure ledger addendum

Date: 2026-09-17  
Status: **ACTIVE JOB-SPECIFIC ANTI-REGRESSION HISTORY**

This file records not just what failed, but why the failure occurred and the permanent control that prevents recurrence.

## S06-F01 — stale 18+2 cursor produced an obsolete collect instruction

**What happened.** The grouped Q003-Q022 queue had already reached 20 SUCCEEDED / 0 unresolved and the final export existed, but an older 18+2 state was reused.

**Why I made it.** I treated a once-valid conversational cursor as action authority instead of reconciling the newest durable queue/export state immediately before the action.

**Risk.** Duplicate provider work, wasted calls and provenance confusion.

**Correction.** Latest durable state wins. Terminal state plus received final export forbids submit/collect/retry absent explicit recovery authority.

## S06-F02 — final export state drift

**What happened.** The already-received final export was mentally downgraded to an in-progress queue state.

**Why.** Execution and analysis states were not explicitly separated.

**Correction.** Track `PROVIDER_TERMINAL`, `FINAL_EXPORT_RECEIVED`, `ANALYTICAL_HARDENING`, `STEP_ACCEPTED` as different state variables.

## S06-F03 — 440/440 acquisition was declared complete analysis too early

**What happened.** Perfect row/rank accounting was initially treated as Step06 completion.

**Why.** Binary provider QA is easy to prove and was allowed to substitute for harder semantic QA.

**Risk.** Collisions, page types and mixed intent contaminate competitors and later clustering.

**Correction.** 440 row classifications + 22 Top-10 profiles + collision control + recurrence + 231 pairwise comparisons + registry are required.

## S06-F04 — Top-20 presence was overweighted

**What happened.** Any rank 1-20 appearance initially contributed too strongly to competitor breadth narrative.

**Why.** Acquisition depth was confused with analytical priority.

**Correction.** Top-10 primary; Top-3 amplifier; 11-20 secondary discovery.

## S06-F05 — domain overlap came too close to cluster inference

**What happened.** Shared domains were initially tempting to read as query-cluster similarity.

**Why.** Domain overlap is easy to count and looks intuitively similar to SERP overlap.

**Risk.** One site can rank different URLs for different intents.

**Correction.** Exact URL overlap and domain overlap are always separate; Step06 never creates final pages from domain recurrence.

## S06-F06 — intent classification was initially too impressionistic

**What happened.** Coarse `COMMERCIAL_LED / INFORMATIONAL_LED / HYBRID / COLLISION` labels were narrated before full Top-10 composition had been materialized.

**Why.** Human-readable SERP impression was allowed to precede reproducible row-level evidence.

**Correction.** Accepted intent derives from classified Top-10 composition and confidence. Source class remains preliminary provenance.

## S06-F07 — collision queries contaminated broad recurrence

**What happened.** Raw recurrence across all representative queries could promote unrelated entities as niche competitors.

**Why.** Mechanical recurrence aggregation is semantically blind.

**Correction.** Preserve raw recurrence and separately materialize collision-heavy exposure and target-usable query subsets.

## S06-F08 — page/result type was not materialized in the first pass

**What happened.** The first local analysis knew URLs/titles/domains but lacked a complete row-level page-type field.

**Why.** I prioritized competitor recurrence before formal intent evidence.

**Correction.** Full 440-row classification is mandatory before final Step06 analytical acceptance.

## S06-F09 — risk of unsupported SERP-feature inference

**What happened.** The external audit highlighted SERP features even though the normalized source did not capture them.

**Why.** General SERP-analysis methodology was being mapped too broadly onto a narrower source schema.

**Correction.** `SERP_FEATURE_COVERAGE = NOT_CAPTURED_BY_CURRENT_SOURCE`; absence in evidence is not evidence of absence in live SERP.

## S06-F10 — snapshot could be over-described as permanent market truth

**What happened.** A 22×20 matrix is large enough to feel like a market census.

**Why.** Volume created false stability confidence.

**Correction.** All conclusions are bounded to the acquisition snapshot; long-term stability needs repeated temporal evidence.

## S06-F11 — Step06 evidence risked drifting toward final page decisions

**What happened.** Strong overlap signals invited query→page conclusions.

**Why.** Similarity evidence naturally resembles a clustering decision.

**Correction.** Step06 similarity = evidence only. Final page ownership belongs to the later governed clustering/architecture step.

## S06-F12 — unobserved artifact identity was previously implied

**What happened.** An `.xz`-style artifact identity was previously implied although only JSON and deterministic `.json.gz` were observed.

**Why.** Expected packaging convention was substituted for direct observation.

**Correction.** No extension/hash/blob/commit is reported without direct local computation or remote readback.

## S06-F13 — irrelevant persistence/Git concern interrupted the bounded analytical cursor

**What happened.** Repository/persistence mechanics were introduced before the active analytical action required them.

**Why.** A project-wide control was allowed to override the immediate cursor.

**Correction.** Ask whether an action advances the bounded cursor; persistence belongs at its defined checkpoint.

## S06-F14 — Work PASS / owner upload was at risk of being treated as acceptance

**What happened.** 440-row semantic work was delegated to Work and manually transported by the owner.

**Why this needs a guard.** Work QA and owner transport are evidence, not independent architectural acceptance.

**Correction.** Main readback + input identity reconciliation + independent downstream QA are required.

## S06-F15 — Work-only owner transport rule was incorrectly generalized to Main ChatGPT

**What happened.** After defining an efficient Work→ZIP→owner workflow, I started asking the owner to transport Main-created/edited artifacts too.

**Why I made it.** I generalized a resource-saving rule beyond the role it was designed for.

**Why it mattered.** It wasted owner time and inverted responsibility: Main can normally publish its own changes.

**Correction.** Owner-mediated transport is the default only for delegated Work. Main publishes Main-created edits itself unless the owner explicitly requests manual transport for that bounded task or a real technical limitation exists.

## S06-F16 — already-published Work files were treated as if they needed rebuilding/re-upload

**What happened.** After the owner had already published the three Work hardening artifacts, I started reconstructing a package that included/recreated them.

**Why.** “Fix all” was interpreted as “republish all” instead of first inventorying remote state and producing only the delta.

**Risk.** Redundant upload, accidental byte drift, wasted tool calls and user time.

**Correction.** Remote inventory first. Existing accepted Work artifacts are immutable inputs unless a concrete defect requires replacement. Final patch contains only changed/new files.

## S06-F17 — low-level blob staging was started before final file set was proven

**What happened.** Temporary Git blobs were created while the final schema/package was still changing.

**Why.** I optimized transport before finishing analytical acceptance.

**Result.** No branch ref or commit was changed, so project state was unaffected, but the calls were useless.

**Correction.** Finalize and locally QA the exact delta first; only then publish. Orphan blobs are not project state.

## S06-F18 — stale preliminary denominators survived in the first hardened competitor registry

**What happened.** The first hardened registry retained fields named `commercial_coverage_8` and `informational_coverage_9` even after Work changed the accepted Top-10 split to 6 commercial / 11 informational / 1 hybrid / 1 uncertain / 3 collision-mismatch.

**Why.** New hardening metrics were joined onto a pre-hardening registry without a schema-provenance audit of every denominator.

**Risk.** A file labeled “hardened” simultaneously encoded old and new populations without clear provenance.

**Correction.** Those stale fields are removed from the final registry. Accepted-intent fields now carry their denominators in the column names (`*_6`, `*_11`, etc.). Preliminary populations may be preserved only under explicit `source_preliminary_*` names.

## S06-F19 — page-type enum was not dataset-extensible enough for audio/listening surfaces

**What happened.** The frozen Work enum had no `AUDIO`; recurring music/listening results under `мантра` fell into `OTHER`.

**Why.** The delegation prompt used a generic page-type taxonomy before checking every recurring surface in this specific dataset.

**Risk.** `OTHER` can look homogeneous when it actually contains a meaningful repeated SERP format.

**Correction.** The Step06 method now requires an extensible taxonomy. For this frozen Work file, the limitation is explicitly disclosed as `AUDIO_SURFACES_MAY_BE_COLLAPSED_TO_OTHER_IN_WORK_SCHEMA`; no redundant 440-row rewrite is required to close this bounded step.

## S06-F20 — “clean recurrence” wording overstated the filtering granularity

**What happened.** The first hardened recurrence used `clean_*` field names for metrics that excluded whole collision-heavy/uncertain queries, not individual non-target rows.

**Why.** A shorthand label blurred query-level and row-level filtering semantics.

**Risk.** Readers could wrongly infer that every retained row had passed `target_relevance=TARGET`.

**Correction.** Final recurrence uses `safe_query_subset_*` and explicitly states `QUERY_LEVEL_COVERAGE; NOT_ROW_LEVEL_RELEVANCE_FILTER`.

## Regression matrix

| Failure class | Final control | Result |
|---|---|---:|
| stale async cursor | newest durable state / terminal guard | PASS |
| acquisition mistaken for analysis | 440 + 22 + 231 hardening | PASS |
| Top-20 overweighting | Top-10 primary | PASS |
| domain overlap used as cluster proof | exact URL matrix separate | PASS |
| preliminary label frozen | accepted Top-10 intent separate | PASS |
| collision contamination | explicit collision/safe scopes | PASS |
| page type omitted | Work full-volume classification | PASS |
| audio subtype hidden in OTHER | limitation disclosed / future taxonomy extensible | PASS WITH DISCLOSED LIMITATION |
| unsupported SERP features | NOT_CAPTURED disclosure | PASS |
| snapshot permanence claim | bounded snapshot disclosure | PASS |
| final page decision | NONE | PASS |
| Work transport generalized to Main | role boundary corrected | PASS |
| redundant Work reupload | delta-only final patch | PASS |
| stale 8/9 denominators | removed / accepted 6/11 denominators | PASS |
| ambiguous clean metric | safe query subset naming + granularity | PASS |

`STEP07_STARTED = FALSE`.
