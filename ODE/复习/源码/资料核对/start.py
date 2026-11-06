exec(open('ODE/复习/源码/资料核对/more.py',encoding='utf-8-sig').read().split('for name,d,nums')[0])
for n in list(range(12,29)):
 if not (out/f'教材-{n:03}.png').exists(): t[n-1].get_pixmap(matrix=f.Matrix(1.4,1.4)).save(str(out/f'教材-{n:03}.png'))
