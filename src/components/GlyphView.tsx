import type { GlyphInstance } from '../types'

/**
 * 字形主体区。
 * 铁律：imageSrc 为空时显示显式的「实物拓图待接入」空帧，绝不伪造字形。
 */
export default function GlyphView({ instance }: { instance: GlyphInstance }) {
  if (instance.imageSrc) {
    return (
      <img
        src={instance.imageSrc}
        alt={`${instance.era}「${instance.artifact}」实物字形`}
      />
    )
  }
  return (
    <div className="glyph-ph">
      <span className="ph-mark">实物拓图待接入</span>
      <span className="ph-sub">此处不以后世字形倒填，亦不用示意图冒充实物</span>
      <span className="ph-note">
        接入数据库后，此帧将展示 {instance.artifact} 的原拓影像
      </span>
    </div>
  )
}
