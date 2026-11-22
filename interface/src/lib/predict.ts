import type { PreviewValue } from '../types'

export type FeatureParse = {
  features: number[]
  invalid: number[]
}

export type Prediction = {
  prediction: number
  label: string
}

export function parseFeatures(values: string[]): FeatureParse {
  const features = values.map((value) =>
    value.trim() === '' ? Number.NaN : Number(value),
  )
  const invalid = features.flatMap((value, index) =>
    Number.isFinite(value) ? [] : [index],
  )
  return { features, invalid }
}

export function previewFeatures(values: string[]): PreviewValue[] {
  return values.map((value) => {
    if (value.trim() === '') return null
    const number = Number(value)
    return Number.isFinite(number) ? number : null
  })
}

export async function requestPrediction(
  endpoint: string,
  features: number[],
): Promise<Prediction> {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ features }),
    signal: AbortSignal.timeout(12000),
  })

  const payload: unknown = await response.json().catch(() => null)

  if (!response.ok) {
    const message =
      payload &&
      typeof payload === 'object' &&
      'error' in payload &&
      typeof payload.error === 'string'
        ? payload.error
        : `Model API responded with status ${response.status}.`
    throw new Error(message)
  }

  if (
    !payload ||
    typeof payload !== 'object' ||
    !('prediction' in payload) ||
    !('label' in payload)
  ) {
    throw new Error('Model API returned an unexpected payload.')
  }

  const prediction = Number(payload.prediction)
  if (!Number.isFinite(prediction)) {
    throw new Error('Model API returned an invalid prediction.')
  }

  return { prediction, label: String(payload.label) }
}
