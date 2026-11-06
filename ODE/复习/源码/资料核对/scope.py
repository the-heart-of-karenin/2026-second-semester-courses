exec(open('ODE/复习/源码/资料核对/more.py',encoding='utf-8-sig').read().split('for name,d,nums')[0])
for n in range(232,239): b[n-1].get_pixmap(matrix=f.Matrix(1.7,1.7)).save(str(out/f'习题集-{n:03}.png'))
for n in [56,57,58,59,60,61,62,63,65,66,67,68,69,70,71,72,74,75,76,77,78,79,80,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104]:
 if not (out/f'教材-{n:03}.png').exists(): t[n-1].get_pixmap(matrix=f.Matrix(1.4,1.4)).save(str(out/f'教材-{n:03}.png'))
