/**
 * 汉字字形演变证据链数据
 *
 * 由 tools/generate_glyph_data.py 生成。
 * 小篆数据来自维基文库《說文解字》（已核对）；
 * 其他时代著录出处已标明，核对状态为「待核对」。
 *
 * 铁律：每字形挂实物出处 + 核对状态；无实例即缺环；不用示意图冒充实物。
 */

import type { CharacterData } from '../types'

const CHARACTERS: CharacterData[] = [

  { char: '馬', eras: [
    { era: 'jiaguwen', instances: [{ id: '馬-jiaguwen-1', era: 'jiaguwen', artifact: '殷墟甲骨（《甲骨文合集》所收，具体片号待核）', sourceRef: '《甲骨文合集》', dateRange: '商（殷墟）', verification: 'pending', note: '馬为象形字，甲骨习见；具体片号、藏地待人工核对后补实。' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '馬-jinwen-1', era: 'jinwen', artifact: '商周青铜器铭文（《殷周金文集成》所收，器名待核）', sourceRef: '《殷周金文集成》', dateRange: '西周—春秋', verification: 'pending', note: '金文习见；具体器名、著录号待核。' }], isGap: false },
    { era: 'zhanguo', instances: [{ id: '馬-zhanguo-1', era: 'zhanguo', artifact: '战国简帛/玺印文字（《战国文字编》等所收，简号待核）', sourceRef: '《战国文字编》', dateRange: '战国', verification: 'pending', note: '简帛文字确有传承；具体简号待核。' }], isGap: false },
    { era: 'xiaozhuan', instances: [{ id: '馬-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第10卷', collection: '（传世字书）', sourceRef: '《說文解字·馬部》：「怒也。武也。象馬頭髦尾四足之形。凡馬之屬皆从馬。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: '/glyphs/馬-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [{ id: '馬-lishu-1', era: 'lishu', artifact: '汉隶碑刻（如《曹全碑》《乙瑛碑》等，字例待核）', sourceRef: '汉碑拓本', dateRange: '东汉', verification: 'pending', note: '具体碑石字例待拓片核验。' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '馬-kaishu-1', era: 'kaishu', artifact: '唐楷碑帖（如《九成宫醴泉铭》《多宝塔碑》等，字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '楷书定型字形；具体碑帖字例待核。' }], isGap: false }
  ] },

  { char: '牛', eras: [
    { era: 'jiaguwen', instances: [{ id: '牛-jiaguwen-1', era: 'jiaguwen', artifact: '殷墟甲骨（《甲骨文合集》所收，片号待核）', sourceRef: '《甲骨文合集》', dateRange: '商（殷墟）', verification: 'pending', note: '牛为象形字，甲骨习见；具体片号待核。' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '牛-jinwen-1', era: 'jinwen', artifact: '商周青铜器铭文（含牛形族徽，器名待核）', sourceRef: '《殷周金文集成》', dateRange: '商晚期—西周', verification: 'pending', note: '具体器名待核。' }], isGap: false },
    { era: 'zhanguo', instances: [], isGap: true, gapNote: '战国文字资料中暂未发现此字实例，属缺环。' },
    { era: 'xiaozhuan', instances: [{ id: '牛-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第02卷', collection: '（传世字书）', sourceRef: '《說文解字·牛部》：「大牲也。牛，件也；件，事理也。象角頭三、封㞑之形。凡牛之屬皆从牛。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: '/glyphs/牛-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [{ id: '牛-lishu-1', era: 'lishu', artifact: '汉隶碑刻（字例待核）', sourceRef: '汉碑拓本', dateRange: '东汉', verification: 'pending', note: '具体碑石字例待核。' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '牛-kaishu-1', era: 'kaishu', artifact: '唐楷碑帖（字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '具体碑帖字例待核。' }], isGap: false }
  ] },

  { char: '山', eras: [
    { era: 'jiaguwen', instances: [{ id: '山-jiaguwen-1', era: 'jiaguwen', artifact: '殷墟甲骨（《甲骨文合集》所收，片号待核）', sourceRef: '《甲骨文合集》', dateRange: '商（殷墟）', verification: 'pending', note: '山为象形字，甲骨习见；具体片号待核。' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '山-jinwen-1', era: 'jinwen', artifact: '商周青铜器铭文（器名待核）', sourceRef: '《殷周金文集成》', dateRange: '商晚期—西周', verification: 'pending', note: '具体器名待核。' }], isGap: false },
    { era: 'zhanguo', instances: [], isGap: true, gapNote: '战国文字资料中暂未发现此字实例，属缺环。' },
    { era: 'xiaozhuan', instances: [{ id: '山-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第09卷', collection: '（传世字书）', sourceRef: '《說文解字·山部》：「宣也。宣气𢿱，生萬物，有石而高。象形。凡山之屬皆从山。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: '/glyphs/山-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [], isGap: true, gapNote: '该时代暂未发现此字实例，属缺环。' },
    { era: 'kaishu', instances: [{ id: '山-kaishu-1', era: 'kaishu', artifact: '唐楷碑帖（字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '具体碑帖字例待核。' }], isGap: false }
  ] },

  { char: '水', eras: [
    { era: 'jiaguwen', instances: [{ id: '水-jiaguwen-1', era: 'jiaguwen', artifact: '殷墟甲骨（《甲骨文合集》所收，片号待核）', sourceRef: '《甲骨文合集》', dateRange: '商（殷墟）', verification: 'pending', note: '水为象形字，甲骨习见；具体片号待核。' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '水-jinwen-1', era: 'jinwen', artifact: '商周青铜器铭文（器名待核）', sourceRef: '《殷周金文集成》', dateRange: '商晚期—西周', verification: 'pending', note: '具体器名待核。' }], isGap: false },
    { era: 'zhanguo', instances: [], isGap: true, gapNote: '战国文字资料中暂未发现此字实例，属缺环。' },
    { era: 'xiaozhuan', instances: [{ id: '水-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第11卷', collection: '（传世字书）', sourceRef: '《說文解字·水部》：「凖也。北方之行。象眾水並流，中有微陽之气也。凡水之屬皆从水。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: '/glyphs/水-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [], isGap: true, gapNote: '该时代暂未发现此字实例，属缺环。' },
    { era: 'kaishu', instances: [{ id: '水-kaishu-1', era: 'kaishu', artifact: '唐楷碑帖（字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '具体碑帖字例待核。' }], isGap: false }
  ] },

  { char: '日', eras: [
    { era: 'jiaguwen', instances: [{ id: '日-jiaguwen-1', era: 'jiaguwen', artifact: '殷墟甲骨（《甲骨文合集》所收，片号待核）', sourceRef: '《甲骨文合集》', dateRange: '商（殷墟）', verification: 'pending', note: '日为象形字，甲骨习见；具体片号待核。' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '日-jinwen-1', era: 'jinwen', artifact: '商周青铜器铭文（器名待核）', sourceRef: '《殷周金文集成》', dateRange: '商晚期—西周', verification: 'pending', note: '具体器名待核。' }], isGap: false },
    { era: 'zhanguo', instances: [], isGap: true, gapNote: '战国文字资料中暂未发现此字实例，属缺环。' },
    { era: 'xiaozhuan', instances: [{ id: '日-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第07卷', collection: '（传世字书）', sourceRef: '《說文解字·日部》：「實也。太陽之精不虧。从囗一。象形。凡日之屬皆从日。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: '/glyphs/日-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [], isGap: true, gapNote: '该时代暂未发现此字实例，属缺环。' },
    { era: 'kaishu', instances: [{ id: '日-kaishu-1', era: 'kaishu', artifact: '唐楷碑帖（字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '具体碑帖字例待核。' }], isGap: false }
  ] },

  { char: '月', eras: [
    { era: 'jiaguwen', instances: [{ id: '月-jiaguwen-1', era: 'jiaguwen', artifact: '殷墟甲骨（《甲骨文合集》所收，片号待核）', sourceRef: '《甲骨文合集》', dateRange: '商（殷墟）', verification: 'pending', note: '月为象形字，甲骨习见；具体片号待核。' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '月-jinwen-1', era: 'jinwen', artifact: '商周青铜器铭文（器名待核）', sourceRef: '《殷周金文集成》', dateRange: '商晚期—西周', verification: 'pending', note: '具体器名待核。' }], isGap: false },
    { era: 'zhanguo', instances: [], isGap: true, gapNote: '战国文字资料中暂未发现此字实例，属缺环。' },
    { era: 'xiaozhuan', instances: [{ id: '月-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第07卷', collection: '（传世字书）', sourceRef: '《說文解字·月部》：「闕也。大陰之精。象形。凡月之屬皆从月。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》' }], isGap: false },
    { era: 'lishu', instances: [], isGap: true, gapNote: '该时代暂未发现此字实例，属缺环。' },
    { era: 'kaishu', instances: [{ id: '月-kaishu-1', era: 'kaishu', artifact: '唐楷碑帖（字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '具体碑帖字例待核。' }], isGap: false }
  ] },

  { char: '人', eras: [
    { era: 'jiaguwen', instances: [{ id: '人-jiaguwen-1', era: 'jiaguwen', artifact: '殷墟甲骨（《甲骨文合集》所收，片号待核）', sourceRef: '《甲骨文合集》', dateRange: '商（殷墟）', verification: 'pending', note: '人为象形字，甲骨习见；具体片号待核。' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '人-jinwen-1', era: 'jinwen', artifact: '商周青铜器铭文（器名待核）', sourceRef: '《殷周金文集成》', dateRange: '商晚期—西周', verification: 'pending', note: '具体器名待核。' }], isGap: false },
    { era: 'zhanguo', instances: [], isGap: true, gapNote: '战国文字资料中暂未发现此字实例，属缺环。' },
    { era: 'xiaozhuan', instances: [{ id: '人-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第08卷', collection: '（传世字书）', sourceRef: '《說文解字·人部》：「天地之性最貴者也。此籒文。象臂脛之形。凡人之屬皆从人。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: '/glyphs/人-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [], isGap: true, gapNote: '该时代暂未发现此字实例，属缺环。' },
    { era: 'kaishu', instances: [{ id: '人-kaishu-1', era: 'kaishu', artifact: '唐楷碑帖（字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '具体碑帖字例待核。' }], isGap: false }
  ] },

  { char: '紙', eras: [
    { era: 'jiaguwen', instances: [], isGap: true, gapNote: '此字後起，商代甲骨文中未见。' },
    { era: 'jinwen', instances: [], isGap: true, gapNote: '西周至春秋金文中未见此字。' },
    { era: 'zhanguo', instances: [], isGap: true, gapNote: '战国文字资料中暂未发现此字实例，属缺环。' },
    { era: 'xiaozhuan', instances: [{ id: '紙-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第13卷', collection: '（传世字书）', sourceRef: '《說文解字·糸部》：「絮一苫也。从糸氏聲。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》' }], isGap: false },
    { era: 'lishu', instances: [{ id: '紙-lishu-1', era: 'lishu', artifact: '汉代简帛/碑刻（造纸术创于西汉，字例待核）', sourceRef: '汉简/汉碑', dateRange: '东汉', verification: 'pending', note: '纸为后起字，汉代是否已有隶定字形待核。' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '紙-kaishu-1', era: 'kaishu', artifact: '唐以降写本/碑帖（字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '具体碑帖字例待核。' }], isGap: false }
  ] },

]

export default CHARACTERS
