/**
 * 数据模型 —— 汉字字形演变「证据链」的核心类型定义。
 *
 * 铁律回顾：
 * 1. 每个字形实例必须挂「实物出处」（哪片甲骨/哪件青铜器/哪块碑/哪件写本）与「核对状态」。
 * 2. 某时代无实例 → 缺环（isGap = true），绝不用后世字形倒填。
 * 3. 不用示意图/字体渲染冒充实物；实物图片一律来自考古著录/馆藏影像。
 */

/** 六大时代标识（按时间先后） */
export type EraId =
  | 'jiaguwen'   // 甲骨文（商）
  | 'jinwen'     // 金文（西周/春秋）
  | 'zhanguo'    // 战国文字
  | 'xiaozhuan'  // 小篆（秦）
  | 'lishu'      // 隶书（汉）
  | 'kaishu'     // 楷书（汉末以降）

/** 核对状态：已核对 / 存疑 / 待核对 */
export type VerificationStatus = 'verified' | 'uncertain' | 'pending'

/** 一个「实物字形实例」：某时代下的一条证据 */
export interface GlyphInstance {
  /** 唯一标识（数据源内稳定） */
  id: string
  /** 所属时代 */
  era: EraId
  /**
   * 实物字形图 URL。
   * 铁律：必须是考古著录/馆藏影像，不得用字体渲染或示意图。
   * 留空表示「实物图像尚未接入」，渲染层会显示显式的待接占位，绝不伪造字形。
   */
  imageSrc?: string
  /**
   * 该实物图像的**原始出处页**（点击图片时跳转）。
   * 例如：港中大《漢語多功能字庫》的 oracle.php?code=… / bronze.php?id=…、
   * 维基共享资源的 File: 页、词典网的碑帖原图页。
   * 留空表示没有可跳转的来源页，渲染层不生成链接。
   */
  sourceUrl?: string
  /** 实物名称——哪片甲骨/哪件青铜器/哪块碑/哪件写本 */
  artifact: string
  /** 著录编号或器物编号，如《甲骨文合集》合 xxxx、出土坑位等 */
  catalogId?: string
  /** 现藏机构，如 台北故宫、北京故宫、社科院等 */
  collection?: string
  /** 著录出处，如《甲骨文合集》第 x 册、《说文解字》等 */
  sourceRef?: string
  /** 断代/年代区间，如「殷墟二期」「西周晚期」 */
  dateRange?: string
  /** 核对状态 */
  verification: VerificationStatus
  /** 核对依据/核对人（可选） */
  verifier?: string
  /** 补充说明（可选） */
  note?: string
}

/** 一个时代条目的聚合：可能有多条实例，或为「缺环」 */
export interface EraEntry {
  era: EraId
  /** 该时代下现存的实物实例（可为空数组 = 缺环） */
  instances: GlyphInstance[]
  /** 是否缺环（无实例） */
  isGap: boolean
  /** 缺环说明：解释为何该时代无实例（如「此字形后起，商代未见」） */
  gapNote?: string
}

/** 一个字的完整证据链 */
export interface CharacterData {
  /** 所考的字 */
  char: string
  /** 六大时代条目，应按时间先后排列 */
  eras: EraEntry[]
}

/** 时代元信息（标签/年代/载体说明），供渲染层统一取用 */
export interface EraMeta {
  id: EraId
  /** 时代名，如「甲骨文」 */
  label: string
  /** 年代区间，如「约前 14—前 11 世纪」 */
  period: string
  /** 典型载体说明，如「龟甲 · 兽骨」 */
  carrier: string
}
