from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
import json,re,sys,collections
sys.path.insert(0,str(Path(__file__).parent))
from translate import CHAPTERS,TERMS

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/'浮士德 第一部与第二部 中文初译.docx'
units=json.loads((ROOT/'edited.json').read_text(encoding='utf-8'))
front=json.loads((ROOT/'frontmatter.json').read_text(encoding='utf-8'))
back=json.loads((ROOT/'appendices.json').read_text(encoding='utf-8'))
doc=Document();sec=doc.sections[0]
sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=Cm(2.1);sec.bottom_margin=Cm(2.0)
sec.left_margin=Cm(2.4);sec.right_margin=Cm(2.2)
sec.header_distance=Cm(0.8);sec.footer_distance=Cm(0.9)

def font(style,name='SimSun',size=11,bold=False):
    style.font.name=name;style.font.size=Pt(size);style.font.bold=bold
    style.font.color.rgb=RGBColor(0,0,0)
    pr=style.element.get_or_add_rPr();fs=pr.find(qn('w:rFonts'))
    if fs is None:fs=OxmlElement('w:rFonts');pr.insert(0,fs)
    for a in ['eastAsia','ascii','hAnsi','cs']:fs.set(qn('w:'+a),name)
    lang=pr.find(qn('w:lang'))
    if lang is None:lang=OxmlElement('w:lang');pr.append(lang)
    lang.set(qn('w:eastAsia'),'zh-CN');lang.set(qn('w:val'),'zh-CN')

normal=doc.styles['Normal'];font(normal)
normal.paragraph_format.line_spacing=Pt(16.5)
normal.paragraph_format.space_after=Pt(6)
normal.paragraph_format.widow_control=True
for nm,size in [('Title',32),('Subtitle',16),('Heading 1',19),('Heading 2',14),('Heading 3',12)]:
    s=doc.styles[nm];font(s,'SimSun',size,nm!='Subtitle')
    s.paragraph_format.space_before=Pt(14);s.paragraph_format.space_after=Pt(9)
    s.paragraph_format.keep_with_next=True
    pr=s.element.get_or_add_pPr()
    for b in list(pr.findall(qn('w:pBdr'))):pr.remove(b)
for nm,size,name in [('Verse',11,'SimSun'),('Stage',10,'KaiTi'),('Speaker',10.5,'SimSun'),('SourceLocator',8.5,'SimSun'),('TOCEntry',10.5,'SimSun'),('Small',9,'SimSun')]:
    s=doc.styles.add_style(nm,WD_STYLE_TYPE.PARAGRAPH);s.base_style=normal;font(s,name,size,nm=='Speaker')
    pf=s.paragraph_format;pf.space_after=Pt(3);pf.line_spacing=Pt(15.5 if nm=='Verse' else 14)
    if nm=='Stage':s.font.italic=True;pf.left_indent=Cm(.5);pf.right_indent=Cm(.4)
    if nm=='Speaker':pf.space_before=Pt(6);pf.space_after=Pt(1);pf.keep_with_next=True
    if nm=='SourceLocator':pf.space_before=Pt(7);pf.space_after=Pt(3);pf.keep_with_next=True;s.font.color.rgb=RGBColor(90,90,90)
    if nm=='TOCEntry':pf.space_after=Pt(1);pf.line_spacing=Pt(14)

# Page numbers are Word fields and update naturally in Word.
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
fr=footer.add_run();fr.font.size=Pt(9)
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');fr._r.addnext(fld)
settings=doc.settings.element
upd=OxmlElement('w:updateFields');upd.set(qn('w:val'),'true');settings.append(upd)
doc.core_properties.title='浮士德 第一部与第二部 中文初译'
doc.core_properties.subject='据卡尔 R 穆勒二〇〇四年英译本转译'
doc.core_properties.author=''
doc.core_properties.keywords='浮士德 歌德 中文 英译本转译'

