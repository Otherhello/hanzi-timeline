#!/usr/bin/env python3
"""抓取历代名帖做「虚化纸背」背景图。

- 来源：维基共享资源（公有领域的名帖扫描件 / 拓本）
- 处理：取 1400px 缩略图 → 转 JPEG(q76) → 存 public/backdrops/
- 产物：data/backdrops.json（含作品名 / 书家 / 时代 / 书体 / 来源页）

用法：python tools/fetch_backdrops.py [--redo]
"""

import json, os, ssl, sys, time, urllib.error, urllib.parse, urllib.request

from PIL import Image, ImageOps

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/120 Safari/537.36')
API = 'https://commons.wikimedia.org/w/api.php'

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
OUT_DIR = os.path.join(ROOT, 'public', 'backdrops')
MANIFEST = os.path.join(ROOT, 'data', 'backdrops.json')

# key, 作品名, 书家, 时代, 书体, 检索词（依次尝试）
# 已知最佳文件（跳过检索直接取，避免搜到展牌 / 建筑照片）
FORCE_FILES = {
    'duobaota': ['File:多宝塔碑.唐.颜真卿.书.清中晚期拓片.东京国立博物馆藏.jpg'],
    'caoquanbei': ['File:Cao Quan Bei Lishu.jpg', 'File:曹全碑.jpg'],
}

# 部分博物馆扫描件底部带比色卡与编号标签，裁掉
CROP_BOTTOM = {'jizhiwengao': 0.16, 'zixutie': 0.16, 'shusutie': 0.16}

WORKS = [
    ('lanting', '蘭亭集序（馮承素摹本）', '王羲之', '東晉', '行書',
     ['蘭亭集序', 'Lantingji Xu', 'Lanting Xu']),
    ('jizhiwengao', '祭姪文稿', '顏真卿', '唐', '行書',
     ['祭姪文稿', 'Jizhi Wengao', 'Ji Zhi Wen Gao']),
    ('zixutie', '自敘帖', '懷素', '唐', '草書',
     ['懷素 自敘帖', '自敘帖', 'Huaisu Zixu', 'Zixu Tie']),
    ('jiuchenggong', '九成宮醴泉銘', '歐陽詢', '唐', '楷書',
     ['九成宮醴泉銘', '九成宫醴泉铭', 'Jiucheng Gong Quanming', 'Ouyang Xun Jiucheng']),
    ('duobaota', '多寶塔碑', '顏真卿', '唐', '楷書',
     ['多寶塔碑 拓本', 'Yan Zhenqing Duobao Pagoda', '多寶塔碑']),
    ('caoquanbei', '曹全碑', '佚名', '東漢', '隸書',
     ['曹全碑 拓本', '曹全碑', 'Cao Quan Bei rubbing']),
    ('shusutie', '蜀素帖', '米芾', '北宋', '行書',
     ['蜀素帖 米芾', '蜀素帖', 'Mi Fu Shusu']),
]


def api(params: dict) -> dict:
    q = urllib.parse.urlencode({**params, 'format': 'json', 'formatversion': '2'})
    url = API + '?' + q
    last = None
    for attempt in range(5):
        try:
            time.sleep(1.2)  # 温和限速，避免共享资源 429
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (429, 500, 502, 503, 504):
                wait = 4 * (2 ** attempt)
                print(f'   {e.code} 限流，{wait}s 后重试')
                time.sleep(wait)
                continue
            raise
        except Exception as e:
            last = e
            time.sleep(3)
    raise last


def search_files(term: str, limit=8):
    try:
        d = api({'action': 'query', 'list': 'search', 'srsearch': term,
                 'srnamespace': '6', 'srlimit': str(limit)})
    except Exception as e:
        print('   search fail', term, type(e).__name__)
        return []
    return [x['title'] for x in d.get('query', {}).get('search', [])
            if x['title'].lower().endswith(('.jpg', '.jpeg', '.png'))]


def imageinfo(titles, width=1400):
    if not titles:
        return {}
    d = api({'action': 'query', 'titles': '|'.join(titles), 'prop': 'imageinfo',
             'iiprop': 'url|size', 'iiurlwidth': str(width)})
    out = {}
    for p in d.get('query', {}).get('pages', []):
        ii = (p.get('imageinfo') or [{}])[0]
        if ii.get('thumburl'):
            out[p['title']] = ii
    return out


