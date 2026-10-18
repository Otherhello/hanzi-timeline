#!/usr/bin/env python3
import re, urllib.request
UA = {'User-Agent': 'Mozilla/5.0 (hanzi-timeline coursework)'}

# extract the 字形演變 table from the saved 馬 ancient.php
dat = open('../data/_lexis_ancient_ma.html', encoding='utf-8').read()
# Find the region after "形義通解" table header containing bronze/oracle/kangxi image cells
# Locate first table with 金文/甲骨 headers
m = re.search(r'<table[^>]*class="[^"]*anc[^"]*"[^>]*>.*?</table>', dat, re.S)
if not m:
    m = re.search(r'(<table[^>]*>.*?<th[^>]*>甲骨.*?</table>)', dat, re.S)
blk = m.group(0) if m else ''
print('glyph table len:', len(blk))

# find all image-generating cells and their alt/tooltips
cells = re.findall(r"<img src='([^']+\.php\?[^']+)'[^>]*onmouseover=\"mouseoverlayer\(\d+, '([^']*)'", blk)
print('glyph image cells:', len(cells))
for src, tip in cells:
    print('  ', src, '=>', tip)

# if empty, dump full block text
if not cells:
    print(re.sub(r'\s+', ' ', blk)[:2000])
