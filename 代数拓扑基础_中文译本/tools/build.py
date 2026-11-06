"""Compile saved LaTeX, read errors, and record progress; no visual PDF review."""
from pathlib import Path
import subprocess
import json
import datetime
import sys

root = Path(__file__).resolve().parents[1]
result = subprocess.run(
    [str(root / 'tools' / 'tectonic.exe'), '--keep-logs', '--keep-intermediates',
     '--outdir', str(root), 'main.tex'],
    cwd=root / 'LaTeX', capture_output=True, encoding='utf-8', errors='replace')
log = result.stdout + result.stderr
(root / 'build-console.log').write_text(log, encoding='utf-8')
record = {'section': sys.argv[1] if len(sys.argv) > 1 else '',
          'time': datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
          'success': result.returncode == 0}
with (root / 'compile-history.jsonl').open('a', encoding='utf-8') as out:
    out.write(json.dumps(record, ensure_ascii=False) + '\n')
print(json.dumps(record, ensure_ascii=False))
if result.returncode == 0 and record['section']:
    section = record['section']
    (root / '翻译进度.md').write_text(
        '# 翻译进度\n\n'
        '原书：Elements of Algebraic Topology, Second Edition，2025，584 个 PDF 页面。\n\n'
        '约定：只排中文；术语首次出现附英文；保留原图及图内标签；保留章节和定理编号；'
        '按原书页码标注；每完成一小节编译，不逐页检查输出 PDF。\n\n'
        f'已翻译并编译：前言、致谢，正文从第 1.1 节至第 {section} 节。\n\n'
        '最新 PDF：main.pdf。LaTeX 主文件：LaTeX/main.tex。\n\n'
        '源书及逐页文字：source/。插图：LaTeX/figures/。编译记录：compile-history.jsonl。\n\n'
        f'最近编译时间：{record["time"]}。\n\n'
        '全书尚未完成；未翻译的部分没有混入英文原页作为译文。\n', encoding='utf-8')
if result.returncode:
    print(log[-6000:])
sys.exit(result.returncode)
