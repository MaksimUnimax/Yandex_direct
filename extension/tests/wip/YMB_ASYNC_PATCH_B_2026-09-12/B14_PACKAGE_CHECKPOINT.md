# B14 package checkpoint — implementation and local execution saved

2026-09-12. The 67-file B13 production tree remains f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47; no production changes.

The exact 53 owner014 file contents already existed as Git objects. They were referenced without rewriting or re-uploading source text into qa/b14_inputs/owner014 (Git tree 72bc1d60b8763448d24ff72c2352bbe5b5551bd6). This removes dependence on a missing uploaded owner ZIP in later QA environments. The saved A baseline SHA256 manifest validates every file. This is baseline source reuse, not a replacement for transporting the final exact ZIP.

The canonical packer was read from qa/e13a-exact-reconstruction-v3, path extension/tests/qa_transport/e13a/canonical_packer_exact.py; its unchanged blob 171a3c99d0c3fb5454a5bc5423c7b4cc5e2da576 is preserved as b14_canonical_packer_exact.py. Only candidate-specific ROOT and EXPECTED_FILES parameters are set by the new wrapper; pack and make_info are unchanged.

Internal candidate ZIP: e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97, 223380 bytes, 67 files. Two packs matched exactly. Fresh extraction matched all 67 source files. Fourteen package/transport guard assertions passed, including corruption, truncation, duplicate/traversal path, metadata, wrong source and symlink rejection.

On the freshly extracted candidate, the unchanged B13 available campaign actually ran: original 118+14, missing coverage 78, full-contract 99, module 254, export 84; all passed, no skips. Node fixtures are NOT Chrome proof. No real Yandex requests.

QA-only incident: initial packaged-suite staging copied qa/inputs but omitted the root QA_INPUTS_README.txt expected by the preserved runner. It failed before product assertions. The wrapper now preserves inherited root QA files and a dedicated guard checks all archived QA inputs. No production or old test was changed to hide this.

Exact new wrapper SHA256: 25a071001679d5c0dcd14e650b919331b86943c1256d629afec587b41f991872.
Exact package-test SHA256: b5082e5e27cf853baa51b2148b868eae2c1bdfab28e659cb6af4089cb9593363.

NEXT: execute the same source-only build on GitHub Actions, download the exact generated package/QA artifact, verify both transport digests, and preserve logs/report/cursor. Do not deliver the internal package to the owner. Do not restart B13 product work.
RELEASE_ALLOWED = NO
INDEPENDENT_GATE = NOT_RUN
BROWSER_RESOURCE = NOT_RUN
