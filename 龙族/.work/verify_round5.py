from pathlib import Path
import hashlib,json,re
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader
import pypdfium2 as pdfium

root=Path(__file__).resolve().parent.parent;work=root/'.work';qa=work/'qa_round5';qa.mkdir(exist_ok=True)
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
assert hashlib.sha256(Path(manifest['source']).read_bytes()).hexdigest()==manifest['sha256']
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
all_results=[]
for i in range(2):
    book=manifest['books'][i];bookid=book['id'];end=book['translated_through_line'];source=json.loads((work/'source'/f'{bookid}.json').read_text(encoding='utf-8'))
    records={}
    for file in sorted((work/'translations').glob(bookid+'_*.tsv')):
        for row in file.read_text(encoding='utf-8').splitlines():
            if row.strip():
                n,t=row.split('\t',1);n=int(n);assert n not in records and t.strip();records[n]=t
    expected={p['line'] for p in source if p['line']<=end};assert set(records)==expected
    path=root/book['working_docx']
    with ZipFile(path) as z:
        tree=etree.fromstring(z.read('word/document.xml'));found=[]
        for p in tree.findall('.//w:body/w:p',ns):
            marks=p.findall('w:bookmarkStart',ns)
            if marks:
                n=int(marks[0].get('{'+ns['w']+'}name').replace('source_line_',''))
                assert ''.join(p.xpath('.//w:t/text()',namespaces=ns))==records[n];found.append(n)
        assert set(found)==expected and len(found)==len(expected)
    pdf_path=qa/f'book{i+1}.pdf';reader=PdfReader(pdf_path);pdf=pdfium.PdfDocument(str(pdf_path))
    assert len(reader.pages)==len(pdf)
    needles=['Act Ten','Epilogue'] if i==0 else ['Prologue','Act One','Act Two','Act Three']
    headings=[]
    for needle in needles:
        hits=[p+1 for p in range(2,len(reader.pages)) if needle.lower() in reader.pages[p].extract_text()[:300].lower()]
        if hits:headings.append(hits[0])
    picks=sorted({1,2,len(pdf),*headings, max(1,len(pdf)-5)})
    for n in picks:pdf[n-1].render(scale=1.5).to_pil().convert('RGB').save(qa/f'book{i+1}-page-{n}.png')
    all_results.append({'book':bookid,'source_paragraphs':len(records),'pages':len(pdf),'sampled_pages':picks,'docx_paragraphs_match':True,'source_unchanged':True,'docx_sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    book['qa_pages']=len(pdf)
(qa/'verification.json').write_text(json.dumps(all_results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(all_results,ensure_ascii=False))
