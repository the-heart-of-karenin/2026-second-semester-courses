from pathlib import Path
import hashlib,json
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import pypdfium2 as pdfium
root=Path(__file__).resolve().parent.parent;work=root/'.work';qa=work/'qa_round8'
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'));book=manifest['books'][1]
assert hashlib.sha256(Path(manifest['source']).read_bytes()).hexdigest()==manifest['sha256']
source=json.loads((work/'source/02.json').read_text(encoding='utf-8'));expected={p['line'] for p in source if p['line']<=9855};records={}
for path in sorted((work/'translations').glob('02_*.tsv')):
    for row in path.read_text(encoding='utf-8').splitlines():
        if row.strip():
            n,t=row.split('\t',1);n=int(n);assert n not in records and t.strip();records[n]=t
assert set(records)==expected
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};docpath=root/book['working_docx']
with ZipFile(docpath) as z:
    tree=etree.fromstring(z.read('word/document.xml'));found=[]
    for p in tree.findall('.//w:body/w:p',ns):
        marks=p.findall('w:bookmarkStart',ns)
        if marks:
            n=int(marks[0].get('{'+ns['w']+'}name').replace('source_line_',''))
            assert ''.join(p.xpath('.//w:t/text()',namespaces=ns))==records[n];found.append(n)
    assert set(found)==expected and len(found)==len(expected)
pdfpath=qa/'book2.pdf';reader=PdfReader(pdfpath);pdf=pdfium.PdfDocument(str(pdfpath));assert len(pdf)==len(reader.pages)
needles=['Act Twelve'];hits={}
for i in range(2,len(reader.pages)):
    text=reader.pages[i].extract_text()[:240]
    for needle in needles:
        if needle in text and needle not in hits:hits[needle]=i+1
    if len(hits)==len(needles):break
samples=sorted({1,2,len(pdf),*hits.values()})
for n in samples:pdf[n-1].render(scale=1.5).to_pil().convert('RGB').save(qa/f'page-{n}.png')
result={'book':'02','source_paragraphs':len(records),'pages':len(pdf),'sampled_pages':samples,'headings':hits,'docx_paragraphs_match':True,'source_unchanged':True,'docx_sha256':hashlib.sha256(docpath.read_bytes()).hexdigest()}
(qa/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
