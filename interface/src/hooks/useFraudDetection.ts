import { useState, type FormEvent } from 'react'
import { useOutletContext } from 'react-router-dom'
import { CLEAN_SAMPLE, DEFAULT_ENDPOINT, EMPTY_VECTOR, FRAUD_SAMPLE } from '../constants'
import { parseFeatures, previewFeatures, requestPrediction } from '../lib/predict'
import type { Phase, StatusTone, Verdict } from '../types'

export type DetectionContext = ReturnType<typeof useFraudDetection>

/** Shared detection state provided by the layout route to both pages. */
export function useDetectionContext(): DetectionContext {
  return useOutletContext<DetectionContext>()
}

export function useFraudDetection() {
  const [values, setValues] = useState<string[]>(() => [...EMPTY_VECTOR])
  const [invalid, setInvalid] = useState<number[]>([])
  const [phase, setPhase] = useState<Phase>('idle')
  const [verdict, setVerdict] = useState<Verdict | null>(null)
  const [error, setError] = useState('')
  const [stale, setStale] = useState(false)
  const [endpoint, setEndpoint] = useState(DEFAULT_ENDPOINT)

  const preview = previewFeatures(values)

  const statusText =
    phase === 'loading'
      ? 'ANALYZING'
      : phase === 'error'
        ? 'LINK ERROR'
        : verdict && !stale
          ? 'MODEL ONLINE'
          : 'STANDBY'
  const statusTone: StatusTone =
    phase === 'loading'
      ? 'busy'
      : phase === 'error'
        ? 'down'
        : verdict && !stale
          ? 'up'
          : 'idle'

  function updateValue(index: number, value: string) {
    setValues((current) => current.map((item, position) => (position === index ? value : item)))
    setInvalid((current) => current.filter((position) => position !== index))
    if (verdict) setStale(true)
  }

  function loadSample(sample: string[]) {
    setValues([...sample])
    setInvalid([])
    setError('')
    if (verdict) setStale(true)
  }

  function resetVector() {
    setValues([...EMPTY_VECTOR])
    setInvalid([])
    setError('')
    if (verdict) setStale(true)
  }

  function loadCleanSample() {
    loadSample(CLEAN_SAMPLE)
  }

  function loadFraudSample() {
    loadSample(FRAUD_SAMPLE)
  }

  function changeEndpoint(value: string) {
    setEndpoint(value)
    if (verdict) setStale(true)
  }

  async function runDetection(target: string, features: number[]) {
    const started = performance.now()
    try {
      const prediction = await requestPrediction(target, features)
      setVerdict({
        ...prediction,
        latency: Math.round(performance.now() - started),
        features,
      })
      setStale(false)
      setPhase('done')
    } catch (caught) {
      setError(
        caught instanceof Error ? caught.message : 'Unable to reach the model API.',
      )
      setPhase('error')
    }
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const target = endpoint.trim()

    if (!target) {
      setError('Enter the model API endpoint before running a check.')
      setPhase('error')
      return
    }

    const { features, invalid: badFields } = parseFeatures(values)

    if (badFields.length > 0) {
      setInvalid(badFields)
      setError(
        `${badFields.length} value${badFields.length === 1 ? '' : 's'} missing or invalid. Check the highlighted fields.`,
      )
      setPhase('error')
      return
    }

    setInvalid([])
    setError('')
    setPhase('loading')
    void runDetection(target, features)
  }

  return {
    values,
    invalid,
    preview,
    phase,
    verdict,
    error,
    stale,
    endpoint,
    statusText,
    statusTone,
    updateValue,
    loadCleanSample,
    loadFraudSample,
    resetVector,
    changeEndpoint,
    submit,
  }
}
