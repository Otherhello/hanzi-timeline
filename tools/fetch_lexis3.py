#!/usr/bin/env python3
import re
dat = open('../data/_lexis_ancient_ma.html', encoding='utf-8').read()
# Find all php endpoints / dynamic image generators
phps = sorted(set(re.findall(r'[\w/]+\.php\?[^"\'<> ]+', dat)))
print('=== php endpoints ===')
for p in phps[:40]:
    print('  ', p)

# Find table headers in 字形 section
print()
print('=== era header <th> texts ===')
for m in re.finditer(r'<th[^>]*>([^<]{1,12})</th>', dat):
    print('  th:', m.group(1).strip())

# Find context around 隸書 / 楷書 / 金文 / 甲骨 in the glyph table
for kw in ['隸書','楷書','金文','甲骨','字形演變','演變']:
    idx = dat.find(kw)
    if idx >= 0:
        s=max(0,idx-200); e=min(len(dat), idx+300)
        print(f'--- {kw} @{idx} ---')
        print(re.sub(r'\s+',' ',dat[s:e]))
