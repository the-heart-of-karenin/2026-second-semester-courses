from pathlib import Path
p=Path('ODE/复习/源码/make_training.py');s=p.read_text(encoding='utf-8')
s=s.replace('assert len(problems)==50, len(problems)','from exam_revision import revise\nproblems = revise(problems)\nassert len(problems)==50, len(problems)')
a=s.index(r'\textbf{使用范围。}');b=s.index(r'\begingroup\small',a)
s=s[:a]+r'''\textbf{修订说明。}本版按新提供的两份期中试卷重配，保持 50 题，考试范围仍截止 3.1（含）。构成为：概念辨析 6 题、代表计算 14 题、基本定理证明 18 题、首次积分综合 6 题、教材应用 6 题。计算组保留必要方法代表题，其余重点训练条件、证明、独立性、解集结构和模型解释。
+
+\textbf{材料标识。}“2025 卷”指用户提供、卷首标有上海交通大学致远班 2025--2026 学年第一学期期中试卷的六张照片；“2023 卷”指用户提供的 2023--2024 学年第一学期试题及部分答案整理 PDF（署编者史瑞普）。本册依据所供文件，不另行认证其官方发布状态。教材指《微分方程 I（101 计划）》；习题集指博亚尔丘克、戈洛瓦奇《高等数学例题与习题集（四）常微分方程》。题目均注明来源、改编或新增小问，不再宣称全部是习题集原题。
+
+\textbf{范围处理。}2023 卷中一般非线性初值问题的存在唯一性与延拓理论可能涉及第四章，本版不借真题扩大考试范围。非唯一性用 2.1--2.2 的显式构造，线性全局存在唯一性及 Picard 误差用 3.1 的证明。本册含完整的 SIR、等角轨线、二体问题三个教材应用专题，二体题不只要求背圆锥曲线公式。
+
+\textbf{作答要求。}证明题必须写出条件、论证与结论，不能把待证定理作为已知使用；计算题写定义域、解区间、漏解检查；首次积分题既检验沿解导数，也检查独立性；模型题先写假设再建方程。一般不附解答，以保留考试训练用途。复习重点末尾另列本轮应练的证明及 Picard 误差标准结果。
+
+\textbf{页码。}习题集选题处 PDF 页＝印刷页＋8；教材 PDF 页＝印刷页＋10。试卷按原大题/小题号定位。新增题目的条件以本册题干为准，原卷或教材表述不直接被改写为“原题”。
+
+'''.replace('\n+','\n')+s[b:]
s=s.replace("p['source']+f'；书 p.{page} / PDF p.{page+8}'", "p['source']+'；'+p.get('location',f'书 p.{page} / PDF p.{page+8}' if isinstance(page,int) else '')")
s=s.replace("{p['page']+8}","{p['page']+8 if isinstance(p['page'],int) else '--'}")
s=s.replace("{p['page']} &", "{p['page'] if isinstance(p['page'],int) else '--'} &")
s=s.replace("p['page']+8,p['topic'],p['note']", "p['page']+8 if isinstance(p['page'],int) else '',p['topic'],p['note'],p.get('location','')")
s=s.replace("'补充说明'])", "'补充说明','来源位置'])")
s=s.replace(r'\large 考试截止到第 3.1 节（含）',r'\large 真题导向修订版 · 截止第 3.1 节（含）')
p.write_text(s,encoding='utf-8')
