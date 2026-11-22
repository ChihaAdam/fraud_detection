import type { Phase, Verdict } from '../../types'
import { ErrorView } from './ErrorView'
import { IdleView } from './IdleView'
import { LoadingView } from './LoadingView'
import { VerdictView } from './VerdictView'
import './ResultPanel.css'

type Props = {
  phase: Phase
  verdict: Verdict | null
  error: string
  stale: boolean
}

export function ResultPanel({ phase, verdict, error, stale }: Props) {
  return (
    <aside className="panel result-panel" aria-label="Detection result">
      <div className="panel-head">
        <span className="panel-index">02</span>
        <h2>Verdict</h2>
        <span className="panel-meta">MODEL RESPONSE</span>
      </div>

      <div className="result-body" aria-live="polite">
        {phase === 'idle' && <IdleView />}
        {phase === 'loading' && <LoadingView />}
        {phase === 'error' && <ErrorView message={error} />}
        {phase === 'done' && verdict && <VerdictView verdict={verdict} stale={stale} />}
      </div>
    </aside>
  )
}
