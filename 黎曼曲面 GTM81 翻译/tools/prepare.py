import fitz
from pathlib import Path
p=Path('黎曼曲面 GTM81 翻译/source')
d=fitz.open(r'D:\Users\Downloads\Lectures on Riemann Surfaces (Otto Forster) (z-library.sk, 1lib.sk, z-lib.sk).pdf')
for i in [10,12,16,17]:
 d[i].get_pixmap(matrix=fitz.Matrix(1.6,1.6)).save(str(p/f'original-page-{i+1:03}.png'))
for i in range(len(d)):
 (p/f'page-{i+1:03}.txt').write_text(d[i].get_text(),encoding='utf-8')
