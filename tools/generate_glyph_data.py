#!/usr/bin/env python3
"""从 說文解字 索引 + 人手审校的出处计划 → 生成前端 CharacterData TS 文件。

生成 src/data/characters.ts

铁律：
1. 每个字形挂实物出处 + 核对状态
2. 某期无实例 → 缺环（isGap=true），不虚列
3. 不用示意图/字体渲染冒充实物
"""

import json, os, html, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
INDEX_PATH = os.path.join(ROOT, 'data', 'shuowen_index.json')
OUT_PATH = os.path.join(ROOT, 'src', 'data', 'characters.ts')
GLYPHS_DIR = os.path.join(ROOT, 'public', 'glyphs')
HKU_PATH = os.path.join(ROOT, 'data', 'hku_glyphs.json')

# 漢語多功能字庫的時代鍵 → 本項目 EraId
HKU_ERA_MAP = {
    'jiaguwen': 'jiaguwen',
    'jinwen': 'jinwen',
    'zhanguo': 'zhanguo',
    'lishu': 'lishu',
    # zhuanwen（籀文）非本项目六期之一，且为康熙图转录，故不纳入。
}

HKU_SOURCE_REF = {
    'jiaguwen': '《甲骨文合集》（據香港中文大學《漢語多功能字庫》）',
    'jinwen': '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）',
    'zhanguo': '《殷周金文集成·戰國器》（據香港中文大學《漢語多功能字庫》）',
    'lishu': '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）',
}

ERA_ORDER = ['jiaguwen', 'jinwen', 'zhanguo', 'xiaozhuan', 'lishu', 'kaishu']

GAP_NOTES = {
    'jiaguwen': '此字後起，商代甲骨文中未见。',
    'jinwen': '西周至春秋金文中未见此字。',
    'zhanguo': '战国文字资料中暂未发现此字实例，属缺环。',
}

# ── 人手审校的出处计划 ──────────────────────────────────────────
# 按「正体字头」收录（說文字头，如 馬、紙）。
# 每时代取值：'gap' → 缺环；dict → 一条待核对实例。
# 小篆时代由說文索引自动填入（verification='verified'），此处可省略。

