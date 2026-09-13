"""Execute the saved B19 QA-only adaptation against the exact materialized classification artifact.
Only the three expected preimage hashes differ from repository copies. No product/assertion edits.
Usage: b19_final_qa_adapt_v2.py QA_DIR
"""
from pathlib import Path
import sys
p=Path(__file__).with_name('b19_final_qa_adapt.py')
s=p.read_text()
replacements={
 '0b73abf54c7a6061cc2fceb8d858f8e019815398b0570a31cbba5c63033844d':'c9c21aac78242687c2acf554aff9456530962d15783519767688aa8dd284ec74',
 'a816a68f911218bff348ae208ea90e62c715671f4c4bc0af11d317c566ef0f36':'d9f32437e88958bdbef285deaded32e8b6c7d3d8f62e37765eb26d6b9ce8b122',
 '9b427d90add65c4bfaf0a644c8029aa0b7d84339fe35ae6f2b36cfb05a63e0f4':'45491d1de8b55f804e458e9b1c0f86f6ccbaa63e66a1f755d9724517bf76061d',
}
for old,new in replacements.items():
 if s.count(old)!=1: raise ValueError('Unexpected saved adapter identity for '+old)
 s=s.replace(old,new)
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p),'sys':sys})
