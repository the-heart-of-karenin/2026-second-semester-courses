"""从随附的逐页原文提取文件重建文献排版；保留可检索的原始书目。"""
from pathlib import Path
import re
import unicodedata

BASE = Path(__file__).resolve().parent

def escape(text):
    # PDF字体将重音符号单独编码；先重新组合成 Unicode 字母。
    text = re.sub(r'\s*([¨´])\s*([A-Za-z])',
                  lambda m: unicodedata.normalize('NFC',m[2]+{'¨':'\u0308','´':'\u0301'}[m[1]]),text)
    text = unicodedata.normalize('NFKC', text)
    text = text.replace('Gr ¨otschel', 'Grötschel').replace('Lov ´asz', 'Lovász')
    text = text.replace('Birkh ¨auser', 'Birkhäuser').replace('Tardos, ´E.', 'Tardos, É.')
    text = text.replace('V ol.', 'Vol.').replace('V olume', 'Volume')
    text = text.replace('Schr ¨oder', 'Schröder')
    for a,b in [('&',r'\&'),('%',r'\%'),('_',r'\_'),('#',r'\#')]:
        text = text.replace(a,b)
    return text

def write(part, pages, first_marker):
    content = []
    for j,p in enumerate(pages):
        text = (BASE/'source'/f'p{p}.txt').read_text(encoding='utf-8')
        if j == 0 and first_marker:
            text = text.split(first_marker,1)[1]
        else:
            text = '\n'.join(text.splitlines()[1:])
        content.append(text)
    text = '\n'.join(content)
    text = re.sub(r'(?<=\w)-\s*\n(?=\w)', '', text)
    # 作者条目的起始行，或书目类别标题。
    starts = re.compile(r'^\S.*\[\d{4}[^\]]*\]\s*:|^(?:General Literature:|Cited References:)$')
    paras=[]
    for line in text.splitlines():
        line=line.strip()
        if not line: continue
        if starts.match(line) or not paras: paras.append(line)
        else: paras[-1] += ' '+line
    lines=[r'{\small\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}\sloppy']
    for p in paras:
        if p == 'General Literature:': lines.append(r'\textbf{一般文献}\par')
        elif p == 'Cited References:': lines.append(r'\textbf{引用文献}\par')
        else: lines.append(escape(p)+r'\par')
    lines.append('}')
    (BASE/f'references{part}.tex').write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__ == '__main__':
    write('13a',[320],'References\n')
    write('13b',[321],None)
    write('14a',[341],'References\n')
    write('14b',[342],None)
