from pathlib import Path
import pymupdf as fitz
r=Path('黎曼曲面 GTM81 翻译');q=r/'source/final-qa'
d=fitz.open(r/'黎曼曲面讲义_中文译稿.pdf')
from PIL import Image,ImageOps,ImageDraw
pages=[1,3,5,7,9,11,20,23,38,67,69,79,85,96,105,106,111,114,117,120,124,127,132,137]
thumbs=[]
for n in pages:
 pix=d[n-1].get_pixmap(matrix=fitz.Matrix(1,1));pix.save(q/f'translated-{n:03}.png')
 im=Image.open(q/f'translated-{n:03}.png').convert('RGB');im.thumbnail((397,562))
 box=Image.new('RGB',(417,592),'#bbbbbb');box.paste(im,(10,20));ImageDraw.Draw(box).text((10,4),f'PDF {n}',fill='black');thumbs.append(box)
for k in range(0,len(thumbs),6):
 sheet=Image.new('RGB',(417*3,592*2),'white')
 for j,im in enumerate(thumbs[k:k+6]):sheet.paste(im,((j%3)*417,(j//3)*592))
 sheet.save(q/f'contact-{k//6+1}.png')
s=fitz.open(r'D:\Users\Downloads\Lectures on Riemann Surfaces (Otto Forster) (z-library.sk, 1lib.sk, z-lib.sk).pdf')
for n in [223,253,254,233,234,235,236,237,238,239,240]:
 s[n-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(q/f'original-{n}.png')
