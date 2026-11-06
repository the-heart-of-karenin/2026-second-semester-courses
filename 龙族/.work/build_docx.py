from pathlib import Path
import json, re, argparse, shutil
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

root=Path(__file__).resolve().parents[1]
work=root/'.work'
parser=argparse.ArgumentParser()
parser.add_argument('--through',type=int,default=4800)
parser.add_argument('--qa-dir',default='qa_round4')
args=parser.parse_args()
through=args.through
chapters=[(176,179,'Prologue','White Emperor City'),(226,229,'Act One','The Gate to Cassell'),(976,979,'Act Two','Golden Eyes'),(1448,1451,'Act Three','The Dictator'),(1817,1820,'Act Four','The Bronze City'),(2257,2260,'Act Five','Dragon Shadow'),(2630,2633,'Act Six','Star and Flower'),(3252,3255,'Act Seven','The Little Brother'),(3680,3683,'Act Eight','The Big Brother'),(4302,4305,'Act Nine','Dragon Tomb')]
chapters=[x for x in chapters if x[0]<=through]
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
source=json.loads((work/'source'/'01.json').read_text(encoding='utf-8'))
translation={}
for path in sorted((work/'translations').glob('01_*.tsv')):
    for row in path.read_text(encoding='utf-8').splitlines():
        if not row.strip(): continue
        key,text=row.split('\t',1)
        key=int(key)
        assert key not in translation, f'duplicate {key}'
        assert text.strip(), f'empty {key}'
        assert not re.search(r'[\u4e00-\u9fff]',text), f'Chinese text in {key}'
        translation[key]=text
expected={p['line'] for p in source if p['line']<=through}
assert set(translation)==expected, f'missing {sorted(expected-set(translation))}, extra {sorted(set(translation)-expected)}'

doc=Document()
sec=doc.sections[0]
sec.page_width=Inches(8.5);sec.page_height=Inches(11)
sec.top_margin=sec.bottom_margin=Inches(.85)
sec.left_margin=sec.right_margin=Inches(.95)
sec.header_distance=sec.footer_distance=Inches(.35)
for name in ('Normal','Title','Subtitle','Heading 1','Heading 2','Header','Footer'):
    style=doc.styles[name]
    style.font.name='Times New Roman'
    style.font.color.rgb=RGBColor(0,0,0)
    style.element.get_or_add_rPr().append(OxmlElement('w:lang'))
    style.element.rPr[-1].set(qn('w:val'),'en-US')
    for fonts in style.element.iter(qn('w:rFonts')):
        for attr in list(fonts.attrib):
            if 'theme' in attr.lower(): del fonts.attrib[attr]
    for border in list(style.element.iter(qn('w:pBdr'))):
        border.getparent().remove(border)
normal=doc.styles['Normal']
normal.font.size=Pt(11.5)
pf=normal.paragraph_format
pf.line_spacing=1.15;pf.space_after=Pt(3);pf.first_line_indent=Inches(.2)
pf.widow_control=True
for name,size in [('Title',30),('Subtitle',17),('Heading 1',20),('Heading 2',15)]:
    s=doc.styles[name];s.font.size=Pt(size)
    s.paragraph_format.first_line_indent=Inches(0)
    s.paragraph_format.keep_with_next=True
doc.styles['Heading 1'].paragraph_format.page_break_before=True
doc.styles['Heading 2'].paragraph_format.space_after=Pt(16)

for text,style in [('Dragon Raja I','Title'),('The Blazing Dawn','Subtitle'),('Jiang Nan',None)]:
    p=doc.add_paragraph(text,style=style)
    p.paragraph_format.first_line_indent=Inches(0)
    p.paragraph_format.space_after=Pt(16)
p=doc.add_paragraph('English Translation Working Draft')
p.paragraph_format.first_line_indent=Inches(0);p.runs[0].bold=True
p=doc.add_paragraph('This working draft contains the complete prologue and Acts One through Nine. The rest of Volume I and the other four books remain in progress.')
p.paragraph_format.first_line_indent=Inches(0)
p=doc.add_paragraph('Translated from the supplied original edition Chinese text. American English. Updated October 27, 2026.')
p.paragraph_format.first_line_indent=Inches(0)
for start,title_line,act,title in chapters:
    p=doc.add_paragraph()
    p.paragraph_format.first_line_indent=Inches(0)
    p.paragraph_format.space_after=Pt(3)
    link=OxmlElement('w:hyperlink');link.set(qn('w:anchor'),f'source_line_{start}')
    run=OxmlElement('w:r');txt=OxmlElement('w:t');txt.text=f'{act}  {title}'
    run.append(txt);link.append(run);p._p.append(link)
