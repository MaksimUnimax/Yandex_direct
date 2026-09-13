# B19 owner authorization for live provider smoke tests

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`

Owner instruction in active validation session: `делай тесты не смотря на квоты`.

Interpretation for this owner-smoke session:

- live Yandex Search provider calls are explicitly authorized;
- quota/cost is not a stop condition for the remaining owner tests;
- tests must still remain bounded, observable and attributable to explicit Manual commands;
- no background polling is authorized;
- no automatic retries are authorized;
- existing job: `owner-smoke-016-01`;
- local owner-smoke tests completed before this authorization: TEST-01 through TEST-09, all PASS, provider calls = 0.

Next live test: TEST-10, one Manual `submit` for `owner-smoke-016-01`.
