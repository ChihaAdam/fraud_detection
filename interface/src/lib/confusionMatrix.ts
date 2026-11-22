import type { ConfusionMatrix } from '../types'
import { apiEndpoint } from './apiEndpoint'

/** Derive the metrics endpoint from the prediction endpoint set in the footer. */
export function confusionMatrixEndpoint(endpoint: string): string {
  return apiEndpoint(endpoint, 'confusion-matrix')
}

function isMatrix(value: unknown): value is number[][] {
  return (
    Array.isArray(value) &&
    value.length === 2 &&
    value.every(
      (row) =>
        Array.isArray(row) &&
        row.length === 2 &&
        row.every((cell) => typeof cell === 'number' && Number.isFinite(cell)),
    )
  )
}

export async function requestConfusionMatrix(
  endpoint: string,
  signal?: AbortSignal,
): Promise<ConfusionMatrix> {
  const response = await fetch(endpoint, { signal, headers: { Accept: 'application/json' } })
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
    !('labels' in payload) ||
    !('matrix' in payload) ||
    !Array.isArray(payload.labels) ||
    payload.labels.length !== 2 ||
    !payload.labels.every((label) => typeof label === 'string') ||
    !isMatrix(payload.matrix)
  ) {
    throw new Error('Model API returned an unexpected confusion matrix.')
  }

  return payload as ConfusionMatrix
}