doc.add_page_break()
for text in ('When you are at your loneliest and most hopeless, a door will open beside you.',
             'Lu Mingfei waited eighteen years. At the lowest, most pathetic moment of his life, the door opened.',
             'This book is dedicated to every hapless kid with a dream.',
             'Jiang Nan'):
    p=doc.add_paragraph(text)
    p.paragraph_format.first_line_indent=Inches(0)
    p.paragraph_format.space_after=Pt(14)
for item in source:
    line=item['line']
    if line not in translation: continue
    text=translation[line]
    if line in {x[0] for x in chapters}:
        p=doc.add_paragraph(text,style='Heading 1')
    elif line in {x[1] for x in chapters}:
        p=doc.add_paragraph(text,style='Heading 2')
    else:
        p=doc.add_paragraph(text)
        if line in (232,355,388,497,531,536,631,707,730,751,786,816):
            p.paragraph_format.space_before=Pt(10)
            p.paragraph_format.first_line_indent=Inches(0)
    # Each translated source paragraph, including headings, has an invisible bookmark.
    mark=OxmlElement('w:bookmarkStart');mark.set(qn('w:id'),str(line));mark.set(qn('w:name'),f'source_line_{line}')
    end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(line))
    p._p.insert(0,mark);p._p.append(end)
header=sec.header.paragraphs[0]
header.text='DRAGON RAJA I  ·  THE BLAZING DAWN  ·  WORKING DRAFT'
header.paragraph_format.first_line_indent=Inches(0)
header.runs[0].font.size=Pt(8)
footer=sec.footer.paragraphs[0];footer.alignment=2
footer.paragraph_format.first_line_indent=Inches(0)
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footer._p.append(field)
doc.core_properties.title='Dragon Raja I The Blazing Dawn English Translation Working Draft'
doc.core_properties.author='Jiang Nan'
doc.core_properties.subject='Complete prologue and Acts One through Nine; translation in progress'
dest=root/'01_火之晨曦_英文工作稿.docx'
if dest.exists():
    archive=work/'archive'
    archive.mkdir(exist_ok=True)
    old_end=manifest['books'][0]['translated_through_line']
    shutil.copy2(dest,archive/f'01_through_{old_end}.docx')
doc.save(dest)
zh_chars=sum(len(re.sub(r'\s','',p['zh'])) for p in source if p['line'] in translation)
words=sum(len(re.findall(r"\b[\w’'-]+\b",t)) for t in translation.values())
manifest['books'][0].update(translated_through_line=through,status='in_progress',completed_sections=[x[2] for x in chapters],translated_source_paragraphs=len(translation),translated_source_nonwhitespace_chars=zh_chars,english_words=words,working_docx=dest.name,next_line=through+1,qa_dir=args.qa_dir,qa_status='pending')
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
total_chars=sum(len(re.sub(r'\s','',p['zh'])) for b in manifest['books'] for p in json.loads((work/'source'/f"{b['id']}.json").read_text(encoding='utf-8')))
report=f'''# 翻译进度

更新时间：2026年10月27日。当前为进行中的翻译项目，尚未完成五册。

| 册 | 当前状态 |
| --- | --- |
| Ⅰ 火之晨曦 | 序章、第一至第九幕全文已译；第十幕至结尾待译。 |
| Ⅱ 悼亡者之瞳 | 正文已分册整理，尚未翻译。 |
| Ⅲ 黑月之潮 上 | 正文已分册整理，尚未翻译。 |
| Ⅲ 黑月之潮 中 | 正文已分册整理，尚未翻译。 |
| Ⅲ 黑月之潮 下 | 正文已分册整理，尚未翻译。 |

已译原文非空白字符约 {zh_chars:,}，译文约 {words:,} 英文词；约占五册已整理正文的 {zh_chars/total_chars:.1%}。此比例按原文字符计，不代表校对质量评分。

已保存译文工作稿：`{dest.name}`。

本轮新增第八幕《哥哥》、第九幕《龙墓》，原 TXT 第3680—4800行（含段间空行）。累计范围第176—{through}行，逐个非空段对应核验。接续位置：第{through+1}行，第十幕《七宗罪》。`.work/manifest.json` 和 `.work/translations/` 保存分册范围与译文，可从此处继续，不能重跑 prepare.py 覆盖进度。

术语表：`术语对照.md`，当前覆盖已译部分并区分外文姓名待复核项。工作稿不视为第一册全本；后续汇入同册后再生成最终文件。

排版检查：待运行。

此记录仅说明已保存的工作，不表示结束对话后会在后台继续运行。
'''
(root/'翻译进度.md').write_text(report,encoding='utf-8')
print(json.dumps({'output':str(dest),'source_paragraphs':len(translation),'source_characters':zh_chars,'english_words':words,'all_books_source_characters':total_chars},ensure_ascii=False))
