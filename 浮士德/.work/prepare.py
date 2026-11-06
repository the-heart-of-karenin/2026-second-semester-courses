from pathlib import Path
from pypdf import PdfReader
import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'D:\Users\Downloads\Faust. Part one and part two (Goethe, Johann Wolfgang von, 1749-1832 etc.) (z-library.sk, 1lib.sk, z-lib.sk).pdf')
reader = PdfReader(SOURCE)
pages = []
for n,p in enumerate(reader.pages,1):
    text = p.extract_text(extraction_mode='layout')
    pages.append({'pdf_page':n, 'text':text})
ROOT.joinpath('source_layout.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
ROOT.joinpath('source.txt').write_text('\n\n'.join(f'=== PDF {p["pdf_page"]} ===\n{p["text"]}' for p in pages),encoding='utf-8')
print('pages',len(pages),'words',sum(len(p['text'].split()) for p in pages),'characters',sum(len(p['text']) for p in pages))
for p in pages:
    ls=[s.strip() for s in p['text'].splitlines() if s.strip()]
    print(p['pdf_page'], ' / '.join(ls[:2])[:125], ' | END ', ' / '.join(ls[-2:])[:100])
