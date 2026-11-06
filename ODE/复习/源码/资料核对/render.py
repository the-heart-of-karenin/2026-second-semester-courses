import pymupdf as f
from pathlib import Path
from PIL import Image,ImageDraw
out=Path('ODE/复习/源码/资料核对')
books={'教材':Path('D:/Users/Downloads/微分方程I 101计划 前三章.pdf'),'习题集':next(Path('D:/Users/Downloads').glob('高等数学例题与习题集 4*.pdf'))}
for name,path in books.items():
 d=f.open(path); print(name,len(d))
 for i in range(6,12):
  if i<len(d): d[i].get_pixmap(matrix=f.Matrix(1.4,1.4)).save(str(out/f'{name}-{i+1:03}.png'))
