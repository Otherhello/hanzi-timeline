# -*- coding: utf-8 -*-
"""按「改良版提示词」生成课堂汇报 PPT（13:50，定额分配）。

结构（时间锁定，超出时按 附录 → 结语 → 数据源细节 的顺序砍）：
  0:00–1:30   选题背景与任务目标        p1–p4
  1:30–4:20   AI Coding 通用技术点       p5–p7   （只讲技术点，不复述项目过程）
  4:20–6:10   数据来源与规模             p8–p9
  6:10–10:50  方案设计与技术路线         p10–p15 （含「如何用 AI」五步 × 五条真实迭代）
  10:50–13:10 现场演示                   p16
  13:10–13:50 分工说明 + 结语            p17–p18
  ———        附录：Prompt Log 全表      p19（不占讲解时间）

产物：docs/汉字字形演变证据链-汇报提纲.pptx
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
         first=False):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = line
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
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
    rule(s, 0, 0, W, BRONZE, 0.055)
    return s


def page_no(slide, n, total):
    tf = textbox(slide, W - 1.75, H - 0.55, 1.1, 0.3)
    para(tf, f"{n} / {total}", size=9.5, color=MUTED, align=PP_ALIGN.RIGHT, first=True)


def head(slide, eyebrow, title, subtitle=None):
    if eyebrow:
        tf = textbox(slide, MARGIN, 0.52, W - 2 * MARGIN, 0.3)
        para(tf, eyebrow, size=11.5, bold=True, color=BRONZE, first=True)
    tf = textbox(slide, MARGIN, 0.86, W - 2 * MARGIN, 0.75)
    para(tf, title, size=26, bold=True, color=INK, face=SERIF, first=True, line=1.15)
    rule(slide, MARGIN, 1.62, 0.95, SEAL, 0.035)
    y = 1.80
    if subtitle:
        tf = textbox(slide, MARGIN, y, W - 2 * MARGIN, 0.4)
        para(tf, subtitle, size=13, color=INK_SOFT, first=True)
        y += 0.46
    return y


def bullets(slide, l, t, w, items, *, size=15.5, gap=8, color=INK_SOFT,
            bullet_color=BRONZE, line=1.38, h=None):
    tf = textbox(slide, l, t, w, h or (H - t - 0.7))
    for i, it in enumerate(items):
        p = para(tf, "", size=size, space_after=gap, line=line, first=(i == 0))
        r = p.add_run()
        r.text = "— "
        r.font.size = Pt(size)
        r.font.color.rgb = bullet_color
        set_ea(r, SANS)
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
# 1 封面                        0:00–0:12
# ══════════════════════════════════════════════════════════
s = new_slide()

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
para(tf, "课程汇报 · 13 分 50 秒 · 28 个字 / 246 条实例 / 245 张实物图", size=13, color=MUTED)
notes(s, "【0:00–0:12｜封面】\n"
         "各位老师、同学好。我们做的是一个很小的东西：输入一个字，看它在六个时代里分别长什么样，\n"
         "并且每一个样子都能指回一件实物。网址在下面，现在就可以打开。\n"
         "接下来 13 分 50 秒，我会讲四件事：为什么做、一个关于 AI 编程的技术点、数据从哪来、然后现场演示。")

# ══════════════════════════════════════════════════════════
# 2 议程                        0:12–0:20
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 2, TOTAL)
y = head(s, "AGENDA", "六件事，时间已锁死",
         "每页备注都标了起止时间；超时按「附录 → 结语 → 数据源细节」的顺序砍。")

rows = [
    ["#", "段落", "要回答的问题", "起–止", "时长"],
    ["1", "选题背景与任务目标", "为什么做、做什么、意义", "0:00–1:30", "1:30"],
    ["2", "AI Coding 通用技术点", "只讲一个技术点：是什么、差在哪、怎么判断", "1:30–4:20", "2:50"],
    ["3", "数据来源与规模", "真实来源、四口径数字、三态怎么标", "4:20–6:10", "1:50"],
    ["4", "方案设计与技术路线", "架构、如何用 AI、踩坑与修复、Prompt Log", "6:10–10:50", "4:40"],
    ["5", "现场作品演示", "3 步脚本，真实数据现场操作", "10:50–13:10", "2:20"],
    ["6", "分工说明 + 结语", "谁做了什么、局限在哪", "13:10–13:50", "0:40"],
]
table(s, MARGIN, y + 0.06, W - 2 * MARGIN, [0.52, 3.05, 4.55, 1.55, 0.85], rows,
      fs=13, hdr_fs=12.5, row_h=0.56, hdr_h=0.44)
callout(s, MARGIN, y + 0.06 + 0.44 + 0.56 * 6 + 0.20, W - 2 * MARGIN,
        "合计 13:50。附录（Prompt Log 全表）不占讲解时间，只在被追问时翻。",
        h=0.58, fs=13, color=INK_SOFT)
notes(s, "【0:12–0:20｜议程】\n"
         "六件事。第 2 段是老师要求的通用 AI 技术点，我只讲一个：AI 编码代理。\n"
         "第 4 段最长，讲架构和我们真实的迭代过程。第 5 段是演示。")

# ══════════════════════════════════════════════════════════
# 3 选题背景                    0:20–0:55
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 3, TOTAL)
y = head(s, "01  选题背景", "我们想回答一个很具体的问题")
bullets(s, MARGIN, y + 0.10, W - 2 * MARGIN - 0.2, [
    ("字形更替是常识，", "可「这个写法出自哪件实物」很少被认真回答。"),
    ("现成的「字形演变图」很好看，", "但多数是后人摹写、重绘或字体渲染，指向不了任何一件原件。"),
    ("于是「演变」变成了看图说话，", "而不是可核对的证据。"),
    ("我们想做的，", "是把「看图」换成「查证据链」——宁可留白，也不给一条假证据。"),
], size=16.5, gap=13)
callout(s, MARGIN, H - 1.92, W - 2 * MARGIN,
        "一句话：这不是一张好看的演变图，而是一条能被逐条追溯、并且敢于留白的证据链。",
        h=0.70, fs=15, color=SEAL)
notes(s, "【0:20–0:55｜背景】\n"
         "先说我的困惑。查一个字，很容易看到「演变图」：甲骨、金文、小篆、隶、楷排一排。\n"
         "但那些图大多没有出处——是摹本、是重绘、是拿字体渲染的。它看起来像证据，其实只是插图。\n"
         "所以我们把问题换成：每一个字形，能不能指回一件实物。这句话是后面所有取舍的标准。")

# ══════════════════════════════════════════════════════════
# 4 目标与三条铁律               0:55–1:30
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
     "每条实例带 artifact、catalogId、sourceRef、sourceUrl"],
    ["② 无实例就是缺环，绝不倒填",
     "数据里有 isGap + gapNote；生成器遇源缺失自动产缺环"],
    ["③ 不用示意图冒充实物",
     "所有图来自馆藏扫描、拓本或传世字书；未接入时显示空帧"],
]
table(s, 6.62, y + 0.44, 5.9, [1.95, 3.95], rules_rows, fs=11, hdr_fs=11.5,
      row_h=0.92, hdr_h=0.38)
notes(s, "【0:55–1:30｜目标与铁律】\n"
         "目标是三句话：六个时代、每个字形挂出处、没有就说没有。\n"
         "右边三条不是口号：第一条对应数据结构里的四个字段，第二条对应 isGap 这个布尔量，\n"
         "第三条对应取图规则——没有图就显示空帧，而不是画一个。\n"
         "这一页定完，后面所有决策都从这里推出来。")

# ══════════════════════════════════════════════════════════
# 5 技术点①：是什么              1:30–2:20
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 5, TOTAL)
y = head(s, "02  AI CODING 通用技术点", "AI 编码代理：把「一次能验证的改动」作为交付单位")
bullets(s, MARGIN, y + 0.06, W - 2 * MARGIN - 0.2, [
    ("定义：", "能自己读文件、跑命令、看报错、改代码，并按轮次交付可运行结果。"),
    ("与「问答 / 补全」的根本区别：", "输入不只是需求，还包括仓库状态和运行反馈。"),
], size=15.5, gap=10)
rows = [
    ["用法", "你给它什么", "它给你什么", "谁来验证"],
    ["问答 / 搜索", "一个问题", "一段解释", "你"],
    ["代码补全", "光标前后的上下文", "几行代码", "你"],
    ["一次性生成", "一段需求描述", "一大段代码", "你（而且很难验）"],
    ["编码代理", "目标 + 仓库 + 验收标准", "可运行的改动 + 报错处理", "每一轮都由你验收"],
]
table(s, MARGIN, y + 1.10, W - 2 * MARGIN, [1.95, 3.35, 3.35, 3.05], rows,
      fs=11.5, hdr_fs=11.5, row_h=0.46, hdr_h=0.38)
callout(s, MARGIN, H - 1.10, W - 2 * MARGIN,
        "所以代理的价值不在「写得更多」，而在「每一轮都能被验证」。",
        h=0.56, fs=14, color=SEAL)
notes(s, "【1:30–2:20｜技术点 1/3】\n"
         "老师要求讲一个通用的 AI 编程技术点。我选的是「AI 编码代理」。\n"
         "一句话定义：它能自己读文件、跑命令、看报错、改代码，并且按轮次交付能跑的结果。\n"
         "下面这张表是它和另外三种用法的区别。关键在最后一列：验证责任在哪。\n"
         "问答和补全，验证责任在你；一次性生成，验证责任也在你，而且你很难验；\n"
         "编码代理，每一轮都有机会验——这是它唯一真正的优势。")

# ══════════════════════════════════════════════════════════
# 6 技术点②：三条差别            2:20–3:15
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 6, TOTAL)
y = head(s, "02  AI CODING 通用技术点", "它真正改变的是三件事：反馈、作用域、交付物")
cards(s, MARGIN, y + 0.12, W - 2 * MARGIN, [
    ("01", "反馈回路", "报错原文成为输入，\n而不是噪声。\n有反馈才谈得上调试。"),
    ("02", "作用域", "一次只动一处，\n改动可回滚、\n可定位到具体一层。"),
    ("03", "交付物", "每轮结束都该有\n一个能跑的东西：\nbuild 过、页面开得了。"),
], h=1.62, gap=0.24, fs=11.5, title_fs=13.5)
callout(s, MARGIN, y + 2.02, W - 2 * MARGIN,
        "推论：提问方式要从「帮我写 X」变成「把 X 做到能跑，用 Y 来验收」。",
        h=0.60, fs=14, color=SEAL)
bullets(s, MARGIN, y + 2.80, W - 2 * MARGIN, [
    ("反例：", "「做一个汉字演变网站」——它会给一个漂亮的空壳，你无法判断哪里坏了。"),
    ("正例：", "「只做小篆一个源，跑通再接入其他时代」——产出一个可验收的最小闭环。"),
], size=13.5, gap=8)
notes(s, "【2:20–3:15｜技术点 2/3】\n"
         "它改变的是三件事。\n"
         "第一，反馈：以前报错对你是噪声，现在报错是它的输入。第二，作用域：一次只动一处，\n"
         "改坏了能回滚、能定位。第三，交付物：每轮结束必须有一个能跑的东西，否则这一轮不算数。\n"
         "由此推出一个很实用的规则：提问要从「帮我写 X」改成「把 X 做到能跑，用 Y 验收」。\n"
         "反面例子就是「做一个汉字演变网站」，正面例子是「只做小篆一个源」。")

# ══════════════════════════════════════════════════════════
# 7 技术点③：判断标准与边界      3:15–4:20
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 7, TOTAL)
y = head(s, "02  AI CODING 通用技术点", "四个判断标准，三条失效边界")
cards(s, MARGIN, y + 0.10, W - 2 * MARGIN, [
    ("标准一", "能自己拿事实", "读文件、跑命令、\n看报错，而不是\n靠你转述"),
    ("标准二", "每轮有验收动作", "build / test /\n打开页面，\n通过才继续"),
    ("标准三", "改动可回滚", "一次只碰一处，\n出问题能退回\n上一轮"),
    ("标准四", "30 秒能判对错", "看一眼结果就知道\n这一轮成没成"),
], h=1.58, gap=0.20, fs=11, title_fs=12.5)

tf = textbox(s, MARGIN, y + 1.94, 6.0, 0.34)
para(tf, "什么时候它会失效", size=13, bold=True, color=SEAL, first=True)
bullets(s, MARGIN, y + 2.30, 6.0, [
    ("需求不可验证：", "「做得好看一点」没有判据"),
    ("事实拿不到：", "数据在需要登录的站内"),
    ("一次跨太多模块：", "改 5 个以上文件，错在哪说不清"),
], size=12.5, gap=7)

tf = textbox(s, 7.15, y + 1.94, 5.4, 0.34)
para(tf, "怎么用（一条可复制的规则）", size=13, bold=True, color=BRONZE, first=True)
bullets(s, 7.15, y + 2.30, 5.4, [
    "先切出一个能验证的最小闭环",
    "再给它事实（文件、报错、标准）",
    "每轮结束先验收，再叠加下一轮",
], size=12.5, gap=7)
notes(s, "【3:15–4:20｜技术点 3/3】\n"
         "这一页是全场最「通用」的一页。四个标准，你拿任何工具都能对照。\n"
         "第一，它能不能自己拿到事实——如果它只能靠你转述，那你就是在替它调试。\n"
         "第二，每轮有没有验收动作。第三，改动能不能回滚。第四，你 30 秒内能不能判断对错。\n"
         "右边是失效边界：需求不可验证、事实拿不到、一次跨太多模块——这三种情况，代理帮不上忙，\n"
         "甚至会让错误扩散得更快。所以我给了一条可复制的规则：先切最小闭环，再给它事实，每轮先验收。")

# ══════════════════════════════════════════════════════════
# 8 数据源                      4:20–5:10
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
      fs=11.5, hdr_fs=12, row_h=0.68, hdr_h=0.42)
callout(s, MARGIN, H - 1.30, W - 2 * MARGIN,
        "四源合起来覆盖六期：小篆有传世字书，甲骨/金文/战国/隶有学术字库，楷书落到具体碑帖。",
        h=0.56, fs=12.5, color=INK_SOFT)
notes(s, "【4:20–5:10｜数据源】\n"
         "四个库，每个管一段。\n"
         "《說文解字》管小篆，9335 个字头，我们抓到 7338 个可解析的。\n"
         "港中大那个最强：一个字进去，甲骨、金文、小篆、简帛分栏列出，旁边就是器名和集成号。\n"
         "楷书没有这样的库，只能落到词典网的碑帖图。\n"
         "最右边这一列是坑，待会儿第 11 页说怎么解决。")

# ══════════════════════════════════════════════════════════
# 9 规模与三态                   5:10–6:10
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 9, TOTAL)
y = head(s, "03  规模与三态", "28 个字 / 246 条实例 / 245 张实物图")

tf = textbox(s, MARGIN, y + 0.04, 5.55, 0.32)
para(tf, "四个口径（不能混着说）", size=12.5, bold=True, color=BRONZE, first=True)
rows2 = [
    ["口径", "数量", "含义"],
    ["字", "28", "可查询的字头总数"],
    ["字形实例", "246", "「字 × 时代」的条目数"],
    ["实物图", "245", "有图可看的实例数"],
    ["缺环", "5", "该时代确无实例"],
]
table(s, MARGIN, y + 0.42, 5.55, [1.35, 0.95, 3.25], rows2, fs=11.5, hdr_fs=11.5,
      row_h=0.50, hdr_h=0.36)

tf = textbox(s, 6.55, y + 0.04, 5.95, 0.32)
para(tf, "三态的准确含义（答辩重点）", size=12.5, bold=True, color=SEAL, first=True)
st = [
    ["状态", "含义", "数量"],
    ["已核对", "图与出处取自权威库，来源页可点开、可机器复核\n（= 库内可溯，不等于逐件核对原拓）", "245"],
    ["待核对", "有出处但暂无图（紙·楷书，该库无此字页）", "1"],
    ["缺环", "该时代确无可信实例，写明原因", "5"],
]
table(s, 6.55, y + 0.42, 5.95, [0.95, 4.15, 0.85], st, fs=10.5, hdr_fs=11,
      row_h=0.80, hdr_h=0.34)
callout(s, MARGIN, H - 1.42, W - 2 * MARGIN,
        "「缺环」里 紙 的甲骨/金文/战国三格，是汉代后起字本无此形——这不是资料不足，恰恰证明我们没有倒填。",
        h=0.62, fs=12.5, color=SEAL)
notes(s, "【5:10–6:10｜规模与三态】\n"
         "先说四个口径，因为「多少条」很容易说不清：28 个字、246 条字形实例、245 张实物图、5 处缺环。\n"
         "左边这张表就是四个数各自的含义，不要混着念。\n"
         "右边是三态。已核对 245，意思是「库内可溯」——图和出处都在权威库里，来源页点得开；\n"
         "它不等于我逐件核对了原拓，这一点我不夸大。待核对 1 条，是紙的楷书，那个库没有这个字页。\n"
         "缺环 5 条，其中紙的三格是「本无此形」，不是「没查到」。")

# ══════════════════════════════════════════════════════════
# 10 架构                       6:10–6:55
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
        h=0.60, fs=13, color=INK_SOFT)
bullets(s, MARGIN, y + 2.56, W - 2 * MARGIN, [
    ("好处：", "换源只改抓取层，改版式只改前端，加字只改字表——三者互不牵连。"),
    ("所以它能长期跑：", "任何一个源挂了，只会多出几条缺环，站点不会崩。"),
], size=14, gap=8)
notes(s, "【6:10–6:55｜架构】\n"
         "这是整条链路：源、抓取、缓存、生成、前端、部署。\n"
         "最关键的一句在中间：抓取和生成是分离的。抓取脚本不知道什么叫缺环，它只负责搬；\n"
         "生成脚本不联网，只按规则组装。这样换源、加字、改版式三个动作互不影响。")

# ══════════════════════════════════════════════════════════
# 11 采集层                     6:55–7:45
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
      fs=11, hdr_fs=11.5, row_h=0.98, hdr_h=0.42)
callout(s, MARGIN, H - 1.34, W - 2 * MARGIN,
        "这些细节才是「能不能长期跑」的分界线：限流、编码、Referer、水印——每一个都能让流水线在半夜静默失败。",
        h=0.62, fs=12.5, color=INK_SOFT)
notes(s, "【6:55–7:45｜采集层】\n"
         "三个脚本的坑，挑三个讲。\n"
         "第一个：抓《說文》前 10 卷顺利，第 11 卷 429。解决办法不是手动重跑，是退避加断点续抓。\n"
         "第二个：港中大返回 200 但是 0 字节，查了半天是 Referer，它只允许同站引用图片。\n"
         "第三个：词典网 https 证书过期，脚本走不了，只能 http。\n"
         "这三个如果不知道，流水线就会在半夜静默失败。")

# ══════════════════════════════════════════════════════════
# 12 生成层                     7:45–8:30
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
callout(s, MARGIN, H - 1.32, W - 2 * MARGIN,
        "所以「加一个字」不需要写代码：改字表 → 跑三个抓取器 → 跑生成脚本 → 构建推送，五步。",
        h=0.58, fs=13, color=INK_SOFT)
notes(s, "【7:45–8:30｜生成层】\n"
         "左边是一条真实数据，拿「馬」的金文举例：器名父辛尊、集成 5749 号、断代商代、\n"
         "一条可点的来源、一张图。这就是「一条实例 = 一条证据」——它不是一个字符串。\n"
         "右边三条规则，第三条最重要：源里没有就写缺环，绝不去别的时代借字形。\n"
         "所以加一个字只要五步，不用写代码。")

# ══════════════════════════════════════════════════════════
# 13 前端                       8:30–9:15
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
callout(s, MARGIN, H - 1.28, 4.55,
        "纸背做了区分度处理：中轴压纸色、四周留字形。", h=0.62, fs=11.5,
        color=INK_SOFT, align=PP_ALIGN.LEFT)
notes(s, "【8:30–9:15｜前端】\n"
         "视觉上只用了四个颜色，尽量像一张纸。时代名竖排，左边一根细线。\n"
         "交互四个：逐期展示、点图看来源、随机纸背、来源标注。\n"
         "第二个是重点：245 张图全部可以点，点开是那个字在字库里的字页，或者碑帖页。")

# ══════════════════════════════════════════════════════════
# 14 工程化                     9:15–10:00
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 14, TOTAL)
y = head(s, "04  工程化", "部署与性能：两个坑，一次 −92%")
bullets(s, MARGIN, y + 0.08, W - 2 * MARGIN - 0.2, [
    ("部署：", "纯静态站。push main → GitHub Actions（pnpm@9 + Node 20）→ upload-pages-artifact → Pages。"),
    ("坑 1：", "图片地址写 `/glyphs/…`（前导斜杠），在 Pages 子路径下被解析到域名根而 404 —— 必须用相对路径。"),
    ("坑 2：", "CI 的 `tsc -b` 会把「声明了但没用」的变量当错误，本地 `vite` 跑看不见。"),
    ("性能：", "纸背 7 幅 1471KB → 124KB（−92%）；把模糊烘焙进像素再转 WebP，运行时不再对整屏做 blur。"),
], size=14.5, gap=12)
callout(s, MARGIN, H - 1.80, W - 2 * MARGIN,
        "原则：既然最终一定要模糊，就不要把高频细节交给浏览器去下载。", h=0.58, fs=13.5, color=SEAL)
callout(s, MARGIN, H - 1.16, W - 2 * MARGIN,
        "7 幅名帖合计 124KB，单幅 12–29KB —— 比一张普通的照片还小，首屏不再为背景等待。",
        h=0.54, fs=12, color=INK_SOFT)
notes(s, "【9:15–10:00｜工程化】\n"
         "两个坑都很具体。第一个：部署后图全裂，是 imageSrc 写成带斜杠的绝对路径，\n"
         "本地 dev 看不出来，上了子路径就 404。第二个：tsc 比 vite 严，声明了没用的变量直接报错。\n"
         "性能：背景原来 1.4MB，现在 124KB。既然一定要模糊，就别把高清细节传到浏览器再糊掉。")

# ══════════════════════════════════════════════════════════
# 15 如何用 AI：五步 × 五条       10:00–10:50
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 15, TOTAL)
y = head(s, "04  如何用 AI（Prompt Log 正文）", "五步 × 五条真实迭代：怎么问、它给什么、我们怎么验")

rows = [
    ["步", "我们的提问（意图原话摘要）", "AI 给了什么", "我们的判断 / 修订"],
    ["① 意图", "「输入一个字，按六期展示；\n每字形挂实物出处与核对状态；\n无实例显示缺环，不许倒填」",
     "React+Vite+TS 单页、\n纵向瀑布流、三态模型",
     "否决「自动搜图填满六期」，\n改为「先有出处再有图」"],
    ["② 方案", "「这几个字库哪些能程序化取数？\n给我可落地的取数方案」",
     "列出维基文库、Commons、\nwiktionary 等候选",
     "逐条实测：zdic 403、zi.tools 是 SPA、\n小學堂是 frameset —— 只留能通的"],
    ["③ 增量", "「先只做小篆一个源，\n跑通再接入其他时代」",
     "只改数据生成器 +\n一个适配器",
     "每轮 tsc + build + 线上验证，\n通过才叠加下一轮"],
    ["④ 调试", "「HTTP 429」「图片 200 但 0 字节」\n「部署后图 404」原文丢回去",
     "退避续抓、同站 Referer、\n相对路径三套修复",
     "逐条复现验证，\n并写进脚本注释与 DEPLOY.md"],
    ["⑤ 审美", "「背景太糊，要能看出字的模样\n但不能抢正文」",
     "给出 blur / 透明度 /\n罩层参数",
     "用 Pillow 合成预览比对，\n最终 26px→9px、.56→.78"],
]
table(s, MARGIN, y + 0.10, W - 2 * MARGIN, [0.80, 3.60, 3.20, 3.62], rows,
      fs=9.5, hdr_fs=10.5, row_h=0.86, hdr_h=0.34)
notes(s, "【10:00–10:50｜如何用 AI / Prompt Log】\n"
         "这一页同时回答两个问题：我们怎么用 AI，以及 Prompt Log。\n"
         "五步正好对应五条真实迭代。重点看最后一列——AI 给的东西，我们几乎每一次都改了。\n"
         "比如第②条它列了六个源，我们实测砍掉四个；第④条它给的修复，我们逐条复现才写下。\n"
         "这不是「AI 替我们写完」，是「AI 帮我们加速迭代，我们负责核对」。")

# ══════════════════════════════════════════════════════════
# 16 现场演示                   10:50–13:10
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 16, TOTAL)
y = head(s, "05  现场演示", "三步：查「马」→ 点开甲骨图 → 查「纸」",
         "不录屏，直接开线上站点；若断网或接口异常，切本地 npm run dev，或用事先截好的静态图兜底。")

steps = [
    ("STEP 1", "输入「马」", "六期里五个时代有实例；金文一次给出三件器，器名与集成号都在图下。"),
    ("STEP 2", "点甲骨文那张小图", "新标签打开港中大这个字的字页——图片本身不允许跨站直链，所以链接指向可复核的字页。"),
    ("STEP 3", "输入「纸」", "甲骨/金文/战国三格是缺环：不是因为没查，而是汉代后起字本无此形；小篆、隶有实例，楷书暂无图。"),
]
yy = y + 0.10
for tag, title, desc in steps:
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(MARGIN), Inches(yy),
                            Inches(W - 2 * MARGIN), Inches(0.94))
    sh.fill.solid()
    sh.fill.fore_color.rgb = WHITE
    sh.line.color.rgb = LINE
    sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    sh.adjustments[0] = 0.10
    tf = textbox(s, MARGIN + 0.22, yy + 0.13, 1.05, 0.3)
    para(tf, tag, size=10.5, bold=True, color=SEAL, first=True)
    tf = textbox(s, MARGIN + 1.35, yy + 0.09, 9.9, 0.34)
    para(tf, title, size=14.5, bold=True, color=INK, face=SERIF, first=True)
    tf = textbox(s, MARGIN + 1.35, yy + 0.45, W - 2 * MARGIN - 1.6, 0.44)
    para(tf, desc, size=11, color=MUTED, first=True, line=1.24)
    yy += 1.06

callout(s, MARGIN, H - 1.76, W - 2 * MARGIN,
        "演示要慢：每点一步，先说「为什么要看这个」，再让结果自己说话。", h=0.54, fs=12, color=INK_SOFT)
callout(s, MARGIN, H - 1.16, W - 2 * MARGIN,
        "兜底：断网 → 本地 npm run dev；接口异常 → 切换事先截好的一张整页截图。",
        h=0.50, fs=11.5, color=MUTED)
notes(s, "【10:50–13:10｜现场演示 2:20】\n"
         "（打开 https://otherhello.github.io/hanzi-timeline/）\n"
         "第一步，输入「马」。六个时代里五个有实例，金文一次给了三件器——父辛尊、小臣守、大馬簠，\n"
         "每件都带集成号。\n"
         "第二步，点这张甲骨文小图。（新标签打开）这是港中大字库里「馬」的字页。\n"
         "为什么不直接链图片？因为那个端点要求同站 Referer，直接链过去是空白页，所以链接指向字页。\n"
         "第三步，输入「纸」。甲骨、金文、战国三格是缺环，写的是：汉代后起字，本无此形。\n"
         "这不是没查到，是这个字在那个时代还不存在。\n"
         "如果还有时间：刷新一次看纸背换了一幅，或者输入「水」看一个六期都有的字。")

# ══════════════════════════════════════════════════════════
# 17 分工                       13:10–13:35
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 17, TOTAL)
y = head(s, "06  分工说明", "按「可独立交付的模块」切，不按行数切")
rows = [
    ["成员", "角色", "具体产出", "参与的迭代轮次"],
    ["成员一（姓名待填）", "数据采集与校验", "三个抓取器、四个数据源、缺环判定规则", "②③④"],
    ["成员二（姓名待填）", "前端与视觉", "六期时间轴、缺环组件、点图看来源、纸背与动效", "①③⑤"],
    ["成员三（姓名待填）", "工程、文档与验收", "部署流水线、性能优化、工作流文档、演示脚本", "③④⑤"],
]
table(s, MARGIN, y + 0.10, W - 2 * MARGIN, [2.45, 2.25, 4.65, 1.85], rows,
      fs=12, hdr_fs=12, row_h=0.66, hdr_h=0.42)
callout(s, MARGIN, y + 0.42 + 0.66 * 3 + 0.26, W - 2 * MARGIN,
        "三人共同参与每一轮的 Prompt 与验收：谁提需求、谁核验结果，都在 Prompt Log 里留痕。",
        h=0.62, fs=12.5, color=INK_SOFT)
callout(s, MARGIN, y + 0.42 + 0.66 * 3 + 1.00, W - 2 * MARGIN,
        "提示：把姓名替换成实际成员；如为个人作业，可改为「个人承担，按模块分阶段推进」。",
        h=0.52, fs=11, color=MUTED)
notes(s, "【13:10–13:35｜分工】\n"
         "分工按能独立交付的模块切：数据、前端、工程与文档，最后一列是各自主要参与的迭代轮次。\n"
         "要说清楚：每一轮的 Prompt 和验收是三个人一起做的。\n"
         "（此处按实际成员替换姓名与贡献。）")

# ══════════════════════════════════════════════════════════
# 18 结语                       13:35–13:50
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 18, TOTAL)
y = head(s, "06  结语", "做到了什么 / 没做什么")

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

callout(s, MARGIN, H - 1.86, W - 2 * MARGIN,
        "它不是一张好看的演变图，而是一条能被逐条追溯、并且敢于留白的证据链。",
        h=0.72, fs=16, color=SEAL)
tf = textbox(s, MARGIN, H - 0.92, W - 2 * MARGIN, 0.34)
para(tf, "谢谢，欢迎提问。线上地址：https://otherhello.github.io/hanzi-timeline/",
     size=12.5, color=MUTED, first=True, align=PP_ALIGN.CENTER)
notes(s, "【13:35–13:50｜结语】\n"
         "最后一句总结：我们做到了每条都能点回来源，也敢说这几格真的没有。\n"
         "局限写在右边：已核对是库内可溯，不是逐件核原拓；楷书还依赖一个站；甲骨释读没做二次校验。\n"
         "这三点如果老师追问，我照实答。谢谢，欢迎提问。")

# ══════════════════════════════════════════════════════════
# 19 附录                       （不占讲解时间）
# ══════════════════════════════════════════════════════════
s = new_slide()
page_no(s, 19, TOTAL)
y = head(s, "附录（不占讲解时间）", "Prompt Log 全表：过程性评价依据")
rows = [
    ["迭代", "我们怎么问（原文摘要）", "AI 给了什么", "确认 / 修订 / 版本变化"],
    ["1 · 意图", "「输入一个字，按六期展示，每字形挂实物出处与核对状态，无实例显示缺环，绝不用后世字形倒填，也不用示意图冒充实物」",
     "React+Vite+TS 单页、纵向瀑布流、GlyphInstance 数据模型与三态",
     "确认三态与缺环语义；否决「自动搜图填满六期」；版本 v0 → v1（假数据骨架）"],
    ["2 · 方案", "「你列的这些源，哪些能程序化取数？给出请求方式、返回结构、注意事项」",
     "列出 Wikisource、Commons、wiktionary、zdic、zi.tools 等候选",
     "实测砍掉四个：zdic 403、zi.tools 是 SPA、小學堂是 frameset；定 Wikisource + 港中大 + 词典网"],
    ["3 · 增量", "「这一轮只做小篆：抓《說文》、生成 8 个字的 characters.ts、页面能渲染出图」",
     "只改数据生成器与一个 GlyphSource 适配器",
     "v1 → v2：先假数据跑通页面再接真源；每轮 tsc + build + 线上验收"],
    ["4 · 调试", "「HTTP 429」/「200 但 0 字节」/「部署后图 404」/「test.ts 未使用变量报错」",
     "退避续抓、同站 Referer、相对路径、删未用变量",
     "四条都复现验证，并写进脚本注释与 DEPLOY.md"],
    ["5 · 审美", "「背景太糊，要能看出字的模样但不能抢正文」/「首屏加载慢」",
     "blur / 透明度 / 罩层参数；WebP + 烘焙模糊方案",
     "blur 26→9、.56→.78、中轴压纸色；1471KB→124KB（−92%）"],
]
table(s, MARGIN, y + 0.10, W - 2 * MARGIN, [0.90, 5.20, 3.05, 3.60], rows,
      fs=8.5, hdr_fs=9.5, row_h=0.92, hdr_h=0.32)
notes(s, "【附录｜不占讲解时间】\n"
         "这是同一组 Prompt 的完整版，含每轮版本变化（v0→v1→v2）。\n"
         "只在老师追问「你们具体怎么问的」时翻到这一页。")

os.makedirs(HERE, exist_ok=True)
prs.save(OUT)
print("saved:", OUT)
print("slides:", len(prs.slides._sldIdLst))
