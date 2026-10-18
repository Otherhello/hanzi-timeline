import type { EraEntry } from '../types'
import { eraMeta } from '../data/eras'
import VerificationBadge from './VerificationBadge'
import GlyphView from './GlyphView'
import GapBox from './GapBox'

export default function EraCard({ entry }: { entry: EraEntry }) {
  const meta = eraMeta(entry.era)

  return (
    <article className="era-card">
      <div className="era-card__head">
        <div className="era-label" aria-hidden="true">{meta.label}</div>
        <div className="era-meta">
          <div className="era-meta__name">{meta.label}</div>
          <div className="era-meta__period">{meta.period}</div>
          <div className="era-meta__carrier">{meta.carrier}</div>
        </div>
        <div className="era-count">
          {entry.isGap ? '缺 环' : `${entry.instances.length} 例`}
        </div>
      </div>

      {entry.isGap ? (
        <GapBox entry={entry} />
      ) : (
        entry.instances.map((inst) => (
          <div className="occurrence" key={inst.id}>
            <div className="glyph-view">
              <GlyphView instance={inst} />
            </div>
            <dl className="provenance">
              <div className="provenance__row">
                <dt>实物</dt>
                <dd className="artifact">{inst.artifact}</dd>
              </div>
              {inst.catalogId && (
                <div className="provenance__row">
                  <dt>编号</dt><dd>{inst.catalogId}</dd>
                </div>
              )}
              {inst.sourceRef && (
                <div className="provenance__row">
                  <dt>著录</dt><dd><em>{inst.sourceRef}</em></dd>
                </div>
              )}
              {inst.collection && (
                <div className="provenance__row">
                  <dt>藏地</dt><dd>{inst.collection}</dd>
                </div>
              )}
              {inst.dateRange && (
                <div className="provenance__row">
                  <dt>断代</dt><dd>{inst.dateRange}</dd>
                </div>
              )}
              <div className="provenance__row">
                <dt>状态</dt>
                <dd><VerificationBadge status={inst.verification} /></dd>
              </div>
              {inst.note && (
                <div className="provenance__row">
                  <dt>备注</dt><dd>{inst.note}</dd>
                </div>
              )}
              {inst.verifier && (
                <div className="provenance__row provenance__row--verifier">
                  <dt>核者</dt><dd>{inst.verifier}</dd>
                </div>
              )}
            </dl>
          </div>
        ))
      )}
    </article>
  )
}
