from pathlib import Path
import re, csv, zipfile, pymupdf
root=Path('ODE/复习'); src=root/'源码'
review=(src/'review.tex').read_text(encoding='utf-8')
training=(src/'training.tex').read_text(encoding='utf-8')
assert len(re.findall(r'\\point\{',review))==48
assert len(re.findall(r'\\problem\{',training))==67
rows=list(csv.DictReader((src/'sources.csv').open(encoding='utf-8-sig')))
assert len(rows)==67 and [int(r['本册题号']) for r in rows]==list(range(1,68))
assert all(int(r['PDF页'])==int(r['印刷页'])+8 for r in rows if r['印刷页'])
for p in root.glob('*.pdf'):
 d=pymupdf.open(p); assert '3.1' in d[0].get_text(); print(p.name,len(d))
files=['review.tex','training.tex','preamble.tex','make_training.py','exam_revision.py','standard_questions.py','build.py','sources.csv']
with zipfile.ZipFile(root/'可编辑源码_截止3.1.zip','w',zipfile.ZIP_DEFLATED) as z:
 z.write(root/'README.md','README.md')
 for name in files:z.write(src/name,'源码/'+name)
report='''# 交付核验记录\n\n2026-10-31：考试范围明确截止第 3.1 节（含）。\n\n- 复习重点：48 个知识点（保留原编号）及真题导向补充，26 页。\n- 训练题：67 道，17 页；来源 CSV 恰有 67 条连续记录。\n- 核对选题原书页面；PDF 页偏移为 +8，教材为 +10；真题与改编另标来源位置。\n- 全部 ODE 作业已纳入范围判断，3.2 作业排除，2.2 旧版去重。\n- XeLaTeX 两遍编译完成；无 Overfull、Undefined、Missing character 或错误报告。\n- 全页缩略图及代表完整页已核验，已修正训练题题干跨页分离和目录溢出。\n- 源码包仅收录独立可编辑文本、题库、映射与编译脚本；不依赖原书图片即可编译。\n'''
(src/'build'/'交付核验记录.md').write_text(report,encoding='utf-8')
print('Verified 48 points, 67 exercises; source archive created.')
