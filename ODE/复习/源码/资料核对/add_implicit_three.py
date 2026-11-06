from pathlib import Path
p=Path('ODE/复习/源码/standard_questions.py');s=p.read_text(encoding='utf-8');s=s.replace('    return problems',r'''
    implicit=[
        (2,r"求一阶隐式微分方程 $(x'(t))^3-(x'(t))^2-x=0$ 的解。"),
        (4,r"在实数范围内求一阶隐式微分方程 $x-tx'(t)-4\sqrt{x'(t)}=0$ 的解。"),
        (6,r"求一阶隐式微分方程 $(x'(t))^3-(x'(t))^2-2t=0$ 的解。")]
    for num,text in implicit:
        problems.append(dict(group='H. 隐式方程补充（3 题）',source=f'教材习题 2.4 第 1({num}) 题',page='',location='教材书 p.46 / PDF p.56',topic='一阶隐式微分方程',text=text,note=''))
    return problems''');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/make_training.py');s=p.read_text(encoding='utf-8').replace('len(problems)==57','len(problems)==60').replace('训练题 57 题','训练题 60 题').replace('全册 57 题','全册 60 题').replace('积分因子补充题 2 题。','积分因子补充题 2 题、隐式方程补充题 3 题。').replace('Generated 57','Generated 60');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/build.py');s=p.read_text(encoding='utf-8').replace('期中训练题57题','期中训练题60题');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/资料核对/final_check.py');s=p.read_text(encoding='utf-8').replace('training))==57','training))==60').replace('len(rows)==57','len(rows)==60').replace('range(1,58)','range(1,61)').replace('57 exercises','60 exercises').replace('57 道','60 道').replace('57 条','60 条');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/README.md');s=p.read_text(encoding='utf-8').replace('期中训练题57题','期中训练题60题').replace('修订版，57 题','修订版，60 题');s+='\n新增第 58--60 题：教材习题 2.4 第 1(2)(4)(6) 题，分别涉及缺自变量的参数法与零解、含根号的 Clairaut 方程及参数范围、缺未知量的参数积分。原编号保持。题面数据在 `standard_questions.py` 的 `implicit` 中。\n';p.write_text(s,encoding='utf-8')
