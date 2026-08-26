import fs from 'node:fs';

const target = process.argv[2];
if (!target || !fs.existsSync(target)) throw new Error(`M14_STABILITY_TARGET_MISSING ${target || '<empty>'}`);

const needle = "  await popup.waitForFunction((expected) => document.getElementById('conversationMeta')?.textContent === expected, { timeout: 12000 }, CKEY);";
const replacement = `  const ownerStable = await worker.evaluate(async (ownerTabId) => {
    await chrome.tabs.update(ownerTabId, { active: true });
    for (let attempt = 0; attempt < 80; attempt += 1) {
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      if (Number(tabs?.[0]?.id) === Number(ownerTabId)) return true;
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
    return false;
  }, owner.active.id);
  assert(ownerStable === true, 'M14_POPUP_OWNER_ACTIVE_STABILITY_FAIL');
  await popup.reload({ waitUntil: 'load', timeout: 12000 });
  const stableBootstrap = await waitUntil(async () => await popup.evaluate(() => {
    const error = globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ || '';
    const result = globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__ || null;
    if (!error && !result) return null;
    return { error, result, status: document.getElementById('status')?.textContent || '', meta: document.getElementById('conversationMeta')?.textContent || '' };
  }), 'M14_STABLE_POPUP_BOOTSTRAP_OUTCOME_TIMEOUT', 12000, 80);
  if (stableBootstrap.error) throw new Error(\`M14_STABLE_POPUP_BOOTSTRAP_ERROR \${stableBootstrap.error}\`);
  assert(stableBootstrap.result?.attempted === true, \`M14_STABLE_POPUP_BOOTSTRAP_NOT_ATTEMPTED \${JSON.stringify(stableBootstrap)}\`);
  await popup.waitForFunction((expected) => document.getElementById('conversationMeta')?.textContent === expected, { timeout: 12000 }, CKEY);
  console.log('M14_POPUP_OWNER_BOOTSTRAP_STABILITY_PASS');`;

let source = fs.readFileSync(target, 'utf8');
const count = source.split(needle).length - 1;
if (count !== 1) throw new Error(`M14_STABILITY_NEEDLE_COUNT ${count}`);
if (!source.includes('__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__')) throw new Error('M14_STABILITY_REQUIRES_PROVEN_BOOTSTRAP_PATCH');
source = source.replace(needle, replacement);
fs.writeFileSync(target, source, 'utf8');
console.log('M14_POPUP_OWNER_STABILITY_PATCHED');
