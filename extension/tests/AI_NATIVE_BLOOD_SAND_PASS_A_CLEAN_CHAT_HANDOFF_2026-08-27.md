# AI-native blood_sand — isolated clean-chat Pass A handoff

Date: 2026-08-27
Status: **READY FOR GENUINELY CLEAN PASS A / PASS B FORBIDDEN UNTIL FREEZE**

## Authority

Target repository for durable output:

```text
MaksimUnimax/Yandex_direct
branch = gate/ai-native-blood-sand-pass-a-2026-08-27
baseline_parent = 9f183e953f7e0a90d71b9538834ac06d50190360
```

Canonical Pass A source manifest:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_SOURCE_MANIFEST_2026-08-27.md
```

Frozen evidence repository:

```text
MaksimUnimax/blood_sand
commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
```

Required output:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md
```

## Clean-context contract

This run exists specifically because the originating long-running project conversation is not a valid Pass A context.

Treat this task as a standalone experiment. For the analysis itself:

- use only the connected GitHub repositories named above;
- do not use web search;
- do not use prior conversations, remembered conclusions, personal-context retrieval, or user-profile memories as evidence;
- if any pre-existing model context mentions `blood_sand` conclusions beyond the files explicitly admitted by the frozen source manifest, treat that context as inadmissible and do not use it;
- do not perform a broad repository search in `MaksimUnimax/blood_sand` because search results can surface forbidden files;
- fetch only the exact files or directory prefixes explicitly allowed by the frozen source manifest, always at commit `0da1fdfa65155fe0b22d67838d366e7d214ccbbe`;
- do not collect fresh paid/provider evidence.

If any forbidden Alice/AI-derived evidence or final R3 decision artifact is accidentally opened before the Pass A output is frozen, fail closed:

```text
INVALID_BASELINE_LEAKAGE
```

Do not write a purported Pass A in that case.

## Exact workflow

1. Refetch the current head of `gate/ai-native-blood-sand-pass-a-2026-08-27`.
2. Read only this handoff and `extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_SOURCE_MANIFEST_2026-08-27.md` from Yandex_direct.
3. Verify `MaksimUnimax/blood_sand` commit `0da1fdfa65155fe0b22d67838d366e7d214ccbbe` exists.
4. From that exact commit, fetch only the business/product/customer, Wordstat, ordinary Yandex Search, and clean ordinary-browser-SERP files admitted by the manifest. Do not use repository-wide search.
5. Produce an independent strong ordinary SEO / semantic-core baseline. Reason from the admitted evidence only.
6. Freeze the result to `extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md` on the gate branch.
7. Commit with message:

```text
qa(ai-native): freeze clean blood_sand Pass A
```

8. Stop. Do not open Pass B sources, Alice directories, cross-surface comparison files, final R3 opportunity artifacts, or the cross-surface evidence ledger.

## Required Pass A contents

The frozen report must include:

- exact `blood_sand` commit;
- exact Yandex_direct manifest path and gate branch;
- explicit anti-leakage declaration;
- source inventory actually read, with exact paths;
- candidate clusters / decision-relevant units;
- intent for each unit;
- `KEEP / INVESTIGATE / REJECT` decision with reasoning;
- priority reasoning based only on business fit, human demand, and ordinary Search;
- page-job recommendation;
- split / merge decisions;
- confidence;
- missing evidence;
- contamination / weak-fit rejection notes;
- explicit ordinary-Search treatment of at least these baseline families where supported by admitted evidence:
  - `печать велеса` and explicit meaning-query variant;
  - named symbol families such as `вегвизир` / related measured symbol roots;
  - automotive protection/use-case roots vs mirror-pendant form-factor roots;
  - zodiac/broad-demand contamination;
  - generic automotive gift roots with weak direct category fit;
  - specialist independent-source opportunity.

Do not include or infer any AI/Alice importance dimension. Do not import final R3 decisions. Do not write H/A/C/O scoring.

A compact decision table is preferred with columns similar to:

```text
unit_id
root_or_cluster
baseline_evidence
intent
decision
priority
page_job
split_merge
confidence
missing_evidence
contamination_or_fit_notes
```

## Freeze acceptance

The Pass A freeze is valid only if all are true:

```text
blood_sand_commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
forbidden_source_opened = false
fresh_provider_requests = 0
pass_b_sources_opened = false
output_path = extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md
```

After committing, return only a concise result containing:

```text
PASS_A_FROZEN
commit_sha = <sha>
forbidden_source_opened = false
fresh_provider_requests = 0
```

Do not continue to Pass B in the clean Pass A chat.