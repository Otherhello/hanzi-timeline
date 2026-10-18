#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《說文解字》抓取器 —— 从 zh.wikisource.org（维基文库）抓取全文，建立「字 → 說文释义 + 部首」离线索引。

用途（对应 data 管线的第一层，最权威、公有领域）：
    小篆时代的事实证据来自《說文解字》（东汉·许慎著，宋·徐铉校定本）。
    只要某字见于《說文解字》，即可确证其有「小篆」字形，并给出原文出处。

用法：
    python fetch_shuowen.py preview 10        # 打印第 10 卷（馬部所在）原始维基文本片段，观察结构
    python fetch_shuowen.py build             # 抓取 15 卷全文 -> 存 data/shuowen_raw.json 并建立索引
    python fetch_shuowen.py lookup 馬          # 查单个字的說文释义与部首
"""

import json
import os
import re
import sys
import time
import html
import urllib.request
import urllib.parse
import urllib.error

API = "https://zh.wikisource.org/w/api.php"
UA = {"User-Agent": "HanziTimeline/0.1 (student coursework; contact via project repo)"}
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "..", "data")
RAW_FILE = os.path.join(DATA_DIR, "shuowen_raw.json")
INDEX_FILE = os.path.join(DATA_DIR, "shuowen_index.json")


def api(params: dict, retries: int = 4) -> dict:
    """带重试与退避的 MediaWiki API 请求，应对 429 / 5xx 限流。"""
    params = dict(params)
    params["format"] = "json"
    params["formatversion"] = "2"
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                wait = 4 * (2 ** attempt)
                sys.stderr.write(f"  [HTTP {e.code}] retry in {wait}s...\n")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def fetch_wikitext(title: str) -> str:
    d = api({"action": "query", "prop": "revisions", "rvprop": "content",
             "rvslots": "main", "titles": title})
    page = d["query"]["pages"][0]
    if "missing" in page:
        return ""
    revs = page.get("revisions") or [{}]
    return revs[0].get("slots", {}).get("main", {}).get("content", "")


def strip_markup(text: str) -> str:
    # 去掉注释、noinclude、模板、链接、ref 等维基标记
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<noinclude>.*?</noinclude>", "", text, flags=re.S)
    text = re.sub(r"<ref[^>]*>.*?</ref>", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\{\{[^{}]*\}\}", "", text)          # 单层模板
    text = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", text)  # 链接取显示文本
    return text


def volume_titles():
    return [f"說文解字/{i:02d}" for i in range(1, 16)]


def build():
    os.makedirs(DATA_DIR, exist_ok=True)
    # 断点续抓：已有卷不再重复请求
    raw = {}
    if os.path.exists(RAW_FILE):
        try:
            raw = json.load(open(RAW_FILE, encoding="utf-8"))
        except Exception:
            raw = {}
    for t in volume_titles():
        if t in raw and raw[t]:
            sys.stderr.write(f"skip {t} (cached)\n")
            continue
        sys.stderr.write(f"fetch {t} ...")
        raw[t] = fetch_wikitext(t)
        sys.stderr.write(f" {len(raw[t])} chars\n")
        time.sleep(2.0)
        # 每卷落盘一次，续抓不丢
        with open(RAW_FILE, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=1)
    sys.stderr.write(f"raw saved -> {RAW_FILE}\n")

    index = build_index(raw)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    sys.stderr.write(f"index saved -> {INDEX_FILE} ({len(index)} chars indexed)\n")


# ── 說文 wikitext 解析器 ──────────────────────────────────────

def _hdr_bu(text: str) -> str:
    """从 ==X部== 标题提取部首名，如「馬部」；失败返回 None。"""
    m = re.search(r"(?:^|\n)\s*==\s*[\u4e00-\u9fffA-Za-z]+\s*==\s*(?:\n|$)", text)
    return m.group(0).strip("= \n") if m else None


def _parse_line_volume(wiki: str, vol_name: str) -> dict:
    """Vol 02-15 格式：每行一个說文字头，部首以 ==X部== 分隔。"""
    # 去掉 header2 模板（页面信息框）
    wiki = re.sub(r'\{\{header2.*?\n\}\}\n?', '', wiki, flags=re.S)
    index = {}
    current_bu = "?"
    # 行格式: 字（[[File:xxx|30px]]）：定義...
    # 或:     字：定義...
    entry_re = re.compile(
        r'^([\u4e00-\u9fff])'           # 字头 CJK 字符
        r'(?:\s*（\s*\[\[[^\]]*\]\]\s*）)?'  # 可选：篆书图片 [[File:xx-seal.svg|30px]]
        r'\s*[：:]\s*'                  # 冒号
        r'(.+?)$'                       # 定义（到行尾）
    , re.M)
    # 部标题
    bu_re = re.compile(r'^(==\s*)([\u4e00-\u9fff]+\s*部)(\s*==)', re.M)

    for line in wiki.split('\n'):
        # 部首标题
        bm = bu_re.search(line)
        if bm:
            current_bu = bm.group(2)
            continue
        # 說文条目
        em = entry_re.match(line.strip())
        if em:
            head = em.group(1)
            defin = html.unescape(em.group(2).strip().rstrip('。；，').strip())
            if head not in index:
                index[head] = {"def": defin, "bu": current_bu, "vol": vol_name}
    return index


def _parse_table_volume(wiki: str, vol_name: str) -> dict:
    """Vol 01 专用：說文条目在 wikitable 中，部首以 ==X部== 标题先行。"""
    wiki = re.sub(r'\{\{header2.*?\n\}\}\n?', '', wiki, flags=re.S)
    index = {}
    current_bu = "?"
    head_re = re.compile(r'\{\{\+\|' + "'''" + r'([\u4e00-\u9fff])' + "'''" + r'\}\}')
    defin_re = re.compile(r'\{\{yw\|(.+?)\}\}')

    # 用部标题切分（保留分隔符），使每段的字头归属正确的部首
    parts = re.split(r'(==[\u4e00-\u9fff]+\s*部==)', wiki)
    for part in parts:
        m = re.match(r'==([\u4e00-\u9fff]+\s*部)==', part.strip())
        if m:
            current_bu = m.group(1)
            continue
        for row in part.split('|-'):
            hm = head_re.search(row)
            if hm:
                head = hm.group(1)
                dm = defin_re.search(row)
                defin = html.unescape(dm.group(1).strip().rstrip('。；，')) if dm else ''
                if head not in index:
                    index[head] = {"def": defin, "bu": current_bu, "vol": vol_name}

    return index


def build_index(raw: dict) -> dict:
    """建立字 → {def, bu, vol} 索引，兼容卷 01（表格）与卷 02-15（行）两种格式。"""
    index = {}
    for t, wiki in raw.items():
        if not wiki:
            continue
        sys.stderr.write(f"parse {t} ...\n")
        if '{|' in wiki:  # 表格格式（卷 01）
            sub = _parse_table_volume(wiki, t)
        else:              # 行格式（卷 02-15）
            sub = _parse_line_volume(wiki, t)
        sys.stderr.write(f"  → {len(sub)} entries\n")
        index.update(sub)
    return index


def lookup(char: str):
    if not os.path.exists(INDEX_FILE):
        sys.stderr.write("索引不存在，请先运行：python fetch_shuowen.py build\n")
        return
    index = json.load(open(INDEX_FILE, encoding="utf-8"))
    rec = index.get(char)
    if not rec:
        print(f"「{char}」未见於《說文解字》索引。")
        return
    print(f"字：「{char}」 部首：{rec['bu']} 卷：{rec['vol']}")
    print(f"說文：{rec['def']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "lookup"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "preview":
        t = f"說文解字/{int(arg):02d}" if arg else "說文解字/10"
        wt = fetch_wikitext(t)
        print(strip_markup(wt)[:2000])
    elif cmd == "build":
        build()
    elif cmd == "lookup" and arg:
        lookup(arg)
    else:
        print(__doc__)