def pick_best(titles, info):
    """优先选宽高比适合做整页背景、且确为字迹图像的长卷/册页。"""
    BAD = ('stamp', '郵票', '邮票', 'fishing', 'port', 'placard', 'map',
           'museum lobby', 'panorama', '碑林', 'no.0', '文言', '展牌')
    GOOD = ('拓', 'rubbing', '卷', '帖', '摹', '墨蹟', '墨迹', '碑', '册')
    best, best_score = None, -1
    for t in titles:
        ii = info.get(t)
        if not ii:
            continue
        w, h = ii.get('width', 0), ii.get('height', 0)
        if not w or not h:
            continue
        low = t.lower()
        if any(b in low for b in BAD):
            continue
        ratio = w / h
        if ratio < 0.35 or ratio > 12:
            continue
        score = 0.0
        if 1.2 <= ratio <= 2.5:
            score += 3
        elif 2.5 < ratio <= 4.0:
            score += 1
        elif ratio > 4.0:
            score -= 1.5
        score += min(w / 4000.0, 1.5)
        if any(g in t for g in GOOD):
            score += 1.5
        if score > best_score:
            best, best_score = (t, ii), score
    return best


def fetch(url: str) -> bytes | None:
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.read()
    except Exception as e:
        print('   download fail', type(e).__name__, e)
        return None


def main():
    redo = '--redo' in sys.argv
    only = None
    for i, a in enumerate(sys.argv):
        if a == '--only' and i + 1 < len(sys.argv):
            only = [x.strip() for x in sys.argv[i + 1].split(',') if x.strip()]
    os.makedirs(OUT_DIR, exist_ok=True)
    manifest = {}
    if os.path.exists(MANIFEST):
        manifest = json.load(open(MANIFEST, encoding='utf-8'))

    for key, name, artist, period, script, terms in WORKS:
        dest = os.path.join(OUT_DIR, f'{key}.jpg')
        if only and key not in only:
            continue
        if key in manifest and os.path.exists(dest) and not redo:
            print(f'== {key} 跳过（已有）')
            continue
        print(f'== {key}  {name}')

        chosen = None
        for forced in FORCE_FILES.get(key, []):
            info = imageinfo([forced])
            if forced in info:
                chosen = (forced, info[forced])
                print(f'   直取 {forced}  {info[forced]["width"]}x{info[forced]["height"]}')
                break
        for term in ([] if chosen else terms):
            titles = search_files(term)
            if not titles:
                continue
            info = imageinfo(titles)
            chosen = pick_best(titles, info)
            if chosen:
                print(f'   命中「{term}」→ {chosen[0]}  {chosen[1]["width"]}x{chosen[1]["height"]}')
                break
        if not chosen:
            print('   !! 未找到')
            continue

        title, ii = chosen
        # 超长卷（如寒食帖 19:1）：按裁剪后仍够宽来反推缩略图宽度
        r0 = ii['width'] / max(ii['height'], 1)
        if r0 > 6:
            want = min(ii['width'], int(1600 * r0 / 2.0))
            ii2 = imageinfo([title], width=want).get(title)
            if ii2 and ii2.get('thumburl'):
                ii = ii2
        data = fetch(ii['thumburl'])
        if not data:
            continue
        try:
            img = Image.open(__import__('io').BytesIO(data)).convert('RGB')
        except Exception as e:
            print('   !! 解码失败', type(e).__name__)
            continue
        # 裁掉底部比色卡 / 藏品编号条
        cb = CROP_BOTTOM.get(key)
        if cb:
            w0, h0 = img.size
            img = img.crop((0, 0, w0, int(h0 * (1 - cb))))
        # 超长卷：裁出居中一段（约 1.8:1），避免整幅缩成一条细线
        w, h = img.size
        if w / h > 2.2:
            seg = min(w, int(h * 1.8))
            x0 = max(0, (w - seg) // 2)
            img = img.crop((x0, 0, x0 + seg, h))
        # 统一长边 1400
        mw = max(img.size)
        if mw > 1400:
            r = 1400 / mw
            img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
        # 深色拓本反白为墨稿：与「宣纸 + 墨」的整体调子统一，
        # 否则整屏会压成灰黑，干扰正文。反白事实记入 manifest 的 inverted 字段。
        inverted = False
        gray = img.convert('L')
        if sum(gray.resize((48, 48)).getdata()) / (48 * 48) < 125:
            img = ImageOps.autocontrast(ImageOps.invert(gray), cutoff=1).convert('RGB')
            inverted = True
            print('   .. 原图为深色拓本，已反白')
        img.save(dest, 'JPEG', quality=80, optimize=True, progressive=True)
        size_kb = os.path.getsize(dest) / 1024
        page = 'https://commons.wikimedia.org/wiki/' + title.replace(' ', '_')
        manifest[key] = {
            'key': key, 'name': name, 'artist': artist, 'period': period,
            'script': script, 'file': f'backdrops/{key}.jpg',
            'source': page, 'title': title,
            'size': f'{img.width}x{img.height}', 'kb': round(size_kb, 1),
            **({'inverted': True} if inverted else {}),
        }
        print(f'   ✓ {key}.jpg  {img.width}x{img.height}  {size_kb:.0f} KB')
        json.dump(manifest, open(MANIFEST, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)

    json.dump(manifest, open(MANIFEST, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f'\n共 {len(manifest)} 幅 → {MANIFEST}')


if __name__ == '__main__':
    main()
