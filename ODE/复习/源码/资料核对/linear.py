exec(open('ODE/复习/源码/资料核对/more.py',encoding='utf-8-sig').read().split('for name,d,nums')[0])
for n in range(243,248): b[n-1].get_pixmap(matrix=f.Matrix(1.7,1.7)).save(str(out/f'习题集-{n:03}.png'))
