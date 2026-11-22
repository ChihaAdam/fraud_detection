import { InputPanel } from '../components/InputPanel'
import { Intro } from '../components/Intro'
import { ResultPanel } from '../components/result/ResultPanel'
import { useDetectionContext } from '../hooks/useFraudDetection'

export function PredictPage() {
  const detection = useDetectionContext()

  return (
    <>
      <Intro />
      <div className="work-grid">
        <InputPanel
          values={detection.values}
          invalid={detection.invalid}
          preview={detection.preview}
          loading={detection.phase === 'loading'}
          onChange={detection.updateValue}
          onSubmit={detection.submit}
          onCleanSample={detection.loadCleanSample}
          onFraudSample={detection.loadFraudSample}
          onReset={detection.resetVector}
        />
        <ResultPanel
          phase={detection.phase}
          verdict={detection.verdict}
          error={detection.error}
          stale={detection.stale}
        />
      </div>
    </>
  )
}
