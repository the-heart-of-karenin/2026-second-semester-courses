"""Check the two-section inventory and refresh the derived source indexes."""
from pathlib import Path
import csv
import re
from collections import Counter

root = Path(__file__).resolve().parent
path = root / 'exercises.tex'
text = path.read_text(encoding='utf-8')

def arg_at(s, start):
    assert s[start] == '{'
    depth, pos = 1, start + 1
    while depth:
        ch = s[pos]
        k = pos - 1
        while k >= 0 and s[k] == '\\':
            k -= 1
        escaped = (pos - k - 1) % 2
        if ch == '{' and not escaped:
            depth += 1
        elif ch == '}' and not escaped:
            depth -= 1
        pos += 1
    return s[start + 1:pos - 1], pos

rows = []
for match in re.finditer(r'\\exercise\{', text):
    pos = match.end() - 1
    title, pos = arg_at(text, pos)
    source, pos = arg_at(text, pos)
    body, pos = arg_at(text, pos)
    # An additional task makes a selection an adaptation, even if its core is unchanged.
    if source.startswith('选录') and any(w in body + source for w in ('新增', '另确定', '再判断', '再证明', '进一步', '后一项', '第二问', '新增双线性', '指定反例')):
        source = source.replace('选录', '改编', 1)
    kind = '自拟' if source.startswith('自拟') else ('改编' if '改编' in source[:5] else '选录')
    i = len(rows) + 1
    rows.append({'题号': i, '节': 1 if i <= 60 else 2, '题目': title,
                 '类型': kind, '来源与改编说明': source, 'body': body,
                 'start': match.start(), 'end': pos})

assert len(rows) == 100, len(rows)
boundary = text.index('\\section{习题二')
assert sum(row['start'] < boundary for row in rows) == 60
assert len({row['题目'] for row in rows}) == 100
assert all(row['body'].strip() for row in rows)

# Only normalize the source classification; never regenerate mathematical body text.
for row in reversed(rows):
    start, end = row['start'], row['end']
    original = text[start:end]
    _, p = arg_at(original, original.index('{'))
    _, q = arg_at(original, p)
    replacement = original[:p] + '{' + row['来源与改编说明'] + '}' + original[q:]
    text = text[:start] + replacement + text[end:]
path.write_text(text, encoding='utf-8')

fields = ['题号', '节', '题目', '类型', '来源与改编说明']
with (root / '题目来源.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(rows)

counts = Counter(row['类型'] for row in rows)
out = ['# 100题来源清单', '',
       '本表由直接修改入口 exercises.tex 提取；每个题号为一组，小问不另计。', '',
       f'共100题，第一节60题，第二节40题。选录{counts["选录"]}组，改编{counts["改编"]}组，自拟{counts["自拟"]}组。', '',
       '选录/改编给出核对过的原书位置；自拟项只给方法背景，不声称具有对应原题。', '',
       '原始资料：课程参考书目录中的史济怀、Stein、Simon Part 2A、Lang第4版；课堂整理稿位于课程根目录。', '',
       '已有作业和两份期末排除范围及近似题辨析见审校记录.md。', '',
       '| 题号 | 节 | 题目 | 类型 | 来源与说明 |', '|---|---|---|---|---|']
for row in rows:
    out.append('| ' + ' | '.join(str(row[field]).replace('|', '\\|') for field in fields) + ' |')
(root / '来源清单.md').write_text('\n'.join(out) + '\n', encoding='utf-8')
print({'total': len(rows), 'section_1': 60, 'section_2': 40, 'types': dict(counts)})
