#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""模拟 GitHub Pages 子路径部署，校验 dist 内的资源与全部字形图片能否 200 取回。

GitHub Pages 项目站点部署在 https://<user>.github.io/<repo>/ 下，
本地 dev server 的根路径是 /，两者不同；此处把 dist 挂到一个名为 <repo> 的子目录下
再以根为文档根服务，用以复现子路径环境。
"""
from __future__ import annotations

import functools
import http.server
import os
import re
import socketserver
import sys
import threading
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
DIST = os.path.join(ROOT, 'dist')
DATA_TS = os.path.join(ROOT, 'src', 'data', 'characters.ts')
REPO = 'hanzi-timeline'


def main() -> int:
    if not os.path.isdir(DIST):
        print('找不到 dist，请先 vite build')
        return 1

    # 用一个临时目录把 dist 放到 <tmp>/hanzi-timeline 下
    import tempfile
    tmp = tempfile.mkdtemp(prefix='pages_')
    link = os.path.join(tmp, REPO)
    import shutil
    shutil.copytree(DIST, link)
    os.chdir(tmp)

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=tmp)
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()

    base = f'http://127.0.0.1:{port}/{REPO}/'
    with open(os.path.join(DIST, 'index.html'), encoding='utf-8') as f:
        html = f.read()

    assets = re.findall(r'(?:src|href)="([^"]+)"', html)
    with open(DATA_TS, encoding='utf-8') as f:
        data_text = f.read()
    images = re.findall(r"imageSrc:\s*'([^']+)'", data_text)

    failures = []

    def check(path: str) -> None:
        from urllib.parse import quote
        url = base + quote(path.lstrip('./'))
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                if resp.status != 200:
                    failures.append((path, resp.status))
                    print(f'  FAIL {resp.status} {path}')
                else:
                    print(f'  ok   {resp.status} {path}  ({resp.headers.get("Content-Type", "")})')
        except Exception as e:  # noqa: BLE001
            failures.append((path, str(e)))
            print(f'  FAIL {e} {path}')

    print(f'== 页面与静态资源（{len(assets)}）==')
    for a in assets:
        check(a)

    print(f'\n== 字形图片（{len(images)}）==')
    seen = set()
    for img in images:
        if img in seen:
            continue
        seen.add(img)
    for img in sorted(seen):
        check(img)

    httpd.shutdown()
    print(f'\n合计检查 {len(assets)} 资源 + {len(seen)} 图片；失败 {len(failures)} 项')
    return 0 if not failures else 2


if __name__ == '__main__':
    sys.exit(main())
