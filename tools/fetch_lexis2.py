#!/usr/bin/env python3
import urllib.request, re
UA = {'User-Agent': 'Mozilla/5.0 (hanzi-timeline coursework)'}

# 1) char_anc_table region in saved search.php
html = open('../data/_lexis_ma.html', encoding='utf-8').read()
m = re.search(r'<table class="char_anc_table.*?</table>', html, re.S)
if m:
    blk = m.group(0)
    print('=== char_anc_table block (len %d) ===' % len(blk))
    print(re.sub(r'\s+', ' ', blk)[:1800])
else:
    print('no char_anc_table')

# 2) ancient.php (形義源流通解) for 馬
print()
print('=== ancient.php 馬 ===')
try:
    dat = urllib.request.urlopen(urllib.request.Request('https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/ancient.php?word=%E9%A6%AC', headers=UA), timeout=15).read().decode('utf-8', errors='replace')
    open('../data/_lexis_ancient_ma.html', 'w', encoding='utf-8').write(dat)
    imgs = re.findall(r'(?:src|href)="([^"]+\.(?:png|gif|jpg|jpeg|svg))"', dat)
    print('ancient.php len=%d, imgs=%d' % (len(dat), len(imgs)))
    for i in imgs[:25]:
        print('   img:', i)
    for kw in ['甲骨','金文','小篆','隸書','楷書','演變']:
        if kw in dat:
            print('   kw:', kw)
except Exception as e:
    print('ERR', e)
