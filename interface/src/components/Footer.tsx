import './Footer.css'

type Props = {
  endpoint: string
  onEndpointChange: (value: string) => void
}

export function Footer({ endpoint, onEndpointChange }: Props) {
  return (
    <footer className="footer">
      <label className="endpoint">
        <span>API ENDPOINT</span>
        <input
          type="text"
          spellCheck={false}
          value={endpoint}
          onChange={(event) => onEndpointChange(event.target.value)}
        />
      </label>
      <span className="footer-note">
        POST /predict · GET /confusion-matrix · GET /correlation-matrix · FLASK MODEL API · VECTORS ARE ONLY SENT WHEN YOU RUN DETECTION
      </span>
    </footer>
  )
}
