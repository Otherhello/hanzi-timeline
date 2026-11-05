"""生成《项目工作流文档》DOCX，供课程报告与 PPT 制作用。"""
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   '汉字字形演变证据链时间轴-项目工作流.docx')

INK = RGBColor(0x23, 0x20, 0x1A)
SEAL = RGBColor(0xA6, 0x3A, 0x2B)
GREY = RGBColor(0x5B, 0x55, 0x4A)

BODY_CN = '宋体'
HEAD_CN = '黑体'
LATIN = 'Times New Roman'
LATIN_HEAD = 'Arial'


def _font(run, cn, latin, size=None, bold=None, color=None, italic=None):
    run.font.name = latin
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rf)
    rf.set(qn('w:ascii'), latin)
    rf.set(qn('w:hAnsi'), latin)
    rf.set(qn('w:eastAsia'), cn)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


def para(doc, text='', size=10.5, bold=False, color=INK, align=None,
         before=0, after=5, indent=None, cn=BODY_CN, latin=LATIN, italic=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing = 1.45
    if indent is not None:
        pf.first_line_indent = Cm(indent)
    if align is not None:
        p.alignment = align
    if text:
        r = p.add_run(text)
        _font(r, cn, latin, size, bold, color, italic)
    return p


def h1(doc, text, number=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(16)
    pf.space_after = Pt(8)
    pf.keep_with_next = True
    if number:
        r0 = p.add_run(number + '  ')
        _font(r0, HEAD_CN, LATIN_HEAD, 15, True, SEAL)
    r = p.add_run(text)
    _font(r, HEAD_CN, LATIN_HEAD, 15, True, INK)
    # 下边框
    from docx.oxml import OxmlElement
    pPr = p._element.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), 'A3874F')
    pbdr.append(bottom)
    pPr.append(pbdr)
    return p


