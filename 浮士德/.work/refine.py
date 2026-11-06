from pathlib import Path
import json,re,sys,concurrent.futures,collections
sys.path.insert(0,str(Path(__file__).parent))
from translate import fetch,glossary

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parent
units=json.loads((ROOT/'translated.json').read_text(encoding='utf-8'))
curated=json.loads((ROOT/'curated.json').read_text(encoding='utf-8'))
curated+=json.loads((ROOT/'curated_extra.json').read_text(encoding='utf-8'))
applied=[]
for c in curated:
    found=[u for u in units if u['page']==c['page'] and u['source'].startswith(c['prefix'])]
    if len(found)!=1:raise ValueError(('curated match',c['page'],c['prefix'],len(found)))
    found[0]['translation']='\n'.join(c['lines']);found[0]['curated']=True;applied.append(found[0]['id'])

STAGES={'(Entering.)':'（上场。）','(Aside.)':'（旁白。）','(Aloud.)':'（高声。）','(Sings.)':'（唱。）','(Sing.)':'（唱。）','(Exit.)':'（退场。）','(Exeunt.)':'（众人退场。）','(Softly.)':'（轻声。）','(In chorus.)':'（齐声。）','(Shouting.)':'（高声喊。）','(To the audience.)':'（对观众。）','(Outside the door.)':'（在门外。）','(Reads.)':'（读。）','(In an undertone.)':'（低声。）','(With a violent start.)':'（猛然一惊。）','(On the balcony.)':'（在阳台上。）','(Surrounding great PAN.)':'（环绕着大神潘。）'}
for u in units:
    if u['kind']=='stage' and u['source'] in STAGES:u['translation']=STAGES[u['source']];u['curated']=True

# Re-run only remaining long English spans. Foreign quotations are explicitly exempt.
pending=[]
for u in units:
    if u.get('curated') or u['kind'] in ['foreign','speaker']:continue
    if len(re.findall(r'[A-Za-z]{2,}',u['translation']))>=5:pending.append(u)
print('English residue blocks',len(pending),flush=True)
def fix(u):
    t=u['translation']
    # Translate each contiguous Latin-script clause, leaving its Chinese context intact.
    pat=r"[A-Za-z][A-Za-z\s’'\-,:;.!?\"“”()|—–/]*[A-Za-z.!?]"
    for m in reversed(list(re.finditer(pat,t))):
        s=m.group()
        if len(re.findall(r'[A-Za-z]{2,}',s))<3:continue
        v=fetch(s)
        if re.search('[\u4e00-\u9fff]',v):t=t[:m.start()]+v+t[m.end():]
    return u['id'],t
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for k,t in pool.map(fix,pending):units[k]['translation']=t

REPL={
'River Inn':'河畔客店',
'WHO':'谁','卡俄斯':'混沌',
'狐猴':'勒穆尔亡灵','永恒的女性气质':'永恒的女性','克尼特尔弗斯':'克尼特尔诗体',
'MEPHISTOPHELES':'梅菲斯特','HOMUNCULUS':'荷蒙库鲁斯','HOMUNCULWUS':'荷蒙库鲁斯',
'Dioskouroi':'狄俄斯库里双子神','myrmidons':'密密麻麻的小人们','Undines':'水中女仙',
'RIVER GOD':'河神','NYMPHS':'仙女们','PSYLLI':'普叙利人','MARSI':'马耳西人',
'Great Pan':'大神潘','keystone':'拱顶石','FAUS 1':'浮士德','lefi':'左边',
'浮士德医生':'浮士德博士','帕特·塞拉菲库斯':'炽爱的神父','父亲狂喜':'狂喜的神父',
'荷蒙库鲁斯的':'荷蒙库鲁斯的','执行退出':'退场'
}
for u in units:
    t=u['translation']
    if u['kind'] not in ['foreign','speaker']:
        for a,b in REPL.items():t=t.replace(a,b)
        t=t.replace('auto-da-fe','auto-da-fe（宗教裁判所的火刑仪式）')
        if u['page']>218:t=t.replace('巴黎','帕里斯')
        if u['kind']=='heading' and u['page']==214:t='第28场  幽美的风景 朦胧微光'
        t=t.replace('@@','')
        t=t.replace('[','').replace(']','')
        t=t.replace('墨菲斯托','梅菲斯特')
        t=re.sub(r'\s+([，。！？；：、）”])',r'\1',t)
        t=re.sub(r'([（“])\s+',r'\1',t)
        t=t.replace(' ,','，').replace('，,','，')
    u['translation']=t
    if u['kind']=='verse' and not u.get('curated') and '\n' in u['source']:
        # The English scan's arbitrary line wraps are restored as Chinese sense lines.
        # Keep phrases intact and break at the translated clauses' natural pauses.
        s=u['translation'].strip()
        if '\n' not in s:
            clauses=re.findall(r'.+?(?:[，。！？；：](?:[”’）]*)|$)',s)
            lines=[];buf=''
            for clause in clauses:
                if not clause:continue
                if buf and len(buf)+len(clause)>24:lines.append(buf);buf=''
                buf+=clause
                if len(buf)>=9 or re.search(r'[。！？；][”’）]*$',buf):lines.append(buf);buf=''
            if buf:lines.append(buf)
            u['translation']='\n'.join(lines)

ROOT.joinpath('edited.json').write_text(json.dumps(units,ensure_ascii=False,indent=2),encoding='utf-8')
ROOT.joinpath('translation_review.txt').write_text('\n\n'.join(f'PDF {u["page"]} / UNIT {u["id"]} / {u["kind"]}\nSOURCE: {u["source"]}\nCHINESE: {u["translation"]}' for u in units),encoding='utf-8')
print('curated blocks',len(applied),'all units',len(units),'Chinese chars',sum(len(re.findall('[\u4e00-\u9fff]',u['translation'])) for u in units))
for u in units:
    if re.search(r'[A-Za-z]{4}',u['translation']) and u['kind'] not in ['foreign','speaker']:
        print('REMAINING',u['page'],u['id'],repr(u['translation'][:600]))
