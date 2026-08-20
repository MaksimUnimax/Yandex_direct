import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../src');
const source=fs.readFileSync(path.join(root,'content_script.js'),'utf8');

function fn(name) {
  const marker=`function ${name}(`;
  const start=source.indexOf(marker);
  assert.notEqual(start,-1,`missing function ${name}`);
  let brace=source.indexOf('{',start), depth=0, string=null, escape=false;
  for(let i=brace;i<source.length;i++){
    const c=source[i];
    if(string){
      if(escape){escape=false;continue;}
      if(c==='\\'){escape=true;continue;}
      if(c===string) string=null;
      continue;
    }
    if(c==='"'||c==="'"||c==='`'){string=c;continue;}
    if(c==='{') depth++;
    if(c==='}' && --depth===0) return source.slice(start,i+1);
  }
  throw new Error(`unterminated ${name}`);
}

test('Manual action is Bridge-owned external Shadow DOM and does not depend on native Copy',()=>{
  assert.match(source,/attachShadow\(\{ mode: "open" \}\)/);
  assert.match(source,/BB2ProvenWritingCapture\.candidateBlocks\(document\)/);
  assert.doesNotMatch(source,/blockForCopy\(/);
  assert.match(source,/data-ymb-owned/);
  assert.match(source,/pointerEvents: "none"/);
  assert.match(source,/className = "ymb-action"/);
  assert.match(source,/textContent = BB2ManualControls\.ACTION_LABEL/);
});

test('Manual click captures the complete block and delegates validation to worker',()=>{
  const body=fn('onManualAction');
  assert.match(body,/BB2ProvenWritingCapture\.textFromBlock\(block\)/);
  assert.match(body,/type: "WS_EXECUTE_MANUAL_BLOCK"/);
  assert.match(body,/block_text: fullBlockText/);
  assert.doesNotMatch(body,/parseCommand|normalizeCommand|isCommandText/);
});

test('Native Copy is never mutated or used as the lifecycle owner of Яндекс action',()=>{
  assert.doesNotMatch(source,/querySelector(All)?\([^)]*copy/i);
  assert.doesNotMatch(source,/aria-label[^\n]*(copy|копир)/i);
  assert.doesNotMatch(source,/nativeCopy|copyButton/i);
});

test('External action identity is block-owned and survives unrelated DOM mutations',()=>{
  assert.match(source,/const actionByBlock = new Map\(\)/);
  assert.match(source,/if \(!actionByBlock\.has\(block\)\) createAction\(block\)/);
  assert.match(source,/if \(!live\.has\(block\) \|\| !block\.isConnected\)/);
});

test('Status plaque uses fixed top-right 18px and stable named slots',()=>{
  assert.match(source,/right: 18px; top: 18px/);
  for(const key of ['operation-state','composer-occupied','autorun-state','picker-state']) assert.match(source,new RegExp(key));
  assert.match(source,/data-status-key/);
});

test('Claimed delivery protects occupied composer and commits before Send',()=>{
  const body=fn('handleClaimedOutbox');
  assert.match(body,/currentText\.trim\(\) && currentText !== entry\.report_text/);
  assert.match(body,/BB2ComposerSend\.setComposerText\(composer, entry\.report_text\)/);
  const commit=body.indexOf('markCommitted(entry)');
  const click=body.indexOf('sendButton.click()');
  assert.ok(commit>=0 && click>commit,'commit boundary must happen before Send click');
});

test('Committed recovery is watch-only and contains no refill or Send click',()=>{
  const body=fn('handleCommittedOutbox');
  assert.doesNotMatch(body,/setComposerText|\.click\(/);
  assert.match(body,/BB2ComposerSend\.composerReady/);
  assert.match(body,/completeOutbox/);
});

test('Autorun only watches protocol of immutable active service',()=>{
  const scan=fn('scanAutorun');
  assert.match(scan,/protocolForService\(activeAutoWatch\.active_service\)/);
  assert.match(scan,/protocol\.isCommandText\(text\)/);
  assert.match(scan,/type: "WS_AUTO_COMMAND"/);
  assert.match(scan,/run_id: activeAutoWatch\.run_id/);
});


test('External action placement and lifetime stay independent from native Copy',()=>{
  const position=fn('actionPosition');
  assert.match(position,/const gap = 10;/);
  assert.match(position,/let left = rect\.right \+ gap/);
  const refresh=fn('refreshActions');
  assert.match(refresh,/if \(!actionByBlock\.has\(block\)\) createAction\(block\)/);
  assert.doesNotMatch(refresh,/copy|Copy|копир/i);
  const manual=fn('setManualState');
  assert.match(manual,/button\.remove\(\)/);
  assert.match(manual,/actionByBlock\.clear\(\)/);
});
