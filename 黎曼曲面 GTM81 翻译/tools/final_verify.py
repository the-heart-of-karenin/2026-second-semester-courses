from pathlib import Path
import pymupdf as fitz,re,json,hashlib,datetime
r=Path('黎曼曲面 GTM81 翻译');q=r/'source/final-qa';p=r/'黎曼曲面讲义_中文译稿.pdf';d=fitz.open(p)
log=(r/'LaTeX/build/main.log').read_text(encoding='utf-8',errors='replace')
issues=[x for x in log.splitlines() if any(y in x for y in ['Overfull','Missing character','undefined','Warning'])]
print('PAGES',len(d),'WARNINGS',issues)
for key in ['27.2','B.9','数学研究生教材丛书目录']:
 print(key,[i+1 for i,page in enumerate(d) if key in page.get_text()])
for n in [107,118,137]:
 d[n-1].get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(q/f'verified-final-{n}.png')
report={'time':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'file':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pdf_pages':len(d),'numbered_body_entries':392,'exercises':105,'reference_entries':len(re.findall(r'\\item\[', (r/'LaTeX/sections/references.tex').read_text(encoding='utf-8'))),'series_entries':len(re.findall(r'\\item ', (r/'LaTeX/sections/series.tex').read_text(encoding='utf-8'))),'subject_index_entries':len(re.findall(r'\\idx\{', (r/'LaTeX/sections/index.tex').read_text(encoding='utf-8'))),'compile_warnings':issues,'visual_sample_pages':[1,3,5,7,9,10,11,20,23,38,44,67,69,79,85,93,96,105,106,107,111,114,117,118,120,124,127,132,137],'full_line_by_line_proofread':False}
(q/'final-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
