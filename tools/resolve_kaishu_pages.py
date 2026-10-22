#!/usr/bin/env python3
"""解析每个字在「词典网·书法字典」的字页 URL，写入 data/kaishu_pages.json。

只做页面解析、不下载图片。产物用于生成器给楷书实例挂「来源页」链接：
http://www.cidianwang.com/shufa/{拼音}{id}.htm
（字页同时列出该字各体、各书家、各碑帖，比直链单张图更适合作为查证入口；
 其图床 c.cidianwang.com 的 https 证书已过期，故链接指向 http 的字页。）
"""

import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_kaishu_glyphs as K  # noqa: E402

OUT = os.path.join(K.ROOT, 'data', 'kaishu_pages.json')


def main():
    pages = {}
    for ch in K.CHARS:
        url = K.resolve_page(ch)
        pages[ch] = url
        print(ch, '->', url)
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=1)
    hit = sum(1 for v in pages.values() if v)
    print(f'{hit}/{len(pages)} resolved -> {OUT}')


if __name__ == '__main__':
    main()
