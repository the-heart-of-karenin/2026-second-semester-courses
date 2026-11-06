from pathlib import Path
import json,re,hashlib,argparse

root=Path(__file__).resolve().parents[1]
work=root/'.work'
parser=argparse.ArgumentParser()
parser.add_argument('--qa-dir',default='qa_round4')
parser.add_argument('--start',type=int,default=3680)
parser.add_argument('--through',type=int,default=4800)
parser.add_argument('--acts',type=int,nargs='+',default=[8,9])
args=parser.parse_args()
qa=work/args.qa_dir
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
verification=json.loads((qa/'verification.json').read_text(encoding='utf-8'))
delta=json.loads((qa/'visual-delta.json').read_text(encoding='utf-8'))
primary=json.loads((qa/'primary-visual-review.json').read_text(encoding='utf-8'))
assert verification['docx_paragraph_text_matches'] and verification['pdf_body_text_matches']
assert manifest['books'][0]['translated_through_line']==args.through
covered=set(delta['identical_to_previously_inspected_pages'])|set(primary['pages'])
reports=[]
for path in sorted(qa.glob('visual-review-*.md')):
    match=re.fullmatch(r'visual-review-(\d+)-(\d+)\.md',path.name)
    if not match:continue
    assert path.stat().st_size>100
    lo,hi=map(int,match.groups())
    covered.update(range(lo,hi+1));reports.append(path.name)
assert covered==set(range(1,verification['pages']+1)),f'Unreviewed pages: {set(range(1,verification["pages"]+1))-covered}'
docx=root/manifest['books'][0]['working_docx']
verification['visual_inspection']='Passed: new or changed pages individually inspected; unchanged pages pixel-identical to previously inspected images.'
verification['visual_review_reports']=reports
verification['docx_sha256']=hashlib.sha256(docx.read_bytes()).hexdigest()
(qa/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
new_sections=[s for s in verification['sections'] if s['section'] in ['Act '+{1:'One',2:'Two',3:'Three',4:'Four',5:'Five',6:'Six',7:'Seven',8:'Eight',9:'Nine',10:'Ten'}[a] for a in args.acts]]
new_paragraphs=sum(s['paragraphs'] for s in new_sections)
new_chars=sum(s['source_nonwhitespace_characters'] for s in new_sections)
previous=manifest.get('last_completed_round')
history=manifest.setdefault('round_history',[])
if previous and previous not in history:history.append(previous)
manifest['last_updated']='2026-10-27'
manifest['last_completed_round']={'acts':args.acts,'source_lines':[args.start,args.through],'source_paragraphs':new_paragraphs,'source_nonwhitespace_characters':new_chars,'status':'translated_reviewed_rendered_verified','qa_dir':args.qa_dir}
manifest['books'][0]['qa_status']='passed'
manifest['books'][0]['qa_pages']=verification['pages']
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
progress=root/'翻译进度.md'
txt=progress.read_text(encoding='utf-8').replace('排版检查：待运行。',f'排版检查：已用本机 Microsoft Word 导出并渲染{verification["pages"]}页。新增及修改页已逐页检查，未修改的页面与上一轮已检查图片逐像素一致。未发现截字、重叠、缺字或异常空白页。{manifest["books"][0]["translated_source_paragraphs"]:,}个原文非空段全部对应，Word正文及渲染后正文与译文记录完全一致。标准渲染器因缺少 LibreOffice 不可用，改用 Word 完成版面检查。内部验证图片、PDF和记录位于 `.work/{args.qa_dir}/`。')
txt=txt.replace('本轮新增第八幕',f'本轮共新增{new_paragraphs:,}段，约{new_chars:,}个原文非空白字符。新增第八幕')
txt=txt.replace('此记录仅说明已保存的工作','前一轮Word已备份至 `.work/archive/`；当前文件夹保留一份累计工作稿。\n\n此记录仅说明已保存的工作')
progress.write_text(txt,encoding='utf-8')
print(json.dumps({'round_completed':args.acts,'pages':verification['pages'],'new_source_characters':new_chars,'cumulative_english_words':manifest['books'][0]['english_words'],'next_source_line':args.through+1},ensure_ascii=False))
