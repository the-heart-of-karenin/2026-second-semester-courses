from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent.parent;work=root/'.work';qa=work/'qa_round6'
m=json.loads((work/'manifest.json').read_text(encoding='utf-8'));v=json.loads((qa/'verification.json').read_text(encoding='utf-8'));review=json.loads((qa/'visual-sample-review.json').read_text(encoding='utf-8'))
assert v['docx_paragraphs_match'] and v['source_unchanged'] and set(v['sampled_pages'])<=set(review['pages'])
b=m['books'][1];assert b['translated_through_line']==8369
assert hashlib.sha256((root/b['working_docx']).read_bytes()).hexdigest()==v['docx_sha256']
b['qa_status']='spot_checked';b['qa_pages']=v['pages']
previous=m.get('last_completed_round');history=m.setdefault('round_history',[])
if previous and previous not in history:history.append(previous)
m['last_completed_round']={'acts':['II:4','II:5','II:6','II:7'],'ranges':{'02':[6918,8369]},'qa_dir':'qa_round6','status':'translated_and_sample_checked'};m['last_updated']='2026-10-27'
(work/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
books=m['books'];total=sum(len(''.join(x['zh'].split())) for b in books for x in json.loads((work/'source'/f"{b['id']}.json").read_text(encoding='utf-8')))
translated=sum(b.get('translated_source_nonwhitespace_chars',0) for b in books);words=sum(b.get('english_words',0) for b in books)
progress=f'''# 翻译进度

更新时间：2026年10月27日。本轮完成第二册第四至第七幕。

| 册 | 当前状态 |
| --- | --- |
| Ⅰ 火之晨曦 | 全文已译，独立 Word 文件已保存。 |
| Ⅱ 悼亡者之瞳 | 序幕及第一至第七幕已译；第八幕及之后待译。 |
| Ⅲ 黑月之潮 上、中、下 | 正文已分册整理，尚未翻译。 |

累计已译原文非空白字符约 {translated:,}，译文约 {words:,} 英文词，约占五册已整理正文的 {translated/total:.1%}。此比例按原文字符计算。

- 第一册：`{books[0]['working_docx']}`。
- 第二册工作稿：`{books[1]['working_docx']}`，{v['pages']}页。
- 术语表：`术语对照.md`，覆盖目前已译内容。

按用户要求精简检查：自动核验已译源段覆盖及 Word 段落文本，并在渲染后抽查少量页面；没有逐页检查。源 TXT 哈希与项目初始记录一致。第二册上一工作稿备份在 `.work/archive/02_through_6917.docx`。

下次从第二册第八幕（原 TXT 第8370行）接续。`.work/manifest.json` 与 `.work/translations/` 保存译文进度。
'''
(root/'翻译进度.md').write_text(progress,encoding='utf-8')
print(json.dumps({'total_source_chars':translated,'english_words':words,'progress_fraction':translated/total,'pages':v['pages']},ensure_ascii=False))
