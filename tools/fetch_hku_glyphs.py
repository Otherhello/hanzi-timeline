#!/usr/bin/env python3
"""从 香港中文大學《漢語多功能字庫》抓取逐字、分时代字形图及出处。

每个字形都对应真实文物：
- 甲骨文  → oracle.php?code=  → 《甲骨文合集》+ CHANT 编号
- 金文    → bronze.php?id=    → 具体青铜器（器名+时代+CHANT 编号）
- 简帛文字 → silk.php?hash=   → 睡虎地秦简 / 马王堆帛书（具体篇名+编号）
- 小篆    → kangxiArchaic.php → 說文小篆（康熙圖）/ 說文籀文

服务器要求带 Referer 才返回图片（否则 0 字节）。
产物：
  public/glyphs/{char}-{era}-{n}.jpg      字形图
  data/hku_glyphs.json                     出处清单（供 generate_glyph_data.py 合并）
"""

import os, re, sys, json, urllib.request, urllib.error, html as htmllib

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120 Safari/537.36')
BASE = 'https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/'

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
GLYPHS_DIR = os.path.join(ROOT, 'public', 'glyphs')
MANIFEST_PATH = os.path.join(ROOT, 'data', 'hku_glyphs.json')

# 8 个演示字（正体字头）
CHARS = ['馬', '牛', '山', '水', '日', '月', '人', '紙']


def fetch_page(word: str) -> str | None:
    """抓取 search.php 页面 HTML，带 Referer。"""
    url = BASE + 'search.php?word=' + urllib.parse.quote(word)
    return html_fetch(url, referer='search.php')


def html_fetch(url: str, referer: str) -> str | None:
    req = urllib.request.Request(url, headers={
        'User-Agent': UA, 'Referer': BASE + referer,
        'Accept-Encoding': 'identity'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'  [!] fetch fail {url}: {type(e).__name__}: {e}')
        return None


def image_fetch(path: str, referer: str) -> bytes | None:
    """抓取字形图（带 Referer）。"""
    url = BASE + path
    req = urllib.request.Request(url, headers={
        'User-Agent': UA, 'Referer': BASE + referer,
        'Accept-Encoding': 'identity'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read()
    except Exception as e:
        print(f'  [!] img fail {path}: {type(e).__name__}: {e}')
        return None


def parse_era_tables(html: str):
    """返回 [{era, entries:[{src, tip}]}]"""
    result = []
    blocks = re.split(r'<table class="char_anc_table', html)[1:]
    for blk in blocks:
        thm = re.search(r'<th[^>]*>(.*?)</th>', blk, re.S)
        era = re.sub(r'<[^>]+>', '', thm.group(1)).strip() if thm else '?'
        cells = re.findall(
            r"<img src='([^']+\.php\?[^']+)'[^>]*onmouseover=\"mouseoverlayer\(\d+, '([^']*)'",
            blk)
        entries = []
        for src, tip in cells:
            tipclean = re.sub(r'<[^>]+>', '', tip)
            tipclean = htmllib.unescape(re.sub(r'\s+', ' ', tipclean)).strip()
            src = src.replace('&amp;', '&')
            entries.append({'src': src, 'tip': tipclean})
        if entries:
            result.append({'era': era, 'entries': entries})
    return result


def pick_for_era(era: str, tables) -> list[str]:
    """根据时代从解析结果挑源 path 列表。"""
    picks = []
    for t in tables:
        if era == '甲骨':
            if t['era'] == '甲骨':
                picks += [e['src'] for e in t['entries']][:1]
        elif era == '金文':
            if t['era'] == '金文':
                # 取最早的两件（商→西周），每件一次
                picks += [e['src'] for e in t['entries'] if '商' in e['tip']][:1]
                picks += [e['src'] for e in t['entries'] if '西周' in e['tip']][:1]
                picks += [e['src'] for e in t['entries'] if '春秋' in e['tip']][:1]
        elif era == '简帛':
            if t['era'] == '簡帛文字':
                for e in t['entries']:
                    if '馬王堆' in e['tip']:
                        picks.append(e['src']); break
                if not picks:
                    for e in t['entries']:
                        if '睡虎地' in e['tip']:
                            picks.append(e['src']); break
        elif era == '籀文':
            if t['era'] == '其他':
                for e in t['entries']:
                    if '籀文' in e['tip']:
                        picks.append(e['src']); break
        elif era == '戰國金文':
            if t['era'] == '金文':
                picks += [e['src'] for e in t['entries'] if '戰國' in e['tip']][:1]
    # 去重、保留顺序
    seen = set(); out = []
    for p in picks:
        if p not in seen:
            seen.add(p); out.append(p)
    return out


def tip_for(path: str, tables) -> str:
    for t in tables:
        for e in t['entries']:
            if e['src'] == path:
                return e['tip']
    return ''


def download(word: str) -> dict:
    print(f'== {word} ==')
    html = fetch_page(word)
    if not html:
        return {}
    tables = parse_era_tables(html)
    meta = {}
    # 各时代源 path
    era_srcs = {
        'jiaguwen': pick_for_era('甲骨', tables),
        'jinwen': pick_for_era('金文', tables),
        'zhanguo': pick_for_era('戰國金文', tables),
        'zhuanwen': pick_for_era('籀文', tables),
        'lishu': pick_for_era('简帛', tables),
    }
    for era, paths in era_srcs.items():
        saved = []
        for n, path in enumerate(paths, start=1):
            fname = f'{word}-{era}-{n}.jpg'
            dest = os.path.join(GLYPHS_DIR, fname)
            data = image_fetch(path, referer='search.php?word=' + urllib.parse.quote(word))
            if data and data[:2] == b'\xff\xd8':  # JPEG
                with open(dest, 'wb') as f:
                    f.write(data)
                tip = tip_for(path, tables)
                saved.append({
                    'imageSrc': f'/glyphs/{fname}',
                    'provenance': tip,
                    'bytes': len(data),
                })
                print(f'   [{era}] {fname} ({len(data)}B)  {tip}')
            else:
                print(f'   [{era}] SKIP {path} (no jpeg)')
        meta[era] = saved
    return meta


def main():
    os.makedirs(GLYPHS_DIR, exist_ok=True)
    manifest = {}
    for ch in CHARS:
        manifest[ch] = download(ch)
        print()
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f'Wrote {MANIFEST_PATH}')


if __name__ == '__main__':
    main()
