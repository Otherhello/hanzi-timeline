# -*- coding: utf-8 -*-
"""
从「词典网」书法字典抓取楷书逐字字形图（带碑帖 / 书家出处）。

源：http://www.cidianwang.com/shufa/{pinyin}{id}.htm
图：https://c.cidianwang.com/file/shufa/kaishu|xiaokai/{calligrapher}/{file}.jpg
出处：img 的 alt（碑帖描述，如「张即之王友度墓志中馬的写法」）+ title（书家，如「张即之写的馬」）

用法：python fetch_kaishu_glyphs.py
产物：public/glyphs/{字}-kaishu-{n}.jpg  +  data/kaishu_glyphs.json
"""
import urllib.request, urllib.parse, urllib.error
import ssl, re, os, json, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_IMG = os.path.join(ROOT, "public", "glyphs")
OUT_JSON = os.path.join(ROOT, "data", "kaishu_glyphs.json")

BASE = "http://www.cidianwang.com"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

CHARS = [
    "馬", "牛", "山", "水", "日", "月", "人", "紙",
    "木", "土", "田", "雨", "魚", "鳥", "犬", "門",
    "貝", "玉", "文", "目", "耳", "口", "心", "大",
    "王", "車", "石", "羊",
]

FAMOUS = ["欧阳询", "颜真卿", "柳公权", "褚遂良", "赵孟頫", "虞世南", "薛稷",
          "王羲之", "王献之", "苏轼", "黄庭坚", "米芾", "文征明", "张即之",
          "于右任", "李邕", "钟繇", "邓石如", "赵之谦", "王宠", "欧阳通",
          "李世民", "武则天", "陆柬之", "智永", "怀素", "董其昌"]

# 楷书最具代表性的名家，择优时加权
TOP_TIER = {"欧阳询", "颜真卿", "柳公权", "褚遂良", "虞世南", "赵孟頫",
            "董其昌", "沈度", "文征明"}

# 该站这些来源的图片带「词典网」底部水印、且字形顶到边缘无法自动裁除，直接排除
EXCLUDE = {"麦华三", "王玄宗"}

WORK_HINTS = ("碑", "墓志", "墓誌", "铭", "銘", "帖", "表", "记", "記",
              "序", "赋", "賦", "卷", "册", "冊", "轴", "軸", "颂", "頌",
              "赞", "贊", "传", "傳", "诗", "詩", "经", "經", "箴", "文")

_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE


def fetch(url, referer=BASE + "/shufa/", timeout=30, retries=3):
    for i in range(retries):
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Referer": referer,
            "Accept-Language": "zh-CN,zh;q=0.9",
        })
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as r:
                return r.status, r.read()
        except Exception as e:
            if i == retries - 1:
                return None, str(e).encode()
            time.sleep(1.5 * (i + 1))
    return None, b""


def resolve_page(ch):
    """用「偏旁部首」页找到字页 URL：/shufa/bushou/{unicode}.htm 内含该字链接。"""
    cp = "U+{:04X}".format(ord(ch))
    url = f"{BASE}/shufa/bushou/{ord(ch):04x}.htm"
    st, body = fetch(url, referer=BASE + "/shufa/bushou/")
    if st != 200:
        return None
    html = body.decode("utf-8", "replace")
    m = re.search(r'href="([^"]*/shufa/[a-z]+[0-9]+\.htm)"[^>]*>\s*' + re.escape(ch), html)
    if m:
        u = m.group(1)
        return "https:" + u if u.startswith("//") else u
    return None


def parse_entries(html, ch):
    """抽出所有 img：data-src(图片) / alt(碑帖) / title(书家)。只保楷书与小楷。"""
    out = []
    for m in re.finditer(r"<img\b[^>]*>", html):
        tag = m.group(0)
        src = re.search(r'data-src="([^"]+)"', tag) or re.search(r'\bsrc="([^"]+\.(?:jpg|gif|png))"', tag)
        if not src:
            continue
        u = src.group(1)
        if "/file/shufa/kaishu/" not in u and "/file/shufa/xiaokai/" not in u:
            continue
        alt = re.search(r'alt="([^"]*)"', tag)
        title = re.search(r'title="([^"]*)"', tag)
        alt = alt.group(1) if alt else ""
        title = title.group(1) if title else ""
        if ch not in alt and ch not in title:
            continue
        info = parse_labels(alt, title, ch)
        out.append({
            "imageUrl": u,
            "alt": alt,
            "title": title,
            "calligrapher": info["calligrapher"],
            "work": info["work"],
            "script": "xiaokai" if "/xiaokai/" in u else "kaishu",
        })
    # 去重（同一图片可能重复出现）
    seen, uniq = set(), []
    for e in out:
        if e["imageUrl"] in seen:
            continue
        seen.add(e["imageUrl"])
        uniq.append(e)
    return uniq


