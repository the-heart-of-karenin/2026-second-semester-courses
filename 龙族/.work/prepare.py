from pathlib import Path
import json, hashlib

root = Path(__file__).resolve().parents[1]
src = Path(r'D:\Users\Downloads\楚路\【龙族原著】\龙族旧版\龙族1～3.txt')
raw = src.read_bytes()
lines = raw.decode('utf-8-sig').splitlines()
work = root / '.work'
(work / 'source').mkdir(parents=True, exist_ok=True)
(work / 'translations').mkdir(exist_ok=True)
specs = [
 ('01', '火之晨曦', 'The Blazing Dawn', 176, 5456),
 ('02', '悼亡者之瞳', 'The Mourner’s Eyes', 5599, 12406),
 ('03a', '黑月之潮 上', 'Black Moon Tide Part One', 12502, 16872),
 ('03b', '黑月之潮 中', 'Black Moon Tide Part Two', 16948, 21182),
 ('03c', '黑月之潮 下', 'Black Moon Tide Part Three', 21363, 28345),
]
books=[]
for ident, zh, en, start, end in specs:
    records=[{'line':i+1,'zh':lines[i].strip()} for i in range(start-1,end) if lines[i].strip()]
    dest=work/'source'/f'{ident}.json'
    dest.write_text(json.dumps(records, ensure_ascii=False, indent=2),encoding='utf-8')
    books.append(dict(id=ident,title_zh=zh,title_en=en,start_line=start,end_line=end,source_paragraphs=len(records),translated_through_line=None,status='pending'))
manifest=dict(source=str(src),sha256=hashlib.sha256(raw).hexdigest(),settings=dict(language='American English',style='Faithful literary translation without abridgment',names='Unaccented pinyin for Chinese names; original names for foreign characters',format='English only with minimal cultural footnotes'),books=books)
(work/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(books,ensure_ascii=False,indent=2))
