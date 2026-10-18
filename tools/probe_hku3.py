#!/usr/bin/env python3
import urllib.request
UA = {'User-Agent': 'Mozilla/5.0 (hanzi-timeline coursework)'}
BASE = 'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/'
tests = [
    ('kangxiArchaic 小篆', 'kangxiArchaic.php?hash=ba4d618d1e3a66b248ae2a12edf56a90'),
    ('kangxiArchaic 籀文', 'kangxiArchaic.php?hash=046f3b509116cbdc24d1379428813905'),
    ('bronze 金文 父辛尊', 'bronze.php?id=78550'),
    ('bronze 金文 虢季子白盤', 'bronze.php?id=99373'),
    ('oracle 甲骨合集', 'oracle.php?code=E8BF'),
    ('silk 睡虎地秦簡', 'silk.php?hash=f4333c64cde09a71e065840bcb2b3f28'),
    ('kangxi.php', 'kangxi.php?hash=1af638fa6deb1f5fcc5de8f068ebb903'),
]
for name, path in tests:
    try:
        req = urllib.request.Request(BASE + path, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            ct = resp.headers.get('Content-Type', '?')
            magic = data[:12]
            print(f'[{name}] HTTP {resp.status} ct={ct} len={len(data)} magic={magic!r}')
    except Exception as e:
        print(f'[{name}] ERR {type(e).__name__}: {str(e)[:70]}')
