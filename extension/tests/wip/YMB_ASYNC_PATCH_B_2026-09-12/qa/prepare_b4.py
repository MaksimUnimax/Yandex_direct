"""Restore EXACT B4 QA modules from saved files, not an installable extension.
Usage: python qa/prepare_b4.py EXTRACTED_OWNER_014_BASELINE EMPTY_OUTPUT_DIR
No network, provider calls, browser changes or package/release operation.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
EXPECTED = {'candidate/shared/search_async_normalizer.js': '7c4fda899456696b1bbcb8ce096def228eded161f5a1f457edc2aaaf129f3415', 'candidate/shared/search_async_policy.js': '8d99cc8ad9b6a7781fad4e2d8df3e79df5297e6cb2c10bd3a57d3244c327ac38', 'candidate/shared/search_async_runtime.js': 'e8be98e7bd692321e44ff3af147415f235c9e4367de508982dc60f88b596de6f', 'qa/b4_normalizer.test.mjs': '8e9365938f88cc2a58abc9a07045fb017192a036a51a0af5c89acf22550a05f9', 'qa/b4_policy.test.mjs': '9b5d85003efe4066af40be34fbb7368d983fb9c6ddade2a959638775deef909c', 'qa/b4_runtime_seams.test.mjs': '4e17f8b9a336f6fc42aa9aabe264682689e0d9723ec41e8a2cb22f2f7f40bbd1', 'qa/idb_test_double.mjs': '1327c21fca17b0a34ebec3a8234c9721d1f09192f00bd862cffdbf1548d025af'}
BASELINE = {'shared/search_xml.js': '790d14469db165795c84c34a6b6e8bf68a259e477d01fb648ff3101244cecffd', 'shared/policy_model.js': '3b714387c85ae1641ef8d29dd3046d608dc7862692ce366007ce9e8fac1d49b8', 'shared/credential_registry.js': 'fb1106f758d23d65639ae384c48a184035ac09a89a0d70fe83a42cf961f48afd'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    baseline, output = (Path(v).resolve() for v in sys.argv[1:])
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise SystemExit('Refusing to overwrite nonempty output')
    inputs = {}
    for relative, expected in EXPECTED.items():
        value = (ROOT / relative).read_bytes()
        if sha(value) != expected:
            raise SystemExit('Saved source/test hash mismatch: ' + relative)
        inputs[relative] = value
    for relative, expected in BASELINE.items():
        value = (baseline / relative).read_bytes()
        if sha(value) != expected:
            raise SystemExit('Wrong exact owner-baseline dependency: ' + relative)
        inputs['baseline/' + relative] = value
    # Verify every input before materializing, without transformations or EOL conversion.
    for relative, value in inputs.items():
        dest = output / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(value)
        if dest.read_bytes() != value:
            raise SystemExit('Write/readback mismatch: ' + relative)
    (output / 'evidence').mkdir(exist_ok=True)
    manifest = {p: sha(b) for p, b in inputs.items()}
    (output / 'evidence/EXACT_B4_QA_INPUTS.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('EXACT_B4_QA_TREE = PASS; no installable build created')
    print('Run: node --test ' + str(output / 'qa') + '/b4*.test.mjs')


if __name__ == '__main__':
    main()
