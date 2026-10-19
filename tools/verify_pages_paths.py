"""模拟 GitHub Pages 项目子站点路径，校验 characters.ts 引用的每张字形图可达。

GitHub Pages 项目站点形如 https://<user>.github.io/<repo>/，
因此页面里的相对路径 glyphs/xxx 最终请求 /<repo>/glyphs/xxx。
本脚本把 dist/ 放到临时目录的 hanzi-timeline/ 下用 http.server 提供，
再逐一请求所有 imageSrc，报告 HTTP 状态与 Content-Type。
"""
import functools
import http.server
import re
import shutil
import socketserver
import sys
import tempfile
import threading
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
CHARS = ROOT / "src" / "data" / "characters.ts"
DIST = ROOT / "dist"


def collect_images() -> list[str]:
    text = CHARS.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"imageSrc:\s*'([^']+)'", text)))


def main() -> int:
    images = collect_images()
    print(f"characters.ts 引用 {len(images)} 张图")

    tmp = Path(tempfile.mkdtemp(prefix="pages-"))
    proj = tmp / "hanzi-timeline"
    shutil.copytree(DIST, proj)

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(tmp))
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as srv:
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()

        bad = []
        for rel in images:
            url = f"http://127.0.0.1:{port}/hanzi-timeline/{quote(rel)}"
            try:
                with urllib.request.urlopen(url) as resp:
                    code = resp.status
                    ctype = resp.headers.get("Content-Type", "")
                    if code != 200:
                        bad.append((rel, code, ctype))
            except Exception as exc:  # noqa: BLE001
                bad.append((rel, "ERR", str(exc)))

        srv.shutdown()

    if bad:
        print(f"\n失败 {len(bad)} 张：")
        for rel, code, info in bad:
            print(f"  {rel} -> {code} {info}")
        return 1
    print(f"全部 {len(images)} 张均 200 OK（模拟 /hanzi-timeline/ 子路径）")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
