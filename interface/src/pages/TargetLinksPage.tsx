import { Intro } from '../components/Intro'
import { TargetLinks } from '../components/visualisation/TargetLinks'
import { useFeatureSelection } from '../hooks/useFeatureSelection'
import { useDetectionContext } from '../hooks/useFraudDetection'
import { featureSelectionEndpoint } from '../lib/featureSelection'
import './TargetLinksPage.css'

export function TargetLinksPage() {
  const { endpoint } = useDetectionContext()
  const selectionEndpoint = featureSelectionEndpoint(endpoint)
  const { phase, selection, error, reload } = useFeatureSelection(selectionEndpoint)

  return (
    <>
      <Intro
        eyebrow="DATASET STRUCTURE / 004"
        title={
          <>
            Follow the target.<br /><em>Find the drivers.</em>
          </>
        }
        lede="The variables the model actually keeps, ranked by the ANOVA F-score computed in feature_selection.py on the training split. Mutual information is shown alongside it."
        stats={[
          { value: selection ? `TOP ${selection.k}` : 'TOP …', label: 'FEATURES' },
          { value: selection?.target ?? 'TARGET', label: 'CLASS' },
          { value: 'LIVE', label: 'API SOURCE' },
        ]}
      />

      <div className="work-grid target-links-layout">
        <section className="panel target-links-panel" aria-label="K best variables">
          <div className="panel-head">
            <span className="panel-index">01</span>
            <h2>K best variables</h2>
            <button
              className="target-links-refresh"
              type="button"
              onClick={reload}
              disabled={phase === 'loading'}
            >
              REFRESH
            </button>
            <span className="panel-meta">GET /feature-selection</span>
          </div>

          <div className="target-links-panel-body" aria-live="polite">
            {phase === 'loading' && (
              <div className="loading-state">
                <div className="scanner" aria-hidden="true"><span /></div>
                <div className="loading-title">LOADING FEATURE SCORES</div>
                <p>Asking the model API for its SelectKBest ranking…</p>
              </div>
            )}

            {phase === 'error' && (
              <div className="error-state">
                <div className="state-tag">LINK FAILURE</div>
                <h3>NO SCORES</h3>
                <p>{error}</p>
                <div className="target-links-error-hint">
                  Start the API with <code>python model/api/api.py</code> and check the endpoint below.
                  <button className="target-links-retry" type="button" onClick={reload}>RETRY</button>
                </div>
              </div>
            )}

            {phase === 'done' && selection && <TargetLinks data={selection} />}
          </div>
        </section>
      </div>
    </>
  )
}