bookmark_id=1
def bookmark(p,name):
    global bookmark_id
    a=OxmlElement('w:bookmarkStart');a.set(qn('w:id'),str(bookmark_id));a.set(qn('w:name'),name)
    b=OxmlElement('w:bookmarkEnd');b.set(qn('w:id'),str(bookmark_id))
    p._p.insert(0,a);p._p.append(b);bookmark_id+=1

def link(p,text,anchor):
    h=OxmlElement('w:hyperlink');h.set(qn('w:anchor'),anchor);h.set(qn('w:history'),'1')
    r=OxmlElement('w:r');pr=OxmlElement('w:rPr')
    f=OxmlElement('w:rFonts')
    for a in ['ascii','hAnsi','eastAsia']:f.set(qn('w:'+a),'SimSun')
    pr.append(f);c=OxmlElement('w:color');c.set(qn('w:val'),'000000');pr.append(c);r.append(pr)
    t=OxmlElement('w:t');t.text=text;r.append(t);h.append(r);p._p.append(h)

def para(text,style=None):return doc.add_paragraph(text,style)
def heading(text,level=1,anchor=None):
    p=doc.add_heading(text,level)
    if anchor:bookmark(p,anchor)
    return p
def locator(n):
    if 16<=n<=496:label=f'原书第 {n-14} 页'
    elif 9<=n<=14:label='原书第 '+{9:'vii',10:'viii',11:'ix',12:'x',13:'xi',14:'xii'}[n]+' 页'
    else:label=f'原 PDF 第 {n} 页'
    return para('〔'+label+'〕','SourceLocator')

# Title page.
p=doc.add_paragraph();p.paragraph_format.space_after=Pt(80)
p=para('浮士德','Title');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
p=para('第一部与第二部 中文初译','Subtitle');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
for txt in ['约翰 沃尔夫冈 冯 歌德 著','卡尔 R. 穆勒 英译','据二〇〇四年英译本转译']:
    p=para(txt);p.alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_page_break()
heading('底本与译文说明',anchor='edition_note')
para('本稿以所附《Faust: Part One and Part Two》扫描本为底本，原作者为 Johann Wolfgang von Goethe（约翰 沃尔夫冈 冯 歌德），英译者为 Carl R. Mueller（卡尔 R. 穆勒），由 Smith and Kraus 于 2004 年出版。正文及书前、书后材料均按该英译本译出。')
para('本稿为机器辅助中文初译。已清理识别文本、重整人物与台词的对应关系、统一主要专名，并校订部分关键段落；全书尚未完成逐句文学终审。')
para('英译者在原书的翻译说明中明确指出，其底本已有删节：第一部删去“瓦尔普吉斯之夜的梦”，第二部删去第三幕开头的“海伦”场景，另有少量诗行删节。本稿的完整范围为所附英译本。导言中的作品解释及词汇表中的陈述，均保留英译者的观点。')
para('原书引用的德文、拉丁文及其他外语词句保留原文，并附中文释义。参考书目的文献题名保留原文。中文对白按语义分行，保留剧本中的人物、场景与舞台提示。方括号中标为“译注”的文字属于中文稿补充。')
para('正文中的“原书第某页”指底本印刷页码；未印页码的书前、书后材料，以原 PDF 页序定位。目录所列同样是底本页码。图书馆印章、借阅记录、空白页及扫描噪点不作正文。')
doc.add_page_break()
heading('目录',anchor='contents')
para('点击条目可跳转。下列页码对应英文底本。','Small')
for txt,anc in [('出版资料与献辞','publication'),('导言  vii','introduction'),('英译者的翻译说明  xii','translation_note')]:link(para('','TOCEntry'),txt,anc)
heading('第一部',2)
for i,(n,en,zh) in enumerate(CHAPTERS,1):
    if i==28:heading('第二部',2)
    if i in [28,35,42,44,47]:para({28:'第一幕',35:'第二幕',42:'第三幕',44:'第四幕',47:'第五幕'}[i],'Speaker')
    if i==28:zh='幽美的风景 朦胧微光'
    link(para('','TOCEntry'),f'第{i}场  {zh}    {n-14}',f'scene_{i}')
