#!/usr/bin/env python3
"""Rebuild self-hosted fonts after copy edits. Requires fonttools and brotli."""
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
from fontTools import subset

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
FONTS = PUBLIC / 'assets/fonts'
SOURCES = {
    'Jua': 'https://raw.githubusercontent.com/google/fonts/main/ofl/jua/Jua-Regular.ttf',
    'SUIT': 'https://raw.githubusercontent.com/sun-typeface/SUIT/main/fonts/variable/woff2/SUIT-Variable.woff2',
}
# build-pages.py가 만드는 급수 안내 페이지는 시스템 글꼴을 쓴다(한자 목록까지 넣으면 첫 화면 글꼴이 커진다).
GENERATED = {PUBLIC / 'grades', PUBLIC / 'exam-schedule'}
text = ''.join(path.read_text() for path in sorted(PUBLIC.rglob('*'))
               if path.is_file() and not GENERATED.intersection(path.parents)
               and (path.suffix in {'.html', '.css', '.js', '.mjs', '.vtt'}
                   or (path.parent == PUBLIC / 'assets/hanzi' and path.suffix == '.json')))
with TemporaryDirectory(prefix='hanja-fonts-') as temporary:
    for family, url in SOURCES.items():
        original = Path(temporary) / url.rsplit('/', 1)[-1]
        urlretrieve(url, original)
        options = subset.Options()
        options.flavor = 'woff2'
        font = subset.load_font(str(original), options)
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(text=text)
        subsetter.subset(font)
        output = FONTS / f'{family}-subset.woff2'
        subset.save_font(font, str(output), options)
        print(f'{output.relative_to(ROOT)}: {output.stat().st_size:,} bytes')
