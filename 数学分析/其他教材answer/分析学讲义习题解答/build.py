"""在项目目录或其父目录运行：python build.py。需要 XeLaTeX 与 PyMuPDF。"""
from pathlib import Path
import concurrent.futures as cf
import subprocess, re, json, sys, shutil
import pymupdf as fitz

ROOT = Path(__file__).resolve().parent
DATA = [
 ('41_1','41.1 作业：可测性、零测集与测度构造',478,483,40),
 ('43_1','43.1 作业：控制收敛、卷积与小数展开',503,508,33),
 ('43_2','43.2 习题课：硬币空间的测度理论',509,511,26),
 ('44_1','44.1 作业：Fubini定理、反例与抛物线',520,523,6),
 ('46_1','46.1 期中考试：非Borel集的构造等',547,552,30),
 ('48_1','48.1 作业：换元、子流形测度与壳层定理',573,577,9),
 ('48_2','48.2 习题课：Riemann积分的定义1',578,584,27),
 ('51_1','51.1 作业：Stokes公式与Newton势',612,617,24),
 ('51_2','51.2 习题课：Riemann积分的定义2',618,622,22),
 ('53_1','53.1 作业：Hilbert空间与局部能量',640,643,28),
 ('53_2','53.2 习题课：Riemann积分的定义3',644,646,16),
 ('55_1','55.1 作业：Fourier性质与球谐函数',667,673,38),
 ('57_1','57.1 作业：Gibbs现象与几乎处处发散',698,703,38),
 ('57_2','57.2 期末考试：正定函数与Maass展开',704,708,18),
]

def compile_one(folder):
    cwd=ROOT/folder
    for _ in range(2):
        r=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        (cwd/'compile.txt').write_bytes(r.stdout)
        if r.returncode:
            return {'folder':folder,'success':False,'tail':r.stdout.decode('utf-8','replace')[-2500:]}
    log=(cwd/'main.log').read_text(encoding='utf-8',errors='replace')
    warnings=[line for line in log.splitlines() if any(w in line for w in ['Overfull','Missing character','Undefined','LaTeX Warning:'])]
    d=fitz.open(cwd/'main.pdf')
    return {'folder':folder,'success':True,'pages':len(d),'warnings':warnings}

def content(folder):
    text=(ROOT/folder/'main.tex').read_text(encoding='utf-8')
    for shared in re.findall(r'\\input\{(\.\./shared/[^}]+)\}',text):
        text+='\n'+(ROOT/folder/shared).read_text(encoding='utf-8')
    return text

