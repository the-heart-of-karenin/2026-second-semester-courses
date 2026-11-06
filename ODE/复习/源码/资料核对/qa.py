import pymupdf as f
from PIL import Image,ImageOps,ImageDraw
from pathlib import Path
root=Path('ODE/复习'); qa=root/'源码/build/qa';qa.mkdir(parents=True,exist_ok=True)
for j,p in enumerate(root.glob('*.pdf')):
 d=f.open(p); print(j,p.name,len(d))
 text=''.join(x.get_text() for x in d)
 (qa/f'doc-{j}.txt').write_text(text,encoding='utf-8')
 for start in range(0,len(d),8):
  sheet=Image.new('RGB',(1000,4*730),'#dddddd'); draw=ImageDraw.Draw(sheet)
  for i in range(start,min(start+8,len(d))):
   pm=d[i].get_pixmap(matrix=f.Matrix(.8,.8)); im=Image.frombytes('RGB',[pm.width,pm.height],pm.samples); im.thumbnail((480,700))
   x=((i-start)%2)*500;y=((i-start)//2)*730
   sheet.paste(im,(x+10,y+25));draw.text((x+10,y+5),str(i+1),fill='black')
  sheet.save(qa/f'doc-{j}-{start+1}.png')
 for k in [0,len(d)//2,len(d)-1]: d[k].get_pixmap(matrix=f.Matrix(1.2,1.2)).save(qa/f'full-{j}-{k+1}.png')
