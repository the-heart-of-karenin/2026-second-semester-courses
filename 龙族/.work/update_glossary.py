from pathlib import Path
import re,json

root=Path(__file__).resolve().parents[1]
work=root/'.work'
glossary=root/'术语对照.md'
marker='<!-- round2_terms -->'
text=glossary.read_text(encoding='utf-8').split(marker)[0].rstrip()
text=text.replace('当前覆盖《火之晨曦》序章及第一幕，随正文翻译增补','当前覆盖《火之晨曦》序章及第一至第九幕，随正文翻译增补')
text=text.replace('当前覆盖《火之晨曦》序章及第一至第四幕，随正文翻译增补','当前覆盖《火之晨曦》序章及第一至第九幕，随正文翻译增补')
text=text.replace('当前覆盖《火之晨曦》序章及第一至第七幕，随正文翻译增补','当前覆盖《火之晨曦》序章及第一至第九幕，随正文翻译增补')
text=text.replace('当前覆盖已译部分','当前覆盖已译部分')
def rows(content):
    result=[]
    for line in content.splitlines():
        if not line.strip().startswith('|'):continue
        cells=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(cells)<2 or cells[0] in ('中文','原文','原文行'):continue
        if all(re.fullmatch(r'[:\- ]+',c or '-') for c in cells):continue
        if len(cells)>=3: result.append((cells[0],cells[1],cells[2]))
    return result
seen={re.sub(r'\s','',r[0]):r[1] for r in rows(text)}
blocks=[];conflicts=[]
for filename,section in [('act2_review.md','第二幕新增术语'),('act3_terms.md','第三幕新增术语'),('act4_terms.md','第四幕新增术语'),('act5_terms.md','第五幕新增术语'),('act6_terms.md','第六幕新增术语'),('act7_terms.md','第七幕新增术语'),('act8_terms.md','第八幕新增术语（前半）'),('act8b_terms.md','第八幕新增术语（后半）'),('act9_terms.md','第九幕新增术语（前半）'),('act9b_terms.md','第九幕新增术语（后半）')]:
    content=(work/filename).read_text(encoding='utf-8')
    if filename=='act2_review.md':content=content.split('## 新增术语建议',1)[1].split('## 保留原作信息',1)[0]
    table=[]
    for zh,en,note in rows(content):
        key=re.sub(r'\s','',zh)
        if key in seen:
            if en.casefold()!=seen[key].casefold():conflicts.append({'term':zh,'existing':seen[key],'new':en,'source':filename})
            continue
        seen[key]=en
        note=note.replace('父代理已确认此译法。','本项目统一采用此译法。').replace('与父代理已有课程名体系保持一致。','与已有课程名体系保持一致。').replace('与父代理已采用译法一致。','与已有译法一致。').replace('按父代理要求','按项目约定')
        note=note.replace('主代理', '项目').replace('本轮跨幕统一要求', '项目统一译法')
        table.append(f'| {zh} | {en} | {note} |')
    blocks.append(f'## {section}\n\n| 中文 | 本项目英文 | 说明 |\n| --- | --- | --- |\n'+'\n'.join(table))
supplement='''## 译法说明

- 第二幕人物先被描述为死亡，后揭示弗里嘉子弹的效果，英文保留原叙事顺序。
- 第1317—1318行只有“逆……”及被枪声打断的第二字，保留为被打断的 Dis…，不擅自补写完整的“逆臣”或“逆命”。这属于解释性译法，保留全书复核项。
- 第三幕“哲人／海蜇”的中文谐音，保留哲人和水母意象，英语表达为 philosopher / stinging jellyfish；不声称能原样重现同音。
- 各幕开篇的预示性摘录及后文重复段落均保留，不当作重复错误删除。
- 人物称呼随原文揭示推进；例如未在该处给出完整名字的角色，不提前补写后文身份。
- 原作中的现实信息、武器参数、神话与影视描述按照小说翻译，不以考据结果改写剧情。已有英文品牌的明显拼写错误按实际名称整理，故意错误的台词英语继续保留。
- 第五幕标题的原附英文 Gragon Shadow 是明显拼写错误，整理为 Dragon Shadow。第六幕附标题 Star & Flower 在正文标题中写作 Star and Flower，意义保持不变。
- 第2304行原文把婴儿称作“门”，与上下文“钥匙”不一致；该处保留 the Gate，不悄悄替换原文称呼，其余相同角色仍按原文 the Key 处理。
'''
glossary.write_text(text+'\n\n'+marker+'\n\n'+'\n\n'.join(blocks)+'\n\n'+supplement,encoding='utf-8')
(work/'glossary_merge_review.json').write_text(json.dumps(conflicts,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'total_term_rows':len(seen),'duplicate_variants_for_review':conflicts},ensure_ascii=False))
