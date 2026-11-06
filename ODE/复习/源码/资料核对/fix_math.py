from pathlib import Path
p=Path('ODE/复习/源码/make_training.py');s=p.read_text(encoding='utf-8')
s=s.replace('parts=[head]',r'''def math_text(s):
    s=s.replace(r'^{\prime\prime}','SECONDPRIME').replace(r'^{\prime}','FIRSTPRIME')
    return s.replace(r'\prime',r'^{\prime}').replace('SECONDPRIME',r'^{\prime\prime}').replace('FIRSTPRIME',r'^{\prime}')
parts=[head]''')
s=s.replace("p['text'].replace(r'\\prime',r'^{\\prime}')","math_text(p['text'])").replace("p['note'].replace(r'\\prime',r'^{\\prime}')","math_text(p['note'])")
p.write_text(s,encoding='utf-8')
