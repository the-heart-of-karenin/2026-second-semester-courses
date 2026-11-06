from pathlib import Path
import json,re,hashlib,argparse
from zipfile import ZipFile
from lxml import etree
from pypdf import PdfReader

root=Path(__file__).resolve().parents[1]
work=root/'.work'
parser=argparse.ArgumentParser()
parser.add_argument('--qa-dir',default='qa_round4')
args=parser.parse_args()
qa=work/args.qa_dir
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
book=manifest['books'][0]
through=book['translated_through_line']
records={}
for file in sorted((work/'translations').glob('01_*.tsv')):
    for row in file.read_text(encoding='utf-8').splitlines():
        if row.strip():
            line,en=row.split('\t',1);line=int(line)
            assert line not in records, f'duplicate {line}'
            records[line]=en
source=json.loads((work/'source'/'01.json').read_text(encoding='utf-8'))
expected={p['line'] for p in source if p['line']<=through}
assert set(records)==expected, f'coverage error: {sorted(expected-set(records))}'
docx=root/manifest['books'][0]['working_docx']
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(docx) as z:
    tree=etree.fromstring(z.read('word/document.xml'))
    actual=[]
    for p in tree.findall('.//w:body/w:p',ns):
        marks=p.findall('w:bookmarkStart',ns)
        if marks:
            line=int(marks[0].get('{'+ns['w']+'}name').replace('source_line_',''))
            txt=''.join(p.xpath('.//w:t/text()',namespaces=ns))
            assert txt==records[line],line
            actual.append(line)
    assert set(actual)==expected and len(actual)==len(expected)
    styles=etree.fromstring(z.read('word/styles.xml'))
    assert not styles.xpath('//w:style[@w:styleId="Title"]/w:pPr/w:pBdr',namespaces=ns)
reader=PdfReader(qa/'working-draft.pdf')
page_text=[]
for i,page in enumerate(reader.pages):
    txt=page.extract_text()
    assert '\ufffd' not in txt, i+1
    if i<2: continue
    txt=txt.replace('DRAGON RAJA I  ·  THE BLAZING DAWN  ·  WORKING DRAFT','')
    txt=re.sub(r'\n\s*'+str(i+1)+r'\s*$','',txt)
    page_text.append(txt)
norm=lambda text: ''.join(c.lower() for c in text if c.isalpha())
pdf_norm=norm('\n'.join(page_text))
expected_norm=norm('\n'.join(records[k] for k in sorted(records)))
render_matches=pdf_norm==expected_norm
if not render_matches:
    # PDF extraction may insert running headers with different spacing.
    pdf_norm=pdf_norm.replace(norm('DRAGON RAJA I THE BLAZING DAWN WORKING DRAFT'),'')
    render_matches=pdf_norm==expected_norm
if not render_matches:
    first=next((i for i,(a,b) in enumerate(zip(pdf_norm,expected_norm)) if a!=b),min(len(pdf_norm),len(expected_norm)))
    raise AssertionError(f'Rendered text differs at {first}: PDF {pdf_norm[first:first+120]} EXPECTED {expected_norm[first:first+120]}')
assert hashlib.sha256(Path(manifest['source']).read_bytes()).hexdigest()==manifest['sha256']
by_act=[]
for lo,hi,name in [(176,225,'Prologue'),(226,975,'Act One'),(976,1447,'Act Two'),(1448,1816,'Act Three'),(1817,2256,'Act Four'),(2257,2629,'Act Five'),(2630,3251,'Act Six'),(3252,3679,'Act Seven'),(3680,4301,'Act Eight'),(4302,4800,'Act Nine')]:
    keys={k for k in records if lo<=k<=hi}
    if not keys: continue
    by_act.append(dict(section=name,paragraphs=len(keys),source_nonwhitespace_characters=sum(len(re.sub(r'\s','',p['zh'])) for p in source if p['line'] in keys),english_words=sum(len(re.findall(r"\b[\w’'-]+\b",records[k])) for k in keys)))
report=dict(source_unchanged=True,source_paragraph_coverage=f'{len(records)} of {len(expected)} through source line {through}',docx_paragraph_text_matches=True,pdf_body_text_matches=True,pages=len(reader.pages),visual_inspection='pending',next_source_line=through+1,sections=by_act)
(qa/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
