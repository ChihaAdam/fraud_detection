import type { CorrelationMatrix } from '../types'
import { apiEndpoint } from './apiEndpoint'

/** Derive the correlation endpoint from the prediction endpoint set in the footer. */
export function correlationMatrixEndpoint(endpoint: string): string {
  return apiEndpoint(endpoint, 'correlation-matrix')
}

function isFiniteNumber(value: unknown): value is number {
  return typeof value === 'number' && Number.isFinite(value)
}

function isCorrelationMatrix(payload: unknown): payload is CorrelationMatrix {
  if (!payload || typeof payload !== 'object') return false

  const data = payload as Record<string, unknown>
  const { dataset, method, target, labels, matrix, target_correlations } = data

  if (
    typeof dataset !== 'string' ||
    typeof method !== 'string' ||
    typeof target !== 'string' ||
    !Array.isArray(labels) ||
    labels.length === 0 ||
    !labels.every((label) => typeof label === 'string') ||
    !Array.isArray(matrix) ||
    matrix.length !== labels.length ||
    !target_correlations ||
    typeof target_correlations !== 'object' ||
    Array.isArray(target_correlations)
  ) {
    return false
  }

  const size = labels.length
  const square = matrix.every(
    (row) =>
      Array.isArray(row) &&
      row.length === size &&
      row.every((value) => isFiniteNumber(value)),
  )

  return (
    square &&
    Object.entries(target_correlations).every(
      ([, value]) => isFiniteNumber(value),
    )
  )
}

export async function requestCorrelationMatrix(
  endpoint: string,
  signal?: AbortSignal,
): Promise<CorrelationMatrix> {
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

  if (!isCorrelationMatrix(payload)) {
    throw new Error('Model API returned an unexpected correlation matrix.')
  }

  return payload
}
