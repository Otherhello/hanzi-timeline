import type { EraId, EraMeta } from '../types'

/** 六大时代元信息，按时间先后排序 */
export const ERAS: EraMeta[] = [
  { id: 'jiaguwen',  label: '甲骨文', period: '约前 14—前 11 世纪', carrier: '龟甲 · 兽骨' },
  { id: 'jinwen',    label: '金文',   period: '约前 11—前 3 世纪',   carrier: '青铜器铭文' },
  { id: 'zhanguo',   label: '战国文字', period: '约前 5—前 3 世纪', carrier: '简帛 · 玺印 · 盟书' },
  { id: 'xiaozhuan', label: '小篆',   period: '秦（前 221—前 206）',  carrier: '刻石 · 权量诏版' },
  { id: 'lishu',     label: '隶书',   period: '汉（前 206—220）',     carrier: '碑刻 · 简牍' },
  { id: 'kaishu',    label: '楷书',   period: '汉末以降',            carrier: '碑志 · 写本' },
]

/** 快速取某个时代的元信息 */
export function eraMeta(id: EraId): EraMeta {
  return ERAS.find((e) => e.id === id)!
}

/** 核对状态 → 中文标签与语义 */
export const VERIFICATION_LABEL: Record<string, string> = {
  verified: '已核对',
  uncertain: '存疑',
  pending: '待核对',
}
