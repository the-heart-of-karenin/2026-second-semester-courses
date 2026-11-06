import pymupdf as f
from pathlib import Path
b=f.open(next(Path('D:/Users/Downloads').glob('高等数学例题与习题集 4*.pdf')))
for n in [143,144,267,268]: b[n-1].get_pixmap(matrix=f.Matrix(3,3)).save(f'ODE/复习/源码/资料核对/clear-{n}.png')
