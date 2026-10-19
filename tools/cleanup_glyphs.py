#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 public/glyphs 下未被 characters.ts 引用的孤儿图片。

生成器只会引用「确实存在且被选中」的图片；抓取脚本重跑后可能留下旧编号的孤儿
（例如某字从 3 张改为 2 张）。本脚本按 characters.ts 中出现的 imageSrc 反查，
删除多余文件，并在最后打印统计。
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
GLYPHS_DIR = os.path.join(ROOT, 'public', 'glyphs')
DATA_TS = os.path.join(ROOT, 'src', 'data', 'characters.ts')


def main() -> int:
    if not os.path.exists(DATA_TS):
        print('找不到 src/data/characters.ts，请先运行 generate_glyph_data.py')
        return 1
    with open(DATA_TS, encoding='utf-8') as f:
        text = f.read()

    referenced = set(re.findall(r"imageSrc:\s*'([^']+)'", text))
    referenced_names = {os.path.basename(p) for p in referenced}

    if not os.path.isdir(GLYPHS_DIR):
        print('找不到 public/glyphs 目录')
        return 1

    existing = {n for n in os.listdir(GLYPHS_DIR) if n.lower().endswith(('.jpg', '.jpeg', '.png', '.svg'))}
    orphans = sorted(existing - referenced_names)

    removed = 0
    for name in orphans:
        path = os.path.join(GLYPHS_DIR, name)
        os.remove(path)
        removed += 1
        print(f'  removed orphan: {name}')

    missing = sorted(referenced_names - existing)
    for name in missing:
        print(f'  WARNING 引用但文件缺失: {name}')

    print(f'\nglyphs: 引用 {len(referenced_names)} 个文件，目录内 {len(existing)} 个，'
          f'删除孤儿 {removed} 个，缺失 {len(missing)} 个')
    return 0 if not missing else 2


if __name__ == '__main__':
    sys.exit(main())
