from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent.parent;work=root/'.work';qa=work/'qa_round5'
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
verification=json.loads((qa/'verification.json').read_text(encoding='utf-8'))
visual=json.loads((qa/'visual-sample-review.json').read_text(encoding='utf-8'))
for item in verification:
    assert item['docx_paragraphs_match'] and item['source_unchanged']
    assert set(item['sampled_pages'])<=set(visual[item['book']])
    doc=root/next(b['working_docx'] for b in manifest['books'] if b['id']==item['book'])
    assert hashlib.sha256(doc.read_bytes()).hexdigest()==item['docx_sha256']
    next(b for b in manifest['books'] if b['id']==item['book'])['qa_status']='spot_checked'
previous=manifest.get('last_completed_round');history=manifest.setdefault('round_history',[])
if previous and previous not in history:history.append(previous)
manifest['last_completed_round']={'acts':['I:10','II:1','II:2','II:3'],'includes':['I:Epilogue','II:Prologue'],'ranges':{'01':[4801,5456],'02':[5599,6917]},'qa_dir':'qa_round5','status':'translated_and_sample_checked'}
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
books=manifest['books'];total=sum(len(''.join(x['zh'].split())) for b in books for x in json.loads((work/'source'/f"{b['id']}.json").read_text(encoding='utf-8')))
translated=sum(b.get('translated_source_nonwhitespace_chars',0) for b in books);words=sum(b.get('english_words',0) for b in books)
counts={r['book']:r for r in verification}
progress=f'''# 翻译进度

更新时间：2026年10月27日。本轮完成第一册第十幕及尾声，第二册序幕及第一至第三幕。

| 册 | 当前状态 |
| --- | --- |
| Ⅰ 火之晨曦 | 全文已译，包含尾声；独立 Word 文件已保存。 |
| Ⅱ 悼亡者之瞳 | 序幕及第一至第三幕已译；第四幕及之后待译。 |
| Ⅲ 黑月之潮 上、中、下 | 正文已分册整理，尚未翻译。 |

累计已译原文非空白字符约 {translated:,}，译文约 {words:,} 英文词，约占五册已整理正文的 {translated/total:.1%}。此比例按原文字符计算。

- 第一册：`{books[0]['working_docx']}`，{counts['01']['pages']}页。
- 第二册工作稿：`{books[1]['working_docx']}`，{counts['02']['pages']}页。
- 术语表：`术语对照.md`，覆盖目前已译内容。

按用户要求精简检查：自动核验已译源段覆盖及 Word 段落文本，并在渲染后抽查了少量页面；没有逐页检查。源 TXT 哈希与项目初始记录一致。第一册上一工作稿备份在 `.work/archive/01_through_4800.docx`。

下次从第二册第四幕（原 TXT 第6918行）接续。`.work/manifest.json` 与 `.work/translations/` 保存译文进度。
'''
(root/'翻译进度.md').write_text(progress,encoding='utf-8')
old=root/'01_火之晨曦_英文工作稿.docx'
if old.exists():
    archived=work/'archive'/'01_through_4800.docx'
    assert archived.exists() and hashlib.sha256(old.read_bytes()).digest()==hashlib.sha256(archived.read_bytes()).digest()
    old.unlink()
print(json.dumps({'total_source_chars':translated,'english_words':words,'progress_fraction':translated/total,'pages':[r['pages'] for r in verification]},ensure_ascii=False))