for txt,anc in [('古典典故词汇表  475','glossary'),('参考书目选编  482','bibliography'),('英译者简介','translator_bio'),('封底介绍','back_cover')]:link(para('','TOCEntry'),txt,anc)
doc.add_page_break()

heading('出版资料与献辞',anchor='publication')
for section in front:
    if section['page']>=9:continue
    heading(section['heading'],2);locator(section['page'])
    for t in section['paragraphs']:para(t)
doc.add_page_break()

# Annotate a proper name once, retaining the source name on first occurrence.
seen=set();name_map={}
for en,zh in TERMS.items():
    if zh not in name_map and len(zh)>1 and not any(c in zh for c in '（）'):name_map[zh]=en
name_re=re.compile('|'.join(re.escape(x) for x in sorted(name_map,key=len,reverse=True)))
def first_names(s):
    def rep(m):
        zh=m.group()
        if zh in seen:return zh
        seen.add(zh)
        if s[m.end():].startswith(('（','(')):return zh
        return zh+'（'+name_map[zh]+'）'
    return name_re.sub(rep,s)

for section in front:
    if section['page']<9:continue
    n=section['page']
    if 'heading' in section:heading(section['heading'],1,'introduction' if n==9 else 'translation_note')
    locator(n)
    for t in section['paragraphs']:
        if n==10:t=t.replace('《葛兹》','《葛兹》（Götz）').replace('《埃格蒙特》','《埃格蒙特》（Egmont）')
        para(first_names(t))

doc.add_page_break();heading('第一部',1,'part_one')
last_page=None;included=[]
for u in units:
    n=u['page'];kind=u['kind'];t=u['translation']
    if n!=last_page:
        if n==214:doc.add_page_break();heading('第二部',1,'part_two')
        locator(n);last_page=n
    if kind=='heading':
        i=int(re.search(r'第(\d+)场',t).group(1))
        if i==28:t='第28场  幽美的风景 朦胧微光'
        heading(t,2,f'scene_{i}')
    elif kind=='act':heading(t,2)
    elif kind=='subheading':heading(t,3)
    elif kind=='speaker':para(first_names(t),'Speaker')
    elif kind=='stage':
        t=re.sub(r'\s*\n\s*',' ',t)
        para(first_names(t),'Stage')
    elif kind=='foreign':
        p=para('','Verse')
        for j,line in enumerate(t.splitlines()):
            if j:p.add_run().add_break()
            r=p.add_run(line)
            if j==0:r.italic=True
    else:
        # A verse block can cross a page; keep individual sense lines together naturally.
        para(first_names(t),'Verse')
    included.append(u['id'])

doc.add_page_break()
for section in back:
    n=section['page']
    if 'heading' in section:
        anc={489:'glossary',496:'bibliography',497:'translator_bio',500:'back_cover'}[n]
        heading(section['heading'],1,anc)
    locator(n)
    for t in section['paragraphs']:
        p=para(t)
        if n<=495:
            m=re.match(r'^(.+?）：)',t)
            if m:
                p.clear();p.add_run(m.group(1)).bold=True;p.add_run(t[m.end():])

doc.save(OUT)
assert len(included)==len(units) and len(set(included))==len(units)
alltext='\n'.join(p.text for p in doc.paragraphs)
assert all(q in alltext for q in ['Sorge','Knittelvers','Sancta simplicitas','Eritis sicut Deus','Dies irae','Chorus Mysticus'])
assert len([u for u in units if u['kind']=='heading'])==53
audit={'output':str(OUT),'unit_count':len(units),'included_unit_count':len(included),'scene_count':53,'source_play_pages':len(set(u['page'] for u in units)),'curated_blocks':sum(bool(u.get('curated')) for u in units),'chinese_characters':len(re.findall('[\u4e00-\u9fff]',alltext)),'paragraph_count':len(doc.paragraphs),'untranslated_units':sum(not bool(u['translation'].strip()) for u in units),'translation_status':'machine-assisted full draft with selective editing; not line-by-line final literary revision'}
ROOT.joinpath('audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
