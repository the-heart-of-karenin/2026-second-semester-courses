"""检查最终PDF、原题附录与索引，生成供人工检查的页面缩略图。"""
from pathlib import Path
import json,re,math
import pymupdf as fitz
from PIL import Image,ImageDraw,ImageFont
from build import ROOT,DATA

OUT=ROOT.parent/'tmp'/'qa'
OUT.mkdir(parents=True,exist_ok=True)
records=[]
norm=lambda s:re.sub(r'\s+','',s)
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
for folder,title,a,b,_ in DATA:
    doc=fitz.open(ROOT/folder/'main.pdf')
    source=fitz.open(ROOT/folder/'original.pdf')
    start=len(doc)-len(source)
    matches=[norm(doc[start+i].get_text())==norm(source[i].get_text()) for i in range(len(source))]
    assert all(matches),(folder,'source appendix mismatch',matches)
    bad=[]
    for i,p in enumerate(doc):
        for block in p.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for s in line['spans']:
                    x0,y0,x1,y1=s['bbox']
                    if x0 < -1 or y0 < -1 or x1 > p.rect.width+1 or y1 > p.rect.height+1:
                        bad.append([i+1,s['text']])
    assert not bad,(folder,'out-of-page text',bad)
    chosen=list(range(start))+[start]
    w,h=450,650
    sheet=Image.new('RGB',(w*3,h*math.ceil(len(chosen)/3)),(225,228,232))
    draw=ImageDraw.Draw(sheet)
    for j,i in enumerate(chosen):
        pix=doc[i].get_pixmap(matrix=fitz.Matrix(1.0,1.0),alpha=False)
        im=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        im.thumbnail((w-18,h-35))
        x=(j%3)*w+(w-im.width)//2;y=(j//3)*h+28
        sheet.paste(im,(x,y));draw.text(((j%3)*w+10,(j//3)*h+5),f'{folder}  page {i+1}',font=font,fill='black')
    sheet.save(OUT/f'{folder}.png')
    records.append({'group':folder,'source_appendix_pages_verified':len(source),'source_text_exact_match':True,'out_of_page_text':False,'contact_sheet':str(OUT/f'{folder}.png')})
index=fitz.open(ROOT/'main.pdf')
for i,p in enumerate(index):
    p.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(OUT/f'index_{i+1}.png')
links=[link for p in index for link in p.get_links()]
assert len(links)==14,('index links',len(links))
for link in links:
    target=link.get('file') or link.get('uri')
    assert target and (ROOT/target).exists(),('broken index target',target)
report={'all_appendix_pages_verified':sum(x['source_appendix_pages_verified'] for x in records),'index_links_verified':14,'documents':records}
(ROOT/'qa_verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'appendix_pages':report['all_appendix_pages_verified'],'index_links':14,'contact_sheets':len(records),'pages':sum(len(fitz.open(ROOT/x[0]/'main.pdf')) for x in DATA)+len(index)},ensure_ascii=False))
