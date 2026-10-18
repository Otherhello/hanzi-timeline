import type { CharacterData } from '../types'
import type { GlyphSource } from './GlyphSource'
import CHARACTERS from '../data/characters'

/**
 * 本地資料源 —— 读取 tools/generate_glyph_data.py 生成的静态数据。
 *
 * 数据构成：
 * - 小篆：维基文库《說文解字》（核对状态 = 已核对）
 * - 甲骨／金文／战国／隶：香港中文大学《漢語多功能字庫》字形（已核对，附器号）
 * - 其余时代：著录出处已标明，核对状态 = 待核对
 * - 缺环：某时代无实例时显式标注，绝不倒填。
 *
 * 繁体→简体映射：局限（仅内置几个演示字的映射）。
 */
const SIMPLIFIED_TO_TRADITIONAL: Record<string, string> = {
  马: '馬',
  纸: '紙',
}

const DB: Record<string, CharacterData> = {}
for (const c of CHARACTERS) {
  DB[c.char] = c
}

function resolve(char: string): string {
  // 先查正体，再查简体→繁体映射
  if (DB[char]) return char
  const trad = SIMPLIFIED_TO_TRADITIONAL[char]
  if (trad && DB[trad]) return trad
  return char
}

export const realSource: GlyphSource = {
  name: '维基文库《說文解字》 · 香港中文大學《漢語多功能字庫》',
  mode: 'live',
  async fetch(char: string): Promise<CharacterData> {
    const key = resolve(char)
    const data = DB[key]
    if (!data) {
      throw new Error(`暂未收录「${char}」的证据链数据。当前收录：馬、牛、山、水、日、月、人、紙。`)
    }
    return data
  },
  has(char: string): boolean {
    const key = resolve(char)
    return Boolean(DB[key])
  },
}

/** 内置演示字（供示例 chips 使用） */
export const SUGGESTED = ['马', '牛', '山', '水', '日', '月', '人', '纸']
