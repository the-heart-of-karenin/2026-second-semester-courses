from pathlib import Path
import json,argparse
import pypdfium2 as pdfium
from PIL import Image, ImageOps, ImageDraw
from pypdf import PdfReader

root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--qa-dir',default='qa_round2')
args=parser.parse_args()
qa=root/args.qa_dir
pdf_path=qa/'working-draft.pdf'
pdf=pdfium.PdfDocument(str(pdf_path))
thumbs=[]
page_info=[]
reader=PdfReader(pdf_path)
for i in range(len(pdf)):
    image=pdf[i].render(scale=1.5).to_pil().convert('RGB')
    image.save(qa/f'page-{i+1}.png')
    thumb=ImageOps.contain(image,(306,396))
    card=Image.new('RGB',(326,426),'#d8d8d8')
    card.paste(thumb,((326-thumb.width)//2,5))
    ImageDraw.Draw(card).text((12,405),f'Page {i+1}',fill='black')
    thumbs.append(card)
    txt=reader.pages[i].extract_text()
    page_info.append(dict(page=i+1,words=len(txt.split()),first=txt[:140],last=txt[-160:]))
for offset in range(0,len(thumbs),12):
    sheet=Image.new('RGB',(326*4,426*3),'white')
    for j,thumb in enumerate(thumbs[offset:offset+12]):sheet.paste(thumb,((j%4)*326,(j//4)*426))
    sheet.save(qa/f'contact-{offset//12+1}.png')
(qa/'page-info.json').write_text(json.dumps(page_info,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pages':len(pdf),'contact_sheets':(len(pdf)+11)//12,'minimum_words_on_body_page':min(x['words'] for x in page_info[1:])}))
