#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为 data/hku_glyphs.json 的每条字形补上「精确来源页」链接。

背景：
  fetch_hku_glyphs.py 下载字形图时用的是 oracle.php?code= / bronze.php?id= /
  silk.php?hash= / kangxiArchaic.php?hash= 这类带参数的图片地址，但当时没把
  该 path 记进清单，导致前端无法给出「这张图来自哪一页」。

做法（只读站内页面，不重下图片）：
  1. 重新抓一次 search.php?word=字，用与 fetch_hku_glyphs 相同的解析/挑选函数
     复算出每期字形图的源 path 列表；
  2. 与清单里同期的条目按条数对齐（条数不符时退回按 provenance 提示文字匹配）；
  3. 给每条写入 srcPath（站内相对 path）与 srcUrl（完整可点链接）。

用法：python tools/link_hku_sources.py [字 ...]
产物：data/hku_glyphs.json 原地更新（新增 srcPath / srcUrl 两键）
"""

import os
import sys
import time
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import fetch_hku_glyphs as f  # noqa: E402

MANIFEST_PATH = f.MANIFEST_PATH


def era_sources(tables):
    """复算 download() 里的 era -> [path] 映射（顺序与下载顺序一致）。"""
    zhanguo = f.pick_for_era('戰國金文', tables)
    return {
        'jiaguwen': f.pick_for_era('甲骨', tables),
        'jinwen': f.pick_for_era('金文', tables),
        'zhanguo': zhanguo,
        'zhanguo_qin': [] if zhanguo else f.pick_for_era('戰國秦系', tables),
        'zhuanwen': f.pick_for_era('籀文', tables),
        'xiaozhuan': f.pick_for_era('小篆', tables),
        'lishu': f.pick_for_era('简帛', tables),
    }


def main():
    only = sys.argv[1:]
    with open(MANIFEST_PATH, encoding='utf-8') as fh:
        manifest = json.load(fh)

    chars = only if only else [c for c in manifest if manifest[c]]
    total_hit = 0
    total_miss = 0

    for ch in chars:
        entries_by_era = manifest.get(ch) or {}
        if not entries_by_era:
            print(f'[{ch}] 清单为空，跳过')
            continue
        html = f.fetch_page(ch)
        if not html:
            print(f'[{ch}] 字页抓取失败，跳过')
            total_miss += sum(len(v) for v in entries_by_era.values())
            continue
        tables = f.parse_era_tables(html)
        srcs = era_sources(tables)
        tip_map = {}
        for era, paths in srcs.items():
            for p in paths:
                tip_map.setdefault((era, f.tip_for(p, tables)), p)

        hit = miss = 0
        for era, entries in entries_by_era.items():
            paths = srcs.get(era, [])
            for i, entry in enumerate(entries):
                path = None
                if len(paths) == len(entries):
                    path = paths[i]
                else:
                    path = tip_map.get((era, entry.get('provenance', '')))
                if path:
                    entry['srcPath'] = path
                    entry['srcUrl'] = f.BASE + path
                    hit += 1
                else:
                    entry.pop('srcPath', None)
                    entry.pop('srcUrl', None)
                    miss += 1
        total_hit += hit
        total_miss += miss
        print(f'[{ch}] 命中 {hit} 条，未命中 {miss} 条')
        time.sleep(0.8)

    with open(MANIFEST_PATH, 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    print(f'\n完成：命中 {total_hit}，未命中 {total_miss} -> {MANIFEST_PATH}')


if __name__ == '__main__':
    main()
