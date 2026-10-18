import type { CharacterData, EraEntry, EraId, GlyphInstance } from '../types'
import type { GlyphSource } from './GlyphSource'

/**
 * 示例数据源 —— 仅用于打通界面与流程。
 *
 * ⚠️ 重要申明：
 * 以下所有「实物出处 / 著录编号 / 藏地」字段均为结构性示例占位，
 * 图像一律留空（imageSrc 未填），渲染层会显示「实物拓图待接入」占位 ——
 * 绝不用示意图/字体渲染冒充实物。待接入真实数据库后整体替换。
 */

let seq = 0
function inst(era: EraId, patch: Partial<GlyphInstance>): GlyphInstance {
  seq += 1
  return {
    id: `mock-${era}-${seq}`,
    era,
    artifact: '（示例）待补实物',
    verification: 'pending',
    ...patch,
  }
}

function eraEntry(era: EraId, instances: GlyphInstance[], gapNote?: string): EraEntry {
  return { era, instances, isGap: instances.length === 0, gapNote }
}

/** 「马」：六大时代均有实例，展示一条完整的证据链 */
const 马: CharacterData = {
  char: '马',
  eras: [
    eraEntry('jiaguwen', [
      inst('jiaguwen', {
        artifact: '（示例）殷墟甲骨——待补具体卜骨/卜甲',
        sourceRef: '《甲骨文合集》——著录编号待核',
        dateRange: '殷墟二期',
        note: '示例占位：确切的甲骨编号与藏地待接入数据库后替换。',
      }),
    ], ''),
    eraEntry('jinwen', [
      inst('jinwen', {
        artifact: '（示例）西周青铜器——待补具体器名',
        sourceRef: '《殷周金文集成》——器号待核',
        dateRange: '西周中期',
      }),
      inst('jinwen', {
        artifact: '（示例）春秋青铜器——待补具体器名',
        dateRange: '春秋晚期',
      }),
    ], ''),
    eraEntry('zhanguo', [
      inst('zhanguo', {
        artifact: '（示例）战国简帛/玺印——待补具体实物',
        dateRange: '战国中晚期',
      }),
    ], ''),
    eraEntry('xiaozhuan', [
      inst('xiaozhuan', {
        artifact: '《说文解字》小篆字头',
        sourceRef: '《说文解字·马部》',
        dateRange: '东汉（许慎著）',
        collection: '（传世字书）',
      }),
    ], ''),
    eraEntry('lishu', [
      inst('lishu', {
        artifact: '（示例）汉碑/汉简——待补具体碑名或简号',
        dateRange: '东汉',
      }),
    ], ''),
    eraEntry('kaishu', [
      inst('kaishu', {
        artifact: '（示例）楷书碑帖——待补具体碑帖名',
        dateRange: '唐及以后',
      }),
    ], ''),
  ],
}

/** 「纸」：后起字，甲骨/金文/战国三期应缺环，展示缺环逻辑 */
const 纸: CharacterData = {
  char: '纸',
  eras: [
    eraEntry('jiaguwen', [], '「纸」为后起字，商代甲骨文中未见此字之形。'),
    eraEntry('jinwen', [], '西周至春秋金文中未见「纸」字，此时该概念尚未以文字记录。'),
    eraEntry('zhanguo', [], '战国文字资料中暂未见可靠实例，属缺环。'),
    eraEntry('xiaozhuan', [
      inst('xiaozhuan', {
        artifact: '《说文解字》小篆字头',
        sourceRef: '《说文解字·糸部》：「纸，絮一苫也。」',
        dateRange: '东汉（许慎著）',
        collection: '（传世字书）',
      }),
    ], ''),
    eraEntry('lishu', [
      inst('lishu', {
        artifact: '（示例）汉简/汉碑——待补具体简号或碑名',
        dateRange: '东汉',
      }),
    ], ''),
    eraEntry('kaishu', [
      inst('kaishu', {
        artifact: '（示例）楷书写本/碑帖——待补具体实物',
        dateRange: '隋唐及以后',
      }),
    ], ''),
  ],
}

const DB: Record<string, CharacterData> = { '马': 马, '纸': 纸 }

export const mockSource: GlyphSource = {
  name: '示例数据（待接入真实数据库）',
  mode: 'mock',
  async fetch(char: string): Promise<CharacterData> {
    // 简化：以简体「马」对齐正体「馬」的演示数据
    const key = char === '馬' ? '马' : char
    const data = DB[key]
    if (!data) {
      throw new Error(`示例库暂无「${char}」的数据，请先试「马」或「纸」。`)
    }
    return data
  },
  has(char: string): boolean {
    return Boolean(DB[char] || (char === '馬' && DB['马']))
  },
}
