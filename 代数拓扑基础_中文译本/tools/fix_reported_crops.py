"""Restore reported original vector figures; never render the compiled book."""
from pathlib import Path
import json
import shutil
import pymupdf as fitz

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / 'LaTeX' / 'figures'
BACKUP = ROOT / 'source' / 'crop-audit' / 'before-repair'
BACKUP.mkdir(parents=True, exist_ok=True)
# Source PDF page numbers are one-based. Rectangles use top-left coordinates.
SPECS = [
    ('3-6-ex-a', 194, (108, 395, 354, 460)),
    ('4-2-1', 207, (68, 56, 370, 246)),
    ('4-3-1', 213, (46, 166, 392, 316)),
    ('4-3-2', 215, (44, 56, 394, 184)),
    ('4-9-3', 254, (108, 56, 331, 259)),
    ('4-9-4', 255, (35, 56, 407, 358)),
    ('4-10-6', 263, (81, 230, 395, 462)),
    ('4-10-2', 259, (54, 437, 384, 578)),
    ('4-11-2', 278, (44, 192, 395, 282)),
    ('4-11-3', 279, (47, 169, 391, 267)),
]

records = []
with fitz.open(ROOT / 'source' / 'original.pdf') as source:
    for name, page_number, bounds in SPECS:
        target = FIGURES / f'{name}.pdf'
        backup = BACKUP / target.name
        if not backup.exists():
            shutil.copy2(target, backup)
        clip = fitz.Rect(bounds)
        assert source[page_number - 1].rect.contains(clip)
        with fitz.open() as result:
            page = result.new_page(width=clip.width, height=clip.height)
            page.show_pdf_page(page.rect, source, page_number - 1, clip=clip)
            temporary = target.with_suffix('.repaired.pdf')
            result.save(temporary, garbage=4, deflate=True)
        temporary.replace(target)
        with fitz.open(target) as check:
            assert len(check) == 1
            assert abs(check[0].rect.width - clip.width) < .01
            assert abs(check[0].rect.height - clip.height) < .01
        records.append({'figure': name, 'source_pdf_page': page_number,
                        'clip': list(bounds), 'vector_preserved': True})

(ROOT / 'source' / 'crop-audit' / 'repairs.json').write_text(
    json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Restored {len(records)} original PDF figure crops.')
