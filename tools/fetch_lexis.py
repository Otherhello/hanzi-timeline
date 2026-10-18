#!/usr/bin/env python3
import urllib.request, re, sys
UA = {'User-Agent': 'Mozilla/5.0 (hanzi-timeline coursework)'}
url = 'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=%E9%A6%AC'
dat = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=15).read().decode('utf-8', errors='replace')
open('../data/_lexis_ma.html', 'w', encoding='utf-8').write(dat)
# find contexts around 甲骨 / 金文 / 小篆
for kw in ['殷商','甲骨','金文','小篆','隸書','楷書','演變']:
    for m in re.finditer(kw, dat):
        s = max(0, m.start()-120); e = min(len(dat), m.end()+160)
        print(f'--- {kw} @{m.start()} ---')
        print(re.sub(r'\s+', ' ', dat[s:e]))
        break
