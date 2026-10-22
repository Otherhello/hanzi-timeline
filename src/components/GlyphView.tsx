import type { GlyphInstance } from '../types'

/**
 * 字形主体区。
 * 铁律：imageSrc 为空时显示显式的「实物拓图待接入」空帧，绝不伪造字形。
 *
 * 若该实例带有 sourceUrl（图像原始出处页），整张图包成一个链接，
 * 点击即在新标签页打开出处页——把"看图"和"查证"连起来。
 */
export default function GlyphView({ instance }: { instance: GlyphInstance }) {
  if (instance.imageSrc) {
    const img = (
      <img
        src={instance.imageSrc}
        alt={`${instance.era}「${instance.artifact}」实物字形`}
        loading="lazy"
      />
    )
    if (instance.sourceUrl) {
      return (
        <a
          className="glyph-link"
          href={instance.sourceUrl}
          target="_blank"
          rel="noopener noreferrer"
          title={`查看图片来源：${instance.artifact}`}
        >
          {img}
          <span className="glyph-link-hint" aria-hidden="true">
            来源 ↗
          </span>
        </a>
      )
    }
    return img
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