PROVENANCE = {
    '馬': {
        'jiaguwen': {'artifact': '殷墟甲骨（《甲骨文合集》所收，具体片号待核）', 'sourceRef': '《甲骨文合集》', 'dateRange': '商（殷墟）', 'note': '馬为象形字，甲骨习见；具体片号、藏地待人工核对后补实。'},
        'jinwen': {'artifact': '商周青铜器铭文（《殷周金文集成》所收，器名待核）', 'sourceRef': '《殷周金文集成》', 'dateRange': '西周—春秋', 'note': '金文习见；具体器名、著录号待核。'},
        'zhanguo': {'artifact': '战国简帛/玺印文字（《战国文字编》等所收，简号待核）', 'sourceRef': '《战国文字编》', 'dateRange': '战国', 'note': '简帛文字确有传承；具体简号待核。'},
        'lishu': {'artifact': '汉隶碑刻（如《曹全碑》《乙瑛碑》等，字例待核）', 'sourceRef': '汉碑拓本', 'dateRange': '东汉', 'note': '具体碑石字例待拓片核验。'},
        'kaishu': {'artifact': '唐楷碑帖（如《九成宫醴泉铭》《多宝塔碑》等，字例待核）', 'sourceRef': '唐碑拓本', 'dateRange': '唐及以后', 'note': '楷书定型字形；具体碑帖字例待核。'},
    },
    '牛': {
        'jiaguwen': {'artifact': '殷墟甲骨（《甲骨文合集》所收，片号待核）', 'sourceRef': '《甲骨文合集》', 'dateRange': '商（殷墟）', 'note': '牛为象形字，甲骨习见；具体片号待核。'},
        'jinwen': {'artifact': '商周青铜器铭文（含牛形族徽，器名待核）', 'sourceRef': '《殷周金文集成》', 'dateRange': '商晚期—西周', 'note': '具体器名待核。'},
        'lishu': {'artifact': '汉隶碑刻（字例待核）', 'sourceRef': '汉碑拓本', 'dateRange': '东汉', 'note': '具体碑石字例待核。'},
        'kaishu': {'artifact': '唐楷碑帖（字例待核）', 'sourceRef': '唐碑拓本', 'dateRange': '唐及以后', 'note': '具体碑帖字例待核。'},
    },
    '山': {
        'jiaguwen': {'artifact': '殷墟甲骨（《甲骨文合集》所收，片号待核）', 'sourceRef': '《甲骨文合集》', 'dateRange': '商（殷墟）', 'note': '山为象形字，甲骨习见；具体片号待核。'},
        'jinwen': {'artifact': '商周青铜器铭文（器名待核）', 'sourceRef': '《殷周金文集成》', 'dateRange': '商晚期—西周', 'note': '具体器名待核。'},
        'kaishu': {'artifact': '唐楷碑帖（字例待核）', 'sourceRef': '唐碑拓本', 'dateRange': '唐及以后', 'note': '具体碑帖字例待核。'},
    },
    '水': {
        'jiaguwen': {'artifact': '殷墟甲骨（《甲骨文合集》所收，片号待核）', 'sourceRef': '《甲骨文合集》', 'dateRange': '商（殷墟）', 'note': '水为象形字，甲骨习见；具体片号待核。'},
        'jinwen': {'artifact': '商周青铜器铭文（器名待核）', 'sourceRef': '《殷周金文集成》', 'dateRange': '商晚期—西周', 'note': '具体器名待核。'},
        'kaishu': {'artifact': '唐楷碑帖（字例待核）', 'sourceRef': '唐碑拓本', 'dateRange': '唐及以后', 'note': '具体碑帖字例待核。'},
    },
    '日': {
        'jiaguwen': {'artifact': '殷墟甲骨（《甲骨文合集》所收，片号待核）', 'sourceRef': '《甲骨文合集》', 'dateRange': '商（殷墟）', 'note': '日为象形字，甲骨习见；具体片号待核。'},
        'jinwen': {'artifact': '商周青铜器铭文（器名待核）', 'sourceRef': '《殷周金文集成》', 'dateRange': '商晚期—西周', 'note': '具体器名待核。'},
        'kaishu': {'artifact': '唐楷碑帖（字例待核）', 'sourceRef': '唐碑拓本', 'dateRange': '唐及以后', 'note': '具体碑帖字例待核。'},
    },
    '月': {
        'jiaguwen': {'artifact': '殷墟甲骨（《甲骨文合集》所收，片号待核）', 'sourceRef': '《甲骨文合集》', 'dateRange': '商（殷墟）', 'note': '月为象形字，甲骨习见；具体片号待核。'},
        'jinwen': {'artifact': '商周青铜器铭文（器名待核）', 'sourceRef': '《殷周金文集成》', 'dateRange': '商晚期—西周', 'note': '具体器名待核。'},
        'kaishu': {'artifact': '唐楷碑帖（字例待核）', 'sourceRef': '唐碑拓本', 'dateRange': '唐及以后', 'note': '具体碑帖字例待核。'},
    },
    '人': {
        'jiaguwen': {'artifact': '殷墟甲骨（《甲骨文合集》所收，片号待核）', 'sourceRef': '《甲骨文合集》', 'dateRange': '商（殷墟）', 'note': '人为象形字，甲骨习见；具体片号待核。'},
        'jinwen': {'artifact': '商周青铜器铭文（器名待核）', 'sourceRef': '《殷周金文集成》', 'dateRange': '商晚期—西周', 'note': '具体器名待核。'},
        'kaishu': {'artifact': '唐楷碑帖（字例待核）', 'sourceRef': '唐碑拓本', 'dateRange': '唐及以后', 'note': '具体碑帖字例待核。'},
    },
    '紙': {
        'jiaguwen': 'gap',
        'jinwen': 'gap',
        'zhanguo': 'gap',
        'lishu': {'artifact': '汉代简帛/碑刻（造纸术创于西汉，字例待核）', 'sourceRef': '汉简/汉碑', 'dateRange': '东汉', 'note': '纸为后起字，汉代是否已有隶定字形待核。'},
        'kaishu': {'artifact': '唐以降写本/碑帖（字例待核）', 'sourceRef': '唐碑拓本', 'dateRange': '唐及以后', 'note': '具体碑帖字例待核。'},
    },
}


