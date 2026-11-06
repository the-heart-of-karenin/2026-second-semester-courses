from pathlib import Path
import json, re, shutil, hashlib
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

root=Path(__file__).resolve().parent.parent
work=root/'.work'
manifest=json.loads((work/'manifest.json').read_text(encoding='utf-8'))
config=[dict(id='02',end=9475,title='Dragon Raja II',subtitle='The Mourner’s Eyes',out='02_悼亡者之瞳_英文工作稿.docx',complete=False,
      headings=[(5599,5602,5608),(5952,5955,5961),(6222,6225,6231),(6591,6594,6600),(6918,6921,6927),(7356,7359,7365),(7776,7779,7785),(7991,7994,8000),(8370,8373,8379),(8632,8635,8641),(8866,8869,8875),(9205,9208,9214)])]

def build(c):
    source=json.loads((work/'source'/f"{c['id']}.json").read_text(encoding='utf-8'))
    expected={x['line'] for x in source if x['line']<=c['end']}
    text={}
    for path in sorted((work/'translations').glob(c['id']+'_*.tsv')):
        for row in path.read_text(encoding='utf-8').splitlines():
            if not row.strip(): continue
            n,t=row.split('\t',1); n=int(n)
            assert n not in text and t.strip() and not re.search(r'[\u4e00-\u9fff]',t), (path,n)
            text[n]=t
    assert set(text)==expected, (c['id'], sorted(expected-set(text)), sorted(set(text)-expected))
    doc=Document(); sec=doc.sections[0]
    sec.page_width=Inches(8.5); sec.page_height=Inches(11)
    sec.top_margin=sec.bottom_margin=Inches(.85); sec.left_margin=sec.right_margin=Inches(.95)
    sec.header_distance=sec.footer_distance=Inches(.35)
    for name in ('Normal','Title','Subtitle','Heading 1','Heading 2','Header','Footer'):
        style=doc.styles[name];style.font.name='Times New Roman';style.font.color.rgb=RGBColor(0,0,0)
        for fonts in style.element.iter(qn('w:rFonts')):
            for attr in list(fonts.attrib):
                if 'theme' in attr.lower(): del fonts.attrib[attr]
        for border in list(style.element.iter(qn('w:pBdr'))): border.getparent().remove(border)
    normal=doc.styles['Normal'];normal.font.size=Pt(11.5)
    pf=normal.paragraph_format;pf.line_spacing=1.15;pf.space_after=Pt(3);pf.first_line_indent=Inches(.2);pf.widow_control=True
    for name,size in [('Title',30),('Subtitle',17),('Heading 1',20),('Heading 2',15)]:
        st=doc.styles[name];st.font.size=Pt(size);st.paragraph_format.first_line_indent=Inches(0);st.paragraph_format.keep_with_next=True
    doc.styles['Heading 1'].paragraph_format.page_break_before=True
    doc.styles['Heading 2'].paragraph_format.space_after=Pt(12)
    for value,style in [(c['title'],'Title'),(c['subtitle'],'Subtitle'),('Jiang Nan',None)]:
        p=doc.add_paragraph(value,style=style);p.paragraph_format.first_line_indent=Inches(0);p.paragraph_format.space_after=Pt(16)
    p=doc.add_paragraph('English Translation' if c['complete'] else 'English Translation Working Draft');p.paragraph_format.first_line_indent=Inches(0);p.runs[0].bold=True
    p=doc.add_paragraph('Complete text of this volume from the supplied original edition.' if c['complete'] else 'This working draft contains the prologue and Acts One through Eleven. The remainder of this volume is in progress.')
    p.paragraph_format.first_line_indent=Inches(0)
    p=doc.add_paragraph('Translated from the supplied Chinese text. American English. Updated October 29, 2026.');p.paragraph_format.first_line_indent=Inches(0)
    for n,sub,alt in c['headings']:
        p=doc.add_paragraph();p.paragraph_format.first_line_indent=Inches(0);p.paragraph_format.space_after=Pt(3)
        link=OxmlElement('w:hyperlink');link.set(qn('w:anchor'),f'source_line_{n}')
        run=OxmlElement('w:r');t=OxmlElement('w:t');t.text=text[n]+('  '+text[sub] if sub else '');run.append(t);link.append(run);p._p.append(link)
    if c['id']=='01':
        doc.add_page_break()
        for value in ('When you are at your loneliest and most hopeless, a door will open beside you.','Lu Mingfei waited eighteen years. At the lowest, most pathetic moment of his life, the door opened.','This book is dedicated to every hapless kid with a dream.','Jiang Nan'):
            p=doc.add_paragraph(value);p.paragraph_format.first_line_indent=Inches(0);p.paragraph_format.space_after=Pt(14)
    heads={x[0] for x in c['headings']};subs={x[1] for x in c['headings'] if x[1]};alts={x[2] for x in c['headings'] if x[2]}
    for item in source:
        n=item['line']
        if n not in text:continue
        if c['id']=='01' and n==5248:p=doc.add_paragraph(text[n],style='Heading 1')
        elif c['id']=='01' and n==5251:p=doc.add_paragraph(text[n],style='Heading 2')
        elif n in heads:p=doc.add_paragraph(text[n],style='Heading 1')
        elif n in subs:p=doc.add_paragraph(text[n],style='Heading 2')
        elif n in alts:
            p=doc.add_paragraph(text[n]);p.paragraph_format.first_line_indent=Inches(0);p.paragraph_format.space_after=Pt(16);p.paragraph_format.keep_with_next=True
            for r in p.runs:r.italic=True
        else:
            p=doc.add_paragraph(text[n])
            if c['id']=='01' and n in (232,355,388,497,531,536,631,707,730,751,786,816):p.paragraph_format.space_before=Pt(10);p.paragraph_format.first_line_indent=Inches(0)
        mark=OxmlElement('w:bookmarkStart');mark.set(qn('w:id'),str(n));mark.set(qn('w:name'),f'source_line_{n}')
        end=OxmlElement('w:bookmarkEnd');end.set(qn('w:id'),str(n));p._p.insert(0,mark);p._p.append(end)
    h=sec.header.paragraphs[0];h.text=c['title'].upper()+'  ·  '+c['subtitle'].upper()+('' if c['complete'] else '  ·  WORKING DRAFT');h.paragraph_format.first_line_indent=Inches(0);h.runs[0].font.size=Pt(8)
    f=sec.footer.paragraphs[0];f.alignment=2;f.paragraph_format.first_line_indent=Inches(0)
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');f._p.append(field)
    doc.core_properties.title=c['title']+' '+c['subtitle']+' English Translation';doc.core_properties.author='Jiang Nan'
    dest=root/c['out'];doc.save(dest)
    chars=sum(len(re.sub(r'\s','',p['zh'])) for p in source if p['line'] in text)
    words=sum(len(re.findall(r"\b[\w’'-]+\b",t)) for t in text.values())
    book=next(b for b in manifest['books'] if b['id']==c['id'])
    book.update(translated_through_line=c['end'],status='completed' if c['complete'] else 'in_progress',completed_sections=[text[x[0]] for x in c['headings']],translated_source_paragraphs=len(text),translated_source_nonwhitespace_chars=chars,english_words=words,working_docx=dest.name,next_line=None if c['complete'] else c['end']+1,qa_dir='qa_round7',qa_status='pending')
    return {'book':c['id'],'paragraphs':len(text),'source_chars':chars,'english_words':words,'output':str(dest)}

archive=work/'archive';archive.mkdir(exist_ok=True)
old=root/'02_悼亡者之瞳_英文工作稿.docx'
if old.exists():shutil.copy2(old,archive/'02_through_8369.docx')
results=[build(c) for c in config]
manifest['last_updated']='2026-10-29'
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False))
