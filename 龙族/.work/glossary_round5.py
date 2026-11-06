from pathlib import Path
import re,json
root=Path(__file__).resolve().parent.parent
work=root/'.work';file=root/'术语对照.md';marker='<!-- round5_terms -->'
text=file.read_text(encoding='utf-8').split(marker)[0].rstrip()
text=text.replace('当前覆盖《火之晨曦》序章及第一至第九幕，随正文翻译增补；尚未翻译的四册中的术语不标为已确认。','当前覆盖《火之晨曦》全文及《悼亡者之瞳》序幕至第三幕，随正文翻译增补；其余内容中的术语不标为已确认。')
def rows(s):
    for line in s.splitlines():
        if not line.strip().startswith('|'):continue
        v=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(v)<3 or v[0] in ('中文','原文','原文行') or all(re.fullmatch(r'[:\- ]+',x or '-') for x in v):continue
        yield v[:3]
seen={re.sub(r'\s','',z):e for z,e,_ in rows(text)}
blocks=[];conflicts=[]
files=[('act10_terms.md','第一册第十幕'),('epilogue_terms.md','第一册尾声'),('book2_opening_terms.md','第二册序幕'),('book2_act1_terms.md','第二册第一幕'),('book2_act2_terms.md','第二册第二幕'),('book2_act3_terms.md','第二册第三幕')]
for name,title in files:
    data=(work/name).read_text(encoding='utf-8');out=[]
    for z,e,note in rows(data):
        k=re.sub(r'\s','',z)
        if k in seen:
            if seen[k].casefold()!=e.casefold():conflicts.append({'zh':z,'previous':seen[k],'new':e,'file':name})
            continue
        seen[k]=e;note=note.replace('主代理','项目').replace('父代理','项目')
        out.append(f'| {z} | {e} | {note} |')
    if out:blocks.append('## '+title+'新增术语\n\n| 中文 | 本项目英文 | 说明 |\n| --- | --- | --- |\n'+'\n'.join(out))
file.write_text(text+'\n\n'+marker+'\n\n'+'\n\n'.join(blocks)+'\n',encoding='utf-8')
(work/'glossary_round5_conflicts.json').write_text(json.dumps(conflicts,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'total':len(seen),'conflicts':conflicts},ensure_ascii=False))
