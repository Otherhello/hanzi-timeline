#!/usr/bin/env python3
"""从 Wikimedia Commons 下载說文字头篆书图片，存入 public/glyphs/。

这些图片由 Wikisource 說文解字项目贡献，为《說文》小篆字头的标准再现。
许可：公有领域（PD-old / CC0）。
"""

import os, sys, time, json, urllib.request, urllib.error
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
GLYPHS_DIR = os.path.join(ROOT, 'public', 'glyphs')

UA = 'hanzi-timeline/1.0 (coursework; wikisource-fetch)'


def resolve_file_url(filename: str) -> str | None:
    """用 Commons API 取文件的原始上传地址。

    直接用 Special:FilePath 会被限流（HTTP 429），而 API + upload.wikimedia.org 稳定。
    """
    q = ('https://commons.wikimedia.org/w/api.php?action=query&format=json'
         '&prop=imageinfo&iiprop=url&titles=' + quote('File:' + filename))
    req = urllib.request.Request(q, headers={'User-Agent': UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.load(resp)
            pages = data.get('query', {}).get('pages', {})
            for page in pages.values():
                info = page.get('imageinfo')
                if info:
                    return info[0]['url']
            return None
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    return None


DEMO_CHARS = [
    '馬', '牛', '山', '水', '日', '月', '人', '紙',
    '木', '土', '田', '雨', '魚', '鳥', '犬', '門',
    '貝', '玉', '文', '目', '耳', '口', '心', '大',
    '王', '車', '石', '羊',
]


def thumb_url(original_url: str, width: int = 500) -> str:
    """把原始文件地址转成 Wikimedia 缩略图地址。

    Wikimedia 对「原始文件」的批量请求会返回 HTTP 429（retry-after 600s），
    但明确要求改用缩略图
    （https://upload.wikimedia.org/wikipedia/commons/thumb/<h1>/<h2>/<name>/<w>px-<name>.png）。
    """
    u = original_url.split('?')[0]
    marker = '/wikipedia/commons/'
    idx = u.find(marker)
    if idx < 0:
        return original_url
    rest = u[idx + len(marker):]          # b/b0/雨-seal.svg
    h1, h2, name = rest.split('/', 2)
    return (f'https://upload.wikimedia.org/wikipedia/commons/thumb/{h1}/{h2}/'
            f'{name}/{width}px-{name}.png')


def download_seal(char: str, dest_dir: str) -> bool:
    """下载一个字的篆书字形（优先原 SVG，取不到时退回 PNG 缩略图）。"""
    filename = f'{char}-seal.svg'
    dest_svg = os.path.join(dest_dir, filename)
    dest_png = os.path.join(dest_dir, f'{char}-seal.png')
    if os.path.exists(dest_svg):
        print(f'  skip (exists): {filename}')
        return True
    if os.path.exists(dest_png):
        print(f'  skip (exists): {char}-seal.png')
        return True

    try:
        url = resolve_file_url(filename)
    except Exception as e:  # noqa: BLE001
        print(f'  FAIL {filename}: resolve error {e}')
        return False
    if not url:
        print(f'  MISS {filename}: 该文件在 Commons 不存在')
        return False

    # 先试原图（若未被限流则拿到矢量 SVG）
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
                ctype = resp.headers.get('Content-Type', '')
            with open(dest_svg, 'wb') as f:
                f.write(data)
            print(f'  done: {filename}  ({len(data)} bytes, {ctype})')
            return True
        except urllib.error.HTTPError as e:
            if e.code == 429:
                break
            print(f'  FAIL {filename}: HTTP {e.code}')
            return False
        except Exception as e:  # noqa: BLE001
            print(f'  FAIL {filename}: {e}')
            return False

    # 退回缩略图 PNG
    turl = thumb_url(url)
    for attempt in range(3):
        try:
            req = urllib.request.Request(turl, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
                ctype = resp.headers.get('Content-Type', '')
            if not data.startswith(b'\x89PNG'):
                print(f'  FAIL {char}-seal.png: 非 PNG 内容 ({ctype})')
                return False
            with open(dest_png, 'wb') as f:
                f.write(data)
            print(f'  done: {char}-seal.png  ({len(data)} bytes, 缩略图)')
            return True
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                wait = 10 * (attempt + 1)
                print(f'  ... 429, retry in {wait}s')
                time.sleep(wait)
                continue
            print(f'  FAIL {char}-seal.png: HTTP {e.code}')
            return False
        except Exception as e:  # noqa: BLE001
            print(f'  FAIL {char}-seal.png: {e}')
            return False
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