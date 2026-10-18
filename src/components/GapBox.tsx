import type { EraEntry } from '../types'

/** 缺环占位：空白 + 说明，明示该时代无实例 */
export default function GapBox({ entry }: { entry: EraEntry }) {
  return (
    <div className="gap-box">
      <div className="gap-mark" aria-hidden="true">缺</div>
      <div className="gap-text">
        <div className="gap-title">缺 环</div>
        <div className="gap-note">
          {entry.gapNote || '此时代暂无可信的实物实例，故不展示字形。'}
        </div>
      </div>
    </div>
  )
}
