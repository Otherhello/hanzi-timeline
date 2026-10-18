#!/usr/bin/env python3
import re
# search.php page for 馬 (saved as _lexis_ma.html)
dat = open('../data/_lexis_ma.html', encoding='utf-8').read()

# All php image endpoints with mouseover tooltips
cells = re.findall(r"<img src='([^']+\.php\?[^']+)'[^>]*onmouseover=\"mouseoverlayer\(\d+, '([^']*)'", dat)
print('img php cells in search.php 馬:')
for src, tip in cells:
    print('  ', src, '=>', tip)

# Also bare .php?hash= anywhere
allsrcs = sorted(set(re.findall(r"[\w/]+\.php\?hash=[0-9a-f]+", dat)))
print('\nall php?hash endpoints:')
for s in allsrcs[:30]:
    print('  ', s)

# bronze.php and oracle.php links (they are <a href> to artifact pages)
for nm in ['bronze','oracle','kangxi','jinwen','jiaguwen','gudian']:
    hits = re.findall(nm + r'\.php\?[a-z]+=\d+[0-9a-f]*', dat)
    print(f'\n{nm}.php hits: {len(set(hits))}')
# Look for the tab menu showing whether 甲骨/金文 tabs exist in 字形
for kw in ['m-anc','ancTable','archaic','甲骨部件','金文部件']:
    if kw in dat:
        print('  struct kw:', kw)
