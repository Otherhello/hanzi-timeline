#!/usr/bin/env python3
import re
dat = open('../data/_lexis_ma.html', encoding='utf-8').read()

# Each era is a <table class="char_anc_table..."> block containing a <th>ERA</th>
blocks = re.split(r'<table class="char_anc_table', dat)[1:]  # drop lead-in
for blk in blocks:
    # era header
    thm = re.search(r'<th[^>]*>(.*?)</th>', blk, re.S)
    era = re.sub(r'<[^>]+>', '', thm.group(1)).strip() if thm else '?'
    # image cells
    cells = re.findall(
        r"<img src='([^']+\.php\?[^']+)'[^>]*onmouseover=\"mouseoverlayer\(\d+, '([^']*)'",
        blk)
    print(f'=== {era} ({len(cells)} img) ===')
    for src, tip in cells:
        tipclean = re.sub(r'<[^>]+>', '', tip)
        tipclean = re.sub(r'\s+', ' ', tipclean).strip()
        print(f'   {src:55s}  {tipclean}')
