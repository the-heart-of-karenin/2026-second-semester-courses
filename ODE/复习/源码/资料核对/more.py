import pymupdf as f
from pathlib import Path
from PIL import Image,ImageDraw
out=Path('ODE/复习/源码/资料核对'); t=f.open('D:/Users/Downloads/微分方程I 101计划 前三章.pdf'); b=f.open(next(Path('D:/Users/Downloads').glob('高等数学例题与习题集 4*.pdf')))
for name,d,nums in [('教材',t,[7,11,27,44,54,64,73,81,105,115,122,130,138]),('习题集',b,[16,39,52,67,86,94,105,127,143,172,190,230,231,240,241,242,250,266])]:
 for n in nums:
  d[n-1].get_pixmap(matrix=f.Matrix(1.7,1.7)).save(str(out/f'{name}-{n:03}.png'))
