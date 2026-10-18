#!/usr/bin/env python3
"""从 Wikimedia Commons 下载說文字头篆书图片，存入 public/glyphs/。

这些图片由 Wikisource 說文解字项目贡献，为《說文》小篆字头的标准再现。
许可：公有领域（PD-old / CC0）。
"""

import os, sys, time, urllib.request, urllib.error
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
GLYPHS_DIR = os.path.join(ROOT, 'public', 'glyphs')

DEMO_CHARS = ['馬', '牛', '山', '水', '日', '人']


def download_seal(char: str, dest_dir: str) -> bool:
    """下载一个字的篆书 SVG，保存为 {char}-seal.svg"""
    filename = f'{char}-seal.svg'
    dest = os.path.join(dest_dir, filename)
    if os.path.exists(dest):
        print(f'  skip (exists): {filename}')
        return True

    # 注意：不带 width 参数则返回原始 SVG（矢量），带 width=300 会得到 PNG 缩略图。
    url = f'https://commons.wikimedia.org/wiki/Special:FilePath/{quote(filename)}'
    req = urllib.request.Request(url, headers={'User-Agent': 'hanzi-timeline/1.0 (coursework; wikisource-fetch)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            real_url = resp.geturl()
        with open(dest, 'wb') as f:
            f.write(data)
        print(f'  done: {filename}  ({len(data)} bytes from {real_url[:80]}...)')
        return True
    except urllib.error.HTTPError as e:
        print(f'  FAIL {filename}: HTTP {e.code}')
        return False
    except Exception as e:
        print(f'  FAIL {filename}: {e}')
        return False


if __name__ == '__main__':
    os.makedirs(GLYPHS_DIR, exist_ok=True)
    ok = 0
    for ch in DEMO_CHARS:
        print(f'Downloading {ch}...')
        if download_seal(ch, GLYPHS_DIR):
            ok += 1
        if ch != DEMO_CHARS[-1]:
            time.sleep(1.0)
    print(f'\nDone: {ok}/{len(DEMO_CHARS)} downloaded to {GLYPHS_DIR}')