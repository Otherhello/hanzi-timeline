#!/usr/bin/env python3
import re
dat = open('../data/_lexis_ma.html', encoding='utf-8').read()
# Find the 字形 table region: from '<th>汉字' (or 小篆) until end of that table
i = dat.find('小篆')
j = dat.find('形義通解')
print('raw region showing era cells:')
start = dat.find('<table', dat.find('汉字'))
# Show the section containing '甲骨' glyph table
k = dat.rfind('<table', 0, dat.find('小篆'))
seg = dat[k: k+4000]
# print first image-bearing row structure
print(re.sub(r'\s+', ' ', seg[:1600]))