def esc(s: str) -> str:
    """转义为 JS 单引号字符串字面量。"""
    return (s or '').replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')


def seal_image_for(char: str) -> str | None:
    """若 public/glyphs/ 存在 {char}-seal.svg，返回相对路径 'glyphs/…'（不加前导斜杠），否则 None。

    用相对路径（无前导斜杠）而非 '/glyphs/…'：站点部署在 GitHub Pages 项目子路径
    （如 /hanzi-timeline/）时，前导斜杠会解析到域名根而 404；相对路径相对当前文档解析，
    dev（/）与 Pages（/repo/）皆正确。
    """
    fname = f'{char}-seal.svg'
    if os.path.exists(os.path.join(GLYPHS_DIR, fname)):
        return f'glyphs/{fname}'
    return None


def parse_hku_tip(tip: str):
    """把『父辛尊[商代](CHANT:5749)』拆成 (artifact, period, catalog)。

    也兼容『甲骨文合集(CHANT:1630)』『馬王堆．五十二病方．104』等无方括号/无编号形式。
    """
    catalog = ''
    mcat = re.search(r'\((CHANT:\d+)\)', tip)
    if mcat:
        catalog = mcat.group(1).replace('CHANT:', '')
        tip = tip[:mcat.start()] + tip[mcat.end():]
    period = ''
    mper = re.search(r'\[([^\]]+)\]', tip)
    if mper:
        period = mper.group(1)
        tip = tip.replace(mper.group(0), '')
    return tip.strip(), period, catalog


def build_hku_instance(era: str, char: str, entry: dict, n: int) -> str:
    """由《漢語多功能字庫》一条字形记录生成 GlyphInstance 对象字面量（含真图 + 实物出处）。"""
    artifact, period, catalog = parse_hku_tip(entry.get('provenance', ''))
    parts = [
        f"id: '{esc(char)}-{era}-{n}'",
        f"era: '{era}'",
        f"artifact: '{esc(artifact)}'",
    ]
    if catalog:
        if era == 'jiaguwen':
            parts.append(f"catalogId: '{esc('CHANT:' + catalog)}'")
        elif era in ('jinwen', 'zhanguo'):
            parts.append(f"catalogId: '{esc('《殷周金文集成》' + catalog + '號')}'")
        else:
            parts.append(f"catalogId: '{esc('CHANT:' + catalog)}'")
    parts.append(f"sourceRef: '{esc(HKU_SOURCE_REF.get(era, '香港中文大學《漢語多功能字庫》'))}'")
    if period:
        parts.append(f"dateRange: '{esc(period)}'")
    parts.append("verification: 'verified'")
    parts.append("verifier: '香港中文大學《漢語多功能字庫》'")
    parts.append(f"imageSrc: '{esc(entry['imageSrc'])}'")
    return '{ ' + ', '.join(parts) + ' }'


def build_instance(era: str, char: str, prov: dict, shuowen: dict | None,
                   fallback_img: str | None = None) -> str:
    """生成一条 GlyphInstance 对象字面量。"""
    parts = [f"id: '{esc(char)}-{era}-1'"]

    if era == 'xiaozhuan' and shuowen:
        # 小篆：說文权威出处，已核对
        bu = shuowen.get('bu', '?')
        defin = html.unescape(shuowen.get('def', ''))
        vol = shuowen.get('vol', '')  # 如 '說文解字/10'
        vol_num = vol.split('/')[-1] if vol else ''
        parts.append(f"era: '{era}'")
        parts.append(f"artifact: '《說文解字》小篆字头'")
        parts.append(f"catalogId: '{esc('說文解字 第' + vol_num + '卷')}'")
        parts.append(f"collection: '（传世字书）'")
        parts.append(f"sourceRef: '{esc('《說文解字·' + bu + '》：「' + defin + '。」')}'")
        parts.append(f"dateRange: '东汉（许慎著）'")
        parts.append(f"verification: 'verified'")
        parts.append(f"verifier: '维基文库《說文解字》'")
        # 若已提供对应篆书图，则挂上 imageSrc（优先 Wikisource 矢量，其次字库康熙图）
        seal = seal_image_for(char)
        img = seal or fallback_img
        if img:
            parts.append(f"imageSrc: '{img}'")
            if not seal:
                parts.append("note: '小篆圖據《康熙字典》字形庫（說文小篆）'")
    else:
        parts.append(f"era: '{era}'")
        parts.append(f"artifact: '{esc(prov['artifact'])}'")
        if prov.get('sourceRef'):
            parts.append(f"sourceRef: '{esc(prov['sourceRef'])}'")
        if prov.get('dateRange'):
            parts.append(f"dateRange: '{esc(prov['dateRange'])}'")
        parts.append(f"verification: 'pending'")
        if prov.get('note'):
            parts.append(f"note: '{esc(prov['note'])}'")

    return '{ ' + ', '.join(parts) + ' }'


