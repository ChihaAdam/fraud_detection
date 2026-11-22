import { ConfusionMatrixChart } from '../components/visualisation/ConfusionMatrixChart'
import { Intro } from '../components/Intro'
import { useConfusionMatrix } from '../hooks/useConfusionMatrix'
import { useDetectionContext } from '../hooks/useFraudDetection'
import { confusionMatrixEndpoint } from '../lib/confusionMatrix'
import './ConfusionMatrixPage.css'

export function ConfusionMatrixPage() {
  const { endpoint } = useDetectionContext()
  const matrixEndpoint = confusionMatrixEndpoint(endpoint)
  const { phase, matrix, error, reload } = useConfusionMatrix(matrixEndpoint)

  return (
    <>
      <Intro
        eyebrow="MODEL PERFORMANCE / 002"
        title={
          <>
            Read the matrix.<br /><em>Trust the numbers.</em>
          </>
        }
        lede="The confusion matrix is computed by the Flask API on the held-out test split — the same model that scores the prediction route, seen through its mistakes."
        stats={[
          { value: '2 × 2', label: 'MATRIX' },
          { value: 'TEST', label: 'EVALUATION SPLIT' },
          { value: 'LIVE', label: 'API SOURCE' },
        ]}
      />

      <div className="work-grid cm-layout">
        <section className="panel cm-panel" aria-label="Confusion matrix">
          <div className="panel-head">
            <span className="panel-index">01</span>
            <h2>Confusion matrix</h2>
            <button className="cm-refresh" type="button" onClick={reload} disabled={phase === 'loading'}>
              REFRESH
            </button>
            <span className="panel-meta">GET /confusion-matrix</span>
          </div>

          <div className="cm-panel-body" aria-live="polite">
            {phase === 'loading' && (
              <div className="loading-state">
                <div className="scanner" aria-hidden="true"><span /></div>
                <div className="loading-title">LOADING TEST MATRIX</div>
                <p>Asking the model API for its held-out predictions…</p>
              </div>
            )}

            {phase === 'error' && (
              <div className="error-state">
                <div className="state-tag">LINK FAILURE</div>
                <h3>NO MATRIX</h3>
                <p>{error}</p>
                <div className="cm-error-hint">
                  Start the API with <code>python model/api/api.py</code> and check the endpoint below.
                  <button className="cm-retry" type="button" onClick={reload}>RETRY</button>
                </div>
              </div>
            )}

            {phase === 'done' && matrix && (
              <>
                <ConfusionMatrixChart data={matrix} />
                <div className="cm-caption">
                  <div className="cm-caption-head">
                    <span>HOW TO READ IT</span>
                    <span>{matrix.dataset} · {matrix.split} SPLIT</span>
                  </div>
                  <p>
                    Rows are the <strong>true class</strong>, columns are the <strong>predicted class</strong>.
                    Red cells are correct decisions; grey cells are the ones the classifier got wrong.
                    Darker shading means a higher count.
                  </p>
                  <div className="cm-legend">
                    <div><span className="cm-swatch cm-swatch-hit" aria-hidden="true" />CORRECT · TN / TP</div>
                    <div><span className="cm-swatch cm-swatch-miss" aria-hidden="true" />ERRORS · FP / FN</div>
                  </div>
                </div>
              </>
            )}
          </div>
        </section>
      </div>
    </>
  )
}
