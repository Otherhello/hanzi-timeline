#!/usr/bin/env python3
"""回填 data/hku_glyphs.json 中缺失的 srcUrl（图片原始出处链接）。

只重抓 search.php 页面（很轻），按 provenance 文本反查图片端点 path，
不重新下载任何图片。
"""

import json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_hku_glyphs as F  # noqa: E402


def main():
    if not os.path.exists(F.MANIFEST_PATH):
        print('no manifest')
        return
    with open(F.MANIFEST_PATH, encoding='utf-8') as f:
        man = json.load(f)

    changed = 0
    for ch, eras in man.items():
        need = [it for items in eras.values() for it in items if not it.get('srcUrl')]
        if not need:
            continue
        print('==', ch, f'({len(need)} missing)')
        html = F.fetch_page(ch)
        if not html:
            print('  fetch fail')
            continue
        tables = F.parse_era_tables(html)
        tipmap = {}
        for t in tables:
            for e in t['entries']:
                tipmap.setdefault(e['tip'], e['src'])
        # 备用索引：CHANT 编号 → path（tip 文本可能随页面措辞微调而不完全一致）
        chantmap = {}
        for t in tables:
            for e in t['entries']:
                mc = re.search(r'CHANT:(\d+)', e['tip'])
                if mc:
                    chantmap.setdefault(mc.group(1), e['src'])
        for items in eras.values():
            for it in items:
                if it.get('srcUrl'):
                    continue
                prov = it.get('provenance', '')
                src = tipmap.get(prov)
                if not src:
                    mc = re.search(r'CHANT:(\d+)', prov)
                    if mc:
                        src = chantmap.get(mc.group(1))
                if src:
                    it['srcUrl'] = F.BASE + src
                    it['srcPath'] = src
                    changed += 1
                else:
                    print('  unmatched:', it.get('provenance'))

    with open(F.MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(man, f, ensure_ascii=False, indent=2)
    print(f'enriched {changed}')


if __name__ == '__main__':
    main()
