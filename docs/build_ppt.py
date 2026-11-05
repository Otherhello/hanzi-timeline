# -*- coding: utf-8 -*-
"""生成课堂汇报用 PPT（13-14 分钟版）。

产物：docs/汉字字形演变证据链-汇报提纲.pptx
每页都带演讲备注（含分钟标记与讲法），便于控时。
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "汉字字形演变证据链-汇报提纲.pptx")

# ── 主题色（与网站一致） ────────────────────────────────
INK      = RGBColor(0x23, 0x20, 0x1A)
INK_SOFT = RGBColor(0x4A, 0x44, 0x38)
MUTED    = RGBColor(0x7A, 0x73, 0x62)
PAPER    = RGBColor(0xF6, 0xF1, 0xE6)
PAPER_2  = RGBColor(0xFB, 0xF7, 0xEE)
SEAL     = RGBColor(0xA6, 0x3A, 0x2B)
BRONZE   = RGBColor(0xA3, 0x87, 0x4F)
LINE     = RGBColor(0xD9, 0xD0, 0xBC)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
DARK_HDR = RGBColor(0x3A, 0x35, 0x2C)

SANS = "微软雅黑"
SERIF = "楷体"

W, H = 13.333, 7.5
MARGIN = 0.78

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]


def set_ea(run, face):
    """同时设置拉丁与东亚字体，否则中文会回落到默认字体。"""
    run.font.name = face
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", face)


def textbox(slide, l, t, w, h, *, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tf


def para(tf, text, *, size=16, bold=False, color=INK, face=SANS,
         space_before=0, space_after=6, line=1.32, align=PP_ALIGN.LEFT,
         first=False, indent=0.0):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = line
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    set_ea(r, face)
    return p


def rule(slide, l, t, w, color=LINE, thick=0.012):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(l), Inches(t),
                                Inches(w), Inches(thick))
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def new_slide(bg=PAPER):
    s = prs.slides.add_slide(BLANK)
    bgr = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bgr.fill.solid()
    bgr.fill.fore_color.rgb = bg
    bgr.line.fill.background()
    bgr.shadow.inherit = False
    # 顶部细线
    rule(s, 0, 0, W, BRONZE, 0.055)
    # 页脚
    tf = textbox(s, W - 1.55, H - 0.52, 1.0, 0.3)
    para(tf, "", size=9, color=MUTED, align=PP_ALIGN.RIGHT, first=True)
    return s


def page_no(slide, n, total):
    tf = textbox(slide, W - 1.75, H - 0.55, 1.1, 0.3)
    para(tf, f"{n} / {total}", size=9.5, color=MUTED, align=PP_ALIGN.RIGHT, first=True)


def head(slide, eyebrow, title, subtitle=None):
    if eyebrow:
        tf = textbox(slide, MARGIN, 0.52, W - 2 * MARGIN, 0.3)
        para(tf, eyebrow, size=11.5, bold=True, color=BRONZE, first=True)
    tf = textbox(slide, MARGIN, 0.86, W - 2 * MARGIN, 0.75)
    para(tf, title, size=27, bold=True, color=INK, face=SERIF, first=True, line=1.15)
    rule(slide, MARGIN, 1.62, 0.95, SEAL, 0.035)
    y = 1.80
    if subtitle:
        tf = textbox(slide, MARGIN, y, W - 2 * MARGIN, 0.4)
        para(tf, subtitle, size=13, color=INK_SOFT, first=True)
        y += 0.46
    return y


def bullets(slide, l, t, w, items, *, size=15.5, gap=8, color=INK_SOFT,
            bullet_color=BRONZE, line=1.38):
    tf = textbox(slide, l, t, w, H - t - 0.7)
    for i, it in enumerate(items):
        p = para(tf, "", size=size, space_after=gap, line=line, first=(i == 0))
        r = p.add_run()
        r.text = "— "
        r.font.size = Pt(size)
        r.font.color.rgb = bullet_color
        set_ea(r, SANS)
        # 支持 (**粗体引导**，正文) 的两段式
        if isinstance(it, tuple):
            lead, rest = it
            r1 = p.add_run()
            r1.text = lead
            r1.font.size = Pt(size)
            r1.font.bold = True
            r1.font.color.rgb = color
            set_ea(r1, SANS)
            r2 = p.add_run()
            r2.text = rest
            r2.font.size = Pt(size)
            r2.font.color.rgb = color
            set_ea(r2, SANS)
        else:
            r2 = p.add_run()
            r2.text = it
            r2.font.size = Pt(size)
            r2.font.color.rgb = color
            set_ea(r2, SANS)
    return tf


def table(slide, l, t, w, col_widths, rows, *, header=True,
          fs=12, hdr_fs=12.5, row_h=0.42, hdr_h=0.46):
    n_rows, n_cols = len(rows), len(col_widths)
    shape = slide.shapes.add_table(n_rows, n_cols, Inches(l), Inches(t),
                                   Inches(w), Inches(hdr_h + row_h * (n_rows - 1)))
    tbl = shape.table
    tbl.first_row = False
    tbl.horz_banding = False
    for i, cw in enumerate(col_widths):
        tbl.columns[i].width = Inches(cw)
    for ri, row in enumerate(rows):
        tbl.rows[ri].height = Inches(hdr_h if (header and ri == 0) else row_h)
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            cell.margin_left = Inches(0.10)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.05)
            cell.margin_bottom = Inches(0.05)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            is_hdr = header and ri == 0
            cell.fill.fore_color.rgb = DARK_HDR if is_hdr else (
                PAPER_2 if ri % 2 == 1 else WHITE)
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = 0
            tf.margin_right = 0
            tf.margin_top = 0
            tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.line_spacing = 1.18
            p.alignment = PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(val)
            r.font.size = Pt(hdr_fs if is_hdr else fs)
            r.font.bold = is_hdr
            r.font.color.rgb = WHITE if is_hdr else INK_SOFT
            set_ea(r, SANS)
    return tbl


def cards(slide, l, t, w, items, *, h=1.32, gap=0.18, fs=11.5, title_fs=12.5):
    """一排卡片：items = [(序号/标签, 标题, 说明)]"""
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    for i, (tag, title, desc) in enumerate(items):
        x = l + i * (cw + gap)
        sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(t),
                                    Inches(cw), Inches(h))
        sh.fill.solid()
        sh.fill.fore_color.rgb = WHITE
        sh.line.color.rgb = LINE
        sh.line.width = Pt(0.75)
        sh.shadow.inherit = False
        sh.adjustments[0] = 0.06
        tf = sh.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.12)
        tf.margin_right = Inches(0.10)
        tf.margin_top = Inches(0.10)
        tf.margin_bottom = Inches(0.08)
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.line_spacing = 1.1
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = tag
        r.font.size = Pt(title_fs - 1.5)
        r.font.bold = True
        r.font.color.rgb = SEAL
        set_ea(r, SANS)
        p2 = tf.add_paragraph()
        p2.line_spacing = 1.12
        p2.space_before = Pt(2)
        p2.alignment = PP_ALIGN.LEFT
        r2 = p2.add_run()
        r2.text = title
        r2.font.size = Pt(title_fs)
        r2.font.bold = True
        r2.font.color.rgb = INK
        set_ea(r2, SANS)
        if desc:
            p3 = tf.add_paragraph()
            p3.line_spacing = 1.16
            p3.space_before = Pt(3)
            p3.alignment = PP_ALIGN.LEFT
            r3 = p3.add_run()
            r3.text = desc
            r3.font.size = Pt(fs)
            r3.font.color.rgb = MUTED
            set_ea(r3, SANS)


def callout(slide, l, t, w, text, *, h=0.62, fs=13, color=SEAL, bg=PAPER_2,
            align=PP_ALIGN.CENTER):
    sh = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t),
                                Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = bg
    sh.line.color.rgb = LINE
    sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    sh.adjustments[0] = 0.12
    tf = sh.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.06)
    tf.margin_bottom = Inches(0.06)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.line_spacing = 1.22
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(fs)
    r.font.color.rgb = color
    set_ea(r, SANS)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


TOTAL = 19

# ══════════════════════════════════════════════════════════
# 1 封面
# ══════════════════════════════════════════════════════════
s = new_slide()
s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0),
                   Inches(W), Inches(H)).fill.background()

# 竖排印章式装饰
seal = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(W - 2.55), Inches(0.95),
                          Inches(1.05), Inches(1.05))
seal.fill.background()
seal.line.color.rgb = SEAL
seal.line.width = Pt(2.2)
seal.shadow.inherit = False
tf = seal.text_frame
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.CENTER
r = p.add_run()
r.text = "證"
r.font.size = Pt(40)
r.font.bold = True
r.font.color.rgb = SEAL
set_ea(r, SERIF)

tf = textbox(s, 1.15, 2.05, 9.0, 2.4)
para(tf, "汉字字形演变", size=54, bold=True, color=INK, face=SERIF, first=True,
     line=1.06, space_after=0)
para(tf, "证据链时间轴", size=54, bold=True, color=INK, face=SERIF, line=1.06,
     space_after=14)
para(tf, "输入一个字，把它的六个时代的样子与出处，逐条摊开。", size=17,
     color=INK_SOFT, line=1.4)

rule(s, 1.15, 5.28, 5.4, BRONZE, 0.028)

tf = textbox(s, 1.15, 5.52, 10.5, 1.0)
para(tf, "线上作品  https://otherhello.github.io/hanzi-timeline/", size=14,
     color=INK_SOFT, first=True, space_after=4)
para(tf, "课程汇报 · 14 分钟 · 28 个字 / 246 条实例 / 245 张实物图", size=13, color=MUTED)
notes(s, "【0:00–0:15｜封面】\n"
         "各位老师、同学好。我们做的是一个很小的东西：输入一个字，看它在六个时代里分别长什么样，\n"
         "并且——每一个样子都能指回一件实物。网址在下面，现在就可以打开。\n"
         "接下来 14 分钟，我会讲清楚：为什么做、数据从哪来、怎么用 AI 把它做出来、然后现场演示。")

# ══════════════════════════════════════════════════════════
# 2 议程与时间分配
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 2, TOTAL)
y = head(s, "AGENDA", "今天讲六件事，时间已排好",
         "每页备注里都写了这一页该讲多久，全部加起来 13 分 40 秒。")

rows = [
    ["#", "段落", "要回答的问题", "时长"],
    ["1", "选题背景与任务目标", "为什么做、做什么", "1:20"],
    ["2", "AI Coding 技术点", "我们用的是哪一种 AI 编程方式", "3:00"],
    ["3", "数据来源与规模", "真实来源、多少条、怎么核对", "1:50"],
    ["4", "方案设计与技术路线", "架构、如何用 AI、Vibe Coding 过程", "4:40"],
    ["5", "现场作品演示", "真实数据现场操作", "2:10"],
    ["6", "分工说明 + Prompt Log", "谁做了什么、怎么提问与核验", "1:00"],
]
table(s, MARGIN, y + 0.05, W - 2 * MARGIN, [0.6, 3.05, 5.4, 1.0], rows,
      fs=13, hdr_fs=13, row_h=0.55, hdr_h=0.46)
callout(s, MARGIN, y + 0.05 + 0.46 + 0.55 * 6 + 0.16, W - 2 * MARGIN,
        "合计约 13:40 —— 演示放在第 11 分钟，因为它最值得看；如果前面超时，第 18 页的 Prompt Log 全表可以跳过。",
        h=0.62, fs=13, color=INK_SOFT)
notes(s, "【0:15–0:25｜议程】\n"
         "六件事。重点在第三、第四和第五节。\n"
         "如果时间紧，我会把第 18 页的 Prompt Log 全表略过，正文第 15 页已经给了五条最关键的。")

# ══════════════════════════════════════════════════════════
# 3 选题背景
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 3, TOTAL)
y = head(s, "01  选题背景", "我们想回答一个很具体的问题")
bullets(s, MARGIN, y + 0.10, W - 2 * MARGIN - 0.2, [
    ("字形更替是常识，", "可「这个写法出自哪件实物」很少被认真回答。"),
    ("现成的「字形演变图」很好看，", "但多数是后人摹写、重绘或字体渲染，指向不了任何一件原件。"),
    ("于是「演变」变成了看图说话，", "而不是可核对的证据。"),
    ("我们想做的，", "是把「看图」换成「查证据链」——宁可留白，也不给一条假证据。"),
], size=16.5, gap=14)
callout(s, MARGIN, H - 2.05, W - 2 * MARGIN,
        "一句话：这不是一张好看的演变图，而是一条能被逐条追溯、并且敢于留白的证据链。",
        h=0.72, fs=15, color=SEAL)
notes(s, "【0:25–1:05｜背景】\n"
         "先说我自己的困惑。我们查一个字，很容易看到「演变图」：甲骨、金文、小篆、隶、楷排一排。\n"
         "但那些图大多没有出处——是摹本、是重绘、是拿字体渲染出来的。\n"
         "它看起来像证据，其实只是一张插图。所以我们把问题换成：每一个字形，能不能指回一件实物。\n"
         "这句话就是整个项目的起点，也是后面所有取舍的标准。")

# ══════════════════════════════════════════════════════════
# 4 目标与三条铁律
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 4, TOTAL)
y = head(s, "01  任务目标", "输入一个字，给出一条证据链")

tf = textbox(s, MARGIN, y + 0.05, 5.35, 0.34)
para(tf, "任务目标", size=13, bold=True, color=BRONZE, first=True)
bullets(s, MARGIN, y + 0.42, 5.35, [
    "按 甲骨文 → 金文 → 战国 → 小篆 → 隶 → 楷 六期纵向展示",
    ("每字形挂实物出处：", "哪片甲骨、哪件青铜器、哪块碑、哪件写本"),
    "每字形挂核对状态：已核对 / 待核对",
    ("某期无实例 → 显式「缺环」：", "空白 + 一句说明"),
], size=14.5, gap=10)

tf = textbox(s, 6.62, y + 0.05, 5.9, 0.34)
para(tf, "三条铁律（从第一行代码起就守）", size=13, bold=True, color=SEAL, first=True)
rules_rows = [
    ["铁律", "系统里怎么落实"],
    ["① 每个字形必须挂实物出处",
     "每条实例都带 artifact（器名/篇名）、catalogId（合集/集成号）、sourceRef、sourceUrl"],
    ["② 无实例就是缺环，绝不倒填",
     "数据里有 isGap + gapNote；生成器遇源缺失自动产缺环，不抛错、不静默补图"],
    ["③ 不用示意图冒充实物",
     "所有图都来自馆藏扫描、拓本或传世字书；未接入时显示「实物拓图待接入」空帧"],
]
table(s, 6.62, y + 0.44, 5.9, [1.95, 3.95], rules_rows, fs=11, hdr_fs=11.5,
      row_h=1.02, hdr_h=0.38)
notes(s, "【1:05–1:50｜目标与铁律】\n"
         "目标是三句话：六个时代、每个字形挂出处、没有就说没有。\n"
         "右边这三条不是口号，第一条对应数据结构里的四个字段，第二条对应 isGap 这个布尔量，\n"
         "第三条对应我们的取图规则——没有图就显示空帧，而不是画一个。\n"
         "答辩时最容易被问的就是第三条：你们怎么保证图不是画的。答案是：所有图都有来源页，点得开。")

# ══════════════════════════════════════════════════════════
# 5 AI Coding 技术点 ①
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 5, TOTAL)
y = head(s, "02  AI CODING 技术点", "我们用的是「AI 编码代理」，不是「AI 生成器」")
bullets(s, MARGIN, y + 0.10, W - 2 * MARGIN - 0.2, [
    ("普通用法：", "把需求丢给 AI，让它一次生成一大段代码，然后自己粘贴、自己调。"),
    ("代理用法：", "AI 能读仓库、跑命令、看报错、自己改，一轮一轮往前推。"),
    ("关键差别不在模型多强，", "而在上下文怎么给——给文件、给报错原文、给验收标准。"),
    ("所以真正的技术点不是「会写提示词」，", "而是「会把一件事切成一次能跑通的一小步」。"),
], size=16, gap=14)
callout(s, MARGIN, H - 2.30, W - 2 * MARGIN,
        "AI 不是替你写完，而是替你加速「一次能跑通的迭代」。", h=0.66, fs=15, color=SEAL)
callout(s, MARGIN, H - 1.50, W - 2 * MARGIN,
        "接下来三页：我们总结的五步闭环、每步的交付物、以及为什么「一次只做一个完整功能」成功率更高。",
        h=0.62, fs=12.5, color=INK_SOFT)
notes(s, "【1:50–2:40｜技术点 1/3】\n"
         "老师要求讲一个通用的 AI Coding 技术点。我们选的是「AI 编码代理的增量开发」。\n"
         "区别很朴素：以前你把需求丢给 AI，它吐一大段；现在是它能自己读文件、跑命令、看报错。\n"
         "但真正决定成败的不是模型，是你给它的上下文——这一点后面 Prompt Log 会用实例证明。")

# ══════════════════════════════════════════════════════════
# 6 五步闭环
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 6, TOTAL)
y = head(s, "02  AI CODING 技术点", "五步闭环：我们全程按这个节奏提问")
cards(s, MARGIN, y + 0.12, W - 2 * MARGIN, [
    ("①", "意图描述", "做什么、长什么样、\n怎么交互"),
    ("②", "方案生成", "让 AI 给方案，\n人工审查选型"),
    ("③", "增量实现", "一次只做一个完整\n功能，跑通再叠加"),
    ("④", "调试改进", "把报错原文\n原样丢回去"),
    ("⑤", "审美与验证", "人工检查完整性、\n准确性、可信度"),
], h=1.55, gap=0.16, fs=11.5, title_fs=12.5)
bullets(s, MARGIN, y + 1.95, W - 2 * MARGIN, [
    ("每步都有明确的「交付物检查点」，", "不通过不进入下一步：②要能说清选型理由，③要能 tsc + build 通过，⑤要能线上点开验证。"),
    ("第④步最关键：", "报错原文比任何转述都值钱——「图片 200 但 0 字节」这种细节，转述一次就丢了。"),
], size=14.5, gap=10)
notes(s, "【2:40–3:35｜技术点 2/3】\n"
         "五步：意图、方案、增量、调试、验证。这是我们问 AI 的固定格式。\n"
         "重点讲第④步：报错一定贴原文。比如「HTTP 200 但返回 0 字节」，\n"
         "如果我说成「图片加载失败」，AI 会去查路径；贴原文它才会想到 Referer。\n"
         "这个差别，在我们项目里直接决定了港中大的图能不能取到。")

# ══════════════════════════════════════════════════════════
# 7 为什么增量
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 7, TOTAL)
y = head(s, "02  AI CODING 技术点", "为什么「一次只做一个完整功能」成功率更高")

tf = textbox(s, MARGIN, y + 0.06, 5.55, 0.34)
para(tf, "反例（我们试过）", size=13, bold=True, color=SEAL, first=True)
bullets(s, MARGIN, y + 0.44, 5.55, [
    "「做一个汉字演变网站」——AI 给出看似完整、实际跑不起来的骨架",
    "页面、数据、抓取混在一轮里，报错时无法判断哪一层坏了",
    "越改越乱，最后只能推倒重来",
], size=13.5, gap=9)

rule(s, 6.38, y + 0.10, 0.014, LINE, 3.55)

tf = textbox(s, 6.62, y + 0.06, 5.95, 0.34)
para(tf, "我们的做法（实际迭代顺序）", size=13, bold=True, color=BRONZE, first=True)
seq = [
    ["轮次", "这一轮只做一件事", "验收"],
    ["1", "输入一字 → 六期卡片渲染（假数据也行）", "页面能跑"],
    ["2", "只接小篆一个源（《說文》）", "8 字有图有义"],
    ["3", "再加甲骨/金文/战国/隶（港中大）", "缺环自动出现"],
    ["4", "补楷书（词典网碑帖）", "六期全有图"],
    ["5", "扩字到 28，补战国秦系", "缺环 13→5"],
]
table(s, 6.62, y + 0.44, 5.95, [0.62, 3.55, 1.78], seq, fs=10.5, hdr_fs=11,
      row_h=0.52, hdr_h=0.34)
callout(s, MARGIN, H - 1.32, W - 2 * MARGIN,
        "增量不是慢，是让错误可定位：每一轮最多只可能错一处，而这一处的报错原文就是下一步的输入。",
        h=0.62, fs=13.5, color=INK_SOFT)
notes(s, "【3:35–4:20｜技术点 3/3】\n"
         "这一页是我们的血泪。第一轮我们真的说过「做一个汉字演变网站」，结果它给了一个漂亮的空壳。\n"
         "后来改成五轮：先假数据跑通页面，再接一个源，再加四期，再补楷书，最后扩到 28 个字。\n"
         "右边这张表就是真实的迭代顺序，每一轮都有验收标准。\n"
         "这就是「一次只做一个完整功能」——完整指的是这一层能跑通，不是功能全。")

# ══════════════════════════════════════════════════════════
# 8 数据源
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 8, TOTAL)
y = head(s, "03  数据来源", "四个公开库，各管一段时代",
         "不是随便找图：每个时代都对应一个有编号体系、可回溯的库。")
rows = [
    ["数据源", "覆盖时代", "怎么取", "必须知道的坑"],
    ["维基文库《說文解字》", "小篆", "MediaWiki API 抓 15 卷，解析部首与释义",
     "小篆字头有矢量图，但并非每字都有"],
    ["港中大《漢語多功能字庫》", "甲骨 / 金文 /\n战国 / 隶", "逐字开字页，解析分时代字形表",
     "图片端点强制同站 Referer，\n否则 200 但 0 字节"],
    ["词典网 · 书法字典", "楷书（历代碑帖）", "逐字开字页，取书家 + 碑帖 + 图",
     "全站 https 证书过期，只能走 http"],
    ["维基共享资源", "小篆矢量图、纸背名帖", "Commons API 检索 + 缩略图",
     "原文件请求 429 限流，须用缩略图"],
]
table(s, MARGIN, y + 0.10, W - 2 * MARGIN, [2.65, 1.72, 3.55, 3.55], rows,
      fs=11.5, hdr_fs=12, row_h=0.70, hdr_h=0.42)
callout(s, MARGIN, H - 1.42, W - 2 * MARGIN,
        "四源合起来覆盖六期：小篆有传世字书，甲骨/金文/战国/隶有学术字库，楷书落到具体碑帖。",
        h=0.60, fs=13, color=INK_SOFT)
notes(s, "【4:20–5:20｜数据源】\n"
         "四个库，每个管一段。\n"
         "《說文解字》管小篆，它有 9335 个字头，我们抓到 7338 个可解析的。\n"
         "港中大那个字库最强：一个字进去，甲骨、金文、小篆、简帛分栏列出来，旁边就是器名和集成号。\n"
         "楷书没有这样的库，只能落到词典网的碑帖图。\n"
         "最右边这一列是我们踩的坑——待会儿第 11 页会说这些坑怎么解决的。")

# ══════════════════════════════════════════════════════════
# 9 规模与核对状态
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 9, TOTAL)
y = head(s, "03  规模与核对状态", "28 个字 / 246 条实例 / 245 张实物图")

tf = textbox(s, MARGIN, y + 0.04, 5.55, 0.32)
para(tf, "六期实例数", size=12.5, bold=True, color=BRONZE, first=True)
eras = [("甲骨文", 27, 0.36), ("金文", 63, 0.84), ("战国", 25, 0.33)]
eras2 = [("小篆", 28, 0.37), ("隶书", 28, 0.37), ("楷书", 75, 1.0)]
yy = y + 0.42
for name, val, ratio in eras + eras2:
    tf = textbox(s, MARGIN, yy, 0.85, 0.3)
    para(tf, name, size=12, color=INK_SOFT, first=True)
    bar_w = 2.9 * ratio
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(MARGIN + 0.92), Inches(yy + 0.05),
                            Inches(max(0.1, bar_w)), Inches(0.20))
    sh.fill.solid()
    sh.fill.fore_color.rgb = BRONZE if val < 60 else SEAL
    sh.line.fill.background()
    sh.shadow.inherit = False
    tf = textbox(s, MARGIN + 0.92 + bar_w + 0.12, yy - 0.01, 0.7, 0.3)
    para(tf, str(val), size=11.5, bold=True, color=INK, first=True)
    yy += 0.36

tf = textbox(s, 6.55, y + 0.04, 5.95, 0.32)
para(tf, "三态与真实含义", size=12.5, bold=True, color=SEAL, first=True)
st = [
    ["状态", "含义", "数量"],
    ["已核对", "图与出处取自权威库，来源页可点开、可机器复核\n（= 库内可溯，不等于逐件人工核验原拓）", "245"],
    ["待核对", "有出处但暂无图（紙·楷书，该库无此字页）", "1"],
    ["缺环", "该时代确无可信实例，写明原因", "5"],
]
table(s, 6.55, y + 0.42, 5.95, [0.95, 4.15, 0.85], st, fs=10.5, hdr_fs=11,
      row_h=0.86, hdr_h=0.34)
callout(s, MARGIN, H - 1.62, W - 2 * MARGIN,
        "「缺环」里 紙 的甲骨/金文/战国三格，是汉代后起字本无此形——这不是资料不足，恰恰证明我们没有倒填。",
        h=0.66, fs=13, color=SEAL)
notes(s, "【5:20–6:05｜规模与状态】\n"
         "28 个字，246 条实例，245 张图。左边是六期分布：金文最多，因为一件青铜器就能贡献一条；楷书 75 条。\n"
         "右边这个表要讲清楚：已核对 245 条，它的意思是「库内可溯」——图和出处都在权威库里，来源页点得开。\n"
         "它不等于我逐件核对了原拓，这一点我不敢夸大。\n"
         "缺环 5 条，其中紙的三格是「本无此形」，不是「没查到」——这个区别就是我们诚实的地方。")

# ══════════════════════════════════════════════════════════
# 10 架构
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 10, TOTAL)
y = head(s, "04  方案设计", "六段流水线：任何一段都能单独重跑")
cards(s, MARGIN, y + 0.14, W - 2 * MARGIN, [
    ("01", "源", "三个公开字库\n+ 名帖图库"),
    ("02", "抓取", "三个 Python 脚本\n限速、退避、续抓"),
    ("03", "缓存", "原文/清单/图片\n全部落盘"),
    ("04", "生成", "按字按时代汇编\n自动补缺环"),
    ("05", "前端", "React 静态站\n六期纵向渲染"),
    ("06", "部署", "push → Actions\n→ Pages"),
], h=1.42, gap=0.14, fs=10.5, title_fs=12)
callout(s, MARGIN, y + 1.78, W - 2 * MARGIN,
        "设计要点：抓取与生成彻底分离 —— 抓取只负责「如实搬下来」，不判断真假；生成只负责「按规则组装」，不联网。",
        h=0.62, fs=13.5, color=INK_SOFT)
bullets(s, MARGIN, y + 2.58, W - 2 * MARGIN, [
    ("好处：", "换源只改抓取层，改版式只改前端，加字只改字表——三者互不牵连。"),
    ("所以它能长期跑：", "任何一个源挂了，只会多出几条缺环，站点不会崩。"),
], size=14.5, gap=9)
notes(s, "【6:05–7:00｜架构】\n"
         "这是整条链路：源、抓取、缓存、生成、前端、部署。\n"
         "最关键的一句在最下面：抓取和生成是分离的。抓取脚本不知道什么叫「缺环」，它只负责搬；\n"
         "生成脚本不联网，它只按规则组装。这样换源、加字、改版式三个动作互不影响。\n"
         "这也是为什么第 5 轮扩到 28 个字时，我们只改了字表，一行代码没动。")

# ══════════════════════════════════════════════════════════
# 11 采集层
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 11, TOTAL)
y = head(s, "04  采集层", "三个抓取器，各自踩过的坑")
rows = [
    ["脚本", "负责", "踩过的坑（都已修复）"],
    ["fetch_shuowen.py", "抓《說文》15 卷，\n解析 7338 字索引",
     "HTTP 429 限流 → 退避 + 断点续抓；全角括号导致带字头图的条目全漏；卷 01 是表格格式、部首归属错位"],
    ["fetch_hku_glyphs.py", "逐字抓四期字形，\n下载并校验文件头",
     "图片端点强制同站 Referer；睡虎地简要区分「战国秦系」与「汉隶」，否则两期重复同一件简"],
    ["fetch_kaishu_glyphs.py", "逐字抓词典网楷书，\n按书家+碑帖去重",
     "https 证书过期；白底图带站方水印，需按行剖面裁掉；字形顶到水印的来源直接排除"],
]
table(s, MARGIN, y + 0.10, W - 2 * MARGIN, [2.35, 2.55, 6.55], rows,
      fs=11, hdr_fs=11.5, row_h=1.02, hdr_h=0.42)
callout(s, MARGIN, H - 1.62, W - 2 * MARGIN,
        "这些细节才是「能不能长期跑」的分界线：限流、编码、Referer、水印——每一个都能让流水线在半夜静默失败。",
        h=0.66, fs=13, color=INK_SOFT)
notes(s, "【7:00–7:55｜采集层】\n"
         "三个脚本的坑，我挑三个讲。\n"
         "第一个：抓《說文》时前 10 卷顺利，第 11 卷 429。解决办法不是手动重跑，是退避加断点续抓——\n"
         "现在断网也不会丢已抓的卷。\n"
         "第二个：港中大返回 200 但是 0 字节。查了半天是 Referer，它只允许同站引用图片。\n"
         "第三个：词典网 https 证书过期，浏览器能点进去但脚本不行，只能走 http。\n"
         "这三个如果不知道，流水线就会在半夜静默失败，第二天打开网站发现图全没了。")

# ══════════════════════════════════════════════════════════
# 12 生成层
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 12, TOTAL)
y = head(s, "04  生成层", "一条实例 = 一条证据")

tf = textbox(s, MARGIN, y + 0.06, 6.35, 0.32)
para(tf, "一条 GlyphInstance 长这样", size=12.5, bold=True, color=BRONZE, first=True)
box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(MARGIN), Inches(y + 0.42),
                         Inches(6.35), Inches(3.05))
box.fill.solid()
box.fill.fore_color.rgb = RGBColor(0x2B, 0x27, 0x20)
box.line.fill.background()
box.shadow.inherit = False
tf = box.text_frame
tf.word_wrap = True
tf.margin_left = Inches(0.22)
tf.margin_right = Inches(0.18)
tf.margin_top = Inches(0.16)
tf.margin_bottom = Inches(0.12)
tf.vertical_anchor = MSO_ANCHOR.TOP
code = [
    "{ era: 'jinwen',",
    "  artifact: '父辛尊',          // 哪件器物",
    "  catalogId: '《殷周金文集成》5749號',",
    "  sourceRef: '《殷周金文集成》…',",
    "  sourceUrl: '…/search.php?word=馬',  // 点得开",
    "  dateRange: '商代',",
    "  imageSrc: 'glyphs/馬-jinwen-1.jpg',",
    "  verification: 'verified',",
    "  verifier: '香港中文大學《漢語多功能字庫》' }",
]
for i, line in enumerate(code):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.line_spacing = 1.30
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = line
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(0xD9, 0xD0, 0xBC)
    r.font.name = "Consolas"
    rPr = r._r.get_or_add_rPr()
    el = etree.SubElement(rPr, qn("a:ea"))
    el.set("typeface", "Consolas")

tf = textbox(s, 7.40, y + 0.06, 5.15, 0.32)
para(tf, "生成规则（写死在脚本里）", size=12.5, bold=True, color=SEAL, first=True)
bullets(s, 7.40, y + 0.44, 5.15, [
    ("有权威源 → ", "生成 verified 条目，带器名与编号"),
    ("源里缺 → ", "自动降级为缺环，写 gapNote，不抛错"),
    ("绝不因为「某期没有」", "就拿别的时代字形来顶"),
], size=13, gap=9)
callout(s, MARGIN, H - 1.55, W - 2 * MARGIN,
        "所以「加一个字」不需要写代码：改字表 → 跑三个抓取器 → 跑生成脚本 → 构建推送，五步。",
        h=0.62, fs=13.5, color=INK_SOFT)
notes(s, "【7:55–8:40｜生成层】\n"
         "左边是一条真实数据，拿「馬」的金文举例：器名父辛尊、集成 5749 号、断代商代、一条可点的来源、一张图。\n"
         "这就是「一条实例 = 一条证据」的意思——它不是一个字符串，是可核对的四件套：器、号、书、图。\n"
         "右边是生成器的三条规则。第三条最重要：源里没有，就写缺环，绝不去别的时代借一个字形。\n"
         "所以加一个字只要五步，不用写代码。")

# ══════════════════════════════════════════════════════════
# 13 前端
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 13, TOTAL)
y = head(s, "04  前端", "一条纵向瀑布流，四个关键交互")

tf = textbox(s, MARGIN, y + 0.04, 4.55, 0.32)
para(tf, "视觉", size=12.5, bold=True, color=BRONZE, first=True)
bullets(s, MARGIN, y + 0.42, 4.55, [
    "墨 / 宣纸 / 印章红 / 青铜金 四色，去掉一切多余装饰",
    "时代名竖排，左侧一条青铜金细线做时间轴",
    "缺环用圆形「缺」印章 + 一句原因，视觉上是「空」而不是「漏」",
], size=12.5, gap=9)

tf = textbox(s, 5.60, y + 0.04, 6.95, 0.32)
para(tf, "交互", size=12.5, bold=True, color=SEAL, first=True)
rows = [
    ["交互", "实现要点"],
    ["逐期展示", "六期卡片顺序渲染；有实例就出图，没实例就出缺环"],
    ["点图看来源", "图片包在链接里，新标签打开该字字页 / 碑帖页（245 条全部可点）"],
    ["随机纸背", "每次进站随机取一幅历代名帖，重度虚化做底纹；中间压纸色保证正文对比度"],
    ["来源标注", "页脚与题识标明三个数据库，与「可追溯」的定位一致"],
]
table(s, 5.60, y + 0.42, 6.95, [1.55, 5.40], rows, fs=10.5, hdr_fs=11,
      row_h=0.72, hdr_h=0.34)
callout(s, MARGIN, H - 1.32, 4.55,
        "纸背做了区分度处理：中轴压纸色、四周留字形。", h=0.66, fs=11.5,
        color=INK_SOFT, align=PP_ALIGN.LEFT)
notes(s, "【8:40–9:35｜前端】\n"
         "视觉上我们只用了四个颜色，尽量像一张纸。时代名竖排，左边一根细线。\n"
         "交互四个：逐期展示、点图看来源、随机纸背、来源标注。\n"
         "第二个是这次的重点：245 张图全部可以点，点开是那个字在字库里的字页，或者是碑帖页。\n"
         "纸背是最近加的：每次进站随机一幅名帖，模糊到只看得出笔势，中间压一层纸色，保证正文还读得清。")

# ══════════════════════════════════════════════════════════
# 14 工程化
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 14, TOTAL)
y = head(s, "04  工程化", "部署与性能：两个坑，一次 −92%")
bullets(s, MARGIN, y + 0.08, W - 2 * MARGIN - 0.2, [
    ("部署：", "纯静态站。push main → GitHub Actions（pnpm@9 + Node 20）→ upload-pages-artifact → Pages。"),
    ("坑 1：", "图片地址写 `/glyphs/…`（前导斜杠），在 Pages 子路径下被解析到域名根而 404 —— 必须用相对路径。"),
    ("坑 2：", "CI 的 `tsc -b` 会把「声明了但没用」的变量当错误，本地 `vite` 跑看不见。"),
    ("性能：", "纸背 7 幅 1471KB → 124KB（−92%）；做法是把模糊烘焙进像素再转 WebP，运行时不再对整屏做 blur。"),
], size=15, gap=13)
callout(s, MARGIN, H - 1.85, W - 2 * MARGIN,
        "原则：既然最终一定要模糊，就不要把高频细节交给浏览器去下载。", h=0.62, fs=14, color=SEAL)
callout(s, MARGIN, H - 1.18, W - 2 * MARGIN,
        "7 幅名帖合计 124KB，单幅 12–29KB —— 比一张普通的照片还小，首屏不再为背景等待。",
        h=0.58, fs=12.5, color=INK_SOFT)
notes(s, "【9:35–10:25｜工程化】\n"
         "这两个坑都很具体。\n"
         "第一个：我们部署完发现图全裂了，查了一晚上，是 imageSrc 写成了带斜杠的绝对路径。\n"
         "在本地 dev 看不出来，因为本地就是根路径；上了 Pages 的子路径就 404。\n"
         "第二个：tsc 比 vite 严，声明了没用的变量它直接报错，而 vite 不管。\n"
         "性能这条：背景原来 1.4MB，现在 124KB。因为既然一定要模糊，就别把高清细节传到浏览器再糊掉。")

# ══════════════════════════════════════════════════════════
# 15 Prompt Log 五条
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 15, TOTAL)
y = head(s, "05  PROMPT LOG", "五条关键迭代：怎么问、AI 给了什么、我们怎么核验")
rows = [
    ["#", "我们的提问（意图）", "AI 给了什么", "我们怎么核验 / 修订"],
    ["①", "「输入一个字，按六期展示；\n每字形必须挂实物出处和核对状态；\n无实例显示缺环，不许倒填」",
     "React+Vite+TS 单页、纵向瀑布流、\n数据模型与三态",
     "人工砍掉「自动抓图」方案，\n改为「先有出处再有图」"],
    ["②", "「这几个字库哪些能程序化取数？\n给我可落地的取数方案」",
     "列出维基文库、Commons、\nwiktionary 等候选",
     "逐条实测：zdic 403、zi.tools 是 SPA、\n小學堂是 frameset —— 只留能通的"],
    ["③", "「先只做小篆一个源，\n跑通再接入其他时代」",
     "只改数据生成器 + 一个适配器",
     "每轮 tsc + build + 线上验证，\n通过才叠加下一轮"],
    ["④", "报错原文直接丢回去：\n「HTTP 429」「图片 200 但 0 字节」\n「部署后图 404」",
     "分别给出退避续抓、同站 Referer、\n相对路径三套修复",
     "逐条复现验证，\n并写进脚本注释与文档"],
    ["⑤", "「背景再清晰一点，\n能看到字的模样但不打扰正文」",
     "给出 blur / 透明度 / 罩层参数",
     "用 Pillow 合成预览反复比对，\n最终 26px→9px、.56→.78"],
]
table(s, MARGIN, y + 0.10, W - 2 * MARGIN, [0.52, 3.55, 3.30, 3.85], rows,
      fs=9.5, hdr_fs=10.5, row_h=0.86, hdr_h=0.34)
notes(s, "【10:25–11:20｜Prompt Log】\n"
         "这一页是过程性证据。五条，正好对应五步闭环。\n"
         "重点看第四列：AI 给的东西，我们几乎每一次都改了。\n"
         "比如第②条，它列了六个源，我们实测砍掉四个；第④条它给的修复我们逐条复现过才写下。\n"
         "这不是「AI 帮我们写完」，是「AI 帮我们加速迭代，我们负责核对」。")

# ══════════════════════════════════════════════════════════
# 16 现场演示
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 16, TOTAL)
y = head(s, "06  现场演示", "三步：查「马」→ 点开甲骨图 → 查「纸」",
         "不用录屏，直接开线上站点；网络异常就切本地 npm run dev 或下一张备用图。")

steps = [
    ("STEP 1", "输入「马」", "六期里五个时代有实例；金文一次给出三件器，器名与集成号都在图下。"),
    ("STEP 2", "点甲骨文那张小图", "新标签打开港中大这个字的字页——图片本身不允许跨站直链，所以链接指向可复核的字页。"),
    ("STEP 3", "输入「纸」", "甲骨/金文/战国三格是缺环：不是因为没查，而是汉代后起字本无此形；小篆、隶有实例，楷书暂无图。"),
]
yy = y + 0.16
for tag, title, desc in steps:
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(MARGIN), Inches(yy),
                            Inches(W - 2 * MARGIN), Inches(0.98))
    sh.fill.solid()
    sh.fill.fore_color.rgb = WHITE
    sh.line.color.rgb = LINE
    sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    sh.adjustments[0] = 0.10
    tf = textbox(s, MARGIN + 0.22, yy + 0.14, 1.05, 0.3)
    para(tf, tag, size=10.5, bold=True, color=SEAL, first=True)
    tf = textbox(s, MARGIN + 1.35, yy + 0.10, 9.9, 0.34)
    para(tf, title, size=15, bold=True, color=INK, face=SERIF, first=True)
    tf = textbox(s, MARGIN + 1.35, yy + 0.47, W - 2 * MARGIN - 1.6, 0.44)
    para(tf, desc, size=11.5, color=MUTED, first=True, line=1.24)
    yy += 1.10

callout(s, MARGIN, H - 1.18, W - 2 * MARGIN,
        "演示要慢：每点一步，先说「为什么要看这个」，再让结果自己说话。",
        h=0.58, fs=12.5, color=INK_SOFT)
notes(s, "【11:20–13:00｜现场演示 2:10】\n"
         "（打开 https://otherhello.github.io/hanzi-timeline/）\n"
         "第一步，输入「马」。注意上面：六个时代里五个有实例，金文一次给了三件器——父辛尊、小臣守、大馬簠，\n"
         "每件都带集成号。\n"
         "第二步，我点这张甲骨文小图。（新标签打开）这是港中大字库里「馬」的这个字页。\n"
         "为什么不直接链到图片？因为那个端点要求同站 Referer，直接链过去是空白页——所以链接要指向可复核的字页。\n"
         "第三步，输入「纸」。（滚动）甲骨、金文、战国三格是「缺环」，上面写的是：汉代后起字，本无此形。\n"
         "这不是我们没查到，是这个字在那个时代还不存在。小篆和隶有实例，楷书那格写着「待核对」。\n"
         "（如时间允许）再输入「水」看一眼，或者刷新一次看纸背换了一幅。")

# ══════════════════════════════════════════════════════════
# 17 分工
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 17, TOTAL)
y = head(s, "07  分工说明", "按「可独立交付的模块」切，不按行数切")
rows = [
    ["成员", "负责", "主要产出"],
    ["成员一（姓名待填）", "数据采集与校验", "三个抓取器、四个数据源、缺环判定规则"],
    ["成员二（姓名待填）", "前端与视觉", "六期纵向时间轴、缺环组件、点图看来源、纸背与动效"],
    ["成员三（姓名待填）", "工程、文档与验收", "部署流水线、性能优化、工作流文档、演示脚本与控时"],
]
table(s, MARGIN, y + 0.10, W - 2 * MARGIN, [2.6, 2.6, 6.15], rows,
      fs=12.5, hdr_fs=12.5, row_h=0.66, hdr_h=0.42)
callout(s, MARGIN, y + 0.42 + 0.66 * 3 + 0.28, W - 2 * MARGIN,
        "三人共同参与每一轮的 Prompt 迭代与验收：谁提需求、谁核验结果，都在 Prompt Log 里留痕。",
        h=0.66, fs=13, color=INK_SOFT)
callout(s, MARGIN, y + 0.42 + 0.66 * 3 + 1.06, W - 2 * MARGIN,
        "提示：把姓名替换成实际成员；如为个人作业，可改为「个人承担，按模块分阶段推进」。",
        h=0.58, fs=11.5, color=MUTED)
notes(s, "【13:00–13:25｜分工】\n"
         "分工按能独立交付的模块切：数据、前端、工程与文档。\n"
         "但要说清楚：每一轮的 Prompt 和验收是三个人一起做的，不是一个人写完另一个验收。\n"
         "（此处按实际成员替换姓名与具体贡献。）")

# ══════════════════════════════════════════════════════════
# 18 Prompt Log 附录
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 18, TOTAL)
y = head(s, "附录", "Prompt Log 全表（过程性评价依据）")
rows = [
    ["迭代", "我们怎么问（原文摘要）", "确认 / 修订 / 版本变化"],
    ["1 · 意图", "「输入一个字，按六期展示，每字形挂实物出处与核对状态，无实例显示缺环，绝不用后世字形倒填，也不用示意图冒充实物」",
     "确认：三态与缺环语义；修订：否决「AI 自动搜图填满六期」，改为缺环优先"],
    ["2 · 方案", "「你列的这些源，哪些能程序化取数？给出请求方式、返回结构、注意事项」",
     "修订：zdic 403 弃用；zi.tools 为 SPA 弃用；定为 Wikisource + 港中大 + 词典网三源"],
    ["3 · 增量", "「这一轮只做小篆：抓《說文》、生成 8 个字的 characters.ts、页面能渲染出图」",
     "版本 v1 → v2：先假数据跑通页面，再接真源；每轮 tsc + build + 线上验收"],
    ["4 · 调试", "「HTTP 429」/「200 但 0 字节」/「部署后图 404」/「test.ts 未使用变量报错」",
     "退避续抓、同站 Referer、相对路径、删未用变量；四条都写进注释与 DEPLOY.md"],
    ["5 · 审美", "「背景太糊，要能看出字的模样但不能抢正文」/「首屏加载慢」",
     "blur 26→9、透明度 .56→.78、中轴压纸色；模糊烘焙进像素 + WebP，1471KB→124KB"],
]
table(s, MARGIN, y + 0.10, W - 2 * MARGIN, [0.95, 6.05, 4.75], rows,
      fs=9, hdr_fs=10, row_h=0.92, hdr_h=0.32)
notes(s, "【13:25–13:40｜附录（可略）】\n"
         "这是同一组 Prompt 的更完整版本，含每轮版本变化。\n"
         "如果前面超时，这一页直接跳过，正文第 15 页已经讲过要点。")

# ══════════════════════════════════════════════════════════
# 19 结语
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 19, TOTAL)
y = head(s, "结语", "做到了什么 / 没做什么")

tf = textbox(s, MARGIN, y + 0.06, 5.75, 0.34)
para(tf, "已经做到", size=13, bold=True, color=BRONZE, first=True)
bullets(s, MARGIN, y + 0.46, 5.75, [
    "28 个字、246 条实例、245 张图，条条可点回来源",
    "缺环如实留白，并区分「本无此形」与「资料不足」",
    "加一个字不改代码；换源只改一层",
], size=13.5, gap=9)

tf = textbox(s, 6.85, y + 0.06, 5.70, 0.34)
para(tf, "局限（不藏）", size=13, bold=True, color=SEAL, first=True)
bullets(s, 6.85, y + 0.46, 5.70, [
    "「已核对」= 库内可溯，未逐件核对原拓",
    "楷书仍依赖单一站点，紙 字无图",
    "甲骨/金文的释读与断代未做二次学术校验",
], size=13.5, gap=9)

callout(s, MARGIN, H - 1.85, W - 2 * MARGIN,
        "它不是一张好看的演变图，而是一条能被逐条追溯、并且敢于留白的证据链。",
        h=0.76, fs=16.5, color=SEAL)
tf = textbox(s, MARGIN, H - 0.92, W - 2 * MARGIN, 0.34)
para(tf, "谢谢，欢迎提问。线上地址：https://otherhello.github.io/hanzi-timeline/",
     size=12.5, color=MUTED, first=True, align=PP_ALIGN.CENTER)
notes(s, "【13:40–14:00｜结语】\n"
         "最后一句总结：我们做到了「每条都能点回来源」，也敢说「这几格真的没有」。\n"
         "局限我也写在这：已核对是库内可溯，不是逐件核原拓；楷书还依赖一个站；甲骨释读没做二次校验。\n"
         "这三点如果老师追问，我会照实答。谢谢，欢迎提问。")

os.makedirs(HERE, exist_ok=True)
prs.save(OUT)
print("saved:", OUT)
print("slides:", len(prs.slides.__iter__.__self__._sldIdLst))
