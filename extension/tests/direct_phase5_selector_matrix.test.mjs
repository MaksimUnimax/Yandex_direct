import test from 'node:test';
import assert from 'node:assert/strict';
import { createPhase5Runtime } from './helpers/phase5_runtime_harness.mjs';

const plain = (value) => JSON.parse(JSON.stringify(value));

test('D-02 all Direct JSON methods build exact provider SelectionCriteria', () => {
  const { ctx } = createPhase5Runtime();
  const P = ctx.DirectProtocol;
  const cases = [
    [
      { method: 'listCampaigns', campaignIds: [11, 12] },
      { Ids: [11, 12] }
    ],
    [
      { method: 'listAdGroups', campaignIds: [11], adGroupIds: [21, 22] },
      { CampaignIds: [11], Ids: [21, 22] }
    ],
    [
      { method: 'listAds', campaignIds: [11], adGroupIds: [21], adIds: [31, 32] },
      { CampaignIds: [11], AdGroupIds: [21], Ids: [31, 32] }
    ],
    [
      { method: 'listKeywords', campaignIds: [11], adGroupIds: [21], keywordIds: [41, 42] },
      { CampaignIds: [11], AdGroupIds: [21], Ids: [41, 42] }
    ]
  ];

  for (const [command, expected] of cases) {
    const request = plain(P.buildRequest(command));
    assert.deepEqual(request.body.params.SelectionCriteria, expected, command.method);
    assert.equal(Object.hasOwn(request.body.params.SelectionCriteria, 'CampaignIds') && command.method === 'listCampaigns', false);
  }
});

test('D-02 optional empty selector normalization is idempotent and listCampaigns accepts no IDs', () => {
  const { ctx } = createPhase5Runtime();
  const P = ctx.DirectProtocol;

  const commands = [
    { method: 'listCampaigns' },
    { method: 'listCampaigns', campaignIds: [] },
    { method: 'getCampaignPerformance', dateFrom: '2026-08-01', dateTo: '2026-08-02' },
    { method: 'getCampaignPerformance', dateFrom: '2026-08-01', dateTo: '2026-08-02', campaignIds: [] }
  ];

  for (const command of commands) {
    const first = P.normalizeCommand(command);
    const second = P.normalizeCommand(first);
    assert.deepEqual(plain(second), plain(first));
    assert.doesNotThrow(() => P.buildRequest(second));
  }

  assert.deepEqual(plain(P.buildRequest({ method: 'listCampaigns' }).body.params.SelectionCriteria), {});
});

test('D-02 selector-required methods still reject all-empty selectors', () => {
  const { ctx } = createPhase5Runtime();
  const P = ctx.DirectProtocol;
  for (const command of [
    { method: 'listAdGroups', campaignIds: [], adGroupIds: [] },
    { method: 'listAds', campaignIds: [], adGroupIds: [], adIds: [] },
    { method: 'listKeywords', campaignIds: [], adGroupIds: [], keywordIds: [] }
  ]) {
    assert.throws(() => P.normalizeCommand(command), (error) => error?.code === 'MISSING_SELECTOR');
  }
});
