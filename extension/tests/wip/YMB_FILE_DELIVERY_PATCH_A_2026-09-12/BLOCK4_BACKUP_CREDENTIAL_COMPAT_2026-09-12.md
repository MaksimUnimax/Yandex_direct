# YMB Patch A — backup / credential compatibility block 4

Date: 2026-09-12
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Candidate: exact candidate2; production bytes unchanged.

## Byte-identity dependency audit

Candidate2 differs from the owner 0.1.4 baseline in exactly seven production paths. Fifty other production files remain byte-identical.

Critical unchanged authorities include:

- `service_worker.js`;
- `service_worker_bootstrap.js`;
- `webmaster_worker_runtime.js`;
- Search Batch / Wordstat Batch worker transports and protocol/runtime modules;
- policy/cost models;
- credential registry/runtime/store;
- Search / Wordstat / Webmaster / Metrika / Direct protocol and provider runtimes;
- settings backup v3 runtime;
- autorun model;
- composer send;
- conversation identity.

## Executed compatibility assertion

A real Patch-A artifact was staged in `ymb_delivery_artifacts_v2`, then the existing settings backup/export+import contract was exercised.

Results:

```text
SETTINGS_EXPORT = PASS
ARTIFACT_PAYLOAD_NOT_INCLUDED_IN_SETTINGS_BACKUP = PASS
ARTIFACT_METADATA_NOT_INCLUDED_IN_SETTINGS_BACKUP = PASS
SETTINGS_IMPORT = PASS
ARTIFACT_STORE_SURVIVES_SETTINGS_IMPORT = PASS
WORDSTAT_CREDENTIAL_PRESERVED = PASS
SEARCH_CREDENTIAL_PRESERVED = PASS
WEBMASTER_CREDENTIAL_PRESERVED = PASS
METRIKA_CREDENTIAL_PRESERVED = PASS
DIRECT_CREDENTIAL_PRESERVED = PASS
ARTIFACT_CLEANUP_AFTER_TEST = PASS
BLOCK4 = PASS
```

The settings backup continued to preserve credentials according to its pre-existing secret-containing backup contract; Patch A did not move attachment bytes or metadata into that backup.

## Release status

```text
PRODUCTION_BYTES_CHANGED_IN_BLOCK = NO
BLOCK4_BACKUP_CREDENTIAL_COMPAT = PASS
RELEASE_ALLOWED = NO
```

Patch A still requires the remaining exact-candidate pre-delivery/dependency gates before acceptance.
