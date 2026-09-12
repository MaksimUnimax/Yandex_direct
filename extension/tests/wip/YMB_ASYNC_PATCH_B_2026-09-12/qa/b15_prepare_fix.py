"""Exact bounded B15 correction over the already-built B14 ZIP. INTERNAL QA ONLY.
Usage: b15_prepare_fix.py FROZEN_BUNDLE EMPTY_OUTPUT
Reuses all canonical ZIP entry metadata/order and original compression settings.
Verifies full source, one pre/post image and exact resulting ZIP before writes.
"""
from pathlib import Path
import copy,hashlib,io,json,re,sys,zipfile
SHA=lambda b:hashlib.sha256(b).hexdigest()
OLD_ZIP='e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97'
NEW_ZIP='d4bdf57268ac904421797d7aad428c47981cee4c870bc549909696479f91ace9'
OLD_TREE='f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47'
NEW_TREE='7b4db94a527778722ee9bbd7b0d131789128dcaee78451f5886a7bddf1ae183a'
PRE='c8fcf6d36a0573b9134b90edc35efdf988b8d178e3649bc3d116c7c02cf262bf'
POST='baa1729159812f4c70e24498ee269ea7939f86ffb5094a19a5520eec9d47e9e7'
ROOT='ymb-b13-internal-qa-not-for-installation/'
NAME='file_delivery_content.js'
def tree(files):return SHA(''.join(SHA(b)+'  '+n+'\n' for n,b in sorted(files.items())).encode())
def patch(before,diff):
 old=before.decode().splitlines(True);lines=diff.decode().splitlines(True);result=[];cursor=0;pos=2
 assert lines[:2]==['--- a/'+NAME+'\n','+++ b/'+NAME+'\n']
 while pos<len(lines):
  m=re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',lines[pos]);assert m
  start,n,newstart,newn=map(int,m.groups());assert start-1>=cursor
  result+=old[cursor:start-1];cursor=start-1;assert len(result)==newstart-1
  pos+=1;a=b=0
  while pos<len(lines) and not lines[pos].startswith('@@'):
   line=lines[pos];assert line[0] in ' +-'
   if line[0] in ' -':assert old[cursor]==line[1:];cursor+=1;a+=1
   if line[0] in ' +':result.append(line[1:]);b+=1
   pos+=1
  assert (a,b)==(n,newn)
 result+=old[cursor:];return ''.join(result).encode()
def main():
 source,out=map(Path,sys.argv[1:]);assert not out.exists(),'exclusive output required'
 raw=(source/'candidate-internal-qa.zip').read_bytes();assert len(raw)==223380 and SHA(raw)==OLD_ZIP
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  assert z.testzip() is None
  infos=z.infolist();assert len({i.filename for i in infos})==len(infos)
  files={i.filename[len(ROOT):]:z.read(i) for i in infos if not i.is_dir()}
  assert len(files)==67 and tree(files)==OLD_TREE and SHA(files[NAME])==PRE
  diff=(Path(__file__).parent.parent/'evidence/B15_SEND_GATE.diff').read_bytes()
  files[NAME]=patch(files[NAME],diff);assert SHA(files[NAME])==POST and tree(files)==NEW_TREE
  buf=io.BytesIO()
  with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as o:
   for info in infos:o.writestr(copy.copy(info),b'' if info.is_dir() else files[info.filename[len(ROOT):]],compress_type=info.compress_type,compresslevel=9)
 new=buf.getvalue();assert len(new)==223544 and SHA(new)==NEW_ZIP
 with zipfile.ZipFile(io.BytesIO(new)) as z:
  assert z.testzip() is None
  assert {i.filename[len(ROOT):]:z.read(i) for i in z.infolist() if not i.is_dir()}==files
 out.mkdir(parents=True)
 (out/'candidate-b15-internal.zip').write_bytes(new)
 for name,b in files.items():
  p=out/'candidate'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 (out/'IDENTITY.json').write_text(json.dumps({'package_sha256':NEW_ZIP,'bytes':len(new),'tree_sha256':NEW_TREE,'pre_tree_sha256':OLD_TREE,'changed':[NAME],'unchanged_files':66,'files':67,'release_allowed':False},indent=2)+'\n')
 print('B15_EXACT_ONE_FILE_CORRECTION_PASS',NEW_ZIP,NEW_TREE)
if __name__=='__main__':main()
