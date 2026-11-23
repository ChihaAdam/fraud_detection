import type { FeatureSelection } from '../types'
import { apiEndpoint } from './apiEndpoint'

/** Derive the feature-selection endpoint from the prediction endpoint set in the footer. */
export function featureSelectionEndpoint(endpoint: string): string {
  return apiEndpoint(endpoint, 'feature-selection')
}

function isFiniteNumber(value: unknown): value is number {
  return typeof value === 'number' && Number.isFinite(value)
}

function isFeatureScore(value: unknown): boolean {
  if (!value || typeof value !== 'object') return false

  const score = value as Record<string, unknown>
  return (
    typeof score.name === 'string' &&
    isFiniteNumber(score.anova_f) &&
    isFiniteNumber(score.mutual_information) &&
    isFiniteNumber(score.rank)
  )
}

function isFeatureSelection(payload: unknown): payload is FeatureSelection {
  if (!payload || typeof payload !== 'object') return false

  const data = payload as Record<string, unknown>
  return (
    typeof data.dataset === 'string' &&
    typeof data.target === 'string' &&
    typeof data.method === 'string' &&
    typeof data.selector === 'string' &&
    isFiniteNumber(data.k) &&
    isFiniteNumber(data.total_features) &&
    Array.isArray(data.features) &&
    data.features.length > 0 &&
    data.features.every(isFeatureScore)
  )
}

export async function requestFeatureSelection(
  endpoint: string,
  signal?: AbortSignal,
): Promise<FeatureSelection> {
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

  if (!isFeatureSelection(payload)) {
    throw new Error('Model API returned an unexpected feature selection.')
  }

  return payload
}
