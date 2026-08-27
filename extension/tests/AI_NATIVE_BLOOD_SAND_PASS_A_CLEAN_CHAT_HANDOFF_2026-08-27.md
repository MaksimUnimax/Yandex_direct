# blood_sand — isolated clean-chat Pass A handoff v2

Date: 2026-08-27
Status: **READY / SEALED TWO-FILE INPUT / FAIL CLOSED ON ANY EXTRA SOURCE**

## 1. Target

Repository:

```text
MaksimUnimax/Yandex_direct
```

Working branch:

```text
gate/ai-native-blood-sand-pass-a-2026-08-27
```

Required output:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md
```

## 2. Complete evidence universe

For semantic analysis, exactly ONE evidence file is permitted:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_SEALED_BASELINE_PACKET_2026-08-27.md
```

This handoff plus that sealed packet are the entire readable source universe for this run.

Do NOT read the older baseline manifest.
Do NOT open `MaksimUnimax/blood_sand`.
Do NOT inspect any other file in `MaksimUnimax/Yandex_direct`.
Do NOT use repository search, code search, web search, prior conversations, personal context, remembered project conclusions, or fresh provider data.

If any file other than this handoff, the sealed packet, or the newly-created Pass A output is opened before freeze, stop with:

```text
INVALID_BASELINE_LEAKAGE
```

## 3. Allowed GitHub operations

Only these operations are allowed:

1. refetch the current head of `gate/ai-native-blood-sand-pass-a-2026-08-27`;
2. fetch this exact handoff path;
3. fetch the exact sealed packet path;
4. reason from the sealed packet only;
5. refetch the branch head immediately before write;
6. create the required Pass A output on the same branch;
7. stop.

Do not verify provenance by opening the source repository. Provenance is already frozen inside the sealed packet.

## 4. Required analysis

Produce a strong ordinary SEO / semantic-core baseline from the sealed packet only.

For each decision-relevant unit, record:

```text
unit_id
root_or_cluster
baseline_evidence
intent
decision = KEEP | INVESTIGATE | REJECT
priority
page_job
split_merge
confidence
missing_evidence
contamination_or_fit_notes
```

The report must independently resolve, where evidence supports it:

- `печать велеса` vs its explicit meaning-query variant;
- named symbol families such as `вегвизир` and related measured roots;
- automotive protection/use-case roots vs mirror-pendant form-factor roots;
- zodiac/broad-demand contamination;
- generic automotive gift roots with weak direct assortment fit;
- specialist independent-site opportunity;
- low-volume exact `symbol + car` wording vs stronger clusters.

Do not assume that high demand means a separate page. Do not assume that two related phrases belong on one page. Use ordinary Search composition, business fit and measured demand.

## 5. Required report header

The output must state:

```text
PASS_A_CONTEXT = CLEAN_SEALED_PACKET_ONLY
sealed_packet_path = extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_SEALED_BASELINE_PACKET_2026-08-27.md
frozen_source_commit = 0da1fdfa65155fe0b22d67838d366e7d214ccbbe
extra_source_opened = false
fresh_provider_requests = 0
```

Also list the actual read inventory, which must contain only:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_CLEAN_CHAT_HANDOFF_2026-08-27.md
extension/tests/AI_NATIVE_BLOOD_SAND_PASS_A_SEALED_BASELINE_PACKET_2026-08-27.md
```

## 6. Freeze

Write:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md
```

Commit message:

```text
qa(ai-native): freeze clean blood_sand Pass A
```

After the commit, STOP. Do not inspect any additional files.

Return only:

```text
PASS_A_FROZEN
commit_sha = <sha>
extra_source_opened = false
fresh_provider_requests = 0
```
