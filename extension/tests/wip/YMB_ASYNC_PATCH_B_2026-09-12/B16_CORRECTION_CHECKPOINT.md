# B16 correction checkpoint

2026-09-12. Exact correction inputs and Node RED/GREEN are now durable in qa/B16_CORRECTION_INPUTS.tar.xz (8184 bytes, SHA256 219b105f09de867a9ccd804c6001183dbbba0805726bba39ce4908585359df11). Archive includes one exact production diff, producer,10 new tests, RED/GREEN/fresh19 logs and SHA256SUMS. Test inputs are internal only, not owner release.

Only file_delivery_content.js changes from B15. Pre baa1729159812f4c70e24498ee269ea7939f86ffb5094a19a5520eec9d47e9e7 -> post655702fa5025e2a4dc87b2d2bb6647cf3b9c69bee88f4017150b35e8f511a9f2. New internal ZIP223870 bytes SHA256 dd6d1ef016d4df3d9b4789cd2806f4d0a36202f93c4655e196e2eeda439f7c73; new67-file tree83ae1351ab057f7cd768243c91060d2dc77e8fe0f5b378055437e47a110012b7. Other66files unchanged. New10 exact-function tests 2PASS/8FAIL ->10PASS; previous9Send assertions retained with required identity fixture -> combined19PASS. Chrome rerun NOT YET COMPLETE.

Use producer only once over ready B15 artifact, preserving package metadata; then reuse its ready output. It reuses B15 primary/supplement tests with exact target guard updated, corrects three expressly documented B16 fixture assumptions, and records all generated hashes. No provider calls, no permissions/version changes.

NEXT = exact Chrome validation of correction, old affected file matrix, new popup/CM/navigation/resource/profile cases.
RELEASE_ALLOWED = NO
