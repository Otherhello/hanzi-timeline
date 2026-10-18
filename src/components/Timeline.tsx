import type { CharacterData } from '../types'
import EraCard from './EraCard'

export default function Timeline({ data }: { data: CharacterData }) {
  return (
    <div className="timeline">
      {data.eras.map((entry) => (
        <div
          key={entry.era}
          className={`timeline-item${entry.isGap ? ' timeline-item--gap' : ''}`}
        >
          <EraCard entry={entry} />
        </div>
      ))}
    </div>
  )
}
