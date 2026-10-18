#!/usr/bin/env python3
import re, urllib.request
UA = {'User-Agent': 'Mozilla/5.0 (hanzi-timeline coursework)'}

def get(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read(), resp.geturl()
    except Exception as e:
        return None, None, f'{type(e).__name__}: {e}'

# 小學堂 首页  及 逐字查询
for name, url in [
    ('xiaoxue home', 'https://xiaoxue.iis.sinica.edu.tw/xiaoxue'),
    ('小學堂 字形 馬', 'https://xiaoxue.iis.sinica.edu.tw/chu/redirect.php?char=%E9%A6%AC'),
    ('小學堂 甲骨 馬', 'https://xiaoxue.iis.sinica.edu.tw/jgw/redirect.php?char=%E9%A6%AC'),
]:
    st, dat, final = get(url)
    print(f'== {name} ==')
    print(f'   status={st} final={final}')
    if dat:
        text = dat.decode('utf-8', errors='replace')
        imgs = re.findall(r'(?:src|href)="([^"]+\.(?:png|gif|jpg|jpeg|svg))"', text)
        phps = re.findall(r'[\w/]+\.php[\w=&?%]*', text)
        print(f'   len={len(text)} imgs={len(imgs)} unique_php={len(set(phps))}')
        for i in imgs[:8]:
            print('     img:', i)
        for kw in ['甲骨','金文','小篆','隸書','楷書','字形','演變','charset','frameset','frame']:
            if kw in text:
                print(f'     kw: {kw}')
