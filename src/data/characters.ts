/**
 * 汉字字形演变证据链数据
 *
 * 由 tools/generate_glyph_data.py 生成。
 * 小篆：维基文库《說文解字》（已核对）。
 * 甲骨/金文/战国/隶：香港中文大学《漢語多功能字庫》字形（已核对，附器名/合集号）。
 * 楷书：词典网·书法字典所收历代碑帖（已核对，附碑帖名/书家）。
 * 其余时代著录出处已标明，核对状态为「待核对」。
 *
 * 铁律：每字形挂实物出处 + 核对状态；无实例即缺环；不用示意图冒充实物。
 */

import type { CharacterData } from '../types'

const CHARACTERS: CharacterData[] = [

  { char: '馬', eras: [
    { era: 'jiaguwen', instances: [{ id: '馬-jiaguwen-1', era: 'jiaguwen', artifact: '甲骨文合集', catalogId: 'CHANT:1630', sourceRef: '《甲骨文合集》（據香港中文大學《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/馬-jiaguwen-1.jpg' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '馬-jinwen-1', era: 'jinwen', artifact: '父辛尊', catalogId: '《殷周金文集成》5749號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '商代', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/馬-jinwen-1.jpg' }, { id: '馬-jinwen-2', era: 'jinwen', artifact: '小臣守', catalogId: '《殷周金文集成》4179號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '西周', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/馬-jinwen-2.jpg' }, { id: '馬-jinwen-3', era: 'jinwen', artifact: '大馬簠', catalogId: '《殷周金文集成》4505號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '春秋早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/馬-jinwen-3.jpg' }], isGap: false },
    { era: 'zhanguo', instances: [{ id: '馬-zhanguo-1', era: 'zhanguo', artifact: '噩君車節', catalogId: '《殷周金文集成》12110號', sourceRef: '《殷周金文集成·戰國器》（據香港中文大學《漢語多功能字庫》）', dateRange: '戰國', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/馬-zhanguo-1.jpg' }], isGap: false },
    { era: 'xiaozhuan', instances: [{ id: '馬-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第10卷', collection: '（传世字书）', sourceRef: '《說文解字·馬部》：「怒也。武也。象馬頭髦尾四足之形。凡馬之屬皆从馬。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: 'glyphs/馬-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [{ id: '馬-lishu-1', era: 'lishu', artifact: '馬王堆．足臂十一脈灸經．8', sourceRef: '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/馬-lishu-1.jpg' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '馬-kaishu-1', era: 'kaishu', artifact: '王友度墓志', catalogId: '张即之 書', sourceRef: '《王友度墓志》张即之書', dateRange: '南宋', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/馬-kaishu-1.jpg' }, { id: '馬-kaishu-2', era: 'kaishu', artifact: '曾孟鸣碑', catalogId: '于右任 書', sourceRef: '《曾孟鸣碑》于右任書', dateRange: '近代', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/馬-kaishu-2.jpg' }], isGap: false }
  ] },

  { char: '牛', eras: [
    { era: 'jiaguwen', instances: [{ id: '牛-jiaguwen-1', era: 'jiaguwen', artifact: '甲骨文合集', catalogId: 'CHANT:1545', sourceRef: '《甲骨文合集》（據香港中文大學《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/牛-jiaguwen-1.jpg' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '牛-jinwen-1', era: 'jinwen', artifact: '牛方鼎', catalogId: '《殷周金文集成》1102號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '商代', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/牛-jinwen-1.jpg' }, { id: '牛-jinwen-2', era: 'jinwen', artifact: '牛鼎', catalogId: '《殷周金文集成》1104號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '西周早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/牛-jinwen-2.jpg' }], isGap: false },
    { era: 'zhanguo', instances: [{ id: '牛-zhanguo-1', era: 'zhanguo', artifact: '噩君車節', catalogId: '《殷周金文集成》12112號', sourceRef: '《殷周金文集成·戰國器》（據香港中文大學《漢語多功能字庫》）', dateRange: '戰國', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/牛-zhanguo-1.jpg' }], isGap: false },
    { era: 'xiaozhuan', instances: [{ id: '牛-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第02卷', collection: '（传世字书）', sourceRef: '《說文解字·牛部》：「大牲也。牛，件也；件，事理也。象角頭三、封㞑之形。凡牛之屬皆从牛。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: 'glyphs/牛-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [{ id: '牛-lishu-1', era: 'lishu', artifact: '馬王堆．五十二病方．182', sourceRef: '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/牛-lishu-1.jpg' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '牛-kaishu-1', era: 'kaishu', artifact: '仿颜真卿倪宽赞传', catalogId: '董其昌 書', sourceRef: '《仿颜真卿倪宽赞传》董其昌書', dateRange: '明', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/牛-kaishu-1.jpg' }, { id: '牛-kaishu-2', era: 'kaishu', artifact: '南城咏古诗帖', catalogId: '迺贤 書', sourceRef: '《南城咏古诗帖》迺贤書', dateRange: '元', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/牛-kaishu-2.jpg' }], isGap: false }
  ] },

  { char: '山', eras: [
    { era: 'jiaguwen', instances: [{ id: '山-jiaguwen-1', era: 'jiaguwen', artifact: '甲骨文合集', catalogId: 'CHANT:1218', sourceRef: '《甲骨文合集》（據香港中文大學《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/山-jiaguwen-1.jpg' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '山-jinwen-1', era: 'jinwen', artifact: '母鼎', catalogId: '《殷周金文集成》2026號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '商代', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/山-jinwen-1.jpg' }, { id: '山-jinwen-2', era: 'jinwen', artifact: '山父乙鼎', catalogId: '《殷周金文集成》1561號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '西周早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/山-jinwen-2.jpg' }, { id: '山-jinwen-3', era: 'jinwen', artifact: '奢淲簠', catalogId: '《殷周金文集成》4539號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '春秋早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/山-jinwen-3.jpg' }], isGap: false },
    { era: 'zhanguo', instances: [{ id: '山-zhanguo-1', era: 'zhanguo', artifact: '中山鉞', catalogId: '《殷周金文集成》11758號', sourceRef: '《殷周金文集成·戰國器》（據香港中文大學《漢語多功能字庫》）', dateRange: '戰國中晚期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/山-zhanguo-1.jpg' }], isGap: false },
    { era: 'xiaozhuan', instances: [{ id: '山-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第09卷', collection: '（传世字书）', sourceRef: '《說文解字·山部》：「宣也。宣气𢿱，生萬物，有石而高。象形。凡山之屬皆从山。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: 'glyphs/山-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [{ id: '山-lishu-1', era: 'lishu', artifact: '馬王堆．老子甲本卷後古佚書．336', sourceRef: '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/山-lishu-1.jpg' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '山-kaishu-1', era: 'kaishu', artifact: '南城咏古诗帖', catalogId: '迺贤 書', sourceRef: '《南城咏古诗帖》迺贤書', dateRange: '元', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/山-kaishu-1.jpg' }, { id: '山-kaishu-2', era: 'kaishu', artifact: '富春江石子诗卷', catalogId: '彭年 書', sourceRef: '《富春江石子诗卷》彭年書', dateRange: '明', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/山-kaishu-2.jpg' }], isGap: false }
  ] },

  { char: '水', eras: [
    { era: 'jiaguwen', instances: [{ id: '水-jiaguwen-1', era: 'jiaguwen', artifact: '甲骨文合集', catalogId: 'CHANT:1305', sourceRef: '《甲骨文合集》（據香港中文大學《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/水-jiaguwen-1.jpg' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '水-jinwen-1', era: 'jinwen', artifact: '沈子它蓋（它）', catalogId: '《殷周金文集成》4330號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '西周早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/水-jinwen-1.jpg' }], isGap: false },
    { era: 'zhanguo', instances: [{ id: '水-zhanguo-1', era: 'zhanguo', artifact: '魚鼎匕', catalogId: '《殷周金文集成》980號', sourceRef: '《殷周金文集成·戰國器》（據香港中文大學《漢語多功能字庫》）', dateRange: '戰國', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/水-zhanguo-1.jpg' }], isGap: false },
    { era: 'xiaozhuan', instances: [{ id: '水-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第11卷', collection: '（传世字书）', sourceRef: '《說文解字·水部》：「凖也。北方之行。象眾水並流，中有微陽之气也。凡水之屬皆从水。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: 'glyphs/水-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [{ id: '水-lishu-1', era: 'lishu', artifact: '馬王堆．五十二病方．104', sourceRef: '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/水-lishu-1.jpg' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '水-kaishu-1', era: 'kaishu', artifact: '真草千字文', catalogId: '赵孟頫 書', sourceRef: '《真草千字文》赵孟頫書', dateRange: '元', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/水-kaishu-1.jpg' }, { id: '水-kaishu-2', era: 'kaishu', artifact: '临大字阴符经', catalogId: '潘伯鹰 書', sourceRef: '《临大字阴符经》潘伯鹰書', dateRange: '近代', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/水-kaishu-2.jpg' }, { id: '水-kaishu-3', era: 'kaishu', artifact: '南城咏古诗帖', catalogId: '迺贤 書', sourceRef: '《南城咏古诗帖》迺贤書', dateRange: '元', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/水-kaishu-3.jpg' }], isGap: false }
  ] },

  { char: '日', eras: [
    { era: 'jiaguwen', instances: [{ id: '日-jiaguwen-1', era: 'jiaguwen', artifact: '甲骨文合集', catalogId: 'CHANT:1136', sourceRef: '《甲骨文合集》（據香港中文大學《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/日-jiaguwen-1.jpg' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '日-jinwen-1', era: 'jinwen', artifact: '婦卣', catalogId: '《殷周金文集成》5349號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '商代', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/日-jinwen-1.jpg' }, { id: '日-jinwen-2', era: 'jinwen', artifact: '', catalogId: '《殷周金文集成》3913號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '西周', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/日-jinwen-2.jpg' }, { id: '日-jinwen-3', era: 'jinwen', artifact: '書缶', catalogId: '《殷周金文集成》10008號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '春秋', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/日-jinwen-3.jpg' }], isGap: false },
    { era: 'zhanguo', instances: [{ id: '日-zhanguo-1', era: 'zhanguo', artifact: '噩君舟節', catalogId: '《殷周金文集成》12113號', sourceRef: '《殷周金文集成·戰國器》（據香港中文大學《漢語多功能字庫》）', dateRange: '戰國', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/日-zhanguo-1.jpg' }], isGap: false },
    { era: 'xiaozhuan', instances: [{ id: '日-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第07卷', collection: '（传世字书）', sourceRef: '《說文解字·日部》：「實也。太陽之精不虧。从囗一。象形。凡日之屬皆从日。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: 'glyphs/日-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [{ id: '日-lishu-1', era: 'lishu', artifact: '馬王堆．五十二病方．104', sourceRef: '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/日-lishu-1.jpg' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '日-kaishu-1', era: 'kaishu', artifact: '真草千字文', catalogId: '赵孟頫 書', sourceRef: '《真草千字文》赵孟頫書', dateRange: '元', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/日-kaishu-1.jpg' }, { id: '日-kaishu-2', era: 'kaishu', artifact: '敬斋箴', catalogId: '沈度 書', sourceRef: '《敬斋箴》沈度書', dateRange: '明', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/日-kaishu-2.jpg' }, { id: '日-kaishu-3', era: 'kaishu', artifact: '临大字阴符经', catalogId: '潘伯鹰 書', sourceRef: '《临大字阴符经》潘伯鹰書', dateRange: '近代', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/日-kaishu-3.jpg' }], isGap: false }
  ] },

  { char: '月', eras: [
    { era: 'jiaguwen', instances: [{ id: '月-jiaguwen-1', era: 'jiaguwen', artifact: '甲骨文合集', catalogId: 'CHANT:1153', sourceRef: '《甲骨文合集》（據香港中文大學《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/月-jiaguwen-1.jpg' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '月-jinwen-1', era: 'jinwen', artifact: '乍父乙', catalogId: '《殷周金文集成》4144號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '商代', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/月-jinwen-1.jpg' }, { id: '月-jinwen-2', era: 'jinwen', artifact: '德方鼎', catalogId: '《殷周金文集成》2661號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '西周早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/月-jinwen-2.jpg' }, { id: '月-jinwen-3', era: 'jinwen', artifact: '者鐘', catalogId: '《殷周金文集成》196號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '春秋', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/月-jinwen-3.jpg' }], isGap: false },
    { era: 'zhanguo', instances: [{ id: '月-zhanguo-1', era: 'zhanguo', artifact: '楚王酓盤', catalogId: '《殷周金文集成》10158號', sourceRef: '《殷周金文集成·戰國器》（據香港中文大學《漢語多功能字庫》）', dateRange: '戰國晚期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/月-zhanguo-1.jpg' }], isGap: false },
    { era: 'xiaozhuan', instances: [{ id: '月-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第07卷', collection: '（传世字书）', sourceRef: '《說文解字·月部》：「闕也。大陰之精。象形。凡月之屬皆从月。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: 'glyphs/月-xiaozhuan-1.jpg', note: '小篆圖據《康熙字典》字形庫（說文小篆）' }], isGap: false },
    { era: 'lishu', instances: [{ id: '月-lishu-1', era: 'lishu', artifact: '馬王堆．五十二病方．104', sourceRef: '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/月-lishu-1.jpg' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '月-kaishu-1', era: 'kaishu', artifact: '真草千字文', catalogId: '赵孟頫 書', sourceRef: '《真草千字文》赵孟頫書', dateRange: '元', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/月-kaishu-1.jpg' }, { id: '月-kaishu-2', era: 'kaishu', artifact: '王友度墓志', catalogId: '张即之 書', sourceRef: '《王友度墓志》张即之書', dateRange: '南宋', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/月-kaishu-2.jpg' }, { id: '月-kaishu-3', era: 'kaishu', artifact: '临大字阴符经', catalogId: '潘伯鹰 書', sourceRef: '《临大字阴符经》潘伯鹰書', dateRange: '近代', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/月-kaishu-3.jpg' }], isGap: false }
  ] },

  { char: '人', eras: [
    { era: 'jiaguwen', instances: [{ id: '人-jiaguwen-1', era: 'jiaguwen', artifact: '甲骨文合集', catalogId: 'CHANT:0001', sourceRef: '《甲骨文合集》（據香港中文大學《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/人-jiaguwen-1.jpg' }], isGap: false },
    { era: 'jinwen', instances: [{ id: '人-jinwen-1', era: 'jinwen', artifact: '乍般甗', catalogId: '《殷周金文集成》944號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '商代', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/人-jinwen-1.jpg' }, { id: '人-jinwen-2', era: 'jinwen', artifact: '宜', catalogId: '《殷周金文集成》4320號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '西周早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/人-jinwen-2.jpg' }, { id: '人-jinwen-3', era: 'jinwen', artifact: '黃子鼎', catalogId: '《殷周金文集成》2566號', sourceRef: '《殷周金文集成》（據香港中文大學《漢語多功能字庫》）', dateRange: '春秋早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/人-jinwen-3.jpg' }], isGap: false },
    { era: 'zhanguo', instances: [{ id: '人-zhanguo-1', era: 'zhanguo', artifact: '中山王方壺', catalogId: '《殷周金文集成》9735號', sourceRef: '《殷周金文集成·戰國器》（據香港中文大學《漢語多功能字庫》）', dateRange: '戰國早期', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/人-zhanguo-1.jpg' }], isGap: false },
    { era: 'xiaozhuan', instances: [{ id: '人-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第08卷', collection: '（传世字书）', sourceRef: '《說文解字·人部》：「天地之性最貴者也。此籒文。象臂脛之形。凡人之屬皆从人。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: 'glyphs/人-seal.svg' }], isGap: false },
    { era: 'lishu', instances: [{ id: '人-lishu-1', era: 'lishu', artifact: '馬王堆．五十二病方．100', sourceRef: '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/人-lishu-1.jpg' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '人-kaishu-1', era: 'kaishu', artifact: '真草千字文', catalogId: '赵孟頫 書', sourceRef: '《真草千字文》赵孟頫書', dateRange: '元', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/人-kaishu-1.jpg' }, { id: '人-kaishu-2', era: 'kaishu', artifact: '临大字阴符经', catalogId: '潘伯鹰 書', sourceRef: '《临大字阴符经》潘伯鹰書', dateRange: '近代', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/人-kaishu-2.jpg' }, { id: '人-kaishu-3', era: 'kaishu', artifact: '南城咏古诗帖', catalogId: '迺贤 書', sourceRef: '《南城咏古诗帖》迺贤書', dateRange: '元', verification: 'verified', verifier: '词典网·书法字典（据历代碑帖）', imageSrc: 'glyphs/人-kaishu-3.jpg' }], isGap: false }
  ] },

  { char: '紙', eras: [
    { era: 'jiaguwen', instances: [], isGap: true, gapNote: '此字後起，商代甲骨文中未见。' },
    { era: 'jinwen', instances: [], isGap: true, gapNote: '西周至春秋金文中未见此字。' },
    { era: 'zhanguo', instances: [], isGap: true, gapNote: '战国文字资料中暂未发现此字实例，属缺环。' },
    { era: 'xiaozhuan', instances: [{ id: '紙-xiaozhuan-1', era: 'xiaozhuan', artifact: '《說文解字》小篆字头', catalogId: '說文解字 第13卷', collection: '（传世字书）', sourceRef: '《說文解字·糸部》：「絮一苫也。从糸氏聲。」', dateRange: '东汉（许慎著）', verification: 'verified', verifier: '维基文库《說文解字》', imageSrc: 'glyphs/紙-xiaozhuan-1.jpg', note: '小篆圖據《康熙字典》字形庫（說文小篆）' }], isGap: false },
    { era: 'lishu', instances: [{ id: '紙-lishu-1', era: 'lishu', artifact: '睡虎地秦簡．日書甲種．61背-2', sourceRef: '簡帛寫本（《馬王堆漢墓帛書》《睡虎地秦墓竹簡》，據《漢語多功能字庫》）', verification: 'verified', verifier: '香港中文大學《漢語多功能字庫》', imageSrc: 'glyphs/紙-lishu-1.jpg' }], isGap: false },
    { era: 'kaishu', instances: [{ id: '紙-kaishu-1', era: 'kaishu', artifact: '唐以降写本/碑帖（字例待核）', sourceRef: '唐碑拓本', dateRange: '唐及以后', verification: 'pending', note: '具体碑帖字例待核。' }], isGap: false }
  ] },

]

export default CHARACTERS
