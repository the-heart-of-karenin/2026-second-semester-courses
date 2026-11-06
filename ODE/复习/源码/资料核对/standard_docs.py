from pathlib import Path
p=Path('ODE/复习/源码/standard_questions.py');s=p.read_text(encoding='utf-8');s=s.replace("    problems[9-1]['topic']='一阶方程'", "    for n in range(7,16): problems[n-1]['topic']='一阶微分方程'\n    problems[16-1]['topic']='非唯一性与奇解'\n    problems[17-1]['topic']='一阶隐式微分方程'")
p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/README.md');s=p.read_text(encoding='utf-8')
s=s.replace('`源码/exam_revision.py`：本次真题导向版本的主要题库源，定义新题与从旧题库选入的题目。长期修改在此文件进行。','`源码/standard_questions.py`：当前标准题面主源。`TEXT` 的 1--50 号分别对应本册题号，后续修改题干在此进行。题面列明条件与待证式，分项编号，不含解法提示。\n- `源码/exam_revision.py`：定义当前选题、分组、考点及来源。修改出处或更换题目时同步维护此文件与标准题面主源。')
s=s.replace('长期修改应回到 `exam_revision.py`，其中 `keep` 引用的旧书题可在 `make_training.py` 修改','题干修改应回到 `standard_questions.py`，分组与来源修改在 `exam_revision.py` 进行')
s=s.replace('当前训练 11 页','当前标准题面版训练 14 页')
s+='\n2026-10-28 题面修订：逐题改为标准考试表述，明确对象、区间、正则性、初值与参数；证明题按需列出待证公式；删除提示、解题顺序建议及暗示性说明。保持 50 题及原有类别配比。仅修改训练题，复习重点本轮未变。\n'
p.write_text(s,encoding='utf-8')
p=Path('README.md');s=p.read_text(encoding='utf-8');s+='\n训练题题面采用标准试题语言：给齐条件、符号、求解或证明目标，必要时明确列出待证等式/不等式，多项任务分编号；不在题干混入解法提示、提醒或暗示结论。出处与改编标记放题面外。\n';p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/资料核对/final_check.py');s=p.read_text(encoding='utf-8');s=s.replace("'exam_revision.py','build.py'", "'exam_revision.py','standard_questions.py','build.py'").replace('训练题：50 道，11 页','训练题：50 道，14 页');p.write_text(s,encoding='utf-8')
