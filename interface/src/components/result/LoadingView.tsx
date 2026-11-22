export function LoadingView() {
  return (
    <div className="loading-state">
      <div className="scanner" aria-hidden="true"><span /></div>
      <div className="loading-title">SCORING INPUT VECTOR</div>
      <p>Waiting for the classifier response…</p>
    </div>
  )
}
