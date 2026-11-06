from pathlib import Path
p=Path('ODE/复习/源码/standard_questions.py');s=p.read_text(encoding='utf-8');s=s.replace('    return problems',r'''
    extra=[
        ('零次齐次方程',r"在 $t>0$ 上求方程 $x'=(t^2+tx+x^2)/t^2$ 的通解，并求满足 $x(1)=0$ 的解及其最大存在区间。",'教材 2.1 零次齐次类型（自拟）','教材书 p.23--24 / PDF p.33--34'),
        ('一阶微分方程',r"求方程 $x'=(x+t)/(x-t+1)$ 的通解或通积分，并求满足 $x(0)=0$ 的局部解。",'教材习题 2.1 第 1(5) 题（增加初值问）','教材书 p.25 / PDF p.35'),
        ('一阶微分方程',r"求方程 $x'=(2t+2x+1)/(t+x-1)$ 的全部实解，并给出满足 $x(0)=0$ 的解的最大存在区间。",'教材 2.1 一次式比值退化类型（自拟）','教材书 p.24 / PDF p.34'),
        ('一阶微分方程',r"求方程 $x'=\cos(t+2x)$ 的通积分及所有直线解。",'教材 2.1 线性组合类型（自拟）','教材书 p.25 / PDF p.35'),
        ('一阶微分方程',r"在 $t>0$ 上求方程 $x'=2x/t+x^2/t^3$ 的全部实解，并求满足 $x(1)=1$ 的解及其最大存在区间。",'教材习题 2.1 第 4 题类型（自拟）','教材书 p.25 / PDF p.35')]
    for topic,text,source,loc in extra:
        problems.append(dict(group='F. 2.1 节补充训练（5 题）',source=source,page='',location=loc,topic=topic,text=text,note=''))
    return problems''')
p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/make_training.py');s=p.read_text(encoding='utf-8');s=s.replace('assert len(problems)==50','assert len(problems)==55').replace('期中训练题 50 题','期中训练题 55 题').replace('全册 50 题','全册 55 题').replace('教材应用 6 题。不附答案。','教材应用 6 题，另附 2.1 节补充题 5 题。原第 1--50 题编号不变。不附答案。').replace('Generated 50 exercises.','Generated 55 exercises.');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/build.py');s=p.read_text(encoding='utf-8').replace('期中训练题50题_截止3.1.pdf','期中训练题55题_截止3.1.pdf');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/review.tex');s=p.read_text(encoding='utf-8').replace('训练题 50 题','训练题 55 题');p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/README.md');s=p.read_text(encoding='utf-8').replace('期中训练题50题_截止3.1.pdf','期中训练题55题_截止3.1.pdf').replace('真题导向修订版，50 题','真题导向修订版，55 题').replace('SIR、等角轨线、二体问题三个应用专题各有两题。','SIR、等角轨线、二体问题三个应用专题各有两题。新增第 51--55 题为 2.1 补充题，原编号保留。').replace('当前标准题面主源。','当前标准题面主源。').replace('50 题及原有类别配比','原第 1--50 题及类别配比');s+='\n本轮补强复习第 12--14 条：零次齐次、一次式比值（交点平移与退化组合）、单一线性组合、加权齐次；各有换元式、分离结果及例子。训练追加第 51--55 题，不改原题编号。追加题源在 `standard_questions.py` 的 `extra` 中；原前 50 题仍用 `TEXT`。\n';p.write_text(s,encoding='utf-8')
p=Path('ODE/复习/源码/资料核对/final_check.py');s=p.read_text(encoding='utf-8').replace('training))==50','training))==55').replace('len(rows)==50','len(rows)==55').replace('range(1,51)','range(1,56)').replace('50 exercises','55 exercises').replace('训练题：50 道，14 页；来源 CSV 恰有 50 条连续记录。','训练题：55 道；来源 CSV 恰有 55 条连续记录。');p.write_text(s,encoding='utf-8')
