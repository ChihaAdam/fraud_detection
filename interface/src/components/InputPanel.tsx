import type { FormEvent } from 'react'
import { FIELDS } from '../constants'
import type { PreviewValue } from '../types'
import { NumberField } from './NumberField'
import './InputPanel.css'

type Props = {
  values: string[]
  invalid: number[]
  preview: PreviewValue[]
  loading: boolean
  onChange: (index: number, value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
  onCleanSample: () => void
  onFraudSample: () => void
  onReset: () => void
}

export function InputPanel({
  values,
  invalid,
  preview,
  loading,
  onChange,
  onSubmit,
  onCleanSample,
  onFraudSample,
  onReset,
}: Props) {
  return (
    <form className="panel form-panel" onSubmit={onSubmit} noValidate>
      <div className="panel-head">
        <span className="panel-index">01</span>
        <h2>Input vector</h2>
        <span className="panel-meta">TIME · V1—V28 · AMOUNT</span>
      </div>

      <div className="core-grid">
        <NumberField
          id="field-0"
          label="TIME"
          index="01"
          variant="core"
          value={values[0]}
          invalid={invalid.includes(0)}
          onChange={(value) => onChange(0, value)}
        />
        <NumberField
          id="field-29"
          label="AMOUNT"
          index="30"
          variant="core"
          placeholder="0.00"
          value={values[29]}
          invalid={invalid.includes(29)}
          onChange={(value) => onChange(29, value)}
        />
      </div>

      <div className="section-bar">
        <span>COMPONENT VECTOR</span>
        <span>V1 — V28 / FIXED ORDER</span>
      </div>

      <div className="vector-grid">
        {FIELDS.slice(1, 29).map((name, offset) => {
          const index = offset + 1
          return (
            <NumberField
              key={name}
              id={`field-${index}`}
              label={name}
              value={values[index]}
              invalid={invalid.includes(index)}
              onChange={(value) => onChange(index, value)}
            />
          )
        })}
      </div>

      <div className="actions">
        <button className="run-button" type="submit" disabled={loading}>
          <span>{loading ? 'SCORING…' : 'RUN DETECTION'}</span>
          <span className="run-arrow" aria-hidden="true">↗</span>
        </button>
        <div className="samples">
          <button type="button" onClick={onCleanSample}>CLEAN SAMPLE</button>
          <button type="button" onClick={onFraudSample}>FRAUD SAMPLE</button>
          <button type="button" onClick={onReset}>CLEAR</button>
        </div>
      </div>

      <details className="payload">
        <summary>PAYLOAD PREVIEW <span>JSON</span></summary>
        <pre>{JSON.stringify({ features: preview }, null, 2)}</pre>
      </details>
    </form>
  )
}