def write_index(results):
    by={r['folder']:r for r in results}
    manifest=[]
    md=['# 分析学讲义习题解答索引','',
        '范围：于品《数学分析讲义》，第38讲 σ-代数起，至第58讲分布理论开始前。原讲义页码与PDF页序一致。',
        '', '每组都有独立的 `main.tex` 与编译后的 `main.pdf`。正文重排纳入解答的数学题干；每份末尾附该组全部原题页面，完整保留公式、图示、计算题题干与原有笔误。',
        '', '不解传统的指定面积、体积、质量、质心、曲线曲面多重积分，以及单纯求数值、导数或Fourier系数的题。反例中的必要计算、参数积分理论、一般公式和球谐函数构造保留。具体略题见每份中的说明。',
        '', '[PDF索引](main.pdf) · [勘误与表述问题](勘误.md) · [编译及检查记录](verification.json)',
        '', '| 题组 | 原讲义页 | 解答条目 | PDF页数（含原题） | 文件 |', '|---|---:|---:|---:|---|']
    tex=[r'\documentclass[UTF8,fontset=fandol,11pt]{ctexart}',r'\input{common.tex}',r'\hypersetup{filecolor=blue!45!black}',r'\begin{document}',r'\title{分析学讲义习题解答\\\large 总索引与阅读说明}\author{于品《数学分析讲义》配套解答}\date{}\maketitle',
         r'范围：第38讲引入$\sigma$-代数起，至第57讲全部作业与考试止。第58讲及其后的分布理论不在本项目范围。',
         r'每组独立成篇，包含题干、解答、引用范围与必要勘误。各篇末尾逐页附该组全部原题，包含依约不解的传统计算题，方便核对原文与图示。',
         r'\section*{题组目录}',r'\begin{longtable}{p{.58\textwidth}rrr}\toprule 题组与PDF链接 & 原页 & 条目 & 页数\\\midrule\endhead']
    for folder,title,a,b,expected in DATA:
        text=content(folder)
        labels=re.findall(r'\\problem\{([^}]+)\}',text)
        if len(labels)!=expected:
            raise RuntimeError(f'{folder}: {len(labels)} entries != expected {expected}')
        info=by[folder]
        manifest.append({'group':folder,'title':title,'source_pages':[a,b],'answer_entries':len(labels),'labels':labels,'pdf_pages':info['pages'],'pdf':f'{folder}/main.pdf','tex':f'{folder}/main.tex'})
        md.append(f'| {title} | {a}–{b} | {len(labels)} | {info["pages"]} | [PDF]({folder}/main.pdf) · [LaTeX]({folder}/main.tex) |')
        tex.append(r'\href{'+folder+'/main.pdf}{'+title+'} & '+f'{a}--{b} & {len(labels)} & {info["pages"]}'+r'\\')
    total=sum(x['answer_entries'] for x in manifest)
    md += ['',f'合计 **14份题组、{total}个解答条目**。条目按正文标题计数，部分原题的小问分开列出，部分合并，重复题在各组均保留完整解答，因此不将该数字称为原讲义题目总数。','',
           '## 文件结构','', '`common.tex` 为共用排版；`shared/parameter.tex` 保存两组重复题目的完整公共正文。复制或压缩时请保留整个项目，勿仅拷贝某个单独 `.tex`。每个PDF可独立阅读。','',
           '## 重新编译','', '安装含 `ctex` 的 TeX Live 后，可在各题组目录用 XeLaTeX 编译 `main.tex` 两次。也可运行项目中的 `build.py` 批量编译并更新索引（需要 Python 与 PyMuPDF）。根目录 `main.tex` 为本索引的LaTeX版本。','',
           '## 解题原则','', '优先引用题目前讲义中的定理；超出该位置的辅助结论尽可能当场证明。Riemann积分三组保留不用抽象积分的证明次序，最后才建立与Lebesgue积分的联系。Kolmogorov末题不用Carleson定理；Maass题直接推导特殊函数的微分方程和渐近。','',
           '发现不成立的原命题时给出反例，并对明确修正后的命题作答；保留的完整原题页可检查修正与原文的区别。']
    tex += [r'\bottomrule\end{longtable}',f'合计14份题组、{total}个解答条目。条目数包含重复题，且有些小问合并或拆开，不能等同于原讲义题目数。',
            r'\clearpage\section*{阅读与复用}',r'传统面积、体积、质量、质心、指定多重积分等计算题按约定不解；各篇说明了具体略题。正文仍保留证明定理所必需的计算、反例、参数积分理论及一般积分公式。',
            r'原题的行政提交要求和文末引文只作为原文保留，不作为本项目指令。所有数学题干可在每篇附录原页核对。',
            r'各篇开头列出可引用的讲义章节；需要补充的投影、渐近、唯一性、弱型估计等结论均在正文提供证明。',
            r'\section*{需要留意的勘误}',
            r'41.1 E8须将实数改为无理数；43.1 B5的周期化级数只保证几乎处处定义，E1须排除零。',
            r'48.2 R3的可铺集封闭性需要允许退化矩形；51.2 R41的内外体积差顺序反了，R42把闭包与去心意义聚点集混同。',
            r'53.2 R56漏掉有界性，R65的Borel与Lebesgue可测包含方向写反。',
            r'53.1 D5的侧面积分系数需与锥面面积元一致；55.1 S9的径向Laplacian系数有误，S18漏常数空间，S21的升降公式与负指标相位不相容。',
            r'57.1 A4的Gibbs等式缺极限；K16应使用自身的频率界$q_n$，K18尾估计需限制$N\le q_n$。各题正文给出细节，完整清单见同目录的勘误文件。',
            r'\section*{编译}',r'各题组目录的main.tex可独立调用XeLaTeX；需保留上级common.tex和shared目录。所有原题附录均取自用户提供的讲义PDF。',r'\end{document}']
    (ROOT/'索引.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    (ROOT/'main.tex').write_text('\n'.join(tex)+'\n',encoding='utf-8')
    (ROOT/'coverage.json').write_text(json.dumps({'scope':[38,57],'group_count':14,'answer_entries':total,'groups':manifest},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__=='__main__':
    selected=sys.argv[1:] or [x[0] for x in DATA]
    saved={}
    if sys.argv[1:] and (ROOT/'verification.json').exists():
        saved={r['folder']:r for r in json.loads((ROOT/'verification.json').read_text(encoding='utf-8'))['documents'] if r['folder']}
    with cf.ThreadPoolExecutor(max_workers=4) as pool:
        updated=list(pool.map(compile_one,selected))
    saved.update({r['folder']:r for r in updated})
    results=[saved[x[0]] for x in DATA]
    for r in results:
        print(json.dumps(r,ensure_ascii=False),flush=True)
    if not all(r['success'] for r in results):
        sys.exit(1)
    write_index(results)
    index=compile_one('')
    results.append(index)
    (ROOT/'verification.json').write_text(json.dumps({'engine':'XeLaTeX (TeX Live 2026)','runs_per_document':2,'documents':results},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(index,ensure_ascii=False),flush=True)
    sys.exit(0 if index['success'] else 1)