def h2(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(11)
    pf.space_after = Pt(5)
    pf.keep_with_next = True
    r = p.add_run(text)
    _font(r, HEAD_CN, LATIN_HEAD, 12, True, INK)
    return p


def bullet(doc, text, lead=None, level=0):
    p = doc.add_paragraph(style='List Bullet')
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.4
    if level:
        pf.left_indent = Cm(0.75 + 0.75 * level)
    if lead:
        r = p.add_run(lead)
        _font(r, BODY_CN, LATIN, 10.5, True, INK)
    r2 = p.add_run(text)
    _font(r2, BODY_CN, LATIN, 10.5, False, INK)
    return p


def note(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(8)
    pf.left_indent = Cm(0.5)
    pf.line_spacing = 1.4
    r = p.add_run(text)
    _font(r, BODY_CN, LATIN, 9.5, False, GREY, italic=True)
    return p


def table(doc, headers, rows, widths=None, size=9):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ''
        p = hdr[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        _font(r, HEAD_CN, LATIN_HEAD, size, True, RGBColor(0xFF, 0xFF, 0xFF))
        shd = hdr[i]._tc.get_or_add_tcPr().makeelement(
            qn('w:shd'), {qn('w:val'): 'clear', qn('w:fill'): '5B554A'})
        hdr[i]._tc.get_or_add_tcPr().append(shd)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ''
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(str(val))
            _font(r, BODY_CN, LATIN, size, False, INK)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Cm(w)
    # 表后留白
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def build():
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.2)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.4)
    sec.right_margin = Cm(2.4)

    normal = doc.styles['Normal']
    normal.font.name = LATIN
    normal.font.size = Pt(10.5)
    normal.element.rPr.rFonts.set(qn('w:eastAsia'), BODY_CN)

    # ---------------- 封面区 ----------------
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(30)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run('汉字字形演变')
    _font(r, HEAD_CN, LATIN_HEAD, 26, True, INK)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run('证据链时间轴')
    _font(r, HEAD_CN, LATIN_HEAD, 26, True, INK)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(28)
    r = p.add_run('项目工作流文档 · 供课程报告与 PPT 制作使用')
    _font(r, BODY_CN, LATIN, 12, False, GREY)

    table(doc,
          ['项目', '内容'],
          [['一句话定位', '输入一个字，给出它从甲骨文到楷书六个时代的真实字形；'
                        '每个字形都挂实物出处与核对状态，没有实例的就明写「缺环」。'],
           ['技术栈', 'React + Vite + TypeScript（纯前端静态站），Python 负责抓取与生成'],
           ['数据规模', '28 字 · 246 个字形实例 · 245 张实物字形图（另有纸背名帖 7 幅）'],
           ['线上地址', 'https://otherhello.github.io/hanzi-timeline/'],
           ['文档用途', '理解系统怎么跑起来、每个操作要做什么，并可直接拆成 PPT 分页']],
          widths=[3.0, 12.6], size=9.5)

    doc.add_page_break()

    # ---------------- 一、速览 ----------------
    h1(doc, '一页速览', '零')

    para(doc, '这个项目要回答一个问题：一个汉字，在三千年的书写史里，'
              '分别在甲骨、青铜、竹简帛书、秦篆、汉隶、唐楷上长什么样？'
              '而这些样子，能不能指出它到底来自哪一件实物？')

    h2(doc, '三个关键数字')
    bullet(doc, '—— 每期都取真实字形，不靠字体渲染。', lead='28 个字')
    bullet(doc, '—— 平均每字近 9 个，分属六个时代。', lead='246 个字形实例')
    bullet(doc, '—— 其中 245 条带有实物出处与可点开的来源页。', lead='245 张实物字形图')

    h2(doc, '一句话讲清系统怎么跑')
    para(doc, '三个公开字库（维基文库、香港中文大学《漢語多功能字庫》、词典网书法字典）'
              '→ 三个 Python 抓取脚本把字形图与著录信息落到本地 JSON 与图片目录 '
              '→ 一个生成脚本把三份原料汇编成前端数据文件 '
              '→ React 静态站按六期纵向渲染 '
              '→ GitHub Actions 自动构建并发布到 GitHub Pages。')
    note(doc, '整条流水线的关键性质：任何一个源缺数据，系统会自动降级为「缺环」，'
              '流水线不会中断，也绝不会拿别的时代字形来顶替。')

    h2(doc, '报告/答辩里最该被记住的一句话')
    para(doc, '「它不是一个好看的汉字字体展示页，而是一条可以被逐条追溯、'
              '并且敢于留白的证据链。」', bold=True, color=SEAL, indent=0.75)

    # ---------------- 二、设计原则 ----------------
    h1(doc, '三条铁律：为什么这样做，而不是那样做', '一')

    para(doc, '项目从第一行代码起就守三条规矩。它们不是口号，每一条都在系统里有对应的实现。')

    table(doc,
          ['铁律', '含义', '系统里怎么落实'],
          [['① 每个字形必须挂实物出处',
            '说清是「哪一片甲骨、哪一件青铜器、哪一块碑、哪一件写本」。',
            '每条实例都带 artifact（器名/篇名）、catalogId（《合集》《集成》编号或卷次）、'
            'sourceRef（著录文字）、sourceUrl（可点开的来源页）。'],
           ['② 无实例就是缺环，绝不倒填',
            '某期找不到可信实例，就明写「缺环」并说明原因，'
            '不用后世字形冒充早期字形。',
            '数据结构里有 isGap 与 gapNote；生成器遇到源缺失自动产出缺环，'
            '不抛错、不静默补图。'],
           ['③ 不用示意图冒充实物',
            '拒绝用字体文件「画」一个看起来像甲骨文的字。',
            '所有图都来自馆藏扫描、拓本或传世字书，'
            '未接入时页面显示「实物拓图待接入」空帧，而不是占位图。']],
          widths=[3.4, 6.0, 6.2], size=9)

    para(doc, '这三条决定了项目的取舍：宁可版面留白、宁可缺三格，也不给一条假证据。'
              '这也是它区别于普通「字形演变图」的地方。')

    # ---------------- 三、系统运行逻辑 ----------------
    h1(doc, '系统运行逻辑：一条从源到页面的流水线', '二')

    para(doc, '整条链路分六段，每段只做一件事，段与段之间用文件交接，'
              '所以任何一段都可以单独重跑。')

    table(doc,
          ['环节', '做什么', '产出/交接物'],
          [['1. 源', '三个公开字库，分别对应不同时代', '网页与图片接口'],
           ['2. 抓取', '三个 Python 脚本按字抓取、限速、断点续抓', 'data/*.json + public/glyphs/*'],
           ['3. 缓存', '原始 wikitext、字库清单、图片全部落盘', '可重复运行，不重复打源站'],
           ['4. 生成', '把三份原料按字、按时代汇编，自动补缺环', 'src/data/characters.ts'],
           ['5. 前端', 'React 按六期纵向渲染，缺环单独渲染', '静态 dist/'],
           ['6. 部署', 'push 到 main，GitHub Actions 构建并发布', 'GitHub Pages']],
          widths=[2.2, 7.2, 6.2], size=9)

    note(doc, '设计要点：抓取与生成彻底分离。抓取器只负责「把源上的东西如实搬下来」，'
              '不判断真假；生成器只负责「按规则组装」，不联网。'
              '这样换源、加字、改版式都不会互相牵连。')

    # ---------------- 四、数据源 ----------------
    h1(doc, '四个数据源与三个抓取器', '三')

    para(doc, '六个时代里，小篆、甲骨、金文、战国、隶都有权威字库可查；'
              '楷书则要落到具体碑帖上。四个源的覆盖如下。')

    table(doc,
          ['数据源', '覆盖时代', '取数方式', '关键坑（必须知道）'],
          [['维基文库《說文解字》', '小篆', 'MediaWiki API 抓 15 卷全文，'
            '解析每个字头的部首与释义', '有小篆字头矢量图，但并非每字都有'],
           ['香港中文大学《漢語多功能字庫》', '甲骨、金文、战国、隶（簡帛）',
            '逐字打开字页，解析分时代字形表', '图片端点强制同站 Referer，'
            '否则返回 200 但 0 字节'],
           ['词典网·书法字典', '楷书（历代碑帖）', '逐字打开字页，抓书家+碑帖+图片',
            'https 证书已过期，只能走 http'],
           ['维基共享资源', '小篆矢量图、纸背名帖', 'Commons API 检索与缩略图',
            '原文件会 429 限流，须改用缩略图或退避重试']],
          widths=[4.2, 3.4, 4.4, 3.6], size=8.5)

    h2(doc, '三个抓取器的分工')
    bullet(doc, 'fetch_shuowen.py —— 抓《說文解字》15 卷并解析出 7338 字的索引。',
           lead='')
    bullet(doc, 'fetch_hku_glyphs.py —— 按字抓港中大四期字形（甲骨/金文/战国/隶），'
                '下载图片并校验文件头。')
    bullet(doc, 'fetch_kaishu_glyphs.py —— 按字抓词典网楷书，'
                '按「书家 + 碑帖」去重择优，并裁掉底部水印。')

    note(doc, '工程上踩过并解决的坑，都在脚本里有注释：429 限流要退避重试、'
              '全角括号导致正则漏匹配、表格式卷与行格式卷要分开解析、'
              '深色拓本要反白、水印图要排除。这些细节是「能不能长期跑」的区别。')

    # ---------------- 五、数据模型 ----------------
    h1(doc, '数据模型与「核对状态」的真实含义', '四')

    para(doc, '一条字形实例（GlyphInstance）就是一条证据，字段如下。')

    table(doc,
          ['字段', '含义'],
          [['era', '所属时代：甲骨文 / 金文 / 战国 / 小篆 / 隶书 / 楷书'],
           ['artifact / catalogId', '实物名与编号（如《甲骨文合集》某号、《殷周金文集成》某号、某碑某卷）'],
           ['sourceRef / sourceUrl', '著录文字与该图的来源页（可点开）'],
           ['dateRange / collection', '年代范围与收藏单位'],
           ['imageSrc', '字形图相对路径；没有图就留空，前端显示空帧'],
           ['verification / verifier', '核对状态与核者（哪个字库/哪本字书）'],
           ['note / isGap + gapNote', '补充说明；缺环单独用 isGap 与说明文字表达']],
          widths=[4.0, 11.6], size=9)

    h2(doc, '核对状态的语义（答辩重点）')
    table(doc,
          ['状态', '准确含义', '当前数量'],
          [['已核对', '图与出处取自权威字库或馆藏，来源页可点开、可机器复核。'
                      '注意：这表示「库内可溯」，不等于「已逐件人工核对原拓」。', '245'],
           ['待核对', '有实物著录但缺图，或需要人工再核。', '1'],
           ['缺环', '该时代确实没有可信实例。'
                    '其中「紙」的甲骨/金文/战国三格属于「汉代后起字，本无此形」，'
                    '是缺环而非资料不足。', '5']],
          widths=[2.4, 10.4, 2.8], size=9)

    note(doc, '把这一层说清楚，比把字数做大更重要：大规模之后，'
              '「每条都能点开来源」才是可信度的基础。')

    # ---------------- 六、生成流水线 ----------------
    h1(doc, '生成流水线与日常操作', '五')

    para(doc, '日常只有两种操作：一种是「加字」，一种是「改样式」。加字不需要写代码。')

    h2(doc, '加一个字的完整步骤')
    table(doc,
          ['步骤', '操作', '说明'],
          [['1', '在 scripts 的字表里加一个字', '三个抓取器与生成器共用一份字表'],
           ['2', '跑港中大抓取', '得到甲骨/金文/战国/隶字形与著录'],
           ['3', '跑词典网抓取', '得到楷书碑帖图与书家、碑帖名'],
           ['4', '跑生成脚本', '汇编成 characters.ts；缺的一律自动变缺环'],
           ['5', '构建并 push', 'Actions 自动发布']],
          widths=[1.4, 6.6, 7.6], size=9)

    h2(doc, '为什么可以「零人工」')
    para(doc, '早期为了兜住个别字，写过一大张人工审校表；后来发现 168 个「字×时代」格子里，'
              '只有 1 格还真的在用人工数据。'
              '现在的规则是：默认按源自动生成，缺口自动成缺环，'
              '只有「本无此字」这类常识判断才写进极少数的手写说明。')

    # ---------------- 七、前端 ----------------
    h1(doc, '前端结构与关键交互', '六')

    para(doc, '页面是一条纵向瀑布流：从甲骨文一路向下到楷书，时代名竖排，'
              '左侧一条青铜金色细线做时间轴。')

    table(doc,
          ['交互', '实现要点'],
          [['逐期展示', '六个时代卡片顺序渲染；有实例就出图，没实例就出缺环'],
           ['缺环', '圆形「缺」印章 + 一句原因说明，视觉上明确是「空」而不是「漏」'],
           ['点图看来源', '图片包在链接里，新标签打开该字形的来源页（字库字页 / 碑帖页）'],
           ['纸背', '每次进入随机取一幅历代名帖，重度虚化后作底纹；'
                    '中间正文区压纸色、四周留出字形'],
           ['来源标注', '页脚与题识标明三个数据库，与「可追溯」的定位一致']],
          widths=[3.2, 12.4], size=9)

    note(doc, '纸背做了区分度处理：中轴用径向纸色压淡以保证正文对比度，'
              '左右留白处保留清晰的字形，做到「看得到字、但不打扰」。')

    # ---------------- 八、部署 ----------------
    h1(doc, '部署流水线', '七')

    para(doc, '项目是纯静态站，托管在 GitHub Pages，push 即发布。')

    table(doc,
          ['环节', '配置'],
          [['构建', 'pnpm@9 + Node 20，执行 tsc 类型检查后 vite build'],
           ['发布', 'upload-pages-artifact 上传 dist，再由 deploy-pages 发布'],
           ['触发', 'push 到 main 分支；也可在 Actions 页手动触发'],
           ['路径', 'vite base 设为相对路径，因此任何仓库名/子路径都能跑']],
          widths=[2.6, 13.0], size=9)

    h2(doc, '三个真实踩过的坑')
    bullet(doc, '图片地址若带前导斜杠，会被解析到域名根而 404 —— 必须用相对路径。')
    bullet(doc, 'CI 里 tsc 会把「声明了但没用到」的变量当错误，本地用 vite 跑则看不出来。')
    bullet(doc, '本地 pnpm 版本较新时会有构建脚本被忽略的告警，CI 里锁定 pnpm@9 即可规避。')

    # ---------------- 九、成果数据 ----------------
    h1(doc, '当前成果数据', '八')

    table(doc,
          ['时代', '实例数', '说明'],
          [['甲骨文', '27', '《甲骨文合集》编号一一对应'],
           ['金文', '63', '多为《殷周金文集成》著录，商、西周、春秋分列'],
           ['战国文字', '25', '含战国金文与睡虎地秦简（战国晚期秦系）'],
           ['小篆', '28', '据《說文解字》字头，附《康熙字典》字形库图'],
           ['隶书', '28', '简帛写本（馬王堆、睡虎地等）'],
           ['楷书', '75', '历代碑帖，附书家与碑帖名'],
           ['待核对', '1', '「紙」楷书（书法字典无此字页）'],
           ['缺环', '5', '貝·战国、文·战国；紙·甲骨/金文/战国']],
          widths=[2.6, 2.6, 10.4], size=9)

    para(doc, '另有备好的字库池：說文索引已收录 7338 字，'
              '港中大与词典网均可按字查询，扩字只是跑一遍流水线的时间成本。')

    # ---------------- 十、性能 ----------------
    h1(doc, '性能优化的两个动作', '九')

    table(doc,
          ['问题', '处理', '效果'],
          [['纸背图偏大、首屏偏慢',
            '图片转 WebP，并把模糊在构建期烘焙进像素',
            '7 幅合计 1471KB → 124KB（−92%），单幅均 17.7KB'],
           ['对整屏固定层做运行时高斯模糊',
            '去掉 filter: blur()，只保留低成本的调色',
            '滚动不再每帧重算模糊']],
          widths=[4.6, 6.4, 4.6], size=9)

    note(doc, '原则：既然最终一定要模糊，就不要把高频细节交给浏览器去下载。')

    # ---------------- 十一、扩展 ----------------
    h1(doc, '可持续扩展的路线', '十')

    para(doc, '如果要把 28 字扩到几百上千字，按这个顺序做，收益最高：')

    bullet(doc, '删掉残余的人工审校表 —— 让加字真正零人工。', lead='① ')
    bullet(doc, '把数据拆成「索引 + 单字 JSON」并懒加载 —— 解开单文件打包的字数天花板。',
           lead='② ')
    bullet(doc, '图片统一 WebP 并限长边 —— 控制仓库体积。', lead='③ ')
    bullet(doc, '增加状态文件与质量闸门 —— 有图必须有来源、缺环必须有说明，'
                '坏数据自动降级为缺环。', lead='④ ')

    para(doc, '分批建议：先 300–500 常用字，跑完看覆盖率报告，'
              '人工只处理失败清单；再上 1000 字以上。')

    # ---------------- 十二、PPT 分页 ----------------
    h1(doc, '附：PPT 分页建议（15 页）', '十一')

    para(doc, '下面这份大纲可以直接对应一套 12–15 分钟的汇报。'
              '每页只放 3–5 条要点，图和数据放右半边。')

    table(doc,
          ['页', '标题', '这一页要讲的话'],
          [['1', '封面', '一句话定位 + 线上地址二维码'],
           ['2', '问题', '输入一个字，能不能说清它在六个时代分别长什么样、出自哪件实物？'],
           ['3', '三条铁律', '挂出处 / 缺环不倒填 / 示意图不算实物 —— 项目的底线'],
           ['4', '整体架构', '六段流水线一张图：源 → 抓取 → 缓存 → 生成 → 前端 → 部署'],
           ['5', '数据源', '四个源的覆盖表；为什么楷书非要落到碑帖上'],
           ['6', '抓取器', '三个脚本各管一段；限速、退避、断点续抓'],
           ['7', '踩坑集', '港中大 Referer、词典网证书过期、Wikimedia 限流 —— 讲工程味'],
           ['8', '数据模型', '一条证据有哪些字段；缺环如何表达'],
           ['9', '核对状态的语义', '「库内可溯」不等于「人工核过」—— 诚实度这一页最重要'],
           ['10', '成品展示', '一张整页截图：六期纵向瀑布流 + 缺环'],
           ['11', '交互演示', '点图跳来源、纸背随机名帖（各一张图）'],
           ['12', '成果数据', '28 字 / 246 实例 / 245 图 / 5 缺环 的统计表'],
           ['13', '性能与工程', '图片 −92%、烘焙模糊、相对路径部署'],
           ['14', '可持续扩展', '四步改造 + 分批路线，回答「能不能做大」'],
           ['15', '结论与局限', '已做到的与尚未做到的，明确列出局限']],
          widths=[1.0, 3.6, 11.0], size=8.5)

    h2(doc, '答辩时最稳的三句话')
    para(doc, '① 每一条字形都能点开来源，缺的地方我明确标成了缺环；')
    para(doc, '② 规模不是靠人工堆出来的，是一条可重跑的流水线；')
    para(doc, '③ 「已核对」指的是库内可溯，我没有夸大成人手核验过原拓。')

    doc.save(OUT)
    print('saved:', OUT)


if __name__ == '__main__':
    build()