def parse_labels(alt, title, ch):
    calligrapher = ""
    m = re.search(r"^(.+?)写的\s*" + re.escape(ch), title)
    if m:
        calligrapher = m.group(1).strip()
    # alt: 「张即之王友度墓志中馬的写法」/「赵孟頫写的馬」
    work = ""
    m = re.match(r"^(.*?)写的\s*" + re.escape(ch), alt)
    if m:
        return {"calligrapher": calligrapher or m.group(1).strip(), "work": ""}
    m = re.match(r"^(.*?)中" + re.escape(ch) + r"的写法", alt)
    if m:
        seg = m.group(1).strip()
    else:
        seg = alt.strip()
    if calligrapher and seg.startswith(calligrapher):
        seg = seg[len(calligrapher):].strip()
    # 去掉拓本前缀（宋拓 / 明拓）但保留原名
    work = seg
    return {"calligrapher": calligrapher, "work": work}


def score(entry):
    s = 0
    w = entry["work"]
    if any(h in w for h in WORK_HINTS):
        s += 100
    if entry["calligrapher"] in FAMOUS:
        s += 10
    if entry["calligrapher"] in TOP_TIER:
        s += 40
    if entry["script"] == "kaishu":
        s += 3
    return s


def pick(entries, n=3):
    """按分数选，且同一「书家+碑帖」只取一次，保证多样性。"""
    entries = sorted(entries, key=score, reverse=True)
    picked, seen = [], set()
    for e in entries:
        key = (e["calligrapher"], e["work"])
        if key in seen:
            continue
        seen.add(key)
        picked.append(e)
        if len(picked) >= n:
            break
    return picked


def download(url, dest):
    st, body = fetch(url, referer=BASE + "/shufa/")
    if st != 200 or len(body) < 400:
        return 0
    if body[:2] != b"\xff\xd8":  # 非 JPEG
        return 0
    with open(dest, "wb") as f:
        f.write(body)
    return len(body)


def _bottom_band(mask, w):
    """返回底部孤立窄带 (band_top, band_h, gap)；不存在则 None。"""
    rowcnt = mask.sum(axis=1)
    thr = max(1, int(0.004 * w))
    quiet = rowcnt <= thr
    nz = np.nonzero(~quiet)[0]
    if len(nz) == 0:
        return None
    r_end = int(nz[-1])
    r = r_end
    while r > 0 and not quiet[r]:
        r -= 1
    band_top = r + 1
    band_h = r_end - band_top + 1
    gap = 0
    rr = band_top - 1
    while rr >= 0 and quiet[rr]:
        gap += 1
        rr -= 1
    return band_top, band_h, gap


def strip_bottom_watermark(path, debug=False):
    """裁掉图片底部独立成一行的小字水印（如「词典网」）。

    同时处理两种极性：浅底深字（深色带）与深底浅字（浅色带，如拓片）。
    """
    global np
    try:
        from PIL import Image
        import numpy as np  # noqa: F811
    except Exception:
        return False
    im = Image.open(path)
    w, h = im.size
    a = np.asarray(im.convert("L"))
    for mask in (a < 100, a > 205):
        band = _bottom_band(mask, w)
        if not band:
            continue
        band_top, band_h, gap = band
        if band_h >= 4 and band_h <= 0.11 * h and gap >= 3 and gap >= 0.02 * h:
            margin = max(2, int(0.012 * h))
            new_h = max(1, band_top - margin)
            im.crop((0, 0, w, new_h)).save(path, quality=92)
            if debug:
                print(f"      (去水印 {band_h}px)")
            return True
    return False


def main():
    os.makedirs(OUT_IMG, exist_ok=True)
    result = {}
    for ch in CHARS:
        page = resolve_page(ch)
        print(f"[{ch}] page={page}")
        if not page:
            print("   无字页，跳过")
            continue
        st, body = fetch(page)
        if st != 200:
            print("   字页抓取失败", st)
            continue
        html = body.decode("utf-8", "replace")
        entries = parse_entries(html, ch)
        entries = [e for e in entries if e["calligrapher"] not in EXCLUDE]
        # 优先取有明确碑帖/作品名者（实物出处可核，且该站这类图多无底部水印）
        named = [e for e in entries if any(h in e["work"] for h in WORK_HINTS)]
        if len(named) >= 2:
            entries = named
        picked = pick(entries, 3)
        print(f"   楷书候选 {len(entries)} 条，选 {len(picked)}")
        saved = []
        for i, e in enumerate(picked, 1):
            fn = f"{ch}-kaishu-{i}.jpg"
            path = os.path.join(OUT_IMG, fn)
            if os.path.exists(path) and os.path.getsize(path) > 400:
                size = os.path.getsize(path)
            else:
                size = download(e["imageUrl"], path)
                time.sleep(0.4)
            if not size:
                print(f"   [{i}] 下载失败：{e['imageUrl']}")
                continue
            if strip_bottom_watermark(path, debug=True):
                size = os.path.getsize(path)
            src_rel = f"glyphs/{fn}"
            saved.append({
                "imageSrc": src_rel,
                "calligrapher": e["calligrapher"],
                "work": e["work"],
                "alt": e["alt"],
                "script": e["script"],
                "srcUrl": e["imageUrl"],
                "bytes": size,
            })
            print(f"   [{i}] {size:>7}B  {e['calligrapher']} / {e['work']}  -> {src_rel}")
        if saved:
            result[ch] = saved
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"\nDone: {sum(len(v) for v in result.values())} imgs, "
          f"{len(result)} chars -> {OUT_JSON}")


if __name__ == "__main__":
    main()
