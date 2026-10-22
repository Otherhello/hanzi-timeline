#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""探测《漢語多功能字庫》字页能否访问，并抽出每期字形图的源 path。

用途：给 characters.ts 的每条字形挂「图片来源链接」（精确到 oracle.php?code= / bronze.php?id= / silk.php?hash=）。
本脚本只读取，不写数据。
"""
import sys, re, urllib.request, urllib.parse

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120 Safari/537.36')
BASE = 'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/'


def main():
    words = sys.argv[1:] or ['馬']
    for w in words:
        url = BASE + 'search.php?word=' + urllib.parse.quote(w)
        req = urllib.request.Request(url, headers={
            'User-Agent': UA, 'Referer': BASE + 'search.php',
            'Accept-Encoding': 'identity'})
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                html = r.read().decode('utf-8', 'replace')
        except Exception as e:
            print(f'FAIL {w}: {type(e).__name__}: {e}')
            continue
        tables = re.findall(r'class="char_anc_table', html)
        imgs = re.findall(r"<img src='([^']+\.php\?[^']+)'", html)
        print(f'{w}: html={len(html)}B tables={len(tables)} imgs={len(imgs)}')
        for p in imgs[:6]:
            print('   ', p)


if __name__ == '__main__':
    main()
