import { Intro } from '../components/Intro'
import { TargetLinks } from '../components/visualisation/TargetLinks'
import { useCorrelationMatrix } from '../hooks/useCorrelationMatrix'
import { useDetectionContext } from '../hooks/useFraudDetection'
import { correlationMatrixEndpoint } from '../lib/correlationMatrix'
import './TargetLinksPage.css'

export function TargetLinksPage() {
  const { endpoint } = useDetectionContext()
  const matrixEndpoint = correlationMatrixEndpoint(endpoint)
  const { phase, matrix, error, reload } = useCorrelationMatrix(matrixEndpoint)

  return (
    <>
      <Intro
        eyebrow="DATASET STRUCTURE / 004"
        title={
          <>
            Follow the target.<br /><em>Find the drivers.</em>
          </>
        }
        lede="Which variables move with fraud, and which barely register? This ranking is computed by the Flask API from the same Pearson correlations shown in the full matrix."
        stats={[
          { value: 'TOP 8', label: 'FEATURES' },
          { value: matrix?.target ?? 'TARGET', label: 'CLASS' },
          { value: 'LIVE', label: 'API SOURCE' },
        ]}
      />

      <div className="work-grid target-links-layout">
        <section className="panel target-links-panel" aria-label="Correlations with the target">
          <div className="panel-head">
            <span className="panel-index">01</span>
            <h2>Target links</h2>
            <button
              className="target-links-refresh"
              type="button"
              onClick={reload}
              disabled={phase === 'loading'}
            >
              REFRESH
            </button>
            <span className="panel-meta">GET /correlation-matrix</span>
          </div>

          <div className="target-links-panel-body" aria-live="polite">
            {phase === 'loading' && (
              <div className="loading-state">
                <div className="scanner" aria-hidden="true"><span /></div>
                <div className="loading-title">LOADING TARGET LINKS</div>
                <p>Asking the model API for feature correlations with the fraud class…</p>
              </div>
            )}

            {phase === 'error' && (
              <div className="error-state">
                <div className="state-tag">LINK FAILURE</div>
                <h3>NO LINKS</h3>
                <p>{error}</p>
                <div className="target-links-error-hint">
                  Start the API with <code>python model/api/api.py</code> and check the endpoint below.
                  <button className="target-links-retry" type="button" onClick={reload}>RETRY</button>
                </div>
              </div>
            )}

            {phase === 'done' && matrix && <TargetLinks data={matrix} />}
          </div>
        </section>
      </div>
    </>
  )
}
