from pathlib import Path
import pymupdf as fitz
from PIL import Image,ImageDraw
r=Path('黎曼曲面 GTM81 翻译');q=r/'source/final-qa'
s=fitz.open(r'D:\Users\Downloads\Lectures on Riemann Surfaces (Otto Forster) (z-library.sk, 1lib.sk, z-lib.sk).pdf')
for n in [116,120,143,163,217,218,233,243]:
 s[n-1].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(q/f'original-{n}.png')
d=fitz.open(r/'黎曼曲面讲义_中文译稿.pdf')
print('Final pages',len(d))
print('WARNINGS')
log=(r/'LaTeX/build/main.log').read_text(encoding='utf-8',errors='replace')
for l in log.splitlines():
 if any(x in l for x in ['Overfull','Missing character','undefined','Warning']):print(l)
for n in [10,44,93,111,117,len(d)]:
 d[n-1].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(q/f'final-{n:03}.png')
# precise locations of corrected formula pages, and back matter.
for key in ['故u为全纯','每个此类自同构','B.9','β(η)','附录','参考文献']:
 print(key,[i+1 for i,p in enumerate(d) if key in p.get_text()])
# high-resolution exercise hint crop
s[222].get_pixmap(matrix=fitz.Matrix(4,4),clip=fitz.Rect(60,150,400,225)).save(q/'hint-27-2.png')
