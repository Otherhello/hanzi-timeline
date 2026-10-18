import { useState } from 'react'

interface Props {
  onQuery: (char: string) => void
  suggestions: string[]
}

export default function SearchBar({ onQuery, suggestions }: Props) {
  const [value, setValue] = useState('')

  const submit = () => {
    const ch = value.trim()
    if (!ch) return
    onQuery(ch.charAt(0))
  }

  return (
    <section>
      <div className="searchbar">
        <div className="searchbox">
          <input
            value={value}
            maxLength={1}
            placeholder="字"
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && submit()}
            aria-label="输入单个汉字"
          />
          <span className="fieldu">单字</span>
        </div>
        <div className="search-actions">
          <button className="btn btn--primary" onClick={submit}>寻 字</button>
        </div>
        {suggestions.length > 0 && (
          <div className="chips">
            <span>示例：</span>
            {suggestions.map((s) => (
              <button
                key={s}
                className="chip"
                onClick={() => onQuery(s)}
              >
                {s}
              </button>
            ))}
          </div>
        )}
      </div>
      <p className="hint">
        输入<b>一个汉字</b>，回车或点击「寻 字」。当数值有核对状态色谱：<span className="badge badge--verified"><span className="badge-dot" />已核对</span> / <span className="badge badge--pending"><span className="badge-dot" />待核对</span>（缺环以空白帧显示）。
      </p>
    </section>
  )
}
