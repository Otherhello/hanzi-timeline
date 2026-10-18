import { useEffect, useState } from 'react'
import type { CharacterData } from './types'
import { realSource, SUGGESTED } from './sources/realSource'
import Header from './components/Header'
import SearchBar from './components/SearchBar'
import Timeline from './components/Timeline'

const SUGGESTIONS = SUGGESTED

export default function App() {
  const [, setChar] = useState('马')
  const [data, setData] = useState<CharacterData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const query = async (ch: string) => {
    setChar(ch)
    setLoading(true)
    setError('')
    try {
      const result = await realSource.fetch(ch)
      setData(result)
    } catch (e) {
      setData(null)
      setError(e instanceof Error ? e.message : '查询失败')
    } finally {
      setLoading(false)
    }
  }

  // 首次挂载即查询默认字
  useEffect(() => { void query('马') }, [])

  return (
    <div className="app">
      <Header />
      <SearchBar onQuery={query} suggestions={SUGGESTIONS} />

      <div className="sourcebar">
        <span className="dot dot--live" />
        数据源：{realSource.name}
        <span className="tag">甲骨·金文·戰國·小篆·隸 已核对 · 楷 待核</span>
      </div>

      {loading && <div className="loading">正 在 寻 检 ……</div>}
      {error && !loading && <div className="error">{error}</div>}
      {data && !loading && <Timeline data={data} />}

      <div className="legend">
        <h4>说 明</h4>
        <ul>
          <li><b>实物出处</b>：每个字形均标注其出自哪片甲骨、哪件青铜器、哪件写本或哪部字书。</li>
          <li><b>核对状态</b>：<span className="badge badge--verified"><span className="badge-dot" />已核对</span> 印章红示已核对——甲骨／金文／战国／隶出自香港中文大学《漢語多功能字庫》字形库（附《合集》《集成》器号），小篆出自维基文库《說文解字》；<span className="badge badge--pending"><span className="badge-dot" />待核对</span> 淡墨灰示出处已标明、尚未逐件核验。</li>
          <li><b>缺环</b>：某时代无可信实例时，以「缺」空白帧说明，绝不倒填后世字形、不用示意图冒充实物。</li>
          <li><b>影像依据</b>：各期字形图取自可溯源的学术字形库（《漢語多功能字庫》《說文解字》），每图对应具体甲骨／青铜器／简帛／字书，非凭空杜撰。</li>
        </ul>
      </div>
    </div>
  )
}
