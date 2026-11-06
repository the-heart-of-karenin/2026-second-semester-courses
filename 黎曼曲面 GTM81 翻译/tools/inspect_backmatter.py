import pymupdf as f
from pathlib import Path
d=f.open(r'D:\Users\Downloads\Lectures on Riemann Surfaces (Otto Forster) (z-library.sk, 1lib.sk, z-lib.sk).pdf')
for i in range(244,len(d)):
 t=d[i].get_text().strip().splitlines()
 print(i+1, ' | '.join(t[:5]), ' ... ', ' | '.join(t[-3:]))
