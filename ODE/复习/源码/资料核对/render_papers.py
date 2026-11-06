import pymupdf as f
from pathlib import Path
from PIL import Image
p=Path('ODE/历年试题')
for name in ['paper2-01','paper2-02']:
 d=f.open(p/(name+'.pdf'));print(name,len(d))
 for i,page in enumerate(d):page.get_pixmap(matrix=f.Matrix(1.7,1.7)).save(str(p/f'{name}-{i+1}.png'))
im=Image.open(p/'paper1-02.jpg');im.rotate(90,expand=True).save(p/'paper1-02-upright.png')
