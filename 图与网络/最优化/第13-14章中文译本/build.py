"""生成书目、编译中文译本，并检查章节和原文页码覆盖。运行：python build.py"""
from pathlib import Path
import json
import re
import shutil
import subprocess
import sys

BASE = Path(__file__).resolve().parent
OUTPUT = BASE/'output'/'组合优化_第13-14章_完整中文译本.pdf'

def run(args):
    result = subprocess.run(args, cwd=BASE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    text = result.stdout.decode('utf-8', errors='replace')
    (BASE/'build'/'last-build.txt').write_text(text,encoding='utf-8')
    if result.returncode:
        print(text[-10000:])
        raise SystemExit(result.returncode)

def main():
    (BASE/'build').mkdir(exist_ok=True)
    (BASE/'output').mkdir(exist_ok=True)
    run([sys.executable,str(BASE/'prepare_references.py')])
    tex = '\n'.join((BASE/p).read_text(encoding='utf-8') for p in ['chapter13.tex','chapter14.tex'])
    expected = list(range(291,322))+list(range(323,343))
    actual = [int(n) for n in re.findall(r'\\srcpage\{(\d+)\}',tex)]
    assert actual == expected, '译稿原书页码覆盖不完整或顺序不正确'
    for chapter,last in [(13,35),(14,25)]:
        for n in range(1,last+1):
            assert re.search(r'(?:定义|定理|命题|引理|推论)'+str(chapter)+r'\.'+str(n)+r'(?!\d)',tex),f'缺少编号 {chapter}.{n}'
    run(['latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error','-outdir=build','main.tex'])
    log=(BASE/'build'/'main.log').read_text(encoding='utf-8',errors='replace')
    warnings = [l for l in log.splitlines() if 'Overfull' in l or 'Missing character:' in l or 'undefined references' in l]
    shutil.copy2(BASE/'build'/'main.pdf',OUTPUT)
    from pypdf import PdfReader
    reader=PdfReader(OUTPUT)
    texts=[p.extract_text() for p in reader.pages]
    assert all(t.strip() for t in texts), '发现空白输出页'
    compact=re.sub(r'\s+','','\n'.join(texts))
    pdf_markers=[int(n) for n in re.findall(r'原书第(\d+)页',compact)]
    assert pdf_markers == expected, 'PDF中的原书页码覆盖不完整'
    for chapter,last in [(13,35),(14,25)]:
        for n in range(1,last+1):
            assert re.search(r'(?:定义|定理|命题|引理|推论)'+str(chapter)+r'\.'+str(n)+r'(?!\d)',compact),f'PDF缺少编号 {chapter}.{n}'
    fulltext='\n'.join(texts)
    for chapter,last in [(13,25),(14,14)]:
        # 第一次匹配跳过目录，从带原书页码的正文中读取实际习题编号。
        start=re.search(r'第\s*'+str(chapter)+r'\s*章习题\s*\n1\.',fulltext)
        assert start, f'PDF没有第{chapter}章习题正文'
        remainder=fulltext[start.end()-2:]
        end=re.search(r'第\s*'+str(chapter)+r'\s*章参考文献',remainder)
        exercise_text=remainder[:end.start()]
        labels=[int(n) for n in re.findall(r'(?m)^(\d+)\.(?!\d)',exercise_text)]
        assert labels == list(range(1,last+1)),f'第{chapter}章习题编号不完整：{labels}'
    assert '\ufffd' not in fulltext, 'PDF提取文本中出现替代字符'
    report={'pdf':OUTPUT.name,'pdf_pages':len(reader.pages),'original_nonblank_pages':len(expected),
            'chapter13_numbered_statements':35,'chapter14_numbered_statements':25,
            'chapter13_exercises':25,'chapter14_exercises':14,'pdf_content_coverage_checked':True,
            'typesetting_warnings':warnings}
    (BASE/'build'/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
