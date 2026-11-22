type Props = {
  message: string
}

export function ErrorView({ message }: Props) {
  return (
    <div className="error-state">
      <div className="state-tag">LINK FAILURE</div>
      <h3>NO VERDICT</h3>
      <p>{message}</p>
      <div className="error-hint">
        Start the API with <code>python model/api/api.py</code> and check the endpoint below.
      </div>
    </div>
  )
}
