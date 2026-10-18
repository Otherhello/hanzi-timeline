#!/usr/bin/env python3
import urllib.request, urllib.error, http.cookiejar, gzip, io
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
BASE = 'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-Agent', UA)]

# 1) establish session by loading search.php?word=馬
try:
    r = opener.open(BASE + 'search.php?word=%E9%A6%AC', timeout=15)
    r.read()
    print('session cookies:', [c.name for c in cj])
except Exception as e:
    print('session err', e)

# helper to fetch image with referer + encoding handling
def fetch(path, referer):
    req = urllib.request.Request(BASE + path, headers={'Referer': BASE + referer, 'Accept-Encoding': 'identity'})
    try:
        with opener.open(req, timeout=15) as resp:
            data = resp.read()
            ct = resp.headers.get('Content-Type', '?')
            return ct, data
    except Exception as e:
        return None, str(e)[:60]

for name, path, ref in [
    ('kangxiArchaic 小篆', 'kangxiArchaic.php?hash=ba4d618d1e3a66b248ae2a12edf56a90', 'search.php?word=%E9%A6%AC'),
    ('bronze 父辛尊', 'bronze.php?id=78550', 'search.php?word=%E9%A6%AC'),
    ('bronze 虢季子白盤', 'bronze.php?id=99373', 'search.php?word=%E9%A6%AC'),
    ('oracle 合集', 'oracle.php?code=E8BF', 'search.php?word=%E9%A6%AC'),
    ('silk 睡虎地', 'silk.php?hash=f4333c64cde09a71e065840bcb2b3f28', 'search.php?word=%E9%A6%AC'),
]:
    ct, data = fetch(path, ref)
    magic = data[:12] if isinstance(data, bytes) else data
    print(f'[{name}] ct={ct} len={len(data) if isinstance(data,bytes) else data} magic={magic!r}')
