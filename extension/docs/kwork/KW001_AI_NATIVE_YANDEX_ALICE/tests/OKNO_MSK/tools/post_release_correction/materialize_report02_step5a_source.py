from __future__ import annotations

import base64
import hashlib
import zlib
from pathlib import Path

ROOT = Path('extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK')
RELEASE = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09'
TARGET = RELEASE / 'sources/02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.md'
TOOLS = Path(__file__).resolve().parent
EXPECTED_SHA256 = 'c687bf07acc41a8d141c5ea8a640c5cb0ad2aa93e75db11f98082cc1950aad4a'

payload = ''.join(
    (TOOLS / f'report02_step5a_source_payload.part{i}.txt').read_text(encoding='ascii').strip()
    for i in range(1, 5)
)
source = zlib.decompress(base64.b64decode(payload.encode('ascii')))
actual = hashlib.sha256(source).hexdigest()
if actual != EXPECTED_SHA256:
    raise SystemExit(f'payload hash mismatch: {actual}')

TARGET.parent.mkdir(parents=True, exist_ok=True)
TARGET.write_bytes(source)
print(f'REPORT02_STEP05A_SOURCE_OK bytes={len(source)} sha256={actual}')
