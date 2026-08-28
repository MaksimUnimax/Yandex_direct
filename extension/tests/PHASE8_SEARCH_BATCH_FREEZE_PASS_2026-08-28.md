# PHASE 8 SEARCH BATCH — EXACT CANDIDATE FREEZE PASS

Status: **PASS / FROZEN — OWNER-LIVE PENDING**
Date: 2026-08-28

## Exact source authority

```text
source_commit = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716
source_ref = phase8/bulk-serp-top-rank-2026-08-28
extension/src tree = bdad1e87a2537d8646e480ca23f8068c3dced17e
```

The candidate branch was created from the exact CI-green source authority. The freeze workflow trigger commit is not product source authority.

## Pre-freeze development gate

```text
run = 33143059673
head_sha = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716
status = completed
conclusion = success
complete root Node suite = PASS (118/118)
controlled installed-extension MV3 browser = PASS
post-browser product identity = PASS
real Yandex requests = 0
```

The browser harness uses a controlled local provider stub. It proves ordinary Search batch provider-boundary behavior without contacting Yandex.

## Exact freeze gate

```text
freeze_run = 33143237276
freeze_trigger_sha = 82fb14dfb6fc715b02d88634861cd04fd429711b
status = completed
conclusion = success
source syntax + complete Node suite = PASS
source controlled MV3 browser = PASS
deterministic ZIP rebuild = PASS
source/extract byte identity = PASS
packaged syntax + complete Node suite = PASS
packaged controlled MV3 browser = PASS
packaged product immutability = PASS
real Yandex requests during freeze = 0
```

## Frozen artifact

GitHub Actions artifact:

```text
artifact_id = 9674766720
artifact_name = phase8-search-batch-candidate-0377d6e1
artifact_wrapper_bytes = 153671
artifact_wrapper_sha256 = a7c9b668089aeb0904fd029e29efab88e8b63b4df802bf6f2ad9e56b50f4ca91
```

Exact install candidate inside the artifact:

```text
filename = yandex-marketing-bridge-0.1.1-phase8-search-batch-candidate.zip
bytes = 150931
sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332
product_files = 53
zip_test = PASS
manifest.json_at_zip_root = YES
deterministic_rebuild = PASS
source_extract_byte_identity = PASS
```

The independently downloaded GitHub artifact wrapper digest matched GitHub artifact metadata, and the independently extracted inner candidate SHA-256/size/file count matched the freeze manifest exactly.

## Accepted Phase 8 pre-owner-live invariants

```text
registry services = exactly 5
Search batch = existing search service
protocol = SEARCH_BATCH_API_V1
result = SEARCH_BATCH_RESULT_V1
provider method inside batch = ordinary search only
provider endpoint = /v2/web/search
start/status/pause/resume/cancel/projection/overlapPage = 0 provider requests
one explicit next = at most 1 provider request
hidden loops = forbidden
automatic retry after provider initiation = forbidden
unknown outcome = durable OUTCOME_UNKNOWN / no replay
500-key start = allowed within explicit caps, 0 provider requests until next
credentials persisted in batch job = NO
```

## Remaining gate

Phase 8 is **not yet closed**. Next required stage is P8-13 minimal owner-live using this exact frozen candidate. Only after owner-live PASS may the exact accepted product bytes be integrated to `main` and Phase 8 be closed.
