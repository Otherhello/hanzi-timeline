#!/usr/bin/env python3
"""探测各候选字形源：能否拿到逐字、分时代字形图。"""
import urllib.request, re, sys

UA = {'User-Agent': 'Mozilla/5.0 (hanzi-timeline coursework)'}


def get(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read()
    except Exception as e:
        return None, (f'{type(e).__name__}: {e}')


def inspect(name, url, keywords):
    st, dat = get(url)
    if st != 200:
        print(f'[{name}] HTTP {st}  {dat}')
        return None
    text = dat.decode('utf-8', errors='replace')
    imgs = re.findall(r'(?:src|href)="([^"]+\.(?:png|gif|jpg|jpeg|svg))"', text)
    print(f'[{name}] HTTP 200, {len(text)} chars, {len(imgs)} image refs')
    for i in imgs[:20]:
        print('   img:', i)
    for kw in keywords:
        if kw in text:
            print(f'   kw: {kw}')
    return text


inspect('HKU Lexis 馬',
        'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=%E9%A6%AC',
        ['字形演變', '字形', '甲骨', '金文', '小篆', '隸書', '楷書', '簽名'])

inspect('小學堂 馬',
        'https://xiaoxue.iis.sinica.edu.tw/chu/redirect.php?char=%E9%A6%AC',
        ['字形', '甲骨', '金文', '小篆', '隸書', '楷書'])
