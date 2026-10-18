import type { CharacterData } from '../types'

/**
 * 数据源适配器接口。
 *
 * 这是整个项目「可替换性」的关键接缝：
 * - 现在用 mockSource（示例数据）跑通界面；
 * - 拿到数据库网址后，新增 liveSource 实现本接口（运行时抓取，或抓取后离线缓存），
 *   在 App 里改一行注入即可，其余组件零改动。
 */
export interface GlyphSource {
  /** 数据源名称，如「小學堂」「示例数据」 */
  readonly name: string
  /** mock = 示例数据；live = 实时/离线抓取 */
  readonly mode: 'mock' | 'live'
  /** 输入单字（一个汉字），返回完整证据链 */
  fetch(char: string): Promise<CharacterData>
  /** 判断是否收录该字（用于输入校验/提示） */
  has?(char: string): boolean
}
