import type { Verdict } from '../../types'

type Props = {
  verdict: Verdict
  stale: boolean
}

export function VerdictView({ verdict, stale }: Props) {
  const fraud = verdict.prediction === 1
  const clean = verdict.prediction === 0
  const verdictWord = fraud ? 'FRAUD' : clean ? 'CLEAR' : 'UNKNOWN'
  const tone = fraud ? 'is-fraud' : clean ? 'is-clear' : 'is-unknown'

  return (
    <div className={`done-state ${tone}`}>
      <div>
        {stale && <div className="stale-banner">INPUT CHANGED · RERUN TO REFRESH</div>}
        <div className="verdict-kicker">CLASSIFIER OUTPUT</div>
        <div className="verdict-word">{verdictWord}</div>
        <div className="verdict-label">MODEL LABEL / {verdict.label.toUpperCase()}</div>
<div className="meter">
        <div className="meter-head">
          <span>RISK SIGNAL</span>
          <span>{fraud ? 'HIGH' : clean ? 'LOW' : 'UNRESOLVED'}</span>
        </div>
      </div>

      <div className="result-stats">
        <div>
          <span>PREDICTION</span>
          <strong>{verdict.prediction}</strong>
        </div>
        <div>
          <span>RESPONSE</span>
          <strong>{verdict.latency}<small>ms</small></strong>
        </div>
      </div>
      </div>
      


      <div className="trace">
        <div><span>REQUEST</span><strong>POST /predict</strong></div>
        <div><span>PAYLOAD</span><strong>30 numeric values</strong></div>
        <div><span>STATUS</span><strong>{stale ? 'STALE RESULT' : 'COMPLETE'}</strong></div>
      </div>
    </div>
  )
}
