from pathlib import Path
import subprocess,json,re,sys,pdfplumber,pypdfium2 as pdfium
from PIL import Image,ImageDraw

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
R=ROOT/'render';P=R/'word_preview.pdf'
BIN=Path(r'C:\Users\HUAWEI\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin')
outliers=[];empty=[];texts=[]
with pdfplumber.open(P) as pdf:
    page_count=len(pdf.pages)
    for i,p in enumerate(pdf.pages,1):
        w=p.width;h=p.height;chars=p.chars
        if not chars:empty.append(i)
        texts.append(''.join(x['text'] for x in chars))
        for x in chars:
            b=[x[k] for k in ['x0','top','x1','bottom']]
            if b[0]<20 or b[1]<20 or b[2]>w-20 or b[3]>h-12:outliers.append([i,x['text'],b])
        p.close()
joined='\n'.join(texts)
compact=re.sub(r'\s+','',joined)
audit={'rendered_pages':page_count,'empty_pages':empty,'page_bounds_violations':outliers,'replacement_glyphs':joined.count('\ufffd'),'scene_labels_in_render':len(set(re.findall(r'第(\d+)场',compact))),'foreign_quote_checks':{s:s in compact for s in ['EritissicutDeus','Sanctasimplicitas','Diesirae','Chacun','Sorge','Knittelvers','Ach!']}}
ROOT.joinpath('layout_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2),flush=True)
assert not empty and not outliers and not audit['replacement_glyphs']

final=R/'final';final.mkdir(exist_ok=True)
pdf=pdfium.PdfDocument(str(P))
for i in range(len(pdf)):
    page=pdf[i];bmp=page.render(scale=1300/page.get_height());im=bmp.to_pil()
    im.save(final/f'page-{i+1:03d}.png');page.close();bmp.close()
pdf.close()
files=sorted(final.glob('page-*.png'))
assert len(files)==page_count
sheets=final/'sheets';sheets.mkdir(exist_ok=True)
for start in range(0,len(files),20):
    sheet=Image.new('RGB',(1000,1460),'#dddddd');d=ImageDraw.Draw(sheet)
    for j,p in enumerate(files[start:start+20]):
        im=Image.open(p).convert('RGB');im.thumbnail((194,270))
        x=(j%4)*250+(250-im.width)//2;y=(j//4)*292+18
        sheet.paste(im,(x,y));d.text(((j%4)*250+9,(j//4)*292+2),p.stem,fill='black')
    sheet.save(sheets/f'sheet-{start//20+1:02d}.jpg',quality=90)
print('Final page PNGs',len(files),'overview sheets',len(list(sheets.glob('*.jpg'))),flush=True)
