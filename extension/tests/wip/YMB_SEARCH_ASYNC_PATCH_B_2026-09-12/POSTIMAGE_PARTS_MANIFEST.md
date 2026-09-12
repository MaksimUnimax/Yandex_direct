# Patch B candidate1 — exact postimage transport manifest

Date: 2026-09-12
Branch: `wip/ymb-search-async-patch-b-2026-09-12`

The earlier single large WIP Base64 object was removed because its tool transport had been truncated. The exact Patch-B postimage is now stored as six independently read-back parts under `postimage_parts/`.

Concatenate files in lexical order with **no separators/newlines added**:

```text
part-01.b64
part-02.b64
part-03.b64
part-04.b64
part-05.b64
part-06.b64
```

Part identities:

| part | bytes | SHA-256 | Git blob SHA |
|---|---:|---|---|
| part-01.b64 | 4000 | `cc12402926b92021990fc2a39a7af1ee9c8e7d05f776d2ebdb3076b85d35e7f5` | `38d5b38155abde72f938e7716abba7993acb6e5c` |
| part-02.b64 | 4000 | `f946182149d8c49444b9fcadedbb6f82569d7e77728699a0ba8e7520f1087452` | `94c8f1426bb6688d37b22b54e85893495e4a3e40` |
| part-03.b64 | 4000 | `e911d6c1fdf469f6da38681760febfb09e89fb9f8b4f452f1881f295c46d9b4f` | `4cf71a87a065517f8722795e334808938f1e9aca` |
| part-04.b64 | 4000 | `2279155f1df4de4f763fd8eefba57ab9f995bbac82639b685384f82f152a941d` | `0902004fc3d199beac46d4c8ca665d2b7dfefbc8` |
| part-05.b64 | 4000 | `b2e31d499c8e839123b8e15ff4ee4914f4a936898ea7834570518efc0f017abb` | `e56b65ad591959d9496bbb18f75d0300fe913d28` |
| part-06.b64 | 2856 | `7cc2570ef4229b07c5503e91bfa8072a2cebe6555bf44fb4008ab23fafff06fd` | `87ff5cd14c2a1253b8a6b9d08bf480506258cd6d` |

Remote GitHub directory readback returned the exact Git blob SHA and byte count shown above for all six parts (`6/6 PASS`).

Combined Base64 identity:

```text
bytes = 22856
SHA-256 = 04c6b247460e1de6c625cdd5adc0a985f096200c286956deaf1fed8f378491dc
```

Decoded deterministic tar.gz identity:

```text
bytes = 17141
SHA-256 = 4c2fc2c4d97149b73d27b6b329749ce16b6b2f01fe838d2516dd536d677a62ef
```

The tar contains exactly the eight Patch-B candidate1 changed postimages:

1. `manifest.json`
2. `phase3_service_worker_bootstrap.js`
3. `search_async_worker_transport.js`
4. `shared/search_async_content_bridge.js`
5. `shared/search_async_protocol.js`
6. `shared/search_async_runtime.js`
7. `shared/search_async_store.js`
8. `shared/search_async_transport.js`

The exact owner 0.1.4 baseline archive plus these eight exact postimages reconstruct Patch B candidate1. No production code is changed by this evidence transport.
