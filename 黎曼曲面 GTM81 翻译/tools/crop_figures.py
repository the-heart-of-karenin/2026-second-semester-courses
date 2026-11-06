from pathlib import Path
import pymupdf as fitz
import json
root=Path(__file__).resolve().parents[1]
d=fitz.open(r'D:\Users\Downloads\Lectures on Riemann Surfaces (Otto Forster) (z-library.sk, 1lib.sk, z-lib.sk).pdf')
records=json.loads((root/'source/figure-crops.json').read_text(encoding='utf-8'))
for record in records:
 box=record['box'];out=fitz.open()
 out.new_page(width=box[2]-box[0],height=box[3]-box[1])
 out[0].show_pdf_page(out[0].rect,d,record['pdf_page']-1,clip=fitz.Rect(box))
 out.save(root/'LaTeX'/'figures'/(record['name']+'.pdf'))
