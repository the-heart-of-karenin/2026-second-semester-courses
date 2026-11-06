from pathlib import Path
import json,hashlib,shutil

root=Path(__file__).resolve().parents[1]
work=root/'.work'
qa=work/'qa_round2'
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
verification=json.loads((qa/'verification.json').read_text(encoding='utf-8'))
delta=json.loads((qa/'visual-delta.json').read_text(encoding='utf-8'))
assert verification['docx_paragraph_text_matches'] and verification['pdf_body_text_matches']
assert verification['pages']==112 and manifest['books'][0]['translated_through_line']==2256
reports=['visual-review-46-68.md','visual-review-69-90.md','visual-review-91-112.md']
for filename in reports:
    assert (qa/filename).exists() and (qa/filename).stat().st_size>100
covered=set(delta['identical_to_previously_inspected_pages'])|{1}|set(range(46,113))
assert covered==set(range(1,113))
verification['visual_inspection']='Passed: page 1 inspected by primary agent; pages 2–45 pixel-identical to previously inspected images; pages 46–112 individually inspected by three reviewers.'
verification['visual_review_reports']=reports
docx=root/manifest['books'][0]['working_docx']
verification['docx_sha256']=hashlib.sha256(docx.read_bytes()).hexdigest()
(qa/'verification.json').write_text(json.dumps(verification,ensure_ascii=False,indent=2),encoding='utf-8')
manifest['last_updated']='2026-10-27'
manifest['last_completed_round']={'acts':[2,3,4],'source_lines':[976,2256],'source_paragraphs':1254,'source_nonwhitespace_characters':70463,'status':'translated_reviewed_rendered_verified','qa_dir':'qa_round2'}
manifest['books'][0]['qa_status']='passed'
manifest['books'][0]['qa_pages']=112
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
progress=root/'翻译进度.md'
txt=progress.read_text(encoding='utf-8').replace('排版检查：待运行。','排版检查：已用本机 Microsoft Word 导出并渲染112页。新增及修改页已逐页检查；第2—45页与上一轮已检查的图片逐像素一致。未发现截字、重叠、缺字或异常空白页。2,036个原文非空段全部对应，Word正文及渲染后正文与译文记录完全一致。标准渲染器因缺少 LibreOffice 不可用，改用 Word 完成版面检查。验证图片、内部PDF和检查记录位于 `.work/qa_round2/`。')
txt=txt.replace('本轮新增第二幕','本轮共新增1,254段，约70,463个原文非空白字符。新增第二幕')
txt=txt.replace('此记录仅说明已保存的工作','上一轮仅至第一幕的Word已备份至 `.work/archive/`；当前文件夹保留一份累计工作稿。\n\n此记录仅说明已保存的工作')
progress.write_text(txt,encoding='utf-8')
old=root/'01_火之晨曦_英文工作稿_序章及第一幕.docx'
if old.exists():
    archive=work/'archive';archive.mkdir(exist_ok=True)
    target=archive/'01_through_975.docx'
    assert old.resolve().parent==root.resolve() and target.resolve().is_relative_to(root.resolve())
    if target.exists():
        assert hashlib.sha256(target.read_bytes()).digest()==hashlib.sha256(old.read_bytes()).digest()
        old.unlink()
    else:shutil.move(str(old),str(target))
print(json.dumps({'round_completed':[2,3,4],'docx':str(docx),'pages':112,'glossary':str(root/'术语对照.md'),'next_source_line':2257,'next_act':'第五幕 龙影'},ensure_ascii=False))
