import fs from 'node:fs';
import process from 'node:process';

const target = process.argv[2];
if (!target || !fs.existsSync(target)) throw new Error(`W14_PATCH_TARGET_MISSING ${target || '<empty>'}`);

const needle = "  await popup.waitForFunction((expected) => document.getElementById('conversationMeta')?.textContent === expected, { timeout: 12000 }, CKEY);";
const insert = `  const bootstrap = await waitUntil(async () => await popup.evaluate(() => {
    const error = globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_ERROR__ || '';
    const result = globalThis.__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__ || null;
    if (!error && !result) return null;
    return { error, result, status: document.getElementById('status')?.textContent || '' };
  }), 'POPUP_BOOTSTRAP_OUTCOME_TIMEOUT', 12000, 80);
  if (bootstrap.error) throw new Error(\`POPUP_BOOTSTRAP_ERROR \${bootstrap.error}\`);
  assert(bootstrap.result?.attempted === true, \`POPUP_BOOTSTRAP_NOT_ATTEMPTED \${JSON.stringify(bootstrap)}\`);
`;

const source = fs.readFileSync(target, 'utf8');
if (!source.includes(needle)) throw new Error('W14_BOOTSTRAP_PATCH_NEEDLE_MISSING');
if (source.includes('__YMB_POPUP_CONTEXT_BOOTSTRAP_RESULT__')) throw new Error('W14_BOOTSTRAP_PATCH_ALREADY_PRESENT');
fs.writeFileSync(target, source.replace(needle, insert + needle));
console.log('W14_PROVEN_BOOTSTRAP_WAIT_PATCHED');
