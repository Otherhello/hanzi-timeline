import { useEffect, useMemo, useState } from 'react'
import { pickBackdrop } from '../data/backdrops'

/**
 * 纸背：每次进入站点随机挑一幅历代名帖，重度虚化后衬在内容之后。
 *
 * - 图片加载完成才淡入，避免首屏闪白
 * - 虚化 + 纸色罩层，保证正文对比度不受影响
 * - 右下角一行极淡的题识，并可直接点进维基共享资源的原件页
 */
export default function Backdrop() {
  const bg = useMemo(pickBackdrop, [])
  const [ready, setReady] = useState(false)

  useEffect(() => {
    let alive = true
    const img = new Image()
    img.onload = () => {
      if (alive) setReady(true)
    }
    img.src = bg.src
    if (img.complete) setReady(true)
    return () => {
      alive = false
    }
  }, [bg.src])

  return (
    <>
      <div
        className={`backdrop${ready ? ' is-ready' : ''}`}
        style={{ backgroundImage: `url(${bg.src})` }}
        aria-hidden="true"
      />
      <div className="backdrop-veil" aria-hidden="true" />
      <a
        className={`backdrop-caption${ready ? ' is-ready' : ''}`}
        href={bg.source}
        target="_blank"
        rel="noopener noreferrer"
        title="在维基共享资源查看此帖原件"
      >
        <span className="bc-name">{bg.name}</span>
        <span className="bc-meta">
          {bg.artist}　{bg.period}　{bg.script}
        </span>
      </a>
    </>
  )
}
