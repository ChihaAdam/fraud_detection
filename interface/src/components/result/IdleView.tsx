export function IdleView() {
  return (
    <div className="idle-state">
      <div className="idle-mark" aria-hidden="true">—</div>
      <div className="idle-title">AWAITING VECTOR</div>
      <p>Fill the thirty parameters, then run detection to query the model API.</p>
      <ol className="idle-steps">
        <li><span>1</span>ENTER PARAMETERS</li>
        <li><span>2</span>POST TO MODEL</li>
        <li><span>3</span>READ VERDICT</li>
      </ol>
    </div>
  )
}
