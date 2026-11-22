import { CorrelationMatrixChart } from '../components/visualisation/CorrelationMatrixChart'
import { Intro } from '../components/Intro'
import { useCorrelationMatrix } from '../hooks/useCorrelationMatrix'
import { useDetectionContext } from '../hooks/useFraudDetection'
import { correlationMatrixEndpoint } from '../lib/correlationMatrix'
import './CorrelationMatrixPage.css'

export function CorrelationMatrixPage() {
  const { endpoint } = useDetectionContext()
  const matrixEndpoint = correlationMatrixEndpoint(endpoint)
  const { phase, matrix, error, reload } = useCorrelationMatrix(matrixEndpoint)

  const size = matrix ? matrix.labels.length : 0

  return (
    <>
      <Intro
        eyebrow="DATASET STRUCTURE / 003"
        title={
          <>
            Find the dependencies.<br /><em>Before the verdict.</em>
          </>
        }
        lede="Pearson correlations computed by the Flask API on the very dataset behind the model. Every cell shows its coefficient — hover or focus one for the exact value."
        stats={[
          { value: size ? `${size} × ${size}` : 'N × N', label: 'MATRIX' },
          { value: matrix?.method.toUpperCase() ?? 'PEARSON', label: 'METHOD' },
          { value: 'LIVE', label: 'API SOURCE' },
        ]}
      />

      <div className="work-grid corr-layout">
        <section className="panel corr-panel" aria-label="Correlation matrix">
          <div className="panel-head">
            <span className="panel-index">01</span>
            <h2>Correlation matrix</h2>
            <button className="corr-refresh" type="button" onClick={reload} disabled={phase === 'loading'}>
              REFRESH
            </button>
            <span className="panel-meta">GET /correlation-matrix</span>
          </div>

          <div className="corr-panel-body" aria-live="polite">
            {phase === 'loading' && (
              <div className="loading-state">
                <div className="scanner" aria-hidden="true"><span /></div>
                <div className="loading-title">LOADING CORRELATIONS</div>
                <p>Asking the model API for the dataset correlation matrix…</p>
              </div>
            )}

            {phase === 'error' && (
              <div className="error-state">
                <div className="state-tag">LINK FAILURE</div>
                <h3>NO MATRIX</h3>
                <p>{error}</p>
                <div className="corr-error-hint">
                  Start the API with <code>python model/api/api.py</code> and check the endpoint below.
                  <button className="corr-retry" type="button" onClick={reload}>RETRY</button>
                </div>
              </div>
            )}

            {phase === 'done' && matrix && (
              <>
                <CorrelationMatrixChart data={matrix} />
                <div className="corr-caption">
                  <div className="corr-caption-head">
                    <span>HOW TO READ IT</span>
                    <span>{matrix.dataset} · {matrix.method.toUpperCase()}</span>
                  </div>
                  <p>
                    Each cell is the Pearson correlation between two features: red for a positive
                    relationship, blue for a negative one. The darker the shade, the closer the
                    coefficient is to +1 or -1. The highlighted row and column belong to{' '}
                    <strong>{matrix.target}</strong>.
                  </p>
                </div>
              </>
            )}
          </div>
        </section>
      </div>
    </>
  )
}