def build_era_entry(era: str, char: str, prov, shuowen: dict | None) -> str:
    """生成一条 EraEntry 对象字面量。"""
    if prov == 'gap':
        gn = GAP_NOTES.get(era, '该时代暂未发现此字实例，属缺环。')
        return f"{{ era: '{era}', instances: [], isGap: true, gapNote: '{esc(gn)}' }}"
    inst = build_instance(era, char, prov, shuowen if era == 'xiaozhuan' else None)
    return f"{{ era: '{era}', instances: [{inst}], isGap: false }}"


def generate() -> str:
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index = json.load(f)

    hku = {}
    if os.path.exists(HKU_PATH):
        with open(HKU_PATH, 'r', encoding='utf-8') as f:
            hku = json.load(f)

    out = []
    out.append('/**')
    out.append(' * 汉字字形演变证据链数据')
    out.append(' *')
    out.append(' * 由 tools/generate_glyph_data.py 生成。')
    out.append(' * 小篆：维基文库《說文解字》（已核对）。')
    out.append(' * 甲骨/金文/战国/隶：香港中文大学《漢語多功能字庫》字形（已核对，附器名/合集号）。')
    out.append(' * 其余时代著录出处已标明，核对状态为「待核对」。')
    out.append(' *')
    out.append(' * 铁律：每字形挂实物出处 + 核对状态；无实例即缺环；不用示意图冒充实物。')
    out.append(' */')
    out.append('')
    out.append("import type { CharacterData } from '../types'")
    out.append('')
    out.append('const CHARACTERS: CharacterData[] = [')
    out.append('')

    for char, prov in PROVENANCE.items():
        shuowen = index.get(char)
        char_hku = hku.get(char, {})
        entries = []
        for era in ERA_ORDER:
            eprov = prov.get(era)
            hku_entries = char_hku.get(HKU_ERA_MAP.get(era, ''), []) if era in HKU_ERA_MAP else []
            if era == 'xiaozhuan' and shuowen:
                # 說文数据存在 → 强制生成 verified 小篆条目（覆盖 provenance 空缺）
                xz_hku = char_hku.get('xiaozhuan', [])
                fb = xz_hku[0]['imageSrc'] if xz_hku else None
                inst = build_instance('xiaozhuan', char, {}, shuowen, fb)
                entries.append(f"{{ era: 'xiaozhuan', instances: [{inst}], isGap: false }}")
            elif hku_entries:
                # 有《漢語多功能字庫》真图与出处 → 一或多件实例（已核对）
                insts = [build_hku_instance(era, char, e, i + 1) for i, e in enumerate(hku_entries)]
                entries.append(f"{{ era: '{era}', instances: [{', '.join(insts)}], isGap: false }}")
            elif eprov is None or eprov == 'gap':
                entries.append(build_era_entry(era, char, 'gap', None))
            else:
                entries.append(build_era_entry(era, char, eprov, None))
        out.append(f'  {{ char: \'{esc(char)}\', eras: [')
        out.append('    ' + ',\n    '.join(entries))
        out.append('  ] },')
        out.append('')

    out.append(']')
    out.append('')
    out.append('export default CHARACTERS')
    out.append('')
    return '\n'.join(out)


if __name__ == '__main__':
    content = generate()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated: {OUT_PATH}")
    print(f"Chars: {len(PROVENANCE)}")
